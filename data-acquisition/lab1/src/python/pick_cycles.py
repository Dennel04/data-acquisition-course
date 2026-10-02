"""Data Acquisition Lab 1, part 4 "Võtmine": the robot picks the glass N times.

README: "robot viib napi klaasile, imemine, tõst, koht, puhumine, lahti.
Kümme korda." and "pumba töötsükkel kümne võtmise ajal".

Same pump control as logger.py -- the Atom decides, this PC only relays the
decision to the MG400 DO lines (with the 500 ms watchdog) -- plus a robot
sequence on top. The Atom's serial port can only be open in one program, so
this script replaces logger.py for the pick run; don't run both.

Before running: in the mg400-base page (mg400 serve -> http://localhost:8000)
press Connect, Enable, and save four locations (Set):
  slot 1  above A   -- a safe height above the glass at place A
  slot 2  A         -- napp touching the glass at place A
  slot 3  above B   -- a safe height above place B
  slot 4  B         -- glass resting at place B
Odd cycles carry the glass A -> B, even cycles B -> A, so ten cycles need no
manual reset.

Writes two files:
  <csv-out>             t_ms, adc, p_kpa, pump    (same format as logger.py)
  <csv-out>.events.csv  wall_s, atom_t_ms, cycle, phase, p_kpa
"""

from __future__ import annotations

import argparse
import csv
import json
import threading
import time
from pathlib import Path

import requests
import serial

from logger import WATCHDOG_TIMEOUT_S, Mg400Pump, send_command

SLOT_ABOVE_A, SLOT_A, SLOT_ABOVE_B, SLOT_B = 1, 2, 3, 4


class AtomLink(threading.Thread):
    """Reads Atom telemetry, writes the CSV, relays the pump decision."""

    def __init__(self, ser: serial.Serial, pump: Mg400Pump, csv_path: Path):
        super().__init__(daemon=True)
        self.ser = ser
        self.pump = pump
        self.csv_path = csv_path
        self.lock = threading.Lock()
        self.last_p: float | None = None
        self.last_t: int | None = None
        self.lost = threading.Event()  # USB gone -> main sequence must stop
        self.stop_flag = threading.Event()

    def send(self, obj: dict) -> None:
        with self.lock:
            send_command(self.ser, obj)

    def run(self) -> None:
        last_line_at = time.monotonic()
        tripped = False
        with open(self.csv_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["t_ms", "adc", "p_kpa", "pump"])
            while not self.stop_flag.is_set():
                try:
                    raw = self.ser.readline()
                except serial.SerialException as exc:
                    print(f"[usb] serial port lost ({exc}), forcing pump off")
                    self.pump.set_mode("off")
                    self.lost.set()
                    return
                now = time.monotonic()
                if raw:
                    try:
                        msg = json.loads(raw.decode("ascii", errors="replace"))
                    except json.JSONDecodeError:
                        continue
                    if "p" not in msg:
                        continue
                    last_line_at = now
                    tripped = False
                    w.writerow([msg.get("t"), msg.get("adc"), msg.get("p"), msg.get("pump")])
                    f.flush()
                    self.last_p, self.last_t = msg.get("p"), msg.get("t")
                    on = bool(msg.get("pump", 0))
                    mode = msg.get("mode", "off")
                    self.pump.set_mode("off" if not on else ("suck" if mode == "suction" else "blow"))
                if now - last_line_at > WATCHDOG_TIMEOUT_S and not tripped:
                    print("[watchdog] no line in 500ms, forcing pump off")
                    self.pump.set_mode("off")
                    tripped = True


