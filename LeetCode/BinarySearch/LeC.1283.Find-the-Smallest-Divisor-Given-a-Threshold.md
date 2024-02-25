# LeC.1283.Find-the-Smallest-Divisor-Given-a-Threshold

## 题目

Given an array of integers `nums` and an integer `threshold`, we will choose a positive integer divisor and divide all the array by it and sum the result of the division. Find the **smallest** divisor such that the result mentioned above is less than or equal to `threshold`.

Each result of division is rounded to the nearest integer greater than or equal to that element. (For example: 7/3 = 3 and 10/2 = 5).

It is guaranteed that there will be an answer.

**Example 1**:

```
Input: nums = [1,2,5,9], threshold = 6
Output: 5
Explanation: We can get a sum to 17 (1+2+5+9) if the divisor is 1. 
If the divisor is 4 we can get a sum to 7 (1+1+2+3) and if the divisor is 5 the sum will be 5 (1+1+1+2).
```

**Example 2**:

```
Input: nums = [2,3,5,7,11], threshold = 11
Output: 3
```

**Example 3**:

```
Input: nums = [19], threshold = 5
Output: 4
```

**Constraints**:

- `1 <= nums.length <= 5 * 10^4`
- `1 <= nums[i] <= 10^6`
- `nums.length <= threshold <= 10^6`

## 题目大意

给你一个整数数组 nums 和一个正整数 threshold  ，你需要选择一个正整数作为除数，然后将数组里每个数都除以它，并对除法结果求和。请你找出能够使上述结果小于等于阈值 threshold 的除数中 最小 的那个。每个数除以除数后都向上取整，比方说 7/3 = 3 ， 10/2 = 5 。题目保证一定有解。

提示：

- 1 <= nums.length <= 5 * 10^4
- 1 <= nums[i] <= 10^6
- nums.length <= threshold <= 10^6

## 解题思路

- 给出一个数组和一个阈值，要求找到一个除数，使得数组里面每个数和这个除数的商之和不超过这个阈值。求除数的最小值。
- 这一题是典型的二分搜索的题目。根据题意，在 [1, 1000000] 区间内搜索除数，针对每次 `mid`，计算一次商的累加和。如果和比 `threshold` 小，说明除数太大，所以缩小右区间；如果和比 `threshold` 大，说明除数太小，所以缩小左区间。最终找到的 `low` 值就是最求的最小除数。

**示例 1：**

```
输入：nums = [1,2,5,9], threshold = 6
输出：5
解释：如果除数为 1 ，我们可以得到和为 17 （1+2+5+9）。
如果除数为 4 ，我们可以得到和为 7 (1+1+2+3) 。如果除数为 5 ，和为 5 (1+1+1+2)。
```

**示例 2：**

```
输入：nums = [2,3,5,7,11], threshold = 11
输出：3
```

**示例 3：**

```
输入：nums = [19], threshold = 5
输出：4
```

**提示：**

- `1 <= nums.length <= 5 * 10^4`
- `1 <= nums[i] <= 10^6`
- `nums.length <= threshold <= 10^6`

**题解**

```go
func smallestDivisor(nums []int, threshold int) int {
    var bound int = threshold
    for _, num := range nums {
        bound = max(bound, num)
    }
    return 1 + sort.Search(bound-1, func(divisor int) bool {
        divisor += 1
        var sum int
        for _, num := range nums {
            if num%divisor > 0 {
                sum += num/divisor + 1
            } else {
                sum += num / divisor
            }
        }
        return sum <= threshold
    })
}
```
