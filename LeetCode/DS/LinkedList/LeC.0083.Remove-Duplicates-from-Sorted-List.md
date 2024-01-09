# LeC.0083.Remove-Duplicates-from-Sorted-List

## 题目

Given a sorted linked list, delete all duplicates such that each element appear only once.

Example 1:

```
Input: 1->1->2
Output: 1->2
```

Example 2:

```
Input: 1->1->2->3->3
Output: 1->2->3
```

## 题目大意

删除链表中重复的结点，以保障每个结点只出现一次。

## 解题思路

按照题意做即可。

**示例 1：**

![](https://assets.leetcode.com/uploads/2021/01/04/list1.jpg)

```
输入：head = [1,1,2]
输出：[1,2]
```

**示例 2：**

![](https://assets.leetcode.com/uploads/2021/01/04/list2.jpg)

```
输入：head = [1,1,2,3,3]
输出：[1,2,3]
```

**提示：**

- 链表中节点数目在范围 `[0, 300]` 内
- `-100 <= Node.val <= 100`
- 题目数据保证链表已经按升序 **排列**

**题解**

```go
// === 递归 ===
func deleteDuplicates(head *ListNode) *ListNode {
    if head == nil {
        return nil
    }
    for head.Next != nil && head.Next.Val == head.Val {
        head.Next = head.Next.Next
    }
    deleteDuplicates(head.Next)
    return head
}
// === 迭代 ===
func deleteDuplicates(head *ListNode) *ListNode {
    cur := head
    for cur != nil && cur.Next != nil {
        for cur.Next != nil && cur.Next.Val == cur.Val {
            cur.Next = cur.Next.Next
        }
        cur = cur.Next
    }
    return head
}
```
