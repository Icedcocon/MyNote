```bash
########################################################################
# 前言
########################################################################
# 1.什么是Go？
# Go是一门并发支持、垃圾回收的编译型系统编程语言
# 旨在创造一门具有在静态编译语言的高性能和动态语言的高效开发之间
# 拥有良好平衡点的一门编程语言。

# 2.Go的主要特点有哪些？
# (1) 类型安全 和 内存安全
# (2) 以非常直观和极低代价的方案实现 高并发
# (3) 高效的垃圾回收机制
# (4) 快速编译（同时解决C语言中头文件太多的问题）
# (5) 为多核计算机提供性能提升的方案
# (6) UTF-8编码支持

# 3.Go环境变量与工作目录
# (1) bin（存放编译后生成的可执行文件）
# (2) pkg（存放编译后生成的包文件）
# (3) src（存放项目源码）
bin/
    mathapp
pkg/
    平台名/如：darwin_amd64、1 inux_amd64
        mymath.a
        github.com/
src/
    mathapp/
        main.go
        mymath/
            sqrt.go
        github.com/

# 4.Go常用命令简介
# (1) go get：获取远程包（需 提前安装 git或hg）
# (2) go run：直接运行程序
# (3) go build：测试编译，检查是否有编译错误
# (4) go fmt：格式化源码（部分IDE在保存时自动调用）
# (5) go install：编译包文件并编译整个程序
# (6) go test：运行测试文件
# (7) go doc：查看文档（CHM手册）
# 配置环境
go env -w GO111MODULE=off
# 项目初始化
mkdir hello && cd hello
go mod init hello    #依赖管理。
touch main.go &vim main.go
go build -x            #编译过程。
```

```go
//#######################################################################
// 基础知识
//#######################################################################
// Go注释方法
// // ：单行注释
// /* */：多行注释

// Go程序的一般结构
// 
// (1) Go程序是通过 package 来组织的（与python类似）
// (2) 只有 package 名称为 main 的包可以包含 main 函数
// (3) 一个可执行程序 有且仅有 一个 main 包
//  
// (1) 通过 import 关键字来导入其它非 main 包
// (2) 通过 const 关键字来进行常量的定义
// (3) 通过在函数体外部使用 var 关键字来进行全局变量的声明与赋值
// (4) 通过 type 关键字来进行结构(struct)或接口(interface)的声明
// (5) 通过 func 关键字来进行函数的声明
// (1) 当前程序的包名
package main
// (2) 导入其它的包
import std "fmt"
// (3) 常量的定义
const PI=3.14
// (4) 全局变量的声明与赋值
var name="gopher"
// (5) 一般类型声明
type newType int
// (6) 结构的声明
type gopher struct{}
// (7) 接口的声明
type golang interface{}
// (8) 由main函数作为程序入口点启动
func main(){
    std.Print1n("Hello world!你好，世界！")
}

// Go程序的package
// (1) 导入package格式
import "fmt"            // ①使用格式<PackageName>.<FuncName>对包中函数调用
import "io"                // ②导入包后未调用其函数或类型将会报出编译错误
import "os"                // 如： imported and not used:"os"
import (
    "fmt"
    "io"
    "os"
)
// (2) package 别名
import (
    io "fmt"
)
io.Println("Hello world!")    // 使用别名
import (
    . "fmt"
)
Println("Hello world!")        // 省略调用
// (3) Go语言可见性规则
// 根据约定，函数名首字母小写即为private,大写 即为public

// 变量定义
// (1) 常量定义
const (
    PI = 3.14
    myConst = "const"
)
// (2) 全局变量的声明与赋值（必须在函数外）
var (
    name1 = "goHarbor"
    name2 = 123
)
// (3) 一般类型声明
type (
    type1 int
    type2 float32
)
```

