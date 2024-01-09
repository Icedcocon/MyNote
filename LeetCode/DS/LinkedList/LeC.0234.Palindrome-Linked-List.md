# LeC.0234.Palindrome-Linked-List

## 题目

Given a singly linked list, determine if it is a palindrome.

Example 1:

```c
Input: 1->2
Output: false
```

Example 2:

```c
Input: 1->2->2->1
Output: true
```

Follow up:  

Could you do it in O(n) time and O(1) space?

## 题目大意

判断一个链表是否是回文链表。要求时间复杂度 O(n)，空间复杂度 O(1)。

## 解题思路

这道题只需要在第 143 题上面改改就可以了。思路是完全一致的。先找到中间结点，然后反转中间结点后面到结尾的所有结点。最后一一判断头结点开始的结点和中间结点往后开始的结点是否相等。如果一直相等，就是回文链表，如果有不相等的，直接返回不是回文链表。

**示例 1：**

![](https://assets.leetcode.com/uploads/2021/03/03/pal1linked-list.jpg)

```
输入：head = [1,2,2,1]
输出：true
```

**示例 2：**

![](https://assets.leetcode.com/uploads/2021/03/03/pal2linked-list.jpg)

```
输入：head = [1,2]
输出：false
```

**提示：**

- 链表中节点数目在范围`[1, 105]` 内
- `0 <= Node.val <= 9`

**进阶：**你能否用 `O(n)` 时间复杂度和 `O(1)` 空间复杂度解决此题？

**题解**

```go
func isPalindrome(head *ListNode) bool {
    dummy := &ListNode{Next: head}
    slow, fast := dummy, dummy
    for fast != nil && fast.Next != nil {
        fast = fast.Next.Next
        slow = slow.Next
    }
    var pre *ListNode
    cur := slow.Next
    for cur != nil {
        next := cur.Next
        cur.Next = pre
        pre = cur
        cur = next
    }
    for head != nil && pre != nil {
        if head.Val != pre.Val {
            return false
        }
        head = head.Next
        pre = pre.Next
    }
    return true
}
```
