### 1 expect 工具介绍

- expect 工具是一个根据脚本与其他交互式程序进行交互。

- 解释型语言提供分支和高级控制结构引导对话，并可以指定控制权交给用户的时机。

- expect能控制和处理输入、输出流，在需要填写数据等需要交互的地方实现自动化处。

### 2 expect 常用指令：

- (1) `spawn cmd`：进入expect环境后的内部命令，开始执行需要交互的指令或程序

- (2) `set timeout`：set可设置变量，此处设置超时时间，单位s， -1 表示永不超时，

- (3) `expect {'str'}`：判断命令输出是否匹配字符串
  
  - 没有立即返回，否则等待一段时间（timeout）返回，与send配合可执行交互动作

- (4) `send 'str'`：执行交互动作，向进程发送字符串（换行符确认结束）

- (5) `interact`：执行完成保持交互状态，控制权交给终端，否则交互完成直接退出
  
  - 若交互程序退出，则使用interact会报错：`expect spawn id exp6 not open`

- (6) `exp_continue`：表示循环式匹配
  
  - 默认匹配后都会退出语句，但exp_continue可使同一字符串循环多次匹配

- (7) `send_user`：打印字符串到标准输出，类似echo

- (8) `exit`：退出expect脚本

- (9) `eof`：expect执行结束 退出

- (10) `set`：定义变量

- (11) `puts`：向标准输出输出内容，如变量

### 3 语法：

##### 3.1 设置变量与开始交互

```bash
#!/usr/bin/expect           
# expect的解析器，与shell中的#!/bin/bash类似

set timeout n               # 设置超时时间n秒，每个expect允许等待n秒钟，后退出。
set name "12345"            # set设置变量，name的值为123456

spawn command1 command2..   # 执行命令，也可以将变量作为命令输入      
```

##### 3.2 expect与分支匹配

```bash
# 单分支匹配（执行一次，匹配成功执行cmd，否则退出）
expect "pat" {send "cmd\n"}
# 分支选择（执行一次，任意pat匹配成功执行对应cmd，否则退出）
expect {
    "pat1" {send "cmd1\n"}
    "pat2" {send "cmd2\n"}
    "pat3" {send "cmd3\n"}
}
expect "pat1" {send "cmd1\n"} "pat2" {send "cmd2\n"} ...
# 循环匹配（若匹配成功，则等待终端给出反馈后再次匹配，直至失败退出）
expect {                             
  "pat" {send "cmd\r"; exp_continue} # 
}
# 分支循环匹配（若任意pat匹配成功，则等待终端给出反馈后再次匹配，直至失败退出）
expect {
    "pat1" {send "cmd1\n"; exp_continue}
    "pat2" {send "cmd2\n"; exp_continue}
    "pat3" {send "cmd3\n"; exp_continue}
}
```

##### 3.3 结束

```bash
# 保持交互
interact 
# 退出expect脚本
exit 
# 结束交互
expect eof  
```

##### 3.4 传参

```bash
#!/usr/bin/expect
set uname [lindex $argv 0]
set pwd [lindex $argv 1]
puts "$argc"
spawn ssh ${uname}@127.0.0.1
expect "*password:"

send "${pwd}\r"
expect "#"

send "exit \r"
expect eof
```

##### 3.5 增量

```bash
puts "------incr-------"
set x 10
puts "$x"
incr x 5
puts "$x"
```

##### 3.6 []运算符

```bash
puts [lindex $argv 1]    # 访问数组
puts [expr $x + 5]       # 数学运算
set ss "aa,bb,cc,dd"
puts [split $ss ","]     # 字符串分割
```

##### 3.7 数组

```bash
set j "a b c d"        # 数组定义
puts "[lindex $j 2]"   # 数组访问
foreach jj $j {        # 数组遍历
    puts "$jj"
}
```

##### 3.8 循环

```bash
puts "------递增-----"
for {set i 0} { $i < 5 } { incr i } {
    puts "$i"
}
puts "------递减-----"
for {set k 5} { $k > 0 } { incr k -1 } {
    puts "$k"
}
puts "------while递增-----"
set m 0
while {$m < 5} {
    puts "$m"
    incr m 2
}
puts "------遍历argv--------"
foreach arg $argv {
    puts "$arg"
}
```

##### 3.9 bash中调用expect

```bash
#!/bin/bash
$ip=10.1.1.15
$user=root
$pass=toor

/usr/bin/expect <<-EOF
set timeout 20
spawn ssh $user@$IP
expect {
 "yes/no" { send "yes\r"; exp_continue }
 "password"  { send "$pass\r" }
}
expect "]#"
send "touch file{1..10}"

EOF
```

### expect 启用选项：

| 选项       | 含义                                                              |
| -------- | --------------------------------------------------------------- |
| **-c**   | 执行脚本前先执行的命令，可多次使用                                               |
| **-d**   | debug模式，可以在运行时输出一些诊断信息，与在脚本开始处使用exp_internal 1相似。               |
| **-D**   | 启用交换调式器,可设一整数参数。                                                |
| **-f**   | 从文件读取命令，仅用于使用#!时。如果文件名为"-"，则从stdin读取(使用"./-"从文件名为-的文件读取)。       |
| **-i**   | 交互式输入命令，使用"exit"或"EOF"退出输入状态                                    |
| **`--`** | 标示选项结束(如果你需要传递与expect选项相似的参数给脚本时)，可放到#!行:`#!/usr/bin/expect --` |
| **-v**   | 显示expect版本信息                                                    |