```go
//#######################################################################
// 变量
//#######################################################################

// 1.基本类型
| ------ 类型 -------| - 长度 - | ---- 范围 --- | ---------- 注意事项 ----------|
// (01) bool            1字节      true, false    不可以用数字代表true或false
// (02) int/uint                                  根据运行平台可能为32或64位
// (03) int8/uint8      1字节     -128~127/0~255
// (04) byte                                      uint8别名
// (05) int16/uint16    2字节     -32768~32767/0~65535
// (06) int32/uint32    4字节     -2^32/2~2^32/2-1/0~2^32-1
// (07) rune                                      uint32别名 
// (08) int64/uint64    8字节     -2^64/2~2^64/2-1/0~2^64-1
// (09) float32/float64 4/8字节   小数位：精确到7/15小数位
// (10) complex64/complex128  8/16字节
// (11) uintptr                      足够保存指针的 32 位或 64 位整数型
// 2.其他值类型
// (1) array
// (2) struct
// (3) string
// 3.引用类型
// (1) slice
// (2) map
// (3) chan
// 4.接口类型
// (1) inteface
// 5.函数类型
// (1) func
```

```go
//#######################################################################
// 声明
//#######################################################################/
// 类型在标识符后面
// Go四种类型的声明语句：变量(var)、常量(const)、类型(type)和函数实体对象(func)
var foo int = 42             // (1) 声明的同时做初始化
var foo, bar int = 42, 1302  // (2) 一次声明和初始化多个变量
var foo = 42                 // (3) 忽略类型，编译器自行推导
foo := 42                    // (4) 简写 只能在函数或者方法体内使用
                             //     无var关键字，隐式推导变量类型
const constant = "A constant"// (5) 常量声明并初始化 不能简写
const (                      // (6) ①iota的值从0开始，用于常量的数值递增
    _ = iota                 // 0   ②通过 = 定义表达式
    a                        // 1   ③默认继承上方表达式
    b                        // 2  
    c = 1 << iota            // 8   ④通过 = 重新定义表达式
    d                        // 16    继承上方表达式
)
```

```go
//#######################################################################
// 数组、切片、映射
//#######################################################################
// 1.数组
var a [10]int          // (1) 声明长度为10的int数组，数组长度是数组类型的一部分
a[3] = 42              // (2) 设置数组元素的值
i := a[3]              // (3) 读数组元素的值
var a = [2]int{1, 2}   // (4) 声明并初始化
a := [2]int{1, 2}      //     简写
a := [...]int{1, 2}    //     编译器自行推导数组长度
a := [...]int{9:9}     //     0 0 0 0 0 0 0 0 0 9  
var ptr *[10]int = &a  // (5) 指向数组的指针
x,y := 1,2
var ptrs [2]*int{&x,&y}// (6) int指针数组
                       // (7) 只能用 == 或 ！= 不能使用 < 和 >等其他

// 2.切片
// (1) 声明切片
var a []int                             // (1) 声明切片，不需要指定长度
var a = []int {1, 2, 3, 4}              // (2) 声明和初始化切片
a := []int{1, 2, 3, 4}                  // (3) 简写
chars := []string{0:"a", 2:"c", 1: "b"} // (4) ["a", "b", "c"]

// (2) 下标索引
var b = a[lo:hi]    // (1) 通过下标索引从已有的数组或切片创建新切片，下标前闭后开
var b = a[1:4]      // (2) 取切片a的下标索引从1到3的值赋值给新切片b
var b = a[:3]       // (3) :前面没有值表示起始索引是0，等同于a[0:3]
var b = a[3:]       // (4) :后面没有值表示结束索引是len(a)，等同于a[3:len(a)]

// (3) 根据数组创建slice以及Reslice
a := []byte{'a','b','c','d','e','f','g'}
sa := a[2:5]    // c d e
sb := sa[2:5]   // e f g   (1) Reslice时索引以被slice的切片为准
sb := sa[2:6]   // error   (2) 索引越界不会导致底层数组的重新分配而是引发错误
                //         (3) 索引不可以超过被slice的切片的容量cap()值
s := a[:]       //         (4) 切片s指向数组x的内存空间，s改变x也变
                //         (5) 思考：两个slice指向同一数组，s1 append超过cap
// (4) Append
a =  append(a,17,3)    // (1) 在slice尾部追加元素
c := append(a,b...)    // (2) 拼接切片a和b，组成新切片
                       // (3) 若长度未超过追加到slice的容量则返回原始slice
                       // (4) 若超过则将重新分配数组并拷贝原始数据

// (5) 使用make来创建切片
a = make([]byte, 3, 5)     // (1) 第2个参数是切片长度，第3个参数是切片容量
fmt.Println(len(a),cap(a)) // (2) 3 5 输出切片长度和容量
a = make([]byte, 5)        // (3) 第3个切片容量参数可选，即可以不传值

// (6) Copy
s1:= []int{1,2,3,4,5,6}    
s2:= []int[7,8,9}
copy(s1,s2)                // (1) 7 8 9 4 5 6 
copy(s2,s1)                // (2) 7 8 9 copy是原址修改，s1已经改变 

// 3.数组和切片上的操作
//len(a)可以用来计算数组或切片的长度，len()是Go的内置函数，不是数组或者切片的方法
// (1) 循环遍历数组或切片
for i, e := range a {
    // i是下标索引，从0开始, e是具体的元素
    // i, e 是局部变量，可通过以下方式修改数组内容

    a[i] = 1000  
}

// (2) 如果你只需要元素，不需要下标索引，可以按照下面的方式做:
for _, e := range a {
    // e是元素
}

// (3) 如果你只需要下标索引，可以按照下面的方式做
for i := range a {
}

//     Go 1.4之前, 如果range的前面不按照上面2个示例那样带上i和e，会编译报错
// (4) Go 1.4开始，可以不用带上i和e，直接for range遍历
for range time.Tick(time.Second) {
    // 每秒执行一次
}

// 4.map映射
m := make(map[string]int)   // (1) 初始化map后才能使用
m["key"] = 42               //     赋值
fmt.Println(m["key"])       //     使用
delete(m, "key")            //     删除键值对
elem, ok := m["key"] // (2) 若key存在,ok为true,elem是对应value
                     //     否则ok是false，elem是map的value的类型的零值
// (3) map字面值，声明的同时做初始化
// type Vertex struct {
//     X, Y float64
// }
var m = map[string]Vertex{
    "Bell Labs": {40.68433, -74.39967},
    "Google":    {37.42202, -122.08408},
}
// (4) 遍历map
for key, value := range m {
    m[key] = {1,2}  // key和value是局部变量，改变不影响map
}
// (5) 复杂map必须逐层初始化
m := make(map[int]map[int]string)
m[1] = make(map[int]string)
m[1][1] = "hello world"
Println(m[1][1])
```

