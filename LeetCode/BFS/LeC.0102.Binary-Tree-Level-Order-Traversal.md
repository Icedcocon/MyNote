# LeC.0102.binary-tree-level-order-traversal

**Medium**

## 题目

Given a binary tree, return the level order traversal of its nodes' values. (ie, from left to right, level by level).

For example:
Given binary tree [3,9,20,null,null,15,7],

```c
    3
   / \
  9  20
    /  \
   15   7
```

return its level order traversal as:

```c
[
  [3],
  [9,20],
  [15,7]
]
```

## 题目大意

按层序从上到下遍历一颗树。

## 解题思路

用一个队列或两个数组即可实现。

**示例 1：**

![](https://assets.leetcode.com/uploads/2021/02/19/tree1.jpg)

```
输入：root = [3,9,20,null,null,15,7]
输出：[[3],[9,20],[15,7]]
```

**示例 2：**

```
输入：root = [1]
输出：[[1]]
```

**示例 3：**

```
输入：root = []
输出：[]
```

**提示：**

- 树中节点数目在范围 `[0, 2000]` 内
- `-1000 <= Node.val <= 1000`

**题解：**

```go
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
 func levelOrder(root *TreeNode) (ans [][]int) {
    if root == nil {
        return
    }
    cur := []*TreeNode{root}
    for len(cur) > 0 {
        nxt := []*TreeNode{}
        vals := make([]int, len(cur)) // 大小已知
        for i, node := range cur {
            vals[i] = node.Val
            if node.Left != nil {
                nxt = append(nxt, node.Left)
            }
            if node.Right != nil {
                nxt = append(nxt, node.Right)
            }
        }
        cur = nxt
        ans = append(ans, vals)
    }
    return
}

func levelOrder(root *TreeNode) (ans [][]int) {
    if root == nil {
        return
    }
    q := []*TreeNode{root}
    for len(q) > 0 {
        n := len(q)
        vals := make([]int, n) // 大小已知
        for i := range vals {
            node := q[0]
            q = q[1:]
            vals[i] = node.Val
            if node.Left != nil {
                q = append(q, node.Left)
            }
            if node.Right != nil {
                q = append(q, node.Right)
            }
        }
        ans = append(ans, vals)
    }
    return
}
```
