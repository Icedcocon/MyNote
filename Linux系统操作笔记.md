# Linux系统操作

## 第二部分文件、目录与磁盘格式

### 第五章 Linux的文件系统与目录配置

#### 1.文件属性：

<img title="" src="file:///D:/Cache/MarkText/2022-07-19-11-09-23-image.png" alt="" width="428" data-align="center">

（1）文件类型：第一栏第一个字符，包括[d]目录、[-]文件、[l]链接文件、[b]块文件、[c]串行文件；

（2）文件权限：第一栏随后九个字符，三个一组分别表示文件拥有者（owner/user）权限、用户组（group）权限、其他人（others）权限；

（3）chgrp：修改文件所述用户组；

```bash
chgrp [-R] dirname/filename ...
-R    递归修改
```

（4）chown：修改文件所述用户组；

```bash
chown [-R] 账号名称 文件或目录
chown [-R] 账号名称:用户组名称 文件或目录
-R    递归修改
```

（5）chmod：修改权限

```bash
chown [-R] [ugoa...][[+-=][rwxXstugo...]...][,...]
chown [-R] 3位数字 文件或目录
-R    递归修改
```

#### 2.目录配置FHS

FHS：Filesystem Hierarchy Standard（文件系统层次化标准）的缩写，多数Linux版本采用这种文件组织形式。

（1）根目录

| 目录     | 应放置文件内容                                                 |
|:------ |:------------------------------------------------------- |
| /bin   | 可被root和一般账号使用的命令，在单人维护模式下能使用的命令                         |
| /boot  | Linux内核文件、启动选项及配置文件，如启动引导程序grub2                        |
| /dev   | 设备和接口，如/dev/null、/dev/zero、/dev/tty、/dev/loop*、/dev/sd* |
| /etc   | 配置文件，一般用户可看但只有root可改                                    |
| /lib   | 函数库                                                     |
| /media | 可移除媒体挂载点                                                |
| /mnt   | 临时挂载某些设备                                                |
| /opt   | 第三方软件放置位置                                               |
| /run   | 系统启动后产生的信息，位于内存中                                        |
| /sbin  | 只被root使用的命令，包括启动、修复、还原系统所需的命令                           |
| /srv   | 存放网络服务所使用的数据                                            |
| /tmp   | 临时文件                                                    |
| /usr   | UNIX Software Resource 存放系统默认软件和大部分第三方软件                |
| /var   | 缓存、日志文件等                                                |
| /home  | 用户目录，[~]当前用户目录、[~admin]admin的用户目录                       |
| /lib64 | 64位函数库                                                  |
| /root  | 系统管理员（root）的家目录                                         |

（2）/usr目录

| 目录           | 应放置文件内容                                    |
|:------------ |:------------------------------------------ |
| /usr/bin     | 可被root和一般账号使用的命令，与/bin相同                   |
| /usr/lib     | 函数库，与/lib相同                                |
| /usr/local   | 系统管理员（root）安装第三方软件                         |
| /usr/sbin    | 只被root使用的命令，与/sbin相同                       |
| /usr/share   | 只读文件和共享文件，如/usr/share/man/、/usr/share/doc/ |
| /usr/games   | 游戏文件                                       |
| /usr/include | C/C++头文件                                   |
| /usr/libexec | 不被一般用户执行的执行文件和脚本                           |
| /usr/lib64   | 64位函数库，与/lib64相同                           |
| /usr/src     | 源码存放位置，内核源码建议放在/usr/src/Linux              |

（3）/var目录

### 第六章 Linux的文件系统与目录配置

#### 1.文件系统常用命令

#### 2.文件查找

（1）which 

根据${PATH}中的路径，查找可执行文件的绝对路径

```bash
which [-a] command
-a    ：列出所有查找到的命令，而非第一个
```

（2）whereis 

根据特定路径，查找二进制文件、手册、源码等的绝对路径

```bash
whereis [-bmsu] 文件或目录名
-l    ：列出查询的目录
-b    ：找二进制文件
-m    ：找手册
-s    ：招源码
-u    ：找除三者外的文件
```

（3）locate / updatedb

updatedb：根据/etc/updatedb.conf的设置五查找系统硬盘内的文件，并更新/var/lib/mlocate内的数据库文件。

