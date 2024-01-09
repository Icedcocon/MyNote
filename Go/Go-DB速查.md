# upper/db库速查表

### 1. 数据库的连接及表的查询

- 数据库连接

```go
import "github.com/upper/v4/adapter/mysql"
var settings = mysql.ConnectionURL{
  Database: `booktown`,
  Host:     `cockroachdb.demo.upper.io`,
  User:     `demouser`,
  Password: `demop4ss`,
}
sess, err := mysql.Open(settings)
```

- 表的查询

```go
// (1) 获取所有表格
collections, err := sess.Collections()
for i := range collections {
  log.Printf("-> %s", collections[i].Name())
}
// (2) 获取某张表格
col := sess.Collection("books")
fmt.Printf("The name of the collection is %q.\n", col.Name())
// (3) 判断表格是否存在
exists, err := collection.Exists()
if errors.Is(err, db.ErrCollectionDoesNotExist) {
  log.Printf("Collection does not exist: %v", err)
}
```

- 表的映射

```go
// omitempty标签字段值为0时, Insert、Update操作将忽略该字段
// 常用于有auto_increment属性的字段
type Book struct {
  ID        int    `db:"id,omitempty"` 
  Title     string `db:"title"`
  AuthorID  int    `db:"author_id"`
  SubjectID int    `db:"subject_id"`
}

// 可以在 db tag 后使用 json tag 从而让结构体既能映射DB也能映射json数据
type Author struct {
  ID        int    `db:"id,omitempty"` // Also has an ID column.
  LastName  string `db:"last_name" json:"last_name"`
  FirstName string `db:"first_name" json:"first_name"`
}

// BookAuthor
type BookAuthor struct {
  // Author 和 Book 都有 ID 字段， 引入book_id字段，并在查询时定义别名加以区分
  BookID int `db:"book_id,omitempty"`

  Author `db:",inline"`
  Book   `db:",inline"`
}
req := sess.SQL().
  Select("b.id AS book_id", db.Raw("b.*"), db.Raw("a.*"),).
  From("books b").
  Join("authors a").On("b.author_id = a.id").
  OrderBy("b.title")
var books []BookAuthor
if err := req.All(&books); err != nil {
  log.Fatal(err)
}
for _, book := range books {
  fmt.Printf(
    "ID: %d\tAuthor: %s\t\tBook: %q\n",
    book.BookID, book.Author.LastName, book.Book.Title,
  )
```

### 2. 原生SQL

- 增

```go
res, err := sess.SQL().
    Exec(`INSERT INTO authors VALUES`)
```

- 删

```go
res, err := sess.SQL().
    Exec(`DELETE authors WHERE id = ?`, "Edgar Allan", eaPoe.ID)
```

- 改

```go
res, err := sess.SQL().
    Exec(`UPDATE authors SET first_name = ? WHERE id = ?`, \
        "Edgar Allan", eaPoe.ID)
```

- 查

```go
rows, err := sess.SQL().
    Query(`SELECT id, first, last FROM authors WHERE last = ?`, \
    "Poe")
row, err := sess.SQL().QueryRow(`SELECT * FROM authors WHERE id = ?`, 23)
```

### 3. SQL构造器(SQL Builder)

- 查

```go
type Book struct {
    ID        uint   `db:"id"`
    Title     string `db:"title"`
    AuthorID  uint   `db:"author_id"`
    SubjectID uint   `db:"subject_id"`
}
builder := sess.SQL()
q1 := sess.SQL().SelectFrom("books")
q2 := sess.SQL().SelecFrom("books").Where("title LIKE ?", "P%")
var books []Book
var book Book
err := q1.All(&books)
err := q2.One(&book)
// 方法一: 对结构体或映射进行遍历
for _, book := range books {
    fmt.Printf("%d：\t%q\n", book.ID, book.Title)
}
// 方法二: 创建迭代器进行遍历
iter := q1.Iterator()   // 返回Iterator对象
defer iter.Close()      // 遍历结束后必须关闭
for iter.Next(&book) {
    // 执行遍历操作
}
if err := iter.Err(); err != nil {} // 判断报错
```

