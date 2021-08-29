from socket import *
import select

def main():
    #创建套接字
    server = socket(AF_INET, SOCK_STREAM)
    #设置套接字的属性为阻塞
    server.setblocking(True)
    #保证端口不会被占用
    server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    #绑定地址和端口
    server.bind(("", 9191))
    #开启监听
    server.listen(5)
    #把套接字放到监视区域中
    server_lists = [server]
    #等待客户连接
    while True:
        #如果监视区域有就绪套接字
        read_list,_,_ = select.select(server_lists,[],[])
        #遍历返回的就绪列表
        for s in read_list:
            #判断是否为主套接字，如果是主套接字，说明有客户连接，生成子套接字，加入监控区域
            if s is server:
                new_server, client =s.accept()
                server_lists.append(new_server)
            else:
                #不是主套接字，说明有数据到来，接收响应
                data = s.recv(1024)
                if data:
                    print(f"收到消息{data.decode('utf-8')}")
                else:
                    s.close()
                    server_lists.remove(s)

if __name__ == "__main__":
    main()