locate：依据/var/lib/mlocate内的数据库记录，找出用户所输入关键词的文件名

```bash
locate [-ir] keyword
-i    ：忽略大小写差异
-c    ：不输出文件名，仅计算找到文件的数量
-l n  ：输出n行
-S    ：输出数据库mlocate.db的信息
-r    ：接正则表达式的显示方式
```

（4）find

递归地在层次目录中处理文件

```bash
find [PATH] [option] [action]
```

### 第八章 文件与文件系统的压缩

#### 1.常见的压缩命令

（1）gzip，zcat/zmore/zless/zgrep

默认原文件被压缩后不存在，变成.gz文件

```bash
gzip [-cdtv#] 文件名
-c    ：将压缩的数据输出到终端，进而利用数据重定向处理
-d    ：解压缩
-t    ：检验压缩文件的一致性，是否损坏
-v    ：显示压缩比等信息
-#    ：#是数字，-1最快但压缩比小，-9最慢但压缩比大，默认-6
```

（2）bzip2，bzcat/bzmore/bzless/bzgrep

```bash
bzip2 [-cdkzv#] 文件名
-c    ：将压缩的数据输出到终端，进而利用数据重定向处理
-d    ：解压缩
-k    ：保留原始文件，不会删除
-z    ：压缩（默认）
-v    ：显示压缩比等信息
-#    ：#是数字，-1最快但压缩比小，-9最慢但压缩比大，默认-6
```

 （3）xz，xzcat/xzmore/xzless/xzgrep

```bash
xz [-cdtlk#] 文件名
-c    ：将压缩的数据输出到终端，进而利用数据重定向处理
-d    ：解压缩
-t    ：检验压缩文件的一致性，是否损坏
-l    ：显示压缩比等信息
-k    ：保留原始文件，不会删除
-#    ：#是数字，-1最快但压缩比小，-9最慢但压缩比大，默认-6
```

#### 2.打包命令

（1）  tar

gzip、bzip2、xz都是将文件单独压缩，tar可以把多个文件压缩成一个。

```bash
tar [-z|-j|-J] [-cv] [-f 待建立的新文件名] filename...  #打包与压缩
tar [-z|-j|-J] [-tv] [-f 既有的tar文件名]              #查看文件名
tar [-z|-j|-J] [-xv] [-f 既有的tar文件名] [-C 目录]     #解压缩
-c    ：建立打包文件，可以配合-v查看被打包的文件名
-t    ：查看被打包的文件名
-x    ：解压缩，配合-C可执行解压目录
-z    ：通过gzip进行压缩/解压缩，此时文件名最好为*.tar.gz
-j    ：通过bzip2进行压缩/解压缩，此时文件名最好为*.tar.bz2
-J    ：通过xz进行压缩/解压缩，此时文件名最好为*.tar.xz
-v    ：在压缩/解压缩过程中，将正在处理的文件名显示出来
-f filename ：要被处理的文件名
-C 目录：用在解压缩后，制定解压缩目录
-p    ：保留备份数据的原有属性与权限
-P    ：保留绝对路径
```

## 第三部分

### 第十三章 Linux的账号与用户组

### 1.账号管理

（1）useradd

```bash
useradd [-u UID] [-g 初始用户组] [-G 次要用户组] 文件名
-u    ：指定UID给这个账号，/etc/passwd第三栏
-g    ：指定初始用户组，/etc/passwd第四栏
-G    ：指定次要用户组，/etc/group
-M    ：强制，不要建立使用者家目录（系统账号默认值）
-m    ：强制，要建立使用者家目录（一般账号默认值）
-c    ：账号说明，/etc/passwd第五栏
-d    ：指定某个绝对路径为家目录，而非默认值
-r    ：建立一个系统账号，UID有限制
-s    ：登录shell，默认/bin/bash
-e    ：账号失效日期[YYYY-MM-DD]
-f    ：密码是否失效，-0立刻失效，-1不会失效
```

（2）passwd

```bash
passwd [--stdin] [账号名称]   <== 所有人均可使用
passwd [-l] [-u] [--stdin] [-S] [-n 日数] \
       [-x 日数] [-w 日数] [-i 日期] 账号<== root可使用
--stdin：通过管道输入，作为密码，常用于脚本
-l    ：Lock，使密码失效
-u    ：与l相对
-S    ：列出shadow中的大部分信息
-n    ：接天数，shadow的第4栏位，多久不可修改密码
-x    ：接天数，shadow的第5栏位，多久必须修改密码
-w    ：接天数，shadow的第6栏位，密码过期前的警告天数
-i    ：接日期，shadow的第7栏位，密码失效日期，格式YYYY-MM-DD
echo "123456" | passwd --stdin username
```

