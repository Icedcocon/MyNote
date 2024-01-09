# LeC.0208.Implement-Trie(Prefix-Tree)

## 题目

Implement a trie with `insert`, `search`, and `startsWith` methods.

**Example:**

    Trie trie = new Trie();
    
    trie.insert("apple");
    trie.search("apple");   // returns true
    trie.search("app");     // returns false
    trie.startsWith("app"); // returns true
    trie.insert("app");   
    trie.search("app");     // returns true

**Note:**

- You may assume that all inputs are consist of lowercase letters `a-z`.
- All inputs are guaranteed to be non-empty strings.

## 题目大意

实现一个 Trie (前缀树)，包含 insert, search, 和 startsWith 这三个操作。

## 解题思路

- 要求实现一个 Trie 的数据结构，具有 `insert`, `search`, `startsWith` 三种操作
- 这一题就是经典的 Trie 实现。本题的实现可以作为 Trie 的模板。

**示例：**

```
输入
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
输出
[null, null, true, false, true, null, true]

解释
Trie trie = new Trie();
trie.insert("apple");
trie.search("apple");   // 返回 True
trie.search("app");     // 返回 False
trie.startsWith("app"); // 返回 True
trie.insert("app");
trie.search("app");     // 返回 True
```

**提示：**

- `1 <= word.length, prefix.length <= 2000`
- `word` 和 `prefix` 仅由小写英文字母组成
- `insert`、`search` 和 `startsWith` 调用次数 **总计** 不超过 `3 * 104` 次

**题解**

```go
type Trie struct {
    isWord   bool
    children [26]*Trie
}

func Constructor() Trie {
    return Trie{isWord: false, children: [26]*Trie{}}
}

func (this *Trie) Insert(word string) {
    node := this
    for _, ch := range word {
        ch -= 'a'
        if node.children[ch] == nil {
            node.children[ch] = &Trie{isWord: false, children: [26]*Trie{}}
        }
        node = node.children[ch]
    }
    node.isWord = true
}

func (this *Trie) Search(word string) bool {
    node := this
    for _, ch := range word {
        ch -= 'a'
        if node.children[ch] == nil {
            return false
        }
        node = node.children[ch]
    }
    return node.isWord
}

func (this *Trie) StartsWith(prefix string) bool {
    node := this
    for _, ch := range prefix {
        ch -= 'a'
        if node.children[ch] == nil {
            return false
        }
        node = node.children[ch]
    }
    return true
}
```
