from gevent import monkey
import gevent
monkey.patch_socket()
from socket import *


class HTTPServer:
    def __init__(self,host = '39.100.143.85',port = 11,dir = None):
        self.host = host
        self.port = port
        self.dir =dir
        self.address = (host,port)
        self.creae_cocket()

    def creae_cocket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sockfd.bind(self.address)
        self.sockfd.listen(3)
        print('listen..from', self.port)

    def serve_forever(self):
        while True:
            c,addr = self.sockfd.accept()
            print('hello',addr)
            gevent.spawn(self.func01,c)

    def func01(self,c):
        while True:
            data = c.recv(2048)
            if not data:
                return
            request_line = data.splitlines()[0]
            info = request_line.decode().split(' ')[1]
            if info == '/' or info[-5:] == '.html':
                self.get_html(c, info)
            else:
                self.get_data(c, info)

    def get_html(self,c,info):
        if info == '/':
            filename = self.dir + "/index.html"
        else:
            filename = self.dir + info
        try:
            fd = open(filename)
        except Exception:
            response = "HTTP/1.1 404 Not Found\r\n"
            response += 'Content-Type:text/html\r\n'
            response += '\r\n'
            response += '<h1>Sorry....</h1>'
        else:
            response = "HTTP/1.1 200 OK\r\n"
            response += 'Content-Type:text/html\r\n'
            response += '\r\n'
            response += fd.read()
        finally:
            c.send(response.encode())

    def get_data(self, c, info):
        response = "HTTP/1.1 200 OK\r\n"
        response += 'Content-Type:text/html\r\n'
        response += '\r\n'
        response += "<h1>Waiting for httpserver 3.0</h1>"
        c.send(response.encode())


if __name__ == '__main__':
    a = HTTPServer('0.0.0.0',8888,'./static')
    a.serve_forever()








