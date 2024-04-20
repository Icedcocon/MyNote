## 0 前言

### 0.1 什么是 Type hints

Type hints 即类型提示，是 Python 在 3.5 版本中加入的语法，并在 Python 3.6 基本可用。在此后的版本中，Type hints 的功能不断扩充，至今已经能够实现一个比较完善的静态类型系统。下面的代码是一个示例。

```python3
def sum_nums(nums: list[int]) -> int:
    result: int = 0
    for num in nums:
        result += num
    return result
```

正如其名称暗示的那样，Type hints 是“类型提示”而不是“类型检查”，Python 并**不会**在程序运行时检查你所标注的类型与变量的真实类型是否一致——如果不一致，也并不会产生错误。Type hints 最大的作用是在编辑器中对代码进行**静态**类型检查，以方便你发现因类型不一致而导致的潜在运行时错误，并增强你代码的重构能力，以提升代码的可维护性。对于大型项目而言，这格外有价值——但即便在小型项目中，Type hints 也具有足够的意义。

> **✨ 提示：**如果你自身对静态类型一无所知，那么 Python 的 Type hints 可能并不适合成为你接触的第一个静态类型系统——当然，你可以试着读下去，看看自己能接受多少。本文假设你有一些基本的、与包含静态类型系统的编程语言打交道的经历，如 Go、Java、C++ 或 TypeScript，否则你可能会发现本文的后半部分并不容易理解。

