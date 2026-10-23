"""DA2 measurement-only logger. No network, pump decisions, or calibration guesses."""
import argparse
import csv
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import re
import sys
import time
import uuid

FIELDS = ["t_ms", "adc", "p_kpa", "pump", "config", "run_id", "seq", "missed",
          "voltage_v", "dmm_reference_v", "dmm_recorded_utc", "condition", "trial", "adc_clipped"]
CONFIGS = {"raw", "opamp"}


def integer(value, lo, hi):
    return type(value) is int and lo <= value <= hi


def decode(line):
    if not line.endswith(b"\n") or len(line) > 512:
        raise ValueError("serial framing/length")
    if line.startswith(b"#"):
        raise ValueError("firmware diagnostic during run")
    data = json.loads(line.decode("ascii"))
    if not isinstance(data, dict):
        raise ValueError("expected object")
    return data


class Rows:
    def __init__(self, config, run):
        if config not in CONFIGS or not re.fullmatch(r"[0-9a-f]{16}",run):
            raise ValueError("invalid config/run")
        self.config, self.run = config, run
        self.last_t = None
        self.last_seq = -1
        self.last_missed = 0
        self.elapsed = 0
        self.gaps = []
        self.count = 0

    def accept(self, obj):
        if set(obj) != {"t","adc","p","pump","config","run","seq","missed"}:
            raise ValueError("telemetry schema")
        if obj["config"] != self.config or obj["run"] != self.run:
            raise ValueError("configuration/run mismatch (possible reboot)")
        if not integer(obj["t"],0,0xffffffff) or not integer(obj["adc"],0,4095):
            raise ValueError("timestamp/ADC")
        if obj["p"] is not None or obj["pump"] is not None:
            raise ValueError("unexpected pressure or actuator state")
        if not integer(obj["seq"],0,0xffffffff) or obj["seq"] != self.last_seq+1:
            raise ValueError("missing/duplicate sample")
        if not integer(obj["missed"],self.last_missed,0xffffffff):
            raise ValueError("missed counter")
        if self.last_t is not None:
            dt=(obj["t"]-self.last_t)&0xffffffff
            if not 1 <= dt <= 500:
                raise ValueError("nonmonotonic time, reset or long gap")
            self.elapsed+=dt
            self.gaps.append(dt)
        self.last_t=obj["t"]; self.last_seq=obj["seq"]; self.last_missed=obj["missed"]
        self.count+=1
        return dict(t_ms=obj["t"],adc=obj["adc"],p_kpa="",pump="",config=self.config,
                    run_id=self.run,seq=obj["seq"],missed=obj["missed"],voltage_v="",
                    adc_clipped=int(obj["adc"] in (0,4095)))

    def summary(self):
        return dict(rows=self.count,elapsed_ms=self.elapsed,missed=self.last_missed,
                    rate_hz=(self.count-1)*1000/self.elapsed if self.elapsed else None,
                    dt_min_ms=min(self.gaps) if self.gaps else None,
                    dt_max_ms=max(self.gaps) if self.gaps else None,
                    timing_ok=bool(self.gaps) and self.last_missed==0 and
                              all(9<=d<=11 for d in self.gaps))


def open_csv(path, append):
    path=Path(path)
    if append:
        with path.open("rb") as binary:
            binary.seek(0,2)
            if binary.tell()==0:
                raise ValueError("empty existing CSV")
            binary.seek(-1,2)
            if binary.read(1)!=b"\n":
                raise ValueError("existing CSV has incomplete final line")
        with path.open(newline="",encoding="utf-8") as existing:
            reader=csv.DictReader(existing)
            if reader.fieldnames != FIELDS:
                raise ValueError("existing CSV schema mismatch")
            for row in reader:
                if row.get("config") not in CONFIGS or None in row or any(v is None for v in row.values()):
                    raise ValueError("invalid existing CSV")
        handle=path.open("a",newline="",encoding="utf-8")
    else:
        handle=path.open("x",newline="",encoding="utf-8")  # never overwrite evidence
    writer=csv.DictWriter(handle,fieldnames=FIELDS)
    if not append:
        writer.writeheader(); handle.flush()
    return handle,writer


def wait_started(port, config, run, clock=time.monotonic):
    end=clock()+5
    while clock()<end:
        line=port.readline(513)
        if not line or line.startswith(b"# DA2_MEASURE_V1"):
            continue
        obj=decode(line)
        if obj != dict(event="started",firmware="DA2_MEASURE_V1",run=run,config=config,
                       period_ms=10,adc_pin=5,adc_bits=12,adc_samples=8,calibrated=False):
            raise ValueError("unexpected start acknowledgement")
        return
    raise TimeoutError("no DA2 start acknowledgement")


