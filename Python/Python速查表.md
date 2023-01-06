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

# 3.1.1 Syntax-Arguments-Scope
# (1) 外围模块是全局作用域,相对当前模块导入模块的变量变成导入模块的属性
# (2) 全局作用域的作用范围仅限于单个文件
# (3) 赋值的变量名除非被声明为global或nonlocal,否则均为局部变量
#     global修改或创建全局变量;nonlocal修改但不能创建外层
# (4) 函数未定义的变量名被假定为外层函数的局部变量、全局变量或内置变量
# (5) 函数的每次调用都会创建一个新的局部作用域,函数间的局部变量相互独立

# 3.4 Class
# 3.4.1 __repr__和__str__
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

# 3.4.2 @staticmethod和@classmethod
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

# 3.4.3 构造函数重载（拦截内置的构造函数操作，并调用自定义方法，__init__是一个入口）
class <name>:
    def __init__(self, a=None):
        self.a = a
    def __new__(cls):
      return super().__new__(cls)
# (1) 实例创建过程中__new__方法先被调用,创建并返回新实例对象,后传入__init__初始化
# (2) 类实例化前先调用__new__方法创建实例，是类方法
# (3) 实例对象创建后调用__init__方法初始化实例,是实例对象的方法,设置实例对象的初始值

# 3.4.4 继承及类接口技术
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


# 3.4.5 多重继承
class A: pass
class B: pass
class C(A, B): pass
# MRO决定命名空间树的搜索顺序
>>> C.mro()
[<class 'C'>, <class 'A'>, <class 'B'>, <class 'object'>]

# 3.4.6 @property @name.setter @name.deleter
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

# 3.4.7 Dataclass（自动生成init()、repr()和eq()）
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

# 3.4.8 Slots
# 需要将属性字符串顺序赋值给__slot__属性，
# 仅__slot__列表内的名称可赋值为实例属性，可以不赋值但不赋值不能被使用
# 显著减少内存占用，优化速度，但与Python的灵活性相背离
class MyClassWithSlots:
    __slots__ = ['a']
    def __init__(self):
        self.a = 1

# 3.4.9 Copy
from copy import copy, deepcopy
# 赋值操作并不clone对象，仅创建引用并绑定到原对象，原对象的一切改变都将反映到赋值对象上
# copy操作clone第一层引用对象
# deepcopy操作递归clone对象
<object> = copy(<object>)
<object> = deepcopy(<object>)
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
