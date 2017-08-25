#!/usr/bin/env python2
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SimpleHTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler 

import BaseHTTPServer
import CGIHTTPServer 
import cgitb; cgitb.enable()  ## This line enables CGI error reporting
 
server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler

server_address = ("", 8000)
handler.cgi_directories = ["/"]

print handler.cgi_directories
 
httpd = server(server_address, handler)
httpd.serve_forever()
handler.send_header('Access-Control-Allow-Origin', '*')
handler.end_headers()
server.serve_forever()
