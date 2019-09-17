# Creat by Darren On 19-9-10  下午5:55

from socket import *
from select import select

class HTTPServer:
    def __init__(self,addr=('0.0.0.0',80),path=''):
        self.addr = addr
        self.path = path
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.sockfd.bind(self.addr)
        self.rlist = []
        self.wlist = []
        self.xlist = []


    def sever_enter(self):
        self.sockfd.listen(3)
        print('Listen:',self.addr)
        self.rlist.append(self.sockfd)

        while True:
            rs,ws,xs = select(self.rlist,self.wlist,self.xlist)
            for r in rs:
                if r is self.sockfd:
                    connfd,addr = r.accept()
                    self.rlist.append(connfd)
                else:
                    self.handle(r)

    def handle(self, connfd):
        data = connfd.recv(4096).decode()
        if not data:
            self.rlist.remove(connfd)
            connfd.close()
            return
        data_line = data.splitlines()[0]
        info = data_line.split(' ')[1]
        print(info)

        if info == '/' or info[-5:] == '.html':
            self.get_html(connfd,info)
        else:
            self.get_data(connfd,info)

    def get_html(self, connfd, info):
        if info == '/':
            filename = self.path + 'index.html'
        else:
            filename = self.path + info
        try:
            f = open(filename,'rb')
        except Exception:
            response = 'HTTP/1.1 404 NotFound\r\n'
            response += 'Conten-type:text/html\r\n\r\n'
            response += '<h1>Sorry</h1>'
            response = response.encode()
        else:
            response = 'HTTP/1.1 200 OK\r\n'
            response += 'Conten-type:text/html\r\n\r\n'
            response =response.encode() + f.read()
            f.close()
        connfd.send(response)



    def get_data(self, connfd, info):
        html = 'HTTP/1.1 200 OK\r\n'
        html += 'Conten-type:text/html\r\n\r\n'
        with open(self.path+'0.jpg' ,'rb') as f:
            html = html.encode() + f.read()
        connfd.send(html)


if __name__ == '__main__':
    Addr = ('0.0.0.0',9119)
    PATH = './'
    http = HTTPServer(Addr,PATH)
    http.sever_enter()