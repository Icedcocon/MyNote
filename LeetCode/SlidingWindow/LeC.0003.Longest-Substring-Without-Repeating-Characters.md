# LeC.0003.Longest-Substring-Without-Repeating-Characters

## 题目

Given a string, find the length of the longest substring without repeating characters.

Example 1:

```c
Input: "abcabcbb"
Output: 3 
Explanation: The answer is "abc", with the length of 3. 
```

Example 2:

```c
Input: "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.
```

Example 3:

```c
Input: "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3. 
             Note that the answer must be a substring, "pwke" is a subsequence and not a substring.
```

## 题目大意

在一个字符串中寻找没有重复字母的最长子串。

## 解题思路

这一题和第 438 题，第 3 题，第 76 题，第 567 题类似，用的思想都是"滑动窗口"。

滑动窗口的右边界不断的右移，只要没有重复的字符，就持续向右扩大窗口边界。一旦出现了重复字符，就需要缩小左边界，直到重复的字符移出了左边界，然后继续移动滑动窗口的右边界。以此类推，每次移动需要计算当前长度，并判断是否需要更新最大长度，最终最大的值就是题目中的所求。

**示例 1:**

```
输入: s = "abcabcbb"
输出: 3 
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
```

**示例 2:**

```
输入: s = "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。
```

**示例 3:**

```
输入: s = "pwwkew"
输出: 3
解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
     请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。
```

**提示：**

- `0 <= s.length <= 5 * 104`
- `s` 由英文字母、数字、符号和空格组成

**题解**

```go
// === 滑动窗口+哈希表 ===
func lengthOfLongestSubstring(s string) int {
    var left, right, res int
    indexes := map[byte]int{}
    for left < len(s) {
        if idx, has := indexes[s[left]]; has && idx >= right {
            right = idx + 1
        }
        indexes[s[left]] = left
        left++
        res = max(res, left-right)
    }
    return res
}
// === 滑动窗口 ===
func lengthOfLongestSubstring(s string) int {
    var left, right, res int = 0, -1, 0
    freq := [127]int{}
    for left < len(s) {
        if right+1 < len(s) && freq[s[right+1]] == 0 {
            freq[s[right+1]]++
            right++
        } else {
            freq[s[left]]--
            left++
        }
        res = max(res, right-left+1)
    }
    return res
}
```
