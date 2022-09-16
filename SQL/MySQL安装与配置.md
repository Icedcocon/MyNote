# MySQL快速启动

## 快速启动一个 MySQL 服务器实例

- 首先，通过通过 [docker](https://hub.docker.com/_/mysql) 镜像，或者 [MySQL](https://hub.docker.com/r/mysql/mysql-server) 官方镜像，进行快速启动一个实例。

```shell
# Docker 官方镜像
$ docker image pull library/mysql:8.0.18
# MySQL 官方镜像
$ docker image pull mysql/mysql-server:8.0.18
```

然后运行这个 image 文件。

```shell
# Docker 官方镜像
$ docker run --name fryMySQL \
  -p 3308:3306 \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -v /etc/localtime:/etc/localtime:ro \
  --rm \
  -d mysql:8.0.18 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
# MySQL 官方镜像
$ docker run -d --name mysqlname mysql/mysql-server:8.0.18 --character-set-server=utf8mb4 --collation-server=utf8mb4_col
```

上面命令的各个参数含义如下：

- `--name fryMySQL` 指定镜像实例的名称，不能与当前已创建实例重复
- `-p 3308:3306` 容器 MySQL 默认端口 `3306` 射到本机的 `3308` 端口。
- `-d` 在后台运行容器，并打印容器ID。
- `--rm` 停止运行后，自动删除容器文件。
- `-e MYSQL_ROOT_PASSWORD=123456` 设置环境变量 `MYSQL_ROOT_PASSWORD` 值为 `my123456` 来设置 `root` 密码，[更多环境变量参考](https://dev.mysql.com/doc/refman/8.0/en/environment-variables.html)。
- `--character-set-server=utf8mb4 --collation-server=utf8mb4_col` 该命令以默认字符集 `utf8mb4` 和数据库默认排序规则 `utf8mb4` 启动 `MySQL` 服务，可以将许多配置选项作为标志传递给 mysqld。这将使您可以灵活地自定义容器，而无需 `cnf` 配置文件，配置 `MySQL Server` 的另一种方法是准备一个配置文件，并将其安装在容器内服务器配置文件的位置。有关详细信息，请参见[持久数据和配置更改](https://dev.mysql.com/doc/refman/8.0/en/docker-mysql-more-topics.html#docker-persisting-data-configuration)。
- `-v /etc/localtime:/etc/localtime:ro` 是让容器的时钟与宿主机时钟同步，避免时区的问题，`ro` 是 `read only` 的意思，就是只读。

可以通过 `容器id`/`容器名称` 查看 MySQL 日志

```shell
$ docker logs mysqlname
```

## 通过命令行访问 MySQL 容器

可以通过[容器名字]或者[容器 ID]进入 MySQL 容器

```shell
$ docker exec -it mysqlname bash
```

## 使用 MySQL 自定义配置文件

MySQL 的默认配置可以在 `/etc/mysql/my.cnf` 中找到，该目录可以包含附加目录，例如 `/etc/mysql/conf.d` 或 `/etc/mysql/mysql.conf.d`。 请检查 MySQL 镜像本身中的相关文件和目录，以获取更多详细信息。

如果 `/my/custom/config-file.cnf` 是自定义配置文件的路径和名称，则可以像这样启动 MySQL 容器（请注意，此命令仅使用自定义配置文件的目录路径）：

```shell
$ docker run --name fryMySQL \
  --rm \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -v /my/custom:/etc/mysql/conf.d \
  -v /etc/localtime:/etc/localtime:ro \
  -d mysql:8.0.18 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

上面命令将启动一个新的容器 `fryMySQL`，其中 MySQL 实例使用 `/etc/mysql/my.cnf` 和 `/etc/mysql/conf.d/config-file.cnf` 中的组合启动设置，其中后者的设置优先。

配置修改，可以通过【容器名字】或者【容器 ID】来重启 MySQL，可让配置生效。

```shell
docker restart mysqlname
```

# MySQL 配置修改

安装完了之后更改配置的需求比较少，所以根据实际使用过程中来修改 MySQL 配置参数，MySQL提供了两个更改配置的方式。

- 在windows上面有个配置工具(MySQL server instance config) 提供了自动配置服务。
- 另一种是手工修改配置文件来修改。

## MySQL安装目录说明

MySQL 不同的版本安装目录会有一点差异，安装目录在`/usr/local/mysql`目录下。

| 目录             | 目录内容                         |
| -------------- | ---------------------------- |
| bin/           | 客户端程序和mysqld服务器，相关命令         |
| data/          |                              |
| docs/          |                              |
| include/       | 包含头文件                        |
| lib/           | 库                            |
| man/           |                              |
| share/         |                              |
| support-files/ | 存在一些默认配置文件，如`my-default.cnf` |

## 配置文件的位置

从命令行终端运行此命令，将在寻找Linux/BSD / OS X系统中的MySQL配置文件 my.cnf 文件：

```shell
mysql --help | grep 'Default options' -A 1
```

上面命令执行后，会有这样的输出：

```shell
Default options are read from the following files in the given order:/etc/my.cnf /etc/mysql/my.cnf /usr/local/etc/my.cnf ~/.my.cnf
```

如果不存在，可以从这个地方复制一份过去 `/usr/local/mysql/support-files/my-default.cnf` 找到一个 `.cnf` 后缀结尾的文件并复制到`/etc/`目录下并重新命名为 `my.cnf`。

## Linux系统配置文件读取

| 文件名字                | 作用                                     |
| ------------------- | -------------------------------------- |
| /etc/my.cnf         | 全局配置（CentOS）                           |
| /etc/mysql/my.cnf   | 全局配置（Ubuntu）                           |
| SYSCONFDIR/my.cnf   | 全局配置（无）                                |
| $MYSQL_HOME/my.cnf  | Server-specific 服务器特定的选项 (仅适用于服务端)     |
| defaults-extra-file | 如果有的话指定该文件`--defaults-extra-file=文件名字` |
| ~/.my.cnf           | Server-specific 服务器特定的选项               |
| ~/.mylogin.cnf      | User-specific 登录路径选择 （仅适用于客户端）         |

- **\$HOME** 上表中表示用户的主目录，即用户的根目录。
- **SYSCONFDIR** 代表指定的目录与SYSCONFDIR配置文件的安装路径，默认情况这个是位于安装目录里面的目录。
- \$MYSQL_HOME 是包含在该服务器的具体my.cnf文件所在的目录的路径环境变量。如果 \$MYSQL_HOME 没有设置，你启动服务器使用mysqld_safe程序，mysqld_safe试图设置 \$MYSQL_HOME

## 配置文件内容

```shell
# 以下选项会被MySQL客户端应用读取。
# 注意只有MySQL附带的客户端应用程序保证可以读取这段内容。
# 如果你想你自己的MySQL应用程序获取这些值。
# 需要在MySQL客户端库初始化的时候指定这些选项。

# mysqld程序
[mysqld]

# ★★★这里很重要️能让MySQL登陆链接变快速
skip-name-resolve

# 使用给定目录作为根目录(安装目录)。
# basedir = .....
# 从给定目录读取数据库文件。
datadir=/var/lib/mysql
# 为mysqld程序指定一个存放进程ID的文件(仅适用于UNIX/Linux系统);
# pid-file = .....
# 指定MsSQL侦听的端口
# port = .....
# server_id = .....
# 为MySQL客户程序与服务器之间的本地通信指定一个套接字文件(Linux下默认是/var/lib/mysql/mysql.sock文件)
# socket = .....
# 设置
character-set-server=utf8

# back_log 是操作系统在监听队列中所能保持的连接数,
# 队列保存了在 MySQL 连接管理器线程处理之前的连接.
# 如果你有非常高的连接率并且出现 “connection refused” 报错,
# 你就应该增加此处的值.
# 检查你的操作系统文档来获取这个变量的最大值.
# 如果将back_log设定到比你操作系统限制更高的值，将会没有效果
# 试图设定back_log高于你的操作系统的限制将是无效的。默认值为50。
# 对于Linux系统推荐设置为小于512的整数。
back_log = 300

# 不在 TCP/IP 端口上进行监听.
# 如果所有的进程都是在同一台服务器连接到本地的 mysqld,
# 这样设置将是增强安全的方法
# 所有 mysqld 的连接都是通过 Unix Sockets 或者命名管道进行的.
# 注意在 Windows下如果没有打开命名管道选项而只是用此项
# (通过 “enable-named-pipe” 选项) 将会导致 MySQL 服务没有任何作用!
#skip-networking

# MySQL 服务所允许的同时会话数的上限
# 其中一个连接将被 SUPER 权限保留作为管理员登录.
# 即便已经达到了连接数的上限.
max_connections = 3000

# 每个客户端连接最大的错误允许数量,如果达到了此限制.
# 这个客户端将会被 MySQL 服务阻止直到执行了 “FLUSH HOSTS” 或者服务重启
# 非法的密码以及其他在链接时的错误会增加此值.
# 查看 “Aborted_connects” 状态来获取全局计数器.
max_connect_errors = 50

# 所有线程所打开表的数量.
# 增加此值就增加了 mysqld 所需要的文件描述符的数量
# 这样你需要确认在 [mysqld_safe] 中 “open-files-limit” 变量设置打开文件数量允许至少等于 table_cache 的值
table_open_cache = 4096

# 允许外部文件级别的锁. 打开文件锁会对性能造成负面影响
# 所以只有在你在同样的文件上运行多个数据库实例时才使用此选项(注意仍会有其他约束!)
# 或者你在文件层面上使用了其他一些软件依赖来锁定 MyISAM 表
#external-locking

# 服务所能处理的请求包的最大大小以及服务所能处理的最大的请求大小(当与大的 BLOB 字段一起工作时相当必要)
# 每个连接独立的大小，大小动态增加
max_allowed_packet = 32M

# 在一个事务中 binlog 为了记录 SQL 状态所持有的 cache 大小
# 如果你经常使用大的,多声明的事务,你可以增加此值来获取更大的性能.
# 所有从事务来的状态都将被缓冲在 binlog 缓冲中然后在提交后一次性写入到 binlog 中
# 如果事务比此值大, 会使用磁盘上的临时文件来替代.
# 此缓冲在每个连接的事务第一次更新状态时被创建
binlog_cache_size = 4M

# 独立的内存表所允许的最大容量。
# 此选项为了防止意外创建一个超大的内存表导致永尽所有的内存资源。
max_heap_table_size = 128M

# 随机读取数据缓冲区使用内存(read_rnd_buffer_size)：和顺序读取相对应，
# 当 MySQL 进行非顺序读取（随机读取）数据块的时候，会利用>这个缓冲区暂存读取的数据
# 如根据索引信息读取表数据，根据排序后的结果集与表进行 Join 等等
# 总的来说，就是当数据块的读取需要满足>一定的顺序的情况下，MySQL 就需要产生随机读取，进而使用到 read_rnd_buffer_size 参数所设置的内存缓冲区
read_rnd_buffer_size = 16M

# 排序缓冲被用来处理类似 ORDER BY 以及 GROUP BY 队列所引起的排序
# 如果排序后的数据无法放入排序缓冲,一个用来替代的基于磁盘的合并分类会被使用
# 查看 “Sort_merge_passes” 状态变量。
# 在排序发生时由每个线程分配
# 每个需要进行排序的线程分配该大小的一个缓冲区。增加这值加速ORDER BY或GROUP BY操作。
# 注意：该参数对应的分配内存是每连接独占！如果有100个连接，那么实际分配的总共排序缓冲区大小为100×6=600MB
sort_buffer_size = 16M

# 此缓冲被使用来优化全联合(FULL JOINS 不带索引的联合)。
# 类似的联合在极大多数情况下有非常糟糕的性能表现,但是将此值设大能够减轻性能影响。
# 通过 “Select_full_join” 状态变量查看全联合的数量
# 当全联合发生时,在每个线程中分配
join_buffer_size = 16M

# 缓存可重用的线程数
# thread_cache = 8

# 避免MySQL的外部锁定，减少出错几率增强稳定性。
# skip-locking                 

# 我们在 cache 中保留多少线程用于重用
# 当一个客户端断开连接后,如果 cache 中的线程还少于 thread_cache_size,则客户端线程被放入cache 中。
# 这可以在你需要大量新连接的时候极大的减少线程创建的开销
# (一般来说如果你有好的线程模型的话,这不会有明显的性能提升。)
thread_cache_size = 16

# 此允许应用程序给予线程系统一个提示在同一时间给予渴望被运行的线程的数量。
# 此值只对于支持 thread_concurrency() 函数的系统有意义( 例如Sun Solaris)。
# 你可可以尝试使用 [CPU数量]*(2..4) 来作为 thread_concurrency 的值
#****(此属性对当前环境无效)****
# thread_concurrency = 8

# 查询缓冲常被用来缓冲 SELECT 的结果并且在下一次同样查询的时候不再执行直接返回结果。
# 打开查询缓冲可以极大的提高服务器速度, 如果你有大量的相同的查询并且很少修改表。
# 查看 “Qcache_lowmem_prunes” 状态变量来检查是否当前值对于你的负载来说是否足够高。
# 注意: 在你表经常变化的情况下或者如果你的查询原文每次都不同,
# 查询缓冲也许引起性能下降而不是性能提升。
query_cache_size = 128M

# 只有小于此设定值的结果才会被缓冲
# 此设置用来保护查询缓冲,防止一个极大的结果集将其他所有的查询结果都覆盖。
query_cache_limit = 4M

# 被全文检索索引的最小的字长。
# 你也许希望减少它，如果你需要搜索更短字的时候。
# 注意在你修改此值之后，你需要重建你的 FULLTEXT 索引
ft_min_word_len = 8

# 如果你的系统支持 memlock() 函数，你也许希望打开此选项用以让运行中的 mysql 在在内存高度紧张的时候，数据在内存中保持锁定并且防止可能被 swapping out
# 此选项对于性能有益
#memlock

# 当创建新表时作为默认使用的表类型，
# 如果在创建表示没有特别执行表类型，将会使用此值
#****(此属性对当前环境无效)****
#default_table_type = InnoDB

# 线程使用的堆大小. 此容量的内存在每次连接时被预留.
# MySQL 本身常不会需要超过 64K 的内存
# 如果你使用你自己的需要大量堆的 UDF 函数或者你的操作系统对于某些操作需要更多的堆，你也许需要将其设置的更高一点.
thread_stack = 512K

# 设定默认的事务隔离级别.可用的级别如下:
# READ-UNCOMMITTED， READ-COMMITTED， REPEATABLE-READ， SERIALIZABLE
transaction_isolation = REPEATABLE-READ

# 内部(内存中)临时表的最大大小
# 如果一个表增长到比此值更大，将会自动转换为基于磁盘的表。
# 此限制是针对单个表的，而不是总和。
tmp_table_size = 128M

# 打开二进制日志功能。
# 在复制(replication)配置中，作为 MASTER 主服务器必须打开此项
# 如果你需要从你最后的备份中做基于时间点的恢复，你也同样需要二进制日志。
log-bin=mysql-bin

# 如果你在使用链式从服务器结构的复制模式 (A->B->C)，
# 你需要在服务器B上打开此项。
# 此选项打开在从线程上重做过的更新的日志， 并将其写入从服务器的二进制日志。
#log_slave_updates

# 打开全查询日志。 所有的由服务器接收到的查询 (甚至对于一个错误语法的查询)
# 都会被记录下来。 这对于调试非常有用， 在生产环境中常常关闭此项。
#log

# 将警告打印输出到错误 log 文件。 如果你对于 MySQL 有任何问题
# 你应该打开警告 log 并且仔细审查错误日志，查出可能的原因。
#log_warnings

# 记录慢速查询。 慢速查询是指消耗了比 “long_query_time” 定义的更多时间的查询。
# 如果 log_long_format 被打开，那些没有使用索引的查询也会被记录。
# 如果你经常增加新查询到已有的系统内的话。 一般来说这是一个好主意，
#log_slow_queries

# 有的使用了比这个时间(以秒为单位)更多的查询会被认为是慢速查询。
# 不要在这里使用“1″, 否则会导致所有的查询,甚至非常快的查询页被记录下来(由于 MySQL 目前时间的精确度只能达到秒的级别)。
long_query_time = 6

# 在慢速日志中记录更多的信息。
# 一般此项最好打开。
# 打开此项会记录使得那些没有使用索引的查询也被作为到慢速查询附加到慢速日志里
#log_long_format

# 此目录被MySQL用来保存临时文件。例如,
# 它被用来处理基于磁盘的大型排序,和内部排序一样。
# 以及简单的临时表。
# 如果你不创建非常大的临时文件,将其放置到 swapfs/tmpfs 文件系统上也许比较好
# 另一种选择是你也可以将其放置在独立的磁盘上。
# 你可以使用”;”来放置多个路径
# 他们会按照 roud-robin 方法被轮询使用。
#tmpdir = /tmp

# *** 主从复制相关的设置

# 唯一的服务辨识号,数值位于 1 到 2^32-1之间。
# 此值在master和slave上都需要设置。
# 如果 “master-host” 没有被设置,则默认为1, 但是如果忽略此选项,MySQL不会作为master生效。
server-id = 1

# 复制的Slave (去掉master段的注释来使其生效)
#
# 为了配置此主机作为复制的slave服务器,你可以选择两种方法:
#
# 1) 使用 CHANGE MASTER TO 命令 (在我们的手册中有完整描述) -
# 语法如下:
#
# CHANGE MASTER TO MASTER_HOST=, MASTER_PORT=,
# MASTER_USER=, MASTER_PASSWORD= ;
#
# 你需要替换掉，等被尖括号包围的字段以及使用master的端口号替换 (默认3306)。
#
# 例子:
#
# CHANGE MASTER TO MASTER_HOST=’125.564.12.1′, MASTER_PORT=3306,
# MASTER_USER=’joe’, MASTER_PASSWORD=’secret’;
#
# 或者
#
# 2) 设置以下的变量. 不论如何, 在你选择这种方法的情况下， 然后第一次启动复制(甚至不成功的情况下，
# 例如如果你输入错密码在master-password字段并且slave无法连接)，
# slave会创建一个 master.info 文件，并且之后任何对于包含在此文件内的参数的变化都会被忽略
# 并且由 master.info 文件内的内容覆盖， 除非你关闭slave服务， 删除 master.info 并且重启slave 服务。
# 由于这个原因，你也许不想碰一下的配置(注释掉的) 并且使用 CHANGE MASTER TO (查看上面) 来代替
#
# 所需要的唯一id号位于 2 和 2^32 – 1之间
# (并且和master不同)
# 如果master-host被设置了.则默认值是2
# 但是如果省略,则不会生效
#server-id = 2
#
# 复制结构中的master – 必须
#master-host =
#
# 当连接到master上时slave所用来认证的用户名 – 必须
#master-user =
#
# 当连接到master上时slave所用来认证的密码 – 必须
#master-password =
#
# master监听的端口.
# 可选 – 默认是3306
#master-port =

#
# MySQL 服务端
#
[client]default-character-set=utf8
```