def capture(port, writer, handle, args, run, clock=time.monotonic):
    rows=Rows(args.config,run)
    summary=dict(run_id=run,config=args.config,condition=args.condition,trial=args.trial,
                 calibrated=False,status="partial",dmm_reference_v=args.dmm_v,
                 dmm_recorded_utc=datetime.now(timezone.utc).isoformat() if args.dmm_v is not None else "")
    try:
        port.reset_input_buffer()
        command=dict(cmd="measure_start",config=args.config,run=run)
        packet=json.dumps(command,separators=(",",":")).encode()+b"\n"
        if port.write(packet)!=len(packet):
            raise IOError("incomplete start write")
        wait_started(port,args.config,run,clock)
        started=last=clock()
        while clock()-started < args.duration+5:
            line=port.readline(513)
            if not line:
                if clock()-last>0.5:
                    raise TimeoutError("no samples for 500 ms; no pump action")
                continue
            row=rows.accept(decode(line)); last=clock()
            row.update(dmm_reference_v=args.dmm_v if args.dmm_v is not None else "",
                       dmm_recorded_utc=summary["dmm_recorded_utc"],condition=args.condition,trial=args.trial)
            writer.writerow(row)
            handle.flush()
            if rows.elapsed>=round(args.duration*1000):
                summary["status"]="complete"
                break
        else:
            raise TimeoutError("capture deadline")
    except (Exception,KeyboardInterrupt) as error:
        summary["error"]=type(error).__name__+": "+str(error)
    finally:
        try:
            port.write(b'{"cmd":"measure_stop"}\n')  # never Lab 1's actuator "stop"
        except Exception:
            pass
        summary.update(rows.summary())
    return summary


def local_port(name):
    return bool(re.fullmatch(r"COM[1-9][0-9]*", name, re.IGNORECASE) or
                re.fullmatch(r"/dev/cu\.[A-Za-z0-9][A-Za-z0-9._-]*", name))


def open_atom(name):
    if not local_port(name):
        raise ValueError("local COM1..COMn or /dev/cu.* serial port required; URLs forbidden")
    import serial
    options=dict(port=None,baudrate=115200,timeout=0.1,write_timeout=0.2)
    if sys.platform != "win32":
        options["exclusive"]=True
    port=serial.Serial(**options)
    try:
        # Configure before open to preserve the existing non-resetting sequence.
        port.dtr=False; port.rts=False; port.port=name
        port.open()
    except BaseException:
        port.close()
        raise
    return port


def parse_args(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--port",required=True)
    p.add_argument("--config",choices=sorted(CONFIGS),required=True)
    p.add_argument("--csv",type=Path,required=True)
    p.add_argument("--condition",required=True,help="e.g. atmosphere, calibration, pulse")
    p.add_argument("--trial",type=int,required=True)
    p.add_argument("--duration",type=float,default=10)
    p.add_argument("--dmm-v",type=float,help="manually measured steady G5-node reference, not a time-series sensor")
    p.add_argument("--append",action="store_true")
    p.add_argument("--electrical-check-confirmed",action="store_true",required=True)
    a=p.parse_args(argv)
    if not local_port(a.port):
        p.error("local COM1..COMn or /dev/cu.* serial port required; URLs forbidden")
    if not re.fullmatch(r"[a-z0-9_-]{1,40}",a.condition) or not 1<=a.trial<=100000:
        p.error("invalid condition/trial")
    if not math.isfinite(a.duration) or not 1<=a.duration<=3600:
        p.error("duration must be 1..3600 seconds")
    if a.dmm_v is not None and (not math.isfinite(a.dmm_v) or not 0<=a.dmm_v<=3.1):
        p.error("G5 reference outside 0..3.1 V: disconnect; record unsafe voltages in bench notes")
    return a


def main(argv=None):
    args=parse_args(argv)
    handle=None
    run=uuid.uuid4().hex[:16]
    summary=dict(status="partial",run_id=run,config=args.config,rows=0)
    try:
        port=open_atom(args.port)
        try:
            # No CSV or sidecar is created when port selection/opening fails.
            handle,writer=open_csv(args.csv,args.append)
            summary=capture(port,writer,handle,args,run)
        finally:
            port.close()
    except (Exception,KeyboardInterrupt) as error:
        summary["error"]=type(error).__name__+": "+str(error)
    finally:
        if handle is not None:
            handle.close()
    if handle is None:
        print(json.dumps(summary,indent=2,allow_nan=False))
        return 1
    with Path(str(args.csv)+".runs.jsonl").open("a",encoding="utf-8") as metadata:
        metadata.write(json.dumps(summary,allow_nan=False)+"\n")
    print(json.dumps(summary,indent=2,allow_nan=False))
    return 0 if summary["status"]=="complete" and summary.get("timing_ok",False) else 1


if __name__=="__main__":
    raise SystemExit(main())
