# LeC.0239.Sliding-Window-Maximum

## 题目

Given an array *nums*, there is a sliding window of size *k* which is moving from the very left of the array to the very right. You can only see the *k* numbers in the window. Each time the sliding window moves right by one position. Return the max sliding window.

**Example:**

    Input: nums = [1,3,-1,-3,5,3,6,7], and k = 3
    Output: [3,3,5,5,6,7] 
    Explanation: 
    
    Window position                Max
    ---------------               -----
    [1  3  -1] -3  5  3  6  7       3
     1 [3  -1  -3] 5  3  6  7       3
     1  3 [-1  -3  5] 3  6  7       5
     1  3  -1 [-3  5  3] 6  7       5
     1  3  -1  -3 [5  3  6] 7       6
     1  3  -1  -3  5 [3  6  7]      7

**Note:**

You may assume *k* is always valid, 1 ≤ k ≤ input array's size for non-empty array.

**Follow up:**

Could you solve it in linear time?

## 题目大意

给定一个数组 nums，有一个大小为 k 的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口 k 内的数字。滑动窗口每次只向右移动一位。返回滑动窗口最大值。

## 解题思路

- 给定一个数组和一个窗口为 K 的窗口，当窗口从数组的左边滑动到数组右边的时候，输出每次移动窗口以后，在窗口内的最大值。
- 这道题最暴力的方法就是 2 层循环，时间复杂度 O(n * K)。
- 另一种思路是用优先队列，每次窗口以后的时候都向优先队列里面新增一个节点，并删除一个节点。时间复杂度是 O(n * log n)
- 最优的解法是用双端队列，队列的一边永远都存的是窗口的最大值，队列的另外一个边存的是比最大值小的值。队列中最大值左边的所有值都出队。在保证了双端队列的一边即是最大值以后，时间复杂度是 O(n)，空间复杂度是 O(K)

**示例 1：**

```
输入：nums = [1,3,-1,-3,5,3,6,7], k = 3
输出：[3,3,5,5,6,7]
解释：
滑动窗口的位置                最大值
---------------               -----
[1  3  -1] -3  5  3  6  7       3
 1 [3  -1  -3] 5  3  6  7       3
 1  3 [-1  -3  5] 3  6  7       5
 1  3  -1 [-3  5  3] 6  7       5
 1  3  -1  -3 [5  3  6] 7       6
 1  3  -1  -3  5 [3  6  7]      7
```

**示例 2：**

```
输入：nums = [1], k = 1
输出：[1]
```

**提示：**

- `1 <= nums.length <= 105`
- `-104 <= nums[i] <= 104`
- `1 <= k <= nums.length`

**题解**

```go
func maxSlidingWindow(nums []int, k int) []int {
    if len(nums) == 0 || len(nums) < k {
        return make([]int, 0)
    }
    window := make([]int, 0, k) // store the index of nums
    result := make([]int, 0, len(nums)-k+1)
    for i, v := range nums { // if the left-most index is out of window, remove it
        if i >= k && window[0] <= i-k {
            window = window[1:]
        }
        for len(window) > 0 && nums[window[len(window)-1]] < v { // maintain window
            window = window[0 : len(window)-1]
        }
        window = append(window, i) // store the index of nums
        if i >= k-1 {
            result = append(result, nums[window[0]]) // the left-most is the index of max value in nums
        }
    }
    return result
}
```
