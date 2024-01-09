##### 打开数据库

- `badger.Open` 会获取目录锁，多个进程无法同时打开同一个数据库

```go
package main

import (
    "log"
    badger "github.com/dgraph-io/badger/v3"
)
func main() {
  // 打开 /tmp/badger 路径下的数据库; 不存在则创建
  db, err := badger.Open(badger.DefaultOptions("/tmp/badger"))
  if err != nil {
      log.Fatal(err)
  }
  defer db.Close() // 进程结束时关闭数据库连接
}
```

- 内存模式/无盘模式

```go
// 默认 Badger 保存数据到磁盘; WithInMemory可以设置纯内存模式;
// 纯内存模式读写速度快;数据在崩溃/关闭时丢失;
opt := badger.DefaultOptions("").WithInMemory(true)
```

- 加密方式

```go
// 启用加密需设置索引缓存大小;否则启用加密时读取速度会非常慢
opts.IndexCache = 100 << 20 // 100 MB缓存
```

##### 事务

- 只读事务

```go
err := db.View(func(txn *badger.Txn) error {
  // 不能进行写入或删除
  return nil
})
```

- 读写事务

```go
err := db.Update(func(txn *badger.Txn) error {
  //允许所有数据库操作; 返回错误会被传递
  return nil
})
```

- 手动管理事务
  - View 和 Update(推荐) 在DB.NewTransaction() 和 Txn.Commit()基础上进行封装

```go
// 布尔参数指定是否是可写
// 读写事务需调用 Txn.Commit() 提交事务; 只读事务仅调用 Txn.Discard() 即可
txn := db.NewTransaction(true)
defer txn.Discard()
err := txn.Set([]byte("answer"), []byte("42"))
if err != nil {
    return err
}
// Txn.Commit() 检查冲突后立即返回,读写异步进行;写完或异常后调用回调函数
// Txn.Commit() 方法可填写回调函数,默认为nil; 
if err := txn.Commit(); err != nil {
    return err
}
```

##### 键/值对

- `Txn.Set()`方法保存键值对

```go
err := db.Update(func(txn *badger.Txn) error {
  err := txn.Set([]byte("answer"), []byte("42"))
  return err
})
```

- `Txn.SetEntry()`方法保存键值对

```go
err := db.Update(func(txn *badger.Txn) error {
  e := badger.NewEntry([]byte("answer"), []byte("42")) // 先创建 Entry
  err := txn.SetEntry(e)  // 用 Txn.SetEntry() 设置该 Entry 来保存
  return err
})
```

- `Txn.Get()`方法获取键值对
  - `Get()`返回值仅在事务内有效,事务外使用需用`copy()`复制

```go
err := db.View(func(txn *badger.Txn) error {
    item, err := txn.Get([]byte("answer"))  // Get()方法获取item对象
    handle(err)
    var valNot, valCopy []byte
    err := item.Value(func(val []byte) error {
      // 读取值的内容到字节数组val中
      valCopy = append([]byte{}, val...) // 可以复制或解析val
      valNot = val // 不能将val切片直接赋值给另一个变量(局部作用域)
      return nil
    })
    handle(err)
    fmt.Printf("答案是：%s\n", valCopy) // 复制后可在item.Value()外使用
    valCopy, err = item.ValueCopy(nil) // item.ValueCopy()也可以赋值
    handle(err)
    fmt.Printf("答案是：%s\n", valCopy)
    return nil
  })
```

- `Txn.Delete()`方法删除键值对

##### 单调递增整数

- `DB.GetSequence`方法返回Sequence对象; 该对象线程安全

```go
seq, err := db.GetSequence(key, 1000)
defer seq.Release()
for {
  num, err := seq.Next()
}
```

##### 合并操作

- MergeFunc的函数将两个值合并,返回一个新值，合并规则由合并函数指定

```go
// 将一个字节切片附加到另一个字节切片的合并函数
func add(originalValue, newValue []byte) []byte {
  return append(originalValue, newValue...)
}

key := []byte("merge")
// GetMergeOperator(要merge的键、合并函数、持续时间值(指定合并频率))
m := db.GetMergeOperator(key, add, 200*time.Millisecond)
defer m.Stop()
m.Add([]byte("A"))
m.Add([]byte("B"))
m.Add([]byte("C"))
res, _ := m.Get() 
```
