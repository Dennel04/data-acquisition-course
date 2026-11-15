"""Automatic pulse series for Lab 2: N identical pump pulses, each logged as one logger.py run.

The Dobot pump box must be in AUTO (I/O) mode so it follows the MG400 digital outputs.
For every trial this script:
  1. starts a managed 100 Hz run on the AtomS3R (DA2_MEASURE_V1) through logger.capture,
  2. keeps the pump off for --off-before s (baseline),
  3. switches the pump on (blow or suck) for --on s (plateau),
  4. switches it off for the rest of the run,
  5. waits --rest s before the next trial.
All trials go to one CSV in the official logger schema (condition=pulse, trial=1..N), with the
logger's .runs.jsonl side file. Pump on/off times relative to the run start are added to a
separate <csv>.pump.jsonl file for choosing baseline/plateau windows.

The pump is driven straight through the MG400 dashboard port (29999) with DOExecute.
Both DO lines are set low before the first trial, after every pulse, on Ctrl+C and on any error.
No robot motion commands are sent.

Example (opamp stage on G5):
  python src/python/pulse_series.py --port COM5 --config opamp --csv data/pulses_2026-11-15.csv \
      --electrical-check-confirmed
"""
import argparse
import json
from pathlib import Path
import socket
import sys
import threading
import time
from types import SimpleNamespace
import uuid

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import logger  # noqa: E402

ROBOT_IP = "192.168.1.6"
DASHBOARD_PORT = 29999
BLOW_DO, SUCK_DO = 1, 2  # mg400-base defaults (MG400_BLOW_DO / MG400_SUCK_DO), used in Lab 1


class Dashboard:
    """Minimal MG400 dashboard client: DOExecute only."""

    def __init__(self, ip, port=DASHBOARD_PORT, timeout=2.0, dry_run=False):
        self.dry_run = dry_run
        self.sock = None
        if not dry_run:
            self.sock = socket.create_connection((ip, port), timeout=timeout)
            self.sock.settimeout(timeout)

    def do(self, index, value):
        cmd = f"DOExecute({int(index)},{1 if value else 0})"
        if self.dry_run:
            return f"dry-run {cmd}"
        self.sock.sendall(cmd.encode("ascii"))
        reply = self.sock.recv(1024).decode("ascii", "replace").strip()
        if not reply.startswith("0,"):
            raise RuntimeError(f"robot refused {cmd}: {reply}")
        return reply

    def pump(self, mode):
        """mode: 'blow', 'suck' or 'off'. Never energises both lines."""
        if mode == "blow":
            self.do(SUCK_DO, 0); self.do(BLOW_DO, 1)
        elif mode == "suck":
            self.do(BLOW_DO, 0); self.do(SUCK_DO, 1)
        else:
            self.do(BLOW_DO, 0); self.do(SUCK_DO, 0)

    def close(self):
        if self.sock:
            self.sock.close()


