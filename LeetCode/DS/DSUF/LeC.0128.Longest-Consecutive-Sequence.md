# LeC.0128.Longest-Consecutive-Sequence

## 题目

Given an unsorted array of integers, find the length of the longest consecutive elements sequence.

Your algorithm should run in O(*n*) complexity.

**Example:**

    Input: [100, 4, 200, 1, 3, 2]
    Output: 4
    Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.

## 题目大意

给定一个未排序的整数数组，找出最长连续序列的长度。要求算法的时间复杂度为 O(n)。

## 解题思路

- 给出一个数组，要求找出最长连续序列，输出这个最长的长度。要求时间复杂度为 `O(n)`。
- 这一题可以先用暴力解决解决，代码见解法三。思路是把每个数都存在 `map` 中，先删去 `map` 中没有前一个数 `nums[i]-1` 也没有后一个数 `nums[i]+1` 的数 `nums[i]`，这种数前后都不连续。然后在 `map` 中找到前一个数 `nums[i]-1` 不存在，但是后一个数 `nums[i]+1` 存在的数，这种数是连续序列的起点，那么不断的往后搜，直到序列“断”了。最后输出最长序列的长度。
- 这一题最优的解法是解法一，针对每一个 `map` 中不存在的数 `n`，插入进去都做 2 件事情。第一件事，先查看 `n - 1` 和 `n + 1` 是否都存在于 `map` 中，如果都存在，代表存在连续的序列，那么就更新 `left`，`right` 边界。那么 `n` 对应的这个小的子连续序列长度为 `sum = left + right + 1`。第二件事就是更新 `left` 和 `right` 左右边界对应的 `length = sum`。
- 这一题还可以用并查集解决，见解法二。利用每个数在 `nums` 中的下标，把下标和下标进行 `union()`，具体做法是看前一个数 `nums[i]-1` 和后一个数 `nums[i]+1` 在 `map` 中是否存在，如果存在就 `union()`，最终输出整个并查集中包含最多元素的那个集合的元素总数。

**示例 1：**

```
输入：nums = [100,4,200,1,3,2]
输出：4
解释：最长数字连续序列是 [1, 2, 3, 4]。它的长度为 4。
```

**示例 2：**

```
输入：nums = [0,3,7,2,5,8,4,6,0,1]
输出：9
```

**提示：**

- `0 <= nums.length <= 105`
- `-109 <= nums[i] <= 109`

**题解**

```go
type UnionFind struct {
    parents []int
    size    []int
}

func NewUnionFind(num int) *UnionFind {
    parents := make([]int, num)
    size := make([]int, num)
    for i := range parents {
        parents[i] = i
        size[i] = 1
    }
    return &UnionFind{parents, size}
}

func (uf *UnionFind) Find(num int) int {
    if uf.parents[num] != num {
        uf.parents[num] = uf.Find(uf.parents[num])
    }
    return uf.parents[num]
}

func (uf *UnionFind) Union(p, q int) {
    rootP, rootQ := uf.Find(p), uf.Find(q)
    if rootP == rootQ {
        return
    }
    if uf.size[p] <= uf.size[q] {
        uf.parents[rootP] = rootQ
        uf.size[rootQ] += uf.size[rootP]
    } else {
        uf.parents[rootQ] = rootP
        uf.size[rootP] += uf.size[rootQ]
    }
}

func (uf *UnionFind) FindMax() int {
    var maxNum int
    for _, s := range uf.size {
        maxNum = max(s, maxNum)
    }
    return maxNum
}

func longestConsecutive(nums []int) int {
    n := len(nums)
    uf := NewUnionFind(n)
    vis := map[int]int{}
    for i, num := range nums {
        if _, has := vis[num]; has {
            continue
        }
        vis[num] = i
        if _, has := vis[num+1]; has {
            uf.Union(i, vis[num+1])
        }
        if _, has := vis[num-1]; has {
            uf.Union(i, vis[num-1])
        }
    }
    return uf.FindMax()
}
```
