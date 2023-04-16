```python
#######################################################################
# 0. WSGI
#######################################################################


# 0.1 WSGI-简介(Python Web Server Gateway Interface)
# (1) WSGI是一种接口规范(类似RESTFUL), 用于服务器和应用程序间通信.
# (2) 遵循这一规范编写的应用,框架或工具集可以运行在任意一种遵循这种规范的服务器上
# (3) 符合WSGI规范的应用可叠加,夹在中间的叫做中间件,须同时实现应用端和服务端的接口
# (4) 对中间件之上的应用它相当于服务器, 对中间件之下的应用或服务器它一个应用程序
# (5) 符合WSGI规范的服务器仅仅接受来自与客户端的请求, 再把请求转给应用程序, 
#     最后把应用程序处理后的响应返回给客户端. 其他细节交由应用程序或中间件完成.


# 0.2 WSGI-应用接口
# (1) WSGI应用接口的实现是一个可调用对象, 即包含object.__call__()方法的类或实例对象
# (2) 该对象必须接收两个位置参数:
#     一个字典对象(包含类似 CGI 中的变量);
#     一个回调函数(应用程序用它来发送 HTTP 状态码和报头等信息给服务器)
# (3) 该可调用对象要返回响应体给服务器, 结构是用可遍历对象包裹的一些字符串对象.
# (4) 应用框架
# 函数作为应用接口
def application (environ, \        # 字典:服务器根据用户请求产生
                 start_response):  # 回调函数:接收HTTP状态码和头部信息作为参数
  response_body = 'Request method: %s' % environ['REQUEST_METHOD']
  status = '200 OK'
  # HTTP 报头信息格式 [(Header name, Header value)]
  response_headers = [    
    ('Content-Type', 'text/plain'),
    ('Content-Length', str(len(response_body)))
  ]
  start_response(status, response_headers)  # 发送响应头
  return [response_body]                    # 返回响应体


# 0.3 WSGI-环境变量字典
# (1) 环境变量字典由服务器产生, 其中的数据是对客户请求处理后得到的CGI风格的变量
# (2) 下方将return [response_body] 改为 return response_body 仍能运行但更慢
#     字符串可遍历, 修改后从返回字符串给客户端,变为逐个字符返回
#     所以为提高性能, 要将响应内容包起来, 使它成为一个整体.
如果响应体中包含多个字符串, 那么响应体的长度会是所有这些字符串长度之和.
# (3) 下面这段脚本会输出整个字典中的内容.
#! /usr/bin/env python
# Python 自带的 WSGI 服务器
from wsgiref.simple_server import make_server
def application (environ, start_response):
  # 对环境变量字典中的键值对排序, 并转换为字符串
  response_body = [
    '%s: %s' % (key, value) for key, value in sorted(environ.items())
  ]
  response_body = '\n'.join(response_body)
  status = '200 OK'
  response_headers = [
    ('Content-Type', 'text/plain'),
    ('Content-Length', str(len(response_body)))
  ]
  start_response(status, response_headers)
  return [response_body.encode('utf-8')]
# 实例化服务器
httpd = make_server (
    'localhost', # 主机名
    8051, # 监听的端口
    application # 应用程序对象
)
# 等待处理一个请求, 完成后退出
httpd.handle_request()

# 0.3 WSGI-服务器端
# (1) 服务器必须提供environ字典和start_response函数.
# (2) 服务器通过调用web应用接口程序来把请求传入应用中.
iterable = app(environ, start_response)
for data in iterable:
   # send data to client
# (3) 应用程序调用start_response生成响应头, 并负责生成iterable中的响应体.
# (4) 服务器再把响应头和体通过HTTP返回给客户端.

# 0.4 WSGI-中间件
# 一个中间件示例, 将下层应用(或中间件)的响应内容改为首字母大写.
class Upperware:
  def __init__(self, app):
      self.wrapped_app = app
  def __call__(self, environ, start_response):
      response_body = []
      for data in self.wrapped_app(environ, start_response):
          response_body.append(data.upper())
      return response_body

# 0.5 WSGI-中间件例子
class Middleware:

    def __init__(self, app):
        self.status = None
        self.headers = None
        self.app = app

    def my_start_response(self, status, headers):
        self.status = status
        self.headers = headers

    def __call__(self, environ, start_response):

        response_body = [b'Upper middleware:<br/>']
        content_len = len(response_body[0])

        for data in self.app(environ, self.my_start_response):
            response_body.append(data.upper())

        response_headers = []

        for header, value in self.headers:
            if header == 'Content-Length':
                value = str(int(value) + content_len)
            response_headers.append((header, value))

        start_response(self.status, response_headers)

        return response_body


@Middleware
def application(environ, start_response):
    response_body = '{}: {}'.format('request method',
                                    environ.get('REQUEST_METHOD'))

    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_headers)

    return [response_body.encode('utf-8')]


# 0.6 WSGI-相似概念
# uwsgi: 是一种 uWSGI 使用的二进制协议, 用于数据传输.
# uWSGI: 是一个应用服务器, 采用可插拔的架构以支持多语言和平台.
# 因为其上开发出来的第一个插件支持的就是Python中的WSGI标准, 所以才有了现在的名字.
```