```go
//#######################################################################
// 控制语句
//#######################################################################

// 控制语句-if
// (1) 基本语法
if x > 10 {
    return x
} else if x == 10 {
    return 10
} else {
    return -x
}
// (2) 在if条件前面可以加一条语句;通常为初始化语句;用分号隔开
if a := b + c; a < 42 {
    return a
} else {
    return a - 42
}
// (3) 在if里做类型判断
var val interface{} = "foo"
if str, ok := val.(string); ok {
    fmt.Println(str)
}

// 控制语句-for
// Go只有for，没有while和until关键字
for i := 1; i < 10; i++ {  // (1) 标准for循环
}
for ; i < 10;  {           // (2) 相当while循环的效果
}
for i < 10  {              // (3) 可以省略分号,相当while循环
}
for {                      // (4) 可以忽略条件，相当于while (true)

// 控制语句-switch
// (1) 标准格式
switch operatingSystem {
case "darwin":
    fmt.Println("Mac OS Hipster")
    // case分支里的代码执行完后会自动退出switch，默认没有fallthrough
case "linux":
    fmt.Println("Linux Geek")
default:
    // Windows, BSD, ...
    fmt.Println("Other")
}
// (2) 和if一样，switch的value之前可以添加一条赋值语句
switch os := runtime.GOOS; os {
case "darwin": ...
}
// (3) switch的case条件还可以是比较语句
number := 42
switch {
    case number < 42:
        fmt.Println("Smaller")
    case number == 42:
        fmt.Println("Equal")
    case number > 42:
        fmt.Println("Greater")
}
// (4) case分支后还可以带多个值，用逗号分隔，任意一个匹配即可
var char byte = '?'
switch char {
    case ' ', '?', '&', '=', '#', '+', '%':
        fmt.Println("Should escape")
}

// 控制语句-跳出循环
// (1) 循环里可以使用break/continue/goto来控制循环执行逻辑
// (2) break/continue/goto还可以和循环外的label一起使用,控制外层循环的执行逻辑
// (3) continue here 表示外层的for循环继续执行，继续执行时外层for循环里的i会++
here:
    for i := 0; i < 2; i++ {
        for j := 0; ; j++ {
            if j == 2 {
                continue here
                // continue可以跳出内层死循环，外层有限循环
            }
            fmt.Println(j)
        }
    }
// (4) break there 表示退出外层循环，也就是退出整个循环了
there:
    for i := 0; ; i++ {
        for j := 0; ; j++ {
            fmt.Println(j)
            if j == 2 {
                break there
                // break可以跳出外层无限循环
            }
        }
    }
// (5) goto where 表示退出外层循环，也就是退出整个循环了
    for i := 0; ; i++ {
        for j := i + 1; j < 3; j++ {
            fmt.Println(j)
            if j == 2 {
                goto where
                // goto对应的标签应该位于循环下方
            }
        }
    }
where:
```

