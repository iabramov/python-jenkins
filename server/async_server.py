import time
import threading
from server import Server
from http.server import BaseHTTPRequestHandler, HTTPServer
from database import DB

class AsyncHTTPServer(object):
 
    def __init__(self, asyncronous=True ):

        self.asyncronous = asyncronous
        self.my_server=Server
        self.httpd = HTTPServer(('', 8080), Server)

        if self.asyncronous :
            self._thread = threading.Thread(target=self.do_server_forever)
            self._thread.daemon = True
            self._thread.start()
        else :
            self.do_server_forever()

    def do_server_forever(self):
        db = DB()
        self.httpd.serve_forever()

    def stop(self, timeout):
        self.httpd.socket.close()
        if self.asyncronous :
            self._thread.join(timeout)
