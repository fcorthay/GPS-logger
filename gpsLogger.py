#! /usr/bin/env python3

import os
import argparse
import socket
import http.server

# ------------------------------------------------------------------------------
# constants
#
GATEWAY = '192.168.1.1'
#GATEWAY = '8.8.8.8'

LOG_FILE_LENGTH = 60*24*3

# ------------------------------------------------------------------------------
# command line arguments
#
parser = argparse.ArgumentParser()
                                                                     # verbosity
parser.add_argument(
    '-v', '--verbose', action='store_true', dest='verbose',
    help = 'verbose console output'
)
                                                            # HTTP Ethernet port
parser.add_argument(
    '-p', '--port', default=11123,
    help = 'the HTTP server port'
)
                                                                 # log directory
parser.add_argument(
    '-l', '--logDir', default=os.path.dirname(os.path.realpath(__file__)),
    help = 'the directory logs'
)
                                                  # parse command line arguments
parser_arguments = parser.parse_args()
verbose = parser_arguments.verbose
server_port = parser_arguments.port
log_directory = parser_arguments.logDir

# ==============================================================================
# Internal functions
#

#-------------------------------------------------------------------------------
# Get IP address
#
def IP_address() :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((GATEWAY, 1))
    return(s.getsockname()[0])

#-------------------------------------------------------------------------------
# log GPS info to file
#
def log_GPS_info(device, parameters) :
                                                               # build file spec
    log_file_spec = os.sep.join([log_directory, device + '.log'])
                                                                     # read file
    log_file_lines = []
    if os.path.isfile(log_file_spec) :
        log_file_lines = open(log_file_spec, "r").read().split("\n")
                                                                      # add info
    log_file_lines.append(' '.join(parameters))
                                                                    # write file
    open(log_file_spec, "w").write(
        "\n".join(log_file_lines[-LOG_FILE_LENGTH:])
    )


#-------------------------------------------------------------------------------
# String to byte array
#
def to_bytes(string) :
    return(bytes(string, "utf-8"))

#-------------------------------------------------------------------------------
# HTTP GET service
#
class MyServer(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
                                                               # analyse request
        (path, params) = self.path.split('?')
        if path[0] == '/' :
            path = path[1:]
        parameters = params.split('&')
                                                                      # log info
        log_GPS_info(path, parameters)
                                                                 # send response
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(to_bytes(
            "<html><head><title>GPS tracking service</title></head>"
        ))
        self.wfile.write(to_bytes("<body>"))
        self.wfile.write(to_bytes("<p>from %s:" % path))
        for parameter in parameters :
            self.wfile.write(to_bytes("<ul>%s</ul>" % parameter))
        self.wfile.write(to_bytes("</p>"))
        self.wfile.write(to_bytes("</body></html>"))

# ==============================================================================
# Main script
#
                                                               # find IP address
hostName = IP_address()
                                                                    # run server
if __name__ == "__main__":        
    webServer = http.server.HTTPServer((hostName, server_port), MyServer)
    print("Server started http://%s:%s" % (hostName, server_port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped")
