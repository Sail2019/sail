# -*- coding: UTF-8 -*-
import gevent
from word_dict import *
from gevent import monkey
monkey.patch_socket()
from socket import *


class TCP_Sever:
    def __init__(self, host='0.0.0.0', port=8880):
        self.host = host
        self.port = port
        self.address = (host, port)
        self.db = Database()
        self.cur = self.db.create_cursor()
        self.creae_cocket()

    def creae_cocket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sockfd.bind(self.address)
        self.sockfd.listen(3)
        print('监听', self.port)

    def serve_forever(self):
        while True:
            c,addr = self.sockfd.accept()
            print('欢迎',addr)
            gevent.spawn(self.fun01,c=c,addr=addr)

    def fun01(self,c,addr):
        name = ''
        while True:
            data = c.recv(1024)
            if not data:
                print('客户端退出',addr)
                break
            data = data.decode().split(' ')
            if data[0] == 'E':
                name = self.select_name(c, data)
            elif data[0] =='L':
                name = self.insert_name(c, data)
            elif data[0] == 'D':
                self.select_dict(c,data,name)
            elif data[0] == 'F':
                self.select_record(c,name)

    def insert_name(self, c, data):
        if self.db.insert(data):
            c.send(b'OK')
            return data[1]
        else:
            c.send(b'NO')

    def select_name(self, c, data):
        n = self.db.select(data)
        if not n:
            c.send(b'NO')
        elif n[0][0] == data[-1]:
            c.send(b'OK')
            return data[1]

    def select_dict(self,c,data,name):
        n = self.db.select_dict(data)
        if not n:
            c.send('没有找到该单词'.encode())
        else:
            c.send(n[0][0].encode())
            self.db.insert_record(name,data)

    def select_record(self,c,name):
        n = self.db.select_record(name)
        if not n:
            c.send('没有找任何记录'.encode())
        else:
            data = ''
            for x in n:
                data += '姓名:%s 单词:%s 时间:%s\n'%(x[1],x[2],x[3])
            c.send(data.encode())


a = TCP_Sever()

a.serve_forever()



