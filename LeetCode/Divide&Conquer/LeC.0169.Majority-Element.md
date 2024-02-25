# LeC.0169.Majority-Element

## 题目

Given an array of size n, find the majority element. The majority element is the element that appears **more than** `⌊ n/2 ⌋` times.

You may assume that the array is non-empty and the majority element always exist in the array.

**Example 1:**

    Input: [3,2,3]
    Output: 3

**Example 2:**

    Input: [2,2,1,1,1,2,2]
    Output: 2

## 题目大意

给定一个大小为 n 的数组，找到其中的众数。众数是指在数组中出现次数大于 ⌊ n/2 ⌋ 的元素。你可以假设数组是非空的，并且给定的数组总是存在众数。

## 解题思路

- 题目要求找出数组中出现次数大于 `⌊ n/2 ⌋` 次的数。要求空间复杂度为 O(1)。简单题。
- 这一题利用的算法是 Boyer-Moore Majority Vote Algorithm。[https://www.zhihu.com/question/49973163/answer/235921864](https://www.zhihu.com/question/49973163/answer/235921864)

**示例 1：**

```
输入：nums = [3,2,3]
输出：3
```

**示例 2：**

```
输入：nums = [2,2,1,1,1,2,2]
输出：2
```

**提示：**

- `n == nums.length`
- `1 <= n <= 5 * 104`
- `-109 <= nums[i] <= 109`

**进阶：**尝试设计时间复杂度为 O(n)、空间复杂度为 O(1) 的算法解决此问题。

**题解**

```go
// === 投票法 ===
func majorityElement(nums []int) int {
    var count, candidate int
    for _, num := range nums {
        if count == 0 || candidate == num {
            candidate = num
            count++
        } else {
            count--
        }
    }
    return candidate
}
// === 分治法 ===
func majorityElement(nums []int) int {
    return divide(nums, 0, len(nums)-1)
}
func divide(nums []int, left, right int) int {
    if left == right {
        return nums[left]
    }
    mid := (left + right) / 2
    l := divide(nums, left, mid)
    r := divide(nums, mid+1, right)
    if l == r {
        return l
    } else {
        return conquer(nums, left, right, l, r)
    }
}
func conquer(nums []int, left, right, l, r int) int {
    var lc, rc int
    for left <= right {
        if nums[left] == l {
            lc++
        } else if nums[left] == r {
            rc++
        }
        left++
    }
    if lc > rc {
        return l
    } else {
        return r
    }
}
```
