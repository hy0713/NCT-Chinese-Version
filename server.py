"""Loopback-only static server; standard Python 3 library, no pip packages."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote
import argparse, threading, webbrowser

ROOT = Path(__file__).resolve().parent
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
    parser.add_argument('--port',type=int,default=8000)
    parser.add_argument('--open',action='store_true')
    options=parser.parse_args()
    url=f'http://localhost:{options.port}/campaign-trail/index.html'
    try: server=ThreadingHTTPServer(('127.0.0.1',options.port),Handler)
    except OSError as error: raise SystemExit(f'Cannot start localhost:{options.port}: {error}\nClose the other server or use --port 8001.')
    print(f'NCT: {url}\nPress Ctrl+C to stop.',flush=True)
    if options.open: threading.Timer(0.5,lambda:webbrowser.open(url)).start()
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
