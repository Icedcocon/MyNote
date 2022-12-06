```yaml
# 内容
'1. Collections': 
  - List
  - Dictionary
  - Set
  - Tuple
  - Range
  - Enumerate
  - Iterator
  - Generator
'2. Types':
  - Type
  - String
  - Regular_Exp
  - Format, Numbers
  - Combinatorics
  - Datetime
'3. Syntax':
  - Args, Inline
  - Import
  - Decorator
  - Class
  - Duck_Types
  - Enum, Exception
'4. System':
  - Exit
  - Print
  - Input
  - Command_Line_Arguments
  - Open
  - Path
  - OS_Commands
'5. Data':
  - JSON
  - Pickle
  - CSV
  - SQLite
  - Bytes
  - Struct
  - Array
  - Memory_View
  - Deque
'6. Advanced':
  - Threading
  - Operator
  - Introspection
  - Metaprograming
  - Eval
  - Coroutine
'7. Libraries':
  - Progress_Bar
  - Plot
  - Table
  - Curses
  - Logging
  - Scraping
  - Web
  - Profile
  - NumPy
  - Image
  - Audio
  - Games
  - Data
```

```python
#######################################################################
# 2. Type
#######################################################################
# 2.1 Type
# 一切皆对象
# 对象有类型（type）
# 类型就是类（class）
# (1) 类型判断
# type() 不会认为子类是一种父类类型，不考虑继承关系。
<type> = type(<el>)               # 或: <el>.__class__
<bool> = isinstance(<el>, <type>) # 或: issubclass(type(<el>), <type>)
# isinstance() 会认为子类是一种父类类型，考虑继承关系
type('a'), 'a'.__class__, str     # (<class 'str'>, <class 'str'>, ...)

import time
import collections
# 1) 基本数据类型
print(type(1))                # (1)<class 'int'>
print(type(3.14))             # (2)<class 'float'>
print(type("hello"))          # (3)<class 'str'>
print(type([1, 2]))           # (4)<class 'list'>
print(type((1, "a")))         # (5)<class 'tuple'>
print(type({"name": "tom"}))  # (6)<class 'dict'>
print(type(False))            # (7)<class 'bool'>
print(type(set())             # (8)<class 'set'>
# 2) <class 'module'>
print(type(time))
# 3) <class 'type'>
print(type(type))
print(type(int))
print(type(float))
print(type(bool))
print(type(str))
print(type(dict))
print(type(list))
print(type(tuple))
print(type(set))
# 4) 自定义的类型：<class '__main__.XXX'>
class A:
    x = 111
    def __init__(self):
        self.x = 1
    def run(self):
        pass
a = A()
print(type(A))  # <class 'type'>
print(type(object))  # <class 'type'>
print(type(a))  # <class '__main__.A'>
# 5) <class 'NoneType'>
print(type(a.__init__()))
print(type(a.run()))
print(type(None))
# 6) <class 'builtin_function_or_method'>
print(type(bin))
print(type(len))
print(type(min))
print(type(dir))
# 7) <class 'collections.XXX'>
data = "message"
result = collections.Counter(data)
dict1 = collections.OrderedDict({"name": "Tom", "age": 25, "address": "CN"})
deq1 = collections.deque("abc")
print(type(result))  # <class 'collections.Counter'>
print(type(dict1))   # <class 'collections.OrderedDict'>
print(type(deq1))    # <class 'collections.deque'>

# (2) 部分类型没有内建名，需要被导入:
from types import FunctionType, MethodType, LambdaType
from types import GeneratorType, ModuleType

test1 = lambda x: x + 1
# 1) 判定是否是lambda类型。lambda就是函数类型，本质是一样的
print(type(test1) == LambdaType)  # True
# 2) 判定是否是函数类型
print(type(test1) == FunctionType)  # True
# 3) 判定是否是内置函数类型
print(type(bin) == BuiltinFunctionType)  # True
class Test2:
    def run(self):
        pass
test2 = Test2()
# 4) 判定是否是方法
print(type(test2.run) == MethodType)
# 5) 判定生成器类型
a = (x * x for x in range(1, 10))
print(type(a) == GeneratorType)
# 6) 判定模块类型
print(isinstance(time, ModuleType)

# (3) 抽象基类
# ①继承ABC的虚子类会被isinstance()和issubclass()函数识别为ABC的子类，却非如此
# ②但利用这一特性，可以根据一个类实现哪些方法来判断该类是哪种ABC的子类
# ③例如可迭代ABC需要iter()方法, 集合ABC需要iter(),contains()和len()方法
from collections.abc import Iterable, Collection, Sequence
isinstance([1, 2, 3], Iterable)         # True
|                  | Iterable | Collection | Sequence |
| ---------------- | -------- | ---------- | -------- |
| list, range, str | check    | check      | check    |
| dict, set        | check    | check      |          |
| iter             | check    |            |          |
from numbers import Number, Complex, Real, Rational, Integral
isinstance(123, Number)                # True
|                    | Number | Complex | Real  | Rational | Integral |
| ------------------ | ------ | ------- | ----- | -------- | -------- |
| int                | check  | check   | check | check    | check    |
| fractions.Fraction | check  | check   | check | check    |          |
| float              | check  | check   | check |          |          |
| complex            | check  | check   |       |          |          |
| decimal.Decimal    | check  |         |       |          |          |

# 2.2 String
# (1) 格式化方法
<str>  = <str>.format(*args, **kwargs)       # 格式化
<str>  = <str>.strip()                       # 字符串左右两侧去空白
<str>  = <str>.strip('<chars>')              # 左右两侧去掉指定字符（多次匹配）
<str>  = <str>.translate(<table>)            # 用str.maketrans()制作翻译表
# (2) 分解与连接方法
<list> = <str>.split()                       # 用空格分割字符串
<list> = <str>.split(sep=None, maxsplit=-1)  # 指定'sep'分割字符串指定次
<list> = <str>.splitlines(keepends=False)    # 在换行符处分割字符串，默认不保留
<str>  = <str>.join(<coll_of_strings>)       # 在每个元素间插入<str>字符串
<str>  = <str>.replace(old, new [, count])   # 将old替换为new最多count次
# (3) 搜索方法
<bool> = <sub_str> in <str>                  # 检查<str>中是否包含<sub_str>
<bool> = <str>.startswith(<sub_str>)         # 从前检测子串和起止点是否匹配
<bool> = <str>.endswith(<sub_str>)           # 从后检测子串和起止点是否匹配
<int>  = <str>.find(<sub_str>)               # 返回第一次出现sub的偏移值或-1
<int>  = <str>.index(<sub_str>)              # 类似但失败返回ValueError
# (4) 其他
<str>  = chr(<int>)                          # int转为Unicode字符
<int>  = ord(<str>)                          # Unicode字符转为int
# 还包括: 'lstrip()', 'rstrip()' and 'rsplit()'.
# 还包括: 'lower()', 'upper()', 'capitalize()' and 'title()'.
# (5) 属性方法
|               | [ !#$%…] | [a-zA-Z] | [¼½¾] | [²³¹] | [0-9] |
| ------------- | -------- | -------- | ----- | ----- | ----- |
| isprintable() | check    | check    | check | check | check |
| isalnum()     |          | check    | check | check | check |
| isnumeric()   |          |          | check | check | check |
| isdigit()     |          |          |       | check | check |
| isdecimal()   |          |          |       |       |       |
# 还包括: isspace()检测'[ \t\n\r\f\v\x1c-\x1f\x85\u2000…]'等空格
```

