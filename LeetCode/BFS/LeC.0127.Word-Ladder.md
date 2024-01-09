# LeC.0127.Word-Ladder

**Hard**

## 题目

Given two words (*beginWord* and *endWord*), and a dictionary's word list, find the length of shortest transformation sequence from *beginWord* to *endWord*, such that:

1. Only one letter can be changed at a time.
2. Each transformed word must exist in the word list. Note that *beginWord* is *not* a transformed word.

**Note:**

- Return 0 if there is no such transformation sequence.
- All words have the same length.
- All words contain only lowercase alphabetic characters.
- You may assume no duplicates in the word list.
- You may assume *beginWord* and *endWord* are non-empty and are not the same.

**Example 1:**

    Input:
    beginWord = "hit",
    endWord = "cog",
    wordList = ["hot","dot","dog","lot","log","cog"]
    
    Output: 5
    
    Explanation: As one shortest transformation is "hit" -> "hot" -> "dot" -> "dog" -> "cog",
    return its length 5.

**Example 2:**

    Input:
    beginWord = "hit"
    endWord = "cog"
    wordList = ["hot","dot","dog","lot","log"]
    
    Output: 0
    
    Explanation: The endWord "cog" is not in wordList, therefore no possible transformation.

## 题目大意

给定两个单词（beginWord 和 endWord）和一个字典，找到从 beginWord 到 endWord 的最短转换序列的长度。转换需遵循如下规则：

1. 每次转换只能改变一个字母。
2. 转换过程中的中间单词必须是字典中的单词。

说明:

- 如果不存在这样的转换序列，返回 0。
- 所有单词具有相同的长度。
- 所有单词只由小写字母组成。
- 字典中不存在重复的单词。
- 你可以假设 beginWord 和 endWord 是非空的，且二者不相同。

## 解题思路

- 这一题要求输出从 `beginWord` 变换到 `endWord` 最短变换次数。可以用 BFS，从 `beginWord` 开始变换，把该单词的每个字母都用 `'a'~'z'` 变换一次，生成的数组到 `wordList` 中查找，这里用 Map 来记录查找。找得到就入队列，找不到就输出 0 。入队以后按照 BFS 的算法依次遍历完，当所有单词都 `len(queue)<=0` 出队以后，整个程序结束。
- 这一题题目中虽然说了要求找到一条最短的路径，但是实际上最短的路径的寻找方法已经告诉你了：
  1. 每次只变换一个字母
  2. 每次变换都必须在 `wordList` 中  
     所以不需要单独考虑何种方式是最短的。 

**示例 1：**

```
输入：beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
输出：5
解释：一个最短转换序列是 "hit" -> "hot" -> "dot" -> "dog" -> "cog", 返回它的长度 5。
```

**示例 2：**

```
输入：beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
输出：0
解释：endWord "cog" 不在字典中，所以无法进行转换。
```

**提示：**

- `1 <= beginWord.length <= 10`
- `endWord.length == beginWord.length`
- `1 <= wordList.length <= 5000`
- `wordList[i].length == beginWord.length`
- `beginWord`、`endWord` 和 `wordList[i]` 由小写英文字母组成
- `beginWord != endWord`
- `wordList` 中的所有字符串 **互不相同**

**题解：**

```go
func ladderLength(beginWord string, endWord string, wordList []string) int {
    wordId := map[string]int{}
    graph := [][]int{}
    addWord := func(word string) int {
        id, has := wordId[word]
        if !has {
            id = len(wordId)
            wordId[word] = id
            graph = append(graph, []int{})
        }
        return id
    }
    addEdge := func(word string) int {
        id1 := addWord(word)
        s := []byte(word)
        for i, b := range s {
            s[i] = '*'
            id2 := addWord(string(s))
            graph[id1] = append(graph[id1], id2)
            graph[id2] = append(graph[id2], id1)
            s[i] = b
        }
        return id1
    }

    for _, word := range wordList {
        addEdge(word)
    }
    beginId := addEdge(beginWord)
    endId, has := wordId[endWord]
    if !has {
        return 0
    }

    const inf int = math.MaxInt64
    dist := make([]int, len(wordId))
    for i := range dist {
        dist[i] = inf
    }
    dist[beginId] = 0
    queue := []int{beginId}
    for len(queue) > 0 {
        v := queue[0]
        queue = queue[1:]
        if v == endId {
            return dist[endId]/2 + 1
        }
        for _, w := range graph[v] {
            if dist[w] == inf {
                dist[w] = dist[v] + 1
                queue = append(queue, w)
            }
        }
    }
    return 0
}



func ladderLength(beginWord string, endWord string, wordList []string) int {
    wordId := map[string]int{}
    graph := [][]int{}
    addWord := func(word string) int {
        id, has := wordId[word]
        if !has {
            id = len(wordId)
            wordId[word] = id
            graph = append(graph, []int{})
        }
        return id
    }
    addEdge := func(word string) int {
        id1 := addWord(word)
        s := []byte(word)
        for i, b := range s {
            s[i] = '*'
            id2 := addWord(string(s))
            graph[id1] = append(graph[id1], id2)
            graph[id2] = append(graph[id2], id1)
            s[i] = b
        }
        return id1
    }

    for _, word := range wordList {
        addEdge(word)
    }
    beginId := addEdge(beginWord)
    endId, has := wordId[endWord]
    if !has {
        return 0
    }

    const inf int = math.MaxInt64
    distBegin := make([]int, len(wordId))
    for i := range distBegin {
        distBegin[i] = inf
    }
    distBegin[beginId] = 0
    queueBegin := []int{beginId}

    distEnd := make([]int, len(wordId))
    for i := range distEnd {
        distEnd[i] = inf
    }
    distEnd[endId] = 0
    queueEnd := []int{endId}

    for len(queueBegin) > 0 && len(queueEnd) > 0 {
        q := queueBegin
        queueBegin = nil
        for _, v := range q {
            if distEnd[v] < inf {
                return (distBegin[v]+distEnd[v])/2 + 1
            }
            for _, w := range graph[v] {
                if distBegin[w] == inf {
                    distBegin[w] = distBegin[v] + 1
                    queueBegin = append(queueBegin, w)
                }
            }
        }

        q = queueEnd
        queueEnd = nil
        for _, v := range q {
            if distBegin[v] < inf {
                return (distBegin[v]+distEnd[v])/2 + 1
            }
            for _, w := range graph[v] {
                if distEnd[w] == inf {
                    distEnd[w] = distEnd[v] + 1
                    queueEnd = append(queueEnd, w)
                }
            }
        }
    }
    return 0
}
```
