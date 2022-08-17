# 基础

##### bash中调用其他解释器

- 在bash中使用python

```bash
#! /bin/bash
/bin/python <<-EOF
print('Hello world!')
print('This is printd by Python.')
EOF
```

- 将代码交给cat解释器执行

```bash
#! /bin/bash
/usr/bin/cat <<-EOF
Hello world!
This is printd by cat.
EOF
```

- 在起止标记前加上“-”可以让结尾的**结束标记不必顶格书写**，即允许结束标记前有tab。

##### bash执行方式

- 在sub shell 中执行bash脚本

```bash
bash scripts.sh
./scripts.sh
```

- 在当前shell中执行
  
  - 当前shell需要使用bash中定义的环境变量时；

```bash
. scripts.sh
source scripts.sh
```

##### bash支持的shell

- 查询Linux支持的shell

```bash
$ cat /etc/shells
/bin/sh
/bin/bash
/usr/bin/sh
/usr/bin/bash
/bin/tcsh
/bin/csh
/usr/bin/tmux
```

- login shell和nonlogin shell
  
  - `su`指令使用nonlogin shell；只执行以下文件：
    
    - `/etc/bashrc`
    
    - `~/.bashrc`
  
  - `su -` 指令使用login shell;惠志兴以下文件：
    
    - `/etc/profile`
    
    - `/etc/bashrc`
    
    - `~/bash_profile`
    
    - `~/.bashrc`

```bash
# nonloin shell 
$  root
# login shell
$ su - root
```

- bash退出时会执行的文件
  
  - `~/.bash_logout`
  
  - `~/.bash_history`中的内容会更新

##### 查询bind软件包的配置文件

```bash
$ rpm -qc COMMAND
```

### bash shell特点

##### 1.命合和文件自动补齐

##### 2.命合历史记忆功能

- `上下键`：历史命令

- `!number`：执行第number条历史命令

- `!string`：找到最近一个以string开头的程序

- `!$`：上一个命令的最后一个参数

- `!!`：执行上一个命令

- `^R`：搜索历史命令

##### 3.别名功能

- `alias` ：别名

- `unalias` ：取消别名 | `\COMMAND`：（跳过别名）

##### 4.快捷键

- ^R：搜索历史命令

- ^D

- ^A：光标移到最前

- ^E：光标移到最后

- ^L

- ^U：光标以前全部删除

- ^K：光标以后全部删除

- ^S

- ^Q

##### 5.前后台作业控制

- &

- nohup

- ^C

- ^Z

- bg %1

- fg %1

- kill %3

- `screen`：可以保存上次回话

##### 6.输入输出重定向

- 0,1,2
- 2>
- 2>>
- 2>&1
- &>
- `cat </etc/hosts`：cat无参时返回标准输入的内容，将**标准输入重定向为文件**。
- `cat <<-EOF`：将标准输入重定向为连续字符串。
- `cat >file1 <<EOF`：**cat输出重定向到文件**。

##### 7.管道 | tee

- 一个命令的输出作为另一个命令的输入

```bash
ip addr | grep 'inet' | grep etho
ip addr | grep 'inet' | tee test | grep etho         # 覆盖
ip addr | grep 'inet' | tee-a test | grep etho-a     # 追加
df | grep '/s'
df | tee df.txt Igrep '/s'
```

##### 8.命令排序

- `;`：不具备逻辑判断

- `&& || `：具备逻辑判断

```bash
ping www.baidu.com && echo success! || echo failure!
```

##### 9.通配符

- `*`：匹配任意多个字符`ls in*`

- `?`：匹配任意一个字符`ll ?ve`

- `[]`：匹配括号中任意-个字符`[abc][a-z][0-9][a-zA-Z0-9][a-zA-Z0-9] l[io]ve l[^a-z]vel`

- `()`：**在子shell中执行**`(cd /boot;ls) (umask077; touch file1000)`

- `{}`：**集合**`touch file{1..9}; mkdir dir{1,2,3}`

```bash
$ cp -rv /etc/sysconfig/network-scripts/ifcfg-eth0/etc/sysconfig/network-scripts/ifcfg-eth0.old
$ cp -rv /etc/sysconfig/network-scripts/{ifcfg-eth0,ifcfg-eth0.old}
$ cp -rv /etc/sysconfig/network-scripts/ifcfg-eth0{,.old}
```

# 变量

```bash
#!/usr/bin/bash
read -p "Please input a ip:" ip # read可以从外界读入变量的值
ping -c1 sip &>/dev/nullI
if $-eq 0 ]then
    echo "sip is up."
else
    echo "sip is down."
fi
```

### 3.位置变量

`$0` ：脚本名称

`$1 $2 $3 ... $9 ${10}`：对应位置的参数

### 4.预定义变量

