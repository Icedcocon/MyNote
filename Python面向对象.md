##### contains

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

- 运算符重载让类拦截常规的Python操作。

- 类可重载所有Python表达式运算符。

- 类也可重载打印、函数调用、属性访问等内置运算。

- 重载使类实例的行为更接近内置类型。

- 重载是通过在一个类中提供特殊名称的方法来实现的。

<img title="" src="file:///D:/Cache/MarkText/2022-07-27-08-36-18-image.png" alt="" width="527" data-align="center">

<img title="" src="file:///D:/Cache/MarkText/2022-07-27-08-36-53-image.png" alt="" width="531" data-align="center">

##### \_\_getitem\_\_和\_\_setitem\_\_

- 把X作为第一位参数传入，并且将方括号内的索引值传给第二个参数。

- \_\_getitem\_\_可以检测它接收的参数类型，并提取分片对象的边界。

- 分片对象拥有start、stop和step这些属性，任何一项被省略的话都可以为None。

##### \_\_index\_\_（不是索引）

- index方法会为一个实例返回一个整数值，供转化数字串为不同进制的内置函数使用。

##### \_\_getitem\_\_

- 任何支持for循环的类也会自动支持Python所有迭代上下文。

- 成员关系测试in、列表推导、内置函数map、列表和元组赋值运算以及类型构造方法会自动调用\_\_getitem\_\_。

##### \_\_iter\_\_和\_\_next\_\_

- Python中所有的迭代上下文都会先尝试\_\_iter\_\_方法，再尝试\_\_getitem\_\_方法。
- \_\_iter\_\_返回迭代器对象（如果本身有\_\_next\_\_方法也可以返回self）。
- Python会重复调用这个迭代器对象的next方法来产生元素。
- 因为iter对象在调用过程中显式地保持了被管理的状态信息，所以比getitem_具有更好的通用性。

##### 单个对象上的多个迭代器

- 如果\_\_iter\_\_被设计为**返回self**，则只能迭代一次，因为只有一个状态信息在self中。
- 生成器函数和生成器表达式会隐式地存储它们的状态，并创建需要的方法来遵守迭代协议。
- \_\_iter\_\_需替迭代器定义一个新的状态对象，即除可迭代对象外定义一个迭代器类。
- 采用**\_\_iter\_\_和yield**可以更方便的实现多个迭代器，生成器函数能够自动地保存局部变量状态并创建\_\_next\_\_。

##### \_\_contains\_\_、\_\_iter\_\_、\_\_getitem\_\_

- 在迭代领域，类通常把in成员关系运算符实现为一个迭代。

- 当\_\_contains\_\_方法存在的时候，它将优先于\_\_iter\_\_方法

- 而\_\_iter\_\_方法则优先于\_\_getitem\_\_方法

- \_\_contains\_\_方法应该把成员关系定义为对一个键值做映射（可以采用快速查找）

##### \_\_getattr\_\_、\_\_setattr\_\_

- \_\_getattr\_\_方法用来拦截属性引用。

- 用一个未定义的（不存在的）属性名称字符串对一个实例对象做点号运算时，它会被调用。

- \_\_setattr\_\_会拦截所有的属性赋值。

##### \_\_repr\_\_和\_\_str\_\_

- \_\_str\_\_会首先被打印操作和str内置函数尝试(print运行的内部等价形式)。它通常应当返回一个用户友好的显示。

- \_\_repr\_\_用于所有其他的场景：包括交互式命令行、repr函数、嵌套的显示，以及没有可用\_\_str\_\_时的print和str调用。它通常应该返回一个编码字符串，可以用来重新创建对象，或者给开发者一个详细的显示。

        **三个注意事项**

1. \_\_str\_\_和_\_\_repr\_\_都必须返回字符串；其他的结果类型不会被自动转换反而会引发错误。
2. \_\_str\_\_的用户友好显示也许只会应用在对象出现在打印操作顶层时。内嵌在更大对象中的对象（如，被放在列表中）也许仍然使用_\_\_repr\_\_或其默认的方法打印。
3. 在少数场景下显示方法也有可能触发无限递归循环，如一个对象里还包括另一个对象的显示。

##### 加法、右侧加法和原位置加法

- \_\_add\_\_方法只支持将实例对象写在+运算符左侧。

- 只有当+右侧是实例对象且左侧不是实例对象时，Python才会调用\_\_radd\_\_。

- 在其他所有情况下，则由左侧实例对象调用\_\_add\_\_方法。

- 可以在\_\_radd\_\_中重用\_\_add\_\_方法

- 使用原位加法+=，可以编写一个\_\_iadd\_\_或一个\_\_add\_\_。如果前者缺省的话就会退而求其次地使用后者。

```python
class Commuter2:
    def init_(self,val):
        self.val val
    def add (self,other):
        print('add',self.val,other)
        return self.val other
    def radd(self,other):                # 调用__add__方法
        return self._add(other)
```

