#!/usr/bin/env python2
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SimpleHTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler 
import BaseHTTPServer

class CORSRequestHandler (SimpleHTTPRequestHandler):
    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        CGIHTTPRequestHandler.end_headers(self)

if __name__ == '__main__':
    BaseHTTPServer.test(CORSRequestHandler, BaseHTTPServer.HTTPServer)