| 参数处理 | 说明                                                                 |
| ---- | ------------------------------------------------------------------ |
| `$#` | 传递到脚本的参数个数                                                         |
| `$*` | 以一个单字符串显示所有向脚本传递的参数。如"∗"用「"」括起来的情况、以"1 2…n"的形式输出所有参数。              |
| `$$` | 脚本运行的当前进程ID号                                                       |
| `$!` | 后台运行的最后一个进程的ID号                                                    |
| `$@` | 与∗相同，但是使用时加引号，并在引号中返回每个参数。如"@"用「"」括起来的情况、以"1""2" … "$n" 的形式输出所有参数。 |
| `$-` | 显示Shell使用的当前选项，与set命令功能相同。                                         |
| `$?` | 显示最后命令的退出状态。0表示没有错误，其他任何值表明有错误。                                    |

##### 命令替换

```bash
# piao和$()中的命令会被shell先执行，并将结果返回
MYDATE=`date +%F`
MYDATE=$(date +%F)
```

# 运算

### 整数运算

- `expr`

- `$(( C风格计算 ))`

- `$[]`

- `let "z=10**3"; echo $z`

# 参数替换

##### 1.`${parameter}`

- 和`$parameter`是相同的，都是表示变量parameter的值

- 可以把变量和字符串连接。

```shell
your_id=${USER}-on-${HOSTNAME}

PATH=${PATH}:/opt/bin 
#在脚本的生存期内，能额外增加路径/opt/bin到环境变量$PATH中去 
```

##### 2.`${parameter-default} ${parameter:-default}`（不修改变量）

- 如果变量没有被设置，**使用默认值**。

- 当参数被声明但没赋值，`${parameter-default}`返回NULL，`${parameter:-default}`返回default。

```shell
TMP_FRY=
echo ${TMP_FRY-"This is NULL."}     # NULL
echo $TMP_FRY                       # NULL.
echo ${TMP_FRY:-"This is NULL."}    # This is NULL.
echo $TMP_FRY                       # NULL.
# 如果变量$TMP_FRY还没有被设置，则把命令`whoami`的结果赋给该变量
```

##### 3.`${parameter=default} ${parameter:=default}`（修改变量）

- 如果变量parameter没有设置，把它**设置成默认值**。

- 当参数被声明但值为NULL时，`${parameter=default}`返回NULL并对变量赋值，`${parameter:=default}`返回default并对变量赋值。

```shell
TMP_FRY=
echo ${TMP_FRY="This is NULL."}     # NULL
echo $TMP_FRY                       # This is NULL.
TMP_FRY=
echo ${TMP_FRY:="This is NULL."}    # This is NULL.
echo $TMP_FRY                       # This is NULL.
# 如果变量$TMP_FRY还没有被设置，则把命令`whoami`的结果赋给该变量
```

##### 4.`${parameter+append} ${parameter:+append}`（不修改变量）

- 在变量后附加字符串，但不修改变量

##### 5.`${parameter:?err_msg} ${parameter:?err_msg}`

- 如果变量parameter已经设置，则使用该值，否则打印err_msg错误信息。

##### 6.`${#var}`

- 打印`$var`的字符个数

##### 7.`${var#pattern} ${var##pattern}`

- `${var#pattern}`删除从`$var`前端开始的最短匹配`$Pattern`的字符串。

- `${var##pattern}`删除从`$var`前端开始的最长匹配`$Pattern`的字符串。

- 可以与通配符`*`配和使用

##### 8.`${var%pattern} ${var%%pattern}`

- `${var%pattern}`删除从`$var`后端开始的最短匹配`$Pattern`的字符串。

- `${var%%pattern}`删除从`$var`后端开始的最长匹配`$Pattern`的字符串。

- 可以与通配符`*`配和使用

##### 9.索引及切片`${var:start:end}`

# 测试

### 格式

- 格式1:  `test 条件表达式`

- 格式2：`[条件表达式]`

- 格式3：`[[条件表达式]]`

### 测试结构

一个if/then结构能包含嵌套的比较和测试。

```shell
echo "Testing \"false\""
if [ "false" ]              #  "false"是一个字符串.
then
  echo "\"false\" is true." #+ 它被测试为真.
else
  echo "\"false\" is false."
fi            # "false"为真.
```

### 文件测试操作符

如果下面的条件成立返回真

