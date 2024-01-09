# LeC.0211.Design-Add-and-Search-Words-Data-Structure

## 题目

Design a data structure that supports the following two operations:

    void addWord(word)
    bool search(word)

search(word) can search a literal word or a regular expression string containing only letters `a-z` or `.`. A `.` means it can represent any one letter.

**Example:**

    addWord("bad")
    addWord("dad")
    addWord("mad")
    search("pad") -> false
    search("bad") -> true
    search(".ad") -> true
    search("b..") -> true

**Note:**You may assume that all words are consist of lowercase letters `a-z`.

## 题目大意

设计一个支持以下两种操作的数据结构：`void addWord(word)`、`bool search(word)`。`search(word)` 可以搜索文字或正则表达式字符串，字符串只包含字母 . 或 a-z 。 "." 可以表示任何一个字母。

## 解题思路

- 设计一个 `WordDictionary` 的数据结构，要求具有 `addWord(word)` 和 `search(word)` 的操作，并且具有模糊查找的功能。
- 这一题是第 208 题的加强版，在第 208 题经典的 Trie 上加上了模糊查找的功能。其他实现一模一样。

**示例：**

```
输入：
["WordDictionary","addWord","addWord","addWord","search","search","search","search"]
[[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]
输出：
[null,null,null,null,false,true,true,true]

解释：
WordDictionary wordDictionary = new WordDictionary();
wordDictionary.addWord("bad");
wordDictionary.addWord("dad");
wordDictionary.addWord("mad");
wordDictionary.search("pad"); // 返回 False
wordDictionary.search("bad"); // 返回 True
wordDictionary.search(".ad"); // 返回 True
wordDictionary.search("b.."); // 返回 True
```

**提示：**

- `1 <= word.length <= 25`
- `addWord` 中的 `word` 由小写英文字母组成
- `search` 中的 `word` 由 '.' 或小写英文字母组成
- 最多调用 `104` 次 `addWord` 和 `search`

```go
type WordDictionary struct {
    isWord   bool
    children [26]*WordDictionary
}

func Constructor() WordDictionary {
    return WordDictionary{isWord: false, children: [26]*WordDictionary{}}
}

func (this *WordDictionary) AddWord(word string) {
    node := this
    for _, ch := range word {
        ch -= 'a'
        if node.children[ch] == nil {
            node.children[ch] = &WordDictionary{isWord: false, children: [26]*WordDictionary{}}
        }
        node = node.children[ch]
    }
    node.isWord = true
}

func (this *WordDictionary) Search(word string) bool {
    node := this
    for i, ch := range word {
        if ch == '.' {
            isMatched := false
            for _, v := range node.children {
                if v != nil && v.Search(word[i+1:]) {
                    isMatched = true
                }
            }
            return isMatched
        } else if node.children[ch-'a'] == nil {
            return false
        }
        node = node.children[ch-'a']
    }
    return node.isWord
}
```
