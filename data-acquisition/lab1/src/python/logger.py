"""PC-side script for Data Acquisition Lab 1, part 2 and part 4.

Graded coursework (SVNC.00.325) -- know this well enough to walk through
it at the oral defense. See ../BUILD_NOTES.md for what's still a
placeholder pending real hardware measurements.

Responsibilities, per README:
  - part 2: read the Atom's JSON telemetry line-by-line, write a CSV with
    columns t_ms, adc, p_kpa, pump (100 Hz target, checked as 1000+-5 rows
    per 10s).
  - part 4: send {"cmd":"mode",...} / {"cmd":"band",...} / {"cmd":"stop"}
    to the Atom, and drive the MG400's pump box over mg400-base's HTTP
    API (POST /api/pump {"mode":"suck"|"blow"|"off"}) based on the Atom's
    own "pump" decision field -- with a 500ms watchdog: if no line has
    arrived in the last 500ms, force the pump off regardless of the last
    known state (README: "Kui 500 ms jooksul rida ei tule, DO maha").

mg400-base API confirmed from https://github.com/KKallas/mg400-base:
  - `mg400 serve` starts an HTTP server on localhost:8000 by default.
  - POST /api/pump  {"mode": "suck" | "blow" | "off"}
  Verify this still matches the version your team actually installed --
  package APIs drift; don't take this comment as a substitute for reading
  its current README.
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import dataclass
from pathlib import Path

import requests
import serial

WATCHDOG_TIMEOUT_S = 0.5  # README part 4: 500ms


@dataclass
class Args:
    port: str
    baud: int
    csv_out: Path
    mg400_url: str
    mode: str  # "suction" | "blow" | "off"
    on_kpa: float
    off_kpa: float
    min_off_ms: int
    max_cycles_per_min: int
    dry_run: bool


def parse_args() -> Args:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--port", required=True, help="e.g. COM5")
    p.add_argument("--baud", type=int, default=115200)
    p.add_argument("--csv-out", type=Path, default=Path("data/lab1_log.csv"))
    p.add_argument("--mg400-url", default="http://localhost:8000")
    p.add_argument("--mode", choices=["suction", "blow", "off"], default="off")
    # These four numbers are the lab's own measured/tuned values (README
    # part 4's "five numbers", minus atmospheric which sensor.h handles on
    # the firmware side) -- pass in what YOUR team measured, don't reuse
    # placeholders across teams/sensors.
    p.add_argument("--on-kpa", type=float, required=True)
    p.add_argument("--off-kpa", type=float, required=True)
    p.add_argument("--min-off-ms", type=int, required=True)
    p.add_argument("--max-cycles-per-min", type=int, default=0)
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="skip MG400 HTTP calls; useful for part-2-only sanity logging "
        "before the robot/pump box is even wired in.",
    )
    a = p.parse_args()
    return Args(
        port=a.port,
        baud=a.baud,
        csv_out=a.csv_out,
        mg400_url=a.mg400_url,
        mode=a.mode,
        on_kpa=a.on_kpa,
        off_kpa=a.off_kpa,
        min_off_ms=a.min_off_ms,
        max_cycles_per_min=a.max_cycles_per_min,
        dry_run=a.dry_run,
    )


class Mg400Pump:
    """Thin wrapper over mg400-base's HTTP API. See module docstring."""

    def __init__(self, base_url: str, dry_run: bool):
        self.base_url = base_url.rstrip("/")
        self.dry_run = dry_run
        self._last_mode: str | None = None

    def set_mode(self, mode: str) -> None:
        """mode: 'suck' | 'blow' | 'off' (mg400-base's own vocabulary --
        note this differs from the Atom's 'suction'/'blow'/'off', translate
        at the call site, don't blur the two)."""
        if mode == self._last_mode:
            return  # don't spam the HTTP API every 10ms for no change
        if self.dry_run:
            print(f"[dry-run] would POST /api/pump mode={mode}")
            self._last_mode = mode
            return
        try:
            r = requests.post(
                f"{self.base_url}/api/pump", json={"mode": mode}, timeout=1.0
            )
            r.raise_for_status()
            body = r.json()
            if not body.get("ok", False):
                print(f"[mg400] pump command rejected: {body}")
        except requests.RequestException as exc:
            # Network hiccup with the robot's HTTP server is exactly the
            # kind of fault the 500ms watchdog exists for upstream of this
            # call -- log it, don't retry-loop inside a 10ms budget.
            print(f"[mg400] request failed: {exc}")
        self._last_mode = mode


def send_command(ser: serial.Serial, obj: dict) -> None:
    ser.write((json.dumps(obj) + "\n").encode("ascii"))


def main() -> None:
    args = parse_args()
    args.csv_out.parent.mkdir(parents=True, exist_ok=True)

    pump = Mg400Pump(args.mg400_url, args.dry_run)

    with serial.Serial(args.port, args.baud, timeout=0.2) as ser, open(
        args.csv_out, "w", newline=""
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["t_ms", "adc", "p_kpa", "pump"])  # README part 2 format

        # Configure the Atom once at startup. Re-send if you change these
        # live during a session -- this script doesn't watch for that.
        send_command(ser, {"cmd": "band", "on": args.on_kpa, "off": args.off_kpa})
        send_command(
            ser,
            {
                "cmd": "limits",
                "minOffMs": args.min_off_ms,
                "maxCyclesPerMin": args.max_cycles_per_min,
            },
        )
        send_command(ser, {"cmd": "mode", "mode": args.mode})

        last_line_at = time.monotonic()
        watchdog_tripped = False

        try:
            while True:
                raw = ser.readline()  # empty bytes on the 0.2s timeout
                now = time.monotonic()

                if raw:
                    last_line_at = now
                    watchdog_tripped = False
                    try:
                        msg = json.loads(raw.decode("ascii", errors="replace"))
                    except json.JSONDecodeError:
                        continue  # dropped/garbled line -- don't crash the logger

                    writer.writerow(
                        [msg.get("t"), msg.get("adc"), msg.get("p"), msg.get("pump")]
                    )
                    f.flush()

                    atom_mode = msg.get("mode", "off")
                    pump_on = bool(msg.get("pump", 0))
                    mg400_mode = (
                        "off"
                        if not pump_on
                        else ("suck" if atom_mode == "suction" else "blow")
                    )
                    pump.set_mode(mg400_mode)

                # 500ms watchdog: independent of what the Atom last said.
                if (now - last_line_at) > WATCHDOG_TIMEOUT_S and not watchdog_tripped:
                    print("[watchdog] no line in 500ms, forcing pump off")
                    pump.set_mode("off")
                    watchdog_tripped = True

        except KeyboardInterrupt:
            print("stopping, forcing pump off")
            send_command(ser, {"cmd": "stop"})
            pump.set_mode("off")


if __name__ == "__main__":
    main()
