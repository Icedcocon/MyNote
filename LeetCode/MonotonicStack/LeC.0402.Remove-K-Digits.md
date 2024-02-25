# LeC.0402.Remove-K-Digits

## 题目

Given a non-negative integer num represented as a string, remove k digits from the number so that the new number is the smallest possible.

Note:

- The length of num is less than 10002 and will be ≥ k.
- The given num does not contain any leading zero.

Example 1:

```c
Input: num = "1432219", k = 3
Output: "1219"
Explanation: Remove the three digits 4, 3, and 2 to form the new number 1219 which is the smallest.
```

Example 2:

```c
Input: num = "10200", k = 1
Output: "200"
Explanation: Remove the leading 1 and the number is 200. Note that the output must not contain leading zeroes.
```

Example 3:

```c
Input: num = "10", k = 2
Output: "0"
Explanation: Remove all the digits from the number and it is left with nothing which is 0.
```

## 题目大意

给定一个以字符串表示的非负整数 num，移除这个数中的 k 位数字，使得剩下的数字最小。

注意:

- num 的长度小于 10002 且 ≥ k。
- num 不会包含任何前导零。

## 解题思路

从开头扫 num 每一位，依次入栈，当新来的数字比栈顶元素小，就依次往前移除掉所有比这个新来数字大的数字。注意最后要求剩下的数字最小，如果最后剩下的数字超过了 K 位，取前 K 位必然是最小的(因为如果后 K 位有比前 K 位更小的值的话，会把前面大的数字踢除的)

注意，虽然 num 不会包含前导 0，但是最终删掉中间的数字以后，比如删掉 0 前面的所有数字以后，前导 0 就会出来，最终输出的时候要去掉前导 0 。

**示例 1 ：**

```
输入：num = "1432219", k = 3
输出："1219"
解释：移除掉三个数字 4, 3, 和 2 形成一个新的最小的数字 1219 。
```

**示例 2 ：**

```
输入：num = "10200", k = 1
输出："200"
解释：移掉首位的 1 剩下的数字为 200. 注意输出不能有任何前导零。
```

**示例 3 ：**

```
输入：num = "10", k = 2
输出："0"
解释：从原数字移除所有的数字，剩余为空就是 0 。
```

**提示：**

- `1 <= k <= num.length <= 105`
- `num` 仅由若干位数字（0 - 9）组成
- 除了 **0** 本身之外，`num` 不含任何前导零

**题解**

```go
func removeKdigits(num string, k int) string {
    stack := []byte{}
    for _, digit := range []byte(num) {
        for len(stack) > 0 && k > 0 && digit < stack[len(stack)-1] {
            stack = stack[:len(stack)-1]
            k--
        }
        stack = append(stack, digit)
    }
    stack = stack[:len(stack)-k]
    ans := strings.TrimLeft(string(stack), "0")
    if ans == "" {
        return "0"
    }
    return ans
}
```
