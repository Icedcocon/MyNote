# 开始

\_\_init\_\_.py 有两个作用：一是包含应用工厂；二是 告诉 Python flaskr 文件夹应当视作为一个包。

create_app 是一个应用工厂函数

# pymysql

```python
import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='10.166.15.33',
                             user='root',
                             password='123456',
                             db='fryDemo',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

if __name__ == '__main__':
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "CREATE TABLE IF NOT EXISTS `users`(\
            `id` int primary key auto_increment not null,\
            `password` varchar(150),\
            `email` varchar(150)\
            )"
            cursor.execute(sql)

        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql, ('webmaster@python.org',))
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()
```

# 路由

## URL 路由注册

- 路由系统的规则定义一般有以下三种方式：
  
  1. 使用`flask.Flask.route()`装饰器。
  2. 使用`flask.Flask.add_url_rule()`功能。
  3. 直接访问底层 Werkzeug 路由系统，以`flask.Flask.url_map.`的形式暴露。

- 路由中的可变部分可以用尖括号 ( `/user/<username>`) 指定。默认情况下，URL 中的可变部分接受任何不带斜杠的字符串，但是也可以使用`<converter:name>`.

- 可变部分作为关键字参数传递给视图函数。

- 可以使用以下转换器：

| 转换器    | 作用              |
| ------ | --------------- |
| string | 接受任何不带斜线的文本（默认） |
| int    | 接受整数            |
| float  | 接受浮点数           |
| path   | 接受带斜杠的文本        |

- 例子：

```python
@app.route('/')
def index():
    pass

@app.route('/<username>')
def show_user(username):
    pass

@app.route('/post/<int:post_id>')
def show_post(post_id):
    pass
```

- 为保证URL唯一， Flask 处理斜杠规则如下（可通过`strict_slashes=None`改变）：
  
  1. 如果规则以斜杠结尾并且用户请求时不使用斜杠，则用户将自动重定向到带有尾部斜杠的同一页面。
  2. 如果规则不以斜杠结尾并且用户请求带有斜杠的页面，则会引发 404 not found。

- 还可以为同一个函数定义多个规则，或指定默认值。

```python
@app.route('/users/', defaults={'page': 1})
@app.route('/users/page/<int:page>')
def show_users(page):
    pass
```

- route() 和 add_url_rule()中的参数

| 规则        | URL 规则作为字符串                                                                                                                                                                                                                               |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| endpoint  | 已注册 URL 规则的端点，是一个名称，用于反向生成URL，`url_for(端点)`。Flask 默认视图函数名（上表show_uesrs）为端点名称。                                                                                                                                                             |
| view_func | 访问端点（URL）时调用的视图函数。存储在以端点（默认视图函数名）为键`view_functions`字典中。                                                                                                                                                                                   |
| defaults  | 一个字典，用于URL不含参数，但视图函数需要参数时。`default = {k:v}`                                                                                                                                                                                               |
| subdomain | 多个子域名指向同一个IP地址时，可以获取子域名``subdomain="<name>"`并处理。如果未指定，则假定为默认子域。                                                                                                                                                                           |
| **options | 要转发到基础 [`Rule`](http://werkzeug.pocoo.org/docs/routing/#werkzeug.routing.Rule "（在工具 v0.11-dev 中）")对象的选项。Werkzeug 的一个变化是处理方法选项。方法是此规则应限制的方法列表（GET，POST 等）。默认情况下，规则只侦听GET（并且隐式地听HEAD）。从 Flask 0.6 开始，OPTIONS被隐式添加并由标准请求处理进行处理。它们必须指定为关键字参数。 |

# 蓝图

蓝图是一个对象，它允许在不需要应用程序对象的情况下定义应用程序函数。它使用与FIsk相同的装饰器，但通过记录它们以供以后注册来推迟对应用程序的需求。

### 请求响应循环（Request-Response Cycle）

<img title="" src="file:///D:/Cache/MarkText/2022-08-08-08-34-12-image.png" alt="" data-align="center" width="258">

<img title="" src="file:///D:/Cache/MarkText/2022-08-08-08-35-36-image.png" alt="" data-align="center" width="293">

### 请求报文及常见方法

<img title="" src="file:///D:/Cache/MarkText/2022-08-08-08-37-32-image.png" alt="" data-align="center" width="582">

![](D:\Cache\MarkText\2022-08-08-08-38-10-image.png)

### Flask中Request对象常用的属性及方法

- 请求解析和响应封装大部分是由Werkzeug完成的；

- Flask子类化Werkzeug的请求(Request)和响应(Response)对象并添加了和程序相关的特定功能

![](D:\Cache\MarkText\2022-08-08-08-41-16-image.png)

### Flask请求处理

1. 路由匹配

2. 设置监听HTTP的方法（GET、POST、HEAD等）

3. URL处理（转换器）

<img src="file:///D:/Cache/MarkText/2022-08-08-08-54-53-image.png" title="" alt="" data-align="center">

### 请求钩子

- 用于对请求进行预处理(preprocessing)和后处理(postprocessing)

- 钩子使用装饰器实现，对函数附加app.before_request装饰器进行注册，每次执行请求前都会触发所有before_request处理函数。

- Flask默认实现的五种请求钩子

<img src="file:///D:/Cache/MarkText/2022-08-08-08-57-41-image.png" title="" alt="" data-align="center">

```python
@app.before_request
def do something()
    pass    # 这里的代码会在每个请求处理前执行
