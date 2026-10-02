"""Summarise a logger.py / pick_cycles.py CSV: the numbers part 4 asks for.

    python analyze_run.py ../../data/<run>.csv

Prints run length, sample rate, pressure range, pump starts, run/idle times,
starts per minute and duty cycle. If <run>.events.csv exists (pick_cycles.py),
also one line per pick cycle.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from statistics import mean


def load(path: Path) -> list[tuple[int, float, int]]:
    rows = []
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            try:
                rows.append((int(float(r["t_ms"])), float(r["p_kpa"]), int(float(r["pump"]))))
            except (TypeError, ValueError):
                continue
    return rows


def runs(rows, value):
    """(start_ms, end_ms) of every stretch where pump == value."""
    out, start = [], None
    for t, _, pump in rows:
        if pump == value and start is None:
            start = t
        elif pump != value and start is not None:
            out.append((start, t))
            start = None
    if start is not None:
        out.append((start, rows[-1][0]))
    return out


def fmt(xs):
    return f"{min(xs):.1f} / {mean(xs):.1f} / {max(xs):.1f} s" if xs else "-"


def main() -> None:
    path = Path(sys.argv[1])
    rows = load(path)
    if len(rows) < 2:
        raise SystemExit("no data rows")
    t0, t1 = rows[0][0], rows[-1][0]
    dur = (t1 - t0) / 1000
    ps = [p for _, p, _ in rows]
    on = runs(rows, 1)
    # idle stretches between two starts only (not the lead-in / tail)
    off = [(a, b) for a, b in runs(rows, 0) if a > t0 and b < t1]
    on_s = [(b - a) / 1000 for a, b in on]
    off_s = [(b - a) / 1000 for a, b in off]

    print(f"file           {path.name}")
    print(f"rows           {len(rows)}  over {dur:.1f} s  ->  {len(rows) / dur:.1f} Hz")
    print(f"pressure       min {min(ps):.2f}  max {max(ps):.2f} kPa")
    print(f"pump starts    {len(on)}  ->  {len(on) / (dur / 60):.2f} per min")
    print(f"run time       min/avg/max {fmt(on_s)}")
    print(f"idle time      min/avg/max {fmt(off_s)}")
    print(f"duty cycle     {100 * sum(on_s) / dur:.1f} %  (pump on {sum(on_s):.1f} s of {dur:.1f} s)")

    ev_path = path.with_suffix(".events.csv")
    if not ev_path.exists():
        return
    with open(ev_path, newline="") as f:
        events = list(csv.DictReader(f))
    print(f"\nper cycle (from {ev_path.name}):")
    print(" cyc  len_s  grip_s  pump_on_s  duty%   min_kPa  carried")
    cycles = sorted({int(e["cycle"]) for e in events})
    for c in cycles:
        ce = [e for e in events if int(e["cycle"]) == c and e["atom_t_ms"]]
        if not ce:
            continue
        a, b = int(ce[0]["atom_t_ms"]), int(ce[-1]["atom_t_ms"])
        phase_t = {e["phase"]: int(e["atom_t_ms"]) for e in ce}
        grip = ((phase_t.get("gripped", b) - phase_t.get("suction", a)) / 1000) if "suction" in phase_t else float("nan")
        seg = [r for r in rows if a <= r[0] <= b]
        on_ms = sum(10 for r in seg if r[2] == 1)  # 10 ms per row
        carried = "yes" if "carried" in phase_t else ("NO" if "dropped?" in phase_t else "-")
        L = (b - a) / 1000
        print(f" {c:3d}  {L:5.1f}  {grip:6.2f}  {on_ms / 1000:9.1f}  {100 * on_ms / 1000 / L if L else 0:5.1f}"
              f"  {min(r[1] for r in seg) if seg else float('nan'):8.2f}  {carried}")


if __name__ == "__main__":
    main()
