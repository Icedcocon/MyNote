# LeC.0445.Add-Two-Numbers-II

## 题目

You are given two non-empty linked lists representing two non-negative integers. The most significant digit comes first and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

Follow up:
What if you cannot modify the input lists? In other words, reversing the lists is not allowed.

Example:

```text
Input: (7 -> 2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 8 -> 0 -> 7
```

## 题目大意

这道题是第 2 题的变种题，第 2 题中的 2 个数是从个位逆序排到高位，这样相加只用从头交到尾，进位一直进位即可。这道题目中强制要求不能把链表逆序。2 个数字是从高位排到低位的，这样进位是倒着来的。

## 解题思路

思路也不难，加法只用把短的链表依次加到长的链表上面来就可以了，最终判断一下最高位有没有进位，有进位再往前进一位。加法的过程可以用到递归。

**题解**

```go
// === 栈 ===
func addTwoNumbers(l1 *ListNode, l2 *ListNode) *ListNode {
    s1, s2 := []int{}, []int{}
    for l1 != nil {
        s1 = append(s1, l1.Val)
        l1 = l1.Next
    }
    for l2 != nil {
        s2 = append(s2, l2.Val)
        l2 = l2.Next
    }
    var carry int
    var dummy = &ListNode{Val: -1}
    for len(s1) != 0 || len(s2) != 0 || carry != 0 {
        if len(s1) != 0 {
            carry += s1[len(s1)-1]
            s1 = s1[:len(s1)-1]
        }
        if len(s2) != 0 {
            carry += s2[len(s2)-1]
            s2 = s2[:len(s2)-1]
        }
        dummy.Next = &ListNode{Val: carry % 10, Next: dummy.Next}
        carry /= 10
    }
    return dummy.Next
}
// === 翻转链表 ===
```
