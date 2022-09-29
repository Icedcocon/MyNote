# systemd 介绍

systemd是目前Linux系统上主要的系统守护进程管理工具，由于init一方面对于进程的管理是串行化的，容易出现阻塞情况，另一方面init也仅仅是执行启动脚本，并不能对服务本身进行更多的管理。所以从CentOS 7开始也由systemd取代了init作为默认的系统进程管理工具。

systemd所管理的所有系统资源都称作Unit，通过systemd命令集可以方便的对这些Unit进行管理。比如systemctl、hostnamectl、timedatectl、localctl等命令，这些命令虽然改写了init时代用户的命令使用习惯（不再使用chkconfig、service等命令），但确实也提供了很大的便捷性。

**systemd 是内核启动后的第一个用户进程，PID 为1，是所有其它用户进程的父进程。**

### systemd 特点

- 最新系统都采用systemd管理（RedHat7，CentOS7，Ubuntu15…）

- CentOS7 支持开机并行启动服务，显著提高开机启动效率

- CentOS7关机只关闭正在运行的服务，而CentOS6，全部都关闭一次。

- CentOS7服务的启动与停止不再使用脚本进行管理，也就是/etc/init.d下不在有脚本。

- CentOS7使用systemd解决原有模式缺陷，比如原有service不会关闭程序产生的子进程。

### systemd 语法

```delphi
systemctl   [command]    [unit]（配置的应用名称）

command可选项· 
start：启动指定的unit         systemctl start nginx
stop：关闭指定的unit          systemctl stop nginx
restart：重启指定unit         systemctl restart nginx
reload：重载指定unit          systemctl reload nginx
enable：系统开机时自动启动指定unit，前提是配置文件中有相关配置 systemctl enable nginx
disable：开机时不自动运行指定unit  systemctl disable nginx
status：查看指定unit当前运行状态   systemctl status nginx
```

### systemd 配置文件说明

```linux
/etc/systemd/system/*  #系统管理员安装的单元, 优先级更高

/run/systemd/system/*  #运行时动态创建unit文件的目录

/usr/lib/systemd/system/* #系统或第三方软件安装时添加的配置文件。存放systemctl脚本
```

CentOS 7的服务systemctl脚本存放在：/usr/lib/systemd/，有系统 system 和用户 user 之分， 即：/usr/lib/systemd/system 和 /usr/lib/systemd/user

- 每一个 Unit 都需要有一个配置文件用于告知 systemd 对于服务的管理方式
- 配置文件存放于/usr/lib/systemd/system/ ，设置开机启动后会在 /etc/systemd/system 目录建立软链接文件
- 每个Unit的配置文件配置默认后缀名为**.service**
- 在 /usr/lib/systemd/system/ 目录中分为 system 和 user 两个目录，一般将开机不登陆就能运行的程序存在系统服务里，也就是 /usr/lib/systemd/system
- 配置文件使用方括号分成了多个部分，并且区分大小写

# 编写服务配置

每一个服务以`.service`结尾，一般会分为3部分：**[Unit]**、**[Service]**和**[Install]**

- **[Unit]**：记录unit文件的通用信息。

- **[Service]**：记录Service的信息

- **[Install]**：安装信息。

```makefile
vim  /usr/lib/systemd/system/nginx.service

[Unit]
Description=nginx - high performance web server   #服务的简单描述
Documentation=http://nginx.org/en/docs/  #指定服务的文档，可以是一个或多个文档的 URL 路径
After=network.target remote-fs.target nss-lookup.target #表明需要依赖的服务，作用决定启动顺序

[Service]
Type=forking # 以 fork 方式从父进程创建子进程，创建后父进程会立即退出，子进程将成为主进程
PIDFile=/usr/local/nginx/logs/nginx.pid #pid文件路径
ExecStartPre=/usr/local/nginx/sbin/nginx -t -c /usr/local/nginx/conf/nginx.conf #启动前要做什么
ExecStart=/usr/local/nginx/sbin/nginx -c /usr/local/nginx/conf/nginx.conf #启动服务命令
ExecReload=/usr/local/nginx/sbin/nginx -s reload  #重启服务命令
ExecStop=/usr/local/nginx/sbin/nginx -s quit 停止当前服务时执行的命令
PrivateTmp=true #True表示给服务分配独立的临时空间

[Install]
WantedBy=multi-user.target #服务安装的用户模式，从字面上看，就是想要使用这个服务的有是谁？上文中使用的是：multi-user.target ，就是指想要使用这个服务的目录是多用户。
```

# 配置项说明

### [Unit]

主要是对这个服务的说明，内容， 文档介绍以及对一些依赖服务定义

- **Description** : 服务的简单描述
- **Documentation** ： 服务文档
- **After **= : 依赖，仅当依赖的服务启动之后再启动自定义的服务单元
- Before：表明被依赖的服务
- Requles：依赖到的其他unit ，强依赖，即依赖的unit启动失败。该unit不启动。
- Wants：依赖到的其他unit，弱依赖，即依赖的unit 启动失败。该unit继续启动
- Conflicts：定义冲突关系

### [Service]

服务的主体定义，主要定义服务的一些运行参数，及操作动作

