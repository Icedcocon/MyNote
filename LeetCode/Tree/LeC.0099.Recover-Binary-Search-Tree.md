# LeC.0099.Recover-Binary-Search-Tree

## 题目

Two elements of a binary search tree (BST) are swapped by mistake.

Recover the tree without changing its structure.

**Example 1:**

    Input: [1,3,null,null,2]
    
       1
      /
     3
      \
       2
    
    Output: [3,1,null,null,2]
    
       3
      /
     1
      \
       2

**Example 2:**

    Input: [3,1,4,null,null,2]
    
      3
     / \
    1   4
       /
      2
    
    Output: [2,1,4,null,null,3]
    
      2
     / \
    1   4
       /
      3

**Follow up:**

- A solution using O(*n*) space is pretty straight forward.
- Could you devise a constant space solution?

## 题目大意

二叉搜索树中的两个节点被错误地交换。请在不改变其结构的情况下，恢复这棵树。

## 解题思路

- 在二叉搜索树中，有 2 个结点的值出错了，要求修复这两个结点。
- 这一题按照先根遍历 1 次就可以找到这两个出问题的结点，因为先访问根节点，然后左孩子，右孩子。用先根遍历二叉搜索树的时候，根结点比左子树都要大，根结点比右子树都要小。所以`左子树比根结点大的话，就是出现了乱序`；`根节点比右子树大的话，就是出现了乱序`。遍历过程中在左子树中如果出现了前一次遍历的结点的值大于此次根节点的值，这就出现了出错结点了，记录下来。继续遍历直到找到第二个这样的结点。最后交换这两个结点的时候，只是交换他们的值就可以了，而不是交换这两个结点相应的指针指向。

**示例 1：**

![](https://assets.leetcode.com/uploads/2020/10/28/recover1.jpg)

```
输入：root = [1,3,null,null,2]
输出：[3,1,null,null,2]
解释：3 不能是 1 的左孩子，因为 3 > 1 。交换 1 和 3 使二叉搜索树有效。
```

**示例 2：**

![](https://assets.leetcode.com/uploads/2020/10/28/recover2.jpg)

```
输入：root = [3,1,4,null,null,2]
输出：[2,1,4,null,null,3]
解释：2 不能在 3 的右子树中，因为 2 < 3 。交换 2 和 3 使二叉搜索树有效。
```

**提示：**

- 树上节点的数目在范围 `[2, 1000]` 内
- `-231 <= Node.val <= 231 - 1`

**进阶**：使用 `O(n)` 空间复杂度的解法很容易实现。你能想出一个只使用 `O(1)` 空间的解决方案吗？

```go
func recoverTree(root *TreeNode) {
    var prev, target1, target2 *TreeNode
    _, target1, target2 = inOrderTraverse(root, prev, target1, target2)
    if target1 != nil && target2 != nil {
        target1.Val, target2.Val = target2.Val, target1.Val
    }

}

func inOrderTraverse(root, prev, target1, target2 *TreeNode) (*TreeNode, *TreeNode, *TreeNode) {
    if root == nil {
        return prev, target1, target2
    }
    prev, target1, target2 = inOrderTraverse(root.Left, prev, target1, target2)
    if prev != nil && prev.Val > root.Val {
        if target1 == nil {
            target1 = prev
        }
        target2 = root
    }
    prev = root
    prev, target1, target2 = inOrderTraverse(root.Right, prev, target1, target2)
    return prev, target1, target2
}

func recoverTree(root *TreeNode)  {
    stack := []*TreeNode{}
    var x, y, pred *TreeNode
    for len(stack) > 0 || root != nil {
        for root != nil {
            stack = append(stack, root)
            root = root.Left
        }
        root = stack[len(stack)-1]
        stack = stack[:len(stack)-1]
        if pred != nil && root.Val < pred.Val {
            y = root
            if x == nil {
                x = pred
            } else {
                break
            }
        }
        pred = root
        root = root.Right
    }
    x.Val, y.Val = y.Val, x.Val
}
```
