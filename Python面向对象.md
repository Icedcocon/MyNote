# Python面向对象

### 特点：

1. 多态：可以对动态类型执行相同操作，而操作行为随类型而异

2. 封装：对外部隐藏对象工作原理的细节

3. 继承：由基类创建派生类

### Python类基础

- C++ 术语描述：类成员通常为 *public* ，所有成员函数都是 *virtual*。

- Python 的内置类型可以用作基类。

- 算术运算符、下标等具有特殊语法的内置运算符都可以为类实例而重新定义。

##### 类的特征

- class语句创建类对象并将其赋值给一个名称。

- class语句内的赋值语句会创建类的属性。

- 类属性提供了对象的状态和行为。

##### 对象的特征

- 像函数那样调用类对象会创建新的实例对象。

- 每个实例对象继承了类的属性并获得了自己的命名空间。

- 在方法内对self属性做赋值运算会产生每个实例自己的属性。

<img title="" src="file:///D:/Cache/MarkText/2022-07-26-08-33-32-image.png" alt="" data-align="center" width="280">

继承是在属性点号运算时发生的，而且只与查找连接对象内的名称有关。

方法必须通过se1f参数才能获取当前处理的实例。

类的内部或外部修改实例属性，内部用self，外部给对象赋值。

添加类所不能使用的数据没有意义，因此使用基于属性访问运算符重载限制。

<img title="" src="file:///D:/Cache/MarkText/2022-07-26-09-03-08-image.png" alt="" data-align="center" width="405">

SecondClass重载了FirstClass中的display？

```python
class ThirdClass(SecondClass):        # Inherit from SecondClass
    def init(self,value):             # On "ThirdClass(value)"
        self.data = value
    def add (self,other):             # On "self other"
        return ThirdClass(self.data + other)
    def str_(self):                   # On "print(self)","str（）"
        return '[Thirdclass:%s]' % self.data
    def mul(self,other):              # In-place change:named
        self.data *= other
```

##### 两种变量

- 类属性，类变量，公共属性，所有实例共享
  
  - 可以通过类名、实例名调用，但只能通过类名修改

- 实例属性，实例变量，成员变量，
  
  - 可以通过实例名调用，只能通过实例名修改

##### 重载、重写、重定义

（1）重写（override）：重写也可以看做覆盖，子类重新定义父类中具有相同名称和参数的虚函数，函数特征相同，但函数的具体实现不同，它主要在继承关系中出现。被重写的函数不能是static的，但必须是virtual的。

（2）重载（overload）：重载是函数名相同，参数列表不同，重载只是在类的内部存在，但是不能返回类型来判断。

（3）重定义：重定义也叫作隐藏，子类重新定义父类中具有的相同名称的非虚函数。如果一个类存在和父类相同的函数，则这个类将会覆盖其父类的方法，只能在调用的时候强制转换为父类类型，否则对子类和父类做类似的重载的调用是不能成功的。

##### 重载运算符

- 以双下划线命名的方法(\_\_X\_\_)是特殊钩子。

- 当实例出现在内置运算中时，这类方法会自动被调用。

- 类可以重载绝大多数内置类型运算。

- 默认的运算符重载方法既不存在，也不需要，即不定义就使用会引起异常。

- 新式类有一些默认的运算符重载方法，但是不属于常见运算。

- 运算符将类与Python的对象模型结合到一起。

##### 世界上最简单的Python类

```python
class rec:pass
```

因为没有写任何方法，所以我们需要无操作的pass占位符语句

类和C的struct类似，调用时也不需要实例对象

##### \_\_dict\_\_属性、__class__属性和__bases__属性

（1）\_\_dict\_\_是一个实例的属性命名空间

```python
>>> list(rec.__dict_.keys())
    ['age','module_','qualname_','weakref','name','dict','doc_']

>>> x.name,x.dict_[.'name']
    ('Sue','Sue')
```

- dir(X)与X.\_\_dict\_\_.keys()类似，但dir还包括继承和内置的属性。

（2）\_\_class\_\_是一个实例中指向其类的链接

```python
>>> x.__class__
    <class 'main_.rec'>
```

- 当类为self属性赋值时会将自身填入实例对象的__class__属性中。

（3）\_\_bases\_\_是其父类对象引用的元组

```python
>>> rec.__bases__
    (<class 'object'>,)
```

##### 总结

Python中的OOP其实就只是在已连接命名空间的对象内寻找属性而已。

### 类代码