```go
//#######################################################################
// 函数
//#######################################################################

// 函数-函数基础
// (0) 函数声明包括函数名、形式参数列表、返回值列表（可省略）以及函数体。
func name(parameter-list) (result-list) {}
// (1) 一个简单的函数
func functionName() {}
// (2) 带参数的函数，参数的类型在标识符后面
func functionName(param1 string, param2 int) {}
// (3)多个参数有相同的类型
func functionName(param1, param2 int) {}
// (4) 返回值类型声明
func functionName() int {
    return 42
}
// (5) 可以返回多个值
func returnMulti() (int, string) {
    return 42, "foobar"
}
var x, str = returnMulti()
// (6)函数返回值有标识符，可以在函数体内对返回标识符赋值
func returnMulti2() (n int, s string) {
    n = 42
    s = "foobar"
    // 只需要return即可，n和s的值会被返回
    return
}
var x, str = returnMulti2()


// 函数-函数闭包
func outer() (func() int, int) {
    outer_var := 2
    // (1) 闭包是匿名函数，闭包可以访问当前作用域可以访问到的变量
    inner := func() int {
        outer_var += 99 // 如果执行了闭包，闭包外面的outer_var的值会被修改
        return outer_var
    }
    inner()
    return inner, outer_var // outer_var的值被改变，这里返回inner函数和101
}

// 函数-参数可变的函数
func main() {
    fmt.Println(adder(1, 2, 3))     // 6
    fmt.Println(adder(9, 9))    // 18
    nums := []int{10, 20, 30}
    fmt.Println(adder(nums...))    // 60
}
// (1) 最后一个参数的类型前面加...表示函数的最后一个传参可以有0个或者多个
func adder(args ...int) int {
    total := 0
    for _, v := range args { // (2) 遍历传进来的参数, args是一个slice类型变量
        total += v
        v++  // (3) 本质是值传递，对slice的修改不会影响外部变量
    }

    return total
}

// 函数-defer
// (1) defer 行为类似析构函数，在函数体执行结束后按照调用顺序的相反顺序逐个执行
// (2) 即使函数发生严重错误也会执行
// (3) 支持匿名函数的调用
// (4) 常用于资源清理、文件关闭、解锁以及记录时间等操作
// (5) 通过与匿名函数配合可在return之后修改函数计算结果(因为最后执行)
// (6) 如果函数体内某个变量作为deferE时匿名函数的参数，则在定义defer
//     时即已经获得了拷坝，否则则是引用某个变量的地址（闭包）
// (7) Go没有异常机制，但有panic/recover模式来处理错误
// (8) Panic可以在任何地方引发，但recover只有在defer调用的函数中有效
func main() {
  defer func() {
    fmt.Println("Done")
  }()
  fmt.Println("Working...")
}
```