class HttpPump:
    """Pump through a running mg400-base server (POST /api/pump) instead of our own 29999 socket.

    The MG400 dashboard keeps one client, so a second 29999 connection kicks mg400-base out
    (15.11.26: Smart Solutions series failed twice, our opamp trial 13 lost the link).
    """

    def __init__(self, url, timeout=2.0, dry_run=False):
        self.url, self.timeout, self.dry_run = url.rstrip("/"), timeout, dry_run
        if not dry_run:
            cfg = self._request("/api/config")
            if (cfg.get("blow_do"), cfg.get("suck_do")) != (BLOW_DO, SUCK_DO):
                raise RuntimeError(f"mg400-base uses blow_do={cfg.get('blow_do')} suck_do={cfg.get('suck_do')}, "
                                   f"expected {BLOW_DO}/{SUCK_DO}")

    def _request(self, path, body=None):
        import urllib.request
        data = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request(self.url + path, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            return json.loads(r.read().decode())

    def pump(self, mode):
        if mode not in ("blow", "suck", "off"):
            raise ValueError(mode)
        if self.dry_run:
            return f"dry-run POST /api/pump {mode}"
        reply = self._request("/api/pump", {"mode": mode})
        if not reply.get("ok"):
            raise RuntimeError(f"mg400-base refused pump {mode}: {reply}")
        return reply

    def close(self):
        pass


def pulse_thread(dash, mode, off_before, on, events, stop, clock=time.monotonic):
    """Runs beside logger.capture: off -> mode -> off. Records times relative to its own start."""
    t0 = clock()
    try:
        if stop.wait(off_before):
            return
        dash.pump(mode)
        events.append(("on", round(clock() - t0, 3)))
        stop.wait(on)
    except Exception as e:  # recorded; capture keeps running and the main loop stops the series
        events.append(("error", repr(e)))
    finally:
        try:
            dash.pump("off")
            events.append(("off", round(clock() - t0, 3)))
        except Exception as e:
            events.append(("off_error", repr(e)))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--port", required=True, help="Atom serial port, e.g. COM5")
    p.add_argument("--config", choices=sorted(logger.CONFIGS), required=True)
    p.add_argument("--csv", type=Path, required=True)
    p.add_argument("--trials", type=int, default=30)
    p.add_argument("--first-trial", type=int, default=1, help="to redo or continue a series")
    p.add_argument("--mode", choices=["blow", "suck"], default="blow")
    p.add_argument("--duration", type=float, default=10.0, help="seconds per run")
    p.add_argument("--off-before", type=float, default=3.0)
    p.add_argument("--on", type=float, default=4.0)
    p.add_argument("--rest", type=float, default=5.0, help="seconds between runs")
    p.add_argument("--robot", default=ROBOT_IP)
    p.add_argument("--mg400-url", help="drive the pump through a running mg400-base, e.g. http://127.0.0.1:8000 "
                                       "(no own 29999 connection)")
    p.add_argument("--dry-run-pump", action="store_true", help="log only, do not touch the robot")
    p.add_argument("--electrical-check-confirmed", action="store_true", required=True,
                   help="the G5 voltage for this config was checked with a multimeter over the full range")
    a = p.parse_args(argv)
    if not 1 <= a.trials <= 100 or a.off_before + a.on >= a.duration or a.on > 6:
        p.error("need 1..100 trials, off_before + on < duration, on <= 6 s")

    if a.mg400_url:
        dash = HttpPump(a.mg400_url, dry_run=a.dry_run_pump)
    else:
        dash = Dashboard(a.robot, dry_run=a.dry_run_pump)
    port = logger.open_atom(a.port)
    pump_log = Path(str(a.csv) + ".pump.jsonl")
    run_log = Path(str(a.csv) + ".runs.jsonl")
    bad = []
    try:
        dash.pump("off")
        last = a.first_trial + a.trials - 1
        for trial in range(a.first_trial, last + 1):
            handle, writer = logger.open_csv(a.csv, a.csv.exists())
            events, stop = [], threading.Event()
            args = SimpleNamespace(config=a.config, condition="pulse", trial=trial, duration=a.duration, dmm_v=None)
            th = threading.Thread(target=pulse_thread, args=(dash, a.mode, a.off_before, a.on, events, stop), daemon=True)
            run = uuid.uuid4().hex[:16]
            try:
                th.start()
                summary = logger.capture(port, writer, handle, args, run)
            finally:
                stop.set(); th.join(10); handle.close()
            with run_log.open("a", encoding="utf-8") as f:
                f.write(json.dumps(summary, allow_nan=False) + "\n")
            with pump_log.open("a", encoding="utf-8") as f:
                f.write(json.dumps(dict(run_id=run, config=a.config, trial=trial, mode=a.mode, events=events)) + "\n")
            ok = summary.get("status") == "complete" and summary.get("timing_ok") and not any(e[0].endswith("error") for e in events)
            on_t = next((e[1] for e in events if e[0] == "on"), None)
            print(f"[{a.config}] trial {trial}/{last}: {'OK' if ok else 'NOT OK'}  rows={summary.get('rows')} "
                  f"missed={summary.get('missed')} pump_on_at={on_t}s"
                  + (f"  error={summary.get('error')}" if summary.get("error") else "")
                  + (f"  atom_stop={summary['atom_stop']}" if summary.get("atom_stop") else "")
                  + ("" if ok else f"  events={events}"), flush=True)
            if not ok:
                bad.append(trial)
                if any(e[0].endswith("error") for e in events) or summary.get("error"):
                    print("Stopping the series: pump or Atom error.", flush=True)
                    break
            if trial != last:
                time.sleep(a.rest)
    except KeyboardInterrupt:
        print("Interrupted.", flush=True)
    finally:
        try:
            dash.pump("off")
        finally:
            dash.close(); port.close()
    print(f"Done. Not OK trials: {bad or 'none'}. CSV: {a.csv}", flush=True)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
