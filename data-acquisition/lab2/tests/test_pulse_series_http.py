"""HttpPump against a local fake mg400-base; no robot or serial device is touched."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import sys
import threading
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src/python"))
import pulse_series  # noqa: E402


class FakeBase(BaseHTTPRequestHandler):
    config = {"blow_do": 1, "suck_do": 2}
    ok = True
    calls = []

    def _reply(self, obj):
        body = json.dumps(obj).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    def do_GET(self):
        self._reply(self.config if self.path == "/api/config" else {})

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        FakeBase.calls.append((self.path, body))
        self._reply({"ok": FakeBase.ok, "errid": 0 if FakeBase.ok else -1})

    def log_message(self, *args):
        pass


class HttpPumpTests(unittest.TestCase):
    def setUp(self):
        FakeBase.calls, FakeBase.ok, FakeBase.config = [], True, {"blow_do": 1, "suck_do": 2}
        self.server = HTTPServer(("127.0.0.1", 0), FakeBase)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"

    def tearDown(self):
        self.server.shutdown(); self.server.server_close()

    def test_pump_modes_post_to_api_pump(self):
        pump = pulse_series.HttpPump(self.url)
        for mode in ("blow", "off", "suck", "off"):
            pump.pump(mode)
        self.assertEqual(FakeBase.calls, [("/api/pump", {"mode": m}) for m in ("blow", "off", "suck", "off")])

    def test_refused_command_raises(self):
        pump = pulse_series.HttpPump(self.url)
        FakeBase.ok = False
        with self.assertRaises(RuntimeError):
            pump.pump("blow")

    def test_different_do_mapping_is_rejected(self):
        FakeBase.config = {"blow_do": 2, "suck_do": 1}
        with self.assertRaises(RuntimeError):
            pulse_series.HttpPump(self.url)

    def test_dry_run_sends_nothing(self):
        pump = pulse_series.HttpPump("http://127.0.0.1:1", dry_run=True)
        pump.pump("blow")
        self.assertEqual(FakeBase.calls, [])


if __name__ == "__main__":
    unittest.main()