- 增 insert

```go
// 方法一: 可以使用Columns方法
res, err = sess.SQL().
  InsertInto("books").
  Columns("title", "author_id", "subject_id").
  Values("Brave New World", 45, 11).
  Exec()
// 方法二: 也可以将结构体作为Values
book := Book{
  Title:    "The Crow",
  AuthorID: ID,
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

- 改 update

```go
q := sess.SQL().
  Update("authors").
  Set("first_name = ?", "Edgar Allan").
  Where("id = ?", eaPoe.ID)
res, err := q.Exec()
```

### 4. 通用方法

### 5. 接口

### 6. SQL类型接口

- SQL接口

```go
type SQL interface {
    // (1) 返回 Selector; 接受列名作为参数
    // q := sqlbuilder.Select("first_name","last_name").
    //                 From("people").
    //                 Where(...)
    Select(columns ...interface{}) Selector

    // (2) 返回 Selector; 从给定表格中选择所有列（类似 SELECT *）
    // q := sqlbuilder.SelectFrom("people").Where(...)
    SelectFrom(table ...interface{}) Selector

    // (3) 返回 Inserter; 目标为给定表格
    // q := sqlbuilder.InsertInto("books").Columns(...).Values(...)
    InsertInto(table string) Inserter

    // (4) 返回 Deleter; 目标为给定的表格
    // q := sqlbuilder.DeleteFrom("tasks").Where(...)
    DeleteFrom(table string) Deleter

    // (5) 返回 Updater; 目标为给定的表格
    // q := sqlbuilder.Update("profile").Set(...).Where(...)
    Update(table string) Updater

    // (6) 返回 Result; 不返回行
    // sqlbuilder.Exec(`INSERT INTO books (title) 
    //                  VALUES("La Ciudad y los Perros")`)
    Exec(query interface{}, args ...interface{}) (sql.Result, error)

    // (7) 返回 Rows; 参数是字符串或upper-db语句
    Query(query interface{}, args ...interface{}) (*sql.Rows, error)

    // (8) 返回 Row(1行); 参数是字符串或upper-db语句
    //  sqlbuilder.QueryRow(`SELECT * FROM people WHERE name = \
    //  "Haruki" AND last_name = "Murakami" LIMIT 1`)
    QueryRow(query interface{}, args ...interface{}) (*sql.Row, error)

    // (9) 返回Iterator, 可查询多行数据
    //  sqlbuilder.Iterator(`SELECT * FROM people WHERE name LIKE "M%"`)
    Iterator(query interface{}, args ...interface{}) Iterator

    // (10) NewIterator 将 *sql.Rows 值转换为 Iterator。
    NewIterator(rows *sql.Rows) Iterator
}
```

### 7. Iterator类型接口

```go
type Iterator interface {
    // (1) ResultMapper提供了一些方法来检索和映射结果。
    ResultMapper

    // (2) Scan将当前结果转储到给定指针变量指针中。
    Scan(dest ...interface{}) error

    // (3) NextScan推进迭代器并执行Scan。
    NextScan(dest ...interface{}) error

    // (4) ScanOne推进迭代器，执行Scan并关闭迭代器。
    ScanOne(dest ...interface{}) error

    // (5) Next将当前元素转储到给定的目标中，可以是指向映射或结构体的指针。
    Next(dest ...interface{}) bool

    // (6) Err返回游标产生的最后一个错误。
    Err() error

    // (7) Close关闭迭代器并释放游标。
    Close() error
}
```

### 8. Result类型接口

```go
type Result interface {

    // (1) 返回用于在查询中使用的SQL语句
    String() string

    // (2) 定义此集合的最大结果数;仅对One()、All()和Next()有影响;负值取消所有限制
    Limit(int) Result

    // (3) 忽略前n个结果;仅对One()、All()和Next()有影响;负值取消所有偏移量设置
    Offset(int) Result

    // (4) 接收一个或多个字段名,定义返回查询结果的顺序;字段名带负号(-)表示降序排列
    OrderBy(...interface{}) Result

    // (5) 接收一个或多个字段名,定义要在结果集中的每个列上获取的特定列
    Select(...interface{}) Result

    // (6) 在现有约束条件之上添加更多过滤条件
    //   res := col.Find(...).And(...)
    And(...interface{}) Result

    // (7) 接收一个或多个字段名,用于将在同一列或多个列中具有相同值的结果分组
    GroupBy(...interface{}) Result

    // (8) 删除结果集中的所有项目; 不会考虑Offset()和Limit()。
    Delete() error

    // (9) 修改结果集中的所有项目; 不会考虑Offset()和Limit()
    Update(interface{}) error

    // (10) 返回符合集合条件的项目数; 不会考虑Offset()和Limit()
    Count() (uint64, error)

    // (11) 如果集合中至少有一个项目存在,则返回true;,否则返回false
    Exists() (bool, error)

    // (12) 获取下个结果,并转储到结构体或映射的指针中; 遍历完后必须调用Close()
    Next(ptrToStruct interface{}) bool

    // (13) 返回结果集中最后发生的错误; 否则返回nil
    Err() error

    // (14) 获取第一个结果,并转储到结构体或映射的指针中; 自动关闭,无需调用Close()
    One(ptrToStruct interface{}) error

    // (15) 获取所有结果,并转储到结构体或映射的指针中; 结果集自动关闭无需调用Close()
    All(sliceOfStructs interface{}) error

    // (16) 结果分页,每页含pageSize个元素;忽略Limit()和Offset(),页面编号从1开始
    //   r = q.Paginate(12)
    //   res := q.Where(conds).OrderBy("-id").Paginate(12)
    //   err := res.Page(4).All(&items)
    Paginate(pageSize uint) Result

    // (17) 仅返回来自由pageNumber标识的页面的结果集; 页面编号从1开始。
    //   r = q.Paginate(12).Page(4)
    Page(pageNumber uint) Result

    // (18) 返回结果集可能生成的总页数; 如果没有设置分页参数，则此值等于1
    TotalPages() (uint, error)

    // (19) 返回结果集中匹配项的总数
    TotalEntries() (uint64, error)

    // (20) 关闭结果集并释放所有锁定的资源
    Close() error
}
```

### 9. Session类型接口

```go
type Session interface {
    // (1) 返回连接数据库时使用的 ConnectionURL
    ConnectionURL() ConnectionURL

    // (2) 返回数据库的名称
    Name() string

    // (3) 检测是否能连接上数据库，若不能则返回错误。
    Ping() error

    // (4) 接收一个表名，返回一个集合引用; 从集合中检索的信息会被缓存;
    Collection(name string) Collection

    // (5) 返回数据库中所有非系统表的集合引用;
    Collections() ([]Collection, error)

    // (6) 创建或更新一条记录
    Save(record Record) error

    // (7) 检索与给定条件匹配的记录
    Get(record Record, cond interface{}) error

    // (8) 删除一条记录
    Delete(record Record) error

    // (9) 重置适配器使用的所有缓存机制
    Reset()

    // (10) 终止当前活动的与数据库管理系统的连接，并清除所有缓存
    Close() error

    // (11) 返回 SQL 数据库的特殊接口
    SQL() SQL

    // (12) 创建事务块并传递给函数 fn; fn返回nil则提交事务,否则回滚事务; 事务会自动关闭
    Tx(fn func(sess Session) error) error

    // (13) 返回在此会话上用作查询默认值和新事务的上下文
    //      如果没有设置上下文，则返回默认的 context.Background()
    Context() context.Context

    // (14) 该接口包含方法来设置连接的超时、设置最大连接数等设置
    Settings
}
```
