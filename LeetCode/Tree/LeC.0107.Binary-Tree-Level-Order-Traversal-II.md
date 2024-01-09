# LeC.0107.Binary-Tree-Level-Order-Traversal-II

## 题目

Given a binary tree, return the bottom-up level order traversal of its nodes' values. (ie, from left to right, level by level from leaf to root).

For example:
Given binary tree [3,9,20,null,null,15,7],

```c
    3
   / \
  9  20
    /  \
   15   7
```

return its bottom-up level order traversal as:

```c
[
  [15,7],
  [9,20],
  [3]
]
```

## 题目大意

按层序从下到上遍历一颗树。

## 解题思路

用一个队列即可实现。

**示例 1：**

![](https://assets.leetcode.com/uploads/2021/02/19/tree1.jpg)

```
输入：root = [3,9,20,null,null,15,7]
输出：[[15,7],[9,20],[3]]
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

**题解**

```go
func levelOrderBottom(root *TreeNode) [][]int {
    levelOrder := [][]int{}
    if root == nil {
        return levelOrder
    }
    queue := []*TreeNode{}
    queue = append(queue, root)
    for len(queue) > 0 {
        level := []int{}
        size := len(queue)
        for i := 0; i < size; i++ {
            node := queue[0]
            queue = queue[1:]
            level = append(level, node.Val)
            if node.Left != nil {
                queue = append(queue, node.Left)
            }
            if node.Right != nil {
                queue = append(queue, node.Right)
            }
        }
        levelOrder = append(levelOrder, level)
    }
    for i := 0; i < len(levelOrder) / 2; i++ {
        levelOrder[i], levelOrder[len(levelOrder) - 1 - i] = levelOrder[len(levelOrder) - 1 - i], levelOrder[i]
    }
    return levelOrder
}

func levelOrderBottom(root *TreeNode) [][]int {
    ans := [][]int{}
    if root == nil {
        return ans
    }
    q := []*TreeNode{root}
    depths := []int{1}
    for i := 0; i < len(q); i++ {
        n := len(q)
        depth := depths[i]
        for ; i < n; i++ {
            if q[i].Right != nil {
                q = append(q, q[i].Right)
                depths = append(depths, depth+1)
            }
            if q[i].Left != nil {
                q = append(q, q[i].Left)
                depths = append(depths, depth+1)
            }
        }
        i--
    }
    for i := len(q) - 1; i >= 0; i-- {
        depth := depths[i]
        list := []int{}
        for ; i >= 0 && depths[i] == depth; i-- {
            list = append(list, q[i].Val)
        }
        i++
        ans = append(ans, append([]int(nil), list...))
    }
    return ans
}
```
