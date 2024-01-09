# LeC.0257.Binary-Tree-Paths

## 题目

Given a binary tree, return all root-to-leaf paths.

**Note:** A leaf is a node with no children.

**Example:**

    Input:
    
       1
     /   \
    2     3
     \
      5
    
    Output: ["1->2->5", "1->3"]
    
    Explanation: All root-to-leaf paths are: 1->2->5, 1->3

## 题目大意

给定一个二叉树，返回所有从根节点到叶子节点的路径。说明: 叶子节点是指没有子节点的节点。

## 解题思路

- Google 的面试题，考察递归

**示例 1：**

![](https://assets.leetcode.com/uploads/2021/03/12/paths-tree.jpg)

```
输入：root = [1,2,3,null,5]
输出：["1->2->5","1->3"]
```

**示例 2：**

```
输入：root = [1]
输出：["1"]
```

**提示：**

- 树中节点的数目在范围 `[1, 100]` 内
- `-100 <= Node.val <= 100`

**题解**

```go
func binaryTreePaths(root *TreeNode) []string {
    ans := []string{}
    path := []string{}
    var dfs func(root *TreeNode)
    dfs = func(root *TreeNode) {
        if root != nil {
            path = append(path, strconv.Itoa(root.Val))
            if root.Left == nil && root.Right == nil {
                ans = append(ans, strings.Join(path, "->"))
            } else {
                dfs(root.Left)
                dfs(root.Right)
            }
            path = path[:len(path)-1]
        }
    }
    dfs(root)
    return ans
}
```
