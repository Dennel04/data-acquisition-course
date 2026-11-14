"""Guided retest of the rebuilt LM358N stage (Lab 2, circuit of 14.11.2026).

One command, three pressure holds (atmosphere, full suction, full blowing),
then a PASS/WARN/FAIL report. Works with either firmware on the AtomS3R:

- DA2_MEASURE_V1 (or its AUTO version): 100 Hz managed runs through logger.py,
  saved in the official logger CSV schema with config=opamp.
- G5 meter (src/firmware_g5meter): about 5 readings per second, used as a fallback.

No pump control, no network. Volts use the uncalibrated Lab 1 factor 3.70 V / 4095.
"""
import argparse
import csv
from datetime import datetime
import json
from pathlib import Path
import re
import statistics
import sys
import time
from types import SimpleNamespace
import uuid

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import logger  # noqa: E402  (same folder: open_atom, capture, open_csv)

VOLTS_PER_CODE = 3.70 / 4095

# Circuit as rebuilt 14.11.2026, docs/opamp_rebuild_2026-11-14.md section 6.
# Change these if the board changes.
RF_K = 10.0
RREF_K = 53.8
SENSOR_V = {"full_suction": 0.32, "atmosphere": 0.831, "full_blowing": 2.40}
TARGET_LOW_V = 0.30

CONDITIONS = [
    ("atmosphere", "ATMOSPHERE: pump off, tube and suction cup open to air."),
    ("full_suction", "FULL SUCTION: suck as hard as the setup can (pump sucking, cup blocked) and hold it."),
    ("full_blowing", "FULL BLOWING: blow as hard as the setup can and hold it."),
]

METER_LINE = re.compile(r"^(\d+),(\d+),(-?\d+\.\d+),(-?\d+\.\d+|nan|-?inf),(-?\d+\.\d+|nan|-?inf)$")
ESPRESSIF_VID = 0x303A


def expected():
    """Gain, Vref and expected Vout per condition for the current design."""
    a = 1 + RF_K / RREF_K
    vref = (a * SENSOR_V["full_suction"] - TARGET_LOW_V) / (a - 1)
    return a, vref, {k: a * v - (a - 1) * vref for k, v in SENSOR_V.items()}


def parse_meter_line(text):
    """Return (t_ms, adc) for a G5 meter CSV line, else None."""
    m = METER_LINE.match(text.strip())
    if not m:
        return None
    adc = int(m.group(2))
    return (int(m.group(1)), adc) if 0 <= adc <= 4095 else None


