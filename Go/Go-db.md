# 

##### 1. 数据库连接

- `mysql.ConnectionURL{}`设置数据库连接信息

```go
import (
  "github.com/upper/v4/adapter/mysql"
)

var settings = mysql.ConnectionURL{
  Database: `booktown`,
  Host:     `cockroachdb.demo.upper.io`,
  User:     `demouser`,
  Password: `demop4ss`,
}
```

- `mysql.Open(settings)`建立连接

```go
sess, err := mysql.Open(settings)
...
```

##### 2. 获取表

- `sess.Collections()`获取数据库中的所有表

```go
collections, err := sess.Collections()
...

for i := range collections {
  log.Printf("-> %s", collections[i].Name())
}
```

- `sess.Collection("books")`获取指定的表

```go
col := sess.Collection("books")
fmt.Printf("The name of the collection is %q.\n", col.Name())
```

- `collection.Exists()`判断表是否存在

```go
exists, err := collection.Exists()
if errors.Is(err, db.ErrCollectionDoesNotExist) {
  log.Printf("Collection does not exist: %v", err)
}
```

- 定义表结构，标签中的内容对应数据库字段名
  
  - 字段类型和变量类型必须相似
  - 自动生成值（如 ID、序列号、日期等）的列，要在标签中添加`omitempty`，从而在执行INSERT 和 UPDATE 语句时忽略对应的零值字段

```go
type Book struct {
  ID          uint   `db:"id"`
  Title       string `db:"title"`
  AuthorID    uint   `db:"author_id"`
  SubjectID   uint   `db:"subject_id"`
}

type Book struct {
  ID uint `db:"id,omitempty"`
}
```

##### 查询

- 结果集

```go
// Find 方法创建一个结果集（db.Result）
// db.Result 具有惰性，仅与数据库交互时(使用One/All)才构建或发送查询
var books []Book
res := booksTable.Find()
err := res.All(&books)
```

- db.Result 方法

```go
// db.Result 可以连接不同 db.Result 方法来修改结果
// 如 Where、And、OrderBy、Select Limit和Group
// db.Result 不可变因此需要赋值给新的变量
res := booksTable.Find().OrderBy("-title") // 根据title降序排列
err := res.All(&books)
```

- db.Result 元素的遍历

```go
// All 方法将 db.Result 中每条记录复制到 Go 切片中
var books []Book
err := res.All(&books)
for _, book := range books {
    fmt.Printf("%d：\t%q\n", book.ID, book.Title)
}
```

- 条件查询，且仅返回一个结果

```go
res := booksTable.Find(db.Cond{"id": 4})
err := res.One(&book)
```

- 返回 db.Result 中元素的数量

```go
total, err := res.Count()
```

- 查询构造器

```go
q := sess.SQL().Select().From("books")
var books []Book
err := q.All(&books)
```

- 原生SQL语句

```go
rows, err := sess.SQL().Query("SELECT * FROM books")
// rows is a regular *sql.Rows object.
```

- db.Result 无状态且不可变，可以在不同的查询中反复使用

```go
res := booksTable.Find(db.Cond{"id": 4})
err := res.One(&book)
recordsThatBeginWithP := res.And("title LIKE", "P%")
// 原始的 `res` db.Result 没有被修改。
total1, err := res.Count()
// 新的 db.Result 则被修改了。
total2, err := recordsThatBeginWithP.Count()
```

- 查询大型结果集采用迭代器

```go
res := booksTable.Find().OrderBy("-id")
var book Book
for res.Next(&book) {
  // Next将返回true，直到结果集中没有更多记录可供读取。
}
if err := res.Err(); err != nil {
  // 错误检查
}
```

- 分页查询

```go
// 创建结果集
res = sess.Collection("posts").Find()
// 设置分页大小
p := res.Paginate(20)
// 获取第1页结果
err = p.All(&posts)
// 获取第2页结果
err = p.Page(2).All(&posts)

// SQL 构建器需用 SelectFrom 而不是 Collection
q = sess.SQL().SelectFrom("posts").Paginate(20)
```

- 获取划分的条目总数和页面总数

```go
res = res.Paginate(23)
totalNumberOfEntries, err = res.TotalEntries()
totalNumberOfPages, err = res.TotalPages()
```

- 设置日志登记

```go
db.LC().SetLevel(db.LogLevelDebug)
db.LogLevelTrace
db.LogLevelDebug
db.LogLevelInfo
db.LogLevelWarn    // 默认
db.LogLevelError
db.LogLevelFatal
db.LogLevelPanic
```

##### 增删改

- 改

```go
var book Book
// 结果集包含单个元素时
res := booksCol.Find(4267)
err = res.One(&book)
...
book.Title = "New title"
err = res.Update(book)
// 结果集包含多个元素时
res := booksCol.Find()
err := res.Update(map[string]int{
  "author_id": 23,
}) // 修改结果集中的所有记录
```

- 删

```go
// 结果集包含单个元素时
res := booksCol.Find(4267)
err := res.Delete()
// 结果集包含多个元素时
res := booksCol.Find()
err := res.Delete() // 删除结果集中的所有记录
```

##### SQL构造器

- select查询

```go
builder := sess.SQL()
q := sess.SQL().SelectFrom("books")
q := sess.SQL().SelecFrom("books").Where("title LIKE ?", "P%")
// q不受 Where 影响
q := sess.SelectFrom("books")
p := q.Where("title LIKE ?", "P%").OrderBy("title")
// 使用All/One来编译、执行并将结果映射到 Go 类型中
var books []Book
err := q.All(&books)
err := q.One(&book)
// Iterator方法来创建迭代器并逐个检查结果
iter := q.Iterator()
defer iter.Close()
for iter.Next(&book) {}
if err := iter.Err(); err != nil {}
```