```

假如我们创建了三个视图函数A、B、C,其中视图C使用了after this request钩子

<img title="" src="file:///D:/Cache/MarkText/2022-08-08-09-14-25-image.png" alt="" data-align="center" width="307">

# HTTP响应

### 响应报文

- 响应报文主要由**协议版本**、**状态码**(status code)、**原因短语**(reason phrase)、**响应首部**和**响应主体**组成。

<img src="file:///D:/Cache/MarkText/2022-08-08-09-18-21-image.png" title="" alt="" data-align="center">

### Flask中生成响应Response

```python
# 完整地说，视图函数可以返回最多由三个元素组成的元组：响应主体、状态码、首部字段。
# 其中首部字段可以为字典，或是两元素元组组成的列表。

# 普通的响应可以只包含主体内容：
@app.route('/hello')
def hello():
    return '<h1>Hello,Flask!</h1>'

# 默认的状态码为200，下面指定了不同的状态码：
@app.route('/hello')
def hello():
    return '<h1>Hello,Flask!</h1>',201

# 有时你会想附加或修改某个首部字段。比如，要生成状态码为3XX的重定向响应，需要将
# 首部中的Location字段设置为重定向的目标URL:
@app.route('/hello')
def hello():
    return '', 302, {'Location', 'http://www.example.com'}
```

##### 重定向：

- 上图代码中状态码为302的重定向响应的主体为空，首部中需要将Location字段设为重定向的目标URL,浏览器接收到重定向响应后会向Location字段中的目标URL发起新的GET请求

<img title="" src="file:///D:/Cache/MarkText/2022-08-08-09-26-03-image.png" alt="" data-align="center" width="415">

```py
# 重定向的简单实现
from flask import Flask,redirect
@app.route('/hello')
def hello():
    return redirect ('http://www.example.com')
```

##### 响应格式

- MIME类型在首部的Content-Type字段中定义，默认为HTML类型

```http
Content-Type:text/html;charset=utf-8
```

- 想使用其他MIME类型，可通过Flask提供的make_response()方法生成响应对象，传人响应的主体作为参数，然后使用响应对象的mimetype属性设置MIME类型

```python
from flask import make_response

@app.route ('/foo')
def foo():
    response = make_response ('Hello,World!')
    response.mimetype ='text/plain'
    return response
```

1. 纯文本
   
   - MIME类型：text/plain

2. HTML
   
   - MIME类型：text/html

3. XML
   
   - MIME类型：application/xml

4. JSON
   
   - MIME类型：application/json
   
   - Flask通过引入Python标准库中的json模块(或simplejson,如果可用)为程序提供了JSON支持。
   
   - 你可以直接从Flask中导人json对象，然后调用dumps()方法将字典、列表或元组序列化
   
   - Flask包装并提供了更方便的jsonify（）函数。借助jsonify()函数将参数转换成JSON字符串，作为响应的主体，然后生成一个响应对象，并且设置正确的MIME类型。
   
   - jsonify()函数默认生成200响应，你也可以通过附加状态码来自定义响应类型

```python
@app.route('/foo')
def foo():            
    return jsonify(message='Error!'),500
```

##### Cookie

- HTTP是无状态(stateless)协议。也就是说，在一次请求响应结束后，服务器不会留下任何关于对方状态的信息。

- 但客户端的某些信息又必须被记住，比如用户的登录状态。Cookie技术通过在请求和响应报文中添加Cookie数据来保存客户端的状态信息。

- 在Flask中在响应中添加一个cookie可以使用Response类提供的set_cookie()方法。

![](D:\Cache\MarkText\2022-08-08-14-53-35-image.png)

![](D:\Cache\MarkText\2022-08-08-14-53-49-image.png)

```python
from flask import Flask,make_response
@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect (url for('hello')))
    response.set_cookie('name',name)
    return response
