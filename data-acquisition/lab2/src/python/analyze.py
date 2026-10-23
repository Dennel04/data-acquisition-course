"""Offline DA2 CSV analysis. Never opens serial ports or supplies calibration."""
import argparse
import csv
import json
import math
from pathlib import Path
import re
import statistics

from logger import FIELDS, Rows


def load(paths):
    """Reuse logger validation; retain independent clocks and metadata per run."""
    runs, captures = {}, {}
    for path in paths:
        sidecar = Path(str(path)+".runs.jsonl")
        if sidecar.exists():
            for line in sidecar.read_text().splitlines():
                record = json.loads(line)
                run_id = record["run_id"]
                if run_id in captures:
                    raise ValueError("duplicate run metadata")
                captures[run_id] = record
        with Path(path).open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != FIELDS:
                raise ValueError(f"{path}: CSV header differs from logger.FIELDS")
            for row in reader:
                if None in row or any(v is None for v in row.values()):
                    raise ValueError(f"{path}: incomplete CSV row")
                run = row["run_id"]
                if not re.fullmatch(r"[0-9a-f]{16}", run):
                    raise ValueError("invalid run_id")
                if not re.fullmatch(r"[a-z0-9_-]{1,40}", row["condition"]):
                    raise ValueError("invalid condition")
                trial = int(row["trial"])
                if not 1 <= trial <= 100000:
                    raise ValueError("invalid trial")
                # Current logger deliberately has no pressure/voltage conversion.
                if any(row[k] for k in ("p_kpa", "voltage_v", "pump")):
                    raise ValueError("expected uncalibrated logger CSV: p_kpa/voltage_v/pump must be blank")
                dmm = row["dmm_reference_v"]
                if dmm and (not math.isfinite(float(dmm)) or not 0 <= float(dmm) <= 3.1):
                    raise ValueError("invalid DMM reference")
                if bool(dmm) != bool(row["dmm_recorded_utc"]):
                    raise ValueError("DMM value/timestamp must occur together")
                meta = (row["config"], row["condition"], trial, dmm, row["dmm_recorded_utc"])
                if run not in runs:
                    runs[run] = dict(validator=Rows(row["config"], run), meta=meta,
                                     t=[], adc=[], sources=[])
                item = runs[run]
                if item["meta"] != meta:
                    raise ValueError(f"{run}: metadata changed inside run")
                obj = dict(t=int(row["t_ms"]), adc=int(row["adc"]), p=None, pump=None,
                           config=row["config"], run=run, seq=int(row["seq"]), missed=int(row["missed"]))
                checked = item["validator"].accept(obj)
                if row["adc_clipped"] != str(checked["adc_clipped"]):
                    raise ValueError("adc_clipped disagrees with ADC code")
                item["t"].append(item["validator"].elapsed / 1000)
                item["adc"].append(obj["adc"])
                if str(path) not in item["sources"]:
                    item["sources"].append(str(path))
    for run, item in runs.items():
        capture = captures.get(run, {})
        item["capture_complete"] = (capture.get("status") == "complete" and
                                    capture.get("rows") == len(item["adc"]) and
                                    capture.get("config") == item["meta"][0] and
                                    capture.get("timing_ok") is True and not capture.get("error"))
        item["capture"] = capture or None
    return runs


def stats(values):
    mean = statistics.mean(values)
    return dict(n=len(values), mean=mean,
                std_sample=statistics.stdev(values) if len(values) > 1 else None,
                minimum=min(values), maximum=max(values), peak_to_peak=max(values)-min(values),
                rms_about_mean=math.sqrt(statistics.mean((v-mean)**2 for v in values)))


