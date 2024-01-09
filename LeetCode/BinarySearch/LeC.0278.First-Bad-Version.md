# LeC.0278.First-Bad-Version

## 题目

You are a product manager and currently leading a team to develop a new product. Unfortunately, the latest version of your product fails the quality check. Since each version is developed based on the previous version, all the versions after a bad version are also bad.

Suppose you have `n` versions `[1, 2, ..., n]` and you want to find out the first bad one, which causes all the following ones to be bad.

You are given an API `bool isBadVersion(version)` which returns whether `version` is bad. Implement a function to find the first bad version. You should minimize the number of calls to the API.

**Example 1:**

```
Input: n = 5, bad = 4
Output: 4
Explanation:
call isBadVersion(3) -> false
call isBadVersion(5) -> true
call isBadVersion(4) -> true
Then 4 is the first bad version.
```

**Example 2:**

```
Input: n = 1, bad = 1
Output: 1
```

**Constraints:**

- `1 <= bad <= n <= 231 - 1`

## 题目大意

你是产品经理，目前正在带领一个团队开发新的产品。不幸的是，你的产品的最新版本没有通过质量检测。由于每个版本都是基于之前的版本开发的，所以错误的版本之后的所有版本都是错的。假设你有 n 个版本 [1, 2, ..., n]，你想找出导致之后所有版本出错的第一个错误的版本。你可以通过调用 bool isBadVersion(version) 接口来判断版本号 version 是否在单元测试中出错。实现一个函数来查找第一个错误的版本。你应该尽量减少对调用 API 的次数。

## 解题思路

- 我们知道开发产品迭代的版本，如果当一个版本为正确版本，则该版本之前的所有版本均为正确版本；当一个版本为错误版本，则该版本之后的所有版本均为错误版本。利用这个性质就可以进行二分查找。利用二分搜索，也可以满足减少对调用 API 的次数的要求。时间复杂度：O(logn)，其中 n 是给定版本的数量。空间复杂度：O(1)。

**示例 1：**

```
输入：nums = [1,3,4,2,2]
输出：2
```

**示例 2：**

```
输入：nums = [3,1,3,4,2]
输出：3
```

**提示：**

- `1 <= n <= 105`
- `nums.length == n + 1`
- `1 <= nums[i] <= n`
- `nums` 中 **只有一个整数** 出现 **两次或多次** ，其余整数均只出现 **一次**

**进阶：**

- 如何证明 `nums` 中至少存在一个重复的数字?
- 你可以设计一个线性级时间复杂度 `O(n)` 的解决方案吗？

**题解**

```go
// === 模板 ===
func firstBadVersion(n int) int {
    return sort.Search(n, func(version int) bool { return isBadVersion(version) })
}
// === 模板1 ===
func firstBadVersion(n int) int {
    left, right := 1, n
    ans := 0
    for left <= right {
        mid := left + (right-left)/2
        if isBadVersion(mid) {
            ans = mid
            right = mid - 1
        } else {
            left = mid + 1
        }
    }
    // (right,left)
    return ans
}
// === 模板2 ===
func firstBadVersion(n int) int {
    left, right := 1, n+1
    // ans := 0
    for left < right {
        mid := left + (right-left)/2
        if isBadVersion(mid) {
            // ans = mid
            right = mid
        } else {
            left = mid + 1
        }
    }
    // right==left
    return left
}
```
