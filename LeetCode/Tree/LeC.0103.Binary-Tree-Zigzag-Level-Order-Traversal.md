# LeC.0103.Binary-Tree-Zigzag-Level-Order-Traversal

## 题目

Given a binary tree, return the zigzag level order traversal of its nodes' values. (ie, from left to right, then right to left for the next level and alternate between).

For example:
Given binary tree [3,9,20,null,null,15,7],

```c
    3
   / \
  9  20
    /  \
   15   7
```

return its zigzag level order traversal as:

```c
[
  [3],
  [20,9],
  [15,7]
]
```

## 题目大意

按照 Z 字型层序遍历一棵树。

## 解题思路

- 按层序从上到下遍历一颗树，但是每一层的顺序是相互反转的，即上一层是从左往右，下一层就是从右往左，以此类推。用一个队列即可实现。
- 第 102 题和第 107 题都是按层序遍历的。

**示例 1：**

![](https://assets.leetcode.com/uploads/2021/02/19/tree1.jpg)

```
输入：root = [3,9,20,null,null,15,7]
输出：[[3],[20,9],[15,7]]
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
- `-100 <= Node.val <= 100`

**题解**

```go
func zigzagLevelOrder(root *TreeNode) (ans [][]int) {
    if root == nil {
        return
    }
    queue := []*TreeNode{root}
    for level := 0; len(queue) > 0; level++ {
        vals := []int{}
        q := queue
        queue = nil
        for _, node := range q {
            vals = append(vals, node.Val)
            if node.Left != nil {
                queue = append(queue, node.Left)
            }
            if node.Right != nil {
                queue = append(queue, node.Right)
            }
        }
        // 本质上和层序遍历一样，我们只需要把奇数层的元素翻转即可
        if level%2 == 1 {
            for i, n := 0, len(vals); i < n/2; i++ {
                vals[i], vals[n-1-i] = vals[n-1-i], vals[i]
            }
        }
        ans = append(ans, vals)
    }
    return
}
```