在大多数时候，你并不需要刻意为使用 Type hints 而做什么配置——编辑器或 IDE 通常提供了开箱即用的 Type hints 支持，如 VSCode 默认使用 [Pyright](https://link.zhihu.com/?target=https%3A//github.com/microsoft/pyright) (Pylance) 提供支持，PyCharm 则使用[其内置的 Type hints 支持](https://link.zhihu.com/?target=https%3A//www.jetbrains.com/help/pycharm/type-hinting-in-product.html)。

> **➡️ 补充：**VSCode 实际使用 [Pylance](https://link.zhihu.com/?target=https%3A//marketplace.visualstudio.com/items%3FitemName%3Dms-python.vscode-pylance) 为 Python 提供支持，而 Pyright 是其中的核心组件，作为 Python 的静态类型检查器 (Staic type checker) 发挥作用，因此如果你使用 VSCode，会看到一些有关类型的提示信息来自 Pylance 而非 Pyright.

Python 官方提供了 [mypy](https://link.zhihu.com/?target=https%3A//mypy-lang.org/) 作为静态类型检查器（可通过 pip 安装）。mypy 的优势在于其支持插件系统，因此一些项目可能依赖于 mypy 提供更进一步的类型支持。在大部分编辑器或 IDE 中，mypy 并不作为其默认使用的静态类型检查器（由于 mypy 的性能较差，并且对新 Type hints 特性的支持较慢），你可能需要安装相应的插件来使用它。不过，由于 mypy 的官方性，许多开源项目仍倾向于优先保证在 mypy 下正常工作，而非 Pyright 或 PyCharm 内置的 Type hints 支持。另外，mypy 也常常被认为是最准确的静态类型检查工具，例如在一些边界情况下 Pyright 的推导可能产生问题，在 mypy 上则很少见——当然，通常来说你不需要担心此类问题。

*本文不会介绍 mypy 等工具的使用，但 [Fluent Python, 2nd Edition, Chapter 8](https://link.zhihu.com/?target=https%3A//learning.oreilly.com/library/view/fluent-python-2nd/9781492056348/ch08.html) 中对 mypy 有比较详细的介绍。*

尽管 Type hints 通常用于提供静态类型检查，但运行时实际上能够读取一部分 Type hints 信息，因此有一些工具如 [FastAPI](https://link.zhihu.com/?target=https%3A//fastapi.tiangolo.com/) 与 [Pydantic](https://link.zhihu.com/?target=https%3A//docs.pydantic.dev/latest/) 也利用 Type hints 提供运行时类型校验能力。由于这一运行时行为，添加 Type hints 有时会给你的 Python 代码带来一些微小的性能损耗，只是它们常常可以忽略不计——相比起它们带来的好处来说。

如果你熟悉其他编程语言（如 Java 或 TypeScript）中的泛型编程概念，可以尝试理解以下这段代码，它演示了 `map` 函数对 List 的特化版本——如果你不理解也没关系，这其中的知识点都会在后续被详细解读：

```python3
from typing import Callable

def map_list[T, U](func: Callable[[T], U], lst: list[T]) -> list[U]:
    return [func(x) for x in lst]
```

下图展示了 VSCode 中 Pyright 对它的静态类型检查支持（错误提示来自于 [Error Lens](https://link.zhihu.com/?target=https%3A//marketplace.visualstudio.com/items%3FitemName%3Dusernamehw.errorlens) 插件）：

![](https://pic4.zhimg.com/80/v2-2a23dcc1d3bcaeb66272d211613b2377_1440w.webp)

——以及对泛型类的支持：

```python3
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Maybe[T]:
    value: T | None

    def map[U](self, func: Callable[[T], U]) -> "Maybe[U]":
        if self.value is None:
            return Maybe(None)
        return Maybe(func(self.value))
```

![](https://pic2.zhimg.com/80/v2-39be9c28341b8f1900347c03aac2c525_1440w.webp)

### 0.2 为什么需要 Type hints？

一个常见的误解是，如果我只使用 Python 编写小脚本或只是用来画一些图表，Type hints 对我来说就没有什么用——然而实际上，“使用 Type hints”与“不使用 Type hints”不是唯二的两种选择，你可以选择仅在必要的时候加上一点 Type hints 来方便自己（与编辑器）理解代码，而不是在所有能加上 Type hints 的地方都加上它们——这也没有必要。

其中一个用处是告知编辑器某个函数参数的类型，以获得由此带来的智能提示，如下图所示。这不会带来什么负担，却能极大提升你编写代码的体验：

![](https://pic1.zhimg.com/80/v2-2a61cac0e8e4d9347aab30eb614b5438_1440w.webp)

如果你安装的某个第三方库也自带了合适的 Type hints，那么编辑器也能从中推导出更多信息以提供更精准的智能提示。即使某个第三方库并未使用 Type hints 编写，也可能由其他作者为其编写合适的 Type hints，并以 `type-xxx` 的名称发布在 PyPI 上供他人下载安装，以帮助编辑器提供更智能的提示——Python 官方维护着一个名为 [typeshed](https://link.zhihu.com/?target=https%3A//github.com/python/typeshed) 的项目，已经为相当多流行的第三方库提供了合适的 Type hints，如 [six](https://link.zhihu.com/?target=https%3A//github.com/benjaminp/six) 和 [requests](https://link.zhihu.com/?target=https%3A//github.com/psf/requests).

![](https://pic2.zhimg.com/80/v2-4f61491b484d0d5aba147fd08993bf19_1440w.webp)

typeshed 主页上的相关描述

当然，如果你通常使用 Python 编写小脚本、进行数据科学工作或是构建人工智能模型，那么使用 Type hints 或许没有想象中的有效，也不一定需要了解它。但如果你正在使用 Python 开发软件或是构建其他大型项目，那么使用 Type hints 能够使你享受静态类型带来的一部分优势，使重构变得更加便利，也能更好地减少代码中因类型不一致产生的潜在运行时错误。

不过，Python 的本质仍是动态类型语言，因此**没有必要追求 100% 的类型提示**，这反而失去了动态类型的优势，陷入了思维定势中——并且实际上目前的 Type hints 并不足以百分百兼容 Python 的灵活性，仍有不少场景是 Type hints 无法很好表示的。

如果你在使用 Type hints 的过程中没有感受到任何便利，或是已经通过大量的单元测试确保了你的 Python 代码已经能覆盖大多数情况，那么使用 Type hints 就不是完全必要的——这理所应当。

> **➡️ 说明：**本文有部分示例来自于 [Fluent Python, 2nd Edition](https://link.zhihu.com/?target=https%3A//learning.oreilly.com/library/view/fluent-python-2nd/9781492056348) 与 Type hints 相关的章节（第 8 章和第 15 章），其余示例大部分为原创，剩余来自 Python 官方文档。目前该书已由人民邮电出版社图灵教育出版，中译名为《流畅的 Python（第 2 版）》，我个人很推荐阅读一下原书——不过，该书中关于 Type hints 的部分也存在不少错漏和疏忽，读的时候建议稍微谨慎一些。

## 1 基础语法

### 1.1 开始

首先不使用 Type Hints 实现函数 `show_count`，返回一个包含数量和名词的单数/复数形式的字符串：

```python3
>>> show_count(99, 'bird')
'99 birds'
>>> show_count(1, 'bird')
'1 bird'
>>> show_count(0, 'bird')
'no bird'
```

这是它的源码：

```python3
def show_count(count, word):
    if count == 1:
        return f'1 {word}'
    count_str = str(count) if count else 'no'
    return f'{count_str} {word}s'
```

下面为它加上 Type Hints：

```python3
def show_count(count: int, word: str) -> str:
    if count == 1:
        return f'1 {word}'
    count_str = str(count) if count else 'no'
    return f'{count_str} {word}s'
```

Python 的 Type Hints 不仅支持基本类型，如`int`, `float`, `str`……也支持自定义的类型。例如：

```python3
class Bird:
    def fly(self):
        ...

def bird_fly(bird: Bird) -> None:
    bird.fly()
```

### 1.2 默认参数及 `Optional`

我们上面定义的 `show_count` 函数还存在一些问题。比如 mouse 的复数是 mice，但这个函数只会返回“mouses”而不是“mice”。于是我们为这里的 `show_count` 函数加上了默认参数：

```python3
def show_count(count: int, singular: str, plural: str = '') -> str:
    if count == 1:
        return f'1 {word}'
    if not plural:
        plural = singular + 's'
    return f'{count_str} {plural}'
```

> **✨ 提示：**根据 [PEP 8 的相关建议](https://link.zhihu.com/?target=https%3A//peps.python.org/pep-0008/%23variable-annotations)，在不使用 Type Hints 时，默认参数的等号两边应该**没有**空格，而使用 Type Hints 时，则建议在等号两边**加上**空格。这或许有些违背你的直觉，但 PEP 8 的确如此规定，而本文的代码也遵照此规范。

但是这里的默认参数只是个特殊情况。有时我们需要使用 `None` 作为默认参数，*特别是在默认参数可变的情况下*，将 `None` 作为默认参数几乎是唯一的选择。

> ✨ **提示：**关于为什么“使用可变值作为默认参数是危险的”，将在本小节的最后进行补充。

那么，需要将 `None` 作为默认值时该怎么做呢？在 Python 3.10+ 中，建议使用 `| None` 用于表示其类型也可以是 `None`，这是联合类型（Union type）的语法，将在下一小节介绍：

```python3
def show_count(count: int, singular: str, plural: str | None = None) -> str:
    ...

>>> show_count(2, 'child', 'children')
'2 children'
>>> show_count(1, 'mouse', 'mice')
'1 mouse'
```

在更早的 Python 版本中，你可以使用 `Optional[...]` 作为替代：

```python3
from typing import Optional

def show_count(count: int, singular: str, plural: Optional[str] = None) -> str:
    ...
```

> ✨ **提示：**“Optional”这个名称具有一定的迷惑性——在 Python 中，我们经常说某一个函数参数是“可选 (Optional)”的，以表示某一个函数参数可以被传递或者不传递。然而这里的 `Optional[...]` 却仅仅表示某个变量的类型可以是 `None`，而其本身却并不具有“可选”的含义。因此在这里你仍需要写成 `plural: Optiona[str] = None` 而不是 `plural: Optional[str]`，这里的 `= None` 并不能被省略——你可以理解为 Type hints 在运行时会被忽略，因此它们通常不具备运行时作用，所以你仍**不能省略这里的 `= None`**. 当然，在 Python 3.10+ 中，你更应该使用前一种语法而不是 `Optional[...]`，这样更容易避免这个名称所带来的迷惑性。

> ➡️ **补充：**为什么使用可变值作为默认参数是危险 ⚠️ 的：

```python3
>>> def func(arg=[]):
...     return arg
...
>>> func()
[]
>>> lst = func()
>>> lst.append(0)
>>> func()
[0]

# 更好的方法是使用 `None` 作为默认值
def func(arg=None):
    if arg is None:
        arg = []
    return arg
```

### 1.3 联合类型 (Union Type)

有时候函数可能有不同类型的返回值，甚至参数也是不同类型的。这时可以使用联合类型语法，即使用竖线 `|` 分隔类型：

```python3
def parse_token(token: str) -> str | float:
    try:
        return float(token)
    except ValueError:
        return token
```

`|` 操作符同样支持 isinstance 和 issubclass 函数：

```python3
isinstance(x, int | str | tuple)
```

需要注意的是，仅 Python 3.10+ 支持该语法，如果你需要在更早的版本中使用联合类型，你需要从 `typing` 中导入 `Union`：

```python3
from typing import Union

def parse_token(token: str) ->  Union[str, float]: ...
```

`Union` 支持多个类型与嵌套。例如以下的两种用法是等价的：

```python3
Union[A, B, Union[C, D, E]]
Union[A, B, C, D, E]
```

下面的代码将全部使用 `|` 而不是 `Union` 作演示。然而 `|` 用作联合类型是 Python 3.10 才加入的，因此记得在 Python 3.9 及以前的版本，仍然需要使用 `Union`。

> ➡️ **补充：关于“一致性 (consistency)”**  
> 在此处，有必要在本文中第一次普及“一致性 (consistency)”的概念，以便于接下来的讲解。这一知识可能并不容易理解——但没有关系，如果你暂时无法理解下面这段话，可以在之后阅读第 2 节中的“理解结构化类型/鸭子类型”以深入理解它。  
> 如果你希望编写一个函数，它能够同时处理 `int`、`float` 和 `complex`，如 `def print_num(num)`，你可能认为将其类型标为 `def print_num(num: int | float | complex) -> None` 是个好主意——然而实际上这是冗余的，你只需要标注为 `def print_num(num: complex) -> None` 就可以了。  
> 要理解这个问题，首先要理解“一致性 (consistency)”的概念。在 Python 中，`int` 与 `float` 是相一致（consistent-with）的，而 `float` 与 `complex` 也是相一致的，因此可接受 `float` 的地方实际也可接受 `int`，而可接受 `complex` 的地方实际也可以接受 `int` 或 `float`。反过来则不行，比如接受 `float` 的地方不可以接受 `complex`，接受 `int` 的地方也不可以接受 `float`.  
> 这是因为 `int` 类型实现了 `float` 类型的所有方法，而 `float` 类型又实现了 `complex` 类型的所有方法。比如 `int` 除了实现了 `float` 类型上常规的减乘除等运算外，还额外实现了整数上才能使用的 `&`、`|`、`<<` 等位运算。  
> 同理，`int` 和 `float` 实际上也实现了 `complex` 的所有方法。你可以曾认为 `.imag`、`.real` 是`complex` 类型上独有的属性，但你实际上也可以在 `int` 和 `float` 上调用这两个属性，例如 `i = 3, i.real` 是 `3`，`i.imag` 则是 `0`.  
> 你或许感到这里“相一致（consistent-with）”的概念有些类似于继承，你可以不太严谨地这么理解。然而实际上 `int`、`float` 和 `complex` 这三个类型都继承自 `object`，它们之间并没有真正的继承关系。

```python3
# 下面的写法是冗余
def print_num(num: int | float | complex) -> None:
    print(num)

# ……它实际上与下面的定义等价
def print_num(num: complex) -> None:
    print(num)
```

### 1.4 类型别名 (Type Alias)

除联合类型外，也可以为类型命名，这被称为“类型别名（Type Alias）”。在 Python 3.12+，你可以使用 `type` 关键字轻松创建一个类型别名：

```python3
type Hexadecimal = str | int

def hex_to_ascii_string(hex: Haxdecimal) -> str:
    ...

# 上面的代码与以下代码是等价的
def hex_to_ascii_string(hex: str | int) -> str:
    ...
```

——不过事实上，使用 `type` 创建类型别名并不是完全必要的。你也可以省略 `type`，直接创建类型别名：

```python3
Hexadecimal = str | int
```

如果你使用早于 Python 3.12 的版本，`type` 关键字还不被支持，你便只能这样写。然而尽管 `type` 似乎不是必要的，仍建议在 Python 3.12+ 中明确写出 `type`，这更清晰地表明了你只是在定义一个类型别名，而不是某个运行时使用的变量。

除了定义简单的类型别名，`type` 关键字还用于更方便地处理泛型定义——如果你暂时不理解泛型也没关系，这会在之后详述：

```python3
type ListOrSet[T] = list[T] | set[T]
```

如果你在使用 Python 3.10~3.11，但也希望能够像 Python 3.12+ 一样明确表示你在定义一个类型别名，你也可以使用 `TypeAlias` 类型，这更加清晰。不过不像 `type` 关键字，使用 `TypeAlias` 最大的作用只是使你的类型别名更清晰并且更容易被静态类型检查器发现：

```python3
Hexadecimal: TypeAlias = str | int
```

在第 1.16 节，会简单介绍 `TypeAlias` 的另一个作用，即避免前向引用类型的别名与值为特定字符串的变量混淆——但无论怎么说，`TypeAlias` 的功能都已经被新引入的 `type` 关键字完全覆盖了，并且在 Python 3.12 中被标记为了废弃 (Deprecated)，所以在 Python 3.12+ 中建议尽可能使用 `type` 关键字。

更多关于 Python 3.12 引入的 `type` 关键字的信息，可以参考 [PEP 695 – Type Parameter Syntax 的相关部分](https://link.zhihu.com/?target=https%3A//peps.python.org/pep-0695/%23generic-type-alias)。

关于 Python 3.10 引入的 `TypeAlias` 的更多信息，可以参考 [PEP 613 – Explicit Type Aliases](https://link.zhihu.com/?target=https%3A//peps.python.org/pep-0613/).

### 1.5 子类型 (`NewType`)

有时候，你会愿意创建类型别名以增强代码可读性：

```python3
type Second = float
type Millisecond = float
type Microsecond = float

def sleep(duration: Second) -> None:
    ...
```

在这里，你通过为 `float` 起类型别名 `Second` 表明了 `sleep` 函数应当接收一个以秒为单位的时间长度。因此，通常你希望用户这样调用它：

```python3
sleep(1.5)  # 休眠 1.5 秒
```

只是这并不能阻止粗心的用户将这里的时间单位当作毫秒。如果用户这么调用它，显然也不会产生错误：

```python3
sleep(1500)  # 试图休眠 1.5 秒，实际休眠了 1500 秒
```

毕竟类型别名只是**别名**，它与原本的类型没有区别。它能起到一定的文档作用，让你的代码更加易读，却不能使静态类型检查器施加更严格的约束。这时，你可能更希望创建“子类型 (Subtype)”，使用户更明确地认识到函数的作用：

```python3
from typing import NewType

Second = NewType("Second", float)
Millisecond = NewType("Millisecond", float)
Microsecond = NewType("Microsecond", float)

def sleep(duration: Second) -> None:
    ...

sleep(1.5)  # 错误: `float` 不是 `Second` 类型
sleep(Millisecond(1.5))  # 错误: `Millisecond` 不是 `Second` 类型
sleep(Second(1.5))  # 正确
```

如你所见，通过 `NewType` 创建了 `float` 的三个子类型 `Second`、`Millisecond` 以及 `Microsecond`. 现在 `sleep` 函数只接收 `Second` 类型，而不能接收 `float`、`Millisecond` 或 `Microsecond`. 这和继承关系有些相似，若指定使用子类型，则不能使用父类型。

在用户 ID 这样的场景下使用 `NewType` 定义子类型可能是个不错的主意：

```python3
from typing import NewType

UserId = NewType("UserId", int)
some_id = UserId(524313)


def get_user_name(user_id: UserId) -> str:
    ...


# 正确
user_a = get_user_name(UserId(42351))

# 错误: `int` 不是 `UserId`
user_b = get_user_name(-1)
```

自然，你也可以继续通过上面定义的 `UserId` 派生新的子类型：

```python3
from typing import NewType

UserId = NewType("UserId", int)

ProUserId = NewType("ProUserId", UserId)
```

然而，通过 `NewType` 定义的子类型不是一个真正的“子类”，它无法通过 class 关键字进行继承：

```python3
from typing import NewType

UserId = NewType("UserId", int)

# 错误: `UserId` 被标记为 final，无法被继承
# 这也会导致运行时错误
class AdminUserId(UserId):
    ... 
```

然而，值得注意的是通过 `NewType` 定义的子类型可执行的操作仍与父类型完全相同。例如即使上面定义了 `UserId` 类型，将两个 `UserId` 相加后得到的结果仍是 `int` 类型：

```python3
# output是 `int` 类型，而非 `UserId` 类型
output = UserId(23413) + UserId(54341)
```

### 1.6 强制类型转换 (Type Casting)

静态类型检查器通常能够理解你的意图——但自然也有些时候它无法正确推导出你预期的类型，因此总需要一种方案来让你手动告诉类型检查器某个变量的类型，这就是“**强制类型转换 (Type Casting)**”的存在价值。

如果你曾与任何一门具有静态类型系统的编程语言打过交道，可能早就熟悉这个概念了。现在让我们看个例子：

```python3
def find_first_str(lst: list[object]) -> str:
    idx = next(i for i, x in enumerate(lst) if isinstance(x, str))
    return lst[idx]
```

你可能暂时不熟悉这里 `list[object]` 的语法，没关系，这在之后会详细解释——但你应当能从直觉里察觉出它表示一个由 `object` 组成的列表。这段代码在逻辑上是没有问题的，只要没有发生异常，它返回的 `lst[idx]` 显然一定是个字符串。

然而静态类型检查器并不能在如此复杂的情况下理解发生了什么。它会报告一个错误：

![](https://pic4.zhimg.com/80/v2-43ac36d398bcc9b2dd0de05a2a572f2b_1440w.webp)

为此，你可以使用 `typing.cast` 强制转换某个值的类型，例如这里将 `lst[idx]` 强制转换为 `str` 以消除错误：

```python3
from typing import cast

def find_first_str(lst: list[object]) -> str:
    idx = next(i for i, x in enumerate(lst) if isinstance(x, str))
    return cast(str, lst[idx])
```

![](https://pic1.zhimg.com/80/v2-04e75909e20f0e4e4bdceaa4c539cb04_1440w.webp)

你可能会疑虑 `cast` 是否会对运行时造成性能影响，实际上几乎不会。这是它的代码实现：

```python3
def cast(typ, val):
    """将一个值转换为某个类型.
    该函数会原样返回值。对于类型检查器来说，这是一个标志，
    表示返回值已经被转换成了指定的类型。但在运行时，我们
    希望该函数不会进行任何类型检查（因为我们希望这个函数
    能够尽可能快）
    """
    return val
```

可以看到，`cast` 只是作为一个标记，它并不在运行时产生任何作用，只是将传入的值原样返回。因此显然它也不会在运行时真正转换值的类型，只是为静态类型检查器提供了提示。

一般只建议在此类编辑器无法正确推导类型，但代码逻辑正确无误的情况下使用 `cast`，而不建议使用 `cast` 故意忽略类型检查器报告的某些潜在运行时错误。通常来说，你不需要过多使用 `cast`，类型检查器一般有足够的能力进行正确推导，仅极少数情况下无法正确理解代码含义。

*虽说如此，如果涉及一些复杂的函数重载和泛型情况，的确得经常使用 `cast`，毕竟 Python 的类型系统还算不得健壮，在处理复杂问题时并不足够智能。此外，许多第三方库也没有包含正确的 Type hints，以至于在一些检查器的严格模式下你常常需要大量使用 `cast` 来避免类型检查器的抱怨……*

### 1.7 `Any` 类型

有时你会发现自己并不能明确表示某个值的类型，此时你可以使用 `Any`，表示任意类型：

```python3
from typing import Any

# 这里先不考虑为该函数标注返回值
def double(x: Any):
    return 2 * x
```

显然，这里的 x 可以是很多类型，例如 `int`、`float` 甚至 `np.uint32` 这样的数字类型，又或者是 `tuple`、`list` 或是 `pd.Series` 这样的序列类型。所以这里使用了 `Any` 类型，因为输入值有很多可能。

在 mypy 中，任何未标注类型的变量、函数参数、函数返回值等被认为是 `Any` 类型，即使通过 `strict_optional` 选项开启了严格类型检查也是如此。例如在 mypy 中，因此下面两段代码是等价的（此处使用了 mypy 进行类型检查，而非 Pyright）：

```python3
from typing import Any

def double(x):
    return 2 * x

def double(x: Any) -> Any:
    return 2 * x
```

![](https://pic4.zhimg.com/80/v2-206ec97b7318eeab64ace6af1f7a87df_1440w.webp)

因此通常来说，你可以认为标注 `Any` 的意义不是很大——这其实就相当于没有标注类型。并且，**有些时候显式标注 `Any` 反而会降低静态类型检查器的推导能力**，使得原本能够推导出更精确类型的地方仅仅被推导为了 `Any`. 下图展示了这种情况：

![](https://pic3.zhimg.com/80/v2-07116650405974ce557b81c7917d54fe_1440w.webp)

`Any` 实际上“**逃避**”了静态类型检查器的类型检查——这是一种独特的类型，假如一个变量的类型是 `Any`，那么任何值都能被赋值给它，同时它也能被赋值给任何类型的变量。我个人建议在任何情况下都不要显式使用 `Any`，除非你的目的就是为了故意使静态类型检查器在某个地方不要理你。

——事实上，如果你希望表示一个值可能是某个**未知**类型，使用 `object` 可能是个更安全的选择，它是 Python 中所有类型的基类，因此很适合这种情况。通过使用 `object`，你能够更好地保证类型安全，并获得至少一部分编辑器的智能提示：

```python3
def parse_string(string: str) -> object:
    ...
```

![](https://pic4.zhimg.com/80/v2-624d69d96004af44febf99396080520f_1440w.webp)

你可能注意到了，我在上面特意提到 mypy 将未标注类型的函数参数与返回值视为 `Any` 类型，但并非所有静态类型检查器都这样工作——VSCode 默认使用的 Pyright 就不是。事实上，Pyright 将未知参数的类型推导为 `Unknown`，以提供更好的推导——这并不是一个你可以在 Python 中获取到的类型，只是 Pyright 内部工作机制所使用的类型。如果你熟悉 TypeScript，这里的 `Unknown` 类型与 TypeScript 中的 `unknown` 类型非常相似，这并不是巧合，TS 团队本就与 Pyright 团队合作密切，它们的类型系统工作原理也非常相似。

把静态类型检查器切换回 Pyright，看一下 Pyright 对不标注类型的 `double` 函数的类型推导：

![](https://pic2.zhimg.com/80/v2-bdc106c5d4c2c526b88b3e8769511315_1440w.webp)

之前的示例在 Pyright 下产生的结果与 mypy 是一致的，就不多演示了。

如果你开启了 Pyright 的严格模式，会发现 Pyright 总是要求你明确标出函数参数和返回值的类型，这时如果你发现了似乎不得不使用 `Any` 的场景，我仍建议你不要使用 `Any`，而是尽可能使用 `object` 替代。

### 1.8 底类型 `Never` 和 `NoReturn`

类型通常包含一些值，例如 `str` 包含所有字符串，`int` 包含所有整数，某个自定义的 `Dog` 类也包含所有它以及其子类的实例。但一个特殊的类型除外，即“**底类型 (Bottom type)**”，它不包含任何值。

在 Python 3.12+ 中，它被命名为 `Never`，你可以从 typing 中导入它——你可能有些奇怪，在什么情况下需要这个类型。这可能的确不是一个常用的类型，但在类型系统中却有着很大的意义。思考一下，我们通常可以将类型的层次理解为一种不精确的“包含”关系——`object` 作为一切的基类包含着所有值，自然也包含了 `Number`，`Number` 则作为所有数字的基类包含着一切 `int`、`float` 和 `complex`，自然就包含了 `int`，而 `int` 又包含着一切具体的整数。而 `Never` 则仅仅作为一个类型，却不具有任何值（一个空集），那么它就被任何其他类型所包含，即任何类型的子类型，存在于层级的“底部”，这就是为什么称它为“底类型”。

什么样的函数会返回 `Never`，这样一个不具有任何值的类型？当然是永远不会返回值的函数。例如 `sys.exit()` 函数必定引发一个错误导致程序退出，那么它就永远不会返回值，因此我们可以这样表示它：

```python3
from typing import Never

def exit(__status: object = ...) -> Never:
    ...
```

在 Python 3.11 及之前的版本中，存在一个 `NoReturn` 类型——在 Python 3.12+ 中你当然也可以使用它。它的含义与 `Never` 一致（类型检查器将 `Never` 和 `NoReturn` 视为同一个类型的不同别名），它的名称也很清晰地表明它表示一个永远不会返回的函数的“返回值类型”，因此我们也可以将 `exit` 的定义写成这样：

```python3
from typing import NoReturn

def exit(__status: object = ...) -> NoReturn:
    ...
```

对于 `exit` 函数的这种情况，用 `NoReturn` 可能是更清晰的写法。只是在 Python 3.12+ 中，Python 官方更建议优先使用 `Never`，因为它更明确表明了该类型的本质，而不是只能作为某个永远不会返回的函数的“返回值类型”使用。

例如，有些时候你也可以用 `Never` 作为某个函数的参数表示它永远不该被调用的函数，在这种情况下它比 `NoReturn` 这个名称看起来要更合适——尽管我们可能很难想象到这样一个函数的存在价值：

```python3
from typing import Never

def never_call_me(arg: Never) -> None:
    ...
```

![](https://pic1.zhimg.com/80/v2-1c2626906ea4ee9e63835b6bb39595ec_1440w.webp)

### 1.9 泛化容器 (Collections)

> **➡️ 说明：**有时也将“Collection”翻译为“集合”，这里为了避免与“Set”的通常译名“集”产生概念混淆，译为“容器”。

Python 中的大多数容器（`list`、`tuple`、`set` 等）都是异构（heterogeneous）的，例如 `list` 就可以包含很多不同类型的值。不过在多数情况下，当使用这些数据结构时，我们倾向于在其中存储同样类型的值。毕竟我们通常希望稍后将放入容器的对象取出进行一些操作，这通常意味着它们必须共享同一个方法。

在 Python 中，你可以这样表示一个容器中只包含特定的值：

```python3
def tokenize(text: str) -> list[str]:
    return text.upper().split()
```

在 Python 3.8 及更早的版本中，你不能像这样直接用 `list`、`set` 等内置关键字直接表示 Python 内置的容器类型（该语法仅适用于 Python 3.9+），而是需要从 typing 中导入它们：

```python3
from typing import List

def tokenize(text: str) -> List[str]:
    return text.upper().split()
```

除此之外，在 Python 3.9+ 中还有很多内置容器类型可以直接使用这种方式表示，例如 `collections.deque[str]`。

*事实上，Python 正考虑在未来（初步计划是 Python 3.14 中）删除对冗余类型 `typing.Tuple` 等类型的支持，因此应该优先使用新语法（`list`、`tuple`、`dict`）而非旧语法（`typing.List`、`typing.Tuple`、`typing.Dict`）。*

如你的直觉所料，这里容器类型之后方括号 `[]` 中包裹的是容器中值的类型。因此，`list[str]` 就表示一个字符串列表，`list[int | str]` 就表示一个值为整数或字符串的列表，以此类推。你也可以省略这个方括号，表示你并不试图指定容器内部值的类型，例如在 mypy 中 `list` 等价于 `list[Any]`（在 Pyright 中则等价于 `list[Unknown]`）。

对于映射 (Mapping) 类型（如 `dict`、`defaultdict`），可以通过 `dict[KeyType, ValueType]` 这样的语法分别表示键和值的类型：

```python3
def count_chars(string: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for char in string:
        result[char] = result.get(char, 0) + 1
```

*`tuple` 类型支持更复杂的操作，所以将在下一节叙述它的用法。*

这里的语法实际上是泛型语法的特殊应用，这在第 2 节会进一步详述。

遗憾的是，截至 Python 3.12，仍然很难通过 Type Hints 标注 `array.array` 的类型，因为 `array.array` 区分 `int` 和 `float`，而在 Python 的类型系统中 `int` 被认为是与 `float`“相一致（consistent-with）”的（正如上文提到的）。更大问题在于 Python 中的数字类型不会溢出，而 `array.array` 中的数字类型会发生溢出错误（OverflowError）。

另外，typing 中包含一个 `Sequence` 类型可以表示 Python 中的序列类型（`str`, `tuple`, `list`, `array`等），同样支持方括号表示容器内值的类型。

```python3
from typing import Sequence, Any

def get_length(seq: Sequence[Any]) -> int:
    ...
```

一般来说，对于函数及方法的形参，推荐优先使用 `Sequence` 而非 `list`，以获得更好的泛化性——如果你暂时不理解为什么在这些情况下更应该使用泛化的 `Sequence`，在后文中会详述。

### 1.10 元组 (Tuple)

元组 (Tuple) 有三种用法：

- 用作记录 (Record)
- 用作具名记录 (Records with Named Fields)
- 用作不可变序列 (Immutable Sequences)

将 Tuple 用作**记录** (Record) 时，可以直接将几个类型分别包含在 `[]` 中。例如 `('Shanghai', 'China', 24.28)` 的类型就可以表示为 `tuple[str, float, str]`

```python3
city_area = {
    'China': {'Shanghai': 6340.5, 'Beijing': ...}, 
    'Russia': {...},
    ...
}

def population_density(city_info: tuple[str, float, str]) -> float:
    name, population, country = city_info
    area = city_area[country][name]
    return population / area
```

将 Tuple 用作**具名记录** (Records with named fields) 时，可以使用 `NamedTuple`：

```python3
from typing import NamedTuple

class Coordinate(NamedTuple):
    latitude: float
    longitude: float

def city_name(lat_lon: Coordinate) -> str:
    ...
```

这里用到了具名元组，而这是很推荐使用的，它使得代码看起来更加清晰。由于 `NamedTuple` 是 `tuple` 的子类，因此 `NamedTuple` 与 `tuple` 也是相一致（consistent-with）的，这意味着可以放心地使用 `NamedTuple`代替 `tuple`，例如这里的 `Coordinate` 也能表示 `tuple[float, float]`，反之则不行，比如 `tuple[float, float]` 就不能表示 `Coordinate`。

将 Tuple 用作**不可变序列** (Immutable Sequences) 时，需要使用 `...` 表示可变长度：

```python3
tuple[int, ...]  # 表示 `int` 类型构成的元组
tuple[int]       # 表示只有一个 `int` 值的元组
```

值得注意的是，**如果省略方括号，`tuple` 等价于 `tuple[Any, ...]` 而非 `tuple[Any]`**。`tuple`的 用法与`list` 不同，这是需要注意的。

### 1.11 类型守卫 (Type Guard)

你可能经常遇到一种情况：你有一个类型未知或者其类型相当“宽泛”的变量，你需要通过一连串的 if 语句判断它的类型，然后分别执行不同的代码逻辑。

例如你有一个变量，它的类型是 `int | str`，你需要根据它的类型分别执行不同的代码：

```python3
from typing import cast

def is_int(x: int | str) -> bool:
    return isinstance(x, int)

def is_str(x: int | str) -> bool:
    return isinstance(x, str)

x = cast(int | str, "foo")

if is_int(x):
    print(x + 1)
else:
    print(x.upper())
```

此处，无论在 `print(x + 1)` 还是 `print(x.upper())` 中，静态类型检查器都无法判断 `x` 究竟是 `int` 还是 `str`，因此在这两处都会报错：

![](https://pic1.zhimg.com/80/v2-9d86a12d140f86669ac7090ddd50f960_1440w.webp)

为此，你可以使用 Python 3.10 引入的 `TypeGuard`：

```python3
from typing import TypeGuard, cast

def is_int(x: int | str) -> TypeGuard[int]:
    return isinstance(x, int)

def is_str(x: int | str) -> TypeGuard[str]:
    return isinstance(x, str)

x = cast(int | str, "foo")

if is_int(x):
    print(x + 1)
elif is_str(x):
    print(x.upper())
```

`TypeGuard[T]` 用于一个至少接收一个参数且返回布尔值的函数。当使用以 `TypeGuard` 定义的函数时，静态类型检查器会将其第一个实参的类型“窄化 (Narrowing)”为 `TypeGuard[T]` 中的 `T`（如果接收多个参数，多出来的实参不会被窄化）。

实际上，`isinstance` 就是一个 `TypeGuard`，它可以被定义为 `def isinstance[T](obj: object, typ: type[T], /) -> TypeGuard[T]`. 在过去，静态类型检查器会对 `isinstance` 做特殊处理以执行窄化。然而自 Python 3.10 起，你也可以使用 `TypeGuard` 自己定义这样的函数了。因此下面的代码也是合法的：

```python3
x = cast(int | str, "foo")

if isinstance(x, int):
    print(x + 1)
else:
    print(x.upper())
```

在学习了 2.8 节介绍的 `Protocol` 后，你或许会意识到 `TypeGuard` 比想象中的更有用。例如你可以用 `Protocol` 定义一个 `Finite` 类型表示某个支持 `__len__` 的类型，然后将 `hasattr(obj, "__len__")` 包装为一个 `TypeGuard[Finite]`——这可以很大程度上减少你对 `cast` 的使用。

### 1.12 标注可变长参数与关键字参数的类型

你应该已经熟悉如何为常规的函数参数标注类型了。然而 Python 中还存在另外两种参数：形如 `*args` 的可变长参数和形如 `**kwargs` 的关键字参数。

你可以使用下面展示的语法标注它们的类型：

```python3
from typing import Optional

def tag(
    name: str,
    /,
    *content: str,
    class_: Optional[str] = None,
    **attrs: str,
) -> str:
```

上面代码中的 `/` 表示 `/` 前面的参数**只能**通过位置指定，不能通过关键字指定。这是 Python 3.8 中新加入的特性。同样的，也可以使用 `*` 表示 `*` 后面的参数**只能**通过关键字指定，不能通过位置指定。这不是 Type Hints 范围内的知识，在这里提及只是作为补充，以免造成阅读时的困惑，在这里就不给出示例了。

> **✨ 提示：**在 Python 3.7 及之前的版本中，按照 PEP 484 中的约定，使用 `__` 前缀表示仅位置参数：

```python3
from typing import Optional

def tag(__name: str, *content: str, class_: Optional[str] = None,
        **attrs: str) -> str:
```

这里对可变参数的类型提示很好理解。例如，`content` 的类型是 `tuple[str, ...]`，而 `attrs` 的类型则是 `dict[str, str]`. 如果把这里的 `**attrs: str` 改成 `**attrs: float` 的话，`attrs` 的实际类型就是 `dict[str, float]`.

### 1.13 可调用对象 (`Callable`)

在 Python 中，对高阶函数的操作是很常见的，因此经常需要使用函数作为参数。Type hints 也提供了 `Callable[[ParamType1, ParamType2, ...], ReturnType]` 这样的语法表示一个可调用对象（例如函数和类）。`Callable` 常用于标注高阶函数的类型。例如：

```python3
from collections.abc import Callable
from typing import Sequence

def reduce_int_sequence(
    seq: Sequence[int],
    func: Callable[[int, int], int],
    initial: int | None = None
) -> int:
    if initial is None:
        initial = seq[0]
        seq = seq[1:]
    result = initial
    for item in seq:
        result = func(result, item)
    return result
```

> **✨ 提示：**你可能曾看到有人从 `typing` 中导入 `Callable`，自 Python 3.9 起，`collections.abc` 中的泛型类型与 `typing` 中的相应类型已经没有区别了，因此 `typing.Callable`、`typing.Hashable` 等已经被标记为废除 (Deprecated) 了，你更应该从 `collections.abc` 中导入它们——当然，如果你在用 Python 3.8 或更早的版本，那么你只能从 `typing` 中导入它们。

如果你熟悉 TypeScript，可以将这里的 `Callable[[int, int], int]` 理解为 `(a: number, b: number) => number`，这或许更为直观。

又如：

```python3
class Order:
    def __init__(
        self,  # `self` 通常不需要显式的类型提示
        customer: Customer,
        cart: Sequence[LineItem],
        promotion: Optional[Callable[["Order"], float]] = None,
    ) -> None:  # `__init__` 总是返回 `None`，因此也不需要类型提示，但标上一个 `None` 通常是推荐的
```

> **✨ 提示：**注意到这里的 `Callable` 使用了 `"Order"` 字符串作为第一个参数的类型而非 `Order`，这涉及到 Python 类定义的实现问题：在 Python 中，类是在读取完整个类之后才被定义的，因此在类体中无法通过直接引用类本身来表示它的类型。这里使用的是将在 1.16 节详述的“前向引用（Forward reference）”语法。暂时来说，你可以简单理解为它使用引号将类型包起来以表示尚未定义的类型。

遗憾的是，目前 `Callable` 本身还不支持可选参数，但可以结合 `Protocol` 用更复杂的形式表示带可选参数的 `Callable`，这将在 2.10 节中详述。

如果需要使用可变长参数，可以结合 2.4 节的 `TypeVarTuple` 用诸如 `Callable[[*Ts], R]` 或 `Callable[[A, *Ts], R]` 的定义来表示。

另外，关于 `Callable` 还涉及一些与“型变 (Variance)”相关的话题，这部分内容将在第 4 节介绍。

### 1.14 字面量（`Literal`）

在 Python 3.8 中，`Literal` 被引入以用于表示字面量的类型。例如：

```python3
from typing import Literal

# 下面的代码定义了 `Fruit` 类型，它只能是 `"apple"`, `"pear", `"banana"` 三个字面量之一
type Fruit = Literal["apple", "pear", "banana"]
```

根据 [PEP 586 – Literal Types](https://link.zhihu.com/?target=https%3A//peps.python.org/pep-0586/) 的说明，`Literal` 支持整数字面量、`byte`、Unicode 字符串、布尔值、枚举 (Enum) 以及 `None`. 例如以下的类型都是合法的：

```python3
Literal[26]
Literal[0x1A]  # Exactly equivalent to Literal[26]
Literal[-4]
Literal["hello world"]
Literal[b"hello world"]
Literal[u"hello world"]
Literal[True]
Literal[Color.RED]  # Assuming Color is some enum
Literal[None]
```

> **➡️ 说明：**`None` 和 `Literal[None]` 是完全等价的，静态类型检查器会将 `Literal[None]` 简化为 `None`.

你或许已经从一开始的例子中发现了，`Literal` 可以接收多个参数，用于表示多个字面量类型的联合类型。这是一种简化的语法，例如 `Literal["apple", "pear", "banana"]` 等价于 `Literal["apple"] | Literal["pear"] | Literal["banana"]`. 和 `Union` 一样，此种语法也支持嵌套：

```python3
type ReadOnlyMode         = Literal["r", "r+"]
type WriteAndTruncateMode = Literal["w", "w+", "wt", "w+t"]
type WriteNoTruncateMode  = Literal["r+", "r+t"]
type AppendMode           = Literal["a", "a+", "at", "a+t"]

type AllModes = Literal[ReadOnlyMode, WriteAndTruncateMode,
                        WriteNoTruncateMode, AppendMode]
```

所以说 `Literal[Literal[Literal[1, 2, 3], "foo"], 5, None]` 和 `Literal[1, 2, 3, "foo", 5, None]` 其实也是等价的。

可以看到，一定程度上，`Literal` 可以替代枚举 (Enum) 类型——当然，与枚举 (Enum) 相比，`Literal` 并不实际提供运行时约束，这也是 Type hints 的一贯风格。但很大程度上，由于 `Literal` 的引入，需要使用枚举的地方已经少了很多了。

### 1.15 字符串字面量（`LiteralString`）

> ⚠️ **适用版本提示：**该特性仅在 **Python 3.11+** 可用

`LiteralString` 可用于表示一个字符串字面量。

什么时候需要用到这一特性呢？`Literal` 难道不足以表示字面量吗？如果仅仅用于表示字符串，`str` 不也可以吗？

事实上，`LiteralString` 的推出是为了满足一些不太常用的安全性需求。例如在下面的例子中，我们使用了某个第三方库执行 SQL 语句，并将一些操作封装到了一个特定的函数中：

```python3
def query_user(conn: Connection, user_id: str) -> User:
    query = f'SELECT * FROM data WHERE user_id = {user_id}'
    conn.execute(query)
```

这段代码看起来很好，但实际上却有着 SQL 注入的风险。例如用户可以通过下面的方式执行恶意代码：

```python3
query_user(conn, 'user123; DROP TABLE data;')
```

目前一些 SQL API 提供了参数化查询方法，以提高安全性，例如 sqlite3 这个库：

```python3
def query_user(conn: Connection, user_id: str) -> User:
    query = 'SELECT * FROM data WHERE user_id = ?'
    conn.execute(query, (user_id,))
```

然而目前 API 作者无法强制用户按照上面的用法使用，sqlite3 的文档也只能告诫读者不要从外部输入动态构建的 SQL 参数。于是在 Python 3.11 加入了 `LiteralString`，允许 API 作者直接通过类型系统表明他们的意图：

```python3
from typing import LiteralString

def execute(self, sql: LiteralString, parameters: Iterable[str] = ...) -> Cursor: ...
```

现在，这里的 `sql` 参数就不能是通过外部输入构建的了。现在再定义上面的 `query_user` 函数，编辑器就会在静态分析后提示错误：

```python3
def query_user(conn: Connection, user_id: str) -> User:
    query = f`SELECT * FROM data WHERE user_id = {user_id}`
    conn.execute(query)
    # Error: Expected LiteralString, got str.
```

而其他字符串可以正常工作：

```python3
def query_data(conn: Connection, user_id: str, limit: bool) -> None:
    # `query` 是一个 `LiteralString`
    query = '''
        SELECT
            user.name,
            user.age
        FROM data
        WHERE user_id = ?
    '''

    if limit:
        # `query` 仍是 `LiteralString`，因为这里只是加上了另一个 `LiteralString`
        query += ' LIMIT 1'

    conn.execute(query, (user_id,))  # 不报错
```

看了这些，你可能会认为 `LiteralString` 在大部分情况下仍然没什么用。然而，不妨想想在其他领域 `LiteralString` 的用途，例如应用在命令行相关的 API 上防止命令注入，或是应用在 Django 这类采用模板生成 HTML 的框架上防止 XSS 注入，甚至用在 Jinja 这类可对字符串形式的 Python 表达式直接求值渲染的框架上防止模板注入……当然，还有经典的日志注入漏洞，也可以通过 `LiteralString` 提高安全性。

如果你当前使用的 Python 版本低于 Python 3.11，可以安装 Python 官方提供的 typing_extensions 扩展库来使用这一特性。

```python3
from typing_extensions import LiteralString

def execute(self, sql: LiteralString, parameters: Iterable[str] = ...) -> Cursor: ...
```

### 1.16 前向引用 (Forward Reference)

在 1.13 节中，我们简单了解了“**前向引用 (Forward Reference)**”的一个应用——用来在类定义内部表示类自身的类型。例如：

```python3
class Rectangle:
    # ... 前面的代码省略 ...
    def stretch(self, factor: float) -> "Rectangle":
        return Rectangle(width=self.width * factor)
```

> **✨ 提示：**在 2.7 节，将提到对于此种特殊情况（在类定义内部表示类自身的类型）的一种更简洁的方案。

事实上，此种用引号包裹尚未在运行时代码中定义类型的前向引用语法，不止适用于在类定义内部表示类自身。假设你首先定义了如下的类：

```python3
class Animal:
    pass

class Dog:
    def bark(self) -> None:
        print("汪")
```

现在，假设你需要在 `Animal` 上定义一个 `as_dog()` 方法，通过判断自身是否是 `Dog` 的实例返回 `Dog` 或 `None`. 一个错误的定义如下：

```python3
class Animal:
    def as_dog(self) -> Dog | None:
        return self if isinstance(self, Dog) else None

class Dog:
    def bark(self) -> None:
        print("汪")
```

这是因为在定义 `Animal` 时还未定义 `Dog`，因此这段代码实际上会产生运行时错误。

你需要用引号包裹 `Dog | None` 来避免运行时的未定义问题：

```python3
class Animal:
    def as_dog(self) -> "Dog | None":
        return self if isinstance(self, Dog) else None

class Dog:
    def bark(self) -> None:
        print("汪")
```

注意，不要仅将 `Dog` 包裹起来写成 `"Dog" | None`，这是不合法的。

前向引用也适用于第 2 节中将介绍的泛型，如 `"Box[str]"`. 通常来说，你总是需要将整个类型用引号包裹，而不是仅包裹尚未定义的类型。

另外，有些时候你可能会尝试给前向引用起个别名。假设你不使用 `type` 关键字或 `TypeAlias`：

```python3
MyType = "ClassName"

class ClassName:
    ...
```

在这里，静态类型检查器无法区分 `MyType` 到底是个前向引用类型，或者仅仅是个值为 `"ClassName"` 的变量。为此，你可以使用 Python 3.12+ 中的 `type` 关键字或 Python 3.10~3.11 可用的 `TypeAlias` 明确表示你打算定义一个前向引用类型的别名：

```python3
type MyType = "ClassName"
# 或
# MyType: TypeAlias = "ClassName"  # 适用于 Python 3.10~3.11

class ClassName:
    ...
```

更多关于前向引用的信息，可以参考 [PEP 563 – Postponed Evaluation of Annotations](https://link.zhihu.com/?target=https%3A//peps.python.org/pep-0563/%23forward-references).

### 1.17 `@override` 装饰器

> ⚠️ **适用版本提示：**该特性仅在 **Python 3.12+** 可用

千呼万唤始出来——终于，Python 现在也有自己的 `@override` 了。

在过去，我们通常使用 `abc` 中的 `ABC` 和 `@abstractmethod` 装饰器来实现一个抽象类：

```python3
from abc import ABC, abstractmethod

class Base(ABC):
    @abstractmethod
    def get_color(self) -> str:
        return 'blue'

class GoodChild(Base):
    def get_color(self) -> str:
        return 'yellow'
```

不过比较遗憾的是，这其实只在运行时奏效。如果我们定义了这样一个类：

```python3
class BadChild(Base):
    def get_colour(self) -> str:
        return 'red'
```

可以看到，这里把 `color` 拼成了 `colour`. 但是类型检查器并不会提示我们这个错误。

在 Python 3.12+ 中，你可以使用 `@override` 装饰器。当你用该装饰器装饰一个方法时，类型检查器会检查该方法是否真的重载了父类中的某个已有方法：

```python3
from typing import override

class Base:
    def get_color(self) -> str:
      return 'blue'

class GoodChild(Base):
    @override  # OK: overrides Base.get_color
    def get_color(self) -> str:
        return 'yellow'

class BadChild(Base):
    @override  # Type checker error: does not override Base.get_color
    def get_colour(self) -> str:
        return 'red'
```

## 2 进阶语法

### 2.1 理解结构化类型/鸭子类型

在 Python 中，类型的定义是“鸭子类型/结构化类型（Duck Type/Structural Type）”，而不是 Java/C++ 等静态语言中所使用的“指称类型（Denotational Type）”。这也是大多数动态语言采用的类型方案，例如TypeScript 的类型系统就与 Python 高度相似（事实上，Python 的许多 TypeScript 语法正是来自于 TypeScript）。

那么，什么是鸭子类型？我们常常用一句话来解释“鸭子类型”，不过，这句话可能使初学者摸不着头脑：

> ✨ 如果一个东西看起来像鸭子，游起来像鸭子，叫起来像鸭子，那么它就是鸭子。

要理解这句话的字面意思很容易，但要把它转换到编程语言中的类型上，就需要一番思考，有时候这并不是很容易。不过不要着急去翻译上面这句话，先看一下在鸭子类型（结构化类型）中，“类型”的定义是什么：

> ✨ 类型是一系列值和可以对其执行的操作。

这句话更加抽象，并且似乎更令人摸不着头脑，但举个例子就很容易理解了。在 Python 中，`str` 类型表示字符串，它“是一系列**值**”，这很容易理解，因为 `str` 类型表示**所有**字符串的值，它是“可以对其执行的**操作**”，这也很容易理解，因为我们可以在 `str` 类型上通过 `+` 进行字符串拼接操作，也可以在字符串上直接调用诸如 `join` 的方法，这都是 `str` 类型所特有的操作。

那么，假如我们定义了两个新类型，一个叫做 `mystr1`，一个叫做 `mystr2`，它们都继承自 `str`，且都实现了并且仅实现了通过 `+` 进行字符串拼接的操作，那么它们是不是同一个类型呢？当然！它们涵盖同样的值，都能进行同样的操作（字符串拼接）。类型是“一系列值及可以对其执行的操作”，它们的值相同，操作也相同，那么当然可以被理解为同一种类型。事实上，Python 正是这样理解类型的，并且在所有采用鸭子类型（结构化类型）的语言中，都是如此。

然而，在 C++/Java 这些使用指称类型的语言中，事实就不同了。上面定义的两个类型，`mystr1` 和 `mystr2`，即使使用上没有任何区别，因为其名称不同，也被认为是不同的类型。

于是，要理解 1.3 节中提到的 `int`、`float`、`complex` 的“一致性（consistent-with）”问题，也变得很简单了。既然 `int` 类型实现了 `float` 类型的所有方法，那么 `float` 就可以被认为包含了 `int`；既然 `float`类型实现了 `complex` 类型的所有方法，那么 `complex` 就可以被认为包含了 `float`。

当然，反过来就不行了，因为 `complex` 没有实现 `float` 的所有方法，而 `float` 也没有实现 `int` 的所有方法。因此，如果函数的某个参数可以是任何数字，那么你可以将其类型直接标注为 `complex` 而不用标注 `int | float | complex`。

希望这一节能够帮助你更好地理解下面的几节内容，因为下面几节内容都是基于对结构化类型的理解之上的。

### 2.2 抽象基类（**Abstract Base Class**）

考虑这样一个函数：

```python3
def name2hex(name: str, color_map: dict[str, int]) -> str:
    ...
```

这里的 `name2hex` 函数接收一个字符串 `name` 以及一个键和值分别为 `str` 和 `int` 类型的字典，然后将字符串根据字典翻译成对应的十六进制字符串返回。

这看起来没问题，但其实有个小缺陷。`defaultdict` 和 `OrderedDict` 是 `dict` 的子类，所以这里的 `color_map` 也可以是 `defaultdict` 或 `OrderedDict`，但 `UserDict` 却不是 `dict` 的子类，所以 `color_map` 不能是 `UserDict`，但使用 `UserDict` 创建自定义映射却是被推荐的。因此，最好使用 `collections.abc` 中的 `Mapping` 抽象类型（映射）或 `MutableMapping` 抽象类型（可变映射），而不是 `dict`.

相比 `Mapping`，`MutableMapping` 实现了更多方法，例如 `setdefault`、`pop` 和 `update`. 但这里的`color_map` 没必要实现这些方法，因此使用 `Mapping` 就可以了：

```python3
from collections.abc import Mapping

def name2hex(name: str, color_map: Mapping[str, int]) -> str: ...
```

然而对于返回值，我们则应该保证类型尽可能明确，因为返回值总是一个具体的类型。比如上面定义的 `tokenize` 函数：

```python3
def tokenize(text: str) -> list[str]:
    return text.upper().split()
```

这里 `tokenize` 的返回值就应该是具体的，例如这里应该使用 `list[str]` 而不是 `Sequence[str]`。

除了 `dict` 可以用 `Mapping` 更好地表示外，`list/tuple` 等序列也应该尽量使用 `Sequence` 来表示（如果不关心序列的具体类型的话），或者用 `Iterable` 表示一个可迭代对象。

值得注意的是，`Sequence` 和 `Iterable` 有一些微妙的区别。例如要使用 `len()` 获取输入值的长度，就只能使用 `Sequence` 而不是 `Iterable`，因为 Python 中的可迭代对象在迭代完成之前是无法得到长度的，更何况还存在一些可以循环迭代的对象长度是无限的。

### 2.3 泛型：类型变量 (`TypeVar`)

你可能使用过 `random.sample` 函数，它用于从一个序列中随机取出若干个值。例如 `sample([1, 2, 3, 4], 2)` 就是从 `[1, 2, 3, 4]` 中随机取出 2 个值。让我们思考一下它的类型定义——一开始，你可能会写出这样的代码：

```python3
from collections.abc import Sequence
from random import shuffle
from typing import Any

def sample(population: Sequence[Any], size: int) -> list[Any]:
    if size < 1:
        raise ValueError('size must be >= 1')
    result = list(population)
    shuffle(result)
    return result[:size]
```

使用 `Any` 固然没错，但这破坏了一些类型安全性：

![](https://pic2.zhimg.com/80/v2-340f064bc0b7214499040980c4ce9485_1440w.webp)

这样的场景非常常见，你可能经常需要对容器进行处理。如果对于此类函数你只能使用 `Any`，那么你就需要每次为这些函数的返回值标上类型来获得编辑器带给你的提示，如 `nums: list[int] = sample([1, 2, 3, 4], 2)`，这既麻烦又容易出错——如果能够让类型检查器“提取出”这里 `population` 参数这个 `Sequence[...]` 中这个 `...` 的类型就好了，然后你就可以返回 `list[...]`——这样一来，调用 `sample([1, 2, 3, 4], 2)` 时，该函数就能从传入的 `[1, 2, 3, 4]` 中推导出 `population` 参数的类型是 `list[int]`，然后从中“提取”出 `int`，最后根据提取出的 `int` 返回 `list[int]`，于是你便不需要手动标注 `nums` 的类型信息而能依赖于自动推导了。这种技术是存在的，它被称为“**泛型 (Generic)**”。

让我们先看一下利用泛型改造该函数的结果：

```python3
from collections.abc import Sequence
from random import shuffle

def sample[T](population: Sequence[T], size: int) -> list[T]:
    ...
```

![](https://pic3.zhimg.com/80/v2-6371a96745196466b28d2087e85b4316_1440w.webp)

在这里，通过在函数名 `sample` 之后添加了 `[T]` 定义了一个适用于该函数的“**类型变量 (Type variable)**”并命名为 `T`（在其他编程语言中，可能更常将其称为“类型参数 (Type parameter)”，它们描述的是同一个事物）。类型变量只有在具体使用时才会被实际绑定到某个类型上，如对于 `sample([1, 2, 3, 4], 2)` 这里的 `T` 就被推导为 `int`，对于 `sample(["foo", "bar", "baz"], 2)` 则被推导为 `str`，以此类推。

值得注意的是，直接像这样定义类型变量是 Python 3.12+ 中才能使用的新语法。在 Python 3.11 及更早的版本中，你需要使用 `typing.TypeVar` 像定义普通变量一样在外部定义类型变量：

```python3
from collections.abc import Sequence
from random import shuffle
from typing import TypeVar

T = TypeVar('T')

def sample(population: Sequence[T], size: int) -> list[T]:
    if size < 1:
        raise ValueError('size must be >= 1')
    result = list(population)
    shuffle(result)
    return result[:size]
```

> **➡️ 故事：**这源于 Python 早期的一个（可以说有点失败的）决策，当时 Python 官方没打算为了引入泛型大改解释器实现，而是希望基本保留原本的语法解析规则，所以选择用手动定义 `TypeVar` 这个手段凑合。但后来大家逐渐发现这样写实在是太逆天太难过了，因此出现了 [PEP 695 – Type Parameter Syntax](https://link.zhihu.com/?target=https%3A//peps.python.org/pep-0695/) 提案引入正经的泛型语法，并且该提案在 Python 3.12 中被最终实现了。本文受限于篇幅不可能详细描述该提案带来的全部改进，我个人建议有时间去稍微读一下这份提案以全面了解它带来的新特性。

和许多其他编程语言一样，在 Python 3.12+ 中你也可以在函数名后边的类型变量列表里定义多个类型变量，比如本文开头的这个示例：

```python3
from typing import Callable

def map_list[T, U](func: Callable[[T], U], lst: list[T]) -> list[U]:
    return [func(x) for x in lst]
```

对于 Python 3.11 及更高的版本，你也自然可以在外头像是定义普通变量一样用 `TypeVar` 创建多个类型变量，就不演示了。

有时，你可能希望精确限制类型变量的取值，这时可以使用“**受限类型变量 (Constrained type variable)**”语法。例如我们想定义一个 `sum_nums` 函数，它只能接受 `int`、`float` 或 `complex` 构成的序列：

```python3
from typing import Sequence, cast

def sum_nums[T: (int, float, complex)](nums: Sequence[T]) -> T:
    res = 0
    for n in nums:
        res += n
    return cast(T, res)
```

![](https://pic2.zhimg.com/80/v2-e566c46e7ffce3085d02ae61e63b8f95_1440w.webp)

要定义受限类型变量，需要在其名称后使用一个包含了若干类型的元组，它们表示该类型变量的可能取值。

在 Python 3.11 及更早的版本中，你需要使用这样的语法定义受限类型变量：

```python3
from typing import Sequence, TypeVar, cast

T = TypeVar("T", int, float, complex)

def sum_nums(nums: Sequence[T]) -> T:
    ...
```

实际上，受限类型变量的引入最初是为了简化一些函数重载的场景（参见第 2.9 节）。例如对于以下情况：

```python3
@overload
def concat(x: str, y: str) -> str: ...
@overload
def concat(x: bytes, y: bytes) -> bytes: ..
```

使用受限类型变量可以将其很好地简化：

```python3
def concat[AnyStr: (str, bytes)](x: AnyStr, y: AnyStr) -> AnyStr:
    ...
```

该 `AnyStr` 类型已经被 typing 库内置，你可以从中导入它。

下面用受限类型变量展示了对 `collections.mode` 的一个实现，用来返回序列中出现次数最多的数据：

```python3
from collections.abc import Iterable
from decimal import Decimal
from fractions import Fraction

def mode[N: (float, Decimal, Fraction)](data: Iterable[N]) -> N:
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError('no mode for empty data')
    return pairs[0][0]
```

当然，和其他许多编程语言类似，Python 的泛型语法支持设置某个类型变量的“上限”。例如对于这里的 `collections.mode`，我们也许不仅希望能支持 `float`、`Decimal`、`Fraction` 这几个类型，也希望支持所有支持哈希的类型（因为代码中使用了 `Counter()`，它的实现依赖于 `dict`，而 `dict` 中的键必须是可哈希的）。

为此，我们可以使用如下语法表示类型变量的“**上限 (Upper bound)**”：

```python3
from collections.abc import Hashable
from decimal import Decimal
from fractions import Fraction

def mode[T: Hashable](data: Iterable[T]) -> T:
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError("no mode for empty data")
    return pairs[0][0]
```

`Hashable` 表示任何实现了 `__hash__` 方法的类型，在这里用起来正合适。

如果你熟悉其他编程语言中的泛型语法，这应当对你来说是更直观的语法，而上面表示受限类型变量的语法则显得有些奇特。

如果不明确标注类型变量的上限，则其默认为 `object`，也就是一切值的基类。

对于 Python 3.11 及更早的版本，你需要使用 `TypeVar` 的 `bound` 参数来表示其上限：

```python3
from collections.abc import Hashable
from decimal import Decimal
from fractions import Fraction
from typing import TypeVar

HashableT = TypeVar('NumberT', bound=Hashable)

def mode(data: Iterable[HashableT]) -> HashableT:
    ...
```

> ✨ **提示：**需要注意的是，这里的 `bound` 表示 `boundary`（边界），和 `bind` 无关。此类具有边界的类型变量也被称为**有界泛型**，它表示某个类型的“上限”。

最后，回到之前 `sum_nums` 的例子，解决一个常见问题——你可能会心想，这里似乎也可以使用类型上限——考虑到 int、float、complex 的一致性关系，你可能会写出这样的代码：

```python3
def sum_nums[T: complex](nums: Sequence[T]) -> T:
    ...
```

这样写没错，但是这会导致类型推导不够精确，有时你会看到一些意料之外的联合类型被推导出来：

![](https://pic3.zhimg.com/80/v2-a353b504c22b4e1cb5e98299118f86e2_1440w.webp)

这是因为 `complex` 不仅包含了 `int`、`float` 和 `complex` 自身，也包括了它们组成的联合类型——因此若不明确限定这里的 T 只能有三种单独的取值，联合类型也可能被推导出来。例如在这里的情况下，`[1, 2.5, 3]` 的类型实际上是 `list[int | float]`，因此 `T` 便被推导为了 `int | float` 而不是更精确的 float.

在 Python 3.12+ 中，`type` 关键字所支持的语法与函数的类型参数列表相同：

```python3
type Point[T] = tuple[T, T]

type IntFunc[**P] = Callable[P, int]  # ParamSpec, 后面会说
type LabeledTuple[*Ts] = tuple[str, *Ts]  # TypeVarTuple, 后面也会说
type HashableSequence[T: Hashable] = Sequence[T]  # TypeVar with bound
type IntOrStrSequence[T: (int, str)] = Sequence[T]  # TypeVar with constraints
```

### 2.4 泛型：类型变量元组（`TypeVarTuple`）

> ⚠️ **适用版本提示：**该特性仅在 **Python 3.11+** 可用

还记得 `tuple` 和 `Union` 吗？它们可以接收任意多个类型参数：

```python3
from typing import Union

type ColorRGB = tuple[int, int, int]
type Hexidecimal = Union[int, str]
```

在 Python 3.10 及之前的版本中，只有一些内置类型支持可变长类型变量。在 Python 3.11 中，加入了泛型元组 (`TypeVarTuple`)，使得定义类似于 `tuple`、`Union` 这种可接收可变长类型变量的泛型成为可能。

假设一下，在过去的版本中，我们想要实现一个自定义类型 `Array`，它可以像下面这样使用：

```python3
def to_gray(videos: Array[Time, Batch, Height, Width, Channels]): ...
```

然而在过去，仅有一些内置类型，例如 `tuple` 能够实现这样的功能。我们曾经只能妥协地将其写为：

```python3
def to_gray(videos: Array): ...
```

而现在，你可以写成这样（这里涉及了泛型类 (Generic class) 的语法，参考之后的第 2.6 节）：

```python3
class Array[DType, *Shape]:
    def __abs__(self) -> "Array[DType, *Shape]": ...
    def __add__(self, other: "Array[DType, *Shape]") -> "Array[DType, *Shape]": ...
```

> **➡️ 提示：**这里将 `Array[DType, *Shape]` 用引号包裹起来作为前向引用以避免自引用问题。如果你忘了，可以回头看看第 1.16 节的相关内容。

与我们常规定义可变长函数参数如 `*args` 类似，也可通过类似的语法定义和使用可变长类型参数。在这里，`Shape` 是一个可变长的类型参数，可接收任意多个类型参数，因此可以通过类似 `Array[float, Height, Wdith]` 的语法调用。同时，也可以将可变长类型参数 `Shape`“展开”并传递给其他泛型，像是这里 `__abs__` 和 `__add__` 方法返回值中的 `Array[DType, *Shape]`.

这种简化的类型变量定义语法是 Python 3.12+ 才能使用的。对于 Python 3.11 及更早的版本，你需要使用 `TypeVarTuple`：

```python3
from typing import Generic, TypeVar, TypeVarTuple

DType = TypeVar('DType')
Shape = TypeVarTuple('Shape')

class Array(Geneirc(DType, *Shape)):
    def __abs__(self) -> "Array[DType, *Shape]": ...
    def __add__(self, other: "Array[DType, *Shape]") -> "Array[DType, *Shape]": ...
```

现在我们便可以像这样使用 `Array` 了：

```python3
from typing import NewType

Height = NewType("Height", int)
Width = NewType("Width", int)

x: Array[float, Height, Width] = Array()
```

你也可以结合 `Lietral`，直接在类型中注释 `Array` 的大小：

```python3
from typing import Literal as L

x: Array[float, L[480], L[640]] = Array()
```

同样的，如果你希望在低版本应用这一特性，可以考虑安装 typing_extensions 库。

### 2.5 泛型：参数规范变量（Parameter Specification Variable）

*——原谅我真不知道该怎么翻译这个词语，只能生硬地这么翻译了。*

正如 1.13 节提到的和即将在 2.10 节说明的，我们目前已知有两种方法定义函数类型，一种简单使用 `Callable`，一种结合 `Protocol` 和 `__call__` 方法。但是，这两种方法似乎都不能很好地与泛型相结合。也就是说，我们无法将 `Callable` 的参数类型“传递”给另外一个类型。而这在装饰器中实际上是一个比较常见的需求。

考虑这段代码：

```python3
from typing import Awaitable, Callable

def add_logging[R](f: Callable[..., R]) -> Callable[..., Awaitable[R]]:
    async def inner(*args: object, **kwargs: object) -> R:
        await log_to_database()
        return f(*args, **kwargs)
    return inner

@add_logging
def takes_int_str(x: int, y: str) -> int:
    return x + 7

await takes_int_str(1, 'A')
await takes_int_str('B', 2)  # Fails at runtime
```

在这里，`f` 的参数类型应当与 `inner` 是一致的。然而由于 `Callable` 自身的限制，我们只能简单使用 `...` 来忽略对参数类型的标注。

而在 Python 3.10 中，引入了 `ParamSpec`，这使得对此类情况的类型标注成为可能：

```python3
from typing import Awaitable, Callable, TypeVar

def add_logging[**P, R](f: Callable[P, R]) -> Callable[P, Awaitable[R]]:
    async def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        await log_to_database()
        return f(*args, **kwargs)
    return inner

@add_logging
def takes_int_str(x: int, y: str) -> int:
   return x + 7

await takes_int_str(1, 'A')  # Accepted
await takes_int_str('B', 2)  # Correctly rejected by the type checker
```

这种简化的类型变量定义语法是 Python 3.12+ 中才可以用，在此处你可以使用 `**` 来定义一个为 `ParamSpec` 的类型参数。对于 Python 3.10~3.11，你需要这么定义：

```python3
from typing import Awaitable, Callable, ParamSpec, TypeVar

P = ParamSpec('P')
R = TypeVar('R')

def add_logging(f: Callable[P, R]) -> Callable[P, Awaitable[R]]:
    ...
```

另一种常见情况是，高阶函数（或可调用对象）的返回值往往依赖于传入的某个函数。它们常常添加、移除或修改另一个函数的参数。因此，随着 `ParamSpec` 的引入，也同样引入了一个 `Concatenate`，它与 `Callable` 和 `ParamSpec` 结合使用。

`Concatenate` 目前只有作为 `Callable` 的第一个参数时有效。`Concatenate` 的最后一个参数必须是`ParamSpec` 或 `...`.

下面是一个 Python 文档中的例子，展示了如何注解一个装饰器 `with_lock`，它为被装饰的函数提供了一个`threading.Lock`，可以使用 `Concatenate` 来表示 `with_lock` 期望一个接受 `Lock` 作为第一个参数的可调用对象，并返回一个具有不同类型签名的可调用对象。在这种情况下，`ParamSpec` 表示返回的可调用对象的参数类型取决于传入的可调用对象的参数类型。

```python3
from collections.abc import Callable
from threading import Lock
from typing import Concatenate

# Use this lock to ensure that only one thread is executing a function at any time.
my_lock = Lock()

def with_lock[**P, R](f: Callable[Concatenate[Lock, P], R]) -> Callable[P, R]:
    """A type-safe decorator which provides a lock."""
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        # Provide the lock as the first argument.
        return f(my_lock, *args, **kwargs)
    return inner

@with_lock
def sum_threadsafe(lock: Lock, numbers: list[float]) -> float:
    """Add a list of numbers together in a thread-safe manner."""
    with lock:
        return sum(numbers)

# We don't need to pass in the lock ourselves thanks to the decorator.
sum_threadsafe([1.1, 2.2, 3.3])
```

### 2.6 泛型：泛型类（Generic Class）

Type hints 中的泛型除了支持函数外，还支持类，例如：

```python3
class Node[T]:
    def __init__(self, data: T, next: "Node[T] | None" = None):
        self._data = data
        self._next = next

    @property
    def data(self) -> T:
        return self._data

    @property
    def next(self) -> "Node[T] | None":
        return self._next
```

在 Python 3.11 及之前的版本中，你需要写成这样：

```python3
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class Node(Generic[T]):
    def __init__(self, data: T, next: Optional["Node[T]"] = None):
        self._data = data
        self._next = next

    @property
    def data(self) -> T:
        return self._data

    @property
    def next(self) -> Optional["Node[T]"]:
        return self._next
```

> **➡️ 说明：**需要注意的是，这里的 `Generic[T]` 需要在最后继承。如果这里的 `Node` 类继承了其他父类，那么需要将其他继承放在前面。

在自定义泛型类后，就可以使用 `Node[...]` 这样的语法为自定义的泛型类绑定类型了，例如 `Node[int]`、`Node[str]`.

有趣的是，类支持显式绑定类型变量而函数不支持的特性还带来了一些有趣的事实。例如你有一个 `def map_list[T, U](f: Callable[[T], U], a: list[T], /) -> list[U]`，你不能直接写成 `map_list[int, str](lambda x: str(x + 1), [1, 2, 3])` 的——这里的 `[int, str]` 是非法的。然而，你可以考虑将 `map_list` 定义成一个类：

```python3
class map_list[T, U]:
    def __new__(cls, f: Callable[[T], U], a: list[T], /) -> list[U]:
        return list(map(f, a))
```

你甚至可以自由选择哪些类型变量是允许绑定的——例如你可能觉得 `U` 并不需要显式绑定，因为类型检查器可以从传入的 `f` 定义里推断出来：

```python3
class map_list[T]:
    def __new__[U](cls, f: Callable[[T], U], a: list[T], /) -> list[U]:
        return list(map(f, a))
```

现在，你就可以编写 `map_list[int](lambda x: str(x + 1), [1, 2, 3])` 了——可以看到你通过这种方法实际上给传入的 lambda 表达式定义了参数类型。有时，我会编写这样一个类用来给 lambda 表达式标上类型：

```python3
from collections.abc import Callable

class typed[*Ts]:
    def __new__[U](cls, f: Callable[[*Ts], U], /) -> Callable[[*Ts], U]:
        return f

add1point5 = typed[int](lambda x: x + 1.5)  # (int) -> float
```

——当然，你也可以选择把 `typed` 定义为一个普通的函数，类型作为 `*args` 在前面传入，毕竟 Python 中的类型也是值，是可以传来传去的，不像 TypeScript. 但定义成类会比较酷炫。

### 2.7 自引用类型 (`Self`)

> ⚠️ **适用版本提示：**该特性仅在 **Python 3.11+** 可用

还记得在 1.16 节中提到的用前向引用表示类型自身的方案吗？考虑到表示自身的类型是一个非常常见的应用，Python 3.11 中加入了 `Self` 用于表示自身。例如：

```python3
from typing import Self

class Shape:
    def set_scale(self, scale: float) -> Self:
        self.scale = scale
        return self
```

除此之外，`Self` 能够更好地在子类型上工作。假如在上面 `Shape` 的例子中，我们将 `set_scale()` 的返回值标记为 `-> "Shape"`，对于下面的例子会出现问题：

```python3
class Circle(Shape):
    def set_radius(self, r: float) -> Circle:
        self.radius = r
        return self

Circle().set_scale(0.5)  # 返回值类型被推导为 `Shape`，而不是 `Circle`
Circle().set_scale(0.5).set_radius(2.7)  # 类型检查出错: `Shape` 不存在属性 `set_radius`
```

在过去，可以使用类似下面的扭曲手段来解决这个问题：

```python3
class Shape:
    def set_scale[S: "Shape"](self: S, scale: float) -> S:
        self.scale = scale
        return self

class Circle(Shape):
    def set_radius(self, radius: float) -> "Circle":
        self.radius = radius
        return self

Circle().set_scale(0.5).set_radius(2.7)  # 返回值的类型被推导为 `Circle`
```

你大概还没忘记在 Python 3.11 及更早的版本中不支持新泛型语法，因此这个 `[S: "Shape"]` 得用 `TypeVar` 表示，那这代码看着就更冗长。

现在，使用 `Self` 就可以优雅地解决问题：

```python3
from typing import Self

class Shape:
    def set_scale(self, scale: float) -> Self:
        self.scale = scale
        return self

class Circle(Shape):
    def set_radius(self, radius: float) -> Self:
        self.radius = radius
        return self
```

事实上，`Self` 不仅可以用在实例方法的返回值里，在类方法、方法参数类型、属性类型、泛型类以及即将介绍的 `Protocol` 中都很有用。由于篇幅限制，就不全部列出了，更多细节可以参阅 [PEP 673 – Self Type](https://link.zhihu.com/?target=https%3A//peps.python.org/pep-0673/).

> **✨ 提示：**你可能发现在上面的例子中我们给 `self` 标上了一个更精确的类型，这是合法的 Type hints 语法，有点类似于 C++ 23 的 Deducing this 特性。该语法可以完成许多有趣的事，例如：

```python3
class Boxed[T]:
    def __init__(self, value: T, /) -> None:
        self._value = value

    @property
    def value(self) -> T:
        return self._value

    def concat(self: "Boxed[str]", s: str, /) -> "Boxed[str]":
        return Boxed(s + self._value)


Boxed("world").concat("hello, ")  # 类型检查通过
Boxed(42).concat("foo")  # 类型检查出错: 无法在 `Boxed[int]` 上访问属性 `concat`
```

![](https://pic3.zhimg.com/80/v2-5e90c366027fe965bc8e769a2af61f8a_1440w.webp)

### 2.8 协议 (`Protocol`)

在 2.1 节中，我们理解了 Type hints 中“鸭子类型”的概念——那么我们该如何自定义一个“鸭子类型”，以表示某个实现了某些特定方法（或包含某些特定属性，或两者既有）的类型呢？在其他语言中，这样的特性通常被称为 `interface`（如 TypeScript 和 Go，注意不是 Java 的 `interface`），在 Python 中则是 `Protocol`.

> ➡️ **说明：**我曾看到有人认为 Rust、Swift 或 Scala 中的 `trait` 也是鸭子类型——**完全不是**这样， 它们都是名义类型 (Nominal type). 自 Dotty (Scala 3) 起，Scala 支持了比较完善的鸭子类型，但也和 `trait` 一点关系没有。

假设现在有一个函数 `top`，接收一个可迭代对象和长度 `n`，返回可迭代对象中最大的 `n` 个值：

```python3
def top(series: Iterable[T], length: int) -> list[T]:
    ordered = sorted(series, reverse=True)
    return ordered[:length]
```

现在的问题在于，这里的 `T` 必须可以使用 `sorted()` 排序。你可能会希望 `collections.abc` 中存在一个名为`Sortable` 的抽象类型表示某个类型是可排序的，然而遗憾的是并不存在这样一个类型。

不过，你可以通过 `Protocol` 创建自己的抽象基础类型。要创建一个类型表示其支持通过 `sorted()` 排序，就要知道 Python 中的 `sorted()` 函数是如何实现的：它使用 `__lt__` 魔术方法比较两个值的大小进行排序。因此如果某个类型要支持 `sorted()`，那么只需要其实现了魔术方法 `__lt__`。

自 Python 3.8 起，可以使用 `Protocol` 表示这样一个类型：

```python3
from collections.abc import Iterable
from typing import Protocol, Any

class SupportsLessThan(Protocol):
    def __lt__(self, other: Any) -> bool: ...

def top[LT: SupportsLessThan](series: Iterable[LT], length: int) -> list[LT]:
    ordered = sorted(series, reverse=True)
    return ordered[:length]
```

相比于 `abc.ABC`（Python 内置的抽象类，这里不过多说明），使用 `Protocol` 的好处是它只关注实现，而不关注继承关系。例如，这里不再需要使用 `SupportsLessThan` 重新派生 `str`、`tuple`、`float`、`set` 等内置类也可以在需要使用 `SupportsLessThan` 参数的地方使用它，唯一的要求只是这一类型必须实现 `__lt__` 方法而已。

`Protocol` 也是支持泛型的，例如：

```python3
from typing import Protocol

class ClassA[S, T](Protocol):
    ...
```

在 Python 3.11 及之前的版本，你则需要写成这样：

```python3
from typing import Protocol, TypeVar

S = TypeVar("S")
T = TypeVar("T")

class ClassA(Protocol[S, T]):
    ...
```

### 2.9 函数重载签名（Overloaded Signature）

Python 是一门动态类型语言——和大多数动态类型语言一样，支持函数参数为任意类型以及默认参数的 Python 没有运行时的函数重载机制（也不太需要）。然而类似于 TypeScript，Type hints 提供了一套给静态类型检查器使用的“函数重载签名”机制，以实现静态类型系统上的“函数重载”。

下面的例子展示了如何给 `sum` 标注函数重载签名：

```python3
import operator
from functools import reduce
from collections.abc import Iterable
from typing import overload

@overload
def sum[T](it: Iterable[T]) -> T | int: ...
@overload
def sum[T, S](it: Iterable[T], /, start: S) -> T | S: ...
def sum(it, /, start=0):
    return reduce(operator.add, it, start)
```

重载签名可以放在在函数的实际定义前。**重载签名本身不能包含实现**，只是用来标注函数的参数以及返回值类型，在 Python 运行时会被自动忽略，仅用来辅助静态类型检查。在重载签名之后定义的函数不必要使用 Type Hints 标注类型，因为前面已经通过重载签名标注过了。

> **✨ 提示：**为了性能考虑，Python 内置的 `sum` 函数是实际上用 C 语言实现的，而不是上面编写的 `reduce(operator.add, it, start)`，这里这么写只是用作演示。

下面再演示 `max` 函数的重载签名：

```python3
from collections.abc import Callable, Iterable
from typing import Protocol, Any, overload

class SupportsLessThan(Protocol):
    def __lt__(self, other: Any) -> bool: ...

MISSING = object()
EMPTY_MSG = 'max() arg is an empty sequence'

@overload
def max[LT: SupportLessThan](__arg1: LT, __arg2: LT, *args: LT, key: None = ...) -> LT:
    ...
@overload
def max[T, LT: SupportLessThan](__arg1: T, __arg2: T, *args: T, key: Callable[[T], LT]) -> T:
    ...
@overload
def max[LT: SupportLessThan](__iterable: Iterable[LT], *, key: None = ...) -> LT:
    ...
@overload
def max[T, LT: SupportLessThan](__iterable: Iterable[T], *, key: Callable[[T], LT]) -> T:
    ...
@overload
def max[LT: SupportLessThan, DT](__iterable: Iterable[LT], *, key: None = ...,
        default: DT) -> LT | DT:
    ...
@overload
def max[T, LT: SupportLessThan, DT](__iterable: Iterable[T], *, key: Callable[[T], LT],
        default: DT) -> T | DT:
    ...
def max(first, *args, key=None, default=MISSING):
    if args:
        series = args
        candidate = first
    else:
        series = iter(first)
        try:
            candidate = next(series)
        except StopIteration:
            if default is not MISSING:
                return default
            raise ValueError(EMPTY_MSG) from None
    if key is None:
        for current in series:
            if candidate < current:
                candidate = current
    else:
        candidate_key = key(candidate)
        for current in series:
            current_key = key(current)
            if candidate_key < current_key:
                candidate = current
                candidate_key = current_key
    return candidate
```

> **✨ 提示：**同样的，Python 内置的 `max` 函数为了性能考虑也是使用 C 语言实现的，这里只是为了演示方便编写了一个示例实现。

可以看到，为了考虑各种情况，max 函数的实现以及重载签名要比我们想象的复杂得多。

同样可以发现，在很多情况下，使用重载签名反而会增加大量的语法噪声，而有时这是不必要的。Python 动态类型带来的优势应该被充分利用，因此有时留下一片没有 Type hints 的区域反而是更好的。

### 2.10 标注更复杂的 `Callable`

在 1.13 节中，我们看到了 `Callable` 可以用于标注可调用对象（如函数和类）的类型。然而 `Callable` 自身的局限性也是很明显的——它无法表示可选参数（默认参数），也无法表示关键字参数。事实上，在学习了 `Protocol` 之后，你大概已经意识到了可以用一个实现了 `__call__` 方法的 `Protocol` 来表示这些更加复杂的 `Callable`.

假设你有一个 `repl` 函数，它接受一个 `input_func` 作为回调：

```python3
class InputFunc(Protocol):
    def __call__(self, expr: str, /, *, logging: bool = False) -> str:
        ...

def repl(input_func: InputFunc) -> None:
    while True:
        expr = input_func('>>> ')
        print(expr)
```

可以看到，通过 `Protocol`，我们可以为回调函数的可选参数标注类型。并且 Pyright 也能检查出错误来：

![](https://pic3.zhimg.com/80/v2-d8c8696eb99f1ac210e66d6bbe760156_1440w.webp)

并且也有了提示：

![](https://pic1.zhimg.com/80/v2-94e28c1cc94280886e384d60aed688f0_1440w.webp)

这里有几点需要注意。

首先，如果你没有在参数中添加 `/` 或 `*`，也就是说，按照默认方式来定义参数：

```python3
class InputFunc(Protocol):
    def __call__(self, expr: str, logging: bool = False) -> str:
        ...
```

由于函数参数默认都可以通过关键字调用，此时会严格匹配参数名称。也就是说像这样的函数：

```python3
def input_func1(exp: str, logging: bool = True) -> str:
    ...
```

也被认为是与 `InputFunc` 不兼容的：

![](https://pic4.zhimg.com/80/v2-389b7d11284423c9e13cb1a02d7253db_1440w.webp)

如果你不想严格匹配参数名，请使用**仅位置参数**：

```python3
class InputFunc(Protocol):
    def __call__(self, expr: str, /, logging: bool = False) -> str:
        ...
```

这样就不会报错了：

![](https://pic2.zhimg.com/80/v2-c0153f12300f605e1c574d4e1fa6678d_1440w.webp)

同理，对于 `*` 之后的**仅关键字参数**也是会严格匹配参数名的，这里就不给出例子了。

并且，上面提到的“consistent-with”机制在这里也是一样的，比如这样的函数：

```python3
def input_func1(exp: str, logging: int = 0) -> str:
    if logging:
        print(f'expr: {exp}')
    return exp
```

实际上是与 `InputFunc` 兼容的，因为 `int` 是 `bool` 的超集，实现了 `bool` 类型的所有方法。Pyright 在这里不会报错：

![](https://pic2.zhimg.com/80/v2-8fa9ca17f71f7037ab933d2357ba3dd9_1440w.webp)

不过其实这一般也是我们想要的，倒也不必过分在意。

## 3 高级特性

### 3.1 类型字典 (`TypedDict`)

类型字典 (`TypedDict`) 是 Python 3.8 中新加入的语法，用来为字典进行详细的类型提示。

在上文中已经提到可以使用 `dict[keyType, valueType]` 标注字典的类型，但这里标注的是字典全部元素的类型。如果字典的不同键或值的类型有所区别，那么就无法使用这种方式标注其类型。

考虑这样一个字典，记录了一本书的信息：

```python3
{
  'isbn': '0134757599',
  'title': 'Refactoring, 2e',
  'authors': ['Martin Fowler', 'Kent Beck'],
  'pagecount': 478,
}
```

在 Python 3.8 之前，只能使用 `Dict[str, Any]` 或是 `Dict[str, Union[str, int, List[str]]]` 表示其类型，但这两种表示方式都不能完全表示这个字典的类型。下面演示使用 `TypedDict` 表示这个字典：

```python3
from typing import TypedDict

class BookDict(TypedDict):
    isbn: str
    title: str
    authors: list[str]
    pagecount: int
```

这看起来和上文提到过的 `NamedTuple` 很像，而 `NamedTuple` 实际上是一个 `dataclass`，但这里的 `TypedDict` **不是**一个 `dataclass`。`TypedDict` **不会**实际创建一个类，它只是借鉴了 `dataclass` 的语法，作为 Type hints 的一部分用来表示一个字典的类型。

在运行时，一个 `TypedDict` 构造器和创建一个包含相同参数的 `dict` 构造器是等价的。这意味着这里的“键”不会创建实例属性，也不能被赋予默认值，同时一个 `TypedDict` 也不能包含任何方法。如下所示：

```python3
>>> from typing import TypedDict
>>> class BookDict(TypedDict):
...     isbn: str
...     title: str
...     authors: list[str]
...     pagecount: int
...
...
>>> bd = BookDict(title='Programming Pearls',
...               authors='Jon Bentley',
...               isbn='0201657880',
...               pagecount=256)
...
>>> bd
{'title': 'Programming Pearls', 'authors': 'Jon Bentley', 'isbn': '0201657880',
 'pagecount': 256}
>>> type(bd)
<class 'dict'>
```

可以看到，在使用 `BookDict` 创建字典 `bd` 时，虽然 `authors` 并没有被赋以由 `TypedDict` 标注的字符串列表，而是被赋以一个字符串，但 Python 在运行时仍不会报错，这是因为 Python 不会对 `TypedDict` 做运行时类型检查。在不使用静态类型检查器时，`TypedDict` 和注释没有任何区别，也不会起到任何作用，它唯一的作用就是提高代码的可读性，而 `dataclass` 则会在运行时创建一个真实的类，这与 `TypedDict` 有明显的不同。

上面定义的 `BookDict` 可以这样使用：

```python3
# 这段代码把字典转换成 XML
AUTHOR_ELEMENT = '<AUTHOR>{}</AUTHOR>'

def to_xml(book: BookDict) -> str:
    elements: list[str] = []
    for key, value in book.items():
        if isinstance(value, list):
            elements.extend(
                AUTHOR_ELEMENT.format(n) for n in value)
        else:
            tag = key.upper()
            elements.append(f'<{tag}>{value}</{tag}>')
    xml = '\n\t'.join(elements)
    return f'<BOOK>\n\t{xml}\n</BOOK>'

# 这段代码把一个 JSON 字符串转换为 BookDict
# 实际上这段代码并不能保证类型安全
# 因为静态类型检查器无法推断 json.loads() 的返回值
# 因此如果需要保证这个函数的可靠性
# 使用该函数时仍需要对返回值做检查
def from_json(data: str) -> BookDict:
    whatever: BookDict = json.loads(data)
    return whatever
```

当然，尽管 `TypedDict` 看起来只是为静态类型检查器提供更多信息，无法真正保证某个运行时变量的类型安全（假如你需要保证诸如 JSON 字符串的类型安全，建议使用 Pydantic 等运行时类型检查方案），但它仍旧非常有用。在过去，要类型安全地传递结构化数据基本上只能通过类，通常使用 dataclass——然而，有些时候使用类可能并不理想，例如在作为配置参数时：

```python3
def setupServer(config: Config) -> Server:
    ...

setupServer(
    Config(
        connection=ConnectionParams(prop1=..., prop2=...),
        database=DatabaseParams(
            host=DatabaseHostParams(prop1=..., prop2=...)
            ...
        )
    )
)
```

像这样使用许多嵌套的类看起来有些冗长——在上面的例子中，用户需要编写大量类似 `Config`、`ConnectionParams`、`DatabaseParams`、`DatabaseHostParams` 的类名来定义配置。通常来说，对于这样的情况，我们会更乐意使用类似 JSON 的格式来定义，在 Python 中就是传入字典：

```python3
def setupServer(config: ...) -> Server:
    ...

setupServer({
    'connection': {'prop1': ..., 'prop2': ...},
    'database': {
        'host': {
            'prop1': ...,
            'prop2': ...,
        }
    }
})
```

这样少写了不少类名，看起来要更清爽一些也更易用一些。许多框架使用这样的风格，如 Django. 然而在 Python 3.8 之前，这样的语法是不太类型安全的，Type hints 无法为这样的字典类型标注详细的类型信息。在 Python 3.8+ 引入了 `TypedDict` 之后，这样的情况终于也变得类型安全了。

另外，在处理网络请求时这也很有意义。例如流行的 `requests` 库，其 `response.json()` 返回一个合法的 JSON 对象，通常用列表或字典表示，其中往往又嵌套着若干层字典和列表。在过去，为了类型安全地访问 `response.json()` 返回的字典，你可能会定义一些 dataclass，然后将其转换为合适的 dataclass——现在则不需要了，你可以直接将其返回值标注为某个 `TypedDict` 以获得字典上的类型安全。

### 3.2 `TypedDict` 中的可选值

> ⚠️ **适用版本提示：**该特性仅在 **Python 3.11+** 可用

`TypedDict` 很不错。但上面演示的 `TypedDict` 有个问题：无法将某个值标记为“可选的”。

这是上面演示过的 `BookDict`：

```python3
from typing import TypedDict

class BookDict(TypedDict):
    isbn: str
    title: str
    authors: list[str]
    pagecount: int
```

如果希望将 `pagecount` 设为可选的要怎么做呢？在 Python 3.11 中，typing 库中引入了 `NotRequired` 类型，可表示某个键值对是“可选的”：

```python3
from typing import TypedDict, NotRequired

class BookDict(TypedDict):
    isbn: str
    title: str
    authors: list[str]
    pagecount: NotRequired[int]
```

当然，Python 也提供了相应的 `Required` 用来表示 `TypedDict` 中某个键是“必要的”。如果你有强迫症的话可以用上：

```python3
from typing import TypedDict, Required, NotRequired

class BookDict(TypedDict):
    isbn: Required[str]
    title: Required[str]
    authors: Required[list[str]]
    pagecount: NotRequired[int]
```

同样的，如果你希望在低版本应用这一特性，可以考虑安装 typing_extensions 库。

**补充：**

嗯……好吧，看起来 `TypedDict` 不是一个太好理解的东西。也确实是这边写得时候为了完备性有点晦涩了，并且 Python 这个 `TypedDict` 实现得也确实不怎么样……

让我们举个实例吧。或许看看 VSCode 里这东西怎么用会直观很多：

![](https://pic2.zhimg.com/80/v2-4bec92f611f9254aa1e72fd561aabda5_1440w.webp)

可以看到，这里我们用 `TypedDict` 获得了更精准的类型提示。这对我们开发显然很有帮助，可以利用编辑器的提示有效减少编码负担。

然后，我们看到，当类型冲突时，VSCode 贴心的给我们报了错：

![](https://pic4.zhimg.com/80/v2-ee31958cacd949c7a0def67760ba749b_1440w.webp)

因为这里希望 `authors` 是个字符串数组，而不是个单纯的字符串。

希望这能让读者意识到 `TypedDict` 是个多么有价值和有必要性的东西。虽然这东西并不能真的在运行时做检查，但也非常好用了。

然后有的时候，我们希望 `pagecount` 是可选的。或许有读者会觉得为什么不这么写呢？

```python3
class BookDict(TypedDict):
    isbn: str
    title: str
    authors: list[str]
    pagecount: int | None
```

好像是个好主意，但是这其实意味着 `pagecount` 仍旧是必须的，只不过它可以是 `None` 而已。如果我们现在简单地去掉 `bd` 中的 `pagecount`，VSCode 还是会报错：

![](https://pic1.zhimg.com/80/v2-319c32169c470c499081e02ff7823b1c_1440w.webp)

你必须要写成这样才行：

![](https://pic3.zhimg.com/80/v2-b39c46cc4e056e5b72cf3a815751ba86_1440w.webp)

但是如果 `BookDict` 中有非常多属性呢？假如有好几十个甚至几百个，其中大多数都是可选的，非要全部写个 `None` 上去显然很烦。

这就是 `NotRequired` 的意义：

![](https://pic2.zhimg.com/80/v2-b8781fad18477598fbd4a4fedce1123d_1440w.webp)

并且，可以看到现在即使你写了个 `'pagecount': None` 也报错了——因为这里期待 `pagecount` 要么不存在，要么就必须是 `int`：

![](https://pic1.zhimg.com/80/v2-63e3ec7f8a49b5c10ac989e6abf2eef4_1440w.webp)

希望有这么个实例能容易理解些。

### 3.3 标注 `**kwargs` 的类型 (`Unpack`)

> ⚠️ **适用版本提示：**该特性仅在 **Python 3.12+** 可用

`Unpack` 提供了对 `**kwargs` 更精确的类型支持。如果你曾深受 `**kwargs` 模糊的类型信息带来的困扰，以至于每次看到某个函数包含了 `*args, **kwargs` 都会对该函数的使用方式感到无限困惑，那么 `Unpack` 就是解决这一困境的绝好方法。

思考以下这段代码：

```python3
def draw_base_chart(color: str, height: int = 400, width: int = 600) -> None:
    ...


def draw_bar_chart(data: list[int], *args, **kwargs) -> None:
    ...
    draw_base_chart(*args, **kwargs)
    ...
```

这段代码中出现了 `*args, **kwargs`——这在 Python 代码中非常常见，以捕获一些并未直接定义在函数参数列表中、可能继续传递给其他函数使用的参数。这在实用中固然非常方便，但这通常会导致 Type hints 无法很好地工作以使编辑器提供智能提示：

![](https://pic1.zhimg.com/80/v2-90df2e48a1ac5d2e40bdd6e8c74535ac_1440w.webp)

在这里，你试图敲个 `wid` 来提示编辑器自动把 `width` 给补全上，但是很遗憾，因为 `*args` 和 `**kwargs` 不能提供任何更进一步的类型信息，编辑器并不能为你提供有意义的智能提示。

![](https://pic1.zhimg.com/80/v2-5acee4b740c18a7efee4d959bb3cd91c_1440w.webp)

而且可以看到，当你少了 `data` 时，编辑器会告诉你少了个参数——

但是当你少了 `color`，同样是个必选参数时：

![](https://pic3.zhimg.com/80/v2-97f71b6d585013a5caf18e948baea112_1440w.webp)

编辑器却并不能“告知”你少传入了一个必选参数，然而这段代码在运行时会产生错误。

按照直觉来说，你可能认为这样可以为 `**kwargs` 标记上合适的 Type hints：

```python3
class BaseChartArgs(TypedDict):
    color: str
    height: NotRequired[int]
    width: NotRequired[int]


def draw_base_chart(**kwargs: BaseChartArgs) -> None:
    ...


def draw_bar_chart(data: list[int], *args, **kwargs: BaseChartArgs) -> None:
    ...
    draw_base_chart(*args, **kwargs)
    ...
```

只是很遗憾，编辑器并不能从这样的 Type hints 中推导出类型信息：

![](https://pic1.zhimg.com/80/v2-b87807bb853ca3b912cf69d1e7435bb4_1440w.webp)

回忆下 1.12 节。对于 `*args`，我们标注的实际上是 `tuple[T, ...]` 中这个 `T` 的类型，而对于 `**kwargs`，我们标注的是 `dict[str, ...]` 中 `...` 的类型。上面这种方式显然不太对。

自 Python 3.12 以来，Python 官方显然意识到了这个问题，因此添加了新类型 `Unpack`，用于解决这个问题：

```python3
from typing import NotRequired, TypedDict, Unpack


class BaseChartArgs(TypedDict):
    color: str
    height: NotRequired[int]
    width: NotRequired[int]


def draw_base_chart(**kwargs: Unpack[BaseChartArgs]) -> None:
    ...


def draw_bar_chart(data: list[int], *args, **kwargs: Unpack[BaseChartArgs]) -> None:
    ...
    draw_base_chart(*args, **kwargs)
    ...
```

现在静态类型检查器就能成功检查出来 `color` 未赋值的问题了：

![](https://pic1.zhimg.com/80/v2-69f3356e87abc1795ee0d18cb459e6e4_1440w.webp)

同时你也获得了编辑器的智能提示：

![](https://pic1.zhimg.com/80/v2-ce676bdd791873c4cfdf1e4a81c16178_1440w.webp)

这真是不能更好的一个特性，快在你的项目中实际用起来吧！

### 3.4 运行时读取 Type hints

在导入模块时，Python 实际上会记录模块中的 Type hints，它们会被保存在 `__annotations__` 属性中。例如：

```python3
# clip_annot.py
def clip(text: str, max_len: int = 80) -> str: ...

# 解释器
>>> from clip_annot import clip
>>> clip.__annotations__
{'text': <class 'str'>, 'max_len': <class 'int'>, 'return': <class 'str'>}
```

值得注意的是，模块在导入时会由解释器对 Type hints 求值，这就是为什么这里的类型是 `<class 'str'>`、`<class 'int'>` 而不是 `'str'`、`'int'` 字符串。这是 Python 3.9 起的标准。

显然，由于 Python 解释器的这一行为，使用 Type hints 会增加模块导入时的 CPU 和内存负担。不过有很多知名的 Python 库高度依赖于这一特性，比如 FastAPI 和 Pydantic。

然而，由于 Python 无法求值尚未定义的类型（也就是自引用类型），因此像是本文 1.10 节中提到的 `Rectangle` 类，其 `stretch` 方法的 `__annotations__` 属性会是字符串 `'Rectangle'` 而不是 `<class 'Rectangle'>`：

```python3
# rectangle.py
class Rectangle:
    # ... 前面的代码省略 ...
    def stretch(self, factor: float) -> 'Rectangle':
        return Rectangle(width=self.width * factor)

# 解释器
>>> from rectangle import Rectangle
>>> Rectangle.stretch.__annotations__
{'factor': <class 'float'>, 'return': 'Rectangle'}
```

因此，Python 拟修改解释器的这一特性，并且有可能在不久之后使 `__annotations__` 默认返回字符串，而不再对类型进行求值。这另一方面也是为了减少 Type hints 带来的额外资源占用，毕竟有很多的 Python 用户实际上并不希望 Type hints 额外造成资源负担。因此，不应该依赖于这一特性在运行时读取 Type Hints.

在当前的 Python 版本下，可以通过 `from __future__ import annotations` 开启这一新特性：

```python3
# clip_annot.py
def clip(text: str, max_len: int = 80) -> str: ...

# 解释器
>>> from __future__ import annotations
>>> from clip_annot import clip
>>> clip.__annotations__
{'text': 'str', 'max_len': 'int', 'return': 'str'}
```

在开启这一特性后，就不能使用 `__annotations__` 属性得到 Type hints 的类型了，而只能得到字符串。这时可以使用 `typing.get_type_hints()`：

```python3
# rectangle.py
class Rectangle:
    # ... 前面的代码省略 ...
    def stretch(self, factor: float) -> 'Rectangle':
        return Rectangle(width=self.width * factor)

# 解释器
>>> from typing import get_type_hints
>>> from rectangle import Rectangle
>>> get_type_hints(Rectangle.stretch)
{'factor': <class 'float'>, 'return': <class 'rectangle.Rectangle'>}
```

`typing.get_type_hints()` 相较于 `__annotations__` 属性更加强大，因为它甚至可以为自引用类型求值。然而，这意味着 `get_type_hints()` 将消耗更多资源。另外，`get_type_hints()` 也不总是返回正确的类型，在某些情况下仍会返回字符串。

除此之外，Python 3.10 中加入了 `inspect.get_annotations()` 函数，它的返回值和不从 `__future__` 导入 `annotations` 时 `__annotations__` 属性的值是相同的：

```python3
# rectangle.py
class Rectangle:
    # ... 前面的代码省略 ...
    def stretch(self, factor: float) -> 'Rectangle':
        return Rectangle(width=self.width * factor)

# 解释器
>>> from inspect import get_annotations
>>> from rectangle import Rectangle
>>> get_annotations(Rectangle.stretch)
{'factor': <class 'float'>, 'return': 'Rectangle'}
```

鉴于 `__annotations__` 属性的值仍然很不稳定，并且随时可能在 Python 的版本更新中发生变动，因此在运行时读取 Type hints 的正确方式是使用 `typing.get_type_hints()`（自 Python 3.5 起）或 `inspect.get_annotations()`（自 Python 3.10 起，这是更为推荐的方式）

## 4 型变 (Variance)

这部分内容是本文初次发布后很久才新增的。事实上，因为这部分内容涉及一些类型理论的知识，实在是有些晦涩难懂，而且平时用得也不那么多，因此我迟迟没有动笔编写这一部分。但是想来想去，为了完整性考虑还是要把这部分加上。我尽我所能把将这些知识写得通俗易懂吧。

一般来说，只有代码库作者需要对这部分有比较深入的了解，所以如果你第一次看不懂，也没关系。或者如果你不打算为 Python 编写什么代码库，那么直接跳过也无妨。

> ✨ **提示：**在 Python 3.12 中实现的 [PEP 695 – Type Parameter Syntax](https://link.zhihu.com/?target=https%3A//peps.python.org/pep-0695/) 提案引入了自动型变性推导，会根据类型参数在类中的使用情况自动推导出其到底是协变、逆变还是不变的。因此在很大程度上，类库作者们已经不太需要手动处理型变问题而是可以依赖于类型检查器的自动推断。在此处仅出于教学目的，为方便理解，使用了 `TypeVar` 语法以避免了自动型变性推导，然而你需要知道的是在 Python 3.12+ 中，型变性通常已经不是个需要你手动处理的问题了。

同样的，这里也参考了很多来自 [Fluent Python, 2nd Edition, Chapter 15](https://link.zhihu.com/?target=https%3A//learning.oreilly.com/library/view/fluent-python-2nd/9781492056348/ch15.html) 的代码示例。

### 4.1 不变 (Invariant)

我们知道，编写这样的代码通常是不会被类型检查器查出问题的：

```python3
class Beverage:
    """任何饮料"""

class Juice(Beverage):
    """任何果汁"""

class OrangeJuice(Juice):
    """橙汁"""

juice1: Juice = Juice()  # OK
juice2: Juice = OrangeJuice()  # OK
```

在上面的例子中，`OrangeJuice` 继承了 `Juice`，因此是 `Juice` 的子类型，所以 `juice2: Juice = OrangeJuice()` 并不会报错——因为子类型可以被赋值给夫类型。

而这样的代码是会报错的：

```python3
juice3: Juice = Beverage()  # Error
```

这里 `Beverage` 是 `Juice` 的父类型，父类型不能赋值给子类型。显然，这符合我们的预期和直觉。

但 `TypeVar` 却不默认遵从这样的规律。假设现在我们有一个饮料贩卖机类：

```python3
T = TypeVar('T')

class BeverageDispenser:
    """饮料贩卖机"""
    def __init__(self, beverage: T) -> None:
        self.beverage = beverage

    def dispense(self) -> T:
        return self.beverage
```

然后我们有一个 `install` 函数，用于安装一台饮料贩卖机。因为某些原因，这台机器只能贩卖果汁：

```python3
def install_dispenser(dispenser: BeverageDispenser[Juice]) -> None:
    """安装果汁贩卖机"""
    ...
```

显然，这样的代码是有效的：

```python3
juice_dispenser = BeverageDispenser(Juice())
install_dispenser(juice_dispenser)
```

理应如此。毕竟我们定义时就明确了 `install_dispenser` 只能安装果汁贩卖机。

按照你的直觉，你推断出下面这样的代码会报错，因为 `Beverage` 是 `Juice` 的父类型，而 `install_dispenser` 只能安装果汁贩卖机。

```python3
beverage_dispenser = BeverageDispenser(Beverage())
install_dispenser(beverage_dispenser)
```

当然，事实也的确如此：

![](https://pic1.zhimg.com/80/v2-f4fb509fe3e93116083ec114da5d9bf4_1440w.webp)

不过，怪异的事情来了。实际上，`install_dispenser` 也不能安装橙汁贩卖机，尽管 `OrangeJuice` 是 `Juice` 的子类：

```python3
orange_juice_dispenser = BeverageDispenser(OrangeJuice())
install_dispenser(orange_juice_dispenser)
```

![](https://pic3.zhimg.com/80/v2-1ad2a852a1f605533feab82769d609fe_1440w.webp)

这就是所谓的“**不变 (Invariant)**”。在 Python 中，使用 `TypeVar` 定义的类型变量默认都是“不变”的，也就是说该容器只能包含某个精确的类型，而不能包含该类型的任何父类或子类。

同理，`list`、`set` 等 Python 内置的**可变**容器类型也是不变的。

![](https://pic3.zhimg.com/80/v2-a73e1172841bce87dbeef4bc8448e806_1440w.webp)

可以看到，`list[OrangeJuice]` 也不能赋值给 `list[Juice]`.

你可能会困惑于为什么要这么设计——似乎这并不十分符合直觉。

考虑下面这段代码：

```python3
class Animal:
    ...

class Dog(Animal):
    ...

class Cat(Animal):
    ...

def add_animal(animal_list: list[Animal]):
    animal_list.append(Cat())
```

现在，让我们假设 `list[Dog]` 可以是 `list[Animal]` 的子类，也就是说现在 `list` 不再是“不变（Invariant）”的，而是自动将子类型关系传递了下来，这就是我们之后会谈到的“协变（Covariant）”。不过，在这里我们暂时不关心具体什么是“协变”，你只需要有这个直觉就可以了。

然后，考虑这段代码：

```python3
dogs: list[Dog] = [Dog(), Dog()]
add_animal(dogs)
```

如果 `list[Dog]` 确实被认为是 `list[Animal]` 的子类，那么这段代码不会报错——`add_animal` 期望接受一个 `list[Animal]`，由于 `list[Dog]` 是 `list[Animal]` 的子类，因此这是合理的。但是我们看到，现在我们意外地向一个原本只应该包含狗的列表中加入了一只猫——这显然不是我们期望的。

因此，`TypeVar` 被设计为是默认不变的，以防止这种意外情况的出现。例如在 VSCode 中，上面的代码就会报错：

![](https://pic2.zhimg.com/80/v2-732e2d01e9c9835d1a1a3f4d62f4441d_1440w.webp)

正如 mypy 给我们的提示所述——`Sequence` 类型实际上不是不变而是协变的，这是它和 `list`、`set` 这些可变序列类型的一个重要差异。

### 4.2 协变 (Covariant)

在上一节最后的例子中，你应该已经能通过直觉朴素地感知到什么是“**协变 (Covariant)**”了。现在，让我们改造一下上面的饮料贩卖机，让它更灵活些，能够贩卖橙汁：

```python3
T_co = TypeVar('T_co', covariant=True)

class BeverageDispenser(Generic[T_co]):
    """饮料贩卖机"""
    def __init__(self, beverage: T_co) -> None:
        self.beverage = beverage

    def dispense(self) -> T_co:
        return self.beverage

def install_dispenser(dispenser: BeverageDispenser[Juice]) -> None:
    """安装果汁贩卖机"""
    ...
```

实际上这里只是在定义泛型 `T` 时加上了一个 `covariant=True`，这表示 `T` 现在是协变的。

> ✨ **提示：**在这里，`T_co` 是一种约定，表明这是协变的类型参数。

现在，我们看到 `BeverageDispenser[OrangeJuice]` 就被认为是 `BeverageDispenser[Juice]` 的子类了：

![](https://pic1.zhimg.com/80/v2-0fea859416910c1be400eaa2e3fe8ae8_1440w.webp)

不过，同样的，`install_dispenser` 还是没法安装通用的饮料贩卖机，这符合我们的预期。

### 4.3 逆变 (Contravariant)

有“**协变 (Covariant)**”，自然也有“**逆变 (Contravariant)**”。正如字面意思所述，假设存在逆变类型 `C`，如果 `A` 是 `B` 的子类，那么 `C[B]` 是 `C[A]` 的子类，恰好与协变反着来。

你可能会疑惑在什么情况下需要“逆变”。事实上，函数参数就是一个典型的“逆变”例子。首先，让我们假设函数参数是协变的，看看会有什么后果。

考虑下面这段代码：

```python3
class Food:
    ...

class Chocolate(Food):
    ...

class DogFood(Food):
    ...

class Animal:
    def eat_food(self, food: Food) -> None:
        ...

class Dog(Animal):
    def eat_food(self, food: DogFood) -> None:
        ...
```

当然，这段代码实际上是会类型报错的，因为函数参数实际上是逆变的：

![](https://pic2.zhimg.com/80/v2-d2430ccac5afed3d872c6cc44fda2669_1440w.webp)

不过，在这里我们不妨假设如果这段代码成立，会有什么后果：

```python3
food: Food = Chocolate()
animals: list[Animal] = [Animal(), Dog()]
for animal in animals:
    animal.eat_food(food)
```

可以看到，在这个例子中，狗意外地食用了巧克力，而狗吃巧克力是会中毒的！但在这里，`Dog()` 由于在 `animals` 数组中，它的类型被推断为 `Animal`，这没有什么问题。然后，我们调用 `animal.eat_food`，这里传入一个 `Food`，这符合该方法的定义，也没有什么问题。但是，意外还是发生了。

这段代码在 VSCode 中会这样报错：

![](https://pic3.zhimg.com/80/v2-5b451e05d392f4e400b1b3850eb703da_1440w.webp)

因此，我们意识到函数参数显然不能是协变的。那么，“逆变”体现在哪里呢？

让我们考虑下面这段代码：

```python3
class Food:
    ...

class Pie(Food):
    def cook(self, callback: Callable[["Pie"], None]) -> None:
        ...
```

在这里，`Pie` 继承了 `Food`，并且有一个 `cook` 方法，它接受一个回调函数，表示如何烹饪这个派。

> ✨ **提示：**这里使用字符串 `"Pie"` 而不是直接使用 `Pie` 涉及到 Type hints 的前向引用语法，如果你有所遗忘，可以回头看看第 1.16 节的描述。

显然，这样的代码是行得通的：

```python3
def cook_pie(pie: Pie) -> None:
    ...

pie = Pie()
pie.cook(cook_pie)
```

但是，如果我们有一个通用的 `cook_food` 函数呢？显然，`cook_food` 也能够烹饪派，那么也应该可以将 `cook_food` 函数作为回调传入 `Pie.cook` 中：

```python3
def cook_food(food: Food) -> None:
    ...

pie = Pie()
pie.cook(cook_food)
```

在 VSCode 中，这段代码并不会报错：

![](https://pic2.zhimg.com/80/v2-bd26b061bf6c7b5fb5823a8f26fcfd61_1440w.webp)

显然，这也符合我们的预期。

我们看到，在上面这个例子中，`Callable[[Food], None]` 被认为是 `Callable[[Pie], None]` 的子类型，而 `Pie` 反而是 `Food` 的子类型。因此，我们看到，**函数参数应当是“逆变”的**。

在此稍微再扩展一点，函数的返回值应该是哪种型变呢？答案是**函数返回值应当是协变的**。这应该不难想到，你可以自己举些例子理解一下。

在函数参数外，逆变的例子似乎不像协变那么多。不过，在这里也可以举一个使用逆变的例子。

考虑一下，假设现在要对食堂垃圾桶建模，为了环保考虑，它必须存放可生物降解的废弃物。我们对其建模如下：

```python3
class Refuse:
    """任何废弃物"""

class Biodegradable(Refuse):
    """可生物降解的废弃物"""

class Compostable(Biodegradable):
    """可制成肥料的废弃物"""

T_contra = TypeVar('T_contra', contravariant=True)

class TrashCan(Generic[T_contra]):
    def put(self, refuse: T_contra) -> None:
        """在倾倒之前存放垃圾"""

def deploy(trash_can: TrashCan[Biodegradable]):
    """放置一个垃圾桶，存放可生物降解的废弃物"""
```

在这里，`deploy` 除了可以放置 `TrashCan[Biodegradable]` 外，应当还能放置 `TrashCan[Refuse]`，因为它可以存放任何废弃物，包括可生物降解的废弃物，不能是 `TrashCan[Compostable]`，因为它只能存放可制成肥料的废弃物，无法处理所有可生物降解的废弃物。

> **✨ 提示：**同理，这里的 `T_contra` 也只是一种约定，表明这是逆变的类型参数。

这是在 VSCode 中的结果：

![](https://pic2.zhimg.com/80/v2-89722027c483bd9615f2e9efeb76b77d_1440w.webp)

显然，这符合我们的预期。

### 4.4 型变总结

在这里，让我们严谨一些，以更形式化的语言来描述这些型变。

- 对于不变类型变量 `L` 来说，无论 `A` 和 `B` 之间是否存在关系，`L[A]` 都不是 `L[B]` 的父类或子类。
- 对于协变类型变量 `C` 来说，如果 `A` 是 `B` 的子类，那么 `C[A]` 也是 `C[B]` 的子类，这可以表述为 . 在这里，  表示左边的类型与与边的类型相等，或是右边类型的子类。
- 对于逆变类型变量 `K` 来说，如果 `A` 是 `B` 的子类，那么 `K[B]` 是 `K[A]` 的子类，这可以表述为 .

根据一些经验，我们可以推知某些类型的具体型变种类：

- 类型变量最好是不变的，以避免可能的意外情况出现。
- 如果某类型变量表示的是从对象中**获取**的数据类型，那么它可能是**协变**的。例如 `frozenset` 等只读容器是协变的。另外，`Iterator` 也是协变的，因为它只会产生输出。同理，函数的返回值类型也是协变的。
- 如果某类型变量表示的是对象初始化后向对象中**输入**的数据类型，那么它可能是**逆变**的。例如上文提到的 `TrashCan` 这种只写的数据结构。另外，`Generator` 等也有一个可逆变的类型变量。同理，函数参数也是逆变的。
- 如果某类型变量表示的是从对象中**获取**的数据类型，同时也是向对象中**输入**的数据类型，那么它必定是**不变**的。例如 Python 中的可变容器都是不变的。

> **✨ 提示：**实际上，除了不变、协变和逆变外，还有一种“双变（bivariance）”，意味着既是协变的也是逆变的。上面提到只读类型可以是协变的，只写类型可以是逆变的，那么可以推断不可读不可写类型应当可以是双变的，比如一个多余的未被使用的函数参数。然而，一个“不可读不可写”的数据结构显然是非常罕见的，而双变也常常导致运行时类型错误，因此在大多数编程语言中双变都几乎未被支持，也包括 Python 的 Type Hints. 除非有明确需要，否则我们也应当尽可能避免对双变的使用。

### 4.5 自动型变性推导

这是后来补充的一节。在上面的例子中，所有的类型变量都使用 `TypeVar` 定义，以避免 Python 3.12+ 中新语法产生的自动型变性推导问题——这只是为了教学目的。实际上，你现在大概已经几乎不需要考虑型变性的问题了。让我们使用 Python 3.12+ 的新语法来定义 `BeverageDispenser`：

```python3
class BeverageDispenser[T]:
    """饮料贩卖机"""

    def __init__(self, beverage: T) -> None:
        self.beverage = beverage

    def dispense(self) -> T:
        return self.beverage
```

看上去类型检查器应该能推断出 `T` 是协变的——因为它看上去在初始化后只能从中获取值（通过 `dispense`），而不会改变其中的值。

但事实并非如此：

![](https://pic3.zhimg.com/80/v2-921251e368eeff8c55cc3613bc530f5a_1440w.webp)

在这里，`T` 还是被推导为了不变的——难道 Pyright 没有实现自动型变性推导吗？实际上，这里隐藏了一个可变的属性——`self.beverage`. 在创建 `BeverageDispenser` 后，用户仍旧可以修改 `beverage` 的值，考虑这种情况：

```python3
class Beverage:
    """任何饮料"""

class Juice(Beverage):
    """任何果汁"""

class AppleJuice(Juice):
    """苹果汁"""

class OrangeJuice(Juice):
    """橙汁"""

class BeverageDispenser[T]:
    """饮料贩卖机"""
    def __init__(self, beverage: T) -> None:
        self.beverage = beverage

    def dispense(self) -> T:
        return self.beverage

def change_dispenser_beverage(dispenser: BeverageDispenser[Juice]) -> None:
    """更改贩卖的果汁"""
    dispenser.beverage = AppleJuice()

orange_juice_dispenser = BeverageDispenser(OrangeJuice())
change_dispenser_beverage(orange_juice_dispenser)  # 把橙汁更改成了苹果汁
```

在这里，假设 `T` 是协变的，那么 `change_dispenser_beverage(orange_juice_dispenser)` 就不会报错——但这实际上是类型不安全的，因为在执行了这个函数之后，橙汁贩卖机变成了苹果汁贩卖机，而这并不符合我们的预期。因此，为了安全性考虑，这里的 `T` 仍旧被推导为了不变的。

![](https://pic4.zhimg.com/80/v2-b57a8cfad91394aaaa46781885cfa867_1440w.webp)

如果使用 `_` 前缀将 `beverage` 变成私有的，静态类型检查器就会将 `T` 推导为协变的了：

```python3
class BeverageDispenser[T]:
    """饮料贩卖机"""
    def __init__(self, beverage: T) -> None:
        self._beverage = beverage

    def dispense(self) -> T:
        return self._beverage
```

![](https://pic1.zhimg.com/80/v2-9a20c44b5fa6bda8d2b7bc8988f05de8_1440w.webp)

现在你大概大致搞明白了自动型变性推导的原理。它会根据实际情况将类型变量推导为不变、协变或逆变的，参考以下例子：

```python3
class ClassA[T1, T2, T3](list[T1]):
    def method1(self, a: T2) -> None:
        ...

    def method2(self) -> T3:
        ...
```

在这个例子中，`T1` 被传递给 `list[T1]`，我们知道 `list` 是不变的，因此 `T1` 被推导为不变的；`T2` 仅被用作函数参数，因此它被推导为逆变的；`T3` 仅被用作函数返回值，因此它被推导为协变的。

当然，具体的推导过程要比这里的直觉化描述复杂一些，你可以参考 [PEP 695 – Type Parameter Syntax 的 Variance Inference 部分](https://link.zhihu.com/?target=https%3A//peps.python.org/pep-0695/)详细了解其中原理。大致上，它为每个类型变量执行以下推导过程：

```python3
# 尝试推导 `T1`
upper = ClassA[object, Dummy, Dummy]  # 使用 `object` 替代 `T1` 创建 upper
lower = ClassA[T1, Dummy, Dummy]  # 使用 `T1` 自身
# 判断 `lower` 能否赋值给 `upper`……不行
# 判断 `upper` 能否赋值给 `lower`……不行
# 确定 `T1` 是不变的

# 尝试推导 `T2`
upper = ClassA[Dummy, object, Dummy]  # 使用 `object` 替代 `T2` 创建 upper
lower = ClassA[Dummy, T2, Dummy]  # 使用 `T2` 自身
# 判断 `lower` 能否赋值给 `upper`……不行
# 判断 `upper` 能否赋值给 `lower`……可以
# 确定 `T2` 是逆变的

# 尝试推导 `T3`
upper = ClassA[Dummy, Dummy, object]  # 使用 `object` 替代 `T3` 创建 upper
lower = ClassA[Dummy, Dummy, T3]  # 使用 `T3` 自身
# 判断 `lower` 能否赋值给 `upper`……可以
# 确定 `T3` 是协变的
```

## 5 结尾

在这里引用 Guido 的一句话作为结尾。

> *I wouldn't like a version of Python where I was morally obligated to add type hints all the time. I really do think that type hints have their place but there are also plenty of times that it's not worth it, and it's so wonderful that you can choose to use them.*  
> —Guido van Rossum

Python 的 Type hints 还有不少缺陷，例如类型变量不支持默认值，不支持表示“大于 0 的数字”的类型，对元编程的支持也比较差。

不过，大多数其他编程语言的类型系统也具有与 Type hints 相似的缺陷——如 Java 和 Go 也不支持类型变量的默认值，并且几乎所有主流语言也都不支持表示“大于 0 的数字”的类型，这需要一些相当高级的类型系统特性 (Dependent type) 提供支持，而这在多数情况下是没什么必要的，只是增加了类型系统的复杂性。

在最近的版本中，Type hints 还增强了对 `Callable` 的支持，如对可变长参数的支持（通过 `TypeVarTuple`，如 `Callable[[*Args], R]`）和对高阶函数的更好支持（通过 `ParamSpec`）；并且自 Python 3.12 之后，更简洁可读的泛型语法被支持，也支持了对类型变量型变性的自动推导，已经易用不少了。

严格来说，从类型系统健壮性的角度来看，Type hints 的类型系统比 Java 和 Go 这样类型系统较弱的静态类型语言都要高级不少。除了对 Type level programming 的支持仍旧不足，和各类型检查器实现层次不齐的问题外，Type hints 已经可以被视为一门相当现代的编程语言应当具有的较高级类型系统了。如果你熟悉 TypeScript，可能会感到 Type hints 与 TypeScript 很相似，只是少了一些 Type level programming 的支持。

但严格来说，这些所谓 Type hints 的“缺陷”并不能说是 Python 的缺陷。动态类型是 Python 的一大特点，Type hints 的目的是为了方便编译器（或其他开发工具）进行类型检查，而不是把 Python 改造成一门静态语言，而目前的 Type hints 其实已经具备了令人惊讶的类型系统完善性。另外，虽然 Type hints 看起来很好，但也不应该完全依赖于它，完善的单元测试仍然是很有必要的。

事实上，在 Python 的 Type hints 语法出现之前很久，使用 Python 的大型企业就已经在使用自动化测试工具来保证代码质量了。如果 Python 程序有足够的单元测试，其可靠性不会比 Java、C++ 等语言更差。并不是只有加入静态类型检查才能编写高质量的代码，单元测试同样可以起到类似的效果。

## 参考资料

https://zhuanlan.zhihu.com/p/464979921
