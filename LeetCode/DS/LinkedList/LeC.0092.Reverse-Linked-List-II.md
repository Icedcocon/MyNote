# LeC.0092.Reverse-Linked-List-II

## 题目

Reverse a linked list from position m to n. Do it in one-pass.

Note: 1 ≤ m ≤ n ≤ length of list.

Example:

```
Input: 1->2->3->4->5->NULL, m = 2, n = 4
Output: 1->4->3->2->5->NULL
```

## 题目大意

给定 2 个链表中结点的位置 m, n，反转这个两个位置区间内的所有结点。

## 解题思路

由于有可能整个链表都被反转，所以构造一个新的头结点指向当前的头。之后的处理方法是：找到第一个需要反转的结点的前一个结点 p，从这个结点开始，依次把后面的结点用“头插”法，插入到 p 结点的后面。循环次数用 n-m 来控制。

这一题结点可以原地变化，更改各个结点的 next 指针就可以。不需要游标 p 指针。因为每次逆序以后，原有结点的相对位置就发生了变化，相当于游标指针已经移动了，所以不需要再有游标 p = p.Next 的操作了。

**示例 1：**

![](https://assets.leetcode.com/uploads/2021/02/19/rev2ex2.jpg)

```
输入：head = [1,2,3,4,5], left = 2, right = 4
输出：[1,4,3,2,5]
```

**示例 2：**

```
输入：head = [5], left = 1, right = 1
输出：[5]
```

**提示：**

- 链表中节点数目为 `n`
- `1 <= n <= 500`
- `-500 <= Node.val <= 500`
- `1 <= left <= right <= n`

**进阶：** 你可以使用一趟扫描完成反转吗？

**题解**

```go
// === 头插法 ===
func reverseBetween(head *ListNode, left int, right int) *ListNode {
    dummyNode := &ListNode{Val: -1, Next: head}
    var prev *ListNode = dummyNode
    for i := 0; i < left-1; i++ {
        prev = prev.Next
    }
    cur := prev.Next
    for i := 0; i < right-left; i++ {
        next := cur.Next
        cur.Next = next.Next
        next.Next = prev.Next
        prev.Next = next
    }
    return dummyNode.Next
}
// === 常规 ===
func reverseBetween(head *ListNode, left int, right int) *ListNode {
    dummyNode := &ListNode{Val: -1, Next: head}
    var prev *ListNode = dummyNode
    for i := 0; i < left-1; i++ {
        prev = prev.Next
    }
    var pre, cur *ListNode = prev, prev.Next
    for i := 0; i <= right-left; i++ {
        next := cur.Next
        cur.Next = pre
        pre = cur
        cur = next
    }
    prev.Next.Next = cur
    prev.Next = pre
    return dummyNode.Next
}
```
