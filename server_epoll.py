from socket import *
import select

def main():
    #创建套接字
    server = socket(AF_INET, SOCK_STREAM)
    #设置套接字的属性为阻塞
    server.setblocking(True)
    #保证端口不会被占用
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    #绑定地址和端口
    server.bind(("", 9999))
    #开启监听
    server.listen(5)

    #创建一个epoll对象，epoll只能在linux环境中使用
    _epoll = select.epoll()
    #将主套接字的文件描述符添加到监听区域
    _epoll.register(server.fileno(), select.EPOLLIN)

    #创建一个字典，用来存放子套接字和客户端信息
    new_socket_dicts = {}
    client_info_dicts = {}

    #等待客户连接
    while True:
        #返回就绪的套接字
        epoll_lists = _epoll.poll()
        for fd, event in epoll_lists:
            if fd == server.fileno():
                #创建子套接字
                new_server, client_info = server.accept()
                _epoll.register(new_server.fileno(), select.EPOLLIN)
                new_socket_dicts[new_server.fileno()] = new_server
                client_info_dicts[new_server.fileno()] = client_info
            else:
                #如果是子套接字
                data = new_socket_dicts[fd].recv(1024).decode("utf-8")
                if data:
                    print(f"接收到来自于{client_info_dicts[fd]}的消息{data}")
                else:
                    new_socket_dicts[fd].close()
                    _epoll.unregister(fd)