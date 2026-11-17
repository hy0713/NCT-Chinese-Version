"""Targeted startup regression; no external network or game data changes."""
import argparse, errno, importlib.util, tempfile, threading, unittest
from urllib.request import urlopen
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch, Mock

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

    def test_localization_cache_policy_over_real_http(self):
        server=module.create_server(0)
        server.browser_session=module.BrowserSession()
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            base=f'http://127.0.0.1:{server.server_port}'
            for path in ['/localization/i18n.js','/localization/zh-CN.json?v=test','/localization/layout.css']:
                with urlopen(base+path) as response:
                    self.assertEqual(response.status,200)
                    self.assertEqual(response.headers.get('Cache-Control'),'no-cache')
            with urlopen(base+'/campaign-trail/index.html') as response:
                self.assertEqual(response.headers.get('Cache-Control'),'no-store')
        finally:
            server.shutdown();server.server_close();thread.join()

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

    def test_browser_never_connects_stops_with_failure_instead_of_orphaning(self):
        session=module.BrowserSession(startup_timeout=0)
        server=SimpleNamespace(shutdown=Mock())
        session.watch(server)
        server.shutdown.assert_called_once()
        self.assertEqual(session.exit_code,1)
        self.assertFalse(session.join())

    def test_last_disconnected_browser_stops_successfully(self):
        session=module.BrowserSession(close_delay=0)
        self.assertTrue(session.join())
        session.leave()
        server=SimpleNamespace(shutdown=Mock())
        session.watch(server)
        server.shutdown.assert_called_once()
        self.assertEqual(session.exit_code,0)

if __name__=='__main__':unittest.main()