```go
//#######################################################################
// 5 结构体
//#######################################################################

// 1.结构体的声明、赋值及访问
// 5.1 结构体-声明
// (0) 结构体是一种类型，也是一系列字段的集合
type node struct {     // (1) 用type <Name> struct{}定义结构，遵守可见性规则
    id    int
    value string
    next  *node        // (2) 支持指向自身的指针类型成员
}
n := node{ 1, "a" }    // (3) 顺序初始化，必须包含全部字段值
                       // 错误: too few values in struct literal
n := node{             // (4) 命名初始化，不用全部字段，也无关顺序
    id   : 2,
    value: "abc",      // 注意结尾逗号 !!!
}
type nNode struct {
    int                // (5) 匿名字段(本质上是以类型名为名称的字段)
    _ string           // (6) 可用 _ 忽略字段名。
    node               // (7) 结构体的嵌套(具名结构体-匿名字段)
}
s := nNode {19, 2, node{id:1, value: "10"}}
// 如果使用外层结构体不存在的字段，会自动向内层查找
// 如果内外层有同名结构体，使用内层字段时，需要指定具体路径
type mNode struct{
    name string
    myNode node        // (8) 结构体的嵌套(具名结构体-具名字段)
}
s := mNode{name: "Name", myNode:node{id:1, value: "10"}}
                       // (9) 相同类型的成员可进行直接拷贝赋值

// 5.2 结构体-匿名结构和空结构
user := struct {         // (1) 匿名结构体通过value := struct{}{}定义使用
    id   int
    name string
}{id: 1, name: "user1"}
type Student struct {    // (2) 匿名结构体可嵌入其他类型,用作成员或定义成员变量
    Person struct {sex, name string}  // 匿名结构体-具名字段
    age, id int                       // 相同类型的声明可以用逗号分割
}
s := Student{age:18, id:0}
ss := []Student{{age:18, id:0}, {age:18, id:0}} // 初始化结构体切片
s.Person.sex = "m"                   // 匿名结构体-具名字段
s.Person.name = "Mary"               // 只能通过字段名赋值
users := make(map[int]struct{})      // 匿名结构也可以用于map的值
var a struct{}          // (3) 空结构中没有字段，常用于值可被忽略的场合;
var b [1000]struct{}    
s := b[:]               // (4) 结构自身和元素类型的长度都为零，但实体存在;
println(unsafe.Sizeof(a), unsafe.Sizeof(b))  // 0, 0
println(len(s), cap(s))                      // 1000, 1000

// 5.2 结构体-比较运算符
// (1) 支持==与！=比较运算符，但不支持>或<
// (2) 仅所有字段全部支持，才可做相等操作。

// 5.3 结构体-指针
// (1) 可用指针选择字段，但不支持多级指针。
// (2) 可以使用匿名字段指针
// (3) 允许直接通过指针来读写结构成员
// (4) 结构体的.运算符
var v = Vertex{1, 2}
var vp = &Vertex{1, 2}
Println(v1.X, v2.X)  // 不论变量是指针还是结构体.运算符具有相同的表现

// 5.4 结构体-标签
// (1) 标签（tag）不是注释，而是对字段进行描述的元数据
// (2) 不是数据成员，却是类型的组成部分。
// (3) 内存布局相同，允许显式类型转换。
type user1 struct {id int `id`}  
type user2 struct {id int `uid`}
u1 := user1{1}
u2 := user2{2}   // 类型不同
_ = u1 == u2     // mismatched types user1 and user2
u1 = user(u2)    // 内存布局相同，支持转换。
fmt.Println(u1)
```

```go
//#######################################################################
// 6 方法
//#######################################################################// 2.在结构体中定义方法
// (1) 在func关键字和方法名称之间加上结构体声明(var_name StructName)
// 调用方法时，会把结构体的值拷贝一份
func (v Vertex) Abs() float64 {
    return math.Sqrt(v.X*v.X + v.Y*v.Y)
}
// 调用结构体方法
v.Abs()

// (2) 调用方法时想改变外部结构体变量的值，方法需要使用指针接受者
// 下面的方法，每次调用add方法时就不会拷贝结构体的值
func (v *Vertex) add(n float64) {
    v.X += n
    v.Y += n
}
var v = Vertex{0,0}
v.add(10)
(*Vertex).add(&v, 10)
```