| 操作符       | 描述                                  |
| --------- | ----------------------------------- |
| -e        | 文件存在                                |
| -a        | 文件存在，这个和-e的作用一样. 它是不赞成使用的，所以它的用处不大。 |
| -f        | 文件是一个普通文件(不是一个目录或是一个设备文件)           |
| -s        | 文件大小不为零                             |
| -d        | 文件是一个目录                             |
| -b        | 文件是一个块设备(软盘，光驱，等等。)                 |
| -c        | 文件是一个字符设备(键盘，调制解调器，声卡，等等。)          |
| -p        | 文件是一个管道                             |
| -h        | 文件是一个符号链接                           |
| -L        | 文件是一个符号链接                           |
| -S        | 文件是一个socket                         |
| -t        | 文件(描述符)与一个终端设备相关。                   |
| -r        | 文件是否可读 (指运行这个测试命令的用户的读权限)           |
| -w        | 文件是否可写 (指运行这个测试命令的用户的读权限)           |
| -x        | 文件是否可执行 (指运行这个测试命令的用户的读权限)          |
| -g        | 文件或目录的设置-组-ID(sgid)标记被设置。           |
| -u        | 文件的设置-用户-ID(suid)标志被设置              |
| -k        | 粘住位设置                               |
| -N        | 文件最后一次读后被修改                         |
| f1 -nt f2 | 文件f1比f2新                            |
| f1 -ot f2 | 文件f1比f2旧                            |
| f1 -ef f2 | 文件f1和f2 是相同文件的硬链接                   |
| !         | "非" -- 反转上面所有测试的结果(如果没有给出条件则返回真)。   |

**注意⚠️**

1. `-t` 这个测试选项可以用于检查脚本中是否标准输入 ([ -t 0 ])或标准输出([ -t 1 ])是一个终端。
2. `-g` 如果一个目录的sgid标志被设置，在这个目录下创建的文件都属于拥有此目录的用户组，而不必是创建文件的用户所属的组。这个特性对在一个工作组里的同享目录很有用处。

### 比较操作符

二元比较操作符比较两个变量或是数值。注意整数和字符串比较的分别。

##### 整数比较

| 比较操作符 | 描述             | 例子                     |
| ----- | -------------- | ---------------------- |
| `-eq` | 等于             | `if [ "$a" -eq "$b" ]` |
| `-ne` | 不等于            | `if [ "$a" -ne "$b" ]` |
| `-gt` | 大于             | `if [ "$a" -gt "$b" ]` |
| `-ge` | 大于等于           | `if [ "$a" -ge "$b" ]` |
| `-lt` | 小于             | `if [ "$a" -lt "$b" ]` |
| `-le` | 小于等于           | `if [ "$a" -le "$b" ]` |
| `<`   | 小于(在双括号里使用)    | `(("$a" < "$b"))`      |
| `<=`  | 小于等于 (在双括号里使用) | `(("$a" <= "$b"))`     |
| `>`   | 大于 (在双括号里使用)   | `(("$a" > "$b"))`      |
| `>=`  | 大于等于(在双括号里使用)  | `(("$a" >= "$b"))`     |

##### 字符串比较

| 比较操作符 | 描述                                    | 例子                                           |
| ----- | ------------------------------------- | -------------------------------------------- |
| =     | 等于                                    | `if [ "$a" = "$b" ]`                         |
| ==    | 等于，它和=是同义词。                           | `if [ "$a" == "$b" ]`                        |
| !=    | 不相等，操作符在[[ ... ]]结构里使用模式匹配.           | `if [ "$a" != "$b" ]`                        |
| <     | 小于，依照ASCII字符排列顺序，注意"<"字符在[ ] 结构里需要转义  | `if [[ "$a" < "$b" ]]` `if [ "$a" \< "$b" ]` |
| >     | 大于，依照ASCII字符排列顺序，注意">"字符在[ ] 结构里需要转义. | `if [[ "$a" > "$b" ]]` `if [ "$a" \> "$b" ]` |
| -z    | 字符串为"null"，即是指字符串长度为零。                | -                                            |
| -n    | 字符串不为"null"，即长度不为零。                   | -                                            |

##### 混合比较

| 比较操作符 | 描述                                       | 例子                          |
| ----- | ---------------------------------------- | --------------------------- |
| -a    | 逻辑与，如果exp1和exp2都为真，则exp1 -a exp2返回真。     | `if [ "$exp1" -a "$exp2" ]` |
| -o    | 逻辑或，只要exp1和exp2任何一个为真，则exp1 -o exp2 返回真。 | `if [ "$exp1" -o "$exp2" ]` |

在一个混合测试中，把一个字符串变量引号引起来可能还不够。如果`$string`变量是空的话，表达式`[ -n "string" -o "a" = "$b" ]`

在一些Bash版本中可能会引起错误。安全的办法是附加一个外部的字符串给可能有空字符串变量比较的所有变量，`[ "x$string" != x -o "x$a" = "x$b" ]` (x字符可以互相抵消)

# case/select

case/select依靠在代码块的顶部或底部的条件判断来决定程序的分支。

### case

case它允许通过判断来选择代码块中多条路径中的一条。它的作用和多个if/then/else语句相同，是它们的简化结构，特别适用于创建目录。

> ```shell
> case "$variable" in
>      "$condition1" )
>      command...     ;;
>      "$condition2" )
>      command...     ;; 
>      *)
>      other... ;;  
> esac  
> ```

- 对变量使用`""`并不是强制的，因为不会发生单词分离。
- 每句测试行，都以右小括号`)`结尾。
- 每个条件块都以两个分号结尾`;;`。
- case块的结束以esac(case的反向拼写)结尾。





```bash

```


