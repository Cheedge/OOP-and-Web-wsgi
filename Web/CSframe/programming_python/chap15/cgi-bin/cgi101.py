#!/usr/bin/python3
import cgi
from sys import version
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
# parse form data
print('Content-type: text/html\n')
# hdr plus blank line
print('<title>Reply Page</title>')
# html reply page
if not 'user' in form:
    print('<h1>Who are you?</h1>')
else:
    print('<h1>Hello <i>%s</i>!</h1>' % cgi.escape(form['user'].value))




    