def calibration(entry, adc, config):
    if entry.get("config") != config or not entry.get("source", "").strip():
        raise ValueError("calibration needs matching config and evidence source")
    slope, offset = float(entry["pa_per_code"]), float(entry["offset_pa"])
    low, high = entry["adc_range"]
    if (not all(math.isfinite(x) for x in (slope, offset, low, high)) or slope == 0
            or not 0 <= low < high <= 4095 or min(adc) < low or max(adc) > high):
        raise ValueError("invalid calibration or samples outside verified adc_range")
    return [slope*x+offset for x in adc], abs(slope)


def window(item, bounds):
    start, end = bounds
    if not (math.isfinite(start) and math.isfinite(end) and
            0 <= start < end <= item["t"][-1]):
        raise ValueError("window must lie inside run, in seconds from first sample")
    indices = [i for i, t in enumerate(item["t"]) if start <= t < end]
    if len(indices) < 2:
        raise ValueError("window needs at least two samples")
    return indices


def snr(item, selection, pressure):
    baseline, plateau = selection["baseline_s"], selection["plateau_s"]
    if max(baseline[0], plateau[0]) < min(baseline[1], plateau[1]):
        raise ValueError("baseline/plateau windows overlap")
    base = [pressure[i] for i in window(item, baseline)]
    top = [pressure[i] for i in window(item, plateau)]
    signal = statistics.mean(top)-statistics.mean(base)
    noise = statistics.stdev(top)
    return dict(signal_pa=signal, plateau_noise_std_pa=noise,
                snr_db=20*math.log10(abs(signal)/noise) if signal and noise else None,
                note="zero signal/noise: SNR undefined" if not signal or not noise else "",
                baseline_s=baseline, plateau_s=plateau)


def spectrum(values, fs):
    """One-sided mean-subtracted Hann periodogram, density in kPa²/Hz."""
    import numpy as np
    x = np.asarray(values, dtype=float) / 1000
    if len(x) < 8:
        raise ValueError("spectrum needs at least eight samples")
    w = np.hanning(len(x))
    power = abs(np.fft.rfft((x-x.mean())*w))**2 / (fs*(w*w).sum())
    power[1:-1 if len(x) % 2 == 0 else None] *= 2
    return np.fft.rfftfreq(len(x), 1/fs), power


