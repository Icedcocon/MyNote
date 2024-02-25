# LeC.0496.Next-Greater-Element-I

## 题目

You are given two arrays (without duplicates) nums1 and nums2 where nums1’s elements are subset of nums2. Find all the next greater numbers for nums1's elements in the corresponding places of nums2.

The Next Greater Number of a number x in nums1 is the first greater number to its right in nums2. If it does not exist, output -1 for this number.

Example 1:

```c
Input: nums1 = [4,1,2], nums2 = [1,3,4,2].
Output: [-1,3,-1]
Explanation:
    For number 4 in the first array, you cannot find the next greater number for it in the second array, so output -1.
    For number 1 in the first array, the next greater number for it in the second array is 3.
    For number 2 in the first array, there is no next greater number for it in the second array, so output -1.
```

Example 2:

```c
Input: nums1 = [2,4], nums2 = [1,2,3,4].
Output: [3,-1]
Explanation:
    For number 2 in the first array, the next greater number for it in the second array is 3.
    For number 4 in the first array, there is no next greater number for it in the second array, so output -1.
```

Note:  

- All elements in nums1 and nums2 are unique.  
- The length of both nums1 and nums2 would not exceed 1000.

## 题目大意

这道题也是简单题。题目给出 2 个数组 A 和 B，针对 A 中的每个数组中的元素，要求在 B 数组中找出比 A 数组中元素大的数，B 中元素之间的顺序保持不变。如果找到了就输出这个值，如果找不到就输出 -1。

## 解题思路

简单题，依题意做即可。

**提示：**

- `1 <= nums1.length <= nums2.length <= 1000`
- `0 <= nums1[i], nums2[i] <= 104`
- `nums1`和`nums2`中所有整数 **互不相同**
- `nums1` 中的所有整数同样出现在 `nums2` 中

**进阶**你可以设计一个时间复杂度为 `O(nums1.length + nums2.length)` 的解决方案吗？

**题解**

```go
func nextGreaterElement(nums1 []int, nums2 []int) []int {
    if len(nums1) == 0 {
        return []int{}
    }
    stack, reocrd := []int{}, map[int]int{}
    for i := len(nums2) - 1; i >= 0; i-- {
        for len(stack) > 0 && nums2[i] > stack[len(stack)-1] {
            stack = stack[:len(stack)-1]
        }
        if len(stack) > 0 {
            reocrd[nums2[i]] = stack[len(stack)-1]
        } else {
            reocrd[nums2[i]] = -1
        }
        stack = append(stack, nums2[i])
    }
    res := make([]int, len(nums1))
    for i := range nums1 {
        res[i] = reocrd[nums1[i]]
    }
    return res
}
```
