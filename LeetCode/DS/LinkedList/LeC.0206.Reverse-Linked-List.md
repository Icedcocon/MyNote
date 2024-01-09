# LeC.0206.Reverse-Linked-List

## 题目

Reverse a singly linked list.

## 题目大意

翻转单链表

## 解题思路

按照题意做即可。

**示例 1：**

![](https://assets.leetcode.com/uploads/2021/02/19/rev1ex1.jpg)

```
输入：head = [1,2,3,4,5]
输出：[5,4,3,2,1]
```

**示例 2：**

![](https://assets.leetcode.com/uploads/2021/02/19/rev1ex2.jpg)

```
输入：head = [1,2]
输出：[2,1]
```

**示例 3：**

```
输入：head = []
输出：[]
```

**提示：**

- 链表中节点的数目范围是 `[0, 5000]`
- `-5000 <= Node.val <= 5000`

**进阶：**链表可以选用迭代或递归方式完成反转。你能否用两种方法解决这道题？

**题解**

```go
// === 迭代 ===
func reverseList(head *ListNode) *ListNode {
    var prev *ListNode
    for head != nil {
        next := head.Next
        head.Next = prev
        prev = head
        head = next
    }
    return prev
}
// === 递归 ===
func reverseList(head *ListNode) *ListNode {
    var dfs func(prev, cur *ListNode) *ListNode
    dfs = func(prev, cur *ListNode) *ListNode {
        if cur == nil {
            return prev
        }
        next := cur.Next
        cur.Next = prev
        return dfs(cur, next)
    }
    return dfs(nil, head)
}
// === 递归 ===
func reverseList(head *ListNode) *ListNode {
    if head == nil || head.Next == nil {
        return head
    }
    newHead := reverseList(head.Next)
    head.Next.Next = head
    head.Next = nil
    return newHead
}
```
