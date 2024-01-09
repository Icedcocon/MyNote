# LeC.0046.Permutations

## 题目

Given a collection of **distinct** integers, return all possible permutations.

**Example:**

    Input: [1,2,3]
    Output:
    [
      [1,2,3],
      [1,3,2],
      [2,1,3],
      [2,3,1],
      [3,1,2],
      [3,2,1]
    ]

## 题目大意

给定一个没有重复数字的序列，返回其所有可能的全排列。

## 解题思路

- 求出一个数组的排列组合中的所有排列，用 DFS 深搜即可。

**示例 1：**

```
输入：nums = [1,2,3]
输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

**示例 2：**

```
输入：nums = [0,1]
输出：[[0,1],[1,0]]
```

**示例 3：**

```
输入：nums = [1]
输出：[[1]]
```

**提示：**

- `1 <= nums.length <= 6`
- `-10 <= nums[i] <= 10`
- `nums` 中的所有整数 **互不相同**

**题解**

```go
func permute(nums []int) [][]int {
    res := [][]int{}
    visited := map[int]bool{}

    var dfs func(path []int)
    dfs = func(path []int) {
        if len(path) == len(nums) {
            temp := make([]int, len(path))
            copy(temp, path)
            res = append(res, temp)
            return
        }
        for _, n := range nums {
            if visited[n] {
                continue
            }
            path = append(path, n)
            visited[n] = true
            dfs(path)
            path = path[:len(path)-1]
            visited[n] = false
        }
    }

    dfs([]int{})
    return res
}
```
