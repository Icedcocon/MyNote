# LeC.1707.Maximum-XOR-With-an-Element-From-Array

给你一个由非负整数组成的数组 `nums` 。另有一个查询数组 `queries` ，其中 `queries[i] = [xi, mi]` 。

第 `i` 个查询的答案是 `xi` 和任何 `nums` 数组中不超过 `mi` 的元素按位异或（`XOR`）得到的最大值。换句话说，答案是 `max(nums[j] XOR xi)` ，其中所有 `j` 均满足 `nums[j] <= mi` 。如果 `nums` 中的所有元素都大于 `mi`，最终答案就是 `-1` 。

返回一个整数数组 `answer` 作为查询的答案，其中 `answer.length == queries.length` 且 `answer[i]` 是第 `i` 个查询的答案。

**示例 1：**

```
输入：nums = [0,1,2,3,4], queries = [[3,1],[1,3],[5,6]]
输出：[3,3,7]
解释：
1) 0 和 1 是仅有的两个不超过 1 的整数。0 XOR 3 = 3 而 1 XOR 3 = 2 。二者中的更大值是 3 。
2) 1 XOR 2 = 3.
3) 5 XOR 2 = 7.
```

**示例 2：**

```
输入：nums = [5,2,4,6,6,3], queries = [[12,4],[8,1],[6,3]]
输出：[15,-1,5]
```

**提示：**

- `1 <= nums.length, queries.length <= 105`
- `queries[i].length == 2`
- `0 <= nums[j], xi, mi <= 109`

**题解**

```go
const maxBit = 30

type Trie struct {
    children [2]*Trie
}

func (this *Trie) add(num int) {
    node := this
    for i := maxBit - 1; i >= 0; i-- {
        bit := num >> i & 1
        if node.children[bit] == nil {
            node.children[bit] = &Trie{}
        }
        node = node.children[bit]
    }
}

func (this *Trie) check(num int) (ans int) {
    node := this
    for i := maxBit - 1; i >= 0; i-- {
        bit := num >> i & 1
        if node.children[bit^1] != nil {
            ans |= 1 << i
            bit ^= 1
        }
        node = node.children[bit]
    }
    return
}

func maximizeXor(nums []int, queries [][]int) []int {
    sort.Ints(nums)

    for i := range queries {
        queries[i] = append(queries[i], i)
    }
    sort.Slice(queries, func(x, y int) bool { return queries[x][1] < queries[y][1] })

    ans := make([]int, len(queries))
    trie := &Trie{}
    idx, n := 0, len(nums)
    for _, q := range queries {
        x, m, qid := q[0], q[1], q[2]
        for idx < n && nums[idx] <= m {
            trie.add(nums[idx])
            idx++
        }
        if idx == 0 { // 字典树为空
            ans[qid] = -1
        } else {
            ans[qid] = trie.check(x)
        }
    }
    return ans
}
```
