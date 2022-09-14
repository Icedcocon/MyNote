# 语法基础

### property和描述符

- property协议允许我们把一个特定属性的获取、设置和修改操作指向我们所提供的函数或方法
  
  - 插入在访问、设置属性时自动运行的代码
  
  - 拦截属性的删除
  
  - 为属性提供文档
  
  - 把一个属性从简单的数据改变为一个计算
    
    ```python
    # -----------------------------  Property 示例  -------------------------------------
    
    class Person:
        def __init__(self, name):
            self._name = name
        def getName(self):
            print('fetch ...')
            return self._name
        def setName(self, value):
            print('change ...')
            self._name = value
        def delName(self):
            print('remove ...')
            del self._name
        name = property(getName, setName, delName, "name property docs")
    
    bob = Person('Bob Smith')
    print(bob.name)
    bob.name = 'Robert Smith'
    print(bob.name)
    del bob.name
    
    print('-'*20)
    sue = Person('Sue Jones')
    print(sue.name)
    print(Person.name.__doc__)
    ```

- 使用装饰器编写property时，被装饰的方法会自动传递给property内置函数的第一个参数。
  
  - property对象有getter、setter和deleter方法
  
  - getter方法通常由创建property这一行为来实现
  
  - setter方法在访问属性时调用
  
  - deleter方法在删除属性时调用
  
  - 三种方法返回property的一个副本
    
    ```python
    # -----------------------------  Property 等价  -------------------------------------
    print('='*20)
    
    class PersonDecorator:
        "PersonDecorator new docs"
        def __init__(self,name):
            self._name = name
    
        @property
        def name(self):
            "name property new docs"
            print('fetch...')
            return self._name
    
        @name.setter
        def name(self, value):
            print('change...')
            self._name = value
    
        @name.deleter
        def name(self):
            print('remove...')
            del self._name
    
    bob = PersonDecorator('Bob Smith')
    print(bob.name)
    bob.name = 'Robert Smith'
    print(bob.name)
    del bob.name
    
    print('-'*20)
    sue = PersonDecorator('Sue Jones')
    print(sue.name)
    print(PersonDecorator.name.__doc__)
    print(PersonDecorator.__doc__)
    ```

- 描述符(descripter)提供了拦截属性访问的另一种替代方法，property是描述符的一种：从技术上讲，property内置函数只是创建一个特定类型的描述符的一种简化方式，而这种描述符在属性访问时运行方法函数。
  
  - 描述符编写成独立的类，并且它们就像方法函数一样被赋值给类属性。
  
  - 描述符管理一个单个的、指定的属性。
  
  - 描述符的适用范围更广，而且提供了一种更为通用的解决方案
  
  - 所有带有\_\_get\_\_、\_\_set\_\_和\_\_delete\_\_方法的类都可以看作描述符。
  
  - 描述符类实例成为另一个类的属性时，访问该类的属性会自动调用这些方法。
  
  - 让使用描述符的类中的描述符实例属性成为只读的，要在描述符类中捕获赋值操作并引发一个异常来阻止属性赋值。
    
    ```python
    # -----------------------------  Desctiptor 等价  -------------------------------------
    print('='*20)
    
    class Name:
        "name descriptor docs"
        def __get__(self, instance, owner):
            print('fetch...')
            return instance._name
    
        def __set__(self, instance, value):
            print('change...')
            instance._name = value
    
        def __delete__(self, instance):
            print('remove...')
            del instance._name
    
    class PersonDesctiptor:
        def __init__(self, value):
            self._name = value
        name = Name()
    
    bob = PersonDesctiptor('Bob Smith')
    print(bob.name)
    bob.name = 'Robert Smith'
    print(bob.name)
    del bob.name
    
    print('-'*20)
    sue = PersonDesctiptor('Sue Jones')
    print(sue.name)
    print(Name.__doc__)
    ```

### 静态方法

# 前言

## 创建型模式

GoF的23种设计模式中，创建型模式讨论的是高效创建对象的问题，共5种：

- 工厂方法模式
- 抽象工厂模式
- 单例模式
- 建造者模式
- 原型模式

## 案例实现

