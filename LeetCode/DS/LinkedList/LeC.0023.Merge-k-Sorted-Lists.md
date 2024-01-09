# LeC.0023.Merge-k-Sorted-Lists

## 题目

Merge k sorted linked lists and return it as one sorted list. Analyze and describe its complexity.

Example :

```
Input:
[
  1->4->5,
  1->3->4,
  2->6
]
Output: 1->1->2->3->4->4->5->6
```

## 题目大意

合并 K 个有序链表

## 解题思路

借助分治的思想，把 K 个有序链表两两合并即可。相当于是第 21 题的加强版。

**题解**

```go
// === 小根堆/优先队列 ===
func mergeKLists(lists []*ListNode) *ListNode {
    nh := NodeHeap{}
    for _, head := range lists {
        if head != nil {
            nh = append(nh, head)
        }
    }
    dummy := &ListNode{}
    cur := dummy
    heap.Init(&nh)
    for nh.Len() > 0 {
        cur.Next = heap.Pop(&nh).(*ListNode)
        cur = cur.Next
        if cur.Next != nil {
            heap.Push(&nh, cur.Next)
        }
    }
    return dummy.Next
}

type NodeHeap []*ListNode

func (nh NodeHeap) Len() int            { return len(nh) }
func (nh NodeHeap) Less(i, j int) bool  { return nh[i].Val < nh[j].Val }
func (nh NodeHeap) Swap(i, j int)       { nh[i], nh[j] = nh[j], nh[i] }
func (nh *NodeHeap) Push(n interface{}) { *nh = append(*nh, n.(*ListNode)) }
func (nh *NodeHeap) Pop() interface{} {
    node := (*nh)[len(*nh)-1]
    *nh = (*nh)[:len(*nh)-1]
    return node
}
// === 分治法 ===
func mergeKLists(lists []*ListNode) *ListNode {
    n := len(lists)
    if n < 1 {
        return nil
    }
    if n == 1 {
        return lists[0]
    }
    left := mergeKLists(lists[:n/2])
    right := mergeKLists(lists[n/2:])
    return merge2Lists(left, right)
}

func merge2Lists(list1, list2 *ListNode) *ListNode {
    if list1 == nil {
        return list2
    }
    if list2 == nil {
        return list1
    }
    if list1.Val < list2.Val {
        list1.Next = merge2Lists(list1.Next, list2)
        return list1
    } else {
        list2.Next = merge2Lists(list1, list2.Next)
        return list2
    }
}
```