class Robot:
    def __init__(self, base_url: str):
        self.url = base_url.rstrip("/")

    def _post(self, path: str, body: dict | None = None) -> dict:
        r = requests.post(self.url + path, json=body or {}, timeout=3)
        r.raise_for_status()
        out = r.json()
        if not out.get("ok"):
            raise RuntimeError(f"{path}: {out.get('error', out)}")
        return out

    def status(self) -> dict:
        return requests.get(self.url + "/api/status", timeout=3).json()

    def slots(self) -> dict[int, dict]:
        data = requests.get(self.url + "/api/locations", timeout=3).json()
        return {s["slot"]: s for s in data["slots"]}

    def speed(self, ratio: int) -> None:
        self._post("/api/speed", {"ratio": ratio})
        self._post("/api/smoothness", {"secs": 1.5})  # gentlest start/stop

    def stop(self) -> None:
        try:
            self._post("/api/stop")
        except Exception as exc:  # best effort on the way out
            print(f"[mg400] stop failed: {exc}")

    def go(self, slot: dict, timeout: float = 120.0, tol: float = 2.0) -> None:
        self._post(f"/api/recall/{slot['slot']}")
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            st = self.status()
            pose = st.get("pose")
            if st.get("stalled") or st.get("servo_error"):
                raise RuntimeError(f"robot fault: {st.get('servo_error') or 'stalled'}")
            if pose and all(abs(pose[i] - slot[k]) <= tol for i, k in enumerate("xyz")):
                return
            time.sleep(0.05)
        raise RuntimeError(f"slot {slot['slot']} not reached in {timeout:.0f}s")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--port", required=True)
    p.add_argument("--baud", type=int, default=115200)
    p.add_argument("--csv-out", type=Path, required=True)
    p.add_argument("--mg400-url", default="http://localhost:8000")
    p.add_argument("--cycles", type=int, default=10)
    p.add_argument("--speed", type=int, default=2,
                   help="robot speed %% -- team rule: turtle speed, 2 %% default, 5 %% max")
    # suction band/limits: the numbers chosen in docs/pump_control.md
    p.add_argument("--on-kpa", type=float, default=-40)
    p.add_argument("--off-kpa", type=float, default=-75)
    p.add_argument("--min-off-ms", type=int, default=15000)
    p.add_argument("--max-cycles-per-min", type=int, default=4)
    p.add_argument("--grip-kpa", type=float, default=-40,
                   help="vacuum at least this strong = glass is held")
    p.add_argument("--grip-timeout", type=float, default=20.0,
                   help="covers the 15 s min-off-time if the pump stopped just before")
    # release: short blow, Atom in blow mode with its own band, then off
    p.add_argument("--blow-on-kpa", type=float, default=5)
    p.add_argument("--blow-off-kpa", type=float, default=20)
    p.add_argument("--blow-ms", type=int, default=800)
    p.add_argument("--dry-run", action="store_true", help="no pump DO calls (robot still moves)")
    a = p.parse_args()
    if not 1 <= a.speed <= 5:
        raise SystemExit("--speed must be 1..5 % (team rule: never jerk the arm)")

    robot = Robot(a.mg400_url)
    st = robot.status()
    if not st.get("enabled"):
        raise SystemExit("robot not enabled: press Connect + Enable on the mg400 page first")
    slots = robot.slots()
    missing = [n for n in (SLOT_ABOVE_A, SLOT_A, SLOT_ABOVE_B, SLOT_B) if not slots[n]["set"]]
    if missing:
        raise SystemExit(f"save locations first, empty slots: {missing}")
    robot.speed(a.speed)

    a.csv_out.parent.mkdir(parents=True, exist_ok=True)
    events_path = a.csv_out.with_suffix(".events.csv")
    pump = Mg400Pump(a.mg400_url, a.dry_run)
    t0 = time.monotonic()

    with serial.serial_for_url(a.port, a.baud, timeout=0.2) as ser, open(events_path, "w", newline="") as ef:
        link = AtomLink(ser, pump, a.csv_out)
        link.start()
        ev = csv.writer(ef)
        ev.writerow(["wall_s", "atom_t_ms", "cycle", "phase", "p_kpa"])

        def event(cycle: int, phase: str) -> None:
            ev.writerow([round(time.monotonic() - t0, 3), link.last_t, cycle, phase, link.last_p])
            ef.flush()
            print(f"  [{cycle:2d}] {phase:<14} p={link.last_p}")

        def check() -> None:
            if link.lost.is_set():
                raise RuntimeError("Atom USB lost")

        def suction_band() -> None:
            link.send({"cmd": "band", "on": a.on_kpa, "off": a.off_kpa})

        link.send({"cmd": "limits", "minOffMs": a.min_off_ms, "maxCyclesPerMin": a.max_cycles_per_min})
        suction_band()
        link.send({"cmd": "mode", "mode": "off"})
        time.sleep(0.5)

        held = 0
        try:
            for c in range(1, a.cycles + 1):
                src = (slots[SLOT_ABOVE_A], slots[SLOT_A]) if c % 2 else (slots[SLOT_ABOVE_B], slots[SLOT_B])
                dst = (slots[SLOT_ABOVE_B], slots[SLOT_B]) if c % 2 else (slots[SLOT_ABOVE_A], slots[SLOT_A])

                robot.go(src[0]); check(); event(c, "above-src")
                robot.go(src[1]); check(); event(c, "at-glass")
                suction_band()
                link.send({"cmd": "mode", "mode": "suction"}); event(c, "suction")
                deadline = time.monotonic() + a.grip_timeout
                while time.monotonic() < deadline and (link.last_p is None or link.last_p > a.grip_kpa):
                    check(); time.sleep(0.02)
                gripped = link.last_p is not None and link.last_p <= a.grip_kpa
                event(c, "gripped" if gripped else "grip-timeout")
                if not gripped:
                    raise RuntimeError(f"cycle {c}: no vacuum after {a.grip_timeout}s -- napp not on glass?")

                robot.go(src[0]); check(); event(c, "lifted")
                robot.go(dst[0]); check()
                still = link.last_p is not None and link.last_p <= a.grip_kpa
                event(c, "carried" if still else "dropped?")
                robot.go(dst[1]); check(); event(c, "at-place")

                link.send({"cmd": "band", "on": a.blow_on_kpa, "off": a.blow_off_kpa})
                link.send({"cmd": "mode", "mode": "blow"}); event(c, "blow")
                time.sleep(a.blow_ms / 1000)
                link.send({"cmd": "mode", "mode": "off"}); event(c, "released")
                robot.go(dst[0]); check(); event(c, "clear")
                held += still
            print(f"done: {a.cycles} cycles, glass held through the carry in {held}")
        except KeyboardInterrupt:
            print("interrupted")
        except Exception as exc:
            print(f"STOP: {exc}")
        finally:
            robot.stop()
            try:
                link.send({"cmd": "stop"})
            except Exception:
                pass
            pump.set_mode("off")
            time.sleep(0.3)
            link.stop_flag.set()
            link.join(timeout=1)
            print(f"csv: {a.csv_out}\nevents: {events_path}")


if __name__ == "__main__":
    main()
