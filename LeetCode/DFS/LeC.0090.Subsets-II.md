# LeC.0090.Subsets II

## 题目

Given a collection of integers that might contain duplicates, ***nums***, return all possible subsets (the power set).

**Note:** The solution set must not contain duplicate subsets.

**Example:**

    Input: [1,2,2]
    Output:
    [
      [2],
      [1],
      [1,2,2],
      [2,2],
      [1,2],
      []
    ]

## 题目大意

给定一个可能包含重复元素的整数数组 nums，返回该数组所有可能的子集（幂集）。说明：解集不能包含重复的子集。

## 解题思路

- 这一题是第 78 题的加强版，比第 78 题多了一个条件，数组中的数字会出现重复。
- 解题方法依旧是 DFS，需要在回溯的过程中加上一些判断。
- 这一题和第 78 题，第 491 题类似，可以一起解答和复习。

**示例 1：**

```
输入：nums = [1,2,2]
输出：[[],[1],[1,2],[1,2,2],[2],[2,2]]
```

**示例 2：**

```
输入：nums = [0]
输出：[[],[0]]
```

**提示：**

- `1 <= nums.length <= 10`
- `-10 <= nums[i] <= 10`

**题解**

```go
func subsetsWithDup(nums []int) (ans [][]int) {
    sort.Ints(nums)
    n := len(nums)
outer:
    for mask := 0; mask < 1<<n; mask++ {
        t := []int{}
        for i, v := range nums {
            if mask>>i&1 > 0 {
                if i > 0 && mask>>(i-1)&1 == 0 && v == nums[i-1] {
                    continue outer
                }
                t = append(t, v)
            }
        }
        ans = append(ans, append([]int(nil), t...))
    }
    return
}

func subsetsWithDup(nums []int) (ans [][]int) {
    sort.Ints(nums)
    t := []int{}
    var dfs func(bool, int)
    dfs = func(choosePre bool, cur int) {
        if cur == len(nums) {
            ans = append(ans, append([]int(nil), t...))
            return
        }
        dfs(false, cur+1)
        if !choosePre && cur > 0 && nums[cur-1] == nums[cur] {
            return
        }
        t = append(t, nums[cur])
        dfs(true, cur+1)
        t = t[:len(t)-1]
    }
    dfs(false, 0)
    return
}
```
