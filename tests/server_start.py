"""Targeted startup regression; no external network or game data changes."""
import argparse, errno, importlib.util, tempfile, unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('nct_server',ROOT/'server.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class Startup(unittest.TestCase):
    def setUp(self):
        (ROOT/'.test-artifacts').mkdir(exist_ok=True)
        folder=Path(tempfile.mkdtemp(prefix='server-start-',dir=ROOT/'.test-artifacts'))
        self.port_patch=patch.object(module,'PORT_FILE',folder/'.nct-port');self.port_patch.start()
        self.addCleanup(self.port_patch.stop)

    def test_reserved_default_chooses_and_remembers_available_port(self):
        server=SimpleNamespace(server_port=18080)
        with patch.object(module,'ThreadingHTTPServer',side_effect=[PermissionError(errno.EACCES,'reserved by Windows'),server]) as bind:
            self.assertIs(module.create_server(),server)
            self.assertEqual([call.args[0] for call in bind.call_args_list],[('127.0.0.1',8000),('127.0.0.1',18080)])
        self.assertEqual(module.preferred_port(),18080)
        with patch.object(module,'ThreadingHTTPServer',return_value=server) as bind:
            module.create_server();self.assertEqual(bind.call_args.args[0],('127.0.0.1',18080))

    def test_occupied_saved_port_can_choose_new_port(self):
        module.PORT_FILE.write_text('18080')
        with patch.object(module,'ThreadingHTTPServer',side_effect=[OSError(errno.EADDRINUSE,'occupied'),PermissionError(errno.EACCES,'reserved'),SimpleNamespace(server_port=28080)]):
            self.assertEqual(module.create_server().server_port,28080)

    def test_explicit_port_failure_is_reported_without_switching(self):
        with patch.object(module,'ThreadingHTTPServer',side_effect=PermissionError(errno.EACCES,'reserved')) as bind:
            with self.assertRaises(SystemExit):module.create_server(8000)
            self.assertEqual(bind.call_count,1)
        self.assertFalse(module.PORT_FILE.exists())

    def test_unexpected_os_error_is_not_hidden(self):
        with patch.object(module,'ThreadingHTTPServer',side_effect=OSError(errno.EMFILE,'too many files')):
            with self.assertRaises(OSError):module.create_server()

    def test_cli_range_and_os_selected_port(self):
        for value in ['-1','65536','invalid']:
            with self.assertRaises(argparse.ArgumentTypeError):module.port_number(value)
        self.assertEqual(module.port_number('0'),0)
        with patch.object(module,'ThreadingHTTPServer',return_value=SimpleNamespace(server_port=49123)):
            self.assertEqual(module.create_server(0).server_port,49123)

if __name__=='__main__':unittest.main()
