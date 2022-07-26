# Python基础语法学习笔记

### 序列运算

序列：包括列表、字符串、元组、字节、字节组

#### 1.序列运算（列表、字符串、元组、字节、字节组）

| 运算                                                  | 描述                               | 类方法                                                    |
| --------------------------------------------------- | -------------------------------- | ------------------------------------------------------ |
| X in S,<br>X not in S                               | 成员测试                             | \_\_container\_\_,<br>\_\_iter\_\_,<br>\_\_getitem\_\_ |
| S1+S2                                               | 级联                               | _\_add_\_                                              |
| S*N, N*S                                            | 重复                               | _\_mul_\_                                              |
| S[i]                                                | 偏移量索引                            | _\_getitem_\_                                          |
| S[i:j],<br>S[i\:j\:k]                               | 分片：S中的项目按照选定<br>的步幅k， 从偏距i到偏距j-1 | _\_getitem_\_                                          |
| len(S)                                              | 长度                               | len                                                    |
| min(S), max(S)                                      | 最小，最大项                           | iter, getitem                                          |
| iter(S)                                             | 迭代协议                             | iter                                                   |
| for X in S:,<br>[expr for x in S],<br> map(func,S)等 | 迭代（全部范围）                         | iter, getitem                                          |

#### 2.易变序列运算（列表、字节组）

| 运算                            | 描述                                        | 类方法            |
| ----------------------------- | ----------------------------------------- | -------------- |
| S[i]=X                        | 索引赋值：按给定偏移量修改要引用的项目X                      | \_\_setitem_\_ |
| S[i:j]=I,<br>S[i\:j\:k]=I     | 分片赋值：按选定的步幅k（可能为空）用<br>可迭代I中的全部项从i到i-1替换S | \_\_setitem_\_ |
| del s[i]                      | 索引删除                                      | _\_delitem_\_  |
| del S[i:j],<br>del S[i\:j\:k] | 分片删除                                      | _\_delitem_\_  |

#### 3.映射运算（字典）

![](D:\Cache\MarkText\2022-07-20-18-39-17-image.png)

#### 4.数值运算

![](D:\Cache\MarkText\2022-07-20-18-39-48-image.png)

#### 5.序列运算说明

（1）**索引**

（2）**分片**

（3）**扩展分片**

（4）**分片赋值**

            ①类似先删除再插入

（5）其他

            ①级联、重复和分片返回新对象

### 特殊内建类型

#### 1.number

（1）**整数**

（2）**浮点数**

（3）整数的**八进制**（0o7）、**十六进制**（0xff）、**二进制**（0b11）

（4）**复数**（3+4j）

（5）基于模块的类型：**小数**（decimal.Decimal('1.33')）、**分数**（fractions.Fraction(4,3)）

#### 2.字符串

        通常的str字符串对象是一个**不变**的**可由offset（位置）访问**的字符序列。其**字符是指向基础字符集中序数的代码**，单个字符是长度为1的字符串对象。

        Python 3.X有字符串、字节和字节组三种带有相似接口的字符串类型：

        ①**str**                ：一个字符不易变序列，用于所有文本一ASCII和更丰富的Unicode。
        ②**bytes**           ：一个不易变短整型序列，用于二进制数据的字节值。
        ③**bytearray**    ：字节的易变变量。

（1）文字生成

        ① 单引号和双引号功能相同，每种引号都可以嵌入其他种类的非转义引号。

```python
'Python"s',"Python's"
```

        ②三重引号块将带有行结束标记(\\n)的多行文本聚合成单个字符串。

```python
"""This is a multiline block"""
```

        ③邻接字符串常量被连接起来，如果带有括号则可以横跨多行。

```python
"This" "is" "concatenated"
```

        ④原始字符串：反斜杠在文字中被保留（除字符串末端），用于正则表达式和DOS。

```python
r'a raw\string', R'another\one'
```

        ⑤Python3.X中字节字符串文字：8位字节值序列表示原二进制数据。

```python
b'...'
```

        ⑥字节组字符串结构：可改变的字节变量。

```python
bytearray(...)
```

        ⑦Python3.X中字节字符串文字：8位字节值序列表示原二进制数据。

```python
b'...'
```

        ⑧Python2.X中Unicode字符串文字：Unicode码点序列。

```python
u'...'
```

        ⑨由整形创建不同进制字符串，用Python3.X中可能的Unicode:编码/解码将对象创建为字符串。

```python
hex(), oct(), bin()            #由整形创建不同进制字符串
str(), bytes(), bytearray()    #将对象创建为字符串
```

        转义字符

<img title="" src="file:///D:/Cache/MarkText/2022-07-21-09-48-29-image.png" alt="" data-align="center" width="423">

（2）字符串格式化

        规范的str字符串支持两种不同风格的字符串格式化：

            ·带有%运算符代码的原始表达式(所有Python版本)：fmt%（值）。
            ·用调用语句编码的更新的方法(3.0,2.6及以后版本)：fmt.format（值）。

        ①字符串格式化表达式及语法

                (i)   一个以上的值要替换，%右侧用元组

                (ii)  一个值要替换，%右侧用单值或元组

                (iii) 左侧存在键名，右侧要用字典

                (iv) 可以用*动态传递宽度和精度

> ```python
> 'The knights who say %s!'%'Ni'
> '%d %s, %d you' % (1,'spam',4.0)
> '%(n)d named %(x)s' % {'n':1,'x':"spam"}
> '%(n).0E=>[%(x)-6s]' % dict(n=100,x='spam')
> ```

                语法：%[(keyname)][flags][width][.prec]typecode

        keyname（键名）在圆括号中，引用期望字典中的一项。
        flags（标志）可以是-（左对齐）、+（数值符号）、空格(在正数前加空白，负数前加-)和0（零填充）。

        width（宽度）整个最小域宽度(使用*从值中提取)。
        prec（精度）给定包括在。后面的数字个数（即精度）(使用*从值中提取)。
        typecode（类型码）表8中的一个字符。

                                            **字符串格式化类型代码**

<img title="" src="file:///D:/Cache/MarkText/2022-07-21-10-00-24-image.png" alt="" data-align="center" width="471">

        ②字符串格式化方法

        （3）**模板字符串置换**

