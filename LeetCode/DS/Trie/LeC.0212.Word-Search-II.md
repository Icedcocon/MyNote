# LeC.0212.Word-Search-II

## 题目

Given a 2D board and a list of words from the dictionary, find all words in the board.

Each word must be constructed from letters of sequentially adjacent cell, where "adjacent" cells are those horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.

**Example:**

    Input: 
    board = [
      ['o','a','a','n'],
      ['e','t','a','e'],
      ['i','h','k','r'],
      ['i','f','l','v']
    ]
    words = ["oath","pea","eat","rain"]
    
    Output: ["eat","oath"]

**Note:**

1. All inputs are consist of lowercase letters `a-z`.
2. The values of `words` are distinct.

## 题目大意

给定一个二维网格 board 和一个字典中的单词列表 words，找出所有同时在二维网格和字典中出现的单词。

单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母在一个单词中不允许被重复使用。

## 解题思路

- 这一题是第 79 题的加强版，在第 79 题的基础上增加了一个 word 数组，要求找出所有出现在地图中的单词。思路还是可以按照第 79 题 DFS 搜索，不过时间复杂度特别高！
- 想想更优的解法。

**示例 1：**

![](https://assets.leetcode.com/uploads/2020/11/07/search1.jpg)

```
输入：board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words = ["oath","pea","eat","rain"]
输出：["eat","oath"]
```

**示例 2：**

![](https://assets.leetcode.com/uploads/2020/11/07/search2.jpg)

```
输入：board = [["a","b"],["c","d"]], words = ["abcb"]
输出：[]
```

**提示：**

- `m == board.length`
- `n == board[i].length`
- `1 <= m, n <= 12`
- `board[i][j]` 是一个小写英文字母
- `1 <= words.length <= 3 * 104`
- `1 <= words[i].length <= 10`
- `words[i]` 由小写英文字母组成
- `words` 中的所有字符串互不相同

**题解**

```go
type Trie struct {
    children [26]*Trie
    isWord   bool
}

func (this *Trie) Insert(word string) {
    node := this
    for _, ch := range word {
        ch -= 'a'
        if node.children[ch] == nil {
            node.children[ch] = &Trie{}
        }
        node = node.children[ch]
    }
    node.isWord = true
}

func (this *Trie) SearchWord(word string) (bool, bool) {
    node := this
    for _, ch := range word {
        ch -= 'a'
        if node.children[ch] == nil {
            return false, false
        }
        node = node.children[ch]
    }
    return true, node.isWord
}

var dirs = []struct{ x, y int }{{1, 0}, {0, 1}, {-1, 0}, {0, -1}}

func findWords(board [][]byte, words []string) []string {
    trie := Trie{}
    for _, word := range words {
        trie.Insert(word)
    }
    m, n := len(board), len(board[0])
    set := map[string]bool{}
    var res = []byte{}
    var dfs func(i, j int)
    dfs = func(i, j int) {
        b := board[i][j]
        res = append(res, b)
        isPre, isWord := trie.SearchWord(string(res))
        if isPre {
            if isWord {
                set[string(res)] = true
            }
            board[i][j] = '#'
            for _, dir := range dirs {
                if i+dir.x >= 0 && i+dir.x < m && j+dir.y >= 0 && j+dir.y < n && board[i+dir.x][j+dir.y] != '#' {
                    dfs(i+dir.x, j+dir.y)
                }
            }
            board[i][j] = b
        }
        res = res[:len(res)-1]
    }
    for i := 0; i < m; i++ {
        for j := 0; j < n; j++ {
            dfs(i, j)
        }
    }
    ans := []string{}
    for word, _ := range set {
        ans = append(ans, word)
    }
    fmt.Println()
    return ans
}
```
