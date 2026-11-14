"""Offline tests for opamp_retest.py: synthetic numbers and mocks only, no serial device."""
import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

SRC = Path(__file__).resolve().parents[1] / "src/python"
sys.path.insert(0, str(SRC))
spec = importlib.util.spec_from_file_location("opamp_retest_under_test", SRC / "opamp_retest.py")
rt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rt)


def hold(volts, n=40, wobble=2):
    code = round(volts / rt.VOLTS_PER_CODE)
    return [code + (i % (2 * wobble + 1)) - wobble for i in range(n)]


class FakeClock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        self.t += 0.05
        return self.t


class FakePort:
    def __init__(self, lines):
        self.lines = list(lines)

    def readline(self, _):
        return self.lines.pop(0) if self.lines else b""

    def reset_input_buffer(self):
        pass


class RetestTests(unittest.TestCase):
    def test_design_numbers(self):
        a, vref, exp = rt.expected()
        self.assertAlmostEqual(a, 1.186, places=3)
        self.assertAlmostEqual(vref, 0.428, places=3)
        self.assertAlmostEqual(exp["full_suction"], 0.30, places=3)
        self.assertAlmostEqual(exp["atmosphere"], 0.906, places=2)
        self.assertAlmostEqual(exp["full_blowing"], 2.767, places=2)

    def test_meter_line(self):
        self.assertEqual(rt.parse_meter_line("4658,1241,1.1213,143.30,-1.41\r\n"), (4658, 1241))
        self.assertIsNone(rt.parse_meter_line("t_ms,adc_raw,g5_volts,p_abs_kpa,p_rel_kpa"))
        self.assertIsNone(rt.parse_meter_line('{"t":1,"adc":2}'))
        self.assertIsNone(rt.parse_meter_line("1,5000,1.0,1.0,1.0"))

    def test_stats_uses_middle_of_hold(self):
        codes = [0] * 10 + [1000] * 30 + [4000] * 10
        s = rt.stats(codes)
        self.assertEqual(s["n"], 50)
        self.assertAlmostEqual(s["mean_code"], 1000)
        self.assertEqual((s["min_code"], s["max_code"]), (0, 4000))
        self.assertEqual(rt.stats([]), dict(n=0))

    def good(self):
        _, _, exp = rt.expected()
        return {k: rt.stats(hold(v)) for k, v in exp.items()}

    def test_good_board_passes(self):
        checks = rt.evaluate(self.good(), timing_ok=True)
        self.assertEqual({c[0] for c in checks}, {"PASS"}, checks)

    def test_old_fault_stuck_output_fails(self):
        stuck = {k: rt.stats(hold(0.5)) for k, _ in rt.CONDITIONS}
        failed = [c[1] for c in rt.evaluate(stuck) if c[0] == "FAIL"]
        self.assertIn("Output follows pressure", failed)
        self.assertIn("Output range", failed)

    def test_low_rail_and_high_end(self):
        r = self.good()
        r["full_suction"] = rt.stats(hold(0.017))
        r["full_blowing"] = rt.stats(hold(3.2))
        failed = [c[1] for c in rt.evaluate(r) if c[0] == "FAIL"]
        self.assertIn("Not stuck at the low end", failed)
        self.assertIn("Safe for G5 at the high end", failed)

    def test_noise_and_offset_only_warn(self):
        r = self.good()
        r["atmosphere"] = rt.stats(hold(1.25, n=205, wobble=20))
        checks = rt.evaluate(r)
        self.assertFalse([c for c in checks if c[0] == "FAIL"], checks)
        warned = [c[1] for c in checks if c[0] == "WARN"]
        self.assertIn("Noise at atmosphere", warned)
        self.assertIn("Close to design: atmosphere", warned)

    def test_too_few_samples(self):
        r = self.good()
        r["full_blowing"] = rt.stats(hold(2.7, n=3))
        self.assertEqual(rt.evaluate(r)[0][:2], ("FAIL", "Enough samples"))

    def test_detect_firmware(self):
        clock = FakeClock()
        self.assertEqual(rt.detect_firmware(FakePort([b"t_ms,adc_raw\n", b"100,900,0.8132,95.0,0.0\n"]), clock=clock), "meter")
        self.assertEqual(rt.detect_firmware(FakePort([b"# AUTO t_ms=1 adc=5\n"]), clock=clock), "da2")
        self.assertEqual(rt.detect_firmware(FakePort([]), seconds=0.2, clock=clock), "da2")

    def test_choose_port(self):
        self.assertEqual(rt.choose_port("COM7"), "COM7")
        with patch.object(rt, "find_ports", return_value=["COM5"]):
            self.assertEqual(rt.choose_port(None), "COM5")
        with patch.object(rt, "find_ports", return_value=["COM5", "COM9"]):
            self.assertEqual(rt.choose_port(None, ask=lambda _: "2"), "COM9")
        with patch.object(rt, "find_ports", return_value=[]):
            with self.assertRaises(SystemExit):
                rt.choose_port(None)

    def test_capture_meter_writes_rows(self):
        rows = []

        class W:
            def writerow(self, r):
                rows.append(r)

        class H:
            def flush(self):
                pass

        port = FakePort([b"10,1000,0.9035,90.0,0.0\n", b"garbage\n", b"20,1002,0.9053,90.1,0.1\n"])
        codes = rt.capture_meter(port, W(), H(), "atmosphere", 1, 1.0, clock=FakeClock())
        self.assertEqual(codes, [1000, 1002])
        self.assertEqual(rows[0]["condition"], "atmosphere")


if __name__ == "__main__":
    unittest.main()