```go
//#######################################################################
// 7 接口
//#######################################################################
// (0) 接口是一个或多个方法签名的集合
type Connecter interface{    // (1) 接口只有方法声明，没有实现，没有数据字段
    Connect()
}
type USB interface{
    Name() string
    Connecter()              // (2) 接口可以匿名嵌入其它接口，或嵌入到结构中
}
type PhoneConnecter struct{  // (3) 类型拥有该接口的所有方法签名，即算实现该接口
    name string              //     无需显示声明实现哪个接口
}                            //     这称为Structural Typing
func (pc PhoneConnecter)Name() string{
    return pc.name
}
func (pc PhoneConnecter)Connect() {
    fmt.Println("Connected:"pc.name)
}
func main() {
    a := PhoneConnecter{"PhoneConnecter"}  // (4) 赋值给接口时会发生拷贝
    a.name = "NewName"      // 接口内部存储指向复制品的指针,而非结构体
    a.Connect()             // 对结构体赋值不会改变复制品的状态，也不能获取指针

    Disconnect(a)
    b := Connecter(a)       // (5) 超集的接口可以转换为子集的接口，反之失败
    b.Connect()             // 成功

    var a interface{}       // (6) 仅接口存储的类型和对象都为nil时接口才等于nil
    fmt.Println(a == nil)   // True
    var p *int = nil
    a = p
    fmt.Println(a == nil)   // False
}
func Disconnect(usbUSB){
    if pc,ok := usb.(PhoneConnecter);ok{  // (7) 判断类型方法一
        fmt.Println("Disconnected:"pc.name)
        return
    }
    fmt.Println("Unknown decive.")
}
func Disconnect(usb interface}){
    switch v:=usb.(type){                 // (8) 判断类型方法二
    case PhoneConnecter:
        fmt.Println("Disconnected:"V.name)
    default:
        fmt.Println("Unknown decive.")
    }
}
//  (9) 接口调用不会做receiver的自动转换，与struct不同
// (10) 接口同样支持匿名字段方法
// (11) 接口也可实现类似OOP中的多态
// (12) 空接口可以作为任何类型数据的容器


// 接口-空接口
// interface{} 表示空接口，可以用它引用任意类型的数据类型
// Golang给interface{}提供类型断言机制以区分此时引用的类型
func myFunc(arg interface{}) {
  value, ok := arg.(string) // 类型断言
  if !ok {
    fmt.Println("arg is not string type")
  } else {
    fmt.Println("arg is string type, value = ", value)
    fmt.Printf("value type is %T\n", value)
  }
}

// 接口-接口值得组成(具体类型、具体类型的值)
// 接口的值是由一个 具体类型 和 具体类型的值 两部分组成
var w io.Writer       // 动态类型: nil; 动态类型的值: nil
w = os.Stdout         // 动态类型: *os.File; 动态类型的值: fd int=1(stdout)
w = new(bytes.Buffer) // 动态类型: *bytes.Buffer; 动态类型的值: data []byte
w = nil               // 动态类型: nil; 动态类型的值: nil
var i interface{}     // 动态类型: nil; 动态类型的值: nil

// 接口-类型断言的本质
// 类型断言其实就是根据 pair 中的 type 获取到 value
// pair 在传递过程中不变，不管 r 还是 w，pair中的tpye始终是Book
type Reader interface {
    ReadBook()
}
type Writer interface {
    WriteBook()
}
type Book struct {} // 具体类型
func (b *Book) ReadBook() {
    fmt.Println("Read a Book")
}
func (b *Book) WriteBook() {
    fmt.Println("Write a Book")
}
func main() {
    // b: pair<type: Book, value: book{} 地址>
    b := &Book{}
    // book ---> reader
    // r: pair<type: , value: >
    var r Reader
    // r: pair<type: Book, value: book{} 地址>
    r = b
    r.ReadBook()
    // reader ---> writer
    // w: pair<type: , value: >
    var w Writer
    // w: pair<type: Book, value: book{} 地址>
    w = r.(Writer) // 此处的断言为什么成功？因为 w, r 的type是一致的
    w.WriteBook()
}
```

