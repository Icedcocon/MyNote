# Python 对象模型概述

## 一切皆对象

首先，在 *Python* 世界， **基本类型也是对象** ，与通常意义的“对象”形成一个有机统一。 换句话讲， *Python* 不再区别对待基本类型和对象，所有基本类型内部均由对象实现。 一个整数是一个对象，一个字符串也是一个对象：

```python
>>> a = 1
>>> b = 'abc'
```

其次， *Python* 中的 **类型也是一种对象** ，称为 **类型对象** 。 整数类型是一个对象，字符串类型是一个对象，程序中通过 *class* 关键字定义的类也是一个对象。

举个例子，整数类型在 *Python* 内部是一个对象，称为 **类型对象** ：

```python
>>> int
<class 'int'>
```

通过整数类型 **实例化** 可以得到一个整数对象，称为 **实例对象** ：

```python
>>> int('1024')
1024
```

面向对象理论中的“ **类** ”和“ **对象** ”这两个基本概念，在 *Python* 内部都是通过对象实现的，这是 *Python* 最大的特点。

![图片描述](https://img1.sycdn.imooc.com/5eb905d50001f78f05540232.png)

## 类型、对象体系

*a* 是一个整数对象( **实例对象** )，其类型是整数类型( **类型对象** )：

```python
>>> a = 1
>>> type(a)
<class 'int'>
>>> isinstance(a, int)
True
```

那么整数类型的类型又是什么呢？

```python
>>> type(int)
<class 'type'>
```

可以看到，整数类型的类型还是一种类型，即 **类型的类型** 。 只是这个类型比较特殊，它的实例对象还是类型对象。

*Python* 中还有一个特殊类型 *object* ，所有其他类型均继承于 *object* ，换句话讲 *object* 是所有类型的基类：

```python
>>> issubclass(int, object)
True
```

综合以上关系，得到以下关系图：

![图片描述](https://img1.sycdn.imooc.com/5eb906470001efa107020273.png)

Python类型系统-1

内置类型已经搞清楚了，自定义类型及对象关系又如何呢？定义一个简单的类来实验：

```python
class Dog(object):

    def yelp(self):
        print('woof')
```

创建一个 *Dog* 实例，毫无疑问，其类型是 *Dog* ：

```python
>>> dog = Dog()
>>> dog.yelp()
woof
>>> type(dog)
<class '__main__.Dog'>
```

*Dog* 类的类型自然也是 *type* ，其基类是 *object* (就算不显式继承也是如此)：

```python
>>> type(Dog)
<class 'type'>
>>> issubclass(Dog, object)
True
```

![图片描述](https://img1.sycdn.imooc.com/5eb9068100010b3505790327.png)

Python类型系统-2

自定义子类及实例对象在图中又处于什么位置？定义一个猎犬类进行实验：

```python
class Sleuth(Dog):

    def hunt(self):
        pass
```

可以看到， 猎犬对象( *sleuth* )是猎犬类( *Sleuth* )的实例， *Sleuth* 的类型同样是 *type* ：

```python
>>> sleuth = Sleuth()
>>> sleuth.hunt()
>>> type(sleuth)
<class '__main__.Sleuth'>
>>> type(Sleuth)
<class 'type'>
```

同时， *Sleuth* 类继承自 *Dog* 类，是 *Dog* 的子类，当然也是 *object* 的子类：

```python
>>> issubclass(Sleuth, Dog)
True
>>> issubclass(Sleuth, object)
True
```

![图片描述](https://img1.sycdn.imooc.com/5eb906d10001d5c205930417.png)

Python类型系统-3

现在不可避免需要讨论 *type* 以及 *object* 这两个特殊的类型。

理论上， *object* 是所有类型的 **基类** ，本质上是一种类型，因此其类型必然是 *type* 。 而 *type* 是所有类型的类型，本质上也是一种类型，因此其类型必须是它自己！

```python
>>> type(object)
<class 'type'>
>>> type(object) is type
True

>>> type(type)
<class 'type'>
>>> type(type) is type
True
```

另外，由于 *object* 是所有类型的 **基类** ，理论上也是 *type* 的基类( *__base__* 属性)：

```python
>>> issubclass(type, object)
True
>>> type.__base__
<class 'object'>
```

但是 *object* 自身便不能有基类了。为什么呢？ 对于存在继承关系的类，成员属性和成员方法查找需要回溯继承链，不断查找基类。 因此，继承链必须有一个终点，不然就死循环了。

![图片描述](https://img1.sycdn.imooc.com/5eb907270001a34e06200413.png)

Python类型系统 (4)

这就完整了！

可以看到，所有类型的基类收敛于 *object* ，所有类型的类型都是 *type* ，包括它自己！ 这就是 *Python* 类型、对象体系全图，设计简洁、优雅、严谨。

该图将成为后续阅读源码、探索 *Python* 对象模型的有力工具，像地图一样指明方向。 图中所有实体在 *Python* 内部均以对象形式存在，至于对象到底长啥样，相互关系如何描述，这些问题先按下不表，后续一起到源码中探寻答案。

## 变量只是名字

先看一个例子，定义一个变量 *a* ，并通过 *id* 内建函数取出其“地址”：

```python
>>> a = 1
>>> id(a)
4302704784
```

定义另一个变量 *b* ，以 *a* 赋值，并取出 *b* 的“地址”：

```python
>>> b = a
>>> id(b)
4302704784
```

惊奇地看到， *a* 和 *b* 这两个变量的地址居然是相同的！这不合常理呀！

对于大多数语言( *C* 语言为例)，定义变量 *a* 即为其分配内存并存储变量值：

![图片描述](https://img1.sycdn.imooc.com/5eb9077f00012a6201980149.png)

变量 *b* 内存空间与 *a* 独立，赋值时进行拷贝：

![图片描述](https://img1.sycdn.imooc.com/5eb907a00001900603960222.png)

在 *Python* 中，一切皆对象，整数也是如此， **变量只是一个与对象关联的名字** ：

![图片描述](https://img1.sycdn.imooc.com/5eb907cb000145b502760202.png)

而变量赋值，只是将当前对象与另一个名字进行关联，背后的对象是同一个：

![图片描述](https://img1.sycdn.imooc.com/5ec604ff0001bd9005280243.png)

因此，在 *Python* 内部，变量只是一个名字，保存指向实际对象的指针，进而与其绑定。 变量赋值只拷贝指针，并不拷贝指针背后的对象。

## 可变对象 与 不可变对象

定义一个整数变量：

```python
>>> a = 1
>>> id(a)
4302704784
```

然后，对其自增 *1* ：

```python
>>> a += 1
>>> a
2
>>> id(a)
4302704816
```

数值符合预期，但是对象变了！初学者一脸懵逼，这是什么鬼？

一切要从 **可变对象** 和 **不可变对象** 说起。 **可变对象** 在对象创建后，其值可以进行修改； 而 **不可变对象** 在对象创建后的整个生命周期，其值都不可修改。

在 *Python* 中，整数类型是不可变类型， 整数对象是不可变对象。 修改整数对象时， *Python* 将以新数值创建一个新对象，变量名与新对象进行绑定； 旧对象如无其他引用，将被释放。

![图片描述](https://img1.sycdn.imooc.com/5eb907f3000158d515770254.png)

> 每次修改整数对象都要创建新对象、回收旧对象，效率不是很低吗？ 确实是。 后续章节将从源码角度来解答： *Python* 如何通过 **小整数池** 等手段进行优化。

可变对象是指创建后可以修改的对象，典型的例子是 **列表** ( *list* )：

```python
>>> l = [1, 2]
>>> l
[1, 2]
>>> id(l)
4385900424
```

往列表里头追加数据，发现列表对象还是原来那个，只不过多了一个元素了：

```python
>>> l.append(3)
>>> l
[1, 2, 3]
>>> id(l)
4385900424
```

实际上，列表对象内部维护了一个 **动态数组** ，存储元素对象的指针：

![图片描述](https://img1.sycdn.imooc.com/5eb9081500014c4106410445.png)

列表对象增减元素，需要修改该数组。例如，追加元素 *3* ：

![图片描述](https://img1.sycdn.imooc.com/5eb90831000191b206460508.png)

## 定长对象 与 变长对象

*Python* 一个对象多大呢？相同类型对象大小是否相同呢？ 想回答类似的问题，需要考察影响对象大小的因素。

标准库 *sys* 模块提供了一个查看对象大小的函数 *getsizeof* ：

```python
>>> import sys
>>> sys.getsizeof(1)
28
```

先观察整数对象：

```python
>>> sys.getsizeof(1)
28
>>> sys.getsizeof(100000000000000000)
32
>>> sys.getsizeof(100000000000000000000000000000000000000000000)
44
```

可见整数对象的大小跟其数值有关，像这样 **大小不固定** 的对象称为 **变长对象** 。

我们知道，位数固定的整数能够表示的数值范围是有限的，可能导致 **溢出** 。 *Python* 为解决这个问题，采用类似 *C++* 中 **大整数类** 的思路实现整数对象—— 串联多个普通 *32* 位整数，以便支持更大的数值范围。 至于需要多少个 *32* 位整数，则视具体数值而定，数值不大的一个足矣，避免浪费。

![图片描述](https://img1.sycdn.imooc.com/5eb9085700019c1604270215.png)

这样一来，整数对象需要在头部额外存储一些信息，记录对象用了多少个 *32* 位整数。 这就是变长对象典型的结构，先有个大概印象即可，后续讲解整数对象源码时再展开。

接着观察字符串对象：

```python
>>> sys.getsizeof('a')
50
>>> sys.getsizeof('abc')
52
```

![图片描述](https://img1.sycdn.imooc.com/5eb9087f0001314404180225.png)

字符串对象也是变长对象，这个行为非常好理解，毕竟字符串长度不尽相同嘛。 此外，注意到字符串对象大小比字符串本身大，因为对象同样需要维护一些额外的信息。 至于具体需要维护哪些信息，同样留到源码剖析环节中详细介绍。

那么，有啥对象是定长的呢？——浮点数对象 *float* ：

```python
>>> sys.getsizeof(1.)
24
>>> sys.getsizeof(1000000000000000000000000000000000.)
24
```

浮点数背后是由一个 *double* 实现，就算表示很大的数，浮点数对象的大小也不变。

![图片描述](https://img1.sycdn.imooc.com/5eb9089d000172d804280177.png)

为啥 *64* 位的 *double* 可以表示这么大的范围呢？答案是：牺牲了精度。

```python
>>> int(1000000000000000000000000000000000.)
999999999999999945575230987042816
```

由于浮点数存储位数是固定的，它能表示的数值范围也是有限的，超出便会抛锚：

```python
>>> 10. ** 1000
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
OverflowError: (34, 'Result too large')
```

# 揭开对象神秘的面纱

面向对象理论中“ **类** ”和“ **对象** ”这两个重要概念，在 *Python* 内部均以对象的形式存在。 “类”是一种对象，称为 **类型对象** ；“类”实例化生成的“对象”也是对象，称为 **实例对象** 。

根据对象不同特点还可进一步分类：

| **类别** | **特点**    |
| ------ | --------- |
| 可变对象   | 对象创建后可以修改 |
| 不可变对象  | 对象创建后不能修改 |
| 定长对象   | 对象大小固定    |
| 变长对象   | 对象大小不固定   |

那么，对象在 *Python* 内部到底长啥样呢？

由于 *Python* 是由 *C* 语言实现的，因此 *Python* 对象在 *C* 语言层面应该是一个 **结构体** ，组织对象占用的内存。 不同类型的对象，数据及行为均可能不同，因此可以大胆猜测：不同类型的对象由不同的结构体表示。

对象也有一些共性，比如每个对象都需要有一个 **引用计数** ，用于实现 **垃圾回收机制** 。 因此，还可以进一步猜测：表示对象的结构体有一个 **公共头部** 。

到底是不是这样呢？——接下来在源码中窥探一二。

## PyObject，对象的基石

在 *Python* 内部，对象都由 *PyObject* 结构体表示，对象引用则是指针 *PyObject* * 。 *PyObject* 结构体定义于头文件 *object.h* ，路径为 *Include/object.h* ，代码如下：

```c
typedef struct _object {
    _PyObject_HEAD_EXTRA
    Py_ssize_t ob_refcnt;
    struct _typeobject *ob_type;
} PyObject;
```

除了 *_PyObject_HEAD_EXTRA* 宏，结构体包含以下两个字段：

- **引用计数** ( ob_refcnt )
- **类型指针** ( ob_type )

**引用计数** 很好理解：对象被其他地方引用时加一，引用解除时减一； 当引用计数为零，便可将对象回收，这是最简单的垃圾回收机制。 **类型指针** 指向对象的 **类型对象** ，**类型对象** 描述 **实例对象** 的数据及行为。

回过头来看 *_PyObject_HEAD_EXTRA* 宏的定义，同样在 *Include/object.h* 头文件内：

```c
#ifdef Py_TRACE_REFS
/* Define pointers to support a doubly-linked list of all live heap objects. */
#define _PyObject_HEAD_EXTRA            \    struct _object *_ob_next;           \    struct _object *_ob_prev;

#define _PyObject_EXTRA_INIT 0, 0,

#else
#define _PyObject_HEAD_EXTRA
#define _PyObject_EXTRA_INIT
#endif
```

如果 *Py_TRACE_REFS* 有定义，宏展开为两个指针，看名字是用来实现 **双向链表** 的：

```c
struct _object *_ob_next;
struct _object *_ob_prev;
```

结合注释，双向链表用于跟踪所有 **活跃堆对象** ，一般不启用，不深入介绍。

对于 **变长对象** ，需要在 *PyObject* 基础上加入长度信息，这就是 *PyVarObject* ：

```c
typedef struct {
    PyObject ob_base;
    Py_ssize_t ob_size; /* Number of items in variable part */
} PyVarObject;
```

变长对象比普通对象多一个字段 *ob_size* ，用于记录元素个数：

![图片描述](https://img1.sycdn.imooc.com/5eb908c40001a82807410317.png)

定长对象变长对象

至于具体对象，视其大小是否固定，需要包含头部 *PyObject* 或 *PyVarObject* 。 为此，头文件准备了两个宏定义，方便其他对象使用：

```c
#define PyObject_HEAD          PyObject ob_base;
#define PyObject_VAR_HEAD      PyVarObject ob_base;
```

例如，对于大小固定的 **浮点对象** ，只需在 *PyObject* 头部基础上， 用一个 **双精度浮点数** *double* 加以实现：

```c
typedef struct {
    PyObject_HEAD

    double ob_fval;
} PyFloatObject;
```

![*![PyFloatObject.svg]()*](https://img1.sycdn.imooc.com/5eb909050001651a03630270.png)

而对于大小不固定的 **列表对象** ，则需要在 *PyVarObject* 头部基础上， 用一个动态数组加以实现，数组存储列表包含的对象，即 *PyObject* 指针：

```c
typedef struct {
    PyObject_VAR_HEAD

    PyObject **ob_item;
    Py_ssize_t allocated;
} PyListObject;
```

![图片描述](https://img1.sycdn.imooc.com/5eb9092600013a1e10680535.png)

如图， *PyListObject* 底层由一个数组实现，关键字段是以下 *3* 个：

- *ob_item* ，指向 **动态数组** 的指针，数组保存元素对象指针；
- *allocated* ，动态数组总长度，即列表当前的 **容量** ；
- *ob_size* ，当前元素个数，即列表当前的 **长度** ；

列表容量不足时， *Python* 会自动扩容，具体做法在讲解 *list* 源码时再详细介绍。

最后，介绍两个用于初始化对象头部的宏定义。 其中，*PyObject_HEAD_INIT* 一般用于 **定长对象** ，将引用计数 *ob_refcnt* 设置为 *1* 并将对象类型 *ob_type* 设置成给定类型：

```c
#define PyObject_HEAD_INIT(type)        \    { _PyObject_EXTRA_INIT              \    1, type },
```

*PyVarObject_HEAD_INIT* 在 *PyObject_HEAD_INIT* 基础上进一步设置 **长度字段** *ob_size* ，一般用于 **变长对象** ：

```c
#define PyVarObject_HEAD_INIT(type, size)       \    { PyObject_HEAD_INIT(type) size },
```

后续在研读源码过程中，将经常见到这两个宏定义。

## PyTypeObject，类型的基石

在 *PyObject* 结构体，我们看到了 *Python* 中所有对象共有的信息。 对于内存中的任一个对象，不管是何类型，它刚开始几个字段肯定符合我们的预期： **引用计数** 、 **类型指针** 以及变长对象特有的 **元素个数** 。

随着研究不断深入，我们发现有一些棘手的问题没法回答：

- 不同类型的对象所需内存空间不同，创建对象时从哪得知内存信息呢？
- 对于给定对象，怎么判断它支持什么操作呢？

对于我们初步解读过的 *PyFloatObject* 和 *PyListObject* ，并不包括这些信息。 事实上，这些作为对象的 **元信息** ，应该由一个独立实体保存，与对象所属 **类型** 密切相关。

注意到， *PyObject* 中包含一个指针 *ob_type* ，指向一个 **类型对象** ，秘密就藏在这里。类型对象 *PyTypeObject* 也在 *Include/object.h* 中定义，字段较多，只讨论关键部分：

```c
typedef struct _typeobject {
    PyObject_VAR_HEAD
    const char *tp_name; /* For printing, in format "<module>.<name>" */
    Py_ssize_t tp_basicsize, tp_itemsize; /* For allocation */

    /* Methods to implement standard operations */
    destructor tp_dealloc;
    printfunc tp_print;

    getattrfunc tp_getattr;
    setattrfunc tp_setattr;

    // ...
    /* Attribute descriptor and subclassing stuff */
    struct _typeobject *tp_base;

    // ......
} PyTypeObject;
```

可见 **类型对象** *PyTypeObject* 是一个 **变长对象** ，包含变长对象头部。 专有字段有：

- **类型名称** ，即 *tp_name* 字段；
- 类型的继承信息，例如 *tp_base* 字段指向基类对象；
- 创建实例对象时所需的 **内存信息** ，即 *tp_basicsize* 和 *tp_itemsize* 字段；
- 该类型支持的相关 **操作信息** ，即 *tp_print* 、 *tp_getattr* 等函数指针；

*PyTypeObject* 就是 **类型对象** 在 *Python* 中的表现形式，对应着面向对象中“**类**”的概念。 *PyTypeObject* 结构很复杂，但是我们不必在此刻完全弄懂它。 先有个大概的印象，知道 *PyTypeObject* 保存着对象的 **元信息** ，描述对象的 **类型** 即可。

接下来，以 **浮点** 为例，考察 **类型对象** 和 **实例对象** 在内存中的形态和关系：

```python
>>> float
<class 'float'>
>>> pi = 3.14
>>> e = 2.71
>>> type(pi) is float
True
```

*float* 为浮点类型对象，系统中只有唯一一个，保存了所有浮点实例对象的元信息。 而浮点实例对象就有很多了，圆周率 *pi* 是一个，自然对数 *e* 是另一个，当然还有其他。

代码中各个对象在内存的形式如下图所示：

![图片描述](https://img1.sycdn.imooc.com/5eb9094e0001808b08600605.png)

其中，两个浮点 **实例对象** 都是 *PyFloatObject* 结构体， 除了公共头部字段 *ob_refcnt* 和 *ob_type* ，专有字段 *ob_fval* 保存了对应的数值。 浮点 **类型对象** 是一个 *PyTypeObject* 结构体， 保存了类型名、内存分配信息以及浮点相关操作。 实例对象 *ob_type* 字段指向类型对象， *Python* 据此判断对象类型， 进而获悉关于对象的元信息，如操作方法等。 再次提一遍，*float* 、 *pi* 以及 *e* 等变量只是一个指向实际对象的指针。

由于浮点 **类型对象** 全局唯一，在 *C* 语言层面作为一个全局变量静态定义即可，*Python* 的确就这么做。 浮点类型对象就藏身于 *Object/floatobject.c* 中， *PyFloat_Type* 是也：

```c
PyTypeObject PyFloat_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "float",
    sizeof(PyFloatObject),
    0,
    (destructor)float_dealloc,                  /* tp_dealloc */

    // ...
    (reprfunc)float_repr,                       /* tp_repr */

    // ...
};
```

其中，第 *2* 行初始化 *ob_refcnt* 、 *ob_type* 以及 *ob_size* 三个字段； 第 3 行将 *tp_name* 字段初始化成类型名称 *float* ；再往下是各种操作的函数指针。

注意到 *ob_type* 指针指向 *PyType_Type* ，这也是一个静态定义的全局变量。 由此可见，代表“ **类型的类型** ” 即 *type* 的那个对象应该就是 *PyType_Type* 了。

## PyType_Type，类型的类型

我们初步考察了 *float* 类型对象，知道它在 *C* 语言层面是 *PyFloat_Type* 全局静态变量。 类型是一种对象，它也有自己的类型，也就是 *Python* 中的 *type* ：

```python
>>> float.__class__
<class 'type'>
```

自定义类型也是如此：

```python
>>> class Foo(object):
...     pass
...
>>> Foo.__class__
<class 'type'>
```

那么， *type* 在 *C* 语言层面又长啥样呢？

围观 *PyFloat_Type* 时，我们通过 *ob_type* 字段揪住了 *PyType_Type* 。 的确，它就是 *type* 的肉身。 *PyType_Type* 在 *Object/typeobject.c* 中定义：

```c
PyTypeObject PyType_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "type",                                     /* tp_name */
    sizeof(PyHeapTypeObject),                   /* tp_basicsize */
    sizeof(PyMemberDef),                        /* tp_itemsize */
    (destructor)type_dealloc,                   /* tp_dealloc */

    // ...
    (reprfunc)type_repr,                        /* tp_repr */

    // ...
};
```

内建类型和自定义类对应的 *PyTypeObject* 对象都是这个通过 *PyType_Type* 创建的。 *PyType_Type* 在 *Python* 的类型机制中是一个至关重要的对象，它是所有类型的类型，称为 **元类型** ( *meta class* )。 借助元类型，你可以实现很多神奇的高级操作。

注意到， *PyType_Type* 将自己的 *ob_type* 字段设置成它自己(第 *2* 行)，这跟我们在 *Python* 中看到的行为是吻合的：

```python
>>> type.__class__
<class 'type'>
>>> type.__class__ is type
True
```

至此，元类型 type 在对象体系里的位置非常清晰了：

![图片描述](https://img1.sycdn.imooc.com/5eb9097b0001168712620775.png)

## PyBaseObject_Type，类型之基

*object* 是另一个特殊的类型，它是所有类型的基类。 那么，怎么找到它背后的实体呢？ 理论上，通过 *PyFloat_Type* 中 *tp_base* 字段顺藤摸瓜即可。

然而，我们发现这个字段在并没有初始化：

```c
0,                                          /* tp_base */
```

这又是什么鬼？

接着查找代码中 *PyFloat_Type* 出现的地方，我们在 *Object/object.c* 发现了蛛丝马迹：

```c
if (PyType_Ready(&PyFloat_Type) < 0)
    Py_FatalError("Can't initialize float type");
```

敢情 *PyFloat_Type* 静态定义后还是个半成品呀！ *PyType_Ready* 对它做进一步加工，将 *PyFloat_Type* 中 *tp_base* 字段初始化成 *PyBaseObject_Type* ：

```c
int
PyType_Ready(PyTypeObject *type)
{
    // ...

    base = type->tp_base;
    if (base == NULL && type != &PyBaseObject_Type) {
        base = type->tp_base = &PyBaseObject_Type;
        Py_INCREF(base);
    }

    // ...
}
```

*PyBaseObject_Type* 就是 *object* 背后的实体，先一睹其真容：

```c
PyTypeObject PyBaseObject_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "object",                                   /* tp_name */
    sizeof(PyObject),                           /* tp_basicsize */
    0,                                          /* tp_itemsize */
    object_dealloc,                             /* tp_dealloc */

    // ...
    object_repr,                                /* tp_repr */
};
```

注意到， *ob_type* 字段指向 *PyType_Type* 跟 *object* 在 *Python* 中的行为时相吻合的：

```python
>>> object.__class__
<class 'type'>
```

又注意到 *PyType_Ready* 函数初始化 *PyBaseObject_Type* 时，不设置 *tp_base* 字段。 因为继承链必须有一个终点，不然对象沿着继承链进行属性查找时便陷入死循环。

```python
>>> print(object.__base__)
None
```

至此，我们完全弄清了 *Python* 对象体系中的所有实体以及关系，得到一幅完整的图画：

![图片描述](https://img1.sycdn.imooc.com/5eb909b30001ef4812470872.png)

虽然很多细节还没来得及研究，这也算是一个里程碑式的胜利！让我们再接再厉！

# 从创建到销毁，对象的生命周期

当我们在控制台敲下这个语句， *Python* 内部是如何从无到有创建一个浮点对象的？

```python
>>> pi = 3.14
```

另外，*Python* 又是怎么知道该如何将它打印到屏幕上的呢？

```python
>>> print(pi)
3.14
```

对象使用完毕， *Python* 必须将其销毁，销毁的时机又该如何确定呢？ 带着这些问题，接着考察对象在从创建到销毁整个生命周期中的行为表现，从中探寻答案。

以下讨论以一个足够简单的类型 *float* 为例，对应的 *C* 实体是 *PyFloat_Type* 。

## C API

开始讨论对象创建前，先介绍 *Python* 提供的 *C API* 。

*Python* 是用 *C* 写成的，对外提供了 *C API* ，让用户可以从 *C* 环境中与其交互。 *Python* 内部也大量使用这些 *API* ，为了更好研读源码，先系统了解 *API* 组成结构很有必要。 *C API* 分为两类： **泛型 API** 以及 **特型 API** 。

### 泛型 API

**泛型 API** 与类型无关，属于 **抽象对象层** ( *Abstract Object Layer* )，简称 *AOL* 。 这类 API 参数是 *PyObject** ，可处理任意类型的对象， *API* 内部根据对象类型区别处理。

以对象打印函数为例：

```c
int
PyObject_Print(PyObject *op, FILE *fp, int flags)
```

接口第一个参数为待打印对象，可以是任意类型的对象，因此参数类型是 *PyObject** 。 *Python* 内部一般都是通过 *PyObject** 引用对象，以达到泛型化的目的。

对于任意类型的对象，均可调用 *PyObject_Print* 将其打印出来：

```c
// 打印浮点对象
PyObject *fo = PyFloatObject_FromDouble(3.14);
PyObject_Print(fo, stdout, 0);

// 打印整数对象
PyObject *lo = PyFloatObject_FromLong(100);
PyObject_Print(lo, stdout, 0);
```

*PyObject_Print* 接口内部根据对象类型，决定如何输出对象。

### 特型 API

**特型 API** 与类型相关，属于 **具体对象层** ( *Concrete Object Layer* )，简称 *COL* 。 这类 *API* 只能作用于某种类型的对象，例如浮点对象 *PyFloatObject* 。 *Python* 内部为每一种内置对象提供了这样一组 *API* ，举例如下：

```c
PyObject *
PyFloat_FromDouble(double fval)
```

*PyFloat_FromDouble* 创建一个浮点对象，并将它初始化为给定值 *fval* 。

## 对象的创建

经过前面的理论学习，我们知道对象的 **元数据** 保存在对应的 **类型对象** 中，元数据当然也包括 **对象如何创建** 的信息。 因此，有理由相信 **实例对象** 由 **类型对象** 创建。

不管创建对象的流程如何，最终的关键步骤都是 **分配内存** 。 *Python* 对 **内建对象** 是无所不知的，因此可以提供 *C API* ，直接分配内存并执行初始化。 以 *PyFloat_FromDouble* 为例，在接口内部为 *PyFloatObject* 结构体分配内存，并初始化相关字段即可。

对于用户自定义的类型 *class Dog(object)* ， *Python* 就无法事先提供 *PyDog_New* 这样的 *C API* 了。 这种情况下，就只能通过 *Dog* 所对应的类型对象创建实例对象了。 至于需要分配多少内存，如何进行初始化，答案就需要在 **类型对象** 中找了。

总结起来，*Python* 内部一般通过这两种方法创建对象：

- 通过 *C API* ，例如 *PyFloat_FromDouble* ，多用于内建类型；
- 通过类型对象，例如 *Dog* ，多用于自定义类型；

通过类型对象创建实例对象，是一个更通用的流程，同时支持内置类型和自定义类型。 以创建浮点对象为例，我们还可以通过浮点类型 *PyFloat_Type* 来创建：

```python
>>> pi = float('3.14')
>>> pi
3.14
```

例子中我们通过调用类型对象 *float* ，实例化了一个浮点实例 *pi* ，对象居然还可以调用！在 *Python* 中，可以被调用的对象就是 **可调用对象** 。

问题来了，可调用对象被调用时，执行什么函数呢？ 由于类型对象保存着实例对象的元信息， *float* 类型对象的类型是 *type* ，因此秘密应该就隐藏在 *type* 中。

再次考察 *PyType_Type* ，我们找到了 *tp_call* 字段，这是一个函数指针：

```c
PyTypeObject PyType_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "type",                                     /* tp_name */
    sizeof(PyHeapTypeObject),                   /* tp_basicsize */
    sizeof(PyMemberDef),                        /* tp_itemsize */

    // ...
    (ternaryfunc)type_call,                     /* tp_call */

    // ...
};
```

当实例对象被调用时，便执行 *tp_call* 字段保存的处理函数。

因此， *float(‘3.14’)* 在 *C* 层面等价于：

```c
PyFloat_Type.ob_type.tp_call(&PyFloat_Type, args, kwargs)
```

即：

```c
PyType_Type.tp_call(&PyFloat_Type, args, kwargs)
```

最终执行， type_call 函数：

```c
type_call(&PyFloat_Type, args, kwargs)
```

调用参数通过 *args* 和 *kwargs* 两个对象传递，先不展开，留到函数机制中详细介绍。

接着围观 *type_call* 函数，定义于 *Include/typeobject.c* ，关键代码如下：

```c
static PyObject *
type_call(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyObject *obj;

    // ...
    obj = type->tp_new(type, args, kwds);
    obj = _Py_CheckFunctionResult((PyObject*)type, obj, NULL);
    if (obj == NULL)
        return NULL;

    // ...
    type = Py_TYPE(obj);
    if (type->tp_init != NULL) {
        int res = type->tp_init(obj, args, kwds);
        if (res < 0) {
            assert(PyErr_Occurred());
            Py_DECREF(obj);
            obj = NULL;
        }
        else {
            assert(!PyErr_Occurred());
        }
    }
    return obj;
}
```

可以看到，关键的步骤有两个：

1. 调用类型对象 *tp_new* 函数指针 **申请内存** (第 *7* 行)；
2. 必要时调用类型对象 *tp_init* 函数指针对对象进行 **初始化** (第 *15* 行)；

至此，对象的创建过程已经非常清晰了：

![图片描述](https://img1.sycdn.imooc.com/5eba86170001db7f11440939.png)

总结一下，*float* 类型对象是 **可调用对象** ，调用 *float* 即可创建实例对象：

1. 调用 *float* ， *Python* 最终执行其类型对象 *type* 的 *tp_call* 函数；
2. *tp_call* 函数调用 *float* 的 *tp_new* 函数为实例对象分配 **内存空间** ；
3. *tp_call* 函数必要时进一步调用 *tp_init* 函数对实例对象进行 **初始化** ；

## 对象的多态性

*Python* 创建一个对象，比如 *PyFloatObject* ，会分配内存，并进行初始化。 此后， *Python* 内部统一通过一个 *PyObject** 变量来保存和维护这个对象，而不是通过 *PyFloatObject** 变量。

通过 *PyObject** 变量保存和维护对象，可以实现更抽象的上层逻辑，而不用关心对象的实际类型和实现细节。 以对象哈希值计算为例，假设有这样一个函数接口：

```c
Py_hash_t
PyObject_Hash(PyObject *v);
```

该函数可以计算任意对象的哈希值，不管对象类型是啥。 例如，计算浮点对象哈希值：

```c
PyObject *fo = PyFloatObject_FromDouble(3.14);
PyObject_Hash(fo);
```

对于其他类型，例如整数对象，也是一样的：

```c
PyObject *lo = PyLongObject_FromLong(100);
PyObject_Hash(lo);
```

然而，对象类型不同，其行为也千差万别，哈希值计算方法便是如此。 *PyObject_Hash* 函数如何解决这个问题呢？ 到 *Object/object.c* 中寻找答案：

```c
Py_hash_t
PyObject_Hash(PyObject *v)
{
    PyTypeObject *tp = Py_TYPE(v);
    if (tp->tp_hash != NULL)
        return (*tp->tp_hash)(v);
    /* To keep to the general practice that inheriting    * solely from object in C code should work without    * an explicit call to PyType_Ready, we implicitly call    * PyType_Ready here and then check the tp_hash slot again    */
    if (tp->tp_dict == NULL) {
        if (PyType_Ready(tp) < 0)
            return -1;
        if (tp->tp_hash != NULL)
            return (*tp->tp_hash)(v);
    }
    /* Otherwise, the object can't be hashed */
    return PyObject_HashNotImplemented(v);
}
```

函数先通过 *ob_type* 指针找到对象的类型 (第 *4* 行)； 然后通过类型对象的 *tp_hash* 函数指针，调用对应的哈希值计算函数 (第 *6* 行)。 换句话讲， *PyObject_Hash* 根据对象的类型，调用不同的函数版本。 这不就是 **多态** 吗？

通过 *ob_type* 字段， *Python* 在 *C* 语言层面实现了对象的 **多态** 特性， 思路跟 *C++* 中的 **虚表指针** 有异曲同工之妙。

## 对象的行为

不同对象的行为不同，比如哈希值计算方法就不同，由类型对象中 *tp_hash* 字段决定。 除了 *tp_hash* ，我们看到 *PyTypeObject* 结构体还定义了很多函数指针，这些指针最终都会指向某个函数，或者为空。 这些函数指针可以看做是 **类型对象** 中定义的 **操作** ，这些操作决定对应 **实例对象** 在运行时的 **行为** 。

尽管如此，不同对象也有一些共性。 举个例子，**整数对象** 和 **浮点对象** 都支持加减乘除等 **数值型操作** ：

```python
>>> 1 + 2
3
>>> 3.14 * 3.14
9.8596
```

**元组对象** *tuple* 和 **列表对象** *list* 都支持下标操作：

```python
>>> t = ('apple', 'banana', 'car', 'dog')
>>> t[-1]
'dog'
>>> l = ['alpha', 'beta']
>>> l[-1]
'beta'
```

因此，以对象行为为依据，可以对对象进行分类：

![图片描述](https://img1.sycdn.imooc.com/5eba86080001a71a03740288.png)

*Python* 便以此为依据，为每个类别都定义了一个 **标准操作集** ：

- *PyNumberMethods* 结构体定义了 **数值型** 操作；
- *PySequenceMethods* 结构体定义了 **序列型** 操作；
- *PyMappingMethods* 结构体定义了 **关联型** 操作；

只要 **类型对象** 提供相关 **操作集** ， **实例对象** 便具备对应的 **行为** 。 操作集字段如下：

```c
typedef struct _typeobject {
    PyObject_VAR_HEAD
    const char *tp_name; /* For printing, in format "<module>.<name>" */
    Py_ssize_t tp_basicsize, tp_itemsize; /* For allocation */

    // ...
    /* Method suites for standard classes */

    PyNumberMethods *tp_as_number;
    PySequenceMethods *tp_as_sequence;
    PyMappingMethods *tp_as_mapping;

    // ...
    /* Functions to access object as input/output buffer */
    PyBufferProcs *tp_as_buffer;

    // ...
} PyTypeObject;
```

以 *float* 为例，类型对象 *PyFloat_Type* 相关字段是这样初始化的：

```c
static PyNumberMethods float_as_number = {
    float_add,          /* nb_add */
    float_sub,          /* nb_subtract */
    float_mul,          /* nb_multiply */
    float_rem,          /* nb_remainder */
    float_divmod,       /* nb_divmod */
    float_pow,          /* nb_power */
    // ...
};

PyTypeObject PyFloat_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "float",
    sizeof(PyFloatObject),

    // ...
    &float_as_number,                           /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */

    // ...
};
```

- 字段 *tp_as_number* 非空，因此 *float* 对象 **支持数值型操作** ；
- 字段 *tp_as_sequence* 为空，因此 *float* 对象 **不支持序列型操作** ；
- 字段 *tp_as_mapping* 为空，因此 *float* 对象 **不支持关联型操作** ；

注意到， *float_as_number* 变量中相关函数指针都初始化为对应的 *float* 版本操作函数。 由于篇幅有限，这里先不深入展开。

## 引用计数

*C/C++* 赋予程序员极大的自由，可以任意申请内存，并按自己的意图灵活管理。 然而，权利的另一面则对应着 **责任** ，一旦内存不再使用，程序员必须将其释放。 这给程序员带来极大的 **工作负担** ，并导致大量问题： **内存泄露** 、 **野指针** 、 **越界访问** 等。

许多后来兴起的开发语言，如 *Java* 、 *Golang* 等，选择 **由语言本身负责内存的管理** 。 **垃圾回收机制** 的引入，程序员摆脱了内存管理的噩梦，可以更专注于业务逻辑。 于此同时，开发人员失去了灵活使用内存的机会，也牺牲了一定的执行效率。

随着垃圾回收机制日益完善，可在大部分对性能要求不苛刻的场景中引入，利大于弊。 *Python* 也采用垃圾回收机制，代替程序员进行繁重的内存管理，**提升开发效率** 的同时，降低 *bug* 发生的几率。

*Python* 垃圾回收机制的关键是对象的 **引用计数** ，它决定了一个对象的生死。 我们知道每个 *Python* 对象都有一个 *ob_refcnt* 字段，记录着对象当前的引用计数。 当对象被其他地方引用时， *ob_refcnt* 加一； 当引用解除时， *ob_refcnt* 减一。 当 *ob_refcnt* 为零，说明对象已经没有任何引用了，这时便可将其回收。

*Python* 对象创建后，引用计数设为 *1* ：

```python
>>> a = 3.14
>>> sys.getrefcount(a)
2
```

咦？这里引用计数为啥是 *2* 呢？

对象作为函数参数传递，需要将引用计数加一，避免对象被提前销毁；函数返回时，再将引用计数减一。 因此，例子中 *getrefcount* 函数看到的对象引用计数为 *2* 。

接着，变量赋值让对象多了一个引用，这很好理解：

```python
>>> b = a
>>> sys.getrefcount(a)
3
```

将对象放在容器对象中，引用计数也增加了，符合预期：

```python
>>> l = [a]
>>> l
[3.14]
>>> sys.getrefcount(a)
4
```

我们将 *b* 变量删除，引用计数减少了：

```python
>>> del b
>>> sys.getrefcount(a)
3
```

接着，将列表清空，引用计数进一步下降：

```python
>>> l.clear()
>>> sys.getrefcount(a)
2
```

最后，将变量 *a* 删除后，引用计数降为 *0* ，便不复存在了：

```python
>>> del a
```

在 *Python* 中，很多场景都涉及引用计数的调整，例如：

- 容器操作；
- 变量赋值；
- 函数参数传递；
- 属性操作；

为此， *Python* 定义了两个非常重要的宏，用于维护对象应用计数。 其中， *Py_INCREF* 将对象应用计数加一 ( *3* 行)：

```c
#define Py_INCREF(op) (                         \    _Py_INC_REFTOTAL  _Py_REF_DEBUG_COMMA       \    ((PyObject *)(op))->ob_refcnt++)
```

*Py_DECREF* 将引用计数减一 ( *5* 行)，并在引用计数为 *0* 是回收对象 ( *8* 行)：

```c
#define Py_DECREF(op)                                   \    do {                                                \        PyObject *_py_decref_tmp = (PyObject *)(op);    \        if (_Py_DEC_REFTOTAL  _Py_REF_DEBUG_COMMA       \        --(_py_decref_tmp)->ob_refcnt != 0)             \            _Py_CHECK_REFCNT(_py_decref_tmp)            \        else                                            \            _Py_Dealloc(_py_decref_tmp);                \    } while (0)
```

当一个对象引用计数为 *0* ， *Python* 便调用对象对应的析构函数销毁对象，但这并不意味着对象内存一定会回收。 为了提高内存分配效率， *Python* 为一些常用对象维护了内存池， 对象回收后内存进入内存池中，以便下次使用，由此 **避免频繁申请、释放内存** 。

**内存池** 技术作为程序开发的高级话题，需要更大的篇幅，放在后续章节中介绍。





参考资料： [06 小试牛刀，解剖浮点对象 float-慕课专栏](https://www.imooc.com/read/76/article/1902)
