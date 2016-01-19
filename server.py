#  coding: utf-8
import SocketServer
import os, string
import mimetypes
import StringIO

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Changes are Copyright 2016 Alain Clark
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

#''' RESOURCES '''
# http://fragments.turtlemeat.com/pythonwebserver.php
# http://www.opensource.apple.com/source/python/python-3/python/Lib/SimpleHTTPServer.py
# https://hg.python.org/cpython/file/2.7/Lib/BaseHTTPServer.py

class MyWebServer(SocketServer.BaseRequestHandler):

    '''
    Expecting the following in a request:

    "GET [path:/] HTTP/1.1

    "

    And we expect to return the following:

    "HTTP/1.1 [code] [message]
    
    [data]"

    With at least one 'header' line:
    
    "Content-type: <T>/<s>"
    '''

    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        try:
            req_type = self.data.split()[0]
            rel_path = self.data.split()[1]
            rel_path = rel_path.split('../')[-1]
            print(rel_path)
            abs_path = self.ex_path(rel_path)
            print("Serving '%s'" % rel_path)
        except:
            print("Bad Request")
        if req_type=="GET":

            if( os.path.commonprefix([web_root, abs_path]) ):
                self.fetch(rel_path)
            else:
                # PERMISSION DENIED - 403
                self.send_response(403)
        else:
            # NOT SUPPORTED - 501
            self.send_response(501)

    def fetch(self, rel_path):
        resource = self.ex_path(rel_path)
        if os.path.isfile(resource):
            f = open(resource, 'r')
            contents = f.read()
            if (contents):
                self.send_response(200)
                self.send_mimetype(resource)
                self.request.sendall(contents)

        elif os.path.isdir(resource):
            # RESOURCE EXISTS - 200
            if not (resource.endswith('/')):
                # 301 redirect
                self.send_response(301)
                self.request.send("Location: %s/\r\n" % rel_path)
            else:
                self.fetch(rel_path + "index.html")
        else:
            self.send_response(404)
            self.request.send('Content-Type: text/html\r\n\r\n')
            self.request.send(ERRNF)

    def ex_path(self,rel_path):
        return os.path.abspath(web_root)+rel_path

        # ========
    def send_response(self, num):
        print('HTTP/1.1 %d %s\r\n' % (num, responses[num]))
        self.request.send('HTTP/1.1 %d %s\r\n' % (num, responses[num]))

    def send_mimetype(self, path):
        print('Content-Type: %s\r\n\r\n' % mimetypes.guess_type(path)[0])
        self.request.send('Content-Type: %s\r\n\r\n' % mimetypes.guess_type(path)[0])

    def send_header(self):
        print('')
        #self.server.

    def end_header(self):
        print('')

    def send_body(self):
        print('')

# ================
# Support for delims, mime-types
# and response codes
# ----------------
web_root = os.getcwd()+"/www"
# ......HTTP......
PRELIM = "HTTP/1.1 "
DELIM = "\r\n"
DDELIM = "\r\n\r\n"

responses = {
        200 : "OK",
        301 : "Redirect",
        403 : "Forbidden",
        404 : "Not Found",
        501 : "Not Implemented"
}

ERRNF = '''
<!DOCTYPE html>
<html>
<head>
	<title>404 ERROR - NOT FOUND</title>
</head>

<body>
<h3>404 - NOT FOUND</h3>
<p>This resource was not found on the server.</p>
</body>
</html> 
'''

# ......MIME......
MIMECT = "Content-type:"

# ================
# Runtime setup
# ----------------
if __name__ == "__main__":
    try: 
        HOST, PORT = "localhost", 8080
        SocketServer.TCPServer.allow_reuse_address = True
        # Create the server, binding to localhost on port 8080
        server = SocketServer.TCPServer((HOST, PORT), MyWebServer)
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()


