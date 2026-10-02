"""Data Acquisition Lab 1, part 4: hold the glass in the air with the Atom deciding.

Grip on the table with the pump forced on (the napp leaks while the glass lies
on the table, 02.10.26: -65 -> 0 kPa in ~3 s), lift, then hand the pump to the
Atom's band so it behaves like the factory smart box. Logs the hold, lowers,
releases with a short blow.

    python hold_test.py --port COM4 --csv-out ../../data/<run>.csv
"""

from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path

import requests

from logger import Mg400Pump, check_zero, open_atom
from pick_cycles import AtomLink


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--port", required=True)
    p.add_argument("--csv-out", type=Path, required=True)
    p.add_argument("--mg400-url", default="http://127.0.0.1:8000")
    p.add_argument("--lift", type=float, default=10.0, help="mm")
    p.add_argument("--hold", type=float, default=120.0, help="s")
    p.add_argument("--on-kpa", type=float, default=-40)
    p.add_argument("--off-kpa", type=float, default=-60)
    p.add_argument("--min-off-ms", type=int, default=15000)
    p.add_argument("--max-cycles-per-min", type=int, default=4)
    p.add_argument("--speed", type=int, default=5)
    a = p.parse_args()
    if not 1 <= a.speed <= 5:
        raise SystemExit("--speed must be 1..5 %")

    U = a.mg400_url.rstrip("/")

    def post(path, body=None):
        r = requests.post(U + path, json=body or {}, timeout=3).json()
        if not r.get("ok"):
            raise RuntimeError(f"{path}: {r}")

    def status():
        return requests.get(U + "/api/status", timeout=3).json()

    def go_z(z, timeout=30.0):
        s = status()
        x, y, r = s["pose"][0], s["pose"][1], s["pose"][3]
        post("/api/move", {"x": x, "y": y, "z": z, "r": r})
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            s = status()
            if s.get("limit_warning") or s.get("error"):
                raise RuntimeError(f"robot: {s.get('limit_warning') or s.get('alarm_ids')}")
            if abs(s["pose"][2] - z) < 0.3:
                return
            time.sleep(0.05)
        raise RuntimeError(f"z {z} not reached")

    s = status()
    if not s.get("enabled"):
        raise SystemExit("robot not enabled")
    z_table = s["pose"][2]
    post("/api/speed", {"ratio": a.speed})
    post("/api/smoothness", {"secs": 1.5})
    post("/api/sync")

    a.csv_out.parent.mkdir(parents=True, exist_ok=True)
    events_path = a.csv_out.with_suffix(".events.csv")
    pump = Mg400Pump(U, dry_run=False)
    t0 = time.monotonic()
    with open_atom(a.port, 115200) as ser, open(events_path, "w", newline="") as ef:
        check_zero(ser)
        link = AtomLink(ser, pump, a.csv_out)
        link.start()
        ev = csv.writer(ef)
        ev.writerow(["wall_s", "atom_t_ms", "cycle", "phase", "p_kpa"])

        def event(phase):
            ev.writerow([round(time.monotonic() - t0, 3), link.last_t, 1, phase, link.last_p])
            ef.flush()
            print(f"  {time.monotonic() - t0:6.1f} s  {phase:<12} p={link.last_p}")

        try:
            link.send({"cmd": "limits", "minOffMs": a.min_off_ms, "maxCyclesPerMin": a.max_cycles_per_min})
            # grip: pump forced on while on the table -- suction starts when p is
            # weaker (higher) than "on", so "on" = -149 starts it at any reading
            # (the glass may still be stuck at -43 from before, which is already
            # stronger than -40 and would keep the pump off), "off" out of reach
            link.send({"cmd": "band", "on": -149, "off": -150})
            link.send({"cmd": "mode", "mode": "suction"})
            event("suction")
            end = time.monotonic() + 8
            while time.monotonic() < end and (link.last_p is None or link.last_p > a.off_kpa):
                time.sleep(0.02)
            if link.last_p is None or link.last_p > a.off_kpa:
                raise RuntimeError("no grip: vacuum never reached the off threshold")
            event("gripped")
            go_z(z_table + a.lift)
            event("lifted")
            # in the air: the Atom's own band, like the smart box
            link.send({"cmd": "band", "on": a.on_kpa, "off": a.off_kpa})
            event("atom-band")
            end = time.monotonic() + a.hold
            while time.monotonic() < end:
                if link.lost.is_set():
                    raise RuntimeError("Atom USB lost")
                time.sleep(0.2)
            event("hold-done")
            # keep the pump on for the way down, then release
            link.send({"cmd": "band", "on": -149, "off": -150})
            link.send({"cmd": "mode", "mode": "off"})      # mode change = commanded start
            link.send({"cmd": "mode", "mode": "suction"})
            go_z(z_table)
            event("at-table")
            link.send({"cmd": "band", "on": 5, "off": 20})
            link.send({"cmd": "mode", "mode": "blow"})
            time.sleep(0.5)
            link.send({"cmd": "mode", "mode": "off"})
            event("released")
        except KeyboardInterrupt:
            print("interrupted")
        except Exception as exc:
            print(f"STOP: {exc}")
            requests.post(U + "/api/stop", timeout=3)
        finally:
            try:
                link.send({"cmd": "stop"})
            except Exception:
                pass
            pump.set_mode("off", force=True)
            pump.flush()
            requests.post(U + "/api/speed", json={"ratio": 10}, timeout=3)
            requests.post(U + "/api/smoothness", json={"secs": 0.5}, timeout=3)
            time.sleep(0.3)
            link.stop_flag.set()
            link.join(timeout=1)
            print(f"csv: {a.csv_out}\nevents: {events_path}")


if __name__ == "__main__":
    main()
