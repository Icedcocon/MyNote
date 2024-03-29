# LeC.0095.Unique-Binary-Search-Trees-II

## 题目

Given an integer *n*, generate all structurally unique **BST's** (binary search trees) that store values 1 ... *n*.

**Example:**

    Input: 3
    Output:
    [
      [1,null,3,2],
      [3,2,null,1],
      [3,1,null,null,2],
      [2,1,3],
      [1,null,2,null,3]
    ]
    Explanation:
    The above output corresponds to the 5 unique BST's shown below:
    
       1         3     3      2      1
        \       /     /      / \      \
         3     2     1      1   3      2
        /     /       \                 \
       2     1         2                 3

## 题目大意

给定一个整数 n，生成所有由 1 ... n 为节点所组成的二叉搜索树。

## 解题思路

- 输出 1~n 元素组成的 BST 所有解。这一题递归求解即可。外层循环遍历 1~n 所有结点，作为根结点，内层双层递归分别求出左子树和右子树。

**示例 1：**

![](https://assets.leetcode.com/uploads/2021/01/18/uniquebstn3.jpg)

```
输入：n = 3
输出：[[1,null,2,null,3],[1,null,3,2],[2,1,3],[3,1,null,null,2],[3,2,null,1]]
```

**示例 2：**

```
输入：n = 1
输出：[[1]]
```

**提示：**

- `1 <= n <= 8`

**题解**

```go
func generateTrees(n int) []*TreeNode {
    if n == 0 {
        return []*TreeNode{}
    }
    return generateBSTree(1, n)
}

func generateBSTree(start, end int) []*TreeNode {
    tree := []*TreeNode{}
    if start > end {
        tree = append(tree, nil)
        return tree
    }
    for i := start; i <= end; i++ {
        left := generateBSTree(start, i-1)
        right := generateBSTree(i+1, end)
        for _, l := range left {
            for _, r := range right {
                root := &TreeNode{Val: i, Left: l, Right: r}
                tree = append(tree, root)
            }
        }
    }
    return tree
}
```
