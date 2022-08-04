# 项目布局

 Python 项目使用 包 来管理代码，把代码分为不同的模块，然后在需要的地方导入模块。

```bash
/home/user/Projects/flask-tutorial
├── flaskr/
│   ├── __init__.py
│   ├── db.py
│   ├── schema.sql
│   ├── auth.py
│   ├── blog.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── blog/
│   │       ├── create.html
│   │       ├── index.html
│   │       └── update.html
│   └── static/
│       └── style.css
├── tests/
│   ├── conftest.py
│   ├── data.sql
│   ├── test_factory.py
│   ├── test_db.py
│   ├── test_auth.py
│   └── test_blog.py
├── venv/
├── setup.py
└── MANIFEST.in
```

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
