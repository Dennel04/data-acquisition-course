"""Port validation/opening tests use mocks only; no serial device is accessed."""
import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

SOURCE=Path(__file__).resolve().parents[1]/"src/python/logger.py"
spec=importlib.util.spec_from_file_location("logger_ports_under_test",SOURCE)
logger=importlib.util.module_from_spec(spec); spec.loader.exec_module(logger)


def args(port, path, append=False):
    values=["--port",port,"--config","raw","--csv",str(path),"--condition","atmosphere",
            "--trial","1","--duration","10","--electrical-check-confirmed"]
    return values+["--append"] if append else values


class LoggerPortTests(unittest.TestCase):
    def test_local_names(self):
        for name in ("COM1","COM3","COM10","COM123","com3","Com10",
                     "/dev/cu.usbmodem1301","/dev/cu.usbserial-123","/dev/cu.Bluetooth-Incoming-Port"):
            with self.subTest(name=name): self.assertTrue(logger.local_port(name))

    def test_invalid_names_and_urls(self):
        for name in ("COM0","COM01","COM-1","COM","COM1:","COM1/x"," COM3","COM3 ",
                     "COM3\n","COM３","/dev/cu.","/dev/cu../tty","/dev/cu.a/../x",
                     "/dev/ttyUSB0","/dev/cu.a\n","socket://localhost:1234",
                     "rfc2217://host:1234","loop://","COM3://host","/dev/cu.socket://host",
                     r"\\.\COM3",""):
            with self.subTest(name=name): self.assertFalse(logger.local_port(name))

    def test_invalid_port_creates_no_csv_or_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"never-created.csv"
            for port in ("COM0","socket://host:1234","/dev/cu.a/other"):
                with self.subTest(port=port), contextlib.redirect_stderr(io.StringIO()), \
                        patch.object(logger,"open_atom") as open_port:
                    with self.assertRaises(SystemExit): logger.main(args(port,path))
                    open_port.assert_not_called()
                    self.assertEqual(list(Path(tmp).iterdir()),[])

    def test_windows_and_macos_open_options(self):
        for platform,name,exclusive in (("win32","COM10",False),("darwin","/dev/cu.usbmodem1301",True)):
            with self.subTest(platform=platform):
                port=Mock(); constructor=Mock(return_value=port)
                with patch.dict(sys.modules,{"serial":SimpleNamespace(Serial=constructor)}), \
                        patch.object(logger.sys,"platform",platform):
                    self.assertIs(logger.open_atom(name),port)
                options=constructor.call_args.kwargs
                self.assertIsNone(options["port"])
                self.assertEqual(options["baudrate"],115200)
                self.assertEqual("exclusive" in options,exclusive)
                if exclusive: self.assertTrue(options["exclusive"])
                self.assertFalse(port.dtr); self.assertFalse(port.rts)
                self.assertEqual(port.port,name)
                port.open.assert_called_once_with()

    def test_open_failure_creates_no_files_and_closes_port(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"never-created.csv"
            port=Mock(); port.open.side_effect=OSError("port unavailable or busy")
            with patch.dict(sys.modules,{"serial":SimpleNamespace(Serial=Mock(return_value=port))}), \
                    contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(logger.main(args("COM3",path)),1)
            port.close.assert_called_once_with()
            self.assertEqual(list(Path(tmp).iterdir()),[])
            self.assertIn("port unavailable",output.getvalue())

    def test_open_failure_preserves_existing_append_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"existing.csv"; path.write_bytes(b"unchanged evidence\n")
            with patch.object(logger,"open_atom",side_effect=OSError("busy")), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(logger.main(args("COM3",path,append=True)),1)
            self.assertEqual(path.read_bytes(),b"unchanged evidence\n")
            self.assertFalse(Path(str(path)+".runs.jsonl").exists())

    def test_success_opens_port_before_csv_and_closes_both(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"synthetic.csv"; port=Mock()
            def opened(name):
                self.assertFalse(path.exists())
                return port
            def captured(port,writer,handle,parsed,run):
                self.assertTrue(path.exists())
                return dict(status="complete",timing_ok=True,rows=0,run_id=run)
            with patch.object(logger,"open_atom",side_effect=opened), \
                    patch.object(logger,"capture",side_effect=captured), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(logger.main(args("COM3",path)),0)
            port.close.assert_called_once_with()
            self.assertEqual(path.read_text().strip(),",".join(logger.FIELDS))
            self.assertTrue(Path(str(path)+".runs.jsonl").exists())


if __name__=="__main__": unittest.main()
