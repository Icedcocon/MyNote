# LeC.0547.Number-of-Provinces

## 题目

There are **N** students in a class. Some of them are friends, while some are not. Their friendship is transitive in nature. For example, if A is a **direct** friend of B, and B is a **direct**friend of C, then A is an **indirect** friend of C. And we defined a friend circle is a group of students who are direct or indirect friends.

Given a **N*N** matrix **M** representing the friend relationship between students in the class. If M[i][j] = 1, then the ith and jth students are **direct** friends with each other, otherwise not. And you have to output the total number of friend circles among all the students.

**Example 1:**

    Input: 
    [[1,1,0],
     [1,1,0],
     [0,0,1]]
    Output: 2
    Explanation:The 0th and 1st students are direct friends, so they are in a friend circle. 
    The 2nd student himself is in a friend circle. So return 2.

**Example 2:**

    Input: 
    [[1,1,0],
     [1,1,1],
     [0,1,1]]
    Output: 1
    Explanation:The 0th and 1st students are direct friends, the 1st and 2nd students are direct friends, 
    so the 0th and 2nd students are indirect friends. All of them are in the same friend circle, so return 1.

**Note:**

1. N is in range [1,200].
2. M[i][i] = 1 for all students.
3. If M[i][j] = 1, then M[j][i] = 1.

## 题目大意

班上有 N 名学生。其中有些人是朋友，有些则不是。他们的友谊具有是传递性。如果已知 A 是 B 的朋友，B 是 C 的朋友，那么我们可以认为 A 也是 C 的朋友。所谓的朋友圈，是指所有朋友的集合。

给定一个 N * N 的矩阵 M，表示班级中学生之间的朋友关系。如果 M[i][j] = 1，表示已知第 i 个和 j 个学生互为朋友关系，否则为不知道。你必须输出所有学生中的已知的朋友圈总数。

注意：

- N 在[1,200]的范围内。
- 对于所有学生，有M[i][i] = 1。
- 如果有 M[i][j] = 1，则有 M[j][i] = 1。

## 解题思路

- 给出一个二维矩阵，矩阵中的行列表示的是两个人之间是否是朋友关系，如果是 1，代表两个人是朋友关系。由于自己和自肯定朋友关系，所以对角线上都是 1，并且矩阵也是关于从左往右下的这条对角线对称。
- 这题有 2 种解法，第一种解法是并查集，依次扫描矩阵，如果两个人认识，并且 root 并不相等就执行 union 操作。扫完所有矩阵，最后数一下还有几个不同的 root 就是最终答案。第二种解法是 DFS 或者 BFS。利用 FloodFill 的想法去染色，每次染色一次，计数器加一。最终扫完整个矩阵，计数器的结果就是最终结果。

**示例 1：**

![](https://assets.leetcode.com/uploads/2020/12/24/graph1.jpg)

```
输入：isConnected = [[1,1,0],[1,1,0],[0,0,1]]
输出：2
```

**示例 2：**

![](https://assets.leetcode.com/uploads/2020/12/24/graph2.jpg)

```
输入：isConnected = [[1,0,0],[0,1,0],[0,0,1]]
输出：3
```

**提示：**

- `1 <= n <= 200`
- `n == isConnected.length`
- `n == isConnected[i].length`
- `isConnected[i][j]` 为 `1` 或 `0`
- `isConnected[i][i] == 1`
- `isConnected[i][j] == isConnected[j][i]`

```go
type UnionFund struct {
    parents []int
}

func NewUnionFund(num int) *UnionFund {
    parents := make([]int, num)
    for i := range parents {
        parents[i] = i
    }
    return &UnionFund{parents}
}

func (uf *UnionFund) Find(num int) int {
    if uf.parents[num] != num {
        uf.parents[num] = uf.Find(uf.parents[num])
    }
    return uf.parents[num]
}

func (uf *UnionFund) Union(p, q int) {
    rootP, rootQ := uf.Find(p), uf.Find(q)
    if rootP == rootQ {
        return
    }
    uf.parents[rootP] = rootQ
}

func findCircleNum(isConnected [][]int) int {
    n := len(isConnected)
    uf := NewUnionFund(n)
    for i, row := range isConnected {
        for j, connect := range row {
            if connect == 1 {
                uf.Union(i, j)
            }
        }
    }
    var res int
    for i := range isConnected {
        if uf.Find(i) == i {
            res++
        }
    }
    return res
}

func findCircleNum(isConnected [][]int) int {
    n := len(isConnected)
    vis := make([]bool, n)
    var count int
    var dfs func(from int)
    dfs = func(from int) {
        if vis[from] {
            return
        }
        vis[from] = true
        for to, conn := range isConnected[from] {
            if conn == 1 {
                dfs(to)
            }
        }
    }
    for i := range vis {
        if !vis[i] {
            dfs(i)
            count++
        }
    }
    return count
}
```
