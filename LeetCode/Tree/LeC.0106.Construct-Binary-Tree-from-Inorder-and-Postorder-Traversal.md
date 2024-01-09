# LeC.0106.Construct-Binary-Tree-from-Inorder-and-Postorder-Traversal

## 题目

Given inorder and postorder traversal of a tree, construct the binary tree.

**Note:**You may assume that duplicates do not exist in the tree.

For example, given

    inorder = [9,3,15,20,7]
    postorder = [9,15,7,20,3]

Return the following binary tree:

        3
       / \
      9  20
        /  \
       15   7

## 题目大意

根据一棵树的中序遍历与后序遍历构造二叉树。

注意:
你可以假设树中没有重复的元素。

## 解题思路

- 给出 2 个数组，根据 inorder 和 postorder 数组构造一颗树。
- 利用递归思想，从 postorder 可以得到根节点，从 inorder 中得到左子树和右子树。只剩一个节点的时候即为根节点。不断的递归直到所有的树都生成完成。

**示例 1:**

![](https://assets.leetcode.com/uploads/2021/02/19/tree.jpg)

```
输入：inorder = [9,3,15,20,7], postorder = [9,15,7,20,3]
输出：[3,9,20,null,null,15,7]
```

**示例 2:**

```
输入：inorder = [-1], postorder = [-1]
输出：[-1]
```

**提示:**

- `1 <= inorder.length <= 3000`
- `postorder.length == inorder.length`
- `-3000 <= inorder[i], postorder[i] <= 3000`
- `inorder` 和 `postorder` 都由 **不同** 的值组成
- `postorder` 中每一个值都在 `inorder` 中
- `inorder` **保证**是树的中序遍历
- `postorder` **保证**是树的后序遍历

**题解**

```go
func buildTree(inorder []int, postorder []int) *TreeNode {
    postorderLen := len(postorder)
    if len(inorder) == 0 {
        return nil
    }
    root := &TreeNode{Val: postorder[postorderLen-1]}
    postorder = postorder[:postorderLen-1]
    for pos, node := range inorder {
        if node == root.Val {
            root.Left = buildTree(inorder[:pos], postorder[:pos])
            root.Right = buildTree(inorder[pos+1:], postorder[pos:])
        }
    }
    return root
}

func buildTree(inorder []int, postorder []int) *TreeNode {
    n := len(inorder)
    if n == 0 {
        return nil
    }
    root := &TreeNode{postorder[n-1], nil, nil}
    stack := []*TreeNode{root}
    var inorderIndex int = n - 1
    for i := n - 2; i >= 0; i-- {
        postorderVal := postorder[i]
        node := stack[len(stack)-1]
        if node.Val != inorder[inorderIndex] {
            node.Right = &TreeNode{Val: postorderVal}
            stack = append(stack, node.Right)
        } else {
            for len(stack) > 0 && stack[len(stack)-1].Val == inorder[inorderIndex] {
                node = stack[len(stack)-1]
                stack = stack[:len(stack)-1]
                inorderIndex--
            }
            node.Left = &TreeNode{Val: postorderVal}
            stack = append(stack, node.Left)
        }
    }
    return root
}
```
