# LeC.0155.Min-Stack

## 题目

Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

push(x) -- Push element x onto stack.
pop() -- Removes the element on top of the stack.
top() -- Get the top element.
getMin() -- Retrieve the minimum element in the stack.

Example:

```c
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin();   --> Returns -3.
minStack.pop();
minStack.top();      --> Returns 0.
minStack.getMin();   --> Returns -2.
```

## 题目大意

这道题是一个数据结构实现题。要求实现一个栈的类，实现 push()、pop()、top()、getMin()。

## 解题思路

按照题目要求实现即可。

**示例 1:**

```
输入：
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]

输出：
[null,null,null,null,-3,null,0,-2]

解释：
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin();   --> 返回 -3.
minStack.pop();
minStack.top();      --> 返回 0.
minStack.getMin();   --> 返回 -2.
```

**提示：**

- `-231 <= val <= 231 - 1`
- `pop`、`top` 和 `getMin` 操作总是在 **非空栈** 上调用
- `push`, `pop`, `top`, and `getMin`最多被调用 `3 * 104` 次

**题解**

```go
==== 辅助栈 ====

type MinStack struct {
    elements, minEls []int
    length           int
}

func Constructor() MinStack {
    return MinStack{make([]int, 0), make([]int, 0), 0}
}

func (this *MinStack) Push(val int) {
    this.elements = append(this.elements, val)
    if this.length == 0 {
        this.minEls = append(this.minEls, val)
    } else {
        this.minEls = append(this.minEls, min(this.GetMin(), val))
    }
    this.length++
}

func (this *MinStack) Pop() {
    this.length--
    this.elements = this.elements[:this.length]
    this.minEls = this.minEls[:this.length]
}

func (this *MinStack) Top() int {
    return this.elements[this.length-1]
}

func (this *MinStack) GetMin() int {
    return this.minEls[this.length-1]
}

==== 单一栈 ====

type MinStack struct {
    elements [][2]int
    length   int
}

func Constructor() MinStack {
    return MinStack{make([][2]int, 0), 0}
}

func (this *MinStack) Push(val int) {
    if this.length == 0 {
        this.elements = append(this.elements, [2]int{val, val})
    } else {
        this.elements = append(this.elements, [2]int{val, min(val, this.GetMin())})
    }
    this.length++
}

func (this *MinStack) Pop() {
    this.length--
    this.elements = this.elements[:this.length]
}

func (this *MinStack) Top() int {
    return this.elements[this.length-1][0]
}

func (this *MinStack) GetMin() int {
    return this.elements[this.length-1][1]
}
```
