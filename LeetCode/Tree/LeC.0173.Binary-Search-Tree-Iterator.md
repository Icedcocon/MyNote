# LeC.0173.Binary-Search-Tree-Iterator

## 题目

Implement an iterator over a binary search tree (BST). Your iterator will be initialized with the root node of a BST.

Calling `next()` will return the next smallest number in the BST.

**Example:**

![](https://assets.leetcode.com/uploads/2018/12/25/bst-tree.png)

    BSTIterator iterator = new BSTIterator(root);
    iterator.next();    // return 3
    iterator.next();    // return 7
    iterator.hasNext(); // return true
    iterator.next();    // return 9
    iterator.hasNext(); // return true
    iterator.next();    // return 15
    iterator.hasNext(); // return true
    iterator.next();    // return 20
    iterator.hasNext(); // return false

**Note:**

- `next()` and `hasNext()` should run in average O(1) time and uses O(h) memory, where h is the height of the tree.
- You may assume that `next()` call will always be valid, that is, there will be at least a next smallest number in the BST when `next()` is called.

## 题目大意

实现一个二叉搜索树迭代器。你将使用二叉搜索树的根节点初始化迭代器。调用 next() 将返回二叉搜索树中的下一个最小的数。

## 解题思路

- 用优先队列解决即可

**示例：**

![](https://assets.leetcode.com/uploads/2018/12/25/bst-tree.png)

```
输入
["BSTIterator", "next", "next", "hasNext", "next", "hasNext", "next", "hasNext", "next", "hasNext"]
[[[7, 3, 15, null, null, 9, 20]], [], [], [], [], [], [], [], [], []]
输出
[null, 3, 7, true, 9, true, 15, true, 20, false]

解释
BSTIterator bSTIterator = new BSTIterator([7, 3, 15, null, null, 9, 20]);
bSTIterator.next();    // 返回 3
bSTIterator.next();    // 返回 7
bSTIterator.hasNext(); // 返回 True
bSTIterator.next();    // 返回 9
bSTIterator.hasNext(); // 返回 True
bSTIterator.next();    // 返回 15
bSTIterator.hasNext(); // 返回 True
bSTIterator.next();    // 返回 20
bSTIterator.hasNext(); // 返回 False
```

**提示：**

- 树中节点的数目在范围 `[1, 105]` 内
- `0 <= Node.val <= 106`
- 最多调用 `105` 次 `hasNext` 和 `next` 操作

**进阶：**

- 你可以设计一个满足下述条件的解决方案吗？`next()` 和 `hasNext()` 操作均摊时间复杂度为 `O(1)` ，并使用 `O(h)` 内存。其中 `h` 是树的高度。

**题解**

```go
type BSTIterator struct {
    stack []*TreeNode
    cur   *TreeNode
}

func Constructor(root *TreeNode) BSTIterator {
    return BSTIterator{cur: root}
}

func (this *BSTIterator) Next() int {
    for ; this.cur != nil; this.cur = this.cur.Left {
        this.stack = append(this.stack, this.cur)
    }
    this.cur, this.stack = this.stack[len(this.stack)-1], this.stack[:len(this.stack)-1]
    val := this.cur.Val
    this.cur = this.cur.Right
    return val
}

func (this *BSTIterator) HasNext() bool {
    return this.cur != nil || len(this.stack) > 0
}
```
