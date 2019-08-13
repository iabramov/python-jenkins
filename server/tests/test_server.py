
import pytest
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from server import Server
from async_server import AsyncHTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests as req
import time
import datetime


class TestServerClass:
    """Server unit tests"""
    @pytest.fixture(scope='session',autouse=True)
    def http_server(self):
        httpd = AsyncHTTPServer()
        yield httpd  # provide the fixture value
        print("teardown httpd")
        httpd.stop(1)

    def test_put(self):
        resp = req.put("http://127.0.0.1:8080/hello/Basil", data = '( "dateOfBirth": "2014-05-01" )', headers={'Content-type': 'text/html'})
        assert 204==resp.status_code


    # A. If username's birthday is in N days: ( "message": "Hello, <username>! Your birthday is in N day(s)" } 
    # B. If username's birthday is today: ( "message": "Hello, <username>! Happy birthday!" }
    def test_get(self):
        resp = req.get("http://127.0.0.1:8080/hello/Basil")
        assert 200==resp.status_code

        date_of_birth = datetime.datetime.strptime("2014-05-01", '%Y-%m-%d').date()
        days = (datetime.date.today() - date_of_birth).days

        if days>0 :
            assert '( "message": "Hello, Basil! Your birthday is in %s day(s)" }' % str(days) == resp.text
        else :
            assert '( "message": "Hello, Basil! Happy birthday!" }' == resp.text

