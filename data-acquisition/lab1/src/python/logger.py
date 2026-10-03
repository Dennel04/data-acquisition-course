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
import queue
import threading
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
    duration: float
    zero: bool
    station: str | None = None


def parse_args() -> Args:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--port", required=True, help="e.g. COM5")
    p.add_argument("--baud", type=int, default=115200)
    p.add_argument("--csv-out", type=Path, default=Path("data/lab1_log.csv"))
    p.add_argument("--mg400-url", default="http://127.0.0.1:8000")  # not localhost: Windows tries IPv6 first, +200 ms per call
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
    p.add_argument("--duration", type=float, default=0,
                   help="stop cleanly (Atom stop + pump off) after this many seconds; 0 = until Ctrl+C")
    p.add_argument("--zero", action="store_true",
                   help="re-take the Atom's atmospheric zero first (pump off, tube OPEN to air)")
    p.add_argument("--station", default=None,
                   help="Smart Solutions station URL, e.g. http://127.0.0.1:5000: forward the "
                        "Atom's letter lines there (merged Atom firmware, USB letter channel)")
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
        duration=a.duration,
        zero=a.zero,
        station=a.station,
    )


class StationLetters:
    """Forward {"letter":...} lines to the station's POST /api/letter.

    03.10.26, merged Atom firmware: the same USB line carries the 10 ms
    telemetry and, on a long button press, one letter line. The lab PC has
    no WiFi, so this port is the letter channel too. POSTs run on their own
    thread: a slow station must never delay the reader, or the 500 ms
    watchdog would switch the pump off."""

    def __init__(self, station_url: str) -> None:
        self.url = station_url.rstrip("/") + "/api/letter"
        self._session = requests.Session()
        self._queue: queue.Queue[dict | None] = queue.Queue()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def submit(self, msg: dict) -> None:
        letter = msg.get("letter")
        if isinstance(letter, str) and len(letter) == 1 and "A" <= letter <= "Z":
            self._queue.put(msg)

    def close(self) -> None:
        self._queue.put(None)
        self._thread.join(3.0)

    def _run(self) -> None:
        while (msg := self._queue.get()) is not None:
            for attempt in range(3):
                try:
                    r = self._session.post(self.url, json=msg, timeout=2.0)
                    print(f"[{stamp()}] [letter] {msg['letter']} seq={msg.get('seq')} -> HTTP {r.status_code}")
                    break
                except requests.RequestException as exc:
                    print(f"[{stamp()}] [letter] {msg['letter']} attempt {attempt + 1}: {exc}")
                    time.sleep(0.25)


class Mg400Pump:
    """mg400-base's HTTP pump API, driven from its own sender thread.

    set_mode() only records the wanted state and returns at once; a sender
    thread posts the newest wanted state. 02.10.26: the read loop used to
    make the HTTP call itself and wait 0.2-1 s for the reply -- meanwhile
    nobody read the Atom, the watchdog saw silence and forced the pump off,
    over and over. Reading the Atom must never wait on the network."""

    def __init__(self, base_url: str, dry_run: bool):
        self.base_url = base_url.rstrip("/")
        self.dry_run = dry_run
        self._want: str | None = None
        self._sent: str | None = None
        self._force = False
        self._cond = threading.Condition()
        self._session = requests.Session()
        threading.Thread(target=self._sender, daemon=True, name="pump-sender").start()

    def set_mode(self, mode: str, force: bool = False) -> None:
        """mode: 'suck' | 'blow' | 'off' (mg400-base's own vocabulary --
        note this differs from the Atom's 'suction'/'blow'/'off', translate
        at the call site, don't blur the two). Non-blocking."""
        with self._cond:
            if mode == self._want and not force:
                return  # don't spam the HTTP API every 10ms for no change
            self._want = mode
            self._force = self._force or force
            self._cond.notify()

    def flush(self, timeout: float = 3.0) -> bool:
        """Wait until the newest wanted state has been sent (e.g. 'off' on exit)."""
        end = time.monotonic() + timeout
        with self._cond:
            while (self._sent != self._want or self._force) and time.monotonic() < end:
                self._cond.wait(0.05)
            return self._sent == self._want

    def _sender(self) -> None:
        while True:
            with self._cond:
                while self._want == self._sent and not self._force:
                    self._cond.wait()
                mode, self._force = self._want, False
            self._post(mode)
            with self._cond:
                self._sent = mode
                self._cond.notify_all()

    def _post(self, mode: str) -> None:
        if self.dry_run:
            print(f"[dry-run] would POST /api/pump mode={mode}")
            return
        try:
            r = self._session.post(f"{self.base_url}/api/pump", json={"mode": mode}, timeout=1.0)
            r.raise_for_status()
            body = r.json()
            if not body.get("ok", False):
                print(f"[mg400] pump command rejected: {body}")
        except requests.RequestException as exc:
            # the watchdog upstream exists for exactly this kind of fault --
            # log it; the next change (or a forced off) is sent right after
            print(f"[mg400] request failed: {exc}")


def open_atom(port: str, baud: int) -> serial.Serial:
    """Open the Atom's USB serial WITHOUT resetting it.

    02.10.26: pyserial's default open/close toggles DTR/RTS, and on the
    ESP32-S3's native USB that is the reset line -- every open rebooted the
    Atom, and the firmware takes its atmospheric zero at boot from whatever
    is in the tube. With the glass held at -62 kPa a reconnect made the
    display read 0. Setting DTR/RTS low before open() leaves it running."""
    ser = serial.serial_for_url(port, baud, timeout=0.2, do_not_open=True)
    ser.dtr = False
    ser.rts = False
    ser.open()
    return ser


