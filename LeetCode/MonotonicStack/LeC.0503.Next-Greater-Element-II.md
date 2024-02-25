# LeC.0503.Next-Greater-Element-II

## 题目

Given a circular array (the next element of the last element is the first element of the array), print the Next Greater Number for every element. The Next Greater Number of a number x is the first greater number to its traversing-order next in the array, which means you could search circularly to find its next greater number. If it doesn't exist, output -1 for this number.

Example 1:

```c
Input: [1,2,1]
Output: [2,-1,2]
Explanation: The first 1's next greater number is 2; 
The number 2 can't find next greater number; 
The second 1's next greater number needs to search circularly, which is also 2.
```

Note: The length of given array won't exceed 10000.

## 题目大意

题目给出数组 A，针对 A 中的每个数组中的元素，要求在 A 数组中找出比该元素大的数，A 是一个循环数组。如果找到了就输出这个值，如果找不到就输出 -1。

## 解题思路

这题是第 496 题的加强版，在第 496 题的基础上增加了循环数组的条件。这一题可以依旧按照第 496 题的做法继续模拟。更好的做法是用单调栈，栈中记录单调递增的下标。

**示例 1:**

```
输入: nums = [1,2,1]
输出: [2,-1,2]
解释: 第一个 1 的下一个更大的数是 2；
数字 2 找不到下一个更大的数； 
第二个 1 的下一个最大的数需要循环搜索，结果也是 2。
```

**示例 2:**

```
输入: nums = [1,2,3,4,3]
输出: [2,3,4,-1,4]
```

**提示:**

- `1 <= nums.length <= 104`
- `-109 <= nums[i] <= 109`

**题解**

```go
// === 单调栈（逆序） ===
func nextGreaterElements(nums []int) []int {
    res, stack := make([]int, len(nums)), []int{}
    for i := 2*len(nums) - 1; i >= 0; i-- {
        num := nums[i%len(nums)]
        // fmt.Println()
        for len(stack) > 0 && nums[stack[len(stack)-1]] <= num {
            stack = stack[:len(stack)-1]
        }
        if len(stack) > 0 {
            res[i%len(nums)] = nums[stack[len(stack)-1]]
        } else {
            res[i%len(nums)] = -1
        }
        stack = append(stack, i%len(nums))
    }
    return res
}
// === 单调栈（顺序） ===
func nextGreaterElements(nums []int) []int {
    res, stack := make([]int, len(nums)), []int{}
    for i := range res {
        res[i] = -1
    }
    for i := 0; i < 2*len(nums); i++ {
        num := nums[i%len(nums)]
        for len(stack) > 0 && nums[stack[len(stack)-1]] < num {
            res[stack[len(stack)-1]] = num
            stack = stack[:len(stack)-1]
        }
        stack = append(stack, i%len(nums))
    }
    return res
}
```
