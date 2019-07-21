from socket import *

class TCP_client:
    def __init__(self, host='0.0.0.0', port=8880):
        self.host = host
        self.port = port
        self.address = (host, port)
        self.creae_cocket()

    def creae_cocket(self):
        self.sockfd = socket()
        self.sockfd.connect(self.address)

    def main(self):
        while True:
            print('1.登录\n2.注册\n3.退出')
            n = input('')
            if n == '1':
                self.__enter()
            elif n == '2':
                self.__login()
            else:
                break

    def __enter(self):
        name = input('请输入姓名')
        password = input('请输入密码')
        data = 'E %s %s'%(name,password)
        self.sockfd.send(data.encode())
        data = self.sockfd.recv(1024)
        if data.decode() == 'OK':
            print('登录成功')
            self.__look_dict()
        else:
            print('登录失败,请输入正确的用户名和密码')

    def __name_pssword(self):
        while True:
            name = input('请输入姓名,回车退出')
            if not name:
                break
            p = input('请输入密码')
            password = input('请再输入一次')
            if p != password:
                print('两次密码不一致')
            elif ' ' in name or ' ' in password:
                print('不能有空格')
            elif password:
                return name, password
            else:
                print('密码不能为空')

    def __login(self):
        a = self.__name_pssword()
        if not a:
            return
        data = 'L %s %s'%(a[0],a[1])
        self.sockfd.send(data.encode())
        data = self.sockfd.recv(1024)
        if data.decode() == 'OK':
            self.__look_dict()
        else:
            print('用户名已经存在')


    def __look_dict(self):
        while True:
            print('1.查单词\n2.历史记录\n3.注销')
            n = input('')
            if n == '1':
                self.__inport_word()
            elif n == '2':
                self.__looked()
            elif n == '3':
                break

    def __inport_word(self):
        while True:
            data = input('请输入单词')
            if not data:
                break
            data = 'D %s'%data
            self.sockfd.send(data.encode())
            data = self.sockfd.recv(1024)
            print(data.decode())

    def __looked(self):
        data = 'F '
        self.sockfd.send(data.encode())
        data = self.sockfd.recv(1024)
        print(data.decode())




a = TCP_client()
a.main()









