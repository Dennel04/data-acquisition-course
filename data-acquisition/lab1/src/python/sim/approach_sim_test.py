"""Run pick_in_place --approach against the simulator for several glass heights."""
import re, subprocess, sys, time
from pathlib import Path
import requests

S = Path(__file__).parent
import os
PY = str(Path(os.environ.get("MG400_BASE", Path.home() / "tools" / "mg400-base")) / ".venv" / "Scripts" / "python.exe")
REPO = Path(__file__).resolve().parent.parent
U = "http://127.0.0.1:8765"


def kill_sims():
    subprocess.run(["powershell", "-NoProfile", "-Command",
                    "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*sim.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }"],
                   capture_output=True)


def run(glass_z):
    kill_sims(); time.sleep(1)
    sim = S / "sim.py"
    sim.write_text(re.sub(r"^GLASS_Z = .*$", f"GLASS_Z = {glass_z}", sim.read_text(encoding="utf-8"), flags=re.M), encoding="utf-8")
    proc = subprocess.Popen([PY, str(sim)], cwd=S, stdout=open(S / "sim.log", "w"), stderr=subprocess.STDOUT)
    for _ in range(40):
        try:
            requests.get(U + "/api/config", timeout=0.5); break
        except Exception:
            time.sleep(0.25)
    requests.post(U + "/api/connect", json={"ip": "127.0.0.1"}, timeout=3)
    requests.post(U + "/api/enable", timeout=5)
    requests.post(U + "/api/z_floor", json={"z": -30}, timeout=3)
    print(f"=== glass top at {glass_z} (pump on at -25, floor -30)", flush=True)
    out = subprocess.run([sys.executable, "pick_in_place.py", "--port", "socket://127.0.0.1:8766", "--mg400-url", U,
                          "--csv-out", str(S / "approach_sim.csv"), "--approach", "--cycles", "2",
                          "--lift", "15", "--clear", "10"], cwd=REPO, capture_output=True, text=True, timeout=200)
    for line in out.stdout.splitlines():
        if line.startswith(("[zero]", "csv:", "events:")):
            continue
        print(line)
    st = requests.get(U + "/api/status", timeout=3).json()
    print(f"   final z {st['pose'][2]:.2f}, lowest z seen must be >= -30; pump {st['pump_mode']}")
    proc.kill()


for gz in (-27.0, -45.0):
    run(gz)
kill_sims()
