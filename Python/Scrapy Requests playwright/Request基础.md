### 介绍

##### 基本用法

- 响应内容

```python
import requests                             # 导入requests库
r = requests.get('https://www.baidu.com')   # 发送get请求并获取响应
r.status_code                    # (1) 状态码
r.history                        # (2) 历史状态码
r.headers['content-type']        # (3) 响应头
r.headers.get('content-type')    #     同上
r.encoding                       # (4) 编码算法()
r.text                           # (5) 字符串(以推测编码解码)
r.json                           # (6) 字典类型(将字符串转为字典)
r.content                        # (7) byte类型(不进行解码)
r.cookies['example_cookie_name'] # (8) cookies(类型为RequestCookieJar)
r.raw.read(10)                   # (9) raw格式(需令get中字典参数stream=True)
```

- 其他请求类型

```python
r = requests.post('https://www.baidu.com')
r = requests.put('https://www.baidu.com')
r = requests.delete('https://www.baidu.com')
r = requests.head('https://www.baidu.com')
r = requests.options('https://www.baidu.com')
```

##### get

- 参数

```python
# (1) 简单get请求
r = requests.get('https://www.baidu.com')

# (2) 带参数的get请求(value可为list)
payload = 'key1=value1&key2=value2&key2=value3'
r = requests.get(f'http://httpbin.org/get?{payload}')
payload = {'key1': 'value1', 'key2': ['value2', 'value3']} 
r = requests.get('https://httpbin.org/get', params=payload)

# (3) 带请求头的get请求
url = 'https://api.github.com/some/endpoint'
headers = {'user-agent': 'my-app/0.0.1'}        # 字典类型
r = requests.get(url, headers=headers)

# (4) 带cookies的get请求
jar = requests.cookies.RequestsCookieJar()
jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies')
jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere')
url = 'https://httpbin.org/cookies'
r = requests.get(url, cookies=jar)

# (5) 为get设置超时时间
requests.get('https://github.com/', timeout=0.001)
```

##### post

- 参数

```python
# (1) 简单post请求
r = requests.post("https://httpbin.org/post")
# (2) 带body的post请求(value可以是列表、元组)
payload = {'key1': 'value1', 'key2': 'value2'}                
r0 = requests.post("https://httpbin.org/post", data=payload)
payload_tuples = [('key1', 'value1'), ('key1', 'value2')]     # 等价
r1 = requests.post('https://httpbin.org/post', data=payload_tuples)
payload_dict = {'key1': ['value1', 'value2']}                 # 等价
r2 = requests.post('https://httpbin.org/post', data=payload_dict)
# (3) 直接传递字符串而非字典类型(不能设置Content-Type)
import json
url = 'https://api.github.com/some/endpoint'
payload = {'some': 'data'}
r = requests.post(url, data=json.dumps(payload)) # 等价
r = requests.post(url, json=payload)             # 等价,指定data/file时忽略
```

- post请求头数据来源
  
  - 1.固定值                   在普通窗口和隐私窗口中值不变化
  - 2.输入值                   在普通窗口和隐私窗口中值根据自身变化
  - 3.预设值-静态文件   需要提前从html中获取
  - 4.预设值-发请求      需要对指定地址发送请求
  - 5.在客户端生成       分析js,模拟生成数据

##### 场景

- 常用

```python
# (1) 获取二进制数据
import requests
r = requests.get('https://www.baidu.com/favicon.ico')
with open('favicon.ico','wb') as f:
  f.write(r.content)

# (2) 上传文本文件
files = {'file': open('report.xls', 'rb')}
files = {'file': ('report.xls', \                     # 传递文件名
         open('report.xls', 'rb'), \                  # 文件
         'application/vnd.ms-excel', \                # 文件类型
         {'Expires': '0'})}                           # 请求头
files = {'file': ('report.csv', \                     # 传递文件名
         'some,data,to,send\nanother,row,to,send\n')} # 将字符串作为文件
r = requests.post(url, files=files)

# (3) Session会话维持
s = requests.Session()   # 两次调用get为两次会话，session可维持cookies不变
s.get('http://httpbin.org/cookies/set/number/123456789')
r = s.get('http://httpbin.org/cookies')

# (4) SSL证书验证
# 访问持有不被CA机构信任的证书网站
resposne = requests.get('https://www.12306.cn',verify=False) 
# 设置verify=False依然存在警告，消除警告方式：
from requests.packages import urllib3
urllib3.disable_warnings()
# 指定客户端证书
response = requests.get('https://www.12306.cn',\
                         cert('/path/server.crt','/path/key'))

# (5) 身份验证
from requests.auth import HTTPBasicAuth
r = requests.get('http://localhost:8080/manager/html',\
                  auth=HTTPBasicAuth('admin','123456')     # 等价
 r = requests.get('http://localhost:8080/manager/html',\
                   auth=('admin','123456'))                
```

- 代理

```python
# (1) 简单代理
import requests
proxies = {
    'http': 'http://161.35.4.201:80',  # 可以是本地代理
    'https': 'https://161.35.4.201:80' # 可以是本地代理
}
try:
    response = requests.get('http://httpbin.org/get', proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)

# (2) Basic Auth
proxies = {
  "http":"http://user:password@161.35.4.201:80"
}
r = requests.get("https://www.taobao.com",proxies=proxies)

# (3) SOCKS协议的代理
pip3 install 'requests[socks]'

import requests
proxies = {
  'http':'socks5://user:password@host:port',
  'https':'socks5://user:password@host:port'
}
request.get('https://www.taobao.com',proxies=proxies)
```

### 参考资料

- https://requests.readthedocs.io/en/stable/
