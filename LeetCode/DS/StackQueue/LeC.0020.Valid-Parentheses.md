# LeC.0020.Valid-Parentheses

## 题目

Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:

Open brackets must be closed by the same type of brackets.
Open brackets must be closed in the correct order.
Note that an empty string is also considered valid.

Example 1:

```
Input: "()"
Output: true
```

Example 2:

```
Input: "()[]{}"
Output: true
```

Example 3:

```
Input: "(]"
Output: false
```

Example 4:

```
Input: "([)]"
Output: false
```

Example 5:

```
Input: "{[]}"
Output: true
```

## 题目大意

括号匹配问题。

## 解题思路

遇到左括号就进栈push，遇到右括号并且栈顶为与之对应的左括号，就把栈顶元素出栈。最后看栈里面还有没有其他元素，如果为空，即匹配。

需要注意，空字符串是满足括号匹配的，即输出 true。

**示例 1：**

```
输入：s = "()"
输出：true
```

**示例 2：**

```
输入：s = "()[]{}"
输出：true
```

**示例 3：**

```
输入：s = "(]"
输出：false
```

**提示：**

- `1 <= s.length <= 104`
- `s` 仅由括号 `'()[]{}'` 组成

**题解**

```go
// === 栈 ===
func isValid(s string) bool {
    stack := []byte{}
    bytes := []byte(s)
    for _, b := range bytes {
        if b == '(' || b == '{' || b == '[' {
            stack = append(stack, b)
        } else {
            if len(stack) == 0 || b-stack[len(stack)-1] > 2 || b-stack[len(stack)-1] < 1 {
                return false
            }
            stack = stack[:len(stack)-1]
        }
    }
    return len(stack) == 0
}
```