<img title="" src="file:///D:/Cache/MarkText/2022-07-21-10-16-18-image.png" alt="" width="309" data-align="center">

        （4）str、bytes、bytearray的区别：

                    ①str是已解码的文本，可能被解码为字节

                    ②bytes、bytearray是原始字节，可能被解码为str

                    ③bytes、bytearray不支持字符串格式化

                    ④bytearray和list类似

        （5）搜索方法

| 函数             | 作用  |
| -------------- | --- |
| S.find()       |     |
| S.rfind()      |     |
| S.index()      |     |
| S.rindex()     |     |
| S.count()      |     |
| S.startswith() |     |
| S.endswith()   |     |

        （6）分解与连接方法

| 函数             | 作用  |
| -------------- | --- |
| S.split()      |     |
| S.join()       |     |
| S.replace()    |     |
| S.splitlines() |     |

        （7）格式化方法

| 函数             | 作用  |
| -------------- | --- |
| S.format()     |     |
| S.capitalize() |     |
| S.expandtabs() |     |
| S.strip()      |     |
| S.lstrip()     |     |
| S.rstrip()     |     |
| S.swapcase()   |     |
| S.upper()      |     |
| S.lower()      |     |
|                |     |
|                |     |
|                |     |
|                |     |
|                |     |
|                |     |
|                |     |

        （8）内容检测方法

| 函数      | 作用  |
| ------- | --- |
| S.is*() |     |

#### 3.Unicode字符串

        （1）字符串的编码与解码

<img title="" src="file:///D:/Cache/MarkText/2022-07-21-11-07-26-image.png" alt="" data-align="center" width="185">

<img title="" src="file:///D:/Cache/MarkText/2022-07-21-11-07-42-image.png" alt="" data-align="center" width="251">

        （2）字节和字节组字符串

                ①bytes

<img title="" src="file:///D:/Cache/MarkText/2022-07-21-11-09-55-image.png" alt="" data-align="center" width="231">

<img title="" src="file:///D:/Cache/MarkText/2022-07-21-11-11-16-image.png" alt="" data-align="center" width="233">

                ②bytearray

