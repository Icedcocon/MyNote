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
// 数组、切片
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
```
