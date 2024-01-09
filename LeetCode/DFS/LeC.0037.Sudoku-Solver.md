# LeC.0037.Sudoku-Solver

## 题目

Write a program to solve a Sudoku puzzle by filling the empty cells.

A sudoku solution must satisfy **all of the following rules**:

1. Each of the digits `1-9` must occur exactly once in each row.
2. Each of the digits `1-9` must occur exactly once in each column.
3. Each of the the digits `1-9` must occur exactly once in each of the 9 `3x3` sub-boxes of the grid.

Empty cells are indicated by the character `'.'`.

![](https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Sudoku-by-L2G-20050714.svg/250px-Sudoku-by-L2G-20050714.svg.png)

A sudoku puzzle...

![](https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Sudoku-by-L2G-20050714_solution.svg/250px-Sudoku-by-L2G-20050714_solution.svg.png)

...and its solution numbers marked in red.

**Note:**

- The given board contain only digits `1-9` and the character `'.'`.
- You may assume that the given Sudoku puzzle will have a single unique solution.
- The given board size is always `9x9`.

## 题目大意

编写一个程序，通过已填充的空格来解决数独问题。一个数独的解法需遵循如下规则：

1. 数字 1-9 在每一行只能出现一次。
2. 数字 1-9 在每一列只能出现一次。
3. 数字 1-9 在每一个以粗实线分隔的 3x3 宫内只能出现一次。

空白格用 '.' 表示。

## 解题思路

- 给出一个数独谜题，要求解出这个数独
- 解题思路 DFS 暴力回溯枚举。数独要求每横行，每竖行，每九宫格内，`1-9` 的数字不能重复，每次放下一个数字的时候，在这 3 个地方都需要判断一次。
- 另外找到一组解以后就不需要再继续回溯了，直接返回即可。

**示例 1：**

![](https://assets.leetcode-cn.com/aliyun-lc-upload/uploads/2021/04/12/250px-sudoku-by-l2g-20050714svg.png)

```
输入：board = [
["5","3",".",".","7",".",".",".","."],
["6",".",".","1","9","5",".",".","."],
[".","9","8",".",".",".",".","6","."],
["8",".",".",".","6",".",".",".","3"],
["4",".",".","8",".","3",".",".","1"],
["7",".",".",".","2",".",".",".","6"],
[".","6",".",".",".",".","2","8","."],
[".",".",".","4","1","9",".",".","5"],
[".",".",".",".","8",".",".","7","9"]]
输出：[
["5","3","4","6","7","8","9","1","2"],
["6","7","2","1","9","5","3","4","8"],
["1","9","8","3","4","2","5","6","7"],
["8","5","9","7","6","1","4","2","3"],
["4","2","6","8","5","3","7","9","1"],
["7","1","3","9","2","4","8","5","6"],
["9","6","1","5","3","7","2","8","4"],
["2","8","7","4","1","9","6","3","5"],
["3","4","5","2","8","6","1","7","9"]]
解释：输入的数独如上图所示，唯一有效的解决方案如下所示：
```

**提示：**

- `board.length == 9`
- `board[i].length == 9`
- `board[i][j]` 是一位数字或者 `'.'`
- 题目数据 **保证** 输入数独仅有一个解

**题解**

```go
func solveSudoku(board [][]byte) {
    var line, column [9][9]bool
    var block [3][3][9]bool
    var spaces [][2]int

    for i, row := range board {
        for j, b := range row {
            if b == '.' {
                spaces = append(spaces, [2]int{i, j})
            } else {
                digit := b - '1'
                line[i][digit] = true
                column[j][digit] = true
                block[i/3][j/3][digit] = true
            }
        }
    }

    var dfs func(int) bool
    dfs = func(pos int) bool {
        if pos == len(spaces) {
            return true
        }
        i, j := spaces[pos][0], spaces[pos][1]
        for digit := byte(0); digit < 9; digit++ {
            if !line[i][digit] && !column[j][digit] && !block[i/3][j/3][digit] {
                line[i][digit] = true
                column[j][digit] = true
                block[i/3][j/3][digit] = true
                board[i][j] = digit + '1'
                if dfs(pos + 1) {
                    return true
                }
                line[i][digit] = false
                column[j][digit] = false
                block[i/3][j/3][digit] = false
            }
        }
        return false
    }
    dfs(0)
}
```