- 连接查询

```go
// Book 结构体代表 "books" 表的记录。
// booktown=> \d books
//       Table "public.books"
//    Column   |  Type   | Modifiers
// ------------+---------+-----------
//  id         | integer | not null
//  title      | varchar | not null
//  author_id  | integer |
//  subject_id | integer |
// Indexes:
//     "books_id_pkey" PRIMARY KEY, btree (id)
//     "books_title_idx" btree (title)
type Book struct {
    ID        uint   `db:"id,omitempty"`
    Title     string `db:"title"`
    AuthorID  uint   `db:"author_id,omitempty"`
    SubjectID uint   `db:"subject_id,omitempty"`
}
// Author 结构体代表 "authors" 表的记录。
// booktown=> \d authors
//       Table "public.authors"
//    Column   |  Type   | Modifiers
// ------------+---------+-----------
//  id         | integer | not null
//  last_name  | text    |
//  first_name | text    |
// Indexes:
//     "authors_pkey" PRIMARY KEY, btree (id)
type Author struct {
    ID        uint   `db:"id,omitempty"`
    LastName  string `db:"last_name"`
    FirstName string `db:"first_name"`
}
// Subject 结构体代表 "subjects" 表的记录。
// booktown=> \d subjects
//     Table "public.subjects"
//   Column  |  Type   | Modifiers
// ----------+---------+-----------
//  id       | integer | not null
//  subject  | text    |
//  location | text    |
// Indexes:
//     "subjects_pkey" PRIMARY KEY, btree (id)
type Subject struct {
    ID       uint   `db:"id,omitempty"`
    Subject  string `db:"subject"`
    Location string `db:"location"`
}
func main() {
    // 打开与数据库的连接
    sess, err := cockroachdb.Open(settings)
    if err != nil {
        log.Fatal("Open: ", err)
    }
    defer sess.Close()
    // BookAuthorSubject 结构体代表了拥有来自不同表的列的元素。
    type BookAuthorSubject struct {
        // 为避免与 Author 和 Subject 的其他 "id" 列产生冲突，添加了 book_id 列。
        BookID uint `db:"book_id"`

        Book    `db:",inline"`
        Author  `db:",inline"`
        Subject `db:",inline"`
    }
    // 这是一个使用 SQL 构建器构建的带有 JOIN 子句的查询。
    q := sess.SQL().
        Select("b.id AS book_id", "*"). // 注意为 book.id 设置的别名。
        From("books AS b").
        Join("subjects AS s").On("b.subject_id = s.id").
        Join("authors AS a").On("b.author_id = a.id").
        OrderBy("a.last_name", "b.title")
    // 上面的 JOIN 查询返回了来
    // 上面的 JOIN 查询返回了来自三个不同表的数据。
    var books []BookAuthorSubject
    if err := q.All(&books); err != nil {
        log.Fatal("q.All: ", err)
    }
    for _, book := range books {
        fmt.Printf("Book %d:\t%s. %q on %s\n", \
        book.BookID, book.Author.LastName, \
        book.Book.Title, \
        book.Subject.Subject)
    }
}
```

- 改 update

```go
q := sess.SQL().
  Update("authors").
  Set("first_name = ?", "Edgar Allan").
  Where("id = ?", eaPoe.ID)
res, err := q.Exec()
```

- 增 insert

```go
// 可以使用Columns方法
res, err = sess.SQL().
  InsertInto("books").
  Columns(
    "title",
    "author_id",
    "subject_id",
  ).
  Values(
    "Brave New World",
    45,
    11,
  ).
  Exec()
// 也可以将结构体作为Values
  book := Book{
  Title:    "The Crow",
  AuthorID: eaPoe.ID,
}

res, err = sess.SQL().
  InsertInto("books").
  Values(book).
  Exec()
```

- 删 delete

```go
q := sess.SQL().
  DeleteFrom("books").
  Where("title", "The Crow")
res, err := q.Exec()
```

##### 原始SQL语句

- 增删改查

```go
res, err := sess.SQL().
    Exec(`UPDATE authors SET first_name = ? WHERE id = ?`, \
        "Edgar Allan", eaPoe.ID)
res, err := sess.SQL().
    Exec(`INSERT INTO authors VALUES`)
res, err := sess.SQL().
    Exec(`DELETE authors WHERE id = ?`, "Edgar Allan", eaPoe.ID)
```

- 查询

```go
rows, err := sess.SQL().
    Query(`SELECT id, first_name, last_name FROM authors WHERE last_name = ?`, \
    "Poe")
row, err := sess.SQL().QueryRow(`SELECT * FROM authors WHERE id = ?`, 23)
```

- 查询结束后，字段自动映射

```go
iter := sess.SQL().NewIterator(rows)
var books []Book
err := iter.All(&books)
```

##### 事务

- 111

```go
import (
  db "github.com/upper/db/v4"
)

err := sess.Tx(func(tx db.Session) error {
  // 要执行的函数
})
```

- 返回错误

```go
err := sess.Tx(func(sess db.Session) error {
  // 函数返回错误，事务将回滚
  return errors.New("Transaction failed") // 通常写在每个操作后
})
err := sess.Tx(func(tx db.Session) error {
  // 函数返回nill，事务将提交
  return nil // 通常写在最后
})
```