def check_zero(ser: serial.Serial, seconds: float = 1.0) -> None:
    """Warn if the Atom just booted (zero taken now) or reads far from 0 kPa
    at rest -- either means the relative pressure may be offset."""
    end = time.monotonic() + seconds
    ps, uptime = [], None
    while time.monotonic() < end:
        try:
            m = json.loads(ser.readline().decode("ascii", errors="replace"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if "p" in m:
            ps.append(float(m["p"]))
            uptime = m.get("t")
    if not ps:
        print("[zero] no telemetry from the Atom yet")
        return
    avg = sum(ps) / len(ps)
    print(f"[zero] Atom up {uptime / 1000:.0f} s, reads {avg:+.1f} kPa now")
    if uptime is not None and uptime < 5000:
        print("[zero] Atom just booted: its zero is whatever was in the tube at boot")
    if abs(avg) > 3:  # the pump is off before the first mode command
        print("[zero] WARNING: not ~0 kPa with the pump off -- open the tube to air "
              "and press the Atom reset button to re-zero, or the band is shifted")


def stamp() -> str:
    return time.strftime("%H:%M:%S") + f".{int(time.time() * 1000) % 1000:03d}"


class Watchdog(threading.Thread):
    """README part 4: "Kui 500 ms jooksul rida ei tule, DO maha".

    Runs in its own thread so it fires on time even when the read loop is
    stuck: 02.10.26 an unplugged USB left readline() hanging inside Windows
    for ~1.5 s before it raised, and the in-loop check waited with it
    (pump went off 1.6 s after the last line). Call feed() on every line."""

    def __init__(self, pump: "Mg400Pump", timeout_s: float = WATCHDOG_TIMEOUT_S):
        super().__init__(daemon=True)
        self.pump = pump
        self.timeout_s = timeout_s
        self._last = time.monotonic()
        self._tripped = False
        self._stop = threading.Event()

    def feed(self) -> None:
        self._last = time.monotonic()
        self._tripped = False

    def stop(self) -> None:
        self._stop.set()

    @property
    def tripped(self) -> bool:
        return self._tripped

    def run(self) -> None:
        while not self._stop.wait(0.05):
            silent = time.monotonic() - self._last
            if silent > self.timeout_s and not self._tripped:
                self._tripped = True
                print(f"[{stamp()}] [watchdog] no line for {silent * 1000:.0f} ms, forcing pump off")
                self.pump.set_mode("off", force=True)


def request_zero(ser: serial.Serial, timeout_s: float = 2.0) -> None:
    """Ask the firmware to re-take its atmospheric zero ({"cmd":"zero"}).
    It refuses while the pump runs or the reading is not near atmosphere."""
    send_command(ser, {"cmd": "zero"})
    end = time.monotonic() + timeout_s
    while time.monotonic() < end:
        try:
            m = json.loads(ser.readline().decode("ascii", errors="replace"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if "zero" in m:
            state = "set" if m.get("ok") else f"refused ({m.get('why')})"
            print(f"[zero] {state}: atmosphere = {m['zero']:.2f} kPa absolute")
            return
    print("[zero] no reply -- old firmware without the zero command?")


def send_command(ser: serial.Serial, obj: dict) -> None:
    ser.write((json.dumps(obj) + "\n").encode("ascii"))


def main() -> None:
    args = parse_args()
    args.csv_out.parent.mkdir(parents=True, exist_ok=True)

    pump = Mg400Pump(args.mg400_url, args.dry_run)
    letters = StationLetters(args.station) if args.station else None

    with open_atom(args.port, args.baud) as ser, open(
        args.csv_out, "w", newline=""
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["t_ms", "adc", "p_kpa", "pump"])  # README part 2 format
        if args.zero:
            request_zero(ser)
        check_zero(ser)

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

        watchdog = Watchdog(pump)
        watchdog.start()
        deadline = time.monotonic() + args.duration if args.duration > 0 else None

        try:
            while True:
                try:
                    raw = ser.readline()  # empty bytes on the 0.2s timeout
                except serial.SerialException as exc:
                    # 02.10.26: on Windows an unplugged USB cable raises here
                    # instead of returning empty bytes, so the watchdog below
                    # never got its chance and the script died with the pump
                    # still on. USB out = pump out, then stop.
                    print(f"[{stamp()}] [usb] serial port lost ({exc}), forcing pump off")
                    pump.set_mode("off", force=True)
                    watchdog.stop()
                    pump.flush()
                    return
                now = time.monotonic()
                if deadline is not None and now >= deadline:
                    raise KeyboardInterrupt  # same clean stop as Ctrl+C

                if raw:
                    try:
                        msg = json.loads(raw.decode("ascii", errors="replace"))
                    except json.JSONDecodeError:
                        continue  # dropped/garbled line -- don't crash the logger
                    if "p" not in msg:
                        # e.g. {"letter":"A"} -- not telemetry, must not switch the pump
                        if letters is not None and "letter" in msg:
                            letters.submit(msg)
                        continue
                    watchdog.feed()

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
                    if not watchdog.tripped:
                        pump.set_mode(mg400_mode)

        except KeyboardInterrupt:
            print("stopping, forcing pump off")
            watchdog.stop()
            send_command(ser, {"cmd": "stop"})
            pump.set_mode("off", force=True)
            pump.flush()


if __name__ == "__main__":
    main()
