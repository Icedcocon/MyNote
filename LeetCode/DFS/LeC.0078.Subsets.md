# LeC.0078. Subsets

## 题目

Given a set of **distinct** integers, *nums*, return all possible subsets (the power set).

**Note:** The solution set must not contain duplicate subsets.

**Example:**

    Input: nums = [1,2,3]
    Output:
    [
      [3],
      [1],
      [2],
      [1,2,3],
      [1,3],
      [2,3],
      [1,2],
      []
    ]

## 题目大意

给定一组不含重复元素的整数数组 nums，返回该数组所有可能的子集（幂集）。说明：解集不能包含重复的子集。

## 解题思路

- 找出一个集合中的所有子集，空集也算是子集。且数组中的数字不会出现重复。用 DFS 暴力枚举即可。
- 这一题和第 90 题，第 491 题类似，可以一起解答和复习。

**示例 1：**

```
输入：nums = [1,2,3]
输出：[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
```

**示例 2：**

```
输入：nums = [0]
输出：[[],[0]]
```

**提示：**

- `1 <= nums.length <= 10`
- `-10 <= nums[i] <= 10`
- `nums` 中的所有元素 **互不相同**

**题解**

```go
func subsets(nums []int) (ans [][]int) {
    n := len(nums)
    for mask := 0; mask < 1<<n; mask++ {
        set := []int{}
        for i, v := range nums {
            if mask>>i&1 > 0 {
                set = append(set, v)
            }
        }
        ans = append(ans, append([]int(nil), set...))
    }
    return
}

func subsets(nums []int) [][]int {
    res := [][]int{}

    dfs := func(i int, list []int) {
        tmp := make([]int, len(list))
        copy(tmp, list)
        res = append(res, tmp)
        for j := i; j < len(nums); j++ {
            list = append(list, nums[j])
            dfs(j+1, list)
            list = list[:len(list)-1]
        }
    }

    dfs(0, []int{})
    return res
}
```