- [《大话设计模式》C++版](https://github.com/yogykwan/design-patterns-cpp)
- [《大话设计模式》Python版](https://github.com/yogykwan/design-patterns-py)

# 简单工厂模式

### 内容

 不直接向客户端暴露对象创建的实现细节，而是通过一个工厂类来负责创建产品类的实

### 角色

- 工厂角色(Creator)

- 抽象产品角色(Product)

- 具体产品角色(Concrete Product)

### 优缺点

- 优点：
  
  - 隐藏了对象创建的实现细节
  
  - 多客户端不需要修改代码

- 缺点：
  
  - 违反了单一职责原则，将创建逻辑几种到一个工厂类里
  
  - 当添加新产品时，需要修改工厂类代码，违反了开闭原则

### 特点

- 判断位于工厂类内，但工厂类并不实现功能

- 具体功能的实现交给其他类完成

- 简单工厂模式的最大优点在于工厂类中包含了必要的逻辑判断，根据客户端的选择条件动态实例化相关的类，对于客户端来说，去除了与具体产品的依赖。

### UML

<img title="" src="file:///D:/Cache/MarkText/2022-08-01-17-33-51-image.png" alt="" width="480" data-align="center">

### 代码

```python
#!/usr/bin/env python
# encoding: utf-8
"""
简单工厂模式
计算器
"""

from abc import ABCMeta, abstractmethod

class Opertaion(object):
    @abstractmethod
    def getResult(self):
        pass

class OperationPlus(Opertaion):
    def getResult(self):
        return self.a + self.b

class OperationMinus(Opertaion):
    def getResult(self):
        return self.a - self.b

class OperationFactory(object):
    def createOperation(self, operator):
        if operator == '+':
            return OperationPlus()
        if operator == '-':
            return OperationMinus()
        else:
            raise Exception('Wrong usage!')

if __name__ == '__main__':
    op = OperationFactory().createOperation('*')
    op.a = 10
    op.b = 5
    print(op.getResult())
```

# 工厂方法模式

### 工厂方法模式

### 内容

 定义一个用于创建对象的接口，让子类决定实例化哪个类。**工厂方法模式让一个类的实例化延迟到其子类。**

### 角色

- 抽象工厂角色(Creator)

- 具体工厂角色(Concrete Creator)

- 抽象产品角色(Product)

- 具体产品角色(Concrete Product)

### 优缺点

- 优点：
  
  - 多每个具体产品都对应一个具体工厂类，不需要修改工厂类代码
  
  - 多隐藏了对象创建的实现细节

- 缺点：
  
  - 每增加一个具体产品类，就必须增加一个相应的具体工厂类

### 特点

- 工厂方法模式就是简单工厂模式的进一步抽像。工厂方法模式中，核心的工厂被提升为一个抽象类，将具体的创建工作交给他的子类完成。这个**抽象的工厂类仅规定具体工厂实现的接口**，而不明确指出如何实例化一个产品类，这使得工厂方法模式允许系统在不修改原有产品结构的情况下轻松的引进新产品。

- 工厂方法**把简单工厂的内部判断逻辑移到了客户端代码**，**本来需要修改工厂类，现在是修改客户端**。

- 简单工厂模式违背了开放-封闭原则，工厂方法模式借助多态，克服了该缺点，却保持了封装对象创建过程的优点。

### UML

<img title="" src="file:///D:/Cache/MarkText/2022-08-01-17-38-01-image.png" alt="" data-align="center" width="578">

### 代码

```python
from abc import ABCMeta, abstractmethod

class Opertaion(object):
    @abstractmethod
    def getResult(self):
        pass

class OperationPlus(Opertaion):
    def getResult(self):
        return self.a + self.b

class OperationMinus(Opertaion):
    def getResult(self):
        return self.a - self.b

class OperationFactory(object):
    @abstractmethod
    def createOperation(self):
        pass

class PlusFactory(OperationFactory):
    def createOperation(self):
        return OperationPlus()

class MinusFactory(OperationFactory):
    def createOperation(self):
        return OperationMinus()

if __name__ == '__main__':
    op = PlusFactory().createOperation()
    op.a = 10
    op.b = 5
    print(op.getResult())
```

# 抽象工厂模式

### 内容

- 抽象工厂模式：提供一个创建一系列相关或互相依赖对象的接口，只需要知道对象的系列，无需知道具体的对象。

- 相比工厂方法模式，抽象工厂模式中的每个具体工厂都生产一套产品。

### 角色

- 抽象工厂角色(Creator)

- 具体工厂角色(Concrete Creator)

- 抽象产品角色(Product)

- 具体产品角色(Concrete Product)

- 多客户端(Client)

### 优缺点

- 优点：
  
  - 将客户端与类的具体实现相分离
  
  - 每个工厂创建了一个完整的产品系列，使得易于交换产品系列
  
  - 有利于产品的一致性（即产品之间的约束关系）

- 缺点：
  
  - 难以支持新种类的（抽象）产品

### 特点

- 在客户端中，具体工厂类只在初始化时出现一次，更改产品系列即可使用不同产品配置。

- 利用简单工厂类替换抽象工厂类及其子类，可以使客户端不再受不同系列的影响。

- 结合反射机制，Assembly.Load(“程序集名称”).CreateInstance(“命名空间”.“类名”)，可以直接通过字符串创建对应类的实例。所有在简单工厂中，都可以通过反射去除switch或if，解除分支判断带来的耦合。

- 反射中使用的字符串可以通过配置文件传入，避免更改代码。

# 单例模式

### 内容

让类自身保证它只有一个实例，并提供一个全局访问点。

### 角色

单例(Singleton)

### 优缺点

- 优点：
  
  - 对唯一实例的受控访问
  
  - 单例相当于全局变量，但防止了命名空间被污染

### 特点

- 多线程下单例模式可能失效，需要采取双重锁定的的方式，确保被锁定的代码同一时刻只被一个进程访问。

- 饿汉式单例：即静态初始化方式，在类初始化时产生私有单例对象，会提前占用资源；渴汉式单例：在第一次被引用时将自己初始化，会产生多线程访问安全问题，需要添加双重锁定。

```python
# -----------------------元类实现单例模式-------------------------------
class MyType(type):
    # 类只创建一次
    def __init__(cls, classname, supers, classdict):
        super().__init__(classname, supers, classdict)
        cls.instance = None
    # 类实例化时会调用__call__方法
    def __call__(cls, *args, **kwargs):
        # 判断是否存在对象，有则不创建，没有就创建
        if not cls.instance:
            cls.instance = cls.__new__(cls)
        # 调用类的__init__去初始化      
        cls.__init__(cls.instance, *args, **kwargs)
        return cls.instance

class Singleton(object, metaclass = MyType):
    pass


if __name__ == '__main__':
    c1 = Singleton()
    c2 = Singleton()

    print(c1)
    print(c2)

# -----------------------__new__()实现单例模式-------------------------------
class Singleton2(object):
    instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance


if __name__ == '__main__':
    c3 = Singleton2()
    c4 = Singleton2()

    print(c3)
    print(c4)
```

# 建造者模式（Builder）

1. 建造者模式：将复杂对象的创建与表示分开，使得相同的创建过程可以有不同的表示。用户只需制定需要建造的类型，不需要知道建造的过程和细节。
2. 指挥者是建造者模式中重要的类，用于控制建造过程，也可以隔离用户与建造过程的关联。
3. 建造者隐藏了产品的组装细节，若需要改变一个产品的内部表示，可以再定义一个具体的建造者。
4. 建造者模式是在当前创造复杂对象的算法，独立于该对象的组成部分和装配方式时适用的模式。

# 原型模式（Prototype）

1. 原型模式：用原型实例指定创建对象的种类，并通过拷贝这些原型创建对象。本质是从一个对象再创建另一个可定制的对象，并且不需要知道创建细节。
2. 原型抽象类的关键是有一个Clone()方法，原型具体类中复写Clone()创建当前对象的浅表副本。
3. 对.Net而言，由于拷贝太常用原型抽象类并不需要，在System命名空间中提供了ICloneable接口，其中唯一的方法就是Clone()，只要实现这个接口就可以完成原型模式。
4. 原型拷贝无需重新初始化对象，动态获取对象的运行状态。既隐藏了对象创建的细节，又提升性能。
5. 在具体原型类中，MemberwiseClone()方法是浅拷贝，对值类型字段诸位拷贝，对引用类型只复制引用但不会把具体的对象值拷贝过来。
6. 比起浅拷贝，深拷贝把引用对象的变量指向新对象，而不是原被引用的对象。对于需要深拷贝的每一层，都需要实现ICloneable原型模式。
7. 数据集对象DataSet，Clone()是浅拷贝，Copy()是深拷贝。

# 对比总结

- 工厂方法模式：为不同子类创建不同工厂；
- 抽象工厂模式：为不同系列建造不同工厂；
- 单例模式：保证实例唯一；
- 建造者模式：为不同类组装出一套相同的方法；
- 原型模式：实现深拷贝。
