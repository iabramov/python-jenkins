# Design and code a simple "Hello World" application that exposes the following HTTP-based APIs: 

# Description: Saves/updates the given user's name and date of birth in the database. 
# Request: PUT /hello/<username> ( "dateOfBirth": "YYYY-MM-DD" ) 
# Response: 204 No Content
 
# Note:
# <usemame> must contains only letters. 
# YYYY-MM-DD must be a date before the today date. 

# Description: Returns hello birthday message for the given user 
# Request: Get /hello/<username> 
# Response: 200 OK 

# Response Examples: 
# A. If username's birthday is in N days: ( "message": "Hello, <username>! Your birthday is in N day(s)" } 
# B. If username's birthday is today: ( "message": "Hello, <username>! Happy birthday!" } 

# Note: Use storage/database of your choice. The code should have at least one unit test. 

from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import json
import cgi
import sqlite3
import datetime
from urllib.parse import urlparse, parse_qs
# from  os.path import split
import os.path
from database import DB
import sys

    # Table mapping response codes to messages; entries have the
    # form {code: (shortmessage, longmessage)}.
    # See RFC 2616.
responses = {
    100: ('Continue', 'Request received, please continue'),
    101: ('Switching Protocols',
          'Switching to new protocol; obey Upgrade header'),
    200: ('OK', 'Request fulfilled, document follows'),
    201: ('Created', 'Document created, URL follows'),
    202: ('Accepted',
          'Request accepted, processing continues off-line'),
    203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
    204: ('No Content', 'Request fulfilled, nothing follows'),
    205: ('Reset Content', 'Clear input form for further input.'),
    206: ('Partial Content', 'Partial content follows.'),
    300: ('Multiple Choices',
          'Object has several resources -- see URI list'),
    301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
    302: ('Found', 'Object moved temporarily -- see URI list'),
    303: ('See Other', 'Object moved -- see Method and URL list'),
    304: ('Not Modified',
          'Document has not changed since given time'),
    305: ('Use Proxy',
          'You must use proxy specified in Location to access this '
          'resource.'),
    307: ('Temporary Redirect',
          'Object moved temporarily -- see URI list'),
    400: ('Bad Request',
          'Bad request syntax or unsupported method'),
    401: ('Unauthorized',
          'No permission -- see authorization schemes'),
    402: ('Payment Required',
          'No payment -- see charging schemes'),
    403: ('Forbidden',
          'Request forbidden -- authorization will not help'),
    404: ('Not Found', 'Nothing matches the given URI'),
    405: ('Method Not Allowed',
          'Specified method is invalid for this resource.'),
    406: ('Not Acceptable', 'URI not available in preferred format.'),
    407: ('Proxy Authentication Required', 'You must authenticate with '
          'this proxy before proceeding.'),
    408: ('Request Timeout', 'Request timed out; try again later.'),
    409: ('Conflict', 'Request conflict.'),
    410: ('Gone',
          'URI no longer exists and has been permanently removed.'),
    411: ('Length Required', 'Client must specify Content-Length.'),
    412: ('Precondition Failed', 'Precondition in headers is false.'),
    413: ('Request Entity Too Large', 'Entity is too large.'),
    414: ('Request-URI Too Long', 'URI is too long.'),
    415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
    416: ('Requested Range Not Satisfiable',
          'Cannot satisfy request range.'),
    417: ('Expectation Failed',
          'Expect condition could not be satisfied.'),
    500: ('Internal Server Error', 'Server got itself in trouble'),
    501: ('Not Implemented',
          'Server does not support this operation'),
    502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
    503: ('Service Unavailable',
          'The server cannot process the request due to a high load'),
    504: ('Gateway Timeout',
          'The gateway server did not receive a timely response'),
    505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
    }

"""Example HTTP API server module"""
# https://stackoverflow.com/questions/18444395/basehttprequesthandler-with-custom-instance

