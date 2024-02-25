# LeC.0215.Kth-Largest-Element-in-an-Array

## 题目

Find the kth largest element in an unsorted array. Note that it is the kth largest element in the sorted order, not the kth distinct element.

Example 1:

```c
Input: [3,2,1,5,6,4] and k = 2
Output: 5
```

Example 2:

```c
Input: [3,2,3,1,2,4,5,5,6] and k = 4
Output: 4
```

Note:     

You may assume k is always valid, 1 ≤ k ≤ array's length.

## 题目大意

找出数组中第 K 大的元素。这一题非常经典。可以用 O(n) 的时间复杂度实现。

## 解题思路

在快速选择 quickselect 的 partition 操作中，每次 partition 操作结束都会返回一个点，这个标定点的下标和最终排序之后有序数组中这个元素所在的下标是一致的。利用这个特性，我们可以不断的划分数组区间，最终找到第 K 大的元素。执行一次 partition 操作以后，如果这个元素的下标比 K 小，那么接着就在后边的区间继续执行 partition 操作；如果这个元素的下标比 K 大，那么就在左边的区间继续执行 partition 操作；如果相等就直接输出这个下标对应的数组元素即可。

**示例 1:**

```
输入: [3,2,1,5,6,4], k = 2
输出: 5
```

**示例 2:**

```
输入: [3,2,3,1,2,4,5,5,6], k = 4
输出: 4
```

**提示：**

- `1 <= k <= nums.length <= 105`
- `-104 <= nums[i] <= 104`

**题解**

```go
// === 快速排序(超时) ===
func findKthLargest(nums []int, k int) int {
    divide(nums, 0, len(nums)-1, k)
    return nums[len(nums)-k]
}

func divide(nums []int, l, r, k int) {
    if l >= r {
        return
    }
    pos := conquer(nums, l, r)
    if pos == len(nums)-k {
        return
    } else if pos < len(nums)-k {
        divide(nums, pos+1, r, k)
    } else {
        divide(nums, l, pos-1, k)
    }
}

func conquer(nums []int, l, r int) int {
    pivot, wall := nums[r], l
    for i := l; i < r; i++ {
        if nums[i] < pivot {
            nums[wall], nums[i] = nums[i], nums[wall]
            wall++
        }
    }
    nums[r], nums[wall] = nums[wall], nums[r]
    return wall
}
// === 堆排序 ===
func findKthLargest(nums []int, k int) int {
    heapSize := len(nums)
    buildMaxHeap(nums, heapSize)
    for i := len(nums) - 1; i > len(nums)-k; i-- {
        nums[i], nums[0] = nums[0], nums[i]
        heapSize--
        maxHeapify(nums, 0, heapSize)
    }
    return nums[0]
}

func buildMaxHeap(nums []int, heapSize int) {
    for i := heapSize / 2; i >= 0; i-- {
        maxHeapify(nums, i, heapSize)
    }
}

func maxHeapify(nums []int, i, heapSize int) {
    l, r, largest := i*2+1, i*2+2, i
    if l < heapSize && nums[l] > nums[largest] {
        largest = l
    }
    if r < heapSize && nums[r] > nums[largest] {
        largest = r
    }
    if largest != i {
        nums[i], nums[largest] = nums[largest], nums[i]
        maxHeapify(nums, largest, heapSize)
    }
}
```
