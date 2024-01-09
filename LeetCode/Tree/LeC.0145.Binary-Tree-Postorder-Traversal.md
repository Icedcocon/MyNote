# LeC.0145.Binary-Tree-Postorder-Traversal

## 题目

Given a binary tree, return the postorder traversal of its nodes' values.

Example :

```c
Input: [1,null,2,3]
   1
    \
     2
    /
   3

Output: [3,2,1]
```

Follow up: Recursive solution is trivial, could you do it iteratively?

## 题目大意

后根遍历一颗树。

## 解题思路

递归的实现方法，见代码。

**示例 1：**

![](https://assets.leetcode.com/uploads/2020/08/28/pre1.jpg)

```
输入：root = [1,null,2,3]
输出：[3,2,1]
```

**示例 2：**

```
输入：root = []
输出：[]
```

**示例 3：**

```
输入：root = [1]
输出：[1]
```

**提示：**

- 树中节点的数目在范围 `[0, 100]` 内
- `-100 <= Node.val <= 100`

**进阶：**递归算法很简单，你可以通过迭代算法完成吗？

**题解**

```go
func postorderTraversal(root *TreeNode) (res []int) {
    var postorder func(*TreeNode)
    postorder = func(node *TreeNode) {
        if node == nil {
            return
        }
        postorder(node.Left)
        postorder(node.Right)
        res = append(res, node.Val)
    }
    postorder(root)
    return
}

func postorderTraversal(root *TreeNode) (res []int) {
    stk := []*TreeNode{}
    var prev *TreeNode
    for root != nil || len(stk) > 0 {
        for root != nil {
            stk = append(stk, root)
            root = root.Left
        }
        root = stk[len(stk)-1]
        stk = stk[:len(stk)-1]
        if root.Right == nil || root.Right == prev {
            res = append(res, root.Val)
            prev = root
            root = nil
        } else {
            stk = append(stk, root)
            root = root.Right
        }
    }
    return
}

func reverse(a []int) {
    for i, n := 0, len(a); i < n/2; i++ {
        a[i], a[n-1-i] = a[n-1-i], a[i]
    }
}

func postorderTraversal(root *TreeNode) (res []int) {
    addPath := func(node *TreeNode) {
        resSize := len(res)
        for ; node != nil; node = node.Right {
            res = append(res, node.Val)
        }
        reverse(res[resSize:])
    }

    p1 := root
    for p1 != nil {
        if p2 := p1.Left; p2 != nil {
            for p2.Right != nil && p2.Right != p1 {
                p2 = p2.Right
            }
            if p2.Right == nil {
                p2.Right = p1
                p1 = p1.Left
                continue
            }
            p2.Right = nil
            addPath(p1.Left)
        }
        p1 = p1.Right
    }
    addPath(root)
    return
}
```