```python
#######################################################################
# 4. System
#######################################################################

# 4.1 Exit
# 通过引发SystemExit异常退出Python解释器。
import sys
sys.exit()                        # 退出 退出码为0 (success).
sys.exit(<el>)                    # 打印到stderr 并退出 退出码为1.
sys.exit(<int>)                   # 退出并指定退出码

# 4.2 Print
print(<el_1>, ..., sep=' ', end='\n', file=sys.stdout, flush=False)
# 参数file=sys.stderr可以输出到标准错误；flush=True可以强制刷新流
from pprint import pprint           # 一种更优雅的输出指令
pprint(<collection>, width=80, depth=None, compact=False, sort_dicts=True)

# 4.3 Input
<str> = input(prompt=None)        # 从stdin或管道中读取一行
                                  # (1) 文本中的换行符会被删除
                                  # (2) prompt提示会被打印到标准输出
                                  # (3) ctrl-d/ctrl-z/EOF 都会抛出EOFError

# 4.4 命令行参数
import sys
scripts_path = sys.argv[0]         # python脚本路径名
arguments    = sys.argv[1:]        # python脚本后跟的变量
from argparse import ArgumentParser, FileType
p = ArgumentParser(description=<str>) # 分割参数
p.add_argument('-<short_name>', '--<name>', action='store_true')# 标志
p.add_argument('-<short_name>', '--<name>', type=<type>)        # 选项
p.add_argument('<name>', type=<type>, nargs=1)                  # 1st参数
p.add_argument('<name>', type=<type>, nargs='+')                # 剩余参数
p.add_argument('<name>', type=<type>, nargs='*')                # 可选参数
args  = p.parse_args()                                          # 报错退出
value = args.<name>
                                   # help=<str>设置帮助中的参数描述
                                   # default=<el>设置默认值
                                   # type=FileType(<mode>)文件 可以encoding

# 4.5 Open
<file> = open(<path>, mode='r', encoding=None, newline=None)# 返回file对象
                                   # encoding=None 默认编码，推荐utf-8
                                   # newline=None 系统换行符与'\n'间自动转换
                                   # newline='' 不转换但仍根据'\n','\r'分行
# (1) Modes
# 'r'  - 只读 (默认).
# 'w'  - 只写 (截断).
# 'x'  - 只写 若文件存在则失败.
# 'a'  - 追加
# 'w+' - 读写 (截断).
# 'r+' - 从头读写.
# 'a+' - 从尾读写.
# 't'  - 文本模式 (默认).
# 'b'  - 二进制模式 ('br', 'bw', 'bx', …).
# (2) Exceptions
# 'FileNotFoundError' 使用 'r' or 'r+' 读取文件时可抛出.
# 'FileExistsError' 使用 'x' 写文件时可抛出.
# 'IsADirectoryError' 和 'PermissionError' 任何模式都可抛出.
# 'OSError' 上述 Exceptions 的父类.
# (3) File对象
<file>.seek(0)                      # 移到文件起始位置.
<file>.seek(offset)                 # 从文件开始移动 'offset' 个字符/字节 .
<file>.seek(0, 2)                   # 移到文件尾.
<bin_file>.seek(±offset, <anchor>)  # Anchor: 0 开头, 1 当前位置, 2 结尾.
<str/bytes> = <file>.read(size=-1)  # 读取 'size' 个字符/字节 或到EOF.
<str/bytes> = <file>.readline()     # 返回一行 若EOF则返回空字符串/字节.
<list>      = <file>.readlines()    # 返回一个包含剩余所有行的列表
<str/bytes> = next(<file>)          # 使用缓存返回一行. 不要混用.
<file>.write(<str/bytes>)           # 写入字符串或字节对象
<file>.writelines(<collection>)     # 写入多个字符串或字节对象s.
<file>.flush()                      # 刷新缓存. 每 4096/8192 B 执行1次.
def read_file(filename):             # 读文件
    with open(filename, encoding='utf-8') as file:
        return file.readlines()
def write_to_file(filename, text):    # 写文件
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

# 4.6 Paths
from os import getcwd, path, listdir, scandir
from glob import glob
<str>  = getcwd()                   # 返回当前工作路径
<str>  = path.join(<path>, ...)     # 连接多个路径名组件
<str>  = path.abspath(<path>)       # 返回绝对路径名
<str>  = path.basename(<path>)      # 返回文件名
<str>  = path.dirname(<path>)       # 返回文件路径
<tup.> = path.split(<path>)            # (<dirname>,<basename>)
<tup.> = path.splitext(<path>)      # 分离扩展名(<pathname>,<ext>) .txt的扩展名为空
<list> = listdir(path='.')          # 列出path下的文件list
<list> = glob('<pattern>')          # 返回匹配的文件list
<bool> = path.exists(<path>)        # 或: <Path>.exists()
<bool> = path.isfile(<path>)        # 或: <DirEntry/Path>.is_file()
<bool> = path.isdir(<path>)         # 或: <DirEntry/Path>.is_dir()
                                    # follow_symlinks=false 链接为false
<stat> = os.stat(<path>)            # 或: <DirEntry/Path>.stat()
<real> = <stat>.st_mtime/st_size/...# 修改时间, 大小(bytes), …
# 与listdir()不同，scandir()返回DirEntry对象
# DirEntry对象缓存isfile、isdir和Windows上的stat信息，提高性能。
<iter> = scandir(path='.')          # 返回指定path的DirEntry对象
<str>  = <DirEntry>.path            # 返回完整路径
<str>  = <DirEntry>.name            # 返回文件名
<file> = open(<DirEntry>)           # 打开并返回文件对象.

# Path Object
from pathlib import Path
<Path> = Path(<path> [, ...])       # 可以是strings,Paths或DirEntry对象
<Path> = <path> / <path> [/ ...]    # 第1个或第2个<path>必须时Path object.
<Path> = Path()                     # 返回相对的cwd. 同 Path('.').
<Path> = Path.cwd()                 # 返回绝对cwd. 同 Path().resolve().
<Path> = Path.home()                # 返回用户的home目录 (绝对路径).
<Path> = Path(__file__).resolve()   # 如果没改变cwd的话 返回脚本绝对路径
<Path> = <Path>.parent              # 仅返回路径
<str>  = <Path>.name                # 仅返回文件名
<str>  = <Path>.stem                # 返回去掉扩展名的文件名
<str>  = <Path>.suffix              # 返回文件扩展名.
<tup.> = <Path>.parts               # 以字符串元组的形式返回所有路径.
<iter> = <Path>.iterdir()           # 使用Path对象返回文件夹内容.
<iter> = <Path>.glob('<pattern>')   # 返回与pattern匹配的文件.
<str>  = str(<Path>)                # 以字符串的形式返回路径.
<file> = open(<Path>)               # 同 <Path>.read/write_text/bytes().

# 4.7 OS 命令
import os, shutil, subprocess
os.chdir(<path>)                # 修改当前工作路径
os.mkdir(<path>, mode=0o777)    # 创建文件夹;八进制权限;目录存在抛OSerror
os.makedirs(<path>, mode=0o777) # 递归创建目录，`exist_ok=False` 存在报错
shutil.copy(from, to)           # 复制文件 'to' 是存在的文件或目录
shutil.copytree(from, to)       # 递归复制 'to' 必须不存在
os.rename(from, to)             # 重命名/移动文件或目录
os.replace(from, to)            # 同上，但'to'存在会被覆盖
os.remove(<path>)               # 删除文件
os.rmdir(<path>)                # 删除空目录
shutil.rmtree(<path>)           # 递归删除目录
# <path>可以使 strings, Paths 或者 DirEntry objects
# 上述函数抛出错误为 OSError 或其子类

# (1) os.popen
<pipe> = os.popen('<command>')  # 在sh或cmd中执行指令;返回stdout pipe
<str>  = <pipe>.read(size=-1)   # 读取'size'字节或到EOF;似readline/s()
<int>  = <pipe>.close()         # 关闭pipe;成功返回None
# (2) subprocess.run  用bc计算'1 + 1'并捕输出:
subprocess.run('bc', input='1 + 1\n', capture_output=True, text=True)
# (3) subprocess.run  将test.in中内容发送给bc (-s 标准模式)，将输出保存在test.out:
from shlex import split
os.popen('echo 1 + 1 > test.in')
subprocess.run(split('bc -s'), stdin=open('test.in'), \
stdout=open('test.out', 'w'), check=True) # 设置check在出错后终止运行
open('test.out').read()
# (4) subprocess.Popen玩猜数字游戏
process = subprocess.Popen(shlex.split('python3 guess.py'),\
stdin=subprocess.PIPE,stdout=subprocess.PIPE)
print(process.stdout.read1().decode())
process.stdin.write(f'{mid}\n'.encode())
process.stdin.flush()
```

```python
#######################################################################
# 5. Data
#######################################################################


# 5.2 yaml
```
