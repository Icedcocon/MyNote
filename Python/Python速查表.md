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
  - Collections
'2. Types':
  - Type
  - String
  - Regular_Exp
  - Format
  - Numbers
  - Combinatorics
  - Datetime
'3. Syntax':
  - Args
  - Splat 
  - Inline
  - Import
  - Decorator
  - Class
  - Duck_Types
  - Enum
  - Exception
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
  - Multiprocessing

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
# 1. Collections
#######################################################################

# 1.9 Collections-Collections
# 1.9.1 Collections-Collections-常见类型
# collections时Python内建集合模块，实现多种特殊容器数据类型，是内置容器的替代方案
# (1)namedtuple   用于创建具有命名字段的 tuple 子类的 factory 函数 (具名元组)
# (2)deque        类似 list 的容器，两端都能实现快速 append 和 pop (双端队列)
# (3)ChainMap     类似 dict 的类，用于创建多个映射的单视图
# (4)Counter      用于计算 hashable 对象的 dict 子类 (可哈希对象计数)
# (5)OrderedDict  记住元素添加顺序的 dict 子类 (有序字典)
# (6)defaultdict  dict 子类调用 factory 函数来提供缺失值
# (7)UserDict     包装 dict 对象以便于 dict 的子类化
# (8)UserList     包装 list 对象以便于 list 的子类化
# (9)UserString   包装 string 对象以便于 string 的子类化

# 1.9.2 Collections-Collections-namedtuple
# (1) 内建普通元组tuple存在不能为元素命名的局限，因此表达意义不明显
# (2) 引入工厂函数collections.namedtuple,构造带字段名的具名元组 
# (3) 两者实例消耗内存相同 (因字段名被保存在对应类中) 但更易理解(即自文档)和维护
# (4) 具名元组不用命名空间字典__dict__ 存放/维护实例属性，更加轻量和快速
# (5) 具名元组namedtuple继承自tuple,属性均不可变
collections.namedtuple(typename, \        # 具名元组名称
                       field_names, \     # 字段名称['x','y']或'x y'或'x,y'
                       *, \
                       verbose=False, \
                       rename=False, \
                       module=None)
# 返回一个tuple子类
from collections import namedtuple
Point = namedtuple("Point", ['x', 'y']) # 初始化一个具名元组 Point
Point                                   # <class '__main__.Point'> 自定义
p1 = Point(2, 3)                        # 实例化Point对象p1
p1                                      # Point(x=2, y=3) 调用__repr__
p1.x                                    # 2 通过字段名获取元素值/字段值
p1[0]                                   # 2 通过索引获取元素值/字段值
for i in p1:                            # 2 3 通过迭代获取元素值/字段值
    print(i)
a, b = p1                               # 能够像普通tuple一样unpack
# 类属性_fields: 获取所有字段名构成的元组
p1._fields              # ('x','y') 获取所有字段名构成的 tuple
# 类方法_make(iterable): 用序列sequence/可迭代对象iterable创建新实例
p2 = p1._make([5, 6])   # Point(x=5, y=6) 实例化一个新Point对象
# 实例方法_replace(**kwargs): 基于实例修改、替换元素生成新实例
p3 = p1._replace(y=4.5) # Point(x=2, y=4.5) 实例化一个新Point对象
# 实例方法_asdict(): 转为collections.OrdereDict对象,用于友好地展示信息
p1._asdict()              # 将namedtuple对象转换为OrderedDict对象
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


# 2.3 Regex正则表达
# 2.3.1 Type-Regex正则表达-常用方法
import re
<Pattern>=re.compile(<str>,flag=0)             # Pattern可调用以下re方法
<str>   = re.sub(<regex>, new, text, count=0)  # new替换所有匹配项
<list>  = re.findall(<regex>, text)            # 返回所有匹配项
<list>  = re.split(<regex>, text, maxsplit=0)  # 将<re>做分隔符分割text
<Match> = re.search(<regex>, text)             # 查找第一个匹配项
<Match> = re.match(<regex>, text)              # 从文本开头查找匹配项
<iter>  = re.finditer(<regex>, text)           # 返回所有的Match object
# (0) <regex> = r'...'
# (1) 参数'new'可以是一个接受Match对象并返回字符串的函数。
# (2) Search()和match()如果找不到匹配则返回None。
# (3) 参数'flags=re.IGNORECASE' 忽略大小写
# (4) 参数'flags=re.MULTILINE'  令'^'和'$'匹配每行的开始/结束等换行符
# (5) 参数'flags=re.DOTALL'     令'.'运算符可以匹配'\n'。
# (6) r'\1'或'\\1'可在new中用于指明<regex>中的group，从而灵活替换
# (7) 在'*'或'+'后添加'?'采用非贪婪模式，即选择尽可能少的字符串匹配

# 2.3.2 Type-Regex正则表达-Match Object
<str>   = <Match>.group()      # 返回所有匹配项，相当于group(0).
<str>   = <Match>.group(1)     # 仅返回第一个括号中的部分
<tuple> = <Match>.groups()     # 返回所有括号中的部分
<int>   = <Match>.start()      # 返回匹配项的开始索引
<int>   = <Match>.end()        # 返回匹配项的唯一结束索引

# 2.3.3 Type-Regex正则表达-Special Sequences 特殊字符序列
'\d' == '[0-9]'                # 匹配整数字符
'\w' == '[a-zA-Z0-9_]'         # 匹配字母、数字和下划线。
'\s' == '[ \t\n\r\f\v]'        # 匹配空格
'(.*?)'                        # 仅返回()内
                               # '.'匹配任何字符
                               # '*'匹配任意多个前一个字符
                               # '?'非贪婪模式，尽可能少的字符串
# \number        \number 匹配相同编号的组的内容
# \A            \A 仅匹配字符串的开头
# \Z            \Z 仅匹配字符串的末尾
# \b            \b 匹配空字符串，但只匹配单词的开头或结尾。
# \B            \B 匹配空字符串，但不匹配单词的开头或结尾
# \d             \d 匹配任何十进制数字 即0-9
# \D            \D 匹配任何非数字字符,相当于 [^\d]
# \s            \s 匹配任何空白字符,即空格、tab键
# \S            \S 匹配任何非空白字符；相当于 [^\s]
# \w            \w 匹配任何字母数字字符,即a-z、A-Z、0-9、_
# \W            \W 匹配 \w 的补码,即匹配非单词字符
# \\            \\ 匹配文字反斜杠
# (1) \d\w\s默认匹配所有编码的十进制字符和空格，除非设置'flags=re.ASCII'

# 2.3.4 Type-Regex正则表达-字符匹配符号
# .             匹配除换行符(\n)以外的任何1个字符
# ^             匹配字符串的开头
# $             匹配字符串的结尾或字符串结尾的换行符之前
# *             匹配前面 RE 的 0 个或多个（贪婪）重复。贪婪意味着它将匹配尽可能多的重复。
# +             匹配前面 RE 的 1 个或多个（贪婪）重复
# ?             匹配前面 RE 的 0 或 1（贪婪）
# *?,+?,??     前三个特殊字符(*,+,?)的非贪婪版本
# {m,n}         匹配前面 RE 的 m 到 n 次重复
# {m,n}?     上述的非贪婪版
# \\         转义特殊字符或表示特殊序列
# []          [] 表示一组字符。匹配[]中列举的字符
# |             A|B，创建一个匹配 A 或 B 的 RE
# (...)         (...) 匹配括号内的 RE。稍后可以在字符串中检索或匹配内容。
# (?aiLmsux) 为 RE 设置 A、I、L、M、S、U 或 X 标志
# (?:...)      (?:...) 正则括号的非分组版本

