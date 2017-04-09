import http.server
import socketserver
import urllib.parse
import json
from itertools import islice
import sys

data_file_name = 'data.txt'
meta_data_file = 'meta.txt'

class BepfService(http.server.SimpleHTTPRequestHandler):

    def get_next_line_number(self):
        with open(meta_data_file, 'r') as f:
            line_number = json.load(f)['line_number']
        f.closed
        return line_number

    def set_next_line_number(self, line_number):
        mess = {"line_number": line_number}
        with open(meta_data_file, 'w') as f:
            line_number = json.dump(mess, f)
        f.closed
        return line_number

    def read_data(self, first_line, chunk_len=None):
        data = []
        with open(data_file_name, 'r') as f:
            linesCounter = 1
            for line in f:
                if linesCounter >= first_line:
                    if chunk_len and linesCounter >= first_line + chunk_len:
                        break
                    data.append(line)
                linesCounter += 1

        f.closed
        # self.set_next_line_number(linesCounter)
        return (''.join(data), linesCounter)

    def do_GET(self):
        if 'favicon.ico' in self.path:
            message = ''
        else:
            line_number = self.get_next_line_number()
            message, line_count = self.read_data(1)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(message,'utf8'))
        return message

    def do_POST(self):
        #print(self.path)
        #print("Header: {0}".format(self.headers))
        length = int(self.headers.get('content-length'))
        data_string = json.loads(str(self.rfile.read(length),'utf-8'))
        self.send_response(200)
        self.end_headers()

        print("Content: {0}".format(data_string))
        self.wfile.write(b'OK')


if __name__ == "__main__":

    service = BepfService

    print(sys.argv)
    if len(sys.argv) == 1:
        host = "127.0.0.1"
        port = 8001
        httpd = socketserver.TCPServer((host, port), service)
        print("Starting Service {0}:{1}".format(host,port))
        httpd.serve_forever()
    elif len(sys.argv) == 3:
        host = sys.argv[1]
        port = sys.argv[2]
        httpd = socketserver.TCPServer((host, port), service)
        print("Starting Service {0}:{1}".format(host,port))
        httpd.serve_forever()
    else:
        print("wrong number of parameters")