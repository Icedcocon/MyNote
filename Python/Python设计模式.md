```python
#######################################################################
# 0 设计模式概念
#######################################################################

# 0.0 设计模式概念-面向对象
# 封装，隐藏内部实现
# 继承，复用现有代码
# 多态，改写对象行为

# 0.1 设计模式概念-接口
# (1) 接口类定义：接口类相比于普通类不支持实例化，仅包含抽象方法而不包含属性，实现
#     接口类的必须实现其中所有方法，标识一种has-a的关系，即拥有某种行为的概念。
# (2) 抽象类定义：抽象类相比于普通类不支持实例化，既包含方法也包含属性，子类继承抽
#     象类的属性和方法，其中子类必须覆盖实现抽象类的所有抽象方法。标识一种is-a的关
#     系，即属于某种东西的概念。
# (3) 作用
#  1) 限制实现接口的类必须按照接口给定的调用方式实现这些方法
#  2) 对高层模块隐藏了类的内部实现

# 0.2 设计模式概念-面向对象设计原则
# (1) 依赖倒置原则(DIP)
# (2) 开放封闭原则(OCP)
# (3) 单一职责原则(SRP)
# (4) Liskov替换原则(LSP)
# (5) 接口隔离原则(ISP)
# (6) 优先使用对象组合，而不是类继承
# (7) 封装变化点
# (8) 针对接口编程，而不是针对实现编程

# 0.2.1 设计模式概念-面向对象设计原则-依赖倒置原则(DIP)
# (1) 高层模块（稳定）不应该依赖于低层模块（变化），二者都应依赖于抽象（稳定）。
# (2) 抽象（稳定）不应该依赖于实现细节（变化），实现细节应应该依赖于抽象（稳定）。
# 要针对接口编程，而不是针对实现编程。
# MainForm -> Line、React
# MainForm -> Shape <- Line、React

# 0.2.2 设计模式概念-面向对象设计原则-开放封闭原则(OCP)
# (1) 对扩展开放，对更改封闭
# (2) 类模块应该是可扩展的，但是不可修改。
# MainForm(+Circle) -> Line、React + Circle 
# MainForm -> Shape <- Line、React + Circle

# 0.2.3 设计模式概念-面向对象设计原则-单一职责原则(SRP)
# (1) 一个类应该仅有一个引起它变化的原因。
# (2) 变化的方向隐含着类的责任。

# 0.2.4 设计模式概念-面向对象设计原则-Liskov替换原则(LSP)
# (1) 子类必须能够替换它们的基类(IS-A)
# (2) 继承表达类型抽象。
# 不应该出现子类继承父类，却不会使用父类方法的情况
class User:
    def show_name(self):
        pass
class VIPUser(User):
    def show_name(self):
        pass
def show_user(user: User):
    res = user.show_name()
show_user(VIPUser())

# 0.2.5 设计模式概念-面向对象设计原则-接口隔离原则(ISP)
# (1) 不应该强迫客户程序依赖它们不用的方法。
# (2) 接口应该小而完备。
# 仅在内部使用的方法(private)不要暴露给外部(public)
from abc import ABCMeta, abstractmethod
class LandAnimal(metaclass=ABCMeta):
    @abstractmethod
    def walk(self):
        pass
class WaterAnimal(metaclass=ABCMeta):
    @abstractmethod
    def swim(self):
        pass
class SkyAnimal(metaclass=ABCMeta):
    @abstractmethod
    def fly(self):
        pass
class Tiger(LandAnimal):
    def walk(self):
        print('老虎走路') 
class Frog(LandAnimal, WaterAnimal):
    pass

# 0.2.6 设计模式概念-面向对象设计原则-优先使用对象组合，而不是类继承
# (1) 类继承通常为“白箱复用”，对象组合通常为“黑箱复用”
# (2) 继承在某种程度上破坏了封装性，子类父类耦合度高
# (3) 而对象组合则只要求被组合的对象具有良好定义的接口耦合度低。
# class A 内部含有 class B

# 0.2.7 设计模式概念-面向对象设计原则-封装变化点
# (1) 使用封装来创建对象之间的分界层，让设计者可以在分界层的一侧进行修改，
# (2) 而不会对另一侧产生不良的影响，从而实现层次间的松耦合。

# 0.2.8 设计模式概念-面向对象设计原则-针对接口编程，而不是针对实现编程
# (1) 不将变量类型声明为某个特定的具体类，而是声明为某个接口
# (2) 客户程序无需获知对象的具体类型，只需要知道对象所具有的接口。
# (3) 减少系统中各部分的依赖关系，从而实现"高内聚、松耦合"的类型设计方案。


# 0.3.1 设计模式概念-设计模式分类-从目的、范围来看
# 从目的来看:
# (1) 创建型（Creational）模式：将对象的部分创建工作延迟到子类或者其他对象
#     从而应对需求变化为对象创建时具体类型实现引来的冲击。
# (2) 结构型（Structural）模式：通过类继承或者对象组合获得更灵活的结构，从
#     而应对需求变化为对象的结构带来的冲击。
# (3) 行为型（Behavioral）模式：通过类继承或者对象组合来划分类与对象间的职
#     责，从而应对需求变化为多个交互的对象带来的冲击
# 从范围来看：
# (1) 类模式处理类与子类的静态关系。
# (2) 对象模式处理对象间的动态关系。

# 0.3.1 设计模式概念-设计模式分类-从封装变化角度对模式分类
# (1) 组件协作
#  1) Template Method
#  2) Observer Event
#  3) Strategy
# (2) 单一职责
#  1) Decorator
#  2) Bridge
# (3) 对象创建：
#  1) Factory Method
#  2) Abstract Factory
#  3) Prototype
#  4) Builder
# (4) 对象性能：
#  1) Singleton
#  2) Flyweight
# (5) 接口隔离：
#  1) Facade
#  2) Proxy
#  3) Mediator
#  4) Adapter
# (6) 状态变化：
#  1) Memento
#  2) State
# (7) 数据结构：
#  1) Composite
#  2) Iterator
#  3) Chain of Resposibility
# (8) 行为变化：
#  1) Command
#  2) Visitor
# (9) 领域问题：
#  1) Interpreter

# 0.4 设计模式概念-类图
# 0.4.0 设计模式概念-类图-6中关系
# (1) 泛化：实线空心箭头：继承关系，存在于父类与子类、父接口与子接口(父类、子类)
# (2) 实现：虚线空心箭头：对应于类和接口之间的关系(接口类、类)
# (3) 依赖：虚线实心箭头：一个类的变化对依赖于它的类产生影响的情况(属性、友元)
# (4) 关联：实线实心箭头：描述了类的结构之间的关系，语义较弱(指针、引用)。
# (5) 聚合：实线空心菱形：特殊关联关系，指明一个聚集（整体）和组成部分之间的关系
# (6) 组合：实线实心菱形：语义更强的聚合，部分和整体具有相同的生命周期

# 0.4.1 设计模式概念-类图-泛化关系
# (1) 定义：B类继承了A类则A和B存在泛化关系，它是依赖关系的特例
# (2) 图例：实线空心箭头
# (3) 泛化关系例子(指向基类)
#  1) A <|-- B    A类是B类的基类/父类

# 0.4.2 设计模式概念-类图-实现关系
# (1) 定义：接口类A中的虚函数由B类实现，则B实现A，是依赖关系的特例
# (2) 图例：虚线空心箭头
# (3) 实现关系例子(实现指向接口)
#  1) B ..|> A  B类实现A的接口的关系

# 0.4.3 设计模式概念-类图-依赖关系
# (1) 定义：在类中用到了对方则存在依赖关系;如果没有对方，则编译不能通过;
# (2) 图例：虚线实心箭头
# (3) 依赖关系例子(指向被依赖方)
#  1) A ..> B    B类是A类的成员属性
#  2) A ..> B    B类是A类的方法的返回类型
#  3) A ..> B    B类是A类方法中的参数类型
#  4) A ..> B    A类方法中用到B类

# 0.4.4 设计模式概念-类图-关联关系
# (1) 定义：类与类之间的联系，类通过联系可访问另一个类的属性和方法，是依赖关系的特例
#          关联具有导航性,双向关系、单向关系、自关联;一对一、一对多、多对多
#          两个类是互相独立的，这两个类可以单独存在
# (2) 图例：实线实心箭头
# (3) 实现关系(指向被依赖方)
#  1) A --> B  A类知道/可以使用B类，但B类可以不存在/未定义

# 0.4.5 设计模式概念-类图-聚合关系
# (1) 定义：聚合关系表示的是整体与部分之间的关系，整体与部分可以分开;
#          聚合关系是关联关系的特例，所以它具有关联的导航性和多重性
# (2) 图例：实线空心菱形
# (3) 实现关系(部分指向整体)
#  1) A o-- B  A类由B类组成，但B类可以不存在

# 0.4.6 设计模式概念-类图-组合关系
# (1) 定义：组合关系也是整体与部分的关系，但是整体与部分不可以分开;
#          聚合关系是关联关系的特例，所以它具有关联的导航性和多重性
# (2) 图例：实线实心菱形
# (3) 实现关系(部分指向整体)
#  1) A *-- B  A类由B类组成，但B类必须存在
#  2) A *-- B  A类删除，B类也被删除(级联删除)
```

