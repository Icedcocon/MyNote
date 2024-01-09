# LeC.0225.Implement-Stack-using-Queues

## 题目

Implement the following operations of a stack using queues.

- push(x) -- Push element x onto stack.
- pop() -- Removes the element on top of the stack.
- top() -- Get the top element.
- empty() -- Return whether the stack is empty.

Example :

```c
MyStack stack = new MyStack();

stack.push(1);
stack.push(2);  
stack.top();   // returns 2
stack.pop();   // returns 2
stack.empty(); // returns false
```

Note:  

- You must use only standard operations of a queue -- which means only push to back, peek/pop from front, size, and is empty operations are valid.
- Depending on your language, queue may not be supported natively. You may simulate a queue by using a list or deque (double-ended queue), as long as you use only standard operations of a queue.
- You may assume that all operations are valid (for example, no pop or top operations will be called on an empty stack).

## 题目大意

题目要求用队列实现一个栈的基本操作：push(x)、pop()、top()、empty()。

## 解题思路

按照题目要求实现即可。

**示例：**

```
输入：
["MyStack", "push", "push", "top", "pop", "empty"]
[[], [1], [2], [], [], []]
输出：
[null, null, null, 2, 2, false]

解释：
MyStack myStack = new MyStack();
myStack.push(1);
myStack.push(2);
myStack.top(); // 返回 2
myStack.pop(); // 返回 2
myStack.empty(); // 返回 False
```

**提示：**

- `1 <= x <= 9`
- 最多调用`100` 次 `push`、`pop`、`top` 和 `empty`
- 每次调用 `pop` 和 `top` 都保证栈不为空

```go
//  ===== 双队列 =====
type MyStack struct {
    inqueue, dequeue []int
}

func Constructor() MyStack {
    return MyStack{make([]int, 0), make([]int, 0)}
}

func (this *MyStack) Push(x int) {
    this.inqueue = append(this.inqueue, x)
}

func (this *MyStack) Pop() int {
    length := len(this.inqueue)
    for i := 0; i < length-1; i++ {
        this.dequeue = append(this.dequeue, this.inqueue[0])
        this.inqueue = this.inqueue[1:]
    }
    ans := this.inqueue[0]
    this.inqueue = this.dequeue
    this.dequeue = nil
    return ans
}

func (this *MyStack) Top() int {
    ans := this.Pop()
    this.inqueue = append(this.inqueue, ans)
    return ans
}

func (this *MyStack) Empty() bool {
    return len(this.inqueue) == 0
}

//  ===== 单队列 =====

type MyStack struct {
    queue  []int
    length int
}

func Constructor() MyStack {
    return MyStack{make([]int, 0), 0}
}

func (this *MyStack) Push(x int) {
    this.queue = append(this.queue, x)
    this.length++
}

func (this *MyStack) Pop() int {
    for i := 0; i < this.length-1; i++ {
        this.queue = append(this.queue, this.queue[0])
        this.queue = this.queue[1:]
    }
    ans := this.queue[0]
    this.queue = this.queue[1:]
    this.length--
    return ans
}

func (this *MyStack) Top() int {
    ans := this.Pop()
    this.queue = append(this.queue, ans)
    this.length++
    return ans
}

func (this *MyStack) Empty() bool {
    return len(this.queue) == 0
}
```