```go
// 反射-两种反射方式
// (1) ValueOf接口用于获取输入参数接口中的数据的值，如果接口为空则返回0
func ValueOf(i interface{}) Value {...}
// (2) TypeOf用来动态获取输入参数接口中的值的类型，如果接口为空则返回nil
func TypeOf(i interface{}) Type {...}

// 反射-获取结构体变量的方式
type User struct {
    Id   int
    Name string
    Age  int
}
func (u User) Call() {
    fmt.Println("user ius called..")
    fmt.Printf("%v\n", u)
}
func main() {
    user := User{1, "AceId", 18}
    DoFieldAndMethod(user)
}
func DoFieldAndMethod(input interface{}) {
    inputType := reflect.TypeOf(input) // 获取input的type
    fmt.Println("inputType is :", inputType.Name())
    inputValue := reflect.ValueOf(input)  // 获取input的value
    fmt.Println("inputValue is :", inputValue)
    // 通过type获取里面的字段
    // 1.获取interface的reflect.Type，通过Type得到NumField，进行遍历
    // 2.得到每个field，数据类型
    // 3.通过field有一个Interface()方法，得到对应的value
    for i := 0; i < inputType.NumField(); i++ {
        field := inputType.Field(i)
        value := inputValue.Field(i).Interface()
        fmt.Printf("%s: %v = %v\n", field.Name, field.Type, value)
    }
    // 通过type获取里面的方法，调用
    for i := 0; i < inputType.NumMethod(); i++ {
        m := inputType.Method(i)
        fmt.Printf("%s: %v\n", m.Name, m.Type)
    }
}

// 反射-结构体标签用于解析json
import (
    "encoding/json"
    "fmt"
)
type Movie struct {
    Title  string   `json:"title"`
    Year   int      `json:"year"`
    Price  int      `json:"price"`
    Actors []string `json:"actors"`
    Test   string   `json:"-"` // 忽略该值,不解析
}
func main() {
    movie := Movie{"喜剧之王", 2000, 10, []string{"xingye", "zhangbozhi"}, "hhh"}
    // 编码：结构体 -> json
    jsonStr, err := json.Marshal(movie)
    if err != nil {
        fmt.Println("json marshal error", err)
        return
    }
    fmt.Printf("jsonStr = %s\n", jsonStr)
    // 解码：jsonstr -> 结构体
    myMovie := Movie{}
    err = json.Unmarshal(jsonStr, &myMovie)
    if err != nil {
        fmt.Println("json unmarshal error", err)
        return
    }
    fmt.Printf("%v\n", myMovie)
}


// (0) 反射问大大提高程序的灵活性，使得interface{}有更大的发挥余地
type User struct
    Id int
    Name string
    Age int
}
func (u User)Hello() {
    fmt.Println("Hello world.")
}
func main() {
    u := User{1,"OK",12}
    Info(&u)
}
func Info(o interface{}){
    t := reflect.Typeof(o)          // TypeOf获取对象类型信息
    fmt.Println("Type:", t.Name())

    if k := t.Kind(); k != reflect.Struct{ // 判断传入类型是否是期望的
        fmt.Println("XX")           // Kind()方法获取对象类型
        return                      // reflect.Struct用于类型判断
    }

    v := reflect.ValueOf(o)         // ValueOf获取对象的值
    fmt.Println("Fields:")

    for i:=0; i<t.NumField(); i++{  // NumField()取得字段数量
        f := t.Field(i)             // Field()方法获取字段
        val := v.Field(i).Interface()  // Interface()取出字段的值
        fmt.Printf("%6s:%v %v\n",f.Name,f.Type,val)
    }

    for i:=0; i<t.NumMethod(); i++{ // NumMethod()取得方法数量
        m := t.Method(i)            // Method()获取方法信息
        fmt.Printf("%6s:%v\n",m.Name,m.Type)
    }
}

type User struct{
    Id int
    Name string
    Age int
}
type Manager struct{
    User
    title string
}
func main() {
    m := Manager{User:User{1,"OK",12},title:"123"}
    t :=reflect.Typeof(m)
    fmt.Printf("%#v\n",t.Field(0))     // 根据index获取匿名字段信息
    fmt.Printf("%#v\n",t.FieldByIndex([]int{0,0})) // 匿名嵌套结构体中的字段
}


// (1) 想要利用反射修改对象状态，前提是interface.data是settable,
       即pointer-interface
× := 123
v := reflect.ValueOf(&x)  // 获取对象的指针
v.Elem().SetInt(999)      // 设置对象的值
fmt.Println(x)

func main() {
    u := User{1,"0K",12}
    set(&u)
    fmt.Println(u)
}
func Set(o interface{}){
    v :reflect.Valueof(o)
    if v.Kind()=reflect.Ptr &!v.Elem().CanSet(){ 
        fmt.Println("XXX")    // 判断类型是否是指针且可修改
        return
    } else {
        v = v.Elem()
    }

    f :=v.FieldByName("Name")  // 根据字段名查找字段
    if !f.IsValid() {          // 判断字段名是否合法
        fmt.Println("BAD")
        return
    }

    if f.Kind() == reflect.String{ // 判断类型是否为string
        f.Setstring("BYEBYE")      // 设置string的值
    }
}

// 通过反射可以“动态”调用方法
type User struct{
    Id int
    Name string
    Age int
}

func (u User)Hello(name string){
    fmt.Println("Hello",name,"my name is",u.Name)
}
func main() {
    u := User{1,"0K",12}
    v := reflect.ValueOf(u)
    mv := v.MethodByName("Hello")

    args :[]reflect.Value{reflect.Valueof("joe")} // Valueof()生成值对象
                                                  // Value对象作为参数
    mv.Call(args)
}
```

