import os 

#返回码
class ErrorCode(object):
    OK = "HTTP/1.1 200 OK\r\n"
    NOT_FOUND = "HTTP/1.1 404 Not Found\r\n"

#Content类型
class ContentType(object):
    HTML = "Content-Type: text/html\r\n"
    PNG = "Content-Type: img/png\r\n"

#请求目录
class HttpRequest(object):
    RootDir ="."
    NotFoundHtml = RootDir + '/' +'404.html'

    def __init__(self):
        self.method = None
        self.url = None
        self.protocal = None
        self.host = None
        self.request_data = None
        self.response_line = ErrorCode.OK #响应码
        self.response_head = None #响应头
        self.response_body = '' #响应内容
    
    #解析请求，得到请求的消息
    def pass_request(self, request):
        request_line, body =request.split('\r\n', 1)
        header_list = request_line.split(' ')
        #得到请求方法
        self.method = header_list[0].upper()
        #得到请求url
        self.url = header_list[1]
        print(f"{self.url}")
        #得到协议
        self.protocal = header_list[2]
        #获得请求参数
        if self.method == 'POST':
            self.request_data = {}
            request_body = body.split('\r\n\r\n',1)[1]
            #获得请求参数数组
            params = request_body.split('\n')
            for para in params:
                key, val = para.split('=')
                self.request_data[key] = val
            self.handle_file_request(HttpRequest.RootDir + self.url)
        if self.method == 'GET':
            file_name = ''
            #h获取get参数
            if self.url.find('?') != -1:
                self.request_data = {}
                req = self.url.split('?',1)[1]
                file_name = self.url.split('?',1)[0]
                params = req.split('&')
                for parm in params:
                    key, val = para.split('=')
                    self.request_data[key] = val
            else:
                file_name = self.url
            if len(self.url) == 1: #如果是根目录
                file_name = '/index.html'
            file_path = HttpRequest.RootDir + file_name
            self.handle_file_request(file_path)

    #处理请求
    def handle_file_request(self, file_path):
        #如果找不到目录输出404响应码
        if not os.path.isfile(file_path):
            f = open(HttpRequest.NotFoundHtml, 'r')
            self.response_line = ErrorCode.NOT_FOUND
            self.response_body = f.read()
            response_contentType = ContentType.HTML
            response_contentLength = "Content-length: " + str(len(self.response_body))
        else:
            f = None
            self.response_line = ErrorCode.OK
            extension_name = os.path.splitext(file_path)[1] #扩展名
            #图片资源需要使用二进制读取
            if extension_name == '.PNG':
                f = open(file_path, 'rb')
                self.response_body = f.read()
                self.response_head = ContentType.PNG+"Content-length: " + str(len(self.response_body))
                
            #执行CGI，将请求转发到本地的python脚本
            elif extension_name == '.py':
                file_path = file_path.split('.',1)[0]
                file_path = file_paht.replace('/','.')
                m = __import__(file_path)
                self.response_head = ContentType.HTML
                self.response_body =m.main.app(self.request_data)
            #其他静态文件
            else:
                f = open(file_path,'r')
                self.response_body = f.read()
                self.response_head = ContentType.HTML + str(len(self.response_body))

    def get_response(self):
        return self.response_line + self.response_head +'\r\n'+ str(self.response_body)


