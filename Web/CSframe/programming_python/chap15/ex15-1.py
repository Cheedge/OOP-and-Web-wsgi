import os, sys
from http.server import HTTPServer, CGIHTTPRequestHandler
webdir = '.'
port = 1234
# where your HTML files and cgi-bin script directory live
# http://servername/ if 80, else use http://servername:xxxx/
if len(sys.argv) > 1: webdir = sys.argv[1]
if len(sys.argv) > 2: port = int(sys.argv[2])
print('webdir "%s", port %s' % (webdir, port))
# command-line args
# else default ., 80
os.chdir(webdir)
# run in HTML root dir
srvraddr = ('', port)
# my hostname, portnumber
srvrobj = HTTPServer(srvraddr, CGIHTTPRequestHandler)
print(srvrobj)
srvrobj.serve_forever()
# serve clients till exit