```python
#######################################################################
# 1 组件协作
#######################################################################
# 1.1 组件协作-模板方法
# 1.1.1 组件协作-模板方法-概念
# (1) 某一项任务有稳定的整体操作结构，但各步骤有很多改变的需求
#     或由于固有原因（如框架与应用）无法和任务整体结构同时实现
# (2) 定义算法骨架（稳定的操作流程），将一些步骤延迟到子类中。
#     使得子类不改变算法操作结构即可重定义该算法的某些特定步骤
# (3) 例子
#     1 -> (2) -> 3 -> (4) -> 5
#  1) 结构化软件设计流程
#     Library开发人员:      (1)开发1、3、5三个步骤
#     Application开发人员:  (1)开发2、4两个步骤;(2)程序主流程
#  1) 面向对象软件设计流程
#     Library开发人员:      (1)开发1、3、5三个步骤;(2)程序主流程
#     Application开发人员:  (1)开发2、4两个步骤

# 1.1.2 组件协作-模板方法-实现
# (1) 角色：
#  1) 抽象类（Abstract Class）：定义抽象的原子操作（钩子操作）；
#                             实现一个模板方法作为算法的骨架
#  2) 具体类（Concrete Class）：实现原子操作
# (2) 适用场景：
#  1) 一次性实现一个算法的不变的部分
#  2) 各子类的公共行为应被提取并集中到公共父类中,以避免代码重复
#  3) 控制子类扩展
# (3) 代码
from abc import ABCMeta, abstractmethod
import time
# 抽象类
class Window(metaclass=ABCMeta):
    @abstractmethod   # (1) Application开发人员实现，通常为protect
    def start(self):
        pass
    @abstractmethod   # (1)
    def repaint(self):
        pass
    @abstractmethod   # (1)
    def stop(self):
        pass
    def run(self):    # (2) Library开发人员实现程序主流程
        self.start()
        while 1:
            try:
                self.repaint()
                time.sleep(1)
            except KeyboardInterrupt:
                break
        self.stop()
# 具体类
class MyWindow(Window):
    def __init__(self, msg):
        self.msg = msg
    def start(self):      # (1)
        print('窗口开始运行...')
    def repaint(self):    # (1)
        print(self.msg)
    def stop(self):       # (1)
        print('窗口结束运行...')
# Client
MyWindow('Hello World!').run() # (3) 通常直接执行主流程而无需操作步骤 

# 1.2 组件协作-策略模式
# 1.2.1 组件协作-策略模式-概念
# (1) 对象使用的算法经常改变，将算法编码到对象中会使对象变得异常复杂；
#     而且有时候支持不使用的算法也是一个性能负担。
# (2) 定义一系列算法，并把它们逐个封装，使它们可互相替换（变化）;
#     该模式使得算法可独立于使用它的客户程序(稳定)而变化（扩展，子类化）


# 1.2.2 组件协作-策略模式-实现
# (1) 角色：
#  1) 抽象策略（Strategy）
#  2) 具体策略（Concrete Strategy）
#  3) 上下文（Context）
# (2) 适用场景：
#  1) 优点：定义了一系列可重用的算法和行为;消除了一些条件语句;
#          可以提供相同行为的不同实现
#  2) 缺点：客户必须了解不同的策略
# (3) 代码
from abc import ABCMeta, abstractmethod
# 抽象策略
class Strategy(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, data):
        pass
# 具体策略
class FastStrategy(Strategy): # (1) 继承父类结合引用实现互相替换(多态)
    def execute(self, data):
        print('快速执行策略%s' % data)
class SlowStrategy(Strategy): # (1)
    def execute(self, data):
        print('慢速执行策略%s' % data)
# 上下文
class Context:
    def __init__(self, strategy, data):
        self.strategy = strategy
        self.data = data
    def set_strategy(self, strategy):
        self.strategy = strategy
    def execute_strategy(self):
        self.strategy.execute(self.data)
# Client
s1 = FastStrategy()
s2 = SlowStrategy()
data = '[...]'
context = Context(s1, data)
context.set_strategy(s2)
context.execute_strategy()


# 1.3 组件协作-观察者模式
# 1.3.1 组件协作-观察者模式-概念
# (1) 一个对象（目标）的状态发生改变，所有的依赖对象（观察者）都将得到通知;
#     一个对象的改变需要同时改变其它对象，而不知道具体有多少对象有待改变;
#     当一个抽象模型有两方面，其中一个方面依赖于另一个方面;
#     一个对象必须通知其它对象，而它又不能假定其它对象是谁（松耦合）;
# (2) 定义对象间的一种一对多的依赖关系;观察者模式又称“发布-订阅”模式;

# 1.3.2 组件协作-观察者模式-实现
# (1) 角色：
#  1) 抽象主题（Subject）                    提供添加/删除观察者和通知功能
#  2) 具体主题/发布者（Concrete Subject）     实现具体信息
#  3) 抽象观察者（Observer）                  提供更新（观察）发布者信息功能
#  4) 具体观察者/订阅者（Concrete Observer）  实现更新（观察）发布者信息功能
# (2) 优缺点：
#  1) 优点：目标和观察者之间的抽象耦合最小;
#          支持广播通信;
# (3) 代码
from abc import ABCMeta, abstractmethod
# 抽象订阅者
class Observer(metaclass=ABCMeta):
    @abstractmethod
    def update(self, notice):
        pass
# 抽象发布者
class Notice:
    def __init__(self):
        self.observers = []
    def attach(self, obs):
        self.observers.append(obs)
    def detach(self, obs):
        self.observers.remove(obs)
    def notify(self):
        for obs in self.observers:
            obs.update(self)
# 具体发布者
class StaffNotice(Notice):
    def __init__(self, company_info=None):
        super().__init__()
        self.__company_info = company_info
    @property
    def company_info(self):
        return self.__company_info
    @company_info.setter
    def company_info(self, info):
        self.__company_info = info
# 具体订阅者
class Staff(Observer):
    def __init__(self):
        self.company_info = None
    def update(self, notice):
        self.company_info = notice.company_info
if __name__ == "__main__":
    company = StaffNotice('今天休息！')
    s1 = Staff()
    s2 = Staff()
    company.attach(s1)
    company.attach(s2)
    company.notify()
    print(s1.company_info) # 今天休息！
    print(s2.company_info) # 今天休息！

# 1.4 组件协作-装饰器模式
# 1.4.1 组件协作-装饰器模式-概念
# (1) 防止过度地使用继承来扩展对象的功能
#     继承为类型引入的静态特质缺乏灵活
#      随子类(扩展功能)增多，各子类的组合(扩展功能的组合)会导致子类的膨胀
# (2) 在不影响其他对象的情况下，以动态、透明的方式给单个对象添加职责
#      处理那些可以撤销的职责
# (3) 通过采用组合而非继承的手法，Decorator模式实现了在运行时动态扩展对象功能的能力，而且可以根据需要扩展多个功能。避免了使用继承带来的“灵活性差”和“多子类衍生问题”。
2.Decorator类在接口上表现为is-a Component的继承关系，即 Decorator类继承了Component类所具有的接口。但在实现上又 表现为has-a Component的组合关系，即Decorator类又使用了另外一个Component类。
3.Decorator模式的目的并非解决“多子类衍生的多继承”问题，Decorator模式应用的要点在于解决“主体类在多个方向上的扩展功能”——是为“装饰”的含义。

# 1.4.2 组件协作-装饰器模式-实现
# (1) 角色：
#  1) 抽象组件（Component）               抽象方法
#  2) 具体组件（Concrete Component）      具体方法
#  3) 抽象装饰器（Decorator）             继承抽象组件(泛化);引用抽象组件(组合)
#										调用抽象组件方法
#  4) 具体装饰器（ Concrete Decorator）   具体装饰函数
# (2) 优缺点：
#  1) 优点：比静态继承更灵活;
#          避免在层次结构高层的类有太多的特征;
# (3) 代码
import gzip
from io import BytesIO
class LogSocket:
    def __init__(self, socket):
        self.socket = socket
    def send(self, data):
        print("Sending {0} to {1}".format(
            data, self.socket.getpeername()[0]))
        self.socket.send(data)
    def close(self):
        self.socket.close()
class GzipSocket:
    def __init__(self, socket):
        self.socket = socket
    def send(self, data):
        buf = BytesIO()
        zipfile = gzip.GzipFile(fileobj=buf, mode="w")
        zipfile.write(data)
        zipfile.close()
        self.socket.send(buf.getvalue())
    def close(self):
        self.socket.close()
if __name__ == "__main__":
    client, addr = server.accept()
    if log_send:
        client = LoggingSocket(client)
    if client.getpeername()[0] in compress_hosts:
        client = GzipSocket(client)
    respond(client)
```
