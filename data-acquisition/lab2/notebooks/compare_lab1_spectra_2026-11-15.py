"""Lab 1 vs Lab 2 noise spectra on the same axes and units (kPa²/Hz), same method as lab1/notebooks/lab1_spectra.ipynb.

Method (as in Lab 1): scipy.signal.welch, fs = 100 Hz, nperseg = 128, Hann window, density, mean removed.
Each signal is converted from ADC codes to kPa with its own Pa/code step:
  Lab 1 raw (13.09.2026): 141 Pa/code (Lab 1 factor 3.70 V / 4095 and the datasheet), Lab 1 notebook
  Lab 2 raw / opamp (15.11.2026): 141.9 / 119.8 Pa/code (docs/bench_session.md, 15.11 calibration)
Pump off:
  Lab 1: lab1_lsb_noise_vacuum_button_13.09.26.csv, first 272 samples (atmosphere), the Lab 1 window
  Lab 2: baseline 0-3 s of each of the 30 runs per config (pump off), Welch per run, averaged over runs
Pump on:
  Lab 1: lab1_autonomous_run_13.09.26.csv, pump-on segments (suction), slow part removed with a 25-sample
         rolling median as in Lab 1, Welch per segment (>= 128 samples), averaged
  Lab 2: plateau 4.5-6.5 s (blowing) of each run, same 25-sample rolling-median residual, averaged over runs
Note: Lab 1 pump-on is suction with the vacuum pump running; Lab 2 is blowing. Different operating point.

Run: python notebooks/compare_lab1_spectra_2026-11-15.py
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.signal import welch

LAB2 = Path(__file__).resolve().parents[1]
LAB1 = LAB2.parent / "lab1"
OUT = LAB2 / "notebooks" / "spectra_lab1_vs_lab2_2026-11-15"
FS, NPS = 100.0, 128
PA = {"lab1_raw": 3.70 / 4095 / (5 * 0.0012858) * 1000, "raw": 141.9, "opamp": 119.8}
EXCLUDED = {"eccfa9c4827c4fbe", "1317e1fd07504975", "4e34cf8a590f40ca"}


def psd(x):
    x = np.asarray(x, float)
    return welch(x - x.mean(), fs=FS, nperseg=min(NPS, len(x)))


def resid(x):
    s = pd.Series(np.asarray(x, float))
    r = (s - s.rolling(25, center=True).median()).to_numpy()
    return r[~np.isnan(r)]


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    res = {"off": {}, "on": {}}
    # Lab 1 pump off
    n = pd.read_csv(LAB1 / "data" / "lab1_lsb_noise_vacuum_button_13.09.26.csv")
    atm = n.adc.to_numpy(float)[:272] * PA["lab1_raw"] / 1000
    res["off"]["Labor 1 toores, 13.09 (atmosfäär)"] = (*psd(atm), atm.std(ddof=1) * 1000, 1)
    # Lab 1 pump on
    a = pd.read_csv(LAB1 / "data" / "lab1_autonomous_run_13.09.26.csv")
    x = a.adc.astype(float)
    noise = (x - x.rolling(25, center=True).median()).to_numpy()
    seg = (a.pump.diff() != 0).cumsum().to_numpy()
    ps, rs = [], []
    for sid in np.unique(seg):
        m = seg == sid
        r = noise[m]; r = r[~np.isnan(r)]
        if len(r) < NPS or int(a.pump[m].iloc[0]) != 1:
            continue
        r = r * PA["lab1_raw"] / 1000
        f, p = psd(r); ps.append(p); rs.append(r)
    res["on"]["Labor 1 toores, 13.09 (pump imeb)"] = (f, np.mean(ps, axis=0), np.concatenate(rs).std(ddof=1) * 1000, len(ps))
    # Lab 2
    d = pd.read_csv(LAB2 / "data" / "pulses_2026-11-15.csv")
    d = d[~d.run_id.isin(EXCLUDED)]
    for cfg, label in (("raw", "Labor 2 raw, 15.11"), ("opamp", "Labor 2 opamp, 15.11")):
        off_p, on_p, off_x, on_x = [], [], [], []
        for _, g in d[d.config == cfg].groupby("run_id"):
            t = (g.t_ms - g.t_ms.iloc[0]).to_numpy() / 1000
            kpa = g.adc.to_numpy(float) * PA[cfg] / 1000
            b = kpa[(t >= 0) & (t < 3)]
            f, p = psd(b); off_p.append(p); off_x.append(b - b.mean())
            r = resid(kpa[(t >= 4.5) & (t < 6.5)])
            f2, p2 = psd(r); on_p.append(p2); on_x.append(r)
        res["off"][label + " (pump väljas)"] = (f, np.mean(off_p, axis=0), np.concatenate(off_x).std(ddof=1) * 1000, len(off_p))
        res["on"][label + " (pump puhub)"] = (f2, np.mean(on_p, axis=0), np.concatenate(on_x).std(ddof=1) * 1000, len(on_p))

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    summary = {}
    for key, title, fn in (("off", "Müra, pump väljas", "spectra_pump_off.png"), ("on", "Müra, pump töötab (aeglane osa eemaldatud)", "spectra_pump_on.png")):
        fig, ax = plt.subplots(figsize=(8, 4.2))
        for label, (f, p, std_pa, nseg) in res[key].items():
            ax.semilogy(f, p, label=f"{label}: std {std_pa:.0f} Pa, {nseg} lõiku")
            summary[f"{key}: {label}"] = dict(noise_std_pa=round(std_pa, 1), segments=nseg,
                                               median_psd_kpa2_per_hz=float(np.median(p[1:])))
        ax.set(xlabel="Sagedus (Hz)", ylabel="PSD (kPa²/Hz)", xlim=(0, 50), title=title)
        ax.grid(True, which="both", alpha=.3); ax.legend(fontsize="small"); fig.tight_layout()
        fig.savefig(OUT / fn, dpi=120); plt.close(fig)
    (OUT / "summary.json").write_text(json.dumps(dict(method=__doc__.split("Run:")[0].strip(), pa_per_code=PA, results=summary),
                                                 indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for k, v in summary.items():
        print(f"{k:55s} std {v['noise_std_pa']:7.1f} Pa  median PSD {v['median_psd_kpa2_per_hz']:.2e}  ({v['segments']} lõiku)")


if __name__ == "__main__":
    main()
