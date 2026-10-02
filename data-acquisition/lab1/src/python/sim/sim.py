"""Bench without hardware: fake MG400 + mg400 server on :8765 + fake Atom on tcp :8766.

Run with the mg400-base venv python, then point the scripts at
--mg400-url http://127.0.0.1:8765 --port socket://127.0.0.1:8766 (see approach_sim_test.py).

The fake Atom mirrors firmware pump_logic.h (band, min-off, cycle limit) and a
crude pneumatic model: pump suck -> p falls toward -85, blow -> rises toward +40,
pump off -> leaks back toward 0 (slowly if 'glass' is on the napp).
"""
import json, socket, sys, threading, time

import os
from pathlib import Path
MG400_BASE = Path(os.environ.get("MG400_BASE", Path.home() / "tools" / "mg400-base"))
sys.path.insert(0, str(MG400_BASE / "tests"))   # fake_mg400.py ships with mg400-base
from fake_mg400 import FakeMG400
from mg400 import server
from mg400.driver import DobotMG400

GLASS_Z = -27.0
fake = FakeMG400()
ports = fake.ports


class Robot(DobotMG400):
    def __init__(self, ip):
        super().__init__(ip, command_timeout=0.5, ports=ports)


server.DobotMG400 = Robot
server.configure(str(Path(__file__).with_name("sim_locations.json")), None)
threading.Thread(target=lambda: server.app.run(port=8765, threaded=True), daemon=True).start()


def atom(conn):
    mode, on, off, min_off, max_cpm = "off", 0.0, 0.0, 0, 0
    p, pump, last_off, win_start, cyc = 0.0, False, -10**9, 0, 0
    commanded = False
    attached = False   # glass stays on the napp once gripped, until blown off
    t0 = time.monotonic()
    conn.settimeout(0.0)
    buf = b""
    nxt = time.monotonic()
    while True:
        try:
            d = conn.recv(4096)
            if not d:
                return
            buf += d
        except BlockingIOError:
            pass
        except OSError:
            return
        while b"\n" in buf:
            line, buf = buf.split(b"\n", 1)
            m = json.loads(line)
            if m["cmd"] == "mode":
                if m["mode"] != mode:
                    pump = False
                    commanded = m["mode"] != "off"
                mode = m["mode"]
            elif m["cmd"] == "band":
                on, off = m["on"], m["off"]
            elif m["cmd"] == "limits":
                min_off, max_cpm = m["minOffMs"], m["maxCyclesPerMin"]
            elif m["cmd"] == "stop":
                mode, pump = "off", False
        now = int((time.monotonic() - t0) * 1000)
        if mode == "off":
            pump = False
        else:
            if max_cpm and now - win_start > 60000:
                win_start, cyc = now, 0
            suction = mode == "suction"
            weaker = p > on if suction else p < on
            stronger = p < off if suction else p > off
            if not pump and weaker and (commanded or now - last_off >= min_off):
                pump = True
            elif pump and stronger:
                pump, last_off = False, now
            commanded = False
        # pneumatics: the real DO lines decide, read from the fake robot
        dob = fake.__dict__.get("do_bits", 0)
        z = fake.pose[2]
        on_glass = z <= GLASS_Z + 0.2
        if on_glass and p < -30: attached = True
        if p > -10: attached = False
        sealed = on_glass or attached
        if pump and mode == "suction":
            p += ((-85 - p) * 0.08) if sealed else ((-12 - p) * 0.05)   # open napp: ~-12 kPa (lab box)
        elif pump and mode == "blow":
            p += (40 - p) * 0.05
        else:
            p += (0 - p) * (0.00035 if sealed else 0.05)   # sealed leak fitted to the real glass: -64 -> -52 kPa in ~6 s
        try:
            conn.sendall((json.dumps({"t": now, "adc": 900, "p": round(p, 2), "mode": mode, "pump": int(pump)}) + "\n").encode())
        except OSError:
            return
        nxt += 0.01
        time.sleep(max(0, nxt - time.monotonic()))


ls = socket.socket()
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ls.bind(("127.0.0.1", 8766))
ls.listen(1)
print("sim ready: mg400 http://localhost:8765, atom socket://127.0.0.1:8766", flush=True)
while True:
    c, _ = ls.accept()
    threading.Thread(target=atom, args=(c,), daemon=True).start()
