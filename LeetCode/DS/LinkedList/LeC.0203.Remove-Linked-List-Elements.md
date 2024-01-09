# LeC.0203.Remove-Linked-List-Elements

## 题目

Remove all elements from a linked list of integers that have value val.

Example :

```c
Input:  1->2->6->3->4->5->6, val = 6
Output: 1->2->3->4->5
```

## 题目大意

删除链表中所有指定值的结点。

## 解题思路

按照题意做即可。

**示例 1：**

![](https://assets.leetcode.com/uploads/2021/03/06/removelinked-list.jpg)

```
输入：head = [1,2,6,3,4,5,6], val = 6
输出：[1,2,3,4,5]
```

**示例 2：**

```
输入：head = [], val = 1
输出：[]
```

**示例 3：**

```
输入：head = [7,7,7,7], val = 7
输出：[]
```

**提示：**

- 列表中的节点数目在范围 `[0, 104]` 内
- `1 <= Node.val <= 50`
- `0 <= val <= 50`

**题解**

```go
// === 迭代 ===
func removeElements(head *ListNode, val int) *ListNode {
    dummy := &ListNode{Next: head}
    cur := dummy
    for cur != nil && cur.Next != nil {
        for cur.Next != nil && cur.Next.Val == val {
            cur.Next = cur.Next.Next
        }
        cur = cur.Next
    }
    return dummy.Next
}
// === 递归 ===
func removeElements(head *ListNode, val int) *ListNode {
    if head == nil {
        return nil
    }
    if head.Val == val {
        return removeElements(head.Next, val)
    } else {
        head.Next = removeElements(head.Next, val)
        return head
    }
}
```
