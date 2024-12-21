如果您熟悉金融科技初创行业，您可能听说过总部位于英国伦敦的知名金融科技巨头Revolut。 Revolut 成立于 2015 年，已获得大量投资，成为英国发展最快的初创企业之一，为许多欧洲公民提供银行服务。

虽然银行业务在如何产生收入方面往往笼罩在神秘之中，但 Revolut 2020 年和 2021 年的一些关键数据已经揭示了其收入来源：

![革命损益表](https://hackernoon.imgix.net/images/tT78NTkPYiNmhs2Sm8rCsKqAGkv2-ur92kzq.jpeg?auto=format&fit=max&w=1920)

如图所示，这家新银行收入的很大一部分来自外汇（FX）、财富管理（包括加密货币）和卡服务。值得注意的是，2021 年，外汇成为最赚钱的行业。

我的一位朋友也是一名软件工程师，他曾经分享过一个关于他几年前在 Revolut 软件工程部门进行技术面试的有趣故事。他的任务是开发一种算法，以确定使用一种或多种中间货币转换两种货币最有利可图的方式。换句话说，他们正在寻找一种货币套利策略。

> *货币套利*是一种交易策略，其中货币交易者通过多次交易利用经纪商为特定货币对提供的不同点差。

任务中明确提到算法的基础必须植根于图论。

## 外汇基础知识

FX（即外汇）在全球贸易中发挥着关键作用，支撑着我们相互联系的世界的运作。显然，外汇在银行成为最富有的组织之一方面也发挥着重要作用。

外汇产生的利润主要是买入价（BID）和卖出价（ASK）之间的差价或点差。虽然每笔交易的这种差异可能显得微不足道，但考虑到日常运营量，它可以累积成数百万美元的利润。这使得一些公司能够仅依靠这些高度自动化的财务运营来蓬勃发展。

在 FX（外汇）领域，我们始终使用货币对，例如欧元/美元。在大多数情况下，这些交换是双向的（即欧元/美元和美元/欧元），并且每个方向的汇率值都不同。

*套利*对代表两种货币（例如欧元和美元）价值之间的数值比率，决定它们之间的汇率。

潜在地，我们可以使用多种中间货币进行有利可图的交易，这被称为*“肯定的赌注”* 。

> *套利保证赌注*是一组以循环方式使用的对。[阅读更多](https://en.wikipedia.org/wiki/Arbitrage_betting?ref=hackernoon.com)

许多提供商采用数学建模和分析来确保自己的利润并防止其他人从中获利。因此，这里可能会强调该术语。

> *确定下注长度*是指构成一组潜在套利机会的对的数量。

在现实世界中，不同银行或交易平台之间的汇率可能会有所不同。游客穿越一座城市寻找最优惠价格的情况并不少见。使用计算机软件，当您可以访问提供商列表时，此过程可以在几毫秒内完成。

在实际的盈利交易中，多个步骤可能涉及通过不同交易平台的各种货币进行兑换。换句话说，套利圈可以相当广泛。

> *套利圈*是获取一种货币，将其转移到另一个平台，与其他货币进行兑换，最终返回到原始货币。

两种货币之间通过一种或多种中间货币进行的汇率计算为*这些中间交易的汇率的乘积*。

## 一个例子

例如，假设我们想用美元购买瑞士法郎，然后将法郎兑换成日元，然后再次出售日元换取美元。在 2023 年 秋季，我们有以下汇率：

1. 我们可以用 1 美元购买 0.91 CHF（瑞士法郎）。

2. 我们可以用 1 瑞士法郎购买 163.16 日元。

3. 我们可以用 1 日元购买 0.0067 美元。

让我们用一个表格来展示它：

```bash
1           USD |   1           CHF |   1       YEN
0.91        CHF |   163.16      YEN |   0.0067  USD
----------------|-------------------|--------------
1.098901099     |   0.006128953     |   149.2537313 
```

现在，我们需要找到这些值的乘积。*当该产品产生的值小于 1 时，一系列交易变得有利可图*：

```bash
 1.098901099 * 0.006128953 * 149.2537313 = 1.005240803
```

我们可以看到结果大于 1，所以看起来我们损失了 0.05% 的钱。但具体有多少呢？我们可以这样整理：

```bash
 0.91 CHF * 163.16 (YEN per 1 CHF) * 0.0067 (USD per 1 YEN) = 0.99478652 US Dollars
```

因此，一开始卖出 1 美元后，我们最终得到 0.994 - 不到 1 美元。

> 简单来说，当可以用少于一单位的相同货币获得一单位的货币时，套利周期就有利可图。

假设我们发现有机会在初始交易中每 1 美元收取 0.92 瑞士法郎，而不是 0.91 瑞士法郎：

```bash
1           USD |   1           CHF |   1       YEN
0.92        CHF |   163.16      YEN |   0.0067  USD
----------------|-------------------|--------------
1.086956522     |   0.006128953     |   149.2537313 
```

乘积将小于 1：

```bash
 1.086956522 * 0.006128953 * 149.2537313 = 0.994314272
```

这意味着，以实际货币计算，它会给我们带来超过 1 美元的收益：

```bash
 0.92 CHF * 163.16 (YEN per 1 CHF) * 0.0067 (USD per 1 YEN) = 1.00571824 US Dollars
```

Wuolah，*我们得到了一些利润！*现在，让我们看看如何使用图形分析来自动化此操作。

因此，检查 3 个套利对的套利圈中的利润或损失的公式如下所示：

```bash
 USD/CHF * CHF/YEN * YEN/USD < 1.0
```

## 图形表示

为了自动化这些过程，我们可以使用图表。前面提到的表格可以自然地转化为图的矩阵表示，其中节点代表货币，边代表双向交换。

因此，在矩阵中表示两对交换很简单，如下所示：

```bash
EUR  USD
 1    1  EUR 
 1    1  USD
```

根据所涉及的对的数量，我们的矩阵可以扩展：

```bash
EUR  USD  YEN  CHF  
 1    1    1    1  EUR 
 1    1    1    1  USD
 1    1    1    1  YEN
 1    1    1    1  CHF
```

因此，如果我们考虑更多的交易平台和资源，即使只有两种货币，我们的桌子也会变得相当大。

为了解决实际的货币套利问题，通常使用包含货币报价的所有关系的完整图表。三种货币兑换表可能如下所示：

```bash
   USD     CHF     YEN
{ 1.0,    1.10,   0.0067 }  USD
{ 0.91,   1.0,    0.0061 }  CHF
{ 148.84, 163.16, 1.0    }  YEN
```

我们可以使用一个简单的[图形数据结构](https://github.com/optiklab/negative-cycles-in-a-graph/blob/main/pathFindingBase.h?ref=hackernoon.com)来表示内存中的货币对：

```csharp
 class GraphNode { public: string Name; }; class Graph { public: vector<vector<double>> Matrix; vector<GraphNode> Nodes; };
```

现在，我们只需要找出如何遍历这个图并找到最有利可图的圈子。但还有一个问题...

## 数学再次拯救我们

经典图算法不太适合处理*边长的乘积*，因为它们旨在查找*定义为这些长度之和的*路径（请参阅任何众所周知的经典路径查找算法[BFS、DFS、Dijkstra 甚至A 星](https://antonyarkov.substack.com/p/universal-implementation-of-bfs-dfs?ref=hackernoon.com)）。

然而，为了规避这一限制，有一种数学方法可以将乘积转换为和：对数。如果乘积出现在对数下，则可以将其转换为对数之和。

![对数](https://hackernoon.imgix.net/images/tT78NTkPYiNmhs2Sm8rCsKqAGkv2-8ta2k4t.png?auto=format&fit=max&w=1080)

在这个等式的右侧，所需的数字小于一，表明该数字的对数必须小于零：

```bash
 USD/CHF * CHF/YEN * YEN/USD < 1.0
 LogE(USD/CHF * CHF/YEN * YEN/USD) < LogE(1.0)
 LogE(USD/CHF) + LogE(CHF/YEN) + LogE(YEN/USD) < 0.0
 #LogE(USD/CHF) * LogE(CHF/YEN) * LogE(YEN/USD) < 0.0
```

这个简单的数学技巧使我们能够从搜索边长*乘积*小于 1 的环路转变*为搜索边长总和小于零的环路*。

我们的矩阵值转换为 LogE(x) 并在点后舍入 2 位数字，现在如下所示：

```bash
   USD      CHF     YEN
{ 0.0,      0.1,     -5.01 }  USD
{ -0.09,    0.0,     -5.1  }  CHF
{ 5.0,      5.09,    0.0   }  YEN
```

```bash
  aptos     usdt      btc
{ 0.0,      0.0,     -5.01 }  aptos
{ 0.0,      0.0,     -5.1  }  usdt 
{ 5.0,      5.09,    0.0   }  btc
```

现在，使用经典图算法可以更容易地解决这个问题。我们需要的是遍历图表寻找最有利可图的交换路径。

## 图算法

每种算法都有其局限性。我在[上一篇文章](https://antonyarkov.substack.com/p/universal-implementation-of-bfs-dfs?ref=hackernoon.com)中提到过其中一些。

我们不能在这里应用经典的 BFS、DFS 甚至 Dijkstra，因为我们的图可能包含负权重，这可能会在遍历图时导致*负循环*。负循环对算法提出了挑战，因为它在每次迭代中不断找到更好的解决方案。

为了解决这个问题，贝尔曼-福特算法简单地限制了迭代次数。它在一个循环中遍历图的每条边，并对所有边应用松弛不超过 V-1 次（其中 V 是节点数）。

因此，贝尔曼-福特算法是该套利系统的核心，因为它能够发现图中两个节点之间满足两个基本标准的路径：它们包含负权重并且不是负循环的一部分。

虽然这个算法在理论上很简单（你可以找到数十亿个关于它的视频），但满足我们的需求的实际实现需要一些努力。让我们深入研究一下。

## 贝尔曼-福特算法实现

> 由于本文的目的是计算机科学，因此我将使用与真实汇率无关的假想汇率。

为了更顺利地介绍该算法，让我们使用一个完全不包含负循环的图：

```csharp
graph.Nodes.push_back({ "USD" });
graph.Nodes.push_back({ "CHF" });
graph.Nodes.push_back({ "YEN" });
graph.Nodes.push_back({ "GBP" });
graph.Nodes.push_back({ "CNY" });
graph.Nodes.push_back({ "EUR" });
// Define exchange rates for pairs of currencies below
//                 USD    CHF   YEN   GBP   CNY   EUR
graph.Matrix = { { 0.0,   0.41, INF,  INF,  INF,  0.29 },  // USD
                 { INF,   0.0,  0.51, INF,  0.32, INF },   // CHF
                 { INF,   INF,  0.0,  0.50, INF,  INF },   // YEN
                 { 0.45,  INF,  INF,  0.0,  INF,  -0.38 }, // GBP
                 { INF,   INF,  0.32, 0.36, 0.0,  INF },   // CNY
                 { INF, -0.29,  INF,  INF,  0.21, 0.0 } }; // EUR
```

当图形缺少负循环时，下面的代码示例使用 Bellman-Ford 算法查找两个节点之间的路径：

```csharp
vector<double> _shortestPath;
vector<int> _previousVertex;

void FindPath(Graph& graph, int start)
{
    int verticesNumber = graph.Nodes.size();

    _shortestPath.resize(verticesNumber, INF);
    _previousVertex.resize(verticesNumber, -1);

    _shortestPath[start] = 0;

    // For each vertex, apply relaxation for all the edges V - 1 times.
    for (int k = 0; k < verticesNumber - 1; k++)
        for (int from = 0; from < verticesNumber; from++)
            for (int to = 0; to < verticesNumber; to++)
                if (_shortestPath[to] > _shortestPath[from] + graph.Matrix[from][to])
                {
                    _shortestPath[to] = _shortestPath[from] + graph.Matrix[from][to];
                    _previousVertex[to] = from;
                }
}
```

针对人民币运行此代码会填充*\_previousVertex*数组并产生如下结果：

```csharp
Path from 4 to 0 is : 4(CNY) 3(GBP) 0(USD)
Path from 4 to 1 is : 4(CNY) 3(GBP) 5(EUR) 1(CHF)
Path from 4 to 2 is : 4(CNY) 3(GBP) 5(EUR) 1(CHF) 2(YEN)
Path from 4 to 3 is : 4(CNY) 3(GBP)
Path from 4 to 4 is : 4(CNY)
Path from 4 to 5 is : 4(CNY) 3(GBP) 5(EUR)
```

正如您所观察到的，它确定了人民币与各种其他货币之间的最佳路径。

> 再说一次，我不会专注于只找到一个最好的，因为这是相对简单的任务，而不是本文的目标。

上述实现在理想情况下效果很好，但在处理包含负循环的图形时效果不佳。

## 检测负循环

我们真正需要的是能够识别图表是否包含负循环，如果是，则查明有问题的部分。这些知识使我们能够减轻这些问题并最终发现有利可图的链条。

迭代次数并不总是必须精确地达到 V - 1。如果在第 (N+1) 个循环中没有发现比第 N 个循环中的路径更好的路径，则认为找到了解决方案。因此，还有轻微优化的空间。

前面提到的代码可以增强，不仅可以找到路径，还可以检测图是否包含负循环，包括我提到的优化：

```csharp
vector<double> _shortestPath;
vector<int> _previousVertex;

bool ContainsNegativeCycles(Graph& graph, int start)
{
    int verticesNumber = graph.Nodes.size();

    _shortestPath.resize(verticesNumber, INF);
    _previousVertex.resize(verticesNumber, -1);

    _shortestPath[start] = 0;

    // For each vertex, apply relaxation for all the edges V - 1 times.
    for (int k = 0; k < verticesNumber - 1; k++)
    {
        updated = false;
        for (int from = 0; from < verticesNumber; from++)
        {
            for (int to = 0; to < verticesNumber; to++)
            {
                if (_shortestPath[to] > _shortestPath[from] + graph.Matrix[from][to])
                {
                    _shortestPath[to] = _shortestPath[from] + graph.Matrix[from][to];
                    _previousVertex[to] = from;
                    updated = true;
                }
            }
        }
        if (!updated) // No changes in paths, means we can finish earlier.
            break;
    }

    // Run one more relaxation step to detect which nodes are part of a negative cycle. 
    if (updated)
        for (int from = 0; from < verticesNumber; from++)
            for (int to = 0; to < verticesNumber; to++)
                if (_shortestPath[to] > _shortestPath[from] + graph.Matrix[from][to])
                    // A negative cycle has occurred if we can find a better path beyond the optimal solution.
                    return true;

    return false;
}
```

现在我们使用一个更复杂的图表，其中包括负循环：

```csharp
graph.Nodes.push_back({ "USD" }); // 1 (Index = 0)
graph.Nodes.push_back({ "CHF" });
graph.Nodes.push_back({ "YEN" });
graph.Nodes.push_back({ "GBP" });
graph.Nodes.push_back({ "CNY" });
graph.Nodes.push_back({ "EUR" });
graph.Nodes.push_back({ "XXX" });
graph.Nodes.push_back({ "YYY" }); // 8  (Index = 7)
//                 USD  CHF  YEN  GBP   CNY  EUR  XXX  YYY
graph.Matrix = { { 0.0, 1.0, INF, INF,  INF, INF, INF, INF },   // USD
                 { INF, 0.0, 1.0, INF,  INF, 4.0, 4.0, INF },   // CHF
                 { INF, INF, 0.0, INF,  1.0, INF, INF, INF },   // YEN
                 { INF, INF, 1.0, 0.0,  INF, INF, INF, INF },   // GBP
                 { INF, INF, INF, -3.0, 0.0, INF, INF, INF },   // CNY
                 { INF, INF, INF, INF,  INF, 0.0, 5.0, 3.0 },   // EUR
                 { INF, INF, INF, INF,  INF, INF, 0.0, 4.0 },   // XXX
                 { INF, INF, INF, INF,  INF, INF, INF, 0.0 } }; // YYY
```

我们的程序只是停止并显示一条消息：

```bash
 Graph contains negative cycle.
```

我们能够指出问题，但是，我们需要浏览图表中有问题的部分。

## 避免负循环

为了实现这一点，我们将使用常量值 NEG\_INF 标记属于负循环一部分的顶点：

```csharp
bool FindPathsAndNegativeCycles(Graph& graph, int start)
{
    int verticesNumber = graph.Nodes.size();
    _shortestPath.resize(verticesNumber, INF);
    _previousVertex.resize(verticesNumber, -1);
    _shortestPath[start] = 0;

    for (int k = 0; k < verticesNumber - 1; k++)
        for (int from = 0; from < verticesNumber; from++)
            for (int to = 0; to < verticesNumber; to++)
            {
                if (graph.Matrix[from][to] == INF) // Edge not exists
                {
                    continue;
                }

                if (_shortestPath[to] > _shortestPath[from] + graph.Matrix[from][to])
                {
                    _shortestPath[to] = _shortestPath[from] + graph.Matrix[from][to];
                    _previousVertex[to] = from;
                }
            }

    bool negativeCycles = false;

    for (int k = 0; k < verticesNumber - 1; k++)
        for (int from = 0; from < verticesNumber; from++)
            for (int to = 0; to < verticesNumber; to++)
            {
                if (graph.Matrix[from][to] == INF) // Edge not exists
                {
                    continue;
                }

                if (_shortestPath[to] > _shortestPath[from] + graph.Matrix[from][to])
                {
                    _shortestPath[to] = NEG_INF;
                    _previousVertex[to] = -2;
                    negativeCycles = true;
                }
            }
    return negativeCycles;
}
```

现在，如果我们在 \_shortestPath 数组中遇到 NEG\_INF，我们可以显示一条消息并跳过该段，同时仍然确定其他货币的最佳解决方案。例如，对于节点 0（代表美元）：

```bash
Graph contains negative cycle.
Path from 0 to 0 is : 0(USD)
Path from 0 to 1 is : 0(USD) 1(CHF)
Path from 0 to 2 is : Infinite number of shortest paths (negative cycle).
Path from 0 to 3 is : Infinite number of shortest paths (negative cycle).
Path from 0 to 4 is : Infinite number of shortest paths (negative cycle).
Path from 0 to 5 is : 0(USD) 1(CHF) 5(EUR)
Path from 0 to 6 is : 0(USD) 1(CHF) 6(XXX)
Path from 0 to 7 is : 0(USD) 1(CHF) 5(EUR) 7(YYY)
```

S哇啦！尽管我们的数据“有点脏”，但我们的代码能够识别许多有利可图的链。上面提到的所有代码示例（包括测试数据）都在[我的 GitHub](https://github.com/optiklab/negative-cycles-in-a-graph?ref=hackernoon.com)上与您共享。

## 即使很小的波动也很重要

现在让我们巩固一下所学的内容。给定三种货币的汇率列表，我们可以轻松检测负周期：

```csharp
graph.Nodes.push_back({ "USD" }); // 1 (Index = 0)
graph.Nodes.push_back({ "CHF" });
graph.Nodes.push_back({ "YEN" }); // 3 (Index = 2)

// LogE(x) table:   USD      CHF     YEN
graph.Matrix = { { 0.0,    0.489,  -0.402 },   // USD
                 { -0.489, 0.0,    -0.891 },   // CHF
                 { 0.402,  0.89,   0.0    } }; // YEN
from = 0;
FindPathsAndNegativeCycles(graph, from);
```

结果：

```bash
Graph contains negative cycle.
Path from 0 to 0 is: Infinite number of shortest paths (negative cycle).
Path from 0 to 1 is: Infinite number of shortest paths (negative cycle).
Path from 0 to 2 is: Infinite number of shortest paths (negative cycle).
```

然而，即使汇率发生微小变化（即矩阵调整）也可能导致显着差异：

```csharp
// LogE(x) table:   USD      CHF     YEN
graph.Matrix = { { 0.0,    0.490,  -0.402 },    // USD
                 { -0.489, 0.0,    -0.891 },    // CHF
                 { 0.403,  0.891,   0.0    } }; // YEN
from = 0;
FindPathsAndNegativeCycles(graph, from);
```

看，我们找到了一条有利可图的链条：

```bash
Path from 0 to 0 is : 0(USD)
Path from 0 to 1 is : 0(USD) 2(YEN) 1(CHF)
Path from 0 to 2 is : 0(USD) 2(YEN)
```

我们可以将这些概念应用于更大的图表，涉及多种货币：

```csharp
graph.Nodes.push_back({ "USD" }); // 1 (Index = 0)
graph.Nodes.push_back({ "CHF" });
graph.Nodes.push_back({ "YEN" });
graph.Nodes.push_back({ "GBP" });
graph.Nodes.push_back({ "CNY" }); // 5  (Index = 4)
// LogE(x) table:  USD     CHF     YEN    GBP   CNY
graph.Matrix = { { 0.0,    0.490, -0.402, 0.7,  0.413 },   // USD
                 { -0.489, 0.0,   -0.891, 0.89, 0.360 },   // CHF
                 { 0.403,  0.891,  0.0,   0.91, 0.581 },   // YEN
                 { 0.340,  0.405,  0.607, 0.0,  0.72 },    // GBP
                 { 0.403,  0.350,  0.571, 0.71, 0.0 } };   // CNY
from = 0;
runDetectNegativeCycles(graph, from);
```

因此，我们可能会找到多个候选者来获取利润：

```bash
Path from 0 to 0 is : 0(USD)
Path from 0 to 1 is : 0(USD) 2(YEN) 1(CHF)
Path from 0 to 2 is : 0(USD) 2(YEN)
Path from 0 to 3 is : 0(USD) 2(YEN) 3(GBP)
Path from 0 to 4 is : 0(USD) 2(YEN) 4(CNY)
```

![斯克鲁奇·麦克老鸭](https://hackernoon.imgix.net/images/tT78NTkPYiNmhs2Sm8rCsKqAGkv2-aeb2kff.jpeg?auto=format&fit=max&w=1920)

不过，有两个重要因素：

1. 时间是实施套利过程的关键因素，主要是由于货币价格的快速波动。因此，确定赌注的寿命非常短暂。

2. 平台对每笔交易收取佣金。

因此，通过限制确定赌注的长度来实现*最小化时间成本*和*减少佣金*至关重要。

经验表明，可接受的确定下注长度通常为 2 到 3 对。除此之外，计算要求不断升级，交易平台收取更大的佣金。

因此，要赚取收入并不足以拥有这些技术，还需要获得低水平的佣金。通常，只有大型金融机构手中才有这样的资源。

## 使用智能合约实现自动化

我深入研究了外汇操作的逻辑以及如何从中获取利润，但我还没有触及用于执行这些操作的技术。虽然这个话题有点偏离主题，但我不能忽略提及智能合约。

使用智能合约是当今进行外汇操作最具创新性的方式之一。智能合约可实现实时外汇操作，无需延迟或人为干预（智能合约的创建除外）。

Solidity 是一种专门的编程语言，用于创建智能合约，使涉及加密货币的金融操作自动化。智能合约的世界是动态的，并受到快速的技术变革和不断变化的法规的影响。这是一个有着相当大的炒作和与钱包和法律合规相关的重大风险的领域。

虽然毫无疑问有才华横溢的个人和团队从这一领域获利，但也有监管机构努力确保市场规则得到维护。

## 我们为什么要调查这个？

尽管全球经济复杂、晦涩且不可预测，外汇仍然是金融世界的隐藏驱动力。它是一个关键要素，使全世界数以千计的公司和数以百万计的个人能够超越国界以和平的方式合作、提供服务并互惠互利。

当然，政治、监管和央行等多种因素都会影响汇率和外汇效率。这些复杂性使得金融格局错综复杂。然而，我们必须相信这些复杂性有助于实现共同利益的更大目标。

许多科学论文深入研究了全球经济中汇率的存在和决定，仅举几例：

+ [进口商、出口商和汇率脱节](https://www.aeaweb.org/articles?id=10.1257%2Faer.104.7.1942&ref=hackernoon.com)

+ [货币选择和汇率传递](https://www.aeaweb.org/articles?id=10.1257%2Faer.100.1.304&ref=hackernoon.com)

+ [汇率难题与政策](https://repositoriodigital.bcentral.cl/xmlui/handle/20.500.12580/7504?ref=hackernoon.com)

这些论文阐明了外汇的一些基本机制，但这些机制仍然难以理解并融入一种模型。

不过，玩代码并尝试找到实际问题的解决方案帮助我获得了更多线索。我希望你和我一样喜欢这次小小的探索之旅。

敬请关注！

## 链接

+ [包含所有这些示例的源代码](https://github.com/optiklab/negative-cycles-in-a-graph/?ref=hackernoon.com)
+ Sedgewick R. - C 语言算法，第 5 部分：图算法
+ [贝尔曼福特算法代码实现](https://www.youtube.com/watch?v=24HziTZ8_xo&ref=hackernoon.com)
+ [William Fiset 的 GitHub 示例 - Bellman Ford On Adjacency Matrix](https://github.com/williamfiset/Algorithms/blob/master/src/main/java/com/williamfiset/algorithms/graphtheory/BellmanFordAdjacencyMatrix.java?ref=hackernoon.com)
+ [William Fiset 的 GitHub 示例 - Bellman Ford On Edge List](https://github.com/williamfiset/Algorithms/blob/master/src/main/java/com/williamfiset/algorithms/graphtheory/BellmanFordEdgeList.java?ref=hackernoon.com)