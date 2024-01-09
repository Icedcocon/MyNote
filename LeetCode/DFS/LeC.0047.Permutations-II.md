# LeC.0047.Permutations-II

## 题目

Given a collection of numbers that might contain duplicates, return all possible unique permutations.

**Example:**

    Input: [1,1,2]
    Output:
    [
      [1,1,2],
      [1,2,1],
      [2,1,1]
    ]

## 题目大意

给定一个可包含重复数字的序列，返回所有不重复的全排列。

## 解题思路

- 这一题是第 46 题的加强版，第 46 题中求数组的排列，数组中元素不重复，但是这一题中，数组元素会重复，所以需要最终排列出来的结果需要去重。
- 去重的方法是经典逻辑，将数组排序以后，判断重复元素再做逻辑判断。
- 其他思路和第 46 题完全一致，DFS 深搜即可。

**示例 1：**

```
输入：nums = [1,1,2]
输出：
[[1,1,2],
 [1,2,1],
 [2,1,1]]
```

**示例 2：**

```
输入：nums = [1,2,3]
输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

**提示：**

- `1 <= nums.length <= 8`
- `-10 <= nums[i] <= 10`

**题解**

```go
func permuteUnique(nums []int) (ans [][]int) {
    sort.Ints(nums)
    n := len(nums)
    perm := []int{}
    vis := make([]bool, n)
    var backtrack func(int)
    backtrack = func(idx int) {
        if idx == n {
            ans = append(ans, append([]int(nil), perm...))
            return
        }
        for i, v := range nums {
            if vis[i] || i > 0 && !vis[i-1] && v == nums[i-1] {
                continue
            }
            perm = append(perm, v)
            vis[i] = true
            backtrack(idx + 1)
            vis[i] = false
            perm = perm[:len(perm)-1]
        }
    }
    backtrack(0)
    return
}
```