#### 4.列表

        Lists(（列表）是由offset（位置）访问的对象引用易变序列。

        （1）内容创建

<img title="" src="file:///D:/Cache/MarkText/2022-07-21-11-15-46-image.png" alt="" data-align="center" width="340">

        （2）运算（专用方法）

| 方法                              | 作用                                                                              |
|:------------------------------- | ------------------------------------------------------------------------------- |
| L.append(X)                     |                                                                                 |
| L.extend(I)                     | 就地在L末尾插入可迭代对象I中每一项<br>类似L[len(L):]=I                                            |
| L.sort(key=None, reverse=False) | 将L就地排序，默认为升序<br>key指定单变量的比较函数<br>                                               |
| L.reverse()                     |                                                                                 |
| L.index( X [, i [, j] )         | 返回L中X对象第一次出现的索引值<br>如果没找到，则发送一个异常                                               |
| L.insert(i,X)                   | 在偏移位i将单个对象插入到L中<br>类似L[i:i]=[X],i可正负                                            |
| L.count(X)                      | 返回L中X出现的次数。                                                                     |
| L.remove(X)                     | 从L中删除第一次出现的X对象<br>如果没有找到对象发送一个异常<br>作用与del L[L.index(X)]相同                      |
| L.pop([i])                      | 删除并返回L中的最后(或偏移量为i)一项<br>与append（）一起用于实现栈(stack)<br>作用等同于x=l[i]、delL[i]和return x |
| L.clear()                       | 从L中删除所有项。                                                                       |
| L.copy()                        | 构建一个L的顶层（表层）拷贝。                                                                 |

        （3）列表综合表达式

<img title="" src="file:///D:/Cache/MarkText/2022-07-21-11-34-21-image.png" alt="" data-align="center" width="359">

<img title="" src="file:///D:/Cache/MarkText/2022-07-21-11-34-50-image.png" alt="" data-align="center" width="316">

        （4）迭代协议

                ①迭代范围运行在一个迭代对象上，这个对象带有一个ter（）方法。
                ②当被调用时，这个迭代的iter（）方法返回一个iterator（迭代器）一一个带有_next_（）方法的对象（可能是同一个对象）。
                ③当被调用时，迭代器的next（）方法返回迭代中的下一项或发送一个StopIteration异常结束该迭代。

                ④内建函数iter(X)调用一个X.iter（）迭代方法

                ⑤内建函数next(I)调用一个I.next_（）迭代方法

        （5）生成器表达式

                ①生成器表达式是在圆括号而不是方括号中编码的综合

<img title="" src="file:///D:/Cache/MarkText/2022-07-21-11-43-01-image.png" alt="" data-align="center" width="383">

<img title="" src="file:///D:/Cache/MarkText/2022-07-21-11-43-14-image.png" alt="" data-align="center" width="222">

        （6）其他

<img title="" src="file:///D:/Cache/MarkText/2022-07-21-11-43-48-image.png" alt="" data-align="center" width="398">

#### 5.字典

        字典是由键(key)（不是位置）访问的对象引用的易变映射，是未排序的表。

        这些表是将键映射到值的，内部实现的动态可扩展的散列(hash)表。

        （1）内容与创建

```python
a = {}
# 一个空字典（不是一个集合）。
{"eg8s":3,"spam":2}
# 一个两项目的字典：键'spam'和'egs',值2和3.
D={'info':{42:1,type():2},'spam':[]}
# 嵌套字典：D['info'][42]提取1.
D=dict(name='Bob',age=45,job=('mgr','dev'))
# 通过将关键词变量传给类型构造器创建字典。
D=dict(zip('abc',[1,2,3]))
# 通过将key/value元组对传给类型构造器创建字典。
D=dict([['a',1],['b',2],['c',3]])
# 与上一行作用相同：接收键和值的任意可迭代对象。
D={c.upper():ord(c) for c in 'spam'}
# 字典综合表达式(在Python3.X和2.7中)，所有语法见“列表综合表达式”。
```

        （2）运算

| 方法                          | 作用                                                                                 |
|:--------------------------- | ---------------------------------------------------------------------------------- |
| D.keys()                    | D中所有的键                                                                             |
| D.values()                  | D中所有排序的值                                                                           |
| D.items()                   | 元组对(key,value),每个对都对应D中的一个项目。                                                      |
| D.clear()                   | 从D中删除所有项目。                                                                         |
| D.copy()                    | 返回D的一个表层（顶层）拷贝。                                                                    |
| D.update(D2)                | 原地将D2中所有项并入D中，<br>与(k,v) in D2.items() : D[k]=v类似。                                 |
| D.get( K [, default] )      | 类似D[K],但返回默认值(或None,如果没有默认值)                                                       |
| D.setdefault(K [, default]) | 与D.get(K,default)相同<br>但如果D中没有K也要将默认值赋予键K。                                         |
| D.popitem(K [, default])    | 删除并返回一个任意元组对(key,value)。                                                           |
| D.pop(K)                    | 如果K在D中，则该方法返回D[K]并删除K<br>否则，返回一个默认值（如果存在），<br>或发送一个KeyError异常（如果没有默认值）             |
| dict.fromkeys( I [, value]) | 该方法创建一个新字典，字典的键值来自迭代I<br>并将每个集合的值设置为value(默认为None)。                                |
| K in D                      | 如果键K不在D中，则返回True,否则返回False<br>在Python3.X中换成了has_key（）。                             |
| for K in D                  | 在D中的键K上进行迭代（所有迭代范围）。<br>字典支持直接迭代：for K in D的作用与for K in D.keys（）相类似以。前者使用字典对象的迭代器。 |

#### 6.元组

        元组是由偏移量（位置）访问的不易变对象引用序列。

        （1）内容与创建

```python
()
# 一个空元组。
(0,)
# 一个单项元组（不是一个简单表达式）。
(0,1,2,3)
# 一个四项元组。
0,1,2,3
# 另外一个四项元组（与前者相同）；
# 当逗号或圆括号为其他意思时无效（如，函数参数)。
T = ('spam',(42,'eggs'))
# 嵌套元组：T[1][1]提取'eggs'。
T = tuple('spam')
# 由调用类型构造器函数创建一个含有任意迭代中所有项的元组。
```

        （2）专用运算

| 方法                      | 作用                                    |
|:----------------------- | ------------------------------------- |
| T.index( X [, i [, j] ) | 返回元组T中对象第一次出现时的索引值；<br>如果没找到，则发送一个异常。 |
| T.count(X)              | 返回元组T中出现的次数。                          |

#### 7.文件

        （1）输入文件

| 方法                           | 作用                                      |
|:---------------------------- | --------------------------------------- |
| infile = open(filename, 'r') | 创建输入文件，连接到命名的外部文件上。                     |
| infile.read()                | D中所有排序的值                                |
| infile.read(N)               | 读取最多W字节(1个或多个)；文件末端为空。                  |
| infile.readline()            | 读取下一行（直到行结束标记）；文件末端为空。                  |
| infile.readlines()           | 将整个文件读入一个行字符串列表。                        |
| for line in infile           | 使用文件对象infile的Iine（行）迭代器，<br>自动步移到文件的所有行 |

        （2）输出文件

| 方法                            | 作用                                                                         |
|:----------------------------- | -------------------------------------------------------------------------- |
| outfile = open(filename, 'w') | 创建输出文件对象，连接到外部文件上。                                                         |
| outfile.write(S)              | 不带格式将字符串S的全部内容写入文件。<br>在文本模式下，'\n'转化为默认的专有平台换行标记。<br>在二进制模式下，字符串可以包含非打印字节。 |
| outfile.writelines(I)         | 将迭代对象I中的所有字符串写入文件，<br>不自动添加任何换行结束符。                                        |

        （3）任何文件

| 方法                           | 作用                              |
|:---------------------------- | ------------------------------- |
| file.close()                 | 手动关闭游离资源                        |
| file.tell()                  | 返回文件的当前位置。                      |
| file.seek(offset [, whence]) | 为了进行随机访问，将当前文件的位置设置为offset。     |
| file.isatty()                | 如果文件被连接到了一个类tty（交互式的）设备上，返回True |
| file.flush()                 | 释放文件的stdio缓冲器                   |
| file.truncate([size])        | 将文件截取为至多size字节                  |
| file.fileno()                | 获取文件的文件号（文件描述符整数）。              |

        （4）其他文件属性

| 方法          | 作用                       |
|:----------- | ------------------------ |
| file.closed | 如果文件已被关闭，则返回True         |
| file.mode   | 传给函数open（）的模式字符串(如，'r')。 |
| file.name   | 对应于外部文件的字符串名。            |

        （5）文件环境管理器

        当文件被回收后如果仍然是打开的，文件对象通常自行关闭。

        如：open('name').read（）

```python
with open(r'C:\misc\script','w') as myfile:
... use myfile ...
```

#### 8.集合

        集合(set)是unique和immutable对象的易变（可改变的）和无序聚集。

        集合支持并和交之类的数学集合运算。

        集合是非顺序（未排序）和非映射（不将值与键映射）的。

（1）内容与创建

```python
set()
# 一个空集合({}是一个空字典)。
S = set('spam')
# 一个四个项目的集合：值为's','p','a','m（接受任何迭代）。
S = {'s','p','a','m'}
#一个四个项目的集合，与上面一条相同(用于Python3.X和2.7版)。
S = {ord(c)for c in 'spam'}
#集合综合表达式(用于Python3.X和2.7版)。
S = frozenset(range(-5,5))
#一个冻结（不易变）的含有-5~4的10个整型数的集合。
```

（2）运算

| 方法                                         | 作用  |
|:------------------------------------------ | --- |
| x in S                                     |     |
| S1 - S2, <br>S1.difference(other)          |     |
| S1 \| S2,<br>S1.union(other)               |     |
| S1 & S2,<br>S1.intersection(other)         |     |
| S1 <= S2,<br>S1.issubset(other)            |     |
| S1 <= S2,<br>S1.isupperset(other)          |     |
| S1 < S2,<br>S1 > S2                        |     |
| S1 ^ S2,<br>S1.symmetric_difference(other) |     |
|                                            |     |
|                                            |     |
|                                            |     |
|                                            |     |
|                                            |     |

#### 9.其他

        （1）序列转换器

<img title="" src="file:///D:/Cache/MarkText/2022-07-21-14-59-51-image.png" alt="" data-align="center" width="473">

        （2）字符串/对象转换器

![](D:\Cache\MarkText\2022-07-21-15-00-33-image.png)

### 语句和语法

#### 1.语法规则

（1）控制流

（2）块

（3）语句

（4）注释

（5）文档字符串

（6）空白

#### 2.命名规则

### 专用语句

#### 1.赋值语句

```python
target = expression                                # 基本赋值语句
target1 = target2 = expression                     # 多目标赋值语句
target1, target2 = expression1, expression2        # 元组赋值格式
target1 += expression                              # 增量赋值

target1, target2, ... = same-length-iterable       # 正则序列复制
(target1, target2, ...) = same-length-iterable
[target1, target2, ...] = same-length-iterable
target1,*target2,... = matching-length-iterable    # 扩展序列赋值
```

#### 2.Expression语句

        任何表达式可以以语句形式出现(在单独一行)，但语句不能出现在任何其他表达式中。

        （1）任意参数调用方法（实参前面的*和**：拆包）：

                专用星号语法也可用于在函数和方法中调用参数列表，将集合分成多个独立的参数

                这个语法是专门为与函数标头的随机参数语法相对称而设计的

                单个表示将元组拆成一个个单独的实参 

                两个则表示将字典拆成一个个单独的带变量名的实参。

<img title="" src="file:///D:/Cache/MarkText/2022-07-21-17-30-49-image.png" alt="" data-align="center" width="317">

#### 3.Print语句

```python
print([value [value]*]
      [sep=str][end=str]
      [file=object][flush=bool])

# sep    ：放在值之间的一个字符串(默认为空格：··)。
# end    ：放置在打印文本末端的字符串(默认值是换行符：\')。
# file   ：文本被写成的类文件对象(默认值为标准输出：sys.stdout)
# flush  ：用于强制输出流开启关闭而传递的true/false(Python3.3开始，默认值False)。

>> print(2 *32,'spam')
   4294967296spam
>> print(2 *32,'spam',sep='')
   4294967296spam
>> print(2 *32,'spam',end='');print(1,2,3)
   4294967296spam123
>> print(2 *32,'spam',sep='',file-open('out', 'w')
>> open('out').read()
   '4294967296spam\n'


#print(X)的等价操作
import sys
sys.stdout.write(str(X)+'\n')
```

#### 4.if语句

```python
if test:
    suite
[elif test:
    suite]*
[else:
suite]
```

#### 5.while语句

```python
while test:
    suite
[else:
    suite]
```

        当顶部测试的结果为真时保持运行第一组语句的一般循环。

        如果循环没有运行到第一组语句中的break语句时就终止而退出了，就运行else语句组。

#### 6.for语句

```python
for target in iterable:
    suite
[else:
    suite]
```

        target可以是显示在赋值语句=左侧的任何对象（例如，tuplelist中的（x,y)）。

#### 7.pass语句

        占位符语句，在语法需要时使用。

#### 8.break语句

        立即退出最靠近的（最里面的）封闭while循环语句或for循环语句

        提示：可以用raise和try语句退出多层循环。

#### 9.continue语句

        这个语句立即跳到最靠近的封闭while循环语句或1oop循环语句的顶部；

#### 10.del语句

```python
del name
del name[i]
del name[i:j:k]
del name.attribute
```

        de1语句删除变量、项目、键、分片和属性。

        这个语句主要用于数据结构，而不是内存管理。

        它删除被引用对象的索引，归零则会被作为废物收集（回收），但这一过程自动进行。

#### 11.def语句

        （1）函数定义中的参数格式

<img title="" src="file:///D:/Cache/MarkText/2022-07-21-18-56-10-image.png" alt="" data-align="center" width="473">

        （2）函数调用时的参数格式

<img title="" src="file:///D:/Cache/MarkText/2022-07-21-18-56-35-image.png" alt="" data-align="center" width="501">

        （3）Python3.X 中 仅为关键词的参数

```python
>>> def f(a, *b, c):print(a,b,c)          #需要kWC
>>> f(1,2,c=3)
1(2,)3
>>> def f(a, *, c=None):print(a,c)        #可选的kwC
>>> f(1)
1 None
>>> f(1,c='spam')
1 spam
```

        （4）Python3.X 中 的函数注释

<img title="" src="file:///D:/Cache/MarkText/2022-07-21-19-02-44-image.png" alt="" data-align="center" width="370">

        （5）lambda表达式

```python
lambda arg,arg,...:expression

>>L=lambda a,b=2,*c,**d:[a,b,c,d]
>>>L(1,2,3,4,X=1,y=2)
[1,2,(3,4),{'y':2,x':1}]
```

        因为lambda是一个表达式，不是一条语句，因此它可以用在def不能定义的地方

        （6）函数默认值与属性

        易变的默认参数值在def语句中每次都要计算，不是在每次调用时计算，因此在调用之间可以保持状态。。

```python
>>> def grow(a, b=[]):        #定义grow(a,b=None):
        b.append(a)           # if b =None:b =[
        print(b)
>>> grow(1);grow(2)
[1]
[1,2]
```

        （7）函数和方法装饰器

                    见末尾

#### 12.return语句

        return语句退出封闭的函数，并返回一个expression（表达式）

        如果忽略expressionis,其默认值为None

对于多值函数的结果返回一个元组。

#### 13.yield语句（存疑）

        yield表达式定义一个生成器函数，按需要产生结果。

        yie1d将函数状态挂起，并返回一个expression（表达式）值。

        下一个迭代中，函数先前的位置和变量状态被恢复，并在yield语句之后立即控制恢复。

        使用return语句结束该迭代或直接离开函数的结尾。

```python
def generateSquares(N):
    for i in range(N):
    yield i *2
>>> G = generateSquares(5)   #含有 init,_next_
>>> 1ist(G)                  #现在生成结果
[0,1,4,9,16]

a. 不接受输入值或者输入值是None
        yield 1
b. 接受输入值
        s = yield 1
c. 接受输入，但不返回数据，这样默认返回None
        s = yield
d.既不接受输入，也不返回值，默认返回None
        yield
第一种：当函数调用到yield时，返回yield的右边经过计算的值 ，这里说计算的意思是，
       yield后面可以写成函数，表达式等，
第二种：当函数调用到yield时，必须传入一个值，该值存入s中，然后返回yield后面的
       表达式的值并保存当前状态
第三种：只是将数据接受进来，然后执行yield后的语句，再次执行到yield时，保存当前
       状态并返回，这样的用例一般是只打印一些处理消息，而不需要结果的方式。
第四种：这样的只能遍历generator内部的数据了。
```

#### 14.global语句（不理解）

        当它在类或函数定义语句中被使用时，会导致出现在那个环境中的name（名称）的所有形式都被处理为对那个名称的一个全局（模块层）变量的引用，即无论这个name（名称）是否被赋值以及这个name（名称）是否已存在。

        可以在局部作用域内重新关联外部作用域的变量。

#### 15.nonlocal语句（不理解）

        当它被用在嵌套函数中时，会导致出现在该环境中name（名称）的所有形式都被处理为对那个名称在内嵌函数范围内的一个局部变量的引用，即无论这个name（名称）是否被赋值。

        可以给外部作用域的变量赋值。

#### 16.import语句

        （1）概念

```python
import [package.]module [as name]
      [[package.]module [as name]]*
```

        可选的as子句将一个变量name赋给导入的模块对象，并将原有模块名字删除。

        可选的packagei前缀表示包目录路径。

        模块通常是一个Python源代码或编译过的字节码文件。

        模块搜索路径是sys.path,一个从程序的顶层目录初始化的目录名列表

        CPython中，导人也可以用对应于外部语言名的属性加载编译过的C和C++扩展名文件。

        （2）导入算法

                由sys.path定义的模块搜索路径中以绝对路径导入最左侧分量迭代每个目录

1. 如果找到了directory\spam\\\__init\_\_.py，则一个导入正规包并将其返回。

2. 如果找到了directory\spam.{py,pyc,or other module extension}，则导入一个简单的模块并将其返回。

3. 如果发现directory\spam\是一个目录，则将其记录并继续在搜索路径的下一个目录中扫描。

4. 如果没有发现上面的任一种情况，则继续在搜索路径的下一个目录中进行扫描。

#### 17.from语句

```python
from [package.]*module import
            [(] name [as othername]
            [, name [as othername]]*[)]
from [package.]*module import *


from source import name [,name]*        #绝对路径：sys.path
from . import module [,module]*         #相对路径：仅pkg
from .source import name [,name]*       #相对路径：仅pkg
from . import module [,module]*         #pkg中的父目录
from ..source import name [,name]       #pkg中的父目录
```

        （1）包相对导入语法

                from语句(不是import)可以在模块名中使用引导点指定内部包模块的引用一导入

#### 18.class语句

```python
[decoration]
class name [ ( super [, super]* [, metaclass=M ) ]
    suite
```

        class语句构建新的类对象，这些对象是加工实例对象的工厂。

        新的类对象继承于给定顺序中每个列出的超类，并被赋给name变量。

- 超类（基类）列在表头中的括号内

- 类中的赋值语句创建类成员

#### 19.try语句

```python
try:
    suite
except [type [as value]]:
    suite
[except [type [as value]]:
    suite]*
[else:
    suite]
[finally:
    suite]


try:
    suite
finally:
    suite
```

        try语句可以用作在try suite中抛出异常句柄的suites指定except子句。

        如果在try suite中没有异常出现则运行else子句。

        finally子句在异常发生或未发生的地方都运行。
        except子句捕获和恢复异常，finally子句运行中断动作（块退出）

#### 20.raise语句----------

#### 21.assert语句

#### 22.with语句

#### 23.命名空间与范围规则

### 函数

#### 1.函数定义及使用

（1）python使用def保留字及[:]定义函数；

（2）参数用逗号隔开；

（3）没有定义return则默认返回None对象；

```python
# 函数的定义
def <函数名>(<参数列表>):
    <函数体>
    return <返回值列表>
# 函数的使用
<函数名>（实参列表）
```

#### 2.匿名函数

（1）匿名函数只能有一个表达式；

（2）直接在使用的地方定义；

```python
# 匿名函数的定义
lambda <参数列表> : <表达式>
<函数名> = lambda <参数列表> : <表达式>
```

### 装饰器----------------------------------

#### 1.函数闭包(function closure)

①函数式语言中的术语
②函数闭包：一个函数，其参数和返回值都是函数，内部写函数的辅助部分
        用于增强函数功能
        面向切面编程(AOP)

#### 2.语法糖(Syntactic sugar)

指计算机语言中添加的某种对语言的功能没有影响的语法，方便程序员使用。
    ·语法糖没有增加新功能，只是一种更方便的写法，
    ·语法糖可以完全等价地转换为原本非语法糖的代码
    ·装饰器在第一次调用被装饰函数时进行增强

#### 3.装饰器

装饰器`@闭包函数名
装饰器在第一次调用被装饰函数时进行增强
    ·增强时机？在第一次调用之前
    ·增强次数？只增强一次

    ·对于含有返回值的函数，返回值无法返回，但是辅助功能可以添加

    ·对于含有参数的函数，调佣闭包函数后，不能传递参数

    ·需要调整闭包函数的参数及返回值与主要函数相对应才能正常使用

    封装顺序为有内而外，执行顺序为由外而内

##### 4.装饰器的实现

- wrapper

```python
# --------------------- 函数实现Wrapper -------------------------
def decorator(func):
    counter = 0
    def wrapper(*args): # 可用于实例方法
        nonlocal counter
        counter += 1
        func(*args)
    return wrapper

@decorator
def moning(name):
    print('Good moning! --%s' % name)

moning(321)

# --------------------- 类实现Wrapper -------------------------
class Decorator:
    def __init__(self, func):
        self.func = func
    def __call__(self, *args):
        print('='*10)
        self.func(*args)
        print('='*10)

@Decorator
def hello(name):
    print('Hello world! --%s' % name)

hello(123)
```

### 迭代器

##### 1.迭代器协议

- 迭代器必须同时实现__next__和__iter__两个方法。

- 迭代器必须是可迭代的，即「迭代器」是一种「可迭代对象」。

- 所有迭代器的__iter__方法都只要return self即可。

<img title="" src="file:///D:/Cache/MarkText/2022-07-25-14-55-15-image.png" alt="" data-align="center" width="359">

- 可迭代对象：迭代的被调对象，其\_\_iter\_\_方法被iter函数所调用，返回迭代器对象。

- 迭代器对象：可迭代对象的返回结果，在迭代过程中实际提供值的对象，提供__next__方法。

    **工作原理**：每次迭代中调用next,并且通过捕捉StopIteration异常来确定何时离开。

##### 2.两种可迭代对象

- 容器类型
                  ■ 列表、元组、字典等
                  ■ 只有__iter__接口
                  ■ 静态的数据
                  ■ 需要额外的迭代器支持
                  ■ 支持多次迭代

- 迭代器类型
                  ■ 文件、StringlO等
                  ■ 同时实现__iter__和__next__接口
                  ■ 动态的
                  ■ 只能迭代一次

##### 3.迭代器的意义

- 统一通过next()方法获取数据，屏蔽底层不同的数据读取方式，简化编程

- 容器类的数据结构只关心数据的静态存储，迭代器对象负责记录迭代过程的状态信息。

##### 4.文件迭代器

```python
>>> for line in open('script2.py'):   # 使用文件迭代器逐行读取
        print(line.upper(),end='')    # 调用__next__，捕获Stoplteration异常

>>> for line in open('script2.py').readlines():    # 全部读入内存，不推荐
        print(line.upper（）,end='')

>>> f open('script2.py')               # 迭代器以C语言速度运行
>>> while True:                        # while循环通过虚拟机运行字节码
        line f.readline()              # 比迭代器慢
        if not line:break
        print(line.upper(),end='')
```

##### 4.手动迭代：iter和next

- 给定一个迭代器对象X,调用next(X)等同于3.X版本中的X._next_（）

- for循环在开始时，会首先把可迭代对象传入内置函数iter,并由此拿到一个迭代器，而iter调用返回的迭代器对象有着所需的next方法。

```python
while True:
    try:
        X next(I)
    except StopIteration:
        break
    print(X *2,end='')
```

##### 5.列表推导式及扩展的列表推导语法

- 列表推导编写起来更加精简。

- 列表推导比手动的for循环语句运行得更快。

```python
lines = [line.rstrip() for line in open('script2.py')]
```

（1）筛选分句：if

推导表达式中嵌套的for循环可以有一个关联的if分句，来过滤掉那些测试不为真的结果项。

```python
lines = [line.rstrip() for line in open('script2.py') if line[0]=='p']
```

（2）嵌套循环：for

完整语法允许任意数目的for分句，并且每个for分句都可以带有一个可选的关联的if分句。

```python
>>> [x +y for x in 'abc'for y in '1mn']
    ['al','am','an','bl','bm','bn','cl','cm','cn']

>>> res = []
>>> for x in 'abc':            # 一种理解方式，通过缩进转换为语句
        for y in '1mn':
            res.append(x y)
```

##### 6.其他可迭代对象

Python还包含了其他许多处理可迭代对象的内置函数。例如

- sorted能够排序可迭代对象中的各项；

- zip能够组合可迭代对象中的各项；

- enumerate能够把可迭代对象中的项与它们的相对位置进行匹配；

- filter能够按照一个函数是否为真来选择可迭代对象中的项；

- reduce能够针对可迭代对象中的成对的项来运行一个函数。

### 生成器

        ●当调用生成器函数得到生成器对象时
                ■此时的生成器对象可以理解为处**初始**状态
        ●通过next（）调用生成器对象，对应的生成器函数代码开始运行
                ■此时生成器对象处于**运行中**状态
        ●如果遇到了yield语句，next（）返回时
                ■yield语句右边的对象作为next（）的返回值
                ■生成器在yield语句所在位置**暂停**，当再次使用next（）时继续从该位置继续运行
        ●如果执行到函数结束，则抛出StopIteration异常
                ■不管是使用了return语句显式地返回值，或者默认返回None值，返回值都只能作为异常的值一并抛出
                ■此时的生成器对象处于**结束**的状态
                ■对于已经结束的生成器对象再次调用next（）,直接抛出StopIteration异常，并且不含返回值

<img title="" src="file:///D:/Cache/MarkText/2022-07-22-12-18-49-image.png" alt="" data-align="center" width="510">

        

       

    sort(*, key=None, reverse=False)

sort() 仅接受关键字参数：

key 指定带有一个参数的函数，用于从每个列表元素中提取比较键，比较键可以是元组（权重降序）。

闭包：闭包是一种定义在某个作用域中的函数，这种函数引用了那个作用域中的变量。

### Python动态类型

        Python中，类型是在运行时自动决定的，而不是通过代码声明。

##### 1.变量与对象

- 变量创建
  Python在代码运行之前先检测变量名，但可以理解为第一次赋值时就创建了它，之后的赋值将会改变已创建的变量名的值。

- 变量类型
  变量永远不会拥有任何和它关联的类型信息或约束。类型的概念存在于对象而不是变量名中。变量原本是通用的，它只是在一个特定的时间点，简单地引用了一个特定的对象而已。

- 变量使用
  当变量出现在表达式中时，它会马上被当前引用的对象所代替，无论这个对象是什么类型。此外，所有的变量必须在使用前被明确地赋值，使用未赋值的变量会产生错误。

<img title="" src="file:///D:/Cache/MarkText/2022-07-25-13-36-38-image.png" alt="" data-align="center" width="198">

每一个对象都有两个标准的头部信息：

类型标志符(type designator)标识这个对象的类型；

引用的计数器(reference counter)决定何时回收这个对象。

##### 2.共享引用

<img title="" src="file:///D:/Cache/MarkText/2022-07-25-13-53-54-image.png" alt="" data-align="center" width="226">

<img title="" src="file:///D:/Cache/MarkText/2022-07-25-13-55-46-image.png" alt="" width="236" data-align="center">

整数是不可变的，因此没有方法能够在原内存位置修改它。

请求Python复制(copy)对象，而不是创建引用。复制一个列表有很多种方法，包括使用内置list函数或者标准库的copy模块。也许最常用的办法就是从头到尾的分片

##### 3.共享引用和相等

```python
>>> L=[1,2,3]
>>> M=L                # M and L reference the same object
>>> L==M               # Same values
    True
>>> L is M             # Same objects
    True
```

“==运算符”，测试两个被引用的对象是否有相同的值。

“is运算符”，检查对象的同一性。

sys模块中的getrefcount函数会返回对象的引用次数。

```python
>>> import sys
>>> sys.getrefcount(1)    # 647 pointers to this shared piece of memory
    647
```

##### 4.弱引用

        弱引用是通过weakref标准库来实现的一种用于防止对象被垃圾回收的引用（这一引用并非来源于自身）。如果对象的最后一次引用是弱引用，那么这个对象将被重新声明，而相应的弱引用会被自动删除（或被告知）

### 命名空间（作用域）

- 大多数命名空间都使用 Python 字典实现

- 点号之后的名称是 **属性**。严格讲，对模块中名称的引用是属性引用。

##### 作用域细节

- 外围模块是全局作用域，导入后相对于外部模块中的全局变量变成模块对象属性，但在模块文件中仍然作为全局变量调用

- 全局作用域的作用范围仅限单个文件，变量名被划分到一个个模块中，必须导入模块才能使用文件中的变量名。

- 赋值的变量名除非被声明为gloabl或nonlocal，否则均为局部变量。

- 所有其他变量名都是外层函数的局部变量、全局变量或内置变量。

- 函数每次调用都会创建一个新的局部作用域。

##### LEGB规则

- Local j局部作用域：函数或者类的方法内部

- Enclosed 外层局部作用域：指的是嵌套函数（一个函数包裹另一个函数，闭包）

- Global 全局作用域：指的是模块中的全局变量

- Built in 内置作用域：指的是 Python 为自己保留的特殊名称

<img title="" src="file:///D:/Cache/MarkText/2022-07-25-10-35-41-image.png" alt="" data-align="center" width="354">

    3.X版本中内置作用域是通过一个名为builtins的标谁库模块来实现

### 混合使用模式：\_\_name\_\_和\_\_main\_\_

##### 模块的内置属性\_\_name\_\_

- 每个模块都有一个名为\_\_name\_\_的内置属性。

- 如果文件作为顶层程序文件执行，在启动时\_\_name\_\_就会被设置为字符串"\_\_main\_\_"。

- 如果文件被导人，\_\_name\_\_就会改设成客户程序所了解的模块名。

##### \_\_name\_\_的作用

- **单元测试代码**：可以在文件末尾加个\_\_name\_\_测试，把模块暴露接口的测试程序代码封装在其中。这样不但可以在客户程序中通过导入来使用该文件，还可以在系统shell或其他启动方案中通过运行来测试其逻辑。

- **双模式代码**：允许模块被同时编写成一个可导入的库和一个顶层脚本，用于编写既可以作为命令行工具也可以作为工具库使用的文件时。

### 参数

##### 参数传递基础

- 参数的传递是通过自动将对象赋值给局部变量名来实现的。参数实际上都是通过指针传人的。

- 在函数内部赋值参数名不会影响调用者。函数头部的参数名是一个新的、局部的变量名。

- 改变函数的可变对象参数的值也许会对调用者有影响。可变参数可以作为函数的输入和输出。

##### 传递模式

- 不可变参数本质上传入了“值”，但不可能在原位置修改不可变对象。

- 可变对象本质上传入了“指针”，而可变对象能够在函数内部做原位置的改变。

##### 避免修改可变参数的方式

- 创建一个显式的可变对象的副本。

```python
L=[1, 2]
changer(X,L[:])
```

- 在函数内部进行复制。

```python
def changer(a,b):
    b=b[:]
    a=2
    b[0]='spam'
```

- 把可变对象转换为不可变对象（不推荐）。

```python
L=[1, 2]
changer(X,tuple(L))
```

        使用这种技术给函数加上了比原本更多的限制，还会让函数丧失对参数使用列表方法的能力，包括那些并不会在原位置修改对象的方法。

##### 输出参数返回多重结果

        因为return能返回任意种类的对象，所以它也能返回多个值，做法是将这些值封装进一个元组或其他的集合类型中。

##### 关键字参数与默认值参数

- 关键字参数
  
  - 关键字参数允许指定传递内容与传递名称的关系，即通过名称匹配，而不是基于位置。例：`f(c=3,b=2,a=1)`

- 默认值参数
  
  - 认值参数允许我们让特定的参数变为可选的。例：`def f(a,b=2,c=3) : print(a,b,c)`

##### 可变长参数

##### Keyword-only参数

- keyword-.only参数编写为出现在参数列表中*args之后的有名参数。
  
  - 在如下的代码中，可以按照名称或位置传入，b收集所有其他的基于位置参数，而c必须只按照关键字传递。
  
  ```python
  def kwonly(a,*b,c):
      print(a,b,c)
  ```

- 参数列表中使用一个“*”字符，来表示一个函数不会接受一个可变长度的参数列表，但是仍然期待跟在“*”后面的所有参数都作为关键字参数传入。

### 模块基础

##### 模块概念

        模块是提供自包含的变量的包（也就是所谓的命名空间）从而将部件组织为系统的一种可行方式。一个模块文件顶层定义的所有变量都变成了被导人的模块对象的属性。

##### 模块意义

- 代码重用

- 系统命名空间的划分

- 实现共享的服务和数据

##### import工作流程

- **第一次导入**时
  
  - 找到模块文件。
  
  - 编译成字节码（如果需要的话）。Python3.2及之后节码文件被集中存放在\_\_pycache\_\_目录中
  
  - 执行模块的代码来创建其所定义的对象。文件中所有语句会从头至尾依次执行。

- 再次导入相同模块时，会跳过这三个步骤，而只提取内存中已加载的模块对象。

##### 模块搜索路径

1. 程序的主目录
   
   - 当你运行一个程序的时候，主目录就是包含程序的顶层脚本文件的目录。
   - 当在交互式命令行下工作时，主目录就是你当前工作的目录。
   - 这个目录是优先搜索的，其文件也将覆盖路径上其他目录中具有同样名称的模块。

2. PYTHONPATH目录（如果设置了的话）
   
   - PYTHONPATH是环境变量
   
   - Python会从左至右搜索PYTHONPATH环境变量设置中罗列出的所有目录。

3. 标准库目录

4. 任何.pth文件中的内容（如果存在的话）
   
   - Python允许用户把需要的目录添加到模块搜索路径中去
   
   - 在后缀名为pth的文本文件中列出目录，并将其放置在会被搜索到的目录中。
   
   - 该功能相对不常用。

5. 第三方扩展应用的site-packages主目录
- 五个组件组合起来就变成了sys.path。

- 第一和第三组件是自动被定义的。

- 第二和第四组件就可以用于拓展路径。

##### 模块原文件

        import b可能被解释为

- 源代码文件 b.py

- 字节码文件 b.pyc

- 优化字节码文件 b.pyo（一种相对不常见的形式）

- 目录b,对于包导入而言(在第24章说明)

- 编译扩展模块(通常用C或C++编写)，导入时使用动态链接（例如，Linux的b.so、Cygwin和Windows的b.dll或b.pyd)

- 用C编写的编译好的内置模块，并被静态链接至Python

- ZIP文件组件，导入时会自动解压缩

- 内存内镜像，对于冻结可执行文件而言

- Java类，在Jython版本的Python中

- NET组件，在IronPython版本的Python中

### 模块包

- 导入还可以指定目录路径。

- Python代码的目录被称为包，因此这样的导入就称为包导入。

- 包导入是把计算机上的目录变成另一个Python命名空间，其属性则对应于目录中所包含的子目录和模块文件。

##### 包导入基础

```python
import dir1.dir2.mod
from dir1.dir2.mod import x

dir0\dir1\dir2\mod.py
# dir1在某个容器目录dirO中，而dirO目录可以在Python模块搜索路径中找到。
```

- import语句中的目录路径只能是以点号间隔的变量。

##### \_\_init\_\_.py

- 结构：diro\diri\dir2\mod.py

- 对应形式的import语句：import diri.dir2.mod

- 必须遵循下列规则：
  
  - dirl和dir2中都必须含有一个init_py文件。
  
  - dir0是容器，不需要initpy文件，如果有的话，这个文件也会被忽略。
  
  - dir0(而非dir0\dir1)必须列在模块搜索路径的sys.path列表中。

- \_\_init\_\_.py代码将在Python第一次导人一个路径的时候被自动运行。

包初始化文件的作用

- 包的初始化：Python在首次导入某个目录时，会自动执行该目录下initpy文件中的所有程序代码。包可以通过其初始化文件来创建所需要的数据文件、连接数据库等。

- 模块使用的声明：声明一个路径是Python包，可以防止有相同名称的目录不小心隐藏了出现在模块搜索路径后面的真正模块。

- 模块命名空间的初始化：在包导入的模型中，你脚本中的目录路径在导入后会变成真实的嵌套对象路径。导人表达式dir1.dir2运行后，会返回一个模块对象，而此对象的命名空间包含了dir2的\_\_init\_\_.py文件中赋值的所有名称。\_\_init\_\_.py文件为目录（没有实际对应的模块文件）创建的模块对象提供了命名空间。

- from\*语句的行为：可以在initpy文件内定义\_\_all\_\_列表来规定目录以from\*语句形式导入时，需要导出什么。如果没有设定\_\_all\_\_,from\*语句不会自动加载嵌套于该目录内的子模块；取而代之的是，只加载该目录的\_\_init\_\_.py文件中赋值语句定义的名称，包括该文件中程序代码显式导入的任何子模块。

##### reload()

- 任何已导入的目录也可以传递给reload,来强制该项目重新执行。

##### from与import

- 如果需要读取两个或两个以上路径内的同名属性时，就必须使用import,而不能用from；

- 如果被调用的函数名称在每个路径内都不同，from语句就可以避免每当调用其中一个函数时，就要重复写出完整包路径的问题；

- from语句的as扩展子句也可以用于提供具有唯一性的别名。

##### 包的相对导入

- 于包中的导入，Python3.X引入了两个变化：
  
  - 它修改了模块导入搜索路径语义，从而默认地跳过包自己的目录。导入只检查sys·path列表中的搜索路径。这称为绝对导人。
  
  - 它扩展了from语句的语法，以允许显式地要求导人只搜索包的目录（以点号开始）。这称为相对导入语法。

- 相对导入基础知识
  
  - **以点号开头的导入**：在from语句中使用以点号开头的模块名，来表示导入应该只相对于外围的包这样的导入将只是在包的内部目录进行搜索，而不会搜索到位于导入搜索路径(sys.path)上某处的同名模块。
  
  - **不以点号开头的导入**：在Python3.X中，在一个包中的导入默认是仅绝对的一在缺少特殊的点号开头语法的时候，导人忽略了外围包自身，转而在sys,path搜索路径上的其他位置查找。
  
  - 无点号开头的from语句与import语句的行为相同

- 相对导入的适用情况
  
  - 相对导入只适用于在包内部的导入。
  
  - 相对导入只能用于from语句。相对导入的特征是在一个from中的模块名前面有一个或多个点号。

##### 模块查找规则总结

- 基础模块的简单名称(例如A)通过搜索sys.path列表上的各个目录，从左到右被查找。

- 包是带有一个特殊的\_\_init\_\_.py文件的Python模块的目录，该文件允许导入中可以使用A.B.C目录路径语法。

- 在一个包文件内，常规的import语句使用和其他地方的导人是一样的sys.path搜索规则。包内导入使用from语句和点号开头的模块名，而且它是相对于包的；也就是说，Python只会检查包目录，而不会采用常规的sys.path搜索。