# 2.3.5 Type-Regex正则表达-常用表达式
# 非负整数：^\d+$
# 正整数：^[0-9]*[1-9][0-9]*$ 
# 非正整数：^((-\d+)|(0+))$ 
# 负整数：^-[0-9]*[1-9][0-9]*$ 
# 整数：^-?\d+$ 
# 浮点数（即小数）：(-?\d*)\.?\d+
# 任何数字 ：(-?\d*)(\.\d+)? 

# 英文字符串：^[A-Za-z]+$ 
# 英文大写串：^[A-Z]+$ 
# 英文小写串：^[a-z]+$ 
# 英文字符数字串：^[A-Za-z0-9]+$ 
# 英数字加下划线串：^\w+$ 

# E-mail地址：^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$ 
# URL：^[a-zA-Z]+://(\w+(-\w+)*)(\.(\w+(-\w+)*))*(\?\s*)?$ 
# 或：^http:\/\/[A-Za-z0-9]+\.[A-Za-z0-9]+[\/=\?%\-&_~`@[\]\':+!]*([^<>\"\"])*$ 
# 中文：^[\u0391-\uFFE5]+$ 
# 双字节字符(包括汉字在内)：^\x00-\xff 
# 匹配首尾空格：(^\s*)|(\s*$)（像vbscript那样的trim函数） 
# 匹配HTML标记：<(.*)>.*<\/\1>|<(.*) \/>
# 匹配空行：\n[\s| ]*\r
# 网络链接：(h|H)(r|R)(e|E)(f|F)  *=  *('|")?(\w|\\|\/|\.)+('|"|  *|>)?
# 邮件地址：\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*
# 图片链接：(s|S)(r|R)(c|C)  *=  *('|")?(\w|\\|\/|\.)+('|"|  *|>)?
# IP地址：(\d+)\.(\d+)\.(\d+)\.(\d+)
# 中国手机号码：(86)*0*13\d{9}
# 中国固定电话号码：(\d3,4\d3,4|\d{3,4}-|\s)?\d{8}
# 中国电话号码（包括移动和固定电话）：(\d3,4\d3,4|\d{3,4}-|\s)?\d{7,14}
# 中国邮政编码：[1-9]{1}(\d+){5}
# 邮政编码：^[1-9]\d{5}$

# 2.4 Types-Format
# 2.4.0 Types-Format-格式化方法及r、u、f、b
<str> = f'{<el_1>}, {<el_2>}'               # f''中大括号含变量名可变量替换
<str> = '{}, {}'.format(<el_1>, <el_2>)     # 等价（上）
<str> = '{0}, {a}'.format(<el_1>, a=<el_2>) # 等价（下）
<str> = '%s, %s' % (<el_1>, <el_2>)         # 冗余的C风格格式化
# r""字符串保留转义字符,\n\t等不进行转义,常用于正则表达式; 
# u""字符串使用unicode编码,防止源码存储格式导致乱码,常用于中文字符前; 
# f""字符串的大括号内支持python表达式，常用于变量替换; 
# b""字符串使用byte类型，常用于网络编程中的数据收发，send()、resv()使用byte类型

# 2.4.1 Types-Format-Attributes
collections.namedtuple('Person', 'name height')
person = Person('Jean-Luc', 187)
f'{person.height}'                # 187 等价
'{p.height}'.format(p=person)     # 187 等价

# 2.4.2 Types-Format-对齐
{<el>:<10}                               # '<el>      '
{<el>:^10}                               # '   <el>   '
{<el>:>10}                               # '      <el>'
{<el>:.<10}                              # '<el>......'
{<el>:0}                                 # '<el>'
# (1) 可以动态生成对其配置: f'{<el>:{<str/int>}[…]}'
# (2) 冒号前添加'!r'在调用repr()时将打印字符串而非对象

# 2.4.3 Types-Format-Strings
{'abcde':10}                             # 'abcde     '
{'abcde':10.3}                           # 'abc       '
{'abcde':.3}                             # 'abc'
{'abcde'!r:10}                           # "'abcde'   "

# 2.4.4 Types-Format-Numbers
{123456:10}                              # '    123456'
{123456:10,}                             # '   123,456'
{123456:10_}                             # '   123_456'
{123456:+10}                             # '   +123456'
{123456:=+10}                            # '+   123456'
{123456: }                               # ' 123456'
{-123456: }                              # '-123456'

# 2.4.5 Types-Format-Floats
{1.23456:10.3}                           # '      1.23'
{1.23456:10.3f}                          # '     1.235'
{1.23456:10.3e}                          # ' 1.235e+00'
{1.23456:10.3%}                          # '  123.456%'

# 2.4.5 Types-Format-Floats(进位补充)
round(number[, ndigits])        # 等价于f'{number:.ndigitsf}'
# (1) ndigits不为0的情况:
#     1) 保留位数后一位小于等于4,则舍去，如 round(5.214,2) = 5.21
#     2) 保留位数后一位等于5,且该位数后无数字,不进位,如round(5.215,2)=5.21
#     3) 保留位数后一位等于5,且该位数后有数字,则进位,如round(5.2151,2)=5.22
#     4) 保留位数后一位大于等于6,则进位。如 round(5.216,2) = 5.22
#     5) 规则2有例外,如round(0.645,2)=0.65,因为浮点数二进制表示是近似值
# (2) 再说下ndigits为0或None的情况：
#     1) 保留位数后一位小于等于4,则舍去,如round(1.4) = 1
#     2) 保留位数后一位等于5,且后无数字,则取最近偶数,如round(1.5)=2,round(2.5)=2
#     3) 保留位数后一位等于5,且后有数字,则近位,如round(2.51)=3
#     4) 保留位数后一位大于等于6 ,则进位,如 round(1.6) = 2
# (3) 实现四舍五入
import decimal
decimal.getcontext().rounding = "ROUND_HALF_UP"              # 设置舍入方式
x = "0.645"
x1 = decimal.Decimal(x).quantize(decimal.Decimal("0.00")) # x1 = '0.65'
y = "2.5"
y1 = decimal.Decimal(y).quantize(decimal.Decimal("0"))      # y1 = '2'

# 2.4.6 Types-Format-Ints
{90:c}                                   # 'Z'
{90:b}                                   # '1011010'
{90:X}                                   # '5A'

