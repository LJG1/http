from socket import *
from threading import Thread
import time
from HttpHead import HttpRequest

def tcp_link(new_server, client, tm):
    print(f"Accept new connection from {client}") 
    request = new_server.recv(1024).decode('utf-8')
    print(f"get data from {client}:{request}")
    if request:
        http_req = HttpRequest()

        http_req.pass_request(request)
        time.sleep(tm)
        #发送数据请求
        new_server.send(http_req.get_response().encode())
    new_server.close()

def main():
    #创建套接字
    server = socket(AF_INET, SOCK_STREAM)
    #设置套接字的属性为阻塞
    server.setblocking(True)
    #保证端口不会被占用
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    #绑定地址和端口
    server.bind(("", 9001))
    #开启监听
    server.listen(5)

    a = input('输入超时时间：')
    tm =int(a)

    while True:
        
        new_server, client = server.accept()
        #接收消息
        if new_server: 
            p = Thread(target = tcp_link, args = (new_server, client, tm))
            p.start()

if __name__ == "__main__":
    main()
