"""
Implement an HTTP web server in Python that knows how to run server-side
CGI scripts coded in Python; serves files and scripts from current working
dir; Python scripts must be stored in webdir\cgi-bin or webdir\htbin;
"""
import os, sys
from http.server import HTTPServer, CGIHTTPRequestHandler
webdir = '.'
port = 8000
# where your html files and cgi-bin script directory live
# default http://localhost/, else use http://localhost:xxxx/
# print(os.getcwd())
os.chdir(webdir)
# print(os.getcwd())
# run in HTML root dir
srvraddr = ("", port)
# my hostname, portnumber
srvrobj = HTTPServer(srvraddr, CGIHTTPRequestHandler)
srvrobj.serve_forever()
# run as perpetual daemon