# 2.5 Types-Numbers
# 2.5.1 Types-Numbers-int/float/complex/fractions
<int>      = int(<float/str/bool>)        # Or: math.floor(<float>)
<float>    = float(<int/str/bool>)        # Or: <real>e±<int>
<complex>  = complex(real=0, imag=0)      # Or: <real> ± <real>j
<Fraction> = fractions.Fraction(0, 1)     # Or: Fraction(numerator=0, denominator=1)
<Decimal>  = decimal.Decimal(<str/int>)   # Or: Decimal((sign, digits, exponent))
# (1) 'int(<str>)' 和 'float(<str>)' 传入非法字符会抛出 ValueError
# (2) Decimal可以精确存储数字，不像float那样不精确
# (3) 浮点数可以用以下方法进行比较 'math.isclose(<float>, <float>)'
# (4) Decimal运算精度通过以下方式设置 'decimal.getcontext().prec = <int>'.

# 2.5.2 Types-Numbers-Basic Functions基本函数
<num> = pow(<num>, <num>)               # Or: <num> ** <num>
<num> = abs(<num>)                      # <float> = abs(<complex>)
<num> = round(<num> [, ±ndigits])       # `round(126, -1) == 130`

# 2.5.3 Types-Numbers-Math数学计算和符号
from math import e, pi, inf, nan, isinf, isnan    # `<el> == nan`永远为False.
from math import sin, cos, tan, asin, acos, atan  # 还有 degrees, radians.
from math import log, log10, log2                 # log可以接受基数作为第二参数

# 2.5.4 Types-Numbers-Statistics数理统计函数
from statistics import mean, median, variance  # 还有stdev, quantiles, groupby

# 2.5.5 Types-Numbers-Random随机数
from random import random, randint, choice  # 还有shuffle,gauss,triangular,seed
<float> = random()                          # [0, 1)间的浮点数
<int>   = randint(from_inc, to_inc)         # [from_inc, to_inc]间的整数
<el>    = choice(<sequence>)                # 保持序列完整

# 2.5.6 Types-Numbers-Bin, Hex
<int> = ±0b<bin>             # Or: ±0x<hex>
<int> = int('±<bin>', 2)     # Or: int('±<hex>', 16)
<int> = int('±0b<bin>', 0)   # Or: int('±0x<hex>', 0)
<str> = bin(<int>)           # 返回 '[-]0b<bin>'.

# 2.5.7 Types-Numbers-Bitwise Operators位操作
<int> = <int> & <int>          # 且  (0b1100 & 0b1010 == 0b1000).
<int> = <int> | <int>          # 或  (0b1100 | 0b1010 == 0b1110).
<int> = <int> ^ <int>          # 异或 (0b1100 ^ 0b1010 == 0b0110).
<int> = <int> << n_bits        # 左移  >> 用于右移
<int> = ~<int>                 # 非 也可用 -<int> 如 - 1

