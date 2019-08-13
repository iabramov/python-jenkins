import time
import threading
from server import Server
from http.server import BaseHTTPRequestHandler, HTTPServer
from database import DB

class AsyncHTTPServer(object):
 
    def __init__(self):

        self.my_server=Server
        self.httpd = HTTPServer(('', 8080), Server)
        self._thread = threading.Thread(target=self.do_server_forever)
        self._thread.daemon = True
        self._thread.start()

    def do_server_forever(self):
        db = DB()
        self.httpd.serve_forever()

    def stop(self, timeout):
        self.httpd.socket.close()
        self._thread.join(timeout)
