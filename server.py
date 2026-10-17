"""Loopback-only static server; standard Python 3 library, no pip packages."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote
import argparse, errno, threading, webbrowser

ROOT = Path(__file__).resolve().parent
PORT_FILE = ROOT / '.nct-port'

def port_number(value):
    try: port = int(value)
    except ValueError: raise argparse.ArgumentTypeError('Port must be a number from 0 to 65535.')
    if not 0 <= port <= 65535:
        raise argparse.ArgumentTypeError('Port must be from 0 to 65535 (0 chooses a free port).')
    return port

def preferred_port():
    try:
        port = int(PORT_FILE.read_text(encoding='ascii').strip())
        if not 1 <= port <= 65535: raise ValueError('saved port out of range')
        return port
    except FileNotFoundError: return 8000
    except (OSError, ValueError) as error:
        print(f'Cannot read saved port ({error}); trying default ports.', flush=True)
        return 8000

def create_server(port=None):
    # Bind the actual server directly; no probe/close/rebind race.
    ports = [port] if port is not None else list(dict.fromkeys([preferred_port(), 8000, 18080, 28080, 0]))
    for candidate in ports:
        try: server = ThreadingHTTPServer(('127.0.0.1', candidate), Handler)
        except OSError as error:
            if port is not None:
                raise SystemExit(f'Cannot start localhost:{port}: {error}\nRun without --port to select an available port automatically.') from error
            if error.errno not in (errno.EACCES, errno.EADDRINUSE) and getattr(error, 'winerror', None) not in (10013, 10048):
                raise
            print(f'Local port {candidate} is unavailable: {error}', flush=True)
            last_error = error
            continue
        if port is None:
            try: PORT_FILE.write_text(str(server.server_port)+'\n', encoding='ascii')
            except OSError as error:
                print(f'Cannot remember the selected port: {error}', flush=True)
        return server
    raise SystemExit(f'Cannot start a local HTTP server: {last_error}')

class Handler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map,
                      '.js':'application/javascript; charset=utf-8',
                      '.json':'application/json; charset=utf-8',
                      '.html':'text/html; charset=utf-8',
                      '.css':'text/css; charset=utf-8'}
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT),**kwargs)
    def do_GET(self):
        if any(part.startswith('.') for part in unquote(self.path.split('?')[0]).split('/') if part):
            self.send_error(404); return
        super().do_GET()

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='NCT local HTTP server')
    parser.add_argument('--port',type=port_number,default=None,help='Explicit port; default selects and remembers an available port.')
    parser.add_argument('--open',action='store_true')
    options=parser.parse_args()
    server=create_server(options.port)
    url=f'http://localhost:{server.server_port}/campaign-trail/index.html'
    print(f'NCT: {url}\nPress Ctrl+C to stop.',flush=True)
    if options.open: threading.Timer(0.5,lambda:webbrowser.open(url)).start()
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
