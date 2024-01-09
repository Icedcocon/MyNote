# LeC.0077.Combinations

## 题目

Given two integers *n* and *k*, return all possible combinations of *k* numbers out of 1 ... *n*.

**Example:**

    Input: n = 4, k = 2
    Output:
    [
      [2,4],
      [3,4],
      [2,3],
      [1,2],
      [1,3],
      [1,4],
    ]

## 题目大意

给定两个整数 n 和 k，返回 1 ... n 中所有可能的 k 个数的组合。

## 解题思路

- 计算排列组合中的组合，用 DFS 深搜即可，注意剪枝

**示例 1：**

```
输入：n = 4, k = 2
输出：
[
  [2,4],
  [3,4],
  [2,3],
  [1,2],
  [1,3],
  [1,4],
]
```

**示例 2：**

```
输入：n = 1, k = 1
输出：[[1]]
```

**提示：**

- `1 <= n <= 20`
- `1 <= k <= n`

**题解**

```go
func combine(n int, k int) [][]int {
    nums := make([]int, n)
    for i := range nums {
        nums[i] = i
    }
    vis := make([]bool, n)
    set := []int{}
    ans := [][]int{}
    var dfs func(int)
    dfs = func(count int) {
        if count == k {
            ans = append(ans, append([]int(nil), set...))
        }
        l := len(set)
        for i, v := range nums {
            if l+(n-i) < k {
                return
            }
            if vis[i] || l > 0 && set[l-1] > v {
                continue
            }
            vis[i] = true
            set = append(set, v+1)
            dfs(count + 1)
            set = set[:l]
            vis[i] = false
        }
    }
    dfs(0)
    return ans
}
```
