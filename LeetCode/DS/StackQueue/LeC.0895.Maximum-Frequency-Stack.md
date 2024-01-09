# LeC.0895.Maximum-Frequency-Stack

## 题目

Implement FreqStack, a class which simulates the operation of a stack-like data structure.

FreqStack has two functions:

push(int x), which pushes an integer x onto the stack.
pop(), which removes and returns the most frequent element in the stack.  
If there is a tie for most frequent element, the element closest to the top of the stack is removed and returned.

Example 1:

```c
Input: 
["FreqStack","push","push","push","push","push","push","pop","pop","pop","pop"],
[[],[5],[7],[5],[7],[4],[5],[],[],[],[]]
Output: [null,null,null,null,null,null,null,5,7,5,4]
Explanation:
After making six .push operations, the stack is [5,7,5,7,4,5] from bottom to top.  Then:

pop() -> returns 5, as 5 is the most frequent.
The stack becomes [5,7,5,7,4].

pop() -> returns 7, as 5 and 7 is the most frequent, but 7 is closest to the top.
The stack becomes [5,7,5,4].

pop() -> returns 5.
The stack becomes [5,7,4].

pop() -> returns 4.
The stack becomes [5,7].
```

Note:

- Calls to FreqStack.push(int x) will be such that 0 <= x <= 10^9.
- It is guaranteed that FreqStack.pop() won't be called if the stack has zero elements.
- The total number of FreqStack.push calls will not exceed 10000 in a single test case.
- The total number of FreqStack.pop calls will not exceed 10000 in a single test case.
- The total number of FreqStack.push and FreqStack.pop calls will not exceed 150000 across all test cases.

## 题目大意

实现 FreqStack，模拟类似栈的数据结构的操作的一个类。

FreqStack 有两个函数：

- push(int x)，将整数 x 推入栈中。
- pop()，它移除并返回栈中出现最频繁的元素。如果最频繁的元素不只一个，则移除并返回最接近栈顶的元素。

## 解题思路

FreqStack 里面保存频次的 map 和相同频次 group 的 map。push 的时候动态的维护 x 的频次，并更新到对应频次的 group 中。pop 的时候对应减少频次字典里面的频次，并更新到对应频次的 group 中。

**示例 1：**

```
输入：
["FreqStack","push","push","push","push","push","push","pop","pop","pop","pop"],
[[],[5],[7],[5],[7],[4],[5],[],[],[],[]]
输出：[null,null,null,null,null,null,null,5,7,5,4]
解释：
FreqStack = new FreqStack();
freqStack.push (5);//堆栈为 [5]
freqStack.push (7);//堆栈是 [5,7]
freqStack.push (5);//堆栈是 [5,7,5]
freqStack.push (7);//堆栈是 [5,7,5,7]
freqStack.push (4);//堆栈是 [5,7,5,7,4]
freqStack.push (5);//堆栈是 [5,7,5,7,4,5]
freqStack.pop ();//返回 5 ，因为 5 出现频率最高。堆栈变成 [5,7,5,7,4]。
freqStack.pop ();//返回 7 ，因为 5 和 7 出现频率最高，但7最接近顶部。堆栈变成 [5,7,5,4]。
freqStack.pop ();//返回 5 ，因为 5 出现频率最高。堆栈变成 [5,7,4]。
freqStack.pop ();//返回 4 ，因为 4, 5 和 7 出现频率最高，但 4 是最接近顶部的。堆栈变成 [5,7]。
```

**提示：**

- `0 <= val <= 109`
- `push` 和 `pop` 的操作数不大于 `2 * 104`。
- 输入保证在调用 `pop` 之前堆栈中至少有一个元素。

**题解**

```go
type FreqStack struct {
    freq    map[int]int
    group   map[int][]int
    maxFreq int
}

func Constructor() FreqStack {
    return FreqStack{map[int]int{}, map[int][]int{}, 0}
}

func (f *FreqStack) Push(val int) {
    f.freq[val]++
    f.group[f.freq[val]] = append(f.group[f.freq[val]], val)
    f.maxFreq = max(f.maxFreq, f.freq[val])
}

func (f *FreqStack) Pop() int {
    ans := f.group[f.maxFreq][len(f.group[f.maxFreq])-1]
    f.freq[ans]--
    f.group[f.maxFreq] = f.group[f.maxFreq][:len(f.group[f.maxFreq])-1]
    if len(f.group[f.maxFreq]) == 0 {
        f.maxFreq--
    }
    return ans
}
```
