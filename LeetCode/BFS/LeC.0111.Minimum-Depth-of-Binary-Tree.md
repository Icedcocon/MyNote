# LeC.0111.Minimum-Depth-of-Binary-Tree

**Easy**

## 题目

Given a binary tree, find its minimum depth.

The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.

**Note:** A leaf is a node with no children.

**Example:**

Given binary tree `[3,9,20,null,null,15,7]`,

        3
       / \
      9  20
        /  \
       15   7

return its minimum depth = 2.

## 题目大意

给定一个二叉树，找出其最小深度。最小深度是从根节点到最近叶子节点的最短路径上的节点数量。说明: 叶子节点是指没有子节点的节点。

## 解题思路

- 递归求出根节点到叶子节点的深度，输出最小值即可

**示例 1：**

![](https://assets.leetcode.com/uploads/2020/10/12/ex_depth.jpg)

```
输入：root = [3,9,20,null,null,15,7]
输出：2
```

**示例 2：**

```
输入：root = [2,null,3,null,4,null,5,null,6]
输出：5
```

**提示：**

- 树中节点数的范围在 `[0, 105]` 内
- `-1000 <= Node.val <= 1000`

**题解:**

```go
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
 func minDepth(root *TreeNode) int {
    if root == nil {
        return 0
    }
    queue := []*TreeNode{}
    count := []int{}
    queue = append(queue, root)
    count = append(count, 1)
    for i := 0; i < len(queue); i++ {
        node := queue[i]
        depth := count[i]
        if node.Left == nil && node.Right == nil {
            return depth
        }
        if node.Left != nil {
            queue = append(queue, node.Left)
            count = append(count, depth + 1)
        }
        if node.Right != nil {
            queue = append(queue, node.Right)
            count = append(count, depth + 1)
        }
    }
    return 0
}
```