def compare(runs, pair, calibrated):
    raw, opamp = pair["raw_run"], pair["opamp_run"]
    a, b = runs[raw], runs[opamp]
    if a["meta"][0] != "raw" or b["meta"][0] != "opamp":
        raise ValueError("spectrum pair must name raw and opamp runs")
    if a["meta"][1:3] != b["meta"][1:3] or not pair.get("protocol", "").strip():
        raise ValueError("comparison needs matching condition/trial and explicit protocol")
    indices = [window(a, pair["raw_s"]), window(b, pair["opamp_s"])]
    if len(indices[0]) != len(indices[1]):
        raise ValueError("spectra need identical sample counts and frequency axes")
    curves = []
    periods = []
    for run, item, ix in zip((raw, opamp), (a, b), indices):
        clock = item["validator"]
        if (not item["capture_complete"] or not clock.summary()["timing_ok"] or
                0 in item["adc"] or 4095 in item["adc"]):
            raise ValueError("spectra need valid timing and no clipped codes")
        gaps = clock.gaps
        if min(gaps) != max(gaps):
            raise ValueError("nonuniform sampling: no automatic interpolation/FFT")
        periods.append(gaps[0])
        curves.append(spectrum([calibrated[run][i] for i in ix], 1000/gaps[0]))
    if periods[0] != periods[1]:
        raise ValueError("spectra need identical sampling periods")
    return curves


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", nargs="*", type=Path)
    parser.add_argument("--out", type=Path, required=True, help="new output directory (never overwritten)")
    parser.add_argument("--plan", type=Path, help="JSON: calibration per run, windows, spectrum_pairs")
    args = parser.parse_args(argv)
    try:
        if not args.csv or any(not p.is_file() for p in args.csv):
            print("Päris CSV-andmed puuduvad. Anna logija olemasolevad CSV-failid; tulemusi ei loodud.")
            return 2
        runs = load(args.csv)
        if not runs:
            print("CSV-s pole mõõteridu; tulemusi ei loodud.")
            return 2
        plan = json.loads(args.plan.read_text()) if args.plan else {}
        for section in ("calibration", "windows"):
            unknown = set(plan.get(section, {}))-set(runs)
            if unknown:
                raise ValueError(f"{section}: unknown run IDs {sorted(unknown)}")
        report, calibrated = {}, {}
        for run, item in runs.items():
            config, condition, trial, dmm, recorded = item["meta"]
            result = dict(config=config, condition=condition, trial=trial,
                          sources=item["sources"], timing=item["validator"].summary(),
                          capture_complete=item["capture_complete"], capture=item["capture"],
                          adc=stats(item["adc"]), clipped_samples=sum(v in (0,4095) for v in item["adc"]),
                          dmm_reference_v=dmm or None, dmm_recorded_utc=recorded or None,
                          note="Whole-run variation is not plateau noise unless the run is stationary.")
            result["timing"]["target_hz"] = 100
            rate = result["timing"]["rate_hz"]
            result["timing"]["error_percent"] = (rate-100) if rate is not None else None
            if run in plan.get("calibration", {}):
                entry = plan["calibration"][run]
                pressure, step = calibration(entry, item["adc"], config)
                calibrated[run] = pressure
                result.update(pa_per_adc_step=step, calibration=entry)
            else:
                result["calibration_todo"] = "Verified per-run Pa/code calibration and range required. DMM alone is insufficient."
            if run in plan.get("windows", {}):
                if (run not in calibrated or not item["capture_complete"] or
                        not result["timing"]["timing_ok"] or result["clipped_samples"]):
                    raise ValueError("SNR needs calibration, valid timing and no clipped codes")
                result["snr"] = snr(item, plan["windows"][run], calibrated[run])
            else:
                result["snr_todo"] = "Select steady non-overlapping baseline/plateau windows after inspecting real data."
            report[run] = result
        comparisons = [compare(runs, pair, calibrated) for pair in plan.get("spectrum_pairs", [])]
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        args.out.mkdir(parents=True, exist_ok=False)
        fig, axes = plt.subplots(2, 1, sharey=True, squeeze=False)
        for run, item in runs.items():
            ax = axes[0 if item["meta"][0] == "raw" else 1, 0]
            ax.plot(item["t"], item["adc"], label=run)
        for i, config in enumerate(("raw", "opamp")):
            axes[i, 0].set(title=config, xlabel="Time from run start (s)", ylabel="ADC code")
            if axes[i, 0].lines:
                axes[i, 0].legend(fontsize="small")
        fig.tight_layout(); fig.savefig(args.out/"adc_time.png"); plt.close(fig)
        for i, curves in enumerate(comparisons):
            fig, ax = plt.subplots()
            for label, (freq, power) in zip(("raw", "opamp"), curves):
                ax.plot(freq, power, label=label)
            ax.set(xlabel="Frequency (Hz)", ylabel="PSD (kPa²/Hz)")
            ax.legend(); fig.tight_layout(); fig.savefig(args.out/f"spectra_{i+1}.png"); plt.close(fig)
        payload = dict(runs=report, spectrum_pairs=plan.get("spectrum_pairs", []),
                       spectrum_method="Mean-subtracted Hann one-sided periodogram, no resampling",
                       spectrum_todo="No spectrum comparison requested" if not comparisons else None)
        (args.out/"summary.json").write_text(json.dumps(payload, indent=2, allow_nan=False)+"\n")
        print(f"Analüüs: {args.out}; jooksud: {len(runs)}. Füüsilise töö tulemusi hinnatakse koos katseprotokolliga.")
        return 0
    except (ValueError, KeyError, TypeError, OSError, ImportError) as error:
        print(f"Analüüs peatatud: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
