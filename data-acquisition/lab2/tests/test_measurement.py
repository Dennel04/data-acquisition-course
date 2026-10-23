"""Software-only synthetic samples in memory/temp directories, never real data."""
import csv
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from types import SimpleNamespace
import unittest

LAB=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("da2_logger",LAB/"src/python/logger.py")
logger=importlib.util.module_from_spec(spec); spec.loader.exec_module(logger)
RUN="0123456789abcdef"


def sample(t=0,seq=0,config="raw",**changes):
    obj=dict(t=t,adc=1234,p=None,pump=None,config=config,run=RUN,seq=seq,missed=0)
    obj.update(changes)
    return obj


def encoded(obj):
    return json.dumps(obj).encode()+b"\n"


class Port:
    def __init__(self,lines): self.lines=iter(lines); self.writes=[]
    def reset_input_buffer(self): pass
    def write(self,data): self.writes.append(data); return len(data)
    def readline(self,n): return next(self.lines,b"")


def clock(step=0.001):
    now=[0]
    def get(): now[0]+=step; return now[0]
    return get


class MeasurementTests(unittest.TestCase):
    def test_unavailable_fields_are_blank_not_fake_pressure(self):
        row=logger.Rows("raw",RUN).accept(sample())
        for key in ("p_kpa","pump","voltage_v"): self.assertEqual(row[key],"")
        self.assertEqual(row["adc"],1234)

    def test_explicit_config_and_run(self):
        for config in ("raw","opamp"):
            self.assertEqual(logger.Rows(config,RUN).accept(sample(config=config))["config"],config)
        for config in ("", "RAW", "unknown"):
            with self.assertRaises(ValueError): logger.Rows(config,RUN)

    def test_config_cannot_change_mid_run(self):
        rows=logger.Rows("raw",RUN)
        with self.assertRaises(ValueError): rows.accept(sample(config="opamp"))

    def test_reboot_or_other_run_is_rejected(self):
        with self.assertRaises(ValueError): logger.Rows("raw",RUN).accept(sample(run="fedcba9876543210"))

    def test_adc_and_timestamp_types_bounds(self):
        for changes in ({"adc":-1},{"adc":4096},{"adc":True},{"adc":1.5},{"t":-1},{"t":True}):
            with self.subTest(changes=changes),self.assertRaises(ValueError):
                logger.Rows("raw",RUN).accept(sample(**changes))

    def test_adc_rails_flagged_without_pressure_claim(self):
        for adc in (0,4095):
            row=logger.Rows("raw",RUN).accept(sample(adc=adc))
            self.assertEqual(row["adc_clipped"],1)
            self.assertEqual(row["p_kpa"],"")

    def test_missing_duplicate_and_backwards_time(self):
        for next_sample in (sample(10,0),sample(10,2),sample(0,1),sample(600,1)):
            rows=logger.Rows("raw",RUN); rows.accept(sample())
            with self.assertRaises(ValueError): rows.accept(next_sample)

    def test_millis_rollover_is_not_a_reset(self):
        rows=logger.Rows("raw",RUN)
        rows.accept(sample(0xfffffff8,0)); rows.accept(sample(2,1))
        self.assertEqual(rows.elapsed,10)

    def test_missed_slots_and_jitter_not_reported_as_pass(self):
        rows=logger.Rows("raw",RUN)
        rows.accept(sample()); rows.accept(sample(20,1,missed=1))
        self.assertFalse(rows.summary()["timing_ok"])
        self.assertEqual(rows.summary()["missed"],1)

    def test_unexpected_pump_or_pressure_refused(self):
        for changes in ({"p":1.0},{"pump":0},{"cmd":"pump"}):
            with self.assertRaises(ValueError): logger.Rows("raw",RUN).accept(sample(**changes))

    def test_partial_malformed_or_diagnostic_frame_rejected(self):
        for data in (b"{",b"{}",b"# serial_overrun\n",b"[]\n",b"x"*513+b"\n",b"\xff\n"):
            with self.assertRaises((ValueError,UnicodeError)): logger.decode(data)

    def test_csv_never_overwrites_and_append_preserves_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"synthetic.csv"
            handle,writer=logger.open_csv(path,False)
            row=logger.Rows("raw",RUN).accept(sample()); writer.writerow(row); handle.close()
            with self.assertRaises(FileExistsError): logger.open_csv(path,False)
            handle,writer=logger.open_csv(path,True)
            writer.writerow(logger.Rows("opamp",RUN).accept(sample(config="opamp")));handle.close()
            with path.open() as handle:
                data=list(csv.DictReader(handle))
            self.assertEqual([r["config"] for r in data],["raw","opamp"])

    def test_wrong_csv_header_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"synthetic.csv";path.write_text("t,adc\n1,2\n")
            with self.assertRaises(ValueError):logger.open_csv(path,True)

    def test_capture_count_and_dmm_metadata(self):
        ack=dict(event="started",firmware="DA2_MEASURE_V1",run=RUN,config="raw",
                 period_ms=10,adc_pin=5,adc_bits=12,adc_samples=8,calibrated=False)
        port=Port([encoded(ack)]+[encoded(sample(i*10,i)) for i in range(101)])
        args=SimpleNamespace(config="raw",condition="calibration",trial=1,duration=1,dmm_v=1.234)
        handle=io.StringIO();writer=csv.DictWriter(handle,fieldnames=logger.FIELDS);writer.writeheader()
        summary=logger.capture(port,writer,handle,args,RUN,clock())
        data=list(csv.DictReader(io.StringIO(handle.getvalue())))
        self.assertEqual(summary["status"],"complete")
        self.assertEqual(len(data),summary["rows"])
        self.assertEqual(len(data),101)
        self.assertEqual(summary["rate_hz"],100)
        self.assertTrue(summary["timing_ok"])
        self.assertEqual(data[0]["dmm_reference_v"],"1.234")
        self.assertEqual(data[0]["voltage_v"],"")
        self.assertEqual(json.loads(port.writes[0])["cmd"],"measure_start")
        self.assertEqual(json.loads(port.writes[-1])["cmd"],"measure_stop")

    def test_append_refuses_missing_final_newline(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"synthetic.csv"
            path.write_text(",".join(logger.FIELDS))
            with self.assertRaises(ValueError): logger.open_csv(path,True)

    def test_ack_then_missing_samples_times_out_without_actuator_command(self):
        ack=dict(event="started",firmware="DA2_MEASURE_V1",run=RUN,config="raw",
                 period_ms=10,adc_pin=5,adc_bits=12,adc_samples=8,calibrated=False)
        args=SimpleNamespace(config="raw",condition="atmosphere",trial=1,duration=1,dmm_v=None)
        handle=io.StringIO();writer=csv.DictWriter(handle,fieldnames=logger.FIELDS)
        port=Port([encoded(ack)])
        summary=logger.capture(port,writer,handle,args,RUN,clock(0.2))
        self.assertEqual(summary["status"],"partial")
        self.assertIn("500 ms",summary["error"])
        self.assertEqual([json.loads(p)["cmd"] for p in port.writes],["measure_start","measure_stop"])

    def test_no_ack_and_sample_watchdog_leave_partial(self):
        args=SimpleNamespace(config="raw",condition="atmosphere",trial=1,duration=1,dmm_v=None)
        handle=io.StringIO();writer=csv.DictWriter(handle,fieldnames=logger.FIELDS)
        port=Port([])
        summary=logger.capture(port,writer,handle,args,RUN,clock(0.2))
        self.assertEqual(summary["status"],"partial")
        self.assertEqual(summary["rows"],0)
        self.assertEqual(json.loads(port.writes[-1])["cmd"],"measure_stop")

    def test_sampling_clock_actual_header(self):
        compiler=shutil.which("c++");self.assertIsNotNone(compiler)
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/"test.cpp";binary=Path(tmp)/"test"
            source.write_text('''#include <cassert>
#include "sampling.h"
int main(){acquisition::Clock c;c.start(100);assert(!c.due(99));assert(c.due(100));
assert(!c.due(100));assert(!c.due(109));assert(c.due(110));assert(c.due(145));
assert(c.missed==2);assert(c.next==150);assert(!c.due(145));
c.start(0xfffffff8u);assert(c.due(0xfffffff8u));assert(!c.due(1));assert(c.due(2));
assert(acquisition::validConfig("raw"));assert(acquisition::validConfig("opamp"));
assert(!acquisition::validConfig("pump"));assert(!acquisition::validRun("bad"));}''')
            subprocess.run([compiler,"-std=c++11","-I",str(LAB/"src/firmware/include"),str(source),"-o",str(binary)],check=True,capture_output=True)
            subprocess.run([str(binary)],check=True,capture_output=True)

    def test_source_has_no_network_pump_or_saved_settings(self):
        main=(LAB/"src/firmware/src/main.cpp").read_text()
        logger_source=(LAB/"src/python/logger.py").read_text()
        for token in ("WiFi", "Preferences", "LittleFS", "digitalWrite", "analogWrite", "OUTPUT", "HTTPClient", "pump::"):
            self.assertNotIn(token,main)
        for token in ("requests", "urllib", "socket", '"cmd":"mode"', '"cmd":"stop"'):
            self.assertNotIn(token,logger_source)
        self.assertIn("pinMode(kAdcPin,INPUT)",main)
        self.assertIn("analogReadResolution(12)",main)
        self.assertIn("ADC_11db",main)
        self.assertIn("port.dtr=False; port.rts=False",logger_source)


if __name__=="__main__":unittest.main()
