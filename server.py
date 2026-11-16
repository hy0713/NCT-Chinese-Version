"""Loopback-only static server; standard Python 3 library, no pip packages."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote, urlsplit, parse_qs
import argparse, errno, secrets, threading, time, webbrowser

ROOT = Path(__file__).resolve().parent
PORT_FILE = ROOT / '.nct-port'


class BrowserSession:
    """Keep serving while a game page holds its local event-stream connection."""
    def __init__(self, close_delay=3, startup_timeout=90):
        self.token = secrets.token_urlsafe(24)
        self.close_delay, self.startup_timeout = close_delay, startup_timeout
        self.lock, self.stopped = threading.Lock(), threading.Event()
        self.clients, self.seen, self.closing = 0, False, False
        self.empty_since = time.monotonic()
        self.exit_code = 0

    def join(self):
        with self.lock:
            if self.closing: return False
            self.clients += 1
            self.seen = True
            return True

    def leave(self):
        with self.lock:
            self.clients -= 1
            if not self.clients: self.empty_since = time.monotonic()

    def watch(self, server):
        while not self.stopped.wait(0.25):
            with self.lock:
                delay = self.close_delay if self.seen else self.startup_timeout
                if self.clients or time.monotonic() - self.empty_since < delay: continue
                self.closing = True
                self.exit_code = 0 if self.seen else 1
            print('All NCT pages closed; stopping server.' if self.seen else
                  'No game page connected; stopping server. Check the browser and retry.', flush=True)
            server.shutdown()
            return

    def script(self):
        # Native EventSource reconnects without page timers. pagehide covers
        # reload/navigation; a closed/crashed browser also drops the connection.
        return ('''<script>
(() => {
  const url = '/_nct/lifetime?token=TOKEN';
  let stream = new EventSource(url);
  addEventListener('pagehide', () => stream.close());
  addEventListener('pageshow', event => { if (event.persisted) stream = new EventSource(url); });
})();
</script>'''.replace('TOKEN', self.token)).encode('utf-8')

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
        session = getattr(self.server, 'browser_session', None)
        request = urlsplit(self.path)
        if session and request.path == '/_nct/lifetime':
            token = parse_qs(request.query).get('token', [''])[0]
            if not secrets.compare_digest(token, session.token): self.send_error(403); return
            if not session.join(): self.send_error(503); return
            try:
                self.send_response(200)
                self.send_header('Content-Type', 'text/event-stream')
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                self.wfile.write(b'retry: 1000\n\n')
                self.wfile.flush()
                while not session.stopped.wait(1):
                    self.wfile.write(b': nct page connected\n\n')
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                pass  # Page/tab closure is the normal end of this stream.
            finally:
                session.leave()
            return
        if session and request.path in ('/campaign-trail/index.html', '/campaign-trail/'):
            body = (ROOT / 'campaign-trail/index.html').read_bytes()
            head = body.index(b'>', body.lower().index(b'<head')) + 1
            body = body[:head] + session.script() + body[head:]
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='NCT local HTTP server')
    parser.add_argument('--port',type=port_number,default=None,help='Explicit port; default selects and remembers an available port.')
    parser.add_argument('--open',action='store_true')
    parser.add_argument('--auto-close',action='store_true',help='Stop after the last game page closes; refreshes have a short grace period.')
    options=parser.parse_args()
    server=create_server(options.port)
    session = BrowserSession() if options.auto_close else None
    server.browser_session = session
    url=f'http://localhost:{server.server_port}/campaign-trail/index.html'
    print(f'NCT: {url}\nPress Ctrl+C to stop.',flush=True)
    if session:
        print('Close the last NCT tab to stop this server automatically.', flush=True)
        threading.Thread(target=session.watch, args=(server,), daemon=True).start()
    if options.open:
        opener = threading.Timer(0.5, webbrowser.open, args=(url,))
        opener.daemon = True
        opener.start()
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally:
        if session: session.stopped.set()
        server.server_close()
    if session: raise SystemExit(session.exit_code)