（3）chage

```bash
chage [-1dEImMW] 
-1    ：列出账号详细密码参数
-d    ：接日期，shadow的第3栏位，最近一次修改密码的日期，格式YYYY-MM-DD
-E    ：接日期，shadow的第8栏位，账号失效日期，格式YYYY-MM-DD
-I    ：接日期，shadow的第7栏位，密码失效日期，格式YYYY-MM-DD
-m    ：接天数，shadow的第4栏位，多久不可修改密码
-M    ：接天数，shadow的第5栏位，多久必须修改密码
-w    ：接天数，shadow的第6栏位，密码过期前的警告天数
```

（3）usermod

```bash
usermod [-cdegGlsuLU] username
-c    ：账号说明，/etc/passwd第五栏
-d    ：接账号家目录，/etc/passwd第六栏
-e    ：接日期，shadow的第8栏位，账号失效日期，格式YYYY-MM-DD
-f    ：接日期，shadow的第7栏位，密码失效日期，格式YYYY-MM-DD
-g    ：指定初始用户组，/etc/passwd第四栏
-G    ：指定次要用户组，/etc/group
-a    ：与-G合用，可增加次要用户组而非设置
-1    ：后面接账号名称，/etc/passwd第一栏
-s    ：设置登录shell文件
-u    ：指定UID给这个账号，/etc/passwd第三栏
-L    ：Lock，使密码失效
-U    ：与l相对
```

（4）userdel

删除用户数据：

①账号密码：/etc/passwd、/etc/shadow

②用户组：/etc/group、/etc/gshadow

②用户个人数据：/home/username、/var/spool/mail/username

如果账号只是暂时不用，可以将/etc/shadow里的账号失效日期（第八栏）设置为0。

```bash
userdel [-r] username
-r    ：连同使用者家目录一起删除
```

（5）visudo

给与普通用户sudo的权限

①单一用户使用root所有命令

```bash
root     ALL=(ALL)                ALL
用户账号  登录来源=（可切换的身份）    可执行的命令
```

②wheel用户组使用root所有命令及免密

```bash
%wheel     ALL=(ALL)                ALL
%用户组     登录来源=（可切换的身份）    可执行的命令
%wheel     ALL=(ALL)                NOPASSWD:ALL
%用户组     登录来源=（可切换的身份）    无需密码
```

## BASH脚本

### 基础

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
  
  - `su - `指令使用login shell;惠志兴以下文件：
    
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

##### bash shell特点

- 命合和文件自动补齐

- 命合历史记忆功能
  
  - `上下键`：历史命令
  
  - `!number`：执行第number条历史命令
  
  - `!string`：找到最近一个以string开头的程序
  
  - `!$`：上一个命令的最后一个参数
  
  - `!!`：执行上一个命令
  
  - `^R`：搜索历史命令

- 别名功能
  
  - `alias` ：别名
  
  - `unalias` ：取消别名 | `\COMMAND`：（跳过别名）

- 快捷键
  
  - ^R：搜索历史命令
  
  - ^D
  
  - ^A：光标移到最前
  
  - ^E：光标移到最后
  
  - ^L
  
  - ^U：光标以前全部删除
  
  - ^K：光标以后全部删除
  
  - ^S
  
  - ^Q

- 前后台作业控制
  
  - &
  
  - nohup
  
  - ^C
  
  - ^Z
  
  - bg %1
  
  - fg %1
  
  - kill %3
  
  - `screen`：可以保存上次回话

- 输入输出重定向
  
  - 0,1,2
  
  - > 
  
  - > > 
  
  - 2>
  
  - 2>>
  
  - 2>&1
  
  - &>
  
  - `cat </etc/hosts`：cat无参时返回标准输入的内容，将**标准输入重定向为文件**。
  
  - `cat <<-EOF`：将标准输入重定向为连续字符串。
  
  - `cat >file1 <<EOF`：**cat输出重定向到文件**。

- 管道

- 