# 2.6 Types-Combinatorics
# 每个函数都会返回一个迭代器
# 打印可传递给list()函数
import itertools as it
>>> it.product([0, 1], repeat=3)
[(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
 (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
>>> it.product('abc', 'abc')                      #   a  b  c
[('a', 'a'), ('a', 'b'), ('a', 'c'),              # a x  x  x
 ('b', 'a'), ('b', 'b'), ('b', 'c'),              # b x  x  x
 ('c', 'a'), ('c', 'b'), ('c', 'c')]              # c x  x  x
>>> it.combinations('abc', 2)                     #   a  b  c
[('a', 'b'), ('a', 'c'),                          # a .  x  x
 ('b', 'c')]                                      # b .  .  x
>>> it.combinations_with_replacement('abc', 2)    #   a  b  c
[('a', 'a'), ('a', 'b'), ('a', 'c'),              # a x  x  x
 ('b', 'b'), ('b', 'c'),                          # b .  x  x
 ('c', 'c')]                                      # c .  .  x
>>> it.permutations('abc', 2)                     #   a  b  c
[('a', 'b'), ('a', 'c'),                          # a .  x  x
 ('b', 'a'), ('b', 'c'),                          # b x  .  x
 ('c', 'a'), ('c', 'b')]                          # c x  x  .
```

```python
#######################################################################
# 3. Syntax
#######################################################################
# 3.1 Syntax-Arguments
# 3.1.1 Syntax-Arguments-函数调用、函数定义、可变对象做默认值
# (1) 函数调用
func(<positional_args>)                           # func(0, 0)
func(<keyword_args>)                              # func(x=0, y=0)
func(<positional_args>, <keyword_args>)           # func(0, y=0)
# (2) 函数定义
def func(<nondefault_args>): ...                  # def func(x, y): ...
def func(<default_args>): ...                     # def func(x=0, y=0): ...
def func(<nondefault_args>, <default_args>): ...  # def func(x, y=0): ...
# (3) 注意
# def语句会创建函数对象并初始化，默认值指向的可变对象内存地址仅在初始化时设置一次
# 每次调用函数会在局部作用域内创建默认值变量，并将变量指向可变对象内存地址
# 若默认值是可变对象(如list)则每次调用函数对可变对象的修改都将传递到下一次调用
def func(data=[]):
    data.append('end')
    print(data)
func()        # ['end']
func()        # ['end', 'end']
# 建议默认值设为None并在函数内部判断
def func(data = None):
    if data is None:
        data = ['end']          # data指向新开辟并初始化的list内存地址
    else:
        data.append('end')      # 防御可变参数 data = list(data)
    print(data)
func()        # ['end']-
func()        # ['end', 'end']

# 3.1.2 Syntax-Arguments-Scope
# (1) 外围模块是全局作用域,相对当前模块导入模块的变量变成导入模块的属性
# (2) 全局作用域的作用范围仅限于单个文件
# (3) 赋值的变量名除非被声明为global或nonlocal,否则均为局部变量
#     global修改或创建全局变量;nonlocal修改但不能创建外层
# (4) 函数未定义的变量名被假定为外层函数的局部变量、全局变量或内置变量
# (5) 函数的每次调用都会创建一个新的局部作用域,函数间的局部变量相互独立


# 3.2 Splat Operator
# 3.2.1 Syntax-Splat Operator-函数调用时的splat运算符
# splat运算符(*)将集合展开为位置参数
# splty-Splat运算符(**)将字典展开为关键字参数
args   = (1, 2)
kwargs = {'x': 3, 'y': 4, 'z': 5}
func(*args, **kwargs)            # 等价于下行
func(1, 2, x=3, y=4, z=5)        # 等价于上行

# 3.2.2 Syntax-Splat Operator-函数定义时的splat运算符
# splat运算符(*)将零个或多个位置参数组合到元组中
# splty-Splat运算符(**)将零个或多个关键字参数组合到字典中
def add(*a):
    return sum(a)
add(1, 2, 3)        # 6
# 合法的参数组合:
def f(*args): ...               # f(1, 2, 3)
def f(x, *args): ...            # f(1, 2, 3)
def f(*args, z): ...            # f(1, 2, z=3)
def f(**kwargs): ...            # f(x=1, y=2, z=3)
def f(x, **kwargs): ...         # f(x=1, y=2, z=3) | f(1, y=2, z=3)
def f(*args, **kwargs): ...     # f(x=1, y=2, z=3) | f(1, y=2, z=3) |
                                # f(1, 2, z=3)     | f(1, 2, 3)
def f(x, *args, **kwargs): ...  # f(x=1, y=2, z=3) | f(1, y=2, z=3) |
                                # f(1, 2, z=3)     | f(1, 2, 3)
def f(*args, y, **kwargs): ...  # f(x=1, y=2, z=3) | f(1, y=2, z=3)
def f(*, x, y, z): ...          # f(x=1, y=2, z=3)
def f(x, *, y, z): ...          # f(x=1, y=2, z=3) | f(1, y=2, z=3)
def f(x, y, *, z): ...          # f(x=1, y=2, z=3) | f(1, y=2, z=3) |
                                # f(1, 2, z=3)

# 3.2.3 Syntax-Splat Operator-splat运算符其他用法
<list>  = [*<coll.> [, ...]]    # Or: list(<collection>) [+ ...]
<tuple> = (*<coll.>, [...])     # Or: tuple(<collection>) [+ ...]
<set>   = {*<coll.> [, ...]}    # Or: set(<collection>) [| ...]
<dict>  = {**<dict> [, ...]}    # Or: dict(**<dict> [, ...])
head, *body, tail = <coll.>     # Head 或 tail 可以被省略

# 3.3 Syntax-Inline
# 3.3.1 Syntax-Inline-Lambda函数
<func> = lambda: <return_value>                     # 单个语句函数
<func> = lambda <arg_1>, <arg_2>: <return_value>    # 可接受默认参数

# 3.3.2 Syntax-Inline-Comprehensions推导式
<list> = [i+1 for i in range(10)]         # Or: [1, 2, ..., 10]
<iter> = (i for i in range(10) if i > 5)  # Or: iter([6, 7, 8, 9])
<set>  = {i+5 for i in range(10)}         # Or: {5, 6, ..., 14}
<dict> = {i: i*2 for i in range(10)}      # Or: {0: 0, 1: 2, ..., 9: 18}
[l+r for l in 'abc' for r in 'abc']       # ['aa', 'ab', 'ac', ..., 'cc']

# 3.3.3 Syntax-Inline-Map, Filter, Reduce
# 对可迭代对象元素进行操作
<iter> = map(lambda x: x + 1, range(10))    # Or: iter([1, 2, ..., 10])
# 对可迭代对向进行过滤，返回True/False
<iter> = filter(lambda x: x > 5, range(10)) # Or: iter([6, 7, 8, 9])
# 对可迭代对象进行组合，函数需要传入两个值，会将结果传入下一次迭代进行处理
<obj>  = reduce(lambda out, x: out + x, range(10))  # Or: 45
# 使用reduce需要导入Reducefunctools模块

# 3.3.4 Syntax-Inline-Any, All
<bool> = any(<collection>)        # 有元素为True则返回True
any([0, '', [], None]) == False
<bool> = all(<collection>)        # 空或所有元素都为True则返回True

# 3.3.5 Syntax-Inline-Conditional Expression条件表达式
<obj> = <exp> if <condition> else <exp>         # 只有一个表达式会执行
>>> [a if a else 'zero' for a in (0, 1, 2, 3)]  # ['zero', 1, 2, 3]

# 3.3.6 Syntax-Inline-Named Tuple, Enum, Dataclass
from collections import namedtuple
Point = namedtuple('Point', 'x y')                 # 创建元组子类
point = Point(0, 0)                                # 返回实例
from enum import Enum
Direction = Enum('Direction', 'N E S W')           # 创建枚举类型
direction = Direction.N                            # 返回值
from dataclasses import make_dataclass
Player = make_dataclass('Player', ['loc', 'dir'])  # 创建dataclass
player = Player(point, direction)                  # 返回实例

# 3.4 Syntax-Class
# 3.4.1 Syntax-Class-__repr__和__str__
class <name>:
    def __init__(self, a):
        self.a = a
    def __repr__(self):
        class_name = self.__class__.__name__
        return f'{class_name}({self.a!r})'
    def __str__(self):
        return str(self.a)
# (1) repr()返回值应明确且无歧义 str()返回值应适合人类阅读
# (2) 只定义repr()未定义str()时 调用str()执行的是repr()
# (3) 调用str()的场合
print(<el>)
f'{<el>}'
logging.warning(<el>)
csv.writer(<file>).writerow([<el>])
raise Exception(<el>)
# (4) 调用repr()的场合
print/str/repr([<el>])
f'{<el>!r}'
Z = dataclasses.make_dataclass('Z', ['a']); print/str/repr(Z(<el>))
<el>

# 3.4.2 Syntax-Class-@staticmethod和@classmethod
class <name>:
    def __init__(self, a):
        self.a = a
    @classmethod
    def get_class_name(cls):
        print cls.__name__
        res = cls()
        return res
    @classmethod
    def singleton(cls):
        if not cls.__instance:
            cls.__instance = cls('duoduo', [])
        return cls.__instance
# (0) Python支持的类相关方法
#  1) 实例方法：第一个参数为self实例对象（默认）
#  2) 静态方法：不传入额外对象（通过@staticmethod）
#  3) 类方法 ：第一个参数为cls类对象（通过@classmethod，元类中默认）
# (1) 共同：
#  1) "@staticmethod"或"@classmethod"可以不实例化直接以类名.方法名()调用
# (2) 不同： 
#  1) "@staticmethod"修饰的方法不接受"self"或"cls"而"@classmethod"接受"cls"
#     两者都可以调用类属性/方法 而"@classmethod"还能调用对象方法/属性
#  2) "@classmethod"可以区分自己被基类还是子类调用 可在子类中新增功能而不改基类
# (3) 用途
#  1) "@staticmethod"用于需要简单函数但仅为类服务的场合，可以节省创建对象的开支
#  2) "@classmethod"可以实现单例模式、工厂模式;可用于对象数据的预处理(子类新功能) 

# 3.4.3 Syntax-Class-构造函数重载
# （拦截内置的构造函数操作，并调用自定义方法，__init__是一个入口）
class <name>:
    def __init__(self, a=None):
        self.a = a
    def __new__(cls):
      return super().__new__(cls)
# (1) 实例创建过程中__new__方法先被调用,创建并返回新实例对象,后传入__init__初始化
# (2) 类实例化前先调用__new__方法创建实例，是类方法
# (3) 实例对象创建后调用__init__方法初始化实例,是实例对象的方法,设置实例对象的初始值

# 3.4.4 Syntax-Class-继承及类接口技术
# (0)继承概念:obj.attr运算会触发继承，Python自底向上搜索命名空间树，下层定义屏蔽上层
#    属性树构造:1.实例属性(self.a=v)2.类属性(class A:b=v)3.父类连接(class B(A))
# (1) Super:    定义一个method函数以及一个delegate函数
class Super:
    def method(self):
        print('in Super.method')
    def delegate(self):        
        self.action()          # 未被定义 （也可用@abstractmethod修饰）
# (2) Inheritor:没有提供任何新的变量名，因此会获得Super中定义的一切内容
class Inheritor(Super):
    pass
# (3) Replacer: 用自己的版本授盖Super的method
class Replacer(Super):
    def method(self):       # 完全代替
        print("in Replacer.method")
# (4) EXtender: 覆盖并回调默认method，从而定制Super的method
class Extender(Super):
    def method(self):      # 方法扩展
        print('starting Extender.method')
        Super.method(self)
        print('ending Extender.method')
# (5) Providel: 实现Super的delegate方法预期的action方法。
class Provider(Super):
    def action(self):                       # 补充所需方法


# 3.4.5 Syntax-Class-多重继承
class A: pass
class B: pass
class C(A, B): pass
# MRO决定命名空间树的搜索顺序
>>> C.mro()
[<class 'C'>, <class 'A'>, <class 'B'>, <class 'object'>]

# 3.4.6 Syntax-Class-@property @name.setter @name.deleter
class Person:
# (1) property时内置装饰器函数 将类的方法伪装成属性并且不能再被()调用
# (2) 被property装饰后的方法，不能带除了self外的任何参数
# (3) 通常用于将私有属性隐藏，防止其被修改
    @property
    def name(self):
        return ' '.join(self._name)c
# (1) @name.setter中的name并不一定与函数名相同,调用时以函数名为准
# (2) 可作为__getattr__和__setattr__重载的代替
    @name.setter
    def na(self, value):
        self._name = value.split()
# (1) @property 表示 只读
# (2) @property 和 @name.setter 表示 可读可写 
# (3) @property 和 @name.setter 和 @name.deleter 表示可读可写可删除
    @name.deleter
    def name(self):
        del self._name
>>> person = Person()
>>> person.na = '\t Guido  van Rossum \n'
>>> person.name
'Guido van Rossum'

# 3.4.7 Syntax-Class-Dataclass（自动生成init()、repr()和eq()）
from dataclasses import dataclass, field
@dataclass(init=True, repr=True, eq=True, order=False, frozen=False)
class <class_name>:
    <attr_name_1>: <type>
    <attr_name_2>: <type> = <default_value>
    <attr_name_3>: list/dict/set = field(default_factory=list/dict/set)
# 对象可以使用'order=True'进行排序 用'frozen=True'使数据类不可变
# 若让对象hashable，必须保证所有属性hashable且'frozen=True'
# <attr_name>: list = []'所有实例共享一个list, 用field()可以解决这个问题
# 对于任意类型的属性使用'typing.Any'类型
from dataclasses import make_dataclass
<class> = make_dataclass('<class_name>', <coll_of_attribute_names>)
<class> = make_dataclass('<class_name>', <coll_of_tuples>)
<tuple> = ('<attr_name>', <type> [, <default_value>])
# 其余类型的注解 (CPython解释器会忽略这些类型):
def func(<arg_name>: <type> [= <obj>]) -> <type>: ...
<var_name>: typing.List/Set/Iterable/Sequence/Optional[<type>]
<var_name>: typing.Dict/Tuple/Union[<type>, ...]

# 3.4.8 Syntax-Class-Slots
# 需要将属性字符串顺序赋值给__slot__属性，
# 仅__slot__列表内的名称可赋值为实例属性，可以不赋值但不赋值不能被使用
# 显著减少内存占用，优化速度，但与Python的灵活性相背离
class MyClassWithSlots:
    __slots__ = ['a']
    def __init__(self):
        self.a = 1

# 3.4.9 Syntax-Class-Copy
from copy import copy, deepcopy
# 赋值操作并不clone对象，仅创建引用并绑定到原对象，原对象的一切改变都将反映到赋值对象上
# copy操作clone第一层引用对象
# deepcopy操作递归clone对象
<object> = copy(<object>)
<object> = deepcopy(<object>)

# 3.5 Syntax-Decorator

# 3.5.0 Syntax-Decorator-第一类对象
# (1) 定义:第一类对象并不一定是类对象，而是指程序中的所有实体(变量、函数、队列、字典等)
# (2) 第一类对象具有以下特征：
#  1) 可以被存入变量或其他结构
#  2) 可以被作为参数传递给其他方法/函数
#  3) 可以被作为方法/函数的返回值
#  4) 可以在执行期被创建，而无需在设计期全部写出
#  5) 有固定身份
# (3) 固有身份概念:指实体有内部表示而非根据名字来识别，如匿名函数可以通过赋值叫任何名字
#                 大部分语言的基本类型的数值(int, float)等都是第一类对象,C数组不是
#                 C数组作为函数参数时，传递首元素地址，且丢失数组长度信息
#                 对于大多数的动态语言，函数/方法都是第一类对象

# 3.5.1 Syntax-Decorator-函数、内部函数
# (1) 函数是python中的一类对象，可以作为别的函数的参数、函数的返回值，赋值给变量或存储
#      在数据结构中
# (2) 内部函数(inner Functions)是在函数内定义的函数;内部函数只能在父函数内使用;

# 3.5.2 Syntax-Decorator-装饰器实现/原理
# (0) @my_decorator可以看作say_whee = my_decorator(say_whee)
def my_decorator(func):  # (1) 装饰器传入函数func作为自由变量 再返回函数wrapper
    def wrapper():       # (2) 定义内部函数，可取代无参数无返回值的函数
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper       # (3) 返回内部函数wrapper，取代被装饰的函数
def say_whee():
    print("Whee!")
say_whee = my_decorator(say_whee)  # (4) 进行装饰
@my_decorator                      # (5) 用语法糖进行装饰，效果相同
def say_whee():
    print("Whee!")
>>> say_whee()
Something is happening before the function is called.
Whee!
Something is happening after the function is called.

# 3.5.3 Syntax-Decorator-装饰器修饰带参数/返回值的函数
def do_twice(func):
    def wrapper_do_twice(*args, **kwargs): 
        # (1) 内部函数使用*args, **kwargs获取任意数量的参数，再传给func
        func(*args, **kwargs)
        func(*args, **kwargs)
        # (1.5) 内部函数无返回值，可装饰无需返回值的函数
    return wrapper_do_twice

def do_twice(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
        # (2) 内部函数有返回值，则装饰后的函数可获取返回值
    return wrapper_do_twice
@do_twice
def say_whee():
    print("Whee!")
    return "Whell!"
>>> say_whee()
Whee!         # 第1次打印
Whee!         # 第2次打印
'Whell!'    # 返回值

# 3.5.4 Syntax-Decorator-保留函数的信息
# (1) 包装后的函数是wrapper_do_twice，函数名的等信息都修改为
#     wrapper_do_twice的信息
>>> say_whee
<function do_twice.<locals>.wrapper_do_twice at 0x7f43700e52f0>
>>> say_whee.__name__
'wrapper_do_twice'

# (2) 使用functools.wraps修饰内部函数，并将被修饰函数作为参数传入装饰器
#     可保留有关原始功能的信息
import functools
def do_twice(func):
    @functools.wraps(func)
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper_do_twice

# 3.5.5 Syntax-Decorator-带参数的装饰器
def repeat(num_times):   
    # (1) 创建装饰器工厂函数，工厂函数的参数为装饰器要接受的参数
    def decorator_repeat(func):                 # 装饰器函数
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs): # 内部函数
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        return wrapper_repeat
        # (2) 本层返回实际装饰后的函数
    return decorator_repeat
    # (3) 工厂函数repeat(num_times)根据参数创建装饰器函数并返回
    #     装饰器函数再装饰say_whee函数
    # (4) 等价于 say_whee = repeat(num_times=4)(say_whee)
@repeat(num_times=4)
def say_whee():
    print("Whee!")

# 3.5.6 Syntax-Decorator-装饰器的典型行为
# (1) 把被装饰的函数替换成新函数
# (2) 两者接受相同的参数
# (3) 新函数（通常）返回被装饰函数本该返回的值
# (4) 做些额外的操作

# 3.5.7 Syntax-Decorator-自由变量、函数闭包、nonlocal
def make_averager():
    ############## 函数闭包 #############
    count = 0
    total = 0
    def averager(new_value):
        nonlocal count, total  # 自由变量
        count += 1
        total += new_value
        return total / count
    ####################################
    return averager
# (1) 自由变量(free variable): 未在本地作用域中绑定的变量，Cell间接引用自由变量
# (2) 自由变量的引用: closure --> cell --> free variable; 
#     cell用于解决多个closure引用自由变量，变量需要改变时要改变多个closure引用问题
# (3) 查看自由变量
function.__closure__                # 可以查看cell对象及内部自由变量的内存地址
function.__closure__[0].cell_contents # 自由变量的值
function.__code__.co_freevars       # 自由变量名称
function.__code__.co_varnames       # 普通变量名称
# (4) 像count这类不可变类型，执行+=操作相当于再次赋值，这会隐式创建局部变量count
#     count不再是自由变量，则不能保存在函数闭包中
# (5) nonlocal声明可以把变量标记为自由变量，即使重新赋值依然是自由变量

# 3.5.8 Syntax-Decorator-带参数和不带参数共存的装饰器
def name(_func=None, *, kw1=val1, kw2=val2, ...):  
    def decorator(func):
        ...  # Create and return a wrapper function.

    if _func is None:
        return decorator                     
    else:
        return decorator(_func)    
        
# 3.5.9 Syntax-Decorator-录状态的类装饰器
# (1) __init__()方法相当于装饰器函数
# (2) __call__()方法相当于内部函数
import functools
class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.num_calls = 0
    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"Call {self.num_calls} of {self.func.__name__!r}")
        return self.func(*args, **kwargs)
@CountCalls
def say_whee():
    print("Whee!")

# 3.5.10 Syntax-Decorator-clock装饰器
import time
import functools
def clock(fmt = "[{elapsed:0.8f}s] {name}({arg_str}) -> {result}"):
    # (1) 装饰器工厂函数传递打印格式参数，并返回装饰器函数
    def decorate(func):
        # (2) 装饰器函数进行函数替换
        def clocked(*args, **kwargs):
            # (3) 内部函数添加新功能
            t0 = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - t0
            name = func.__name__
            arg_lst = []
            if args:
                arg_lst.append(', '.join(repr(arg) for arg in args))
            if kwargs:
                pairs = [f'{k}={w}' for k, w in sorted(kwargs.items())]
                arg_lst.append(', '.join(pairs))
            arg_str = ', '.join(arg_lst)
            print(fmt.format(**locals()))
            return result
        return clocked
    return decorate
    
# 3.5.11 Syntax-Decorator-装饰器实现单例模式
import functools
def singleton(cls):
    """Make a class a Singleton class (only one instance)"""
    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance
    wrapper_singleton.instance = None
    return wrapper_singleton
@singleton
class TheOne:
    pass
    
    
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

```python
#######################################################################
# 7. Libraries
#######################################################################

# 7.1 Libraries-Multiprocessing

# 7.1.0 Libraries-Multiprocessing-创建管理进程模块和同步子进程模块
# 创建管理进程模块
# (1) Process        （用于创建进程）
# (2) Pool           （用于创建管理进程池）
# (3) Queue          （用于进程通信，资源共享）
# (4) Value, Array   （用于进程通信，资源共享）
# (5) Pipe           （用于管道通信）
# (6) Manager        （用于资源共享）
# 同步子进程模块
# (1) Condition      （条件变量）
# (2) Event          （事件）
# (3) Lock           （互斥锁）
# (4) RLock          （可重入的互斥锁(同一个进程可以多次获得它，同时不会造成阻塞)
# (5) Semaphore      （信号量）

# 7.1.0.1 Libraries-Multiprocessing-Process
multiprocessing.Process(group=None, target=None, name=None, 
                        args=(), kwargs={}, *, daemon=None)
# (1) 参数介绍
#  1) group:    分组，仅用于兼容threading.Thread，值始终为None
#  2) target:   由run()方法调用的可调用对象，即子进程执行的任务，可传入方法名 
#  3) name:     为子进程设定名称，通过Process.name获取
#  4) args:     要传给target函数的位置参数，以元组方式进行传入。
#  5) kwargs:   要传给target函数的字典参数，以字典方式进行传入。
# (2) 实例方法
#  1) start():            启动子进程，并调用该子进程中的p.run()方法
#  2) run():              在子进程中调用target并传入args，可以重定义以代替target函数
#  3) is_alive():        返回进程是否在运行，仍然运行返回True
#  4) join([timeout]):  进程同步，阻塞至子进程完成或超时后执行后续代码，timeout是
#                       可选超时秒数，进程可被join多次，但不能join自身
#  5) terminate():        向子进程发送SIGTERM信号，无清理操作，其子进程变僵尸，锁不会释放
#  6) kill():            类似，发送SIGKILL信号
#  7) close():            关闭Process对象释放关联的所有资源，若子进程运行引发ValueError
# (3) 属性介绍
#  1) daemon:     默认False，True表示p为守护进程，随父进程终止而终止，且p不能创建新进程
#                 改参数必须在p.start()之前设置
#  2) name:       进程的名称
#  3) pid:        进程的pid
#  4) exitcode:   进程在运行时为None、如果为–N，表示被信号N结束(了解即可)
#  5) authkey:    进程间身份认证(对称加密),默认由os.urandom()生成(32),IPC安全

# 7.1.0.2 Libraries-Multiprocessing-pool.Pool
multiprocessing.pool.Pool([processes[, initializer[, initargs[, 
                           maxtasksperchild[, context]]]]])
# (1) 参数介绍
#  1) processes:    要创建的进程数，默认为os.cpu_count()返回数量
#  2) initializer:  默认None，否则每个工作进程启动时执行initializer(*initargs)
#  3) initargs:     传给initializer的参数组
#  4) maxtasksperchild:工作进程退出之前可以完成的任务数，到达后释放资源占用让新进程代替
#                   默认None，即进程寿命与Pool对象相同
#  5) context:      指定工作进程上下文
# (2) 实例方法
#  1) apply(func[, args[, kwargs]]): 在进程池中选1个工作进程执行func(args,*kwargs)
#                   因为返回结果前会阻塞，因此想用不同参数并发执行func，必须从不同线程调
#                   用p.apply()函数或使用p.apply_async()函数（极少用）
#  2) apply_async(func[, arg[, kwds={}[, callback=None]]]):进程池选1个工作进程异步
#                   执行func(args,*kwargs),返回AsyncResult类实例;callback是仅接受1
#                   个参数的可调用对象，必须非阻塞否则将阻塞其它异步结果接受，func成功返回
#                   时传递给callback，
#  3) map(func, iterable[, chunksize=None]):阻塞执行;逐个将iterable元素赋予func执行;
#                    chunksize指定每块的项数;将iterable分割为多块交给进程池;返回列表;
#  4) map_async(func, iterable[, chunksize=None]):异步执行，其余同上;
#  5) imap():        与map区别为，执行完1个立即返回1个可迭代对象，而非全部完成返回列表
#  6) imap_unordered(): 不保证返回的结果顺序与进程添加的顺序一致，其余同上
#  7) close():       阻止后续任务提交到进程池，当所有任务执行完成后，工作进程会exit()
#  8) terminate():  立即终止所有工作进程，不执行清理或结束挂起，Pool对象垃圾回收时自动执行
#  9) join():       等待所有工作进程退出。此方法只能在close()或teminate()之后调用
# (3) multiprocessing.pool.AsyncResult,方法apply_async()和map_async()的返回值
#  1) get([timeout]):    返回执行结果，远程调用发生异常，异常会在执行get()时重新抛出
#                        若timeout非None且超时则抛出multiprocessing.TimeoutError
#  2) wait([timeout]):   阻塞，直到返回结果，或者 timeout 秒后超时。
#  3) ready():           反回执行状态，完成返回True
#  4) successful():      若调用未完成或有异常, 则将引发 ValueError，否则返回True

# 7.1.0.3 Libraries-Multiprocessing-Queue
multiprocessing.Queue([maxsize])
# (0) 优缺点
#  1) Queue可以在多进程间传递数据
#  2) 只适用Process类，不能在Pool进程池中使用
# (1) 参数介绍
#  2) maxsize是队列中允许最大项数，省略则无大小限制。
# (2) 实例方法

#  1) put(obj[, block[, timeout]])：插入数据obj到队列;如果blocked为True（默认值）
#                        并且timeout为正值，阻塞至超时会抛出Queue.Full异常;
#                        如果blocked为False，Queue已满，会立即抛出Queue.Full异常
#  2) get([block[, timeout]])：从队列读取并且删除一个元素;如果blocked为True（默认值）
#                        并且timeout为正值，阻塞至超时会抛出Queue.Empty异常;
#                        如果blocked为False，Queue已空，会立即抛出Queue.Empty异常
#  3) get_nowait():        同q.get(False)
#  4) put_nowait():        同q.put(False)
#  5) empty():            调用此方法时q为空则返回True，该结果不可靠
#  6) full():            调用此方法时q已满则返回True，该结果不可靠
#  7) qsize():            返回队列中目前项目的正确数量，结果也不可靠

# 7.1.0.4 Libraries-Multiprocessing-Value，Array
# 在共享内存中创建ctypes()对象来共享数据
multiprocessing.Value(typecode_or_type, *args, lock=True)
# (1) 参数介绍
#  1) typecode_or_type:指明返回对象类型，可以是类型码(单字符)或C类型
#  2) args：透传给typecode_or_type这个类的构造函数作为参数
#  3) lock：默认True将创建互斥锁保护Value;传入Lock或RLock实例将用于同步;False则不保护
multiprocessing.Array(typecode_or_type, size_or_initializer, *, lock=True)
# (1) 参数介绍
#  1) typecode_or_type:指明返回对象类型，可以是类型码(单字符)或C类型
#  2) size_or_initializer:若为整数表示数组长度，元素初始化为0;否则是用于初始化数组的序列
#  3) *:传递给typecode_or_type构造函数的参数
#  4) lock：默认True将创建互斥锁保护Value;传入Lock或RLock实例将用于同步;False则不保护
# | Type code | C Type             | Python Type       | bytes |
# | --------- | ------------------ | ----------------- | ------|
# | `'b'`     | signed char        | int               | 1     |
# | `'B'`     | unsigned char      | int               | 1     |
# | `'u'`     | Py_UNICODE         | Unicode character | 2     |
# | `'h'`     | signed short       | int               | 2     |
# | `'H'`     | unsigned short     | int               | 2     |
# | `'i'`     | signed int         | int               | 2     |
# | `'I'`     | unsigned int       | int               | 2     |
# | `'l'`     | signed long        | int               | 4     |
# | `'L'`     | unsigned long      | int               | 4     |
# | `'q'`     | signed long long   | int               | 8     |
# | `'Q'`     | unsigned long long | int               | 8     |
# | `'f'`     | float              | float             | 4     |
# | `'d'`     | double             | float             | 8     |

# 7.1.0.5 Libraries-Multiprocessing-Pipe
# 返回一对 Connection`对象  ``(conn1, conn2)` ， 分别表示管道的两端。
multiprocessing.Pipe([duplex])
# (1) 参数介绍
# dumplex:默认全双工，duplex为False则conn1只能用于接收conn2只能用于发送
# (2) 实例方法
#  1) send(obj):    通过pipe发送对象
#  2) recv():       接收另一端发送的对象;无消息则阻塞;另一端关闭则抛出EOFError
#  3) close():      关闭连接;被垃圾回收将自动调用此方法
#  4) fileno():     返回连接使用的整数文件描述符
#  5) poll([timeout]):有数据则返回True;忽略timeout将立刻返回结果,None则一直阻塞
#  6) recv_bytes([maxlength]):接受字节信息;长度超maxlength引发IOError;
#                   另一端关闭则返回EOFError异常
#  7) send_bytes(buffer [, offset [, size]]):发送字节信息;buffer支持缓冲区
#                    接口任意对象;offset缓冲区中字节偏移量;size要发送字节数
#  8) recv_bytes_into(buffer [, offset]):接收一条完整字节消息，并保存在buffer
#                    (持缓冲区接口的)对象中;返回值是收到的字节数;消息长度大于可用
#                     的缓冲区空间，将引发BufferTooShort异常

# 7.1.0.6 Libraries-Multiprocessing-Manager、BaseManager
multiprocessing.Manager()
# (1) Manager()返回manager对象, 控制一个独立的server子进程,进程包含的python对象
# (2) 子进程以服务器形式运行，可被其他的进程通过代理访问共享对象，代理作为客户端运行
# (3) Manager()是BaseManager的子类，返回启动的SyncManager()实例
# (4) SyncManager()实例可用于创建共享对象并返回访问这些共享对象的代理
# (5) Manager模块常与Pool模块一起使用
# (6) Manager支持的类型有
# list, dict, Namespace, 
# Lock, RLock, Semaphore, BoundedSemaphore, Condition,
# Event, Queue, Value, Array

multiprocessing.managers.BaseManager([address[, authkey]])
# 创建管理器服务器的基类
# (1) 参数介绍
#  1) address:(hostname,port);服务进程监听的地址;None允许任意主机的请求建立连接
#  2) authkey:连接服务器的客户端身份验证，默认current_process().authkey的值
# (2) 实例方法：
#  1) start([initializer[, initargs]]):启动单独子进程,并在其中启动管理器服务器
#                    若initializer不是None，则子进程启动前执行该函数
#  2) get_server(): 返回Server对象，是管理器在后台控制的真实的服务
#  3) connect():    将本地管理器对象连接到一个远程管理器进程:
#  4) shutdown():   停止管理器进程，只能在start()方法之后调用;它可以被多次调用
# (3) 实例属性：
#  1) address：只读属性，管理器所用的地址

# 7.1.0.7 Libraries-Multiprocessing-Lock
multiprocessing.Lock()
# Lock是一个工厂函数,返回默认上下文初始化的multiprocessing.synchronize.Lock对象
# 一个进程/线程acquire锁，任何其他进程/线程的acquire请求都会被阻塞直到锁被释放
# (1) 参数介绍
# (2) 实例方法：
#  1) acquire([timeout]): 使线程进入同步阻塞状态，尝试获得锁定。
#  2) release(): 释放锁;使用前线程必须已获得锁定，否则将抛出异常。
lock = multiprocessing.Lock()
lock.acquire()
try:
    # do something
finally:
    lock.release()
with lock:
    # do something

# 7.1.0.8 Libraries-Multiprocessing-RLock
multiprocessing.RLock
# 可重入锁可以被同一线程请求多次acquire(),释放锁时需要调用release()相同次数
# (1) 参数介绍
# (2) 实例方法：
#  1) acquire([timeout])：同Lock
# 2) release(): 同Lock

# 7.1.0.9 Libraries-Multiprocessing-Semaphore
multiprocessing.Semaphore([value])
信号量有一个计数器,当占用信号量的线程数超过信号量时线程阻塞
构造方法:Semaphore([value])
# (1) 参数介绍
#  1) value：设定信号量，默认值为1
# (2) 实例方法：
#  1) acquire([timeout])：同Lock
#  2) release(): 同Lock

# 7.1.0.10 Libraries-Multiprocessing-Condition 条件变量
multiprocessing.Condition([lock])
# Condition在内部维护一个锁对象（默认是RLock）,提供除锁外的其他方法
# (1) 参数介绍:
#  1) lock:可以传递一个Lock/RLock实例给构造方法，否则它将自己生成一个RLock实例。
# (2) 实例方法：
#  1) acquire([timeout]):获取底层锁,无法获取则wait
#  2) release():释放锁
# wait([timeout]):线程进入Condition的等待池等待notify并释放锁
#                 wait状态的线程接到通知后会重新判断条件
# notify():       从等待池挑选一个线程并通知，被通知线程调用acquire()尝试获得锁定
#                 其他线程仍然在等待池中，使用前必须获得锁
# notifyAll():    通知等待池中所有的线程，这些线程都将进入锁定池尝试获得锁定
#                  使用前必须获得锁

# 7.1.1 Libraries-Multiprocessing-上下文和启动方法
# (1) spawn:父进程启动新解释器，子进程仅继承run()所需资源,慢,Unix/Win(默认)
# (2) fork: 父进用os.fork()开启解释器分支,父子进程初相同,进程不安全,Unix(默认)
# (3) forkserver:父进程请求服务器fork,服务器单线程故安全,仅fork所需资源，Unix
# (4) 不兼容:fork上下文创建的锁不能传递给spawn或forkserver启动方法启动的进程

import multiprocessing as mp
def foo(q):
    q.put('hello')
if __name__ == '__main__':
    mp.set_start_method('spawn')    # 不应该被多次调用
 ## ctx = mp.get_context('spawn')   # 同一程序中使用多种启动方法
    q = mp.Queue()                  # 队列是线程和进程安全的
 ## q = ctx.Queue()
    p = mp.Process(target=foo, args=(q,))
 ## p = ctx.Process(target=foo, args=(q,))
    p.start()
    print(q.get())
    p.join()

# 7.1.2 Libraries-Multiprocessing-在进程之间交换对象
# (1) 队列(队列是线程和进程安全的)
from multiprocessing import Process, Queue
def f(q):
    q.put([42, None, 'hello'])
if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print(q.get())    # prints "[42, None, 'hello']"
    p.join()
# (2) 管道
#     1) Pipe()返回管道的两端(连接对象)，两端均有send()和recv()方法，默认双工
#     2) 若两进程（或线程）同时读或写管道同一端，管道中数据可能损坏
from multiprocessing import Process, Pipe
def f(conn):
    conn.send([42, None, 'hello'])
    conn.close()
if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    p.join()


# 7.1.3 Libraries-Multiprocessing-进程间同步
from multiprocessing import Process, Lock
def f(l, i):
    l.acquire()                    # 加锁
    try:
        print('hello world', i)    # 确保只有一个进程打印输出
    finally:
        l.release()                # 释放
if __name__ == '__main__':
    lock = Lock()
    for num in range(10):
        Process(target=f, args=(lock, num)).start()

# 7.1.4 Libraries-Multiprocessing-进程间共享状态
# (1) 共享内存（尽量避免）
#     1) 参数'd'和'i'是array模块使用类型的typecode: 'd'双精度浮点数'i'有符号整数
#     2) multiprocessing.sharedctypes可分配任意ctypes对象，更灵活
#     3) alue或Array是进程和线程安全的
from multiprocessing import Process, Value, Array
def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]
if __name__ == '__main__':
    num = Value('d', 0.0)        # Value或Array将数据存储在共享内存映射中
    arr = Array('i', range(10))    
    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()
    print(num.value)
    print(arr[:])
# (2) 服务进程
# Manager()返回管理器对象控制的服务进程,该进程保存Python对象并允许其他进程用代理操作
# Manager()返回的管理器支持类型：list、dict、Namespace、Lock、RLock、Semaphore
#                            、BoundedSemaphore、Condition、Event、Barrier
#                            、Queue、Value和Array 
from multiprocessing import Process, Manager
def f(d, l):
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.reverse()
if __name__ == '__main__':
    with Manager() as manager:
        d = manager.dict()
        l = manager.list(range(10))
        p = Process(target=f, args=(d, l))
        p.start()
        p.join()
        print(d)
        print(l)

# 7.1.5 Libraries-Multiprocessing-工作进程池
# 进程池的方法只能由创建它的进程使用
from multiprocessing import Pool, TimeoutError
import time
import os
def f(x):
    return x*x
if __name__ == '__main__':
    # 开启4个工作进程
    with Pool(processes=4) as pool:
        # print "[0, 1, 4,..., 81]"
        print(pool.map(f, range(10)))       
        # 随机顺序打印上述数字
        for i in pool.imap_unordered(f, range(10)): 
            print(i)
        # 单个进程异步执行"f(20)"
        res = pool.apply_async(f, (20,))  # 仅开启一个进程执行
        print(res.get(timeout=1))         # 打印"400"
        # 可能有多个进程异步执行
        multiple_results = [pool.apply_async(os.getpid, ()) for i in range(4)]
        print([res.get(timeout=1) for res in multiple_results])
        # 超时报错
        res = pool.apply_async(time.sleep, (10,))
        try:
            print(res.get(timeout=1))
        except TimeoutError:
            print("We lacked patience and got a multiprocessing.TimeoutError")
        print("For the moment, the pool remains available for more work")
    # pool对象声明周期结束
    print("Now the pool is closed and no longer available")


# 7.1.6 Libraries-Multiprocessing-Process和异常API
multiprocessing.Process(group=None, \  # 仅兼容threading,应始终是None
                        target=None, \ # run()方法调用的可调用对象
                        name=None, \   # 是进程名称
                        args=(), \     # 目标调用的位置参数元组
                        kwargs={}, \   # 关键字参数字典
                        *, daemon=None)
run() # 仅在子进程中执行,该方法只会调用target指向的函数,可被重载代替target
```
