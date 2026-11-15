"""Build the analyze.py plan for the 15.11.2026 pulse series (data/pulses_2026-11-15.csv).

Calibration = ADC code -> G5 volts from multimeter points, then MPX5700AP datasheet transfer function.
No pressure reference was used; this is the "datasheet model" route from notebooks/README.md.

Multimeter points (15.11.2026), each paired with the ADC level of the same state:
  raw   atmosphere     sensor pin 1  0.837 V  <-> raw baseline mean 944.3 codes (30 runs, 0-3 s)
  raw   full blowing   sensor row 22 2.43 V   <-> raw peak 2690 codes (assumed the same pressure; +-35 codes)
  opamp atmosphere     G5 node       0.865 V  <-> opamp baseline mean 978.4 codes
ADC line from the two raw points: V = Q * code + B_RAW. The opamp run uses the same ADC slope
(same pin, same firmware) and its own offset from its atmosphere point.
Datasheet (MPX5700AP): Vout = Vs * (0.0012858 * P_kPa + 0.04), Vs = 5.0 V (measured 15.11).
Stage (opamp): V_G5 = A * Vsensor - (A - 1) * Vref, A = 1 + 10/54 (Rref measured ~54 kOhm), Vref = 0.686 V
(calculated from the 15.11 multimeter points).

Run: python notebooks/make_plan_2026-11-15.py  -> writes notebooks/plan_2026-11-15.json
"""
import json
from pathlib import Path

LAB2 = Path(__file__).resolve().parents[1]
RUNS = LAB2 / "data" / "pulses_2026-11-15.csv.runs.jsonl"
OUT = LAB2 / "notebooks" / "plan_2026-11-15.json"
EXCLUDED = {"eccfa9c4827c4fbe", "1317e1fd07504975", "4e34cf8a590f40ca"}  # bench note 15.11: failed, redone

VS, SENS, OFFSET_RATIO = 5.0, 0.0012858, 0.04
A, VREF = 1 + 10 / 54, 0.686
RAW_PTS = [(944.3, 0.837), (2690.0, 2.43)]
OPAMP_PT = (978.4, 0.865)

Q = (RAW_PTS[1][1] - RAW_PTS[0][1]) / (RAW_PTS[1][0] - RAW_PTS[0][0])  # V per code
B_RAW = RAW_PTS[0][1] - Q * RAW_PTS[0][0]
B_OPAMP = OPAMP_PT[1] - Q * OPAMP_PT[0]


def pa_line(volts_per_code, volts_offset, stage_gain=1.0, stage_offset=0.0):
    """Return (Pa per code, Pa offset) so that P_Pa = K * code + C (absolute pressure)."""
    # sensor volts = (V_G5 + stage_offset) / stage_gain
    k_v = volts_per_code / stage_gain
    c_v = (volts_offset + stage_offset) / stage_gain
    return k_v / (VS * SENS) * 1000, (c_v / VS - OFFSET_RATIO) / SENS * 1000


def main():
    k_raw, c_raw = pa_line(Q, B_RAW)
    k_op, c_op = pa_line(Q, B_OPAMP, A, (A - 1) * VREF)
    src = ("docs/bench_session.md 15.11.2026 + multimeter 15.11 (sensor pin 1 0.837 V, row 22 2.43 V at full blowing, "
           "G5 0.865 V); ADC line from the two raw points; MPX5700AP datasheet Vout = Vs(0.0012858 P + 0.04), Vs 5.0 V")
    runs = [json.loads(line) for line in RUNS.read_text(encoding="utf-8").splitlines() if line.strip()]
    plan = {"calibration": {}, "windows": {}, "spectrum_pairs": []}
    for r in runs:
        if r["run_id"] in EXCLUDED:
            continue
        if r["config"] == "raw":
            entry = dict(config="raw", source=src, pa_per_code=k_raw, offset_pa=c_raw, adc_range=[900, 2700])
        else:
            entry = dict(config="opamp", source=src + f"; stage A {A:.4f}, Vref {VREF} V; ADC slope from raw points, "
                         "codes above 2690 extrapolated", pa_per_code=k_op, offset_pa=c_op, adc_range=[900, 3100])
        plan["calibration"][r["run_id"]] = entry
        plan["windows"][r["run_id"]] = {"baseline_s": [0.0, 3.0], "plateau_s": [4.5, 6.5]}
    ids = {(r["config"], r["trial"]): r["run_id"] for r in runs if r["run_id"] not in EXCLUDED}
    proto = "15.11.2026 pulse_series.py: pump off 0-3 s, blow (DO1) 3-7 s, off 7-10 s, 100 Hz, same day, same tube with small leak"
    for label, win in (("baseline, pump off", [0.0, 3.0]), ("plateau, pump blowing", [4.5, 6.5])):
        plan["spectrum_pairs"].append(dict(raw_run=ids[("raw", 1)], opamp_run=ids[("opamp", 1)], raw_s=win, opamp_s=win,
                                           protocol=f"{proto}; trial 1; window {label}"))
    OUT.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(f"ADC: {Q * 1000:.4f} mV/code, offset raw {B_RAW * 1000:+.1f} mV, opamp {B_OPAMP * 1000:+.1f} mV")
    print(f"raw:   {k_raw:.1f} Pa/code, offset {c_raw / 1000:.2f} kPa")
    print(f"opamp: {k_op:.1f} Pa/code, offset {c_op / 1000:.2f} kPa")
    print(f"atmosphere: raw {(k_raw * 944.3 + c_raw) / 1000:.1f} kPa, opamp {(k_op * 978.4 + c_op) / 1000:.1f} kPa (absolute)")
    print(f"{len(plan['calibration'])} runs, {len(plan['spectrum_pairs'])} spectrum pairs -> {OUT}")


if __name__ == "__main__":
    main()
