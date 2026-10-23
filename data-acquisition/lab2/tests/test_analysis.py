"""Synthetic inputs stay in memory or TemporaryDirectory, never lab results."""
import contextlib
import csv
import importlib.util
import io
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest

PYTHON = Path(__file__).resolve().parents[1]/"src/python"
sys.path.insert(0, str(PYTHON))
import analyze
from logger import FIELDS

RUN = "0123456789abcdef"
OTHER = "fedcba9876543210"


def rows(run=RUN, config="raw", timestamps=None):
    times = timestamps if timestamps is not None else list(range(0, 200, 10))
    return [dict(zip(FIELDS, [t, 100+i%3, "", "", config, run, i, 0,
                             "", "", "", "pulse", 1, 0])) for i, t in enumerate(times)]


def write(path, records, complete=True):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader(); writer.writerows(records)
    captures = []
    for run in dict.fromkeys(r["run_id"] for r in records):
        subset = [r for r in records if r["run_id"] == run]
        captures.append(dict(run_id=run, config=subset[0]["config"], rows=len(subset),
                             status="complete" if complete else "partial", timing_ok=True))
    Path(str(path)+".runs.jsonl").write_text("\n".join(json.dumps(r) for r in captures)+"\n")


class AnalysisTests(unittest.TestCase):
    def load(self, records, complete=True):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"synthetic.csv"
            write(path, records, complete)
            return analyze.load([path])

    def test_no_input_creates_no_results(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()) as out:
            target = Path(tmp)/"results"
            self.assertEqual(analyze.main(["--out", str(target)]), 2)
            self.assertFalse(target.exists())
            self.assertIn("puuduvad", out.getvalue())

    def test_schema_is_exact(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"wrong.csv"; path.write_text("adc,t_ms\n1,10\n")
            with self.assertRaises(ValueError): analyze.load([path])

    def test_split_runs_and_100hz(self):
        runs = self.load(rows()+rows(OTHER, "opamp"))
        self.assertEqual(len(runs), 2)
        self.assertEqual(runs[RUN]["validator"].summary()["rate_hz"], 100)
        self.assertTrue(runs[RUN]["capture_complete"])
        self.assertEqual(runs[OTHER]["t"][0], 0)

    def test_rollover(self):
        run = self.load(rows(timestamps=[0xfffffff8, 2, 12]))[RUN]
        self.assertEqual(run["t"], [0, .01, .02])

    def test_invalid_adc_sequence_metadata_and_finite_dmm(self):
        for key, value in (("adc",4096), ("seq",3), ("condition","bad space"),
                           ("dmm_reference_v","nan"), ("p_kpa","1"), ("adc_clipped",1)):
            data = rows(); data[1][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError): self.load(data)

    def test_missing_samples_rejected(self):
        data = rows(); del data[2]
        with self.assertRaises(ValueError): self.load(data)

    def test_missed_and_jitter_reported(self):
        data = rows(timestamps=[0, 10, 30]); data[-1]["missed"] = 1
        run = self.load(data)[RUN]
        self.assertFalse(run["validator"].summary()["timing_ok"])

    def test_partial_is_preserved(self):
        self.assertFalse(self.load(rows(), False)[RUN]["capture_complete"])

    def test_missing_sidecar_not_complete(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"synthetic.csv"; write(path, rows())
            Path(str(path)+".runs.jsonl").unlink()
            self.assertFalse(analyze.load([path])[RUN]["capture_complete"])

    def test_stats_and_snr(self):
        self.assertEqual(analyze.stats([1,2,3])["std_sample"], 1)
        item = dict(t=[0,1,2,3,4,5])
        result = analyze.snr(item, dict(baseline_s=[0,2], plateau_s=[2,5]), [0,0,9,10,11,10])
        self.assertEqual(result["signal_pa"], 10)
        self.assertEqual(result["plateau_noise_std_pa"], 1)
        self.assertEqual(result["snr_db"], 20)
        with self.assertRaises(ValueError):
            analyze.snr(item, dict(baseline_s=[0,3], plateau_s=[2,5]), [0]*6)
        self.assertIsNone(analyze.snr(item, dict(baseline_s=[0,2], plateau_s=[2,5]), [0]*6)["snr_db"])

    def test_calibration_requires_evidence_range_and_config(self):
        entry = dict(config="raw", source="temporary test evidence", pa_per_code=-2,
                     offset_pa=1000, adc_range=[90,110])
        pressure, step = analyze.calibration(entry, [100,101], "raw")
        self.assertEqual((pressure,step), ([800,798],2))
        for values, config in (([111],"raw"),([100],"opamp")):
            with self.assertRaises(ValueError): analyze.calibration(entry,values,config)
        entry["source"] = ""
        with self.assertRaises(ValueError): analyze.calibration(entry,[100],"raw")

    @unittest.skipUnless(importlib.util.find_spec("numpy"), "numpy needed for spectra")
    def test_periodogram_peak_and_density(self):
        values = [1000*math.sin(2*math.pi*10*i/100) for i in range(100)]
        freq, power = analyze.spectrum(values,100)
        self.assertAlmostEqual(freq[power.argmax()],10)
        self.assertAlmostEqual(sum(power)*(freq[1]-freq[0]), .5, places=3)

    @unittest.skipUnless(importlib.util.find_spec("matplotlib"), "plot dependency required")
    def test_end_to_end_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            path = Path(tmp)/"synthetic.csv"; target = Path(tmp)/"output"
            write(path,rows()+rows(OTHER,"opamp"))
            self.assertEqual(analyze.main([str(path),"--out",str(target)]),0)
            report = json.loads((target/"summary.json").read_text())
            self.assertIn("calibration_todo",report["runs"][RUN])
            self.assertTrue((target/"adc_time.png").exists())
            self.assertEqual(analyze.main([str(path),"--out",str(target)]),2)

    @unittest.skipUnless(importlib.util.find_spec("matplotlib"), "plot dependency required")
    def test_calibrated_pipeline_in_temporary_directory(self):
        with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
            path = Path(tmp)/"synthetic.csv"; target = Path(tmp)/"output"
            data = rows()+rows(OTHER,"opamp")
            for row in data:
                row["adc"] += 10 if row["seq"] >= 10 else 0
            write(path,data)
            plan = dict(calibration={},windows={},spectrum_pairs=[dict(
                raw_run=RUN,opamp_run=OTHER,raw_s=[0,.1],opamp_s=[0,.1],protocol="synthetic")])
            for run,config in ((RUN,"raw"),(OTHER,"opamp")):
                plan["calibration"][run] = dict(config=config,source="synthetic test only",
                    pa_per_code=2,offset_pa=0,adc_range=[90,120])
                plan["windows"][run] = dict(baseline_s=[0,.08],plateau_s=[.1,.18])
            planfile = Path(tmp)/"plan.json"; planfile.write_text(json.dumps(plan))
            self.assertEqual(analyze.main([str(path),"--plan",str(planfile),"--out",str(target)]),0)
            report = json.loads((target/"summary.json").read_text())
            self.assertEqual(report["runs"][RUN]["pa_per_adc_step"],2)
            self.assertIsNotNone(report["runs"][RUN]["snr"]["snr_db"])
            self.assertTrue((target/"spectra_1.png").exists())

    @unittest.skipUnless(importlib.util.find_spec("numpy"), "numpy needed for spectra")
    def test_pair_checks_and_common_axes(self):
        runs = self.load(rows()+rows(OTHER,"opamp"))
        pair = dict(raw_run=RUN,opamp_run=OTHER,raw_s=[0,.1],opamp_s=[0,.1],protocol="synthetic test")
        calibrated = {r:item["adc"] for r,item in runs.items()}
        curves = analyze.compare(runs,pair,calibrated)
        self.assertEqual(list(curves[0][0]),list(curves[1][0]))
        pair["opamp_s"] = [0,.15]
        with self.assertRaises(ValueError): analyze.compare(runs,pair,calibrated)
        pair["opamp_s"] = [0,.1]; runs[RUN]["capture_complete"] = False
        with self.assertRaises(ValueError): analyze.compare(runs,pair,calibrated)


if __name__ == "__main__":
    unittest.main()