##### 一般形式及属性

```python
class name(superclass,...):        # Assign to name
    attr = value                   # Shared class data
    def method(self,...):          # Methods
        self.attr = value          # Per-instance data
```

- 在class语句内，任何赋值语句都会产生类属性。

- 类似函数，class语句中的赋值语句创建的名称位于其局部作用域中。

- 类似模块，class语句中赋值的名称会成为类对象中的属性。

- 当class语句本身运行时（不是创建实例时），内部的所有语句都会执行。

##### 方法

- 方法的第一位参数总是当前的实例对象self。

- Python会把实例方法的调用映射为类的方法函数，方法调用需通过实例

- 第一位参数通常都称为self，只有其位置重要，名称不重要。

##### 调用父类构造函数

- 必须通过类显式地调用父类的__init__方法保证子类执行父类构造函数。

##### 继承

- 实例属性是由对方法内的self属性进行赋值运算而产生的。（或class外）

- 类属性是通过class语句内的语句（赋值语句）而创建的。（或class外）

- 父类的连接是通过class语句首行的括号内列出的类而产生的。

<img title="" src="file:///D:/Cache/MarkText/2022-07-26-11-42-56-image.png" alt="" data-align="center" width="378">

##### 抽象父类

        类的部分行为预期由其子类来提供。若子类未定义，当继承搜索失败时引发名称未定义异常。

```python
class Super:
    def method(self):
        print('in Super.method')
    def delegate(self):
        self.action()
    def action(self):                            # 如果父类被误调用，报错
        assert False, 'action must be defined!'
        # raise NotImplementedError('action must be defined!')

from abc import ABCMeta,abstractmethod

class Super(metaclass = ABCMeta):
    def delegate(self):
        self.action()
    @abstractmethod
    def action(self):
        pass

class Provider(Super):
    def action(self):
        print('in Provider.action')

if __name__ == "__main__":
    x = Provider()
    x.method()
    x.delegate()


in Super.method
in Provider.action
```

1. 在x.delegate调用一开始，Python会搜索Provider实例和类树中更上层的类对象，直到在Super中找到delegate的方法。实例x会照常传给该方法的self参数。

2. 在Super.delegate方法中，self.action会对self以及它上层的对象发起另一次新的继承搜索。因为self引用了一个Provider的实例，所以action方法会在Provider子类中找到。

3. 采用ABCMeta,abstractmethod，除非子类中的所有抽象方法都已经定义，否则带有抽象方法的类是不能实例化的

##### 不同类型的变量

```python
# manynames.py
X = 11                    # 1
def f():
    print(X)
def g():
    X=22                  # 2
    print(X)
class C:
    X=33                  # 3
    def m(self):
        X=44              # 4
        self.X 55         # 5

# otherfile.py
import manynames
X = 66                    # 6
```

1. 模块属性

2. 函数内的局部变量

3. 类属性

4. 方法中的局部变量

5. 实例属性

6. 全局属性

        **类是一个可以访问其外层作用域的局部作用域，但其本身却不能作为一个外层作用域被访问。**

#### 文档字符串

1. 模块中的字符串docstr.\_\_doc\_\_

2. 函数中的字符串docstr.fun.\_\_doc\_\_

3. 类中的字符串spam.\_\_doc\_\_或者docstr.spam.\_\_doc\_\_

4. 方法中的字符串spam.method.\_\_doc\_\_或者self.method.\_\_doc\_\_

```python
"I am:docstr.__doc__"
def func(args):                
    "I am:docstr.func.__doc__"
    pass
class spam:
    "I am:spam.doc or docstr.spam.__doc__ or self.__doc__"
    def method(self):
        "I am:spam.method.__doc__ or self.method.__doc__"
        print(self.__doc__)
        print(self.method.__doc__)

import docstr
docstr.__doc__
```

##### 类与模块的相同点及区别

    和模块一样，类也支持 Python 动态特性：在运行时创建，创建后还可以修改。

- 模块
  
  - 实现了数据/逻辑包。
  
  - 通过Python文件或其他语言的扩展来创建。
  
  - 通过导入来使用。
  
  - 成为Python程序结构的顶层。

- 类
  
  - 实现了新的功能完整的对象。
  
  - 通过class语句来创建。
  
  - 通过调用来使用。
  
  - 总是位于一个模块中。



### 运算符重载

        实例被创建时，首先触发new方法，创建并返回一个新的实例对象，并传入init函数以供初始化。
