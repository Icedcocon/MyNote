# LeC.0076.Minimum-Window-Substring

## 题目

Given a string S and a string T, find the minimum window in S which will contain all the characters in T in complexity O(n).

Example:

```c
Input: S = "ADOBECODEBANC", T = "ABC"
Output: "BANC"
```

Note:    

- If there is no such window in S that covers all characters in T, return the empty string "".
- If there is such window, you are guaranteed that there will always be only one unique minimum window in S.

## 题目大意

给定一个源字符串 s，再给一个字符串 T，要求在源字符串中找到一个窗口，这个窗口包含由字符串各种排列组合组成的，窗口中可以包含 T 中没有的字符，如果存在多个，在结果中输出最小的窗口，如果找不到这样的窗口，输出空字符串。

## 解题思路

这一题是滑动窗口的题目，在窗口滑动的过程中不断的包含字符串 T，直到完全包含字符串 T 的字符以后，记下左右窗口的位置和窗口大小。每次都不断更新这个符合条件的窗口和窗口大小的最小值。最后输出结果即可。

**示例 1：**

```
输入：s = "ADOBECODEBANC", t = "ABC"
输出："BANC"
解释：最小覆盖子串 "BANC" 包含来自字符串 t 的 'A'、'B' 和 'C'。
```

**示例 2：**

```
输入：s = "a", t = "a"
输出："a"
解释：整个字符串 s 是最小覆盖子串。
```

**示例 3:**

```
输入: s = "a", t = "aa"
输出: ""
解释: t 中两个字符 'a' 均应包含在 s 的子串中，
因此没有符合条件的子字符串，返回空字符串。
```

**提示：**

- `m == s.length`
- `n == t.length`
- `1 <= m, n <= 105`
- `s` 和 `t` 由英文字母组成

**进阶：**你能设计一个在 `o(m+n)` 时间内解决此问题的算法吗？

**题解**

```go
func minWindow(s string, t string) string {
    freq := map[byte]int{}
    for i := 0; i < len(t); i++ {
        freq[t[i]]++
    }
    left, minW, minStart, count := 0, len(s)+1, 0, 0
    for i := 0; i < len(s); i++ {
        if _, has := freq[s[i]]; has {
            if freq[s[i]] > 0 {
                count++
            }
            freq[s[i]]--
        }
        for count == len(t) {
            if i-left+1 < minW {
                minW = i - left + 1
                minStart = left
            }
            if _, has := freq[s[left]]; has {
                freq[s[left]]++
                if freq[s[left]] > 0 {
                    count--
                }
            }
            left++
        }
    }
    if minW <= len(s) {
        return s[minStart : minStart+minW]
    } else {
        return ""
    }
}
```