##### \_\_call\_\_

- 当调用**实例**时会使用\_\_call\_\_方法。
- 并且传递所有的基于位置参数或关键字参数。
- 它既允许我们编写遵循函数调用接口的对象，又让我们能使用类的诸如状态信息记忆和继承关系等功能。
- 如基于回调的代码，如果想让事件处理器保存事件之间的状态，那么你既可以注册类的绑定方法，也可以注册遵循所需接口的实例对象

```python
class Prod:
    def init (self,value):
        self.valuevalue
    def call(self,other):
        return self.value other


x = Prod(2)
x(3)
x(4)
```

### 类的设计

##### Python和OOP

- **继承**：继承以Python中(X.name表达式内)的属性查找为基础。

- **多态**：在X.method中，method的意义取决于主体对象X的类型（类）。

- **封装**：方法和运算符实现行为，不过默认情况下数据隐藏是一种惯例。

##### 与C++的区别

- Python中的多态基于对象接口而不是基于参数类型签名(type signature)（传递的参数个数及其类型）的重载函数。

- 通过参数列表来重载方法可以运行，但是因为def直接把对象赋值给类作用域中的变量名，所以方法函数的最后一次定义才是被唯一保留的。

```python
class C:
    def meth(self,x):
        ...
    def meth(self,x,y,z):
        ...
```

- Python可以实现基于类型进行选择的代码，但通常推荐对不同的操作使用不同的方法名而不应依赖函数调用签名。

```python
class C:
    def meth(self,x):
        x.operation()
```

##### 继承、组合（聚合）和委托

- 继承（is-a）：继承是由属性点号操作启动的，并由此触发实例、类以及任何父类中的变量名搜索。

- 组合（has-a）：组合涉及把其他对象嵌入容器对象内，并促使其实现容器方法。

- 委托：委托通常是指控制器对象内嵌其他对象，并把操作请求传递给那些内嵌的对象。使用包装器（有时叫作代理）类管理单一的内嵌对象，而包装器类则保留了内嵌对象的大多数或全部的接口。

##### 对象的序列化和持久化

- 通过序列化(**pickle**)或持久化(**shelve**)一个类实例

- 序列化机制把内存中的对象转换成序列化的字节流(Python中的字符串)，它们可以保存在文件中，也可通过网络进行发送。

- 反序列化则将字节流转换为相同的一个内存中的对象。

- 持久化机制会自动把对象序列化并存储到一个按健访问的数据库中，而数据库导出类似于字典的接口。

##### name-mangling

- 用C++术语来讲，Python中的属性都是“public”和“virtual'”的，它们在任意地方都可进行读取，并且在运行时进行动态查找。

- name-mangling是一种把类所创建的名称局部化到这个类的方式：名称重整并不能够阻止来自类外部代码的访问，这种功能主要是为了**避免实例内的命名空间冲突**，而不是限制名称的访问，因此重整后的变量名最好称之为“伪私有”，而不是“私有”。

- 概念：只在class语句内部，任意开头有双下划线，但结尾没有双下划线的名称，会自动在前面包含外围类的名称从而进行扩展。例如，Spam类中的\_\_X这样的名称会自动变成\_Spam\_\_X。

- 所以类的编写者可以相当安全地假设：他们真的拥有前面带有双下划线的变量名。

- 这个功能一般只在大型的多人项目中使用，而且只用于已选定的名称。

- 只有当某些名称真的需要被单个类控制时，才使用这项功能。

##### 绑定方法对象和未绑定方法对象

- 未绑定（类）方法对象：无self。
  
  - 通过对类进行点号运算从而获取类的函数属性，会传回未绑定(unboud)方法对象。
  
  - 调用该方法时，必须明确提供实例对象作为第一位参数，在Python3.X中若方法不需要实例，也可以不传入。
  
  - 在Python3.X中，一个未绑定方法和一个简单函数是相同的，并且可以通过类名来调用

- 绑定（实例）方法对象：self+函数
  
  - 通过对实例进行点号运算从而获取类的函数属性，会传回绑定(bound)方法对象。
  
  - Pytho在绑定方法对象中自动把实例和函数打包，所以不用传递实例去调用该方法。

---

- 可以把这个绑定方法对赋值给另一个变量名，然后像简单函数那样调用它

```python
object1 Spam()
x = object1.doit
x('hello world')


object1 Spam()
t = Spam.doit
t(object1,'howdy')
```

- Python支持三种类级别的方法：实例，静态和类

- Python3.X这门语言已经删除了未绑定方法的概念，未绑定方法在3.X中被当作简单函数对待。

- 只有经实例调用，Python3.X才会向方法传递一个实例。经类调用的方法只有在需要一个实例的时候，才必须手动传递实例。

- 由于绑定方法在单步打包中组合了函数和实例，因此它们在调用时不需要任何特殊语法，并且可被当作其他可调用对象那样来对待，如，通过变量进行传递。
