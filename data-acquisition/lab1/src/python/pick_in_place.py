"""Data Acquisition Lab 1, part 4 "Võtmine": N picks of the glass in one spot.

Each cycle: napp on the glass (the start Z, the floor) -> suction -> lift ->
hold with the Atom's band -> back down -> short blow -> clear -> down again.
Same pump logic as hold_test.py (02.10.26): the pump is forced on while the
glass is on the support (the napp leaks there) and on the way down; in the
air the Atom's band decides, like the factory smart box.

Start with the napp resting on the glass. That Z is taken as the floor: no
target is ever below it.

    python pick_in_place.py --port COM4 --csv-out ../../data/<run>.csv
    python analyze_run.py ../../data/<run>.csv
"""

from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path

import requests

from logger import Mg400Pump, check_zero, open_atom
from grip import GripError, approach_and_grip
from pick_cycles import AtomLink

FORCED_ON = {"cmd": "band", "on": -149, "off": -150}   # suction: p is always weaker than -149


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--port", required=True)
    p.add_argument("--csv-out", type=Path, required=True)
    p.add_argument("--mg400-url", default="http://127.0.0.1:8000")
    p.add_argument("--cycles", type=int, default=10)
    p.add_argument("--lift", type=float, default=20.0, help="mm above the glass")
    p.add_argument("--clear", type=float, default=10.0, help="mm the napp backs off after release")
    p.add_argument("--hold", type=float, default=3.0, help="s in the air per cycle")
    p.add_argument("--grip-kpa", type=float, default=-50)
    p.add_argument("--grip-timeout", type=float, default=10.0)
    p.add_argument("--on-kpa", type=float, default=-40)
    p.add_argument("--off-kpa", type=float, default=-60)
    p.add_argument("--min-off-ms", type=int, default=15000)
    p.add_argument("--max-cycles-per-min", type=int, default=4)
    p.add_argument("--blow-ms", type=int, default=500)
    p.add_argument("--speed", type=int, default=5)
    p.add_argument("--approach", action="store_true",
                   help="start ABOVE the piece: lower, vacuum on --pump-on-mm above the floor, "
                        "stop on the seal, the Atom stops the pump when attached")
    p.add_argument("--floor", type=float, default=None, help="lowest Z (default: the server's Z floor)")
    p.add_argument("--pump-on-mm", type=float, default=5.0)
    p.add_argument("--seal-kpa", type=float, default=-25.0)
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

    s = status()
    if not s.get("enabled") or s.get("error"):
        raise SystemExit(f"robot not ready: {s.get('mode_name')} {s.get('alarm_ids')}")
    x0, y0, z_glass, r0 = s["pose"]
    if a.approach:
        floor = a.floor if a.floor is not None else float(s["z_floor"])
        floor = max(floor, float(s["z_floor"]))   # never below the server's floor
        z_glass = floor                            # replaced by the contact Z each cycle
    else:
        floor = max(z_glass, float(s.get("z_floor", z_glass)))

    def go_z(z, timeout=30.0):
        if z < floor - 0.05:
            raise RuntimeError(f"refusing Z {z:.1f}: below the floor {floor:.1f}")
        post("/api/move", {"x": x0, "y": y0, "z": z, "r": r0})
        end = time.monotonic() + timeout
        while time.monotonic() < end:
            st = status()
            if st.get("limit_warning") or st.get("error"):
                raise RuntimeError(f"robot: {st.get('limit_warning') or st.get('alarm_ids')}")
            if abs(st["pose"][2] - z) < 0.3:
                return
            time.sleep(0.05)
        raise RuntimeError(f"Z {z:.1f} not reached")

    post("/api/speed", {"ratio": a.speed})
    post("/api/smoothness", {"secs": 1.5})
    post("/api/sync")

    a.csv_out.parent.mkdir(parents=True, exist_ok=True)
    events_path = a.csv_out.with_suffix(".events.csv")
    pump = Mg400Pump(U, dry_run=False)
    t0 = time.monotonic()
    ok_cycles = 0
    in_air = False   # glass lifted: an error must set it down first
    with open_atom(a.port, 115200) as ser, open(events_path, "w", newline="") as ef:
        check_zero(ser)
        link = AtomLink(ser, pump, a.csv_out)
        link.start()
        ev = csv.writer(ef)
        ev.writerow(["wall_s", "atom_t_ms", "cycle", "phase", "p_kpa"])

        def event(c, phase):
            ev.writerow([round(time.monotonic() - t0, 3), link.last_t, c, phase, link.last_p])
            ef.flush()
            print(f"  [{c:2d}] {time.monotonic() - t0:6.1f} s  {phase:<10} p={link.last_p}")

        def check():
            if link.lost.is_set():
                raise RuntimeError("Atom USB lost")

        try:
            link.send({"cmd": "limits", "minOffMs": a.min_off_ms, "maxCyclesPerMin": a.max_cycles_per_min})
            for c in range(1, a.cycles + 1):
                if a.approach:
                    # lower, vacuum on just above the floor, stop on the seal,
                    # the Atom's band stops the pump: attached (grip.py)
                    event(c, "approach")
                    g = approach_and_grip(U, link, floor, pump_on_mm=a.pump_on_mm, seal_kpa=a.seal_kpa,
                                          on_kpa=a.on_kpa, off_kpa=a.off_kpa, approach_speed=a.speed,
                                          log=lambda m: print(f"       {m}"))
                    z_glass = g.z_contact
                    post("/api/speed", {"ratio": a.speed})
                    post("/api/smoothness", {"secs": 1.5})
                    event(c, "attached")
                else:
                    # grip on the support: pump forced on
                    link.send(FORCED_ON)
                    link.send({"cmd": "mode", "mode": "suction"})
                    event(c, "suction")
                    end = time.monotonic() + a.grip_timeout
                    while time.monotonic() < end and (link.last_p is None or link.last_p > a.grip_kpa):
                        check()
                        time.sleep(0.02)
                    if link.last_p is None or link.last_p > a.grip_kpa:
                        raise RuntimeError(f"cycle {c}: no grip ({link.last_p} kPa after {a.grip_timeout:g} s)")
                    event(c, "gripped")
                in_air = True
                go_z(z_glass + a.lift); check()
                # in the air: the Atom's band, like the smart box
                link.send({"cmd": "band", "on": a.on_kpa, "off": a.off_kpa})
                event(c, "lifted")
                time.sleep(a.hold); check()
                held = link.last_p is not None and link.last_p <= a.on_kpa
                event(c, "carried" if held else "dropped?")
                if not held:
                    raise RuntimeError(f"cycle {c}: vacuum lost in the air ({link.last_p} kPa)")
                # down with the pump on, then release; off -> suction is a mode
                # change, so the firmware starts it at once (no min-off wait)
                link.send(FORCED_ON)
                link.send({"cmd": "mode", "mode": "off"})
                link.send({"cmd": "mode", "mode": "suction"})
                go_z(z_glass); check()
                in_air = False
                event(c, "at-place")
                link.send({"cmd": "band", "on": 5, "off": 20})
                link.send({"cmd": "mode", "mode": "blow"})
                time.sleep(a.blow_ms / 1000)
                link.send({"cmd": "mode", "mode": "off"})
                event(c, "released")
                go_z(z_glass + a.clear); check()
                time.sleep(0.5)
                if not a.approach:            # --approach comes down again by itself
                    go_z(z_glass); check()
                event(c, "clear")
                ok_cycles += 1
            print(f"done: {ok_cycles}/{a.cycles} picks")
        except KeyboardInterrupt:
            print("interrupted")
        except Exception as exc:
            print(f"STOP: {exc}")
            try:
                requests.post(U + "/api/stop", timeout=3)
            except Exception:
                pass
            # glass may be in the air: set it down with the pump on before
            # anything is switched off -- unless the robot itself is faulted
            try:
                st = status()
                if in_air and not st.get("error") and st["pose"][2] > z_glass + 1 and not link.lost.is_set():
                    print("setting the glass down before stopping")
                    link.send(FORCED_ON)
                    link.send({"cmd": "mode", "mode": "off"})
                    link.send({"cmd": "mode", "mode": "suction"})
                    post("/api/sync")
                    go_z(z_glass)
            except Exception as exc2:
                print(f"could not set it down: {exc2}")
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
