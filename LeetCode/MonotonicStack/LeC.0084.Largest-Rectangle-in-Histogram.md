# LeC.0084.Largest-Rectangle-in-Histogram

## 题目

Given n non-negative integers representing the histogram's bar height where the width of each bar is 1, find the area of largest rectangle in the histogram.

 ![](https://assets.leetcode.com/uploads/2018/10/12/histogram.png)

Above is a histogram where width of each bar is 1, given height = [2,1,5,6,2,3].

![](https://assets.leetcode.com/uploads/2018/10/12/histogram_area.png)

The largest rectangle is shown in the shaded area, which has area = 10 unit.

Example:

```c
Input: [2,1,5,6,2,3]
Output: 10
```

## 题目大意

给出每个直方图的高度，要求在这些直方图之中找到面积最大的矩形，输出矩形的面积。

## 解题思路

用单调栈依次保存直方图的高度下标，一旦出现高度比栈顶元素小的情况就取出栈顶元素，单独计算一下这个栈顶元素的矩形的高度。然后停在这里(外层循环中的 i--，再 ++，就相当于停在这里了)，继续取出当前最大栈顶的前一个元素，即连续弹出 2 个最大的，以稍小的一个作为矩形的边，宽就是 2 计算面积…………如果停在这里的下标代表的高度一直比栈里面的元素小，就一直弹出，取出最后一个比当前下标大的高度作为矩形的边。宽就是最后一个比当前下标大的高度和当前下标 i 的差值。计算出面积以后不断的更新 maxArea 即可。

**示例 1:**

![](https://assets.leetcode.com/uploads/2021/01/04/histogram.jpg)

```
输入：heights = [2,1,5,6,2,3]
输出：10
解释：最大的矩形为图中红色区域，面积为 10
```

**示例 2：**

![](https://assets.leetcode.com/uploads/2021/01/04/histogram-1.jpg)

```
输入： heights = [2,4]
输出： 4
```

**提示：**

- `1 <= heights.length <=105`
- `0 <= heights[i] <= 104`

**题解**

```go
// === 单调栈 ===
func largestRectangleArea(heights []int) int {
    heights = append(heights, 0)
    stack := []int{}
    var res int
    for i, h := range heights {
        for len(stack) > 0 && h < heights[stack[len(stack)-1]] {
            prePos := stack[len(stack)-1]
            stack = stack[:len(stack)-1]
            if len(stack) == 0 {
                res = max(res, heights[prePos]*(i))
            } else {
                res = max(res, heights[prePos]*(i-(stack[len(stack)-1]+1)))
            }
        }
        stack = append(stack, i)
    }
    return res
}
// === 分治法 ===
func largestRectangleArea(heights []int) int {
    return divide(heights, 0, len(heights)-1)
}

func divide(heights []int, left, right int) int {
    if left > right {
        return 0
    }
    if left == right {
        return heights[left]
    }
    var minHeightPos int = left
    for cur := left + 1; cur <= right; cur++ {
        if heights[cur] < heights[minHeightPos] {
            minHeightPos = cur
        }
    }
    l := divide(heights, left, minHeightPos-1)
    r := divide(heights, minHeightPos+1, right)
    return max((right-left+1)*heights[minHeightPos], max(l, r))
}
```
