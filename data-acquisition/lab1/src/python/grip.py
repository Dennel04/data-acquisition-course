"""Approach-and-grip: lower onto a piece, sense the contact by vacuum, attach.

    above the floor ──(normal speed)──> floor + pump_on_mm
        vacuum on (commanded start)
    ──(slow creep toward the floor)──> napp seals on the piece:
        p drops below seal_kpa within ~0.2 s  -> stop the arm right there
    Atom band stops the pump at off_kpa          -> piece attached

The arm never goes below the floor. Reaching it without a seal means there
is no piece (or it is not under the napp): the pump is switched off and
GripError is raised. Used by pick_in_place.py --approach.
"""

from __future__ import annotations

import time
from dataclasses import dataclass

import requests


class GripError(RuntimeError):
    pass


@dataclass
class GripResult:
    z_contact: float      # Z where the seal was felt (the arm stopped there)
    p_seal: float         # pressure when the seal was detected, kPa
    p_attached: float     # pressure when the Atom stopped the pump, kPa
    creep_mm: float       # how far the arm crept with the vacuum on
    seal_s: float         # time from vacuum on to seal


def approach_and_grip(
    url: str,
    link,                      # pick_cycles.AtomLink: .send(), .last_p, .last_pump, .lost
    floor: float,
    pump_on_mm: float = 5.0,
    seal_kpa: float = -25.0,
    on_kpa: float = -40.0,
    off_kpa: float = -60.0,
    approach_speed: int = 5,
    creep_speed: int = 2,
    creep_ramp_s: float = 0.3,
    attach_timeout_s: float = 4.0,
    log=print,
) -> GripResult:
    url = url.rstrip("/")

    def post(path, body=None):
        r = requests.post(url + path, json=body or {}, timeout=3).json()
        if not r.get("ok"):
            raise GripError(f"{path}: {r}")

    def status():
        return requests.get(url + "/api/status", timeout=3).json()

    def fault(st):
        if st.get("error"):
            return f"robot alarm {st.get('alarm_ids')}"
        if st.get("limit_warning"):
            return f"limit guard: {st['limit_warning']}"
        if link.lost.is_set():
            return "Atom USB lost"
        return None

    st = status()
    x, y, z_now, r = st["pose"]
    z_pump = floor + pump_on_mm
    if z_now < z_pump - 0.3:
        raise GripError(f"start Z {z_now:.1f} is already below the pump-on point {z_pump:.1f}")

    # 1. pump off, normal speed down to the pump-on point
    link.send({"cmd": "mode", "mode": "off"})
    post("/api/speed", {"ratio": approach_speed})
    post("/api/smoothness", {"secs": 1.5})
    post("/api/move", {"x": x, "y": y, "z": z_pump, "r": r})
    end = time.monotonic() + 30
    while True:
        st = status()
        if fault(st):
            raise GripError(fault(st))
        if abs(st["pose"][2] - z_pump) < 0.3:
            break
        if time.monotonic() > end:
            raise GripError("pump-on point not reached")
        time.sleep(0.03)

    # 2. vacuum on (mode change = commanded start), band stops it at off_kpa
    link.send({"cmd": "band", "on": on_kpa, "off": off_kpa})
    link.send({"cmd": "mode", "mode": "suction"})
    t_on = time.monotonic()
    log(f"vacuum on at Z {z_pump:.1f}, creeping toward the floor {floor:.1f}")

    # 3. slow creep with a short braking ramp; stop on the seal
    post("/api/speed", {"ratio": creep_speed})
    post("/api/smoothness", {"secs": creep_ramp_s})
    post("/api/move", {"x": x, "y": y, "z": floor, "r": r})
    sealed = False
    end = time.monotonic() + 30
    while time.monotonic() < end:
        p = link.last_p
        if p is not None and p <= seal_kpa:
            post("/api/stop")             # brake now: ~v*ramp/2 = 0.6 mm at 2 %
            sealed = True
            break
        st = status()
        if fault(st):
            post("/api/stop")
            link.send({"cmd": "mode", "mode": "off"})
            raise GripError(fault(st))
        if abs(st["pose"][2] - floor) < 0.3:
            # at the floor: give the seal a moment (napp may touch just here)
            t_floor = time.monotonic()
            while time.monotonic() - t_floor < 1.0:
                if link.last_p is not None and link.last_p <= seal_kpa:
                    sealed = True
                    break
                time.sleep(0.01)
            break
        time.sleep(0.01)
    if not sealed:
        link.send({"cmd": "mode", "mode": "off"})
        raise GripError(f"reached the floor {floor:.1f} with no seal ({link.last_p} kPa): no piece under the napp?")
    seal_s = time.monotonic() - t_on
    p_seal = link.last_p
    time.sleep(0.15)
    z_contact = status()["pose"][2]
    post("/api/sync")                     # hold exactly where it stopped
    log(f"seal at Z {z_contact:.1f} ({p_seal:.1f} kPa, {seal_s:.2f} s after vacuum on)")

    # 4. the Atom stops the pump at off_kpa: attached
    end = time.monotonic() + attach_timeout_s
    while time.monotonic() < end:
        if link.last_pump == 0 and link.last_p is not None and link.last_p <= off_kpa + 2:
            break
        time.sleep(0.01)
    else:
        raise GripError(f"seal but the pump never reached {off_kpa:g} kPa ({link.last_p} kPa)")
    log(f"attached: pump stopped by the Atom at {link.last_p:.1f} kPa")
    return GripResult(z_contact, p_seal, link.last_p, z_pump - z_contact, seal_s)