```go
// 并发

// 并发-runtime.Goexit()
// runtime.Goexit()可以退出当前goroutine
func main() {
    go func() {
        defer fmt.Println("A.defer")
        func() {
            defer fmt.Println("B.defer")
            runtime.Goexit() // 退出当前goroutine
        }()
    }()
    time.Sleep(1 * time.Second) // 防止程序退出
}

// 并发-channel的使用
// Channel通过make创建，close关闭
make(chan Type) // 等价于 make(chan Type, 0)
make(chan Type, capacity)
channel <- value    // 发送value到channel
<-channel            // 接收并将其丢弃
x := <-channel        // 从channel中接收数据，并赋值给x
x, ok := <-channel    // 功能同上，同时检查通道是否已关闭或为空
// 有缓存channel特点
//   1) 当 channel 已经满，再向⾥面写数据，就会阻塞。
//   2) 当 channel 为空，从⾥面取数据也会阻塞。
func main(){
    c := make(chan bool)
    // c := make(chan bool, 1)
    go func(){
        fmt.Println("Go Go Go!!!")
        c <- true
    }()
    <-c    // 阻塞直至channel中有数据
}

// 并发-channel关闭
// (1) 关闭channel再发送数据回引发panic错误，导致接收立即返回零值
// (2) 关闭channel可以继续从channel接收数据
// (3) 对于nil channel⽆论收发都会被阻塞
func main() {
    c := make(chan int)
    go func() {
        for i := 0; i < 5; i++ {
            c <- i
        }
        close(c) // close可以关闭一个channel
    }()
    for {
        if data, ok := <-c; ok { // ok为true表示channel没有关闭
            fmt.Println(data)
        } else {
            break
        }
    }
  // (4) 可以使用range来迭代不断操作channel,效果
  //for data := range c {
  //    fmt.Println(data)
  //}
    fmt.Println("Main Finished..")
}


// 并发-channel与select
// (1) 可处理一个或多个channel的发送与接收
// (2) 同时有多个可用的channel时按随机顺序处理
// (3) 可用空的select来阻塞main函数
// (4) 可设置超时
select{
    case <- chan1:
        // 如果chanl成功读到欧据，则进行该case处理语句
    case chan2 <- 1:
        // 如果成功向chan2写入数据，则进行该case处理语句
    default:
        //如果上面都没有成功，则进入default处理流程
}
func fibonacii(c, quit chan int) {
    x, y := 1, 1
    for {
        select {
        case c <- x: // 如果c可写，则进入该case
            x, y = y, x+y
        case <-quit: // 如果quit可读，则进入该case
            fmt.Println("quit")
            return
        }
    }
}
func main() {
    c := make(chan int)
    quit := make(chan int)

    go func() { // sub go
        for i := 0; i < 6; i++ {
            fmt.Println(<-c)
        }
        quit <- 0
    }()
    fibonacii(c, quit) // main go
}
```