class Server(BaseHTTPRequestHandler):
    """Simple HTTP API server"""
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
    
    def _set_headers(self, response_code, headers):

        try:
            short_msg, long_msg = responses[response_code]
        except KeyError:
            short_msg, long_msg = '???', '???'

      #   if message is None:
      #       message = short_msg

        self.send_response(response_code)
        self.send_header(short_msg,long_msg)

        for k, v in headers.items():
            self.send_header(k, v)

        self.end_headers()

    def _send_204(self):
        self.send_response(204)
        self.end_headers()

    def _send_200(self):
        self.send_response(200)
        # or text/plain; charset=us-ascii
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()
        
    def parse_request_path(self, path):
      """Parse a request path & validate"""
      splitted_path = os.path.split(path)
      if len(splitted_path)>2 :
          raise Exception('Path should conform /hello/<username> pattern. %s breaks this rule' % username)

      username=splitted_path[1]

      if ''==username :
        raise Exception('Path should conform /hello/<username> pattern. %s breaks this rule' % username)

      # re.search('[a-zA-Z]', username) - less fast
      if not any(c.isalpha() for c in username) :
          raise Exception('<username> must contains only letters. %s does not conform with this rule' % username)

      return username


    def get_greetings(self, username, days):
        """Get greetings"""
        if days>0 :
            return '( "message": "Hello, %s! Your birthday is in %s day(s)" }' % (username, str(days))
        else :
            return '( "message": "Hello, %s! Happy birthday!" }' % username


    # Description: Returns hello birthday message for the given user 
    # Request: Get /hello/<username> 
    # Response: 200 OK 
    # Response Examples: 
    # A. If username's birthday is in N days: ( "message": "Hello, <username>! Your birthday is in N day(s)" } 
    # B. If username's birthday is today: ( "message": "Hello, <username>! Happy birthday!" }
    def do_GET(self):
        try:
            # parse a request path & validate
            username = self.parse_request_path(self.path)

            c = DB.conn.cursor()

            # Read a user info
            user_cursor = c.execute("""SELECT date_of_birth 
            FROM user_test 
            WHERE username = '%s' 
            """ % username)

            user = user_cursor.fetchone()

            if None == user :
                raise Exception('No username %s found in database.' % username)
            
            today = datetime.date.today()
            date_of_birth = datetime.datetime.strptime(user[0], '%Y-%m-%d').date()
            next_birthday = datetime.datetime(today.year+1,date_of_birth.month,date_of_birth.day).date()
            days = (next_birthday - today).days

            response = self.get_greetings(username, days)

            self._send_200()
            self.wfile.write(response.encode())
        except Exception as e:
            print("Error {0}".format(str(e.args[0])).encode("utf-8"))
        except:
            print("Unexpected error:", sys.exc_info()[0])

    # Description: Saves/updates the given user's name and date of birth in the database. 
    # Request: PUT /hello/<username> ( "dateOfBirth": "YYYY-MM-DD" ) 
    # Response: 204 No Content
    # Note:
    # <usemame> must contains only letters. 
    # YYYY-MM-DD must be a date before the today date. 
    # https://github.com/enthought/Python-2.7.3/blob/master/Lib/BaseHTTPServer.py
    def do_PUT(self):
      #   ctype, pdict = cgi.parse_header(self.headers['content-type'])

        try:
            # read the message and convert it into a python dictionary
            length = int(self.headers['content-length'])

            raw_message = self.rfile.read(length)
            raw_message = raw_message.decode('utf8').replace("(", "{").replace(")", "}")
            message = json.loads(raw_message.encode())

            # parse a request path & validate
            username  = self.parse_request_path(self.path)

            date_of_birth = datetime.datetime.strptime(message["dateOfBirth"], '%Y-%m-%d').date()

            if datetime.date.today() <= date_of_birth :
                raise Exception('%s must be a date before the today date.' % date_of_birth.strftime('%Y-%m-%d'))

            c = DB.conn.cursor()

            # Upsert a user
            query = """INSERT OR REPLACE INTO user_test (username, date_of_birth) 
            VALUES ('%s', '%s')
            """ % (username,date_of_birth.strftime('%Y-%m-%d'))

            try:
                c.execute(query)
                DB.conn.commit()
            except sqlite3.Error as e:
                print("An error occurred:", e.args[0])

            self._send_204()
        except Exception as e:
            print("Error {0}".format(str(e.args[0])).encode("utf-8"))
        except:
            print("Unexpected error:", sys.exc_info()[0])
