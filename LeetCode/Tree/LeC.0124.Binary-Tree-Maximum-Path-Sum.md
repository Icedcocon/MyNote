# LeC.0124.Binary-Tree-Maximum-Path-Sum

## 题目

Given a **non-empty** binary tree, find the maximum path sum.

For this problem, a path is defined as any sequence of nodes from some starting node to any node in the tree along the parent-child connections. The path must contain **at least one node** and does not need to go through the root.

**Example 1:**

    Input: [1,2,3]
    
           1
          / \
         2   3
    
    Output: 6

**Example 2:**

    Input: [-10,9,20,null,null,15,7]
    
       -10
       / \
      9  20
        /  \
       15   7
    
    Output: 42

## 题目大意

给定一个非空二叉树，返回其最大路径和。本题中，路径被定义为一条从树中任意节点出发，达到任意节点的序列。该路径至少包含一个节点，且不一定经过根节点。

## 解题思路

- 给出一个二叉树，要求找一条路径使得路径的和是最大的。
- 这一题思路比较简单，递归维护最大值即可。不过需要比较的对象比较多。`maxPathSum(root) = max(maxPathSum(root.Left), maxPathSum(root.Right), maxPathSumFrom(root.Left) (if>0) + maxPathSumFrom(root.Right) (if>0) + root.Val)` ，其中，`maxPathSumFrom(root) = max(maxPathSumFrom(root.Left), maxPathSumFrom(root.Right)) + root.Val`

**示例 1：**

![](https://assets.leetcode.com/uploads/2020/10/13/exx1.jpg)

```
输入：root = [1,2,3]
输出：6
解释：最优路径是 2 -> 1 -> 3 ，路径和为 2 + 1 + 3 = 6
```

**示例 2：**

![](https://assets.leetcode.com/uploads/2020/10/13/exx2.jpg)

```
输入：root = [-10,9,20,null,null,15,7]
输出：42
解释：最优路径是 15 -> 20 -> 7 ，路径和为 15 + 20 + 7 = 42
```

**提示：**

- 树中节点数目范围是 `[1, 3 * 104]`
- `-1000 <= Node.val <= 1000`

**题解**

```go
func maxPathSum(root *TreeNode) int {
    var maxnum int = math.MinInt64
    var dfs func(root *TreeNode) int
    dfs = func(root *TreeNode) int {
        if root == nil {
            return 0
        }
        left := max(dfs(root.Left), 0)
        right := max(dfs(root.Right), 0)

        maxnum = max(maxnum, root.Val+left+right)
        return root.Val + max(left, right)
    }
    dfs(root)
    return maxnum
}
```