```

### Session

- Flask提供了session对象用来将Cookie数据加密储存。

- **1.设置程序密钥**
  
  - session通过密钥对数据进行签名以加密数据，使用前先设置。密钥是一个具有一定复杂度和随机性的字符串，比如`“Drmhze6 EPcv0fN81Bj-nA”`。
  
  - 程序的密钥可以通过Flask.secret_key属性或配置变量SECRET_KEY设置，比如：
  
  - ```python
    app.secret_key ='secret string'
    
    # 更安全的做法是把密钥写进系统环境变量(在命令行中使用export或set命令)
    # 或是保存在.env文件中
    SECRET_KEY=secret string
    ```

    import os
    app.secret_key = os.getenv ('SECRET KEY','secret string')
    # 可以在getenv()方法中添加第二个参数，作为没有获取到对应环境变量时使用的默认值
    ```

- 2.模拟用户认证
  
  ```python
  from flask import redirect,session,url_for
  @app.route('/login')
  def login():
      session['logged in']=True#写入session
      return redirect(url for('hello'))
  # =============== Hello ========================
  from flask import request,session
  @app.route ('/'
  @app.route('/hello')
  def hello():
      name request.args.get (name')
      if name is None:
          name = request.cookies.get(name','Human')
          response='<h1>He11o,%s!</h1>' % name
      #根据用户认证状态返回不同的内容
      if 'logged in' in session:
          response += '[Authenticated]'
      else:
          response +='[Not Authenticated]'
      return response
  # ============== 模拟后台管理 =====================
  from flask import session
  @app.route('/logout')
  def logout():
      if 'logged in'in session:
      session.pop('logged in')
      return redirect (url for('hello'))
  ```
  
  - session对象可以像字典一样操作，我们向session中添加一个logged-in cookie,将它的值设为True,表示用户已认证。
  
  - 当我们使用session对象添加cookie时，数据会使用程序的密钥对其进行签名，加密后的数据存储在一块名为session的cookie里
  
  - 程序中的某些资源仅提供给登入的用户，比如管理后台，这时我们就可以通过判断session是否存在logged-in键来判断用户是否认证

### Flask上下文

- Flask中有两种上下文，程序上下文(application context).和请求上下文(request context)。
  
  - 直接从Flask导人一个全局的request对象，然后在视图函数里直接调用request的属性获取数据。Flask会在每个请求产生后自动激活当前请求的上下文，激活请求上下文后，request被临时设为全局可访问。而当每个请求结束后，Flask就销毁对应的请求上下文。
  
  - 假设有三个客户端同时向服务器发送请求，这时每个请求都有各自不同的请求报文，所以请求对象也必然是不同的。因此，请求对象只在各自的线程内是全局的。Flask通过本地线程(thread local)技术将请求对象在特定的线程和请求中全局可访问。

- **Flask上下文变量**
  
  - 在不同的视图函数中，request对象都表示和视图函数对应的请求，也就是当前请求(currentrequest)。而程序也会有多个程序实例的情况，为了能获取对应的程序实例，而不是固定的某一个程序实例，我们就需要使用current_app变量
  
  - g存储在程序上下文中，而程序上下文会随着每一个请求的进入而激活，随着每一个请求的处理完毕而销毁，所以每次请求都会重设这个值。
  
  - 

![](D:\Cache\MarkText\2022-08-08-15-37-51-image.png)

##### 激活上下文

- 在下面这些情况下，Flsk会自动帮我们激活程序上下文：
  
  - 当我们使用flask run命令启动程序时。
  
  - 使用旧的app.run()方法启动程序时。
  
  - 执行使用@app.cli.command()装饰器注册的flask命令时。
  
  - 使用flask shell命令启动Python Shell时。

- 我们可以在视图函数中或在视图函数内调用的函数/方法中使用所有上下文全局变量。

##### 上下文钩子

- Flask也为上下文提供了一个teardown_appcontext钩子，使用它注册的回调函数会在程序上下文被销毁时调用，而且通常也会在请求上下文被销毁时调用。

```python
@app.teardown appcontext
def teardown db(exception):
    db.close()
```

- 使用app.teardown_appcontext装饰器注册的回调函数需要接收异常对象作为参数，当请求被正常处理时这个参数值将是None,这个函数的返回值将被忽略。