- **Type**: 启动类型simple、forking、oneshot、notify、dbus
  - simple: 默认值，执行ExecStart指定的命令，启动主进程
  - forking: 以 fork 方式从父进程创建子进程，创建后父进程会立即退出，子进程将成为主进程
  - oneshot: 一次性进程，类似于simple，但只执行一次，Systemd 会等当前服务退出，再继续往下执行
  - dbus: 当前服务通过D-Bus启动，类似于simple，但会等待 D-Bus 信号后启动
  - notify: 当前服务启动完毕，会发出通知信号通知Systemd，然后 Systemd 再继续启动其他服务
  - idle: 类似于simple，但是要等到其他任务都执行完毕，才会启动该服务。一种使用场合是为让该服务的输出，不与其他服务的输出相混合
- User：指定开机自动运行该程序的用户名
- Group：指定开机自动运行该程序的用户组
- LimitCORE=infinity：限制内核文件的大小
- LimitNOFILE=65536：服务最大允许打开的文件描述符数量
- LimitNPROC=65536：进程的最大数量
- **PIDFile**：指定开机自动运行该程序的pid文件(一般在程序配置文件中配置该项)
- **ExecStart**：启动当前服务的命令
- **ExecStartPre**：启动当前服务之前执行的命令,上文中是测试配置文件 －t
- ExecStartPost：启动当前服务之后执行的命令
- **ExecReload**：重启当前服务时执行的命令
- **ExecStop**：停止当前服务时执行的命令
- ExecStopPost：停止当其服务之后执行的命令
- KillMode：定义如何停止服务。KillMode字段可以设置的值如下
  - control-group(默认值)：当前控制组里面的所有子进程，都会被杀掉;
  - process：只杀主进程;
  - mixed：主进程将收到SIGTERM信号，子进程收到SIGKILL信号;
  - none：没有进程会被杀掉，只是执行服务的stop命令。如ssh服务将KillMode设为process，不停止任何sshd子进程，即子进程打开的SSH session仍然保持连接，这个设置不太常见，但对 sshd 很重要，否则你停止服务的时候，会连自己打开的 SSH session一起杀掉。
- KillSignal: 设置杀死进程的第一步使用什么信号, 默认值为 `SIGTERM` 信号。
- RestartSec：自动重启当前服务等待的秒数
- Restart：定义了当前服务退出后，Systemd的重启方式，可能的值包括
  - no(默认值)：退出后不会重启;
  - always：不管是什么退出原因，总是重启;
  - on-success：只有正常退出时(退出状态码为0)，才会重启;
  - on-failure：非正常退出时(退出状态码非0)，包括被信号终止和超时，才会重启;
  - on-abnormal：只有被信号终止和超时，才会重启;
  - on-abort：只有在收到没有捕捉到的信号终止时，才会重启;
  - on-watchdog：超时退出，才会重启，如ssh服务设置为on-failure，表示任何意外的失败，就将重启sshd。如果sshd正常停止(比如执行systemctl stop命令)，它就不会重启。
- RemainAfterExit：值为yes或no，表示进程退出以后，服务仍然保持执行。这样的话，一旦使用systemctl stop命令停止服务，ExecStop指定的命令就会执行
- TimeoutSec：定义 Systemd 停止当前服务之前等待的秒数
- Environment：指定当前服务的环境变量
- EnvironmentFile：指定当前服务的环境参数文件，该文件的key=value键值对，可以用$key的形式，在当前配置文件中获取
- 所有的启动设置都可以加上一个连词号(-)，表示"抑制错误"，即发生错误的时候，不影响其他命令的执行。比如，EnvironmentFile=-/etc/sysconfig/sshd，表示即使/etc/sysconfig/sshd文件不存在，也不会抛出错误。
- **PrivateTmp** 的值设置成true ，服务启动时会在/tmp目录下生成类似systemd-private-433ef27ba3d46d8aac286aeb1390e1b-nginx.service-RedVyu的文件夹，用于存放nginx的临时文件。

### [Install]

服务安装的相关设置，一般可设置为多用户的

- **WantedBy**：它的值是一个或多个 Target，当前 Unit 激活时(enable)符号链接会放入/etc/systemd/system目录下面以 Target 名 + .wants后缀构成的子目录中

- RequiredBy：它的值是一个或多个 Target，当前 Unit 激活时，符号链接会放入/etc/systemd/system目录下面以 Target 名 + .required后缀构成的子目录中

- Alias：当前 Unit 可用于启动的别名

- Also：当前 Unit 激活(enable)时，会被同时激活的其他 Unit

- Linux 缓和的执行进程关闭，然后重启。在对配置文件修改后需要重启进程时可发送此信号。

# 配置文件示例

## Tomcat服务

```ini
## YUM安装
[Unit]
Description=Apache Tomcat Web Application Container
After=syslog.target network.target

[Service]
Type=simple
EnvironmentFile=/etc/tomcat/tomcat.conf
Environment="NAME="
EnvironmentFile=-/etc/sysconfig/tomcat
ExecStart=/usr/libexec/tomcat/server start
SuccessExitStatus=143
User=tomcat

[Install]
WantedBy=multi-user.target


## 二进制安装
[Unit]
Description=tomcat
After=network.target

[Service]
Type=forking
Environment="export JAVA_HOME=/opt/jdk"
Environment="export JAVA_BIN=$JAVA_HOME/bin"
Environment="export JRE_HOME=$JAVA_HOME/jre"
Environment="export CLASSPATH=$JAVA_HOME/jre/lib:$JAVA_HOME/lib"
Environment="export PATH=$PATH:$JAVA_HOME/bin"
ExecStart=/usr/local/tomcat/bin/startup.sh
ExecStop=/usr/local/tomcat/bin/shutdown.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