def stats(codes):
    """Statistics of one hold. Mean/std use the middle 60 % so the edges of the hold do not count."""
    if not codes:
        return dict(n=0)
    n = len(codes)
    mid = codes[n // 5: n - n // 5] if n >= 10 else codes
    mean = statistics.fmean(mid)
    return dict(n=n, mean_code=mean, mean_v=mean * VOLTS_PER_CODE,
                std_code=statistics.pstdev(mid) if len(mid) > 1 else 0.0,
                min_code=min(codes), max_code=max(codes),
                min_v=min(codes) * VOLTS_PER_CODE, max_v=max(codes) * VOLTS_PER_CODE)


def evaluate(results, timing_ok=None):
    """results: condition -> stats(). Returns list of (status, check, detail)."""
    a, _, exp = expected()
    out = []
    s = {k: results.get(k, {}) for k, _ in CONDITIONS}
    short = [k for k, v in s.items() if v.get("n", 0) < 10]
    if short:
        out.append(("FAIL", "Enough samples", "too few readings in: " + ", ".join(short)))
        return out
    suc, atm, blo = s["full_suction"]["mean_v"], s["atmosphere"]["mean_v"], s["full_blowing"]["mean_v"]

    ok = suc + 0.2 <= atm and atm + 0.2 <= blo
    out.append(("PASS" if ok else "FAIL", "Output follows pressure",
                f"suction {suc:.3f} V < atmosphere {atm:.3f} V < blowing {blo:.3f} V"
                + ("" if ok else " (expected at least 0.2 V between each)")))

    span = blo - suc
    out.append(("PASS" if span >= 1.5 else "FAIL", "Output range",
                f"{span:.2f} V from full suction to full blowing (need >= 1.5 V, design {exp['full_blowing'] - exp['full_suction']:.2f} V)"))

    low = s["full_suction"]
    ok = low["min_code"] >= 60 and suc >= 0.10
    out.append(("PASS" if ok else "FAIL", "Not stuck at the low end",
                f"full suction min {low['min_v']:.3f} V, mean {suc:.3f} V (need min >= 0.054 V and mean >= 0.10 V)"))

    high = s["full_blowing"]
    ok = high["max_v"] <= 3.0 and high["max_code"] < 4095
    out.append(("PASS" if ok else "FAIL", "Safe for G5 at the high end",
                f"full blowing max {high['max_v']:.3f} V (need <= 3.0 V)"))

    noise = s["atmosphere"]["std_code"]
    out.append(("PASS" if noise <= 10 else "WARN", "Noise at atmosphere",
                f"{noise:.1f} ADC codes = {noise * VOLTS_PER_CODE * 1000:.1f} mV standard deviation (aim <= 10 codes)"))

    for k, _ in CONDITIONS:
        d = s[k]["mean_v"] - exp[k]
        out.append(("PASS" if abs(d) <= 0.25 else "WARN", f"Close to design: {k}",
                    f"{s[k]['mean_v']:.3f} V vs {exp[k]:.3f} V expected ({d:+.3f} V, allowed +-0.25 V)"))

    sensor_span = SENSOR_V["full_blowing"] - SENSOR_V["full_suction"]
    implied = span / sensor_span
    ok = abs(implied - a) / a <= 0.15
    out.append(("PASS" if ok else "WARN", "Implied gain",
                f"{implied:.3f} vs design {a:.3f}; assumes the pump reached the 14.11 sensor range {SENSOR_V['full_suction']}-{SENSOR_V['full_blowing']} V"))

    if timing_ok is not None:
        out.append(("PASS" if timing_ok else "WARN", "100 Hz timing (DA2 firmware)",
                    "all runs on time" if timing_ok else "at least one run had sample gaps; see .runs.jsonl"))
    return out


def find_ports():
    from serial.tools import list_ports
    return [p.device for p in list_ports.comports()
            if p.vid == ESPRESSIF_VID and logger.local_port(p.device)]


def choose_port(given, ask=input):
    if given:
        return given
    ports = find_ports()
    if len(ports) == 1:
        return ports[0]
    if not ports:
        raise SystemExit("No AtomS3R found. Plug it in with a USB-C data cable and run again.\n"
                         "If it still is not found, run with --port COM5 (Windows) or --port /dev/cu.usbmodemXXXX (macOS).")
    for i, p in enumerate(ports, 1):
        print(f"  {i}) {p}")
    pick = ask("Several Atoms found. Type the number of the one on the op-amp board: ").strip()
    return ports[int(pick) - 1]


def detect_firmware(port, seconds=3.0, clock=time.monotonic):
    """'meter' if G5 meter lines arrive, otherwise 'da2' (V1 is silent until measure_start)."""
    end = clock() + seconds
    while clock() < end:
        raw = port.readline(513)
        if not raw:
            continue
        text = raw.decode("ascii", "replace")
        if parse_meter_line(text):
            return "meter"
        if text.startswith(("# AUTO", "# DA2")):
            return "da2"
    return "da2"


class Tee:
    def __init__(self, writer):
        self.writer, self.rows = writer, []

    def writerow(self, row):
        self.writer.writerow(row)
        self.rows.append(row)


def capture_meter(port, writer, handle, condition, trial, duration, clock=time.monotonic):
    codes = []
    port.reset_input_buffer()
    end = clock() + duration
    while clock() < end:
        hit = parse_meter_line(port.readline(513).decode("ascii", "replace"))
        if hit:
            codes.append(hit[1])
            writer.writerow(dict(t_ms=hit[0], adc=hit[1], voltage_v=f"{hit[1] * VOLTS_PER_CODE:.4f}",
                                 condition=condition, trial=trial, source="g5meter"))
            handle.flush()
    return codes


def ask_float(prompt, ask=input):
    text = ask(prompt).strip().replace(",", ".")
    if not text:
        return None
    try:
        v = float(text)
    except ValueError:
        print("  Not a number, skipped.")
        return None
    if not 0 <= v <= 3.1:
        print("  Outside 0..3.1 V, skipped. Disconnect G5 and write the value in the bench notes.")
        return None
    return v


def write_report(outdir, info, results, checks):
    a, vref, exp = expected()
    verdict = "FAIL" if any(c[0] == "FAIL" for c in checks) else ("PASS with warnings" if any(c[0] == "WARN" for c in checks) else "PASS")
    lines = [f"# Op-amp retest {info['started']}", "",
             f"**Verdict: {verdict}**", "",
             f"- Port: `{info['port']}`, firmware: `{info['firmware']}`",
             f"- Design: Rf {RF_K} kOhm, Rref {RREF_K} kOhm, gain {a:.3f}, Vref {vref:.3f} V",
             "- Volts are uncalibrated (Lab 1 factor 3.70 V / 4095). Pressure is not converted.", "",
             "| Condition | Mean V | Min V | Max V | Noise mV | Samples | Expected V |",
             "|---|---|---|---|---|---|---|"]
    for k, _ in CONDITIONS:
        r = results.get(k, {})
        if r.get("n"):
            lines.append(f"| {k} | {r['mean_v']:.3f} | {r['min_v']:.3f} | {r['max_v']:.3f} | "
                         f"{r['std_code'] * VOLTS_PER_CODE * 1000:.1f} | {r['n']} | {exp[k]:.3f} |")
        else:
            lines.append(f"| {k} | - | - | - | - | 0 | {exp[k]:.3f} |")
    lines += ["", "| Result | Check | Detail |", "|---|---|---|"]
    lines += [f"| {s} | {n} | {d} |" for s, n, d in checks]
    if info.get("dmm_v") is not None:
        lines += ["", f"Multimeter at the G5 node, atmosphere: {info['dmm_v']} V "
                      f"(ADC mean {results['atmosphere'].get('mean_v', float('nan')):.3f} V)."]
    if info.get("errors"):
        lines += ["", "Errors:"] + [f"- {e}" for e in info["errors"]]
    lines += ["", "Files: `opamp_retest.csv`, `summary.json`" + (", `opamp_retest.csv.runs.jsonl`" if info["firmware"] == "da2" else "")]
    (outdir / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (outdir / "summary.json").write_text(json.dumps(dict(info=info, results=results, checks=checks, verdict=verdict),
                                                    indent=2, allow_nan=False), encoding="utf-8")
    return verdict


def main(argv=None, ask=input):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--port", help="only needed if the Atom is not found automatically")
    p.add_argument("--duration", type=float, default=8, help="seconds per hold (default 8)")
    p.add_argument("--out", type=Path, help="output folder (default lab2/data/opamp_retest_<date>)")
    a = p.parse_args(argv)
    if not 3 <= a.duration <= 60:
        p.error("duration must be 3..60 s")

    amp, vref, exp = expected()
    print("\nOp-amp stage retest (Lab 2)")
    print(f"Design: gain {amp:.3f}, Vref {vref:.3f} V. Expected at G5: "
          + ", ".join(f"{k} {v:.2f} V" for k, v in exp.items()))
    print("You will hold three pressures for", a.duration, "seconds each. Nothing else to type.\n")

    port_name = choose_port(a.port, ask)
    if ask("Was the stage output checked with a multimeter (<= 3.0 V at full blowing) before G5 was connected? [y/N] ").strip().lower() not in ("y", "yes", "j", "jah", "d", "da"):
        print("Stop. Check Vout at full blowing with a multimeter first (G5 disconnected).")
        return 2

    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    outdir = a.out or HERE.parents[1] / "data" / f"opamp_retest_{stamp}"
    outdir.mkdir(parents=True, exist_ok=False)
    info = dict(started=datetime.now().isoformat(timespec="seconds"), port=port_name,
                design=dict(rf_k=RF_K, rref_k=RREF_K, sensor_v=SENSOR_V, target_low_v=TARGET_LOW_V),
                duration_s=a.duration, errors=[], dmm_v=None)
    results, timing = {}, []

    port = logger.open_atom(port_name)
    try:
        info["firmware"] = mode = detect_firmware(port)
        print(f"Atom on {port_name}, firmware: {'G5 meter (about 5 readings/s)' if mode == 'meter' else 'DA2 measurement (100 Hz)'}\n")
        csv_path = outdir / "opamp_retest.csv"
        if mode == "da2":
            handle, writer = logger.open_csv(csv_path, False)
        else:
            handle = csv_path.open("w", newline="", encoding="utf-8")
            writer = csv.DictWriter(handle, fieldnames=["t_ms", "adc", "voltage_v", "condition", "trial", "source"])
            writer.writeheader()
        run_log = Path(str(csv_path) + ".runs.jsonl")
        try:
            for trial, (cond, text) in enumerate(CONDITIONS, 1):
                print(f"[{trial}/3] {text}")
                dmm = None
                if cond == "atmosphere":
                    dmm = ask_float("  Optional: multimeter reading at the G5 node in volts (Enter to skip): ", ask)
                    info["dmm_v"] = dmm
                ask("  Press Enter when the pressure is steady...")
                print(f"  Recording {a.duration:g} s, keep holding...")
                if mode == "da2":
                    tee = Tee(writer)
                    args = SimpleNamespace(config="opamp", condition=cond, trial=trial, duration=a.duration, dmm_v=dmm)
                    summary = logger.capture(port, tee, handle, args, uuid.uuid4().hex[:16])
                    with run_log.open("a", encoding="utf-8") as f:
                        f.write(json.dumps(summary, allow_nan=False) + "\n")
                    if summary.get("error"):
                        info["errors"].append(f"{cond}: {summary['error']}")
                        print("  Error:", summary["error"])
                    timing.append(bool(summary.get("timing_ok")))
                    codes = [r["adc"] for r in tee.rows]
                else:
                    codes = capture_meter(port, writer, handle, cond, trial, a.duration)
                results[cond] = stats(codes)
                r = results[cond]
                print(f"  {r['mean_v']:.3f} V mean, {r['n']} readings (expected {exp[cond]:.2f} V)\n" if r.get("n")
                      else "  No readings received.\n")
        finally:
            handle.close()
    finally:
        port.close()

    if mode == "da2" and not any(results.get(k, {}).get("n") for k, _ in CONDITIONS):
        info["errors"].append("No data. The Atom may run firmware this test does not know. "
                              "Put back DA2_MEASURE_V1 or the G5 meter (see docs/opamp_rebuild_2026-11-14.md).")
    checks = evaluate(results, all(timing) if timing else None)
    verdict = write_report(outdir, info, results, checks)
    print("Result:")
    for s, n, d in checks:
        print(f"  {s:4}  {n}: {d}")
    print(f"\nVerdict: {verdict}")
    print(f"Saved in {outdir}\nSend that folder (or commit it) so the team can see the result.")
    return 1 if verdict == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
