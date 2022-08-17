# Docker 概念

### 1.Docker的概念

- 是实现容器技术的一种工具
- 是一个开源的应用容器引擎
- 使用 C/S 架构模式，通过远程API 来管理
- 可以打包一个应用及依赖包到一个轻量级、可移植的容器中

### 2.容器的概念

- 对应用软件和依赖包进行标准打包

- 应用或服务之间相互隔离，但又共享一个 OS

- 可以打包运行在不同的系统上

### 3.为什么使用容器？

- 为了提高部署应用效率和虚拟化的局限性

### 4.Docker和虚拟化的区别

![](https://uploadfiles.nowcoder.com/images/20220508/802578331_1652010574419/E06E4C03862AF6B0B6B3023E2A061F90)

### 5.Docker 容器有几种在状态？

<img title="" src="file:///D:/Cache/MarkText/Docker-state.jpeg" alt="" data-align="center" width="525">

- starting 运行状态
- Exited 退出状态
- Paused 暂停状态
- healthy 健康状态
- unhealthy 非健康状态

### Docker基础指令

| 命令                | 描述                                                                       |
| ----------------- | ------------------------------------------------------------------------ |
| docker attach     | 将本地的标准输入、输出、错误流附加到正在运行的容器上。                                              |
| docker build      | 从Dockerfile构建镜像                                                          |
| docker builder    |                                                                          |
| docker checkpoint |                                                                          |
| docker commit     | 利用修改后的容器构建镜像。                                                            |
| docker config     | 管理Docker的配置文件                                                            |
| docker container  | 管理容器                                                                     |
| docker context    |                                                                          |
| docker cp         | 在本地文件系统和容器间拷贝数据                                                          |
| docker create     | 创建一个处于stopped态的容器                                                        |
| docker diff       | Inspect changes to files or directories on a container’s  filesystem     |
| docker events     | Get real time events from the server                                     |
| docker exec       | 在一个running态的容器中执行指令                                                      |
| docker export     | Export a container’s filesystem as a tar archive                         |
| docker history    | 显示镜像的历史                                                                  |
| docker image      | 管理镜像                                                                     |
| docker images     | 列出镜像                                                                     |
| docker import     |                                                                          |
| docker info       |                                                                          |
| docker inspect    | 返回Docker对象的底层信息                                                          |
| docker kill       | Kill 一个或多个处于running态的镜像                                                  |
| docker load       |                                                                          |
| docker login      |                                                                          |
| docker logout     |                                                                          |
| docker logs       | 获取容器的日志                                                                  |
| docker manifest   | Manage Docker image manifests and manifest lists                         |
| docker network    | 管理Docker网络                                                               |
| docker node       | 管理Swarm nodes                                                            |
| docker pause      | 暂停一个或多个容器中所有的进程                                                          |
| docker plugin     |                                                                          |
| docker port       |                                                                          |
| docker ps         | 列出容器                                                                     |
| docker pull       | 从注册表？拉取镜像或仓库                                                             |
| docker push       | 推送镜像或仓库                                                                  |
| docker rename     | 重命名一个容器                                                                  |
| docker restart    | 重启一个或多个容器                                                                |
| docker rm         | 删除一个或多个容器                                                                |
| docker rmi        | 删除一个或多个镜像                                                                |
| docker run        | 在一个新的容器中执行指令                                                             |
| docker save       | Save one or more images to a tar archive (streamed to STDOUT by default) |
| docker search     | 在Docker Hub中查找镜像                                                         |
| docker secret     |                                                                          |
| docker service    |                                                                          |
| docker stack      |                                                                          |
| docker start      | 启动一个或多个处于 stopped 态的容器                                                   |
| docker stats      | Display a live stream of container(s) resource usage statistics          |
| docker stop       | 停止一个或多个处于 running 态的容器                                                   |
| docker swarm      | Manage Swarm                                                             |
| docker system     | 管理 Docker                                                                |
| docker tag        | Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE                    |
| docker top        | Display the running processes of a container                             |
| docker trust      | Manage trust on Docker images                                            |
| docker unpause    | Unpause all processes within one or more containers                      |
| docker update     | Update configuration of one or more containers                           |
| docker version    | Show the Docker version information                                      |
| docker volume     | Manage volumes                                                           |
| docker wait       | Block until one or more containers stop, then print their exit  codes    |

# Docker RUN操作

- 建立并运行容器

### 选项

```bash
# docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
# Options:
#   -a, --attach list        指定标准输入输出类型 STDIN/STDOUT/STDERR。
docker run -a stdin -a stdout -i -t nginx /bin/bash
#       --cidfile string     将容器ID写入该文件
#   -d, --detach             后台运行容器并输出容器ID
docker run -d nginx /bin/bash -c "while true; do echo 'He80llo world'; done"
#       --device             允许访问宿主机指定设备
docker run -it --device /dev/mapper/centos-home:/dev/home:r  python /bin/bash
#       --entrypoint string  覆盖镜像默认的ENTRYPOINT
#   -e, --env list           设置环境变量，使用多个标志设置多个环境变量
docker run -e "MYNAME=ruyi" -e NEWNAME="Ashley"  --rm -dit --name temp_nginx nginx /bin/bash
#       --env-file list      从文件中读入环境变量
#       --expose list        标记应该暴露哪些端口，可以与-P配合将list中端口暴露
docker run -d --expose 80 --expose 8080 -P nginx # 暴露不等于容器内部监听端口
#   -h, --hostname string    指定容器hostname，默认docker id的一部分
docker run -it -h ruyi nginx /bin/bash
#   -i, --interactive        Keep STDIN open even if not attached
docker run -it nginx /bin/bash
#   -m, --memory bytes       设置内存限制
#       --name string        为容器命名
docker run --name temp_nginx -it nginx /bin/bash
#       --network network    将容器连接到网络，默认启用网络
#       --network="bridge"
docker run --network none nginx #禁用所有传入和传出网络。
#       --dns list           设置DNS服务器，默认容器与主机的 DNS 服务器相同
#       --pid string         '':默认启用容器 PID 命名空间 进程分离 可重用PID 1
#                            'container:<name|id>':加入其他容器的PID命名空间
#                            'host':使用宿主机的命名空间
docker run -it --pid='host' python /bin/bash
#       --privileged         可以访问宿主机所有设备，且程序可以像宿主机程序一样运行
docker run --rm -it --privileged  python /bin/bash
#   -p, --publish list       将容器端口映射（发布到）到宿主机指定端口
docker run -d -p 127.0.0.1:3306:3306 mysql /bin/bash
#   -P, --publish-all        将容器指定端口映射（发布到）到宿主机随机端口
docker run -d --expose 80 --expose 8080 -P nginx
#       --restart string     容器退出时的重启策略 (默认为"no")
docker run --restart=on-failure:10 nginx
#       --rm                 当容器处于exits状态时，自动删除容器
docker run --rm -it python /bin/bash
#   -t, --tty                分配一个伪终端
docker run -it --privileged  python /bin/bash
#   -u, --user string        指定执行指令的用户名或ID
#                            (格式: <name|uid>[:<group|gid>])
#       --userns string      指定要是用的User namespace
#       --uts string         指定要是用的UTS namespace
#   -v, --volume list        Bind mount a volume
#       --volumes-from list  Mount volumes from the specified container(s)
#   -w, --workdir string     指定命令运行时的工作目录
```

### 前台模式

```bash
-a=[]           : 连接（Attach to）到`STDIN`,`STDOUT`和/或`STDERR`
-t              : 分配一个伪终端pts（run默认连接`STDOUT`和`STDERR`）。
-i              : 保持STDIN打开，从而可以与容器交互
```

- 不使用`-a`标志的默认情况下，Docker将当前终端连接（attach）容器的`stdout`和`stdin`。

```bash
docker run -a stdin -a stdout -i -t ubuntu /bin/bash
```

- 当Docker客户端从管道接受标准输入时，不能使用`-t`指令，如下：

```bash
echo test | docker run -i busybox cat
echo "cat /etc/hosts" | sudo docker run --rm -i nginx /bin/bash
```

- 只是用`-t`指令，由于容器输入未指定，因此只能输出`STDOUT`和`STDERR`而不能交互。

- 只是用`-i`指令，由于未分配伪终端，因此不会显示shell提示符。

### 网络设置

```bash
# --dns=[]           : 设置容器的DNS服务器
# --network="bridge" : 设置容器的网络连接
#                       'bridge': 网桥（默认）
#                       'none': 无网络
#                       'container:<name|id>': 复用另一个容器的网络栈
#                       'host': 使用Docker宿主机的网络栈
#                       '<network-name>|<network-id>': 连接用户定义网络
# --network-alias=[] : 为容器的网络添加别名
# --add-host=""      : 向/etc/hosts (host:IP)中添加一行字符串
# --mac-address=""   : 设置容器的以太网设备的MAC地址
# --ip=""            : 设置容器的以太网设备的IPv4地址
# --ip6=""           : 设置容器的以太网设备的IPv6地址
# --link-local-ip=[] : 设置一个或多个容器的以太网设备的连接为本地IPv4/IPv6地址
```

- `--link` 可以指定一个容器名，使用该标志的容器可以将容器名作为域名解析出对应的veth IP地址。该标志实际修改了`/etc/hosts`文件中的路由转发表。（不建议使用）

- 各容器间暴露端口只能通过网桥进行。

- 容器的DNS服务器默认与宿主机一致，但可以使用`--dns`指定新的服务器。

- 容器的MAC 地址默认使用容器的 IP 地址自动生成，可通过`--mac-address`参数显示指定MAC地址。但Docker 不检查手动指定的 MAC 地址是否唯一。

| 网络类型                       | 描述                                     |
| -------------------------- | -------------------------------------- |
| **none**                   | 无网络连接。                                 |
| **bridge** (default)       | 使用**veth接口**连接**容器**和**网桥**            |
| **host**                   | 在容器中使用宿主机的网络栈                          |
| **container**:\<name\|id\> | 通过指定容器的名字或ID，使用另一个容器的网络栈               |
| **NETWORK**                | 连接自定义网络 (`docker network create` 命令创建) |

<img title="" src="file:///D:/Cache/MarkText/2022-08-11-20-37-30-image.png" alt="" data-align="center" width="449">

<img title="" src="file:///D:/Cache/MarkText/2022-08-11-20-38-37-image.png" alt="" data-align="center" width="429">

##### none

- 除了自身的`loopback`接口，容器不能访问任何外部路由，但是仍然可以通过标准输入输出访问。

##### bridge

- 容器默认的网络设置为网桥`bridge`，该网络类型会创建一对`veth`接口，一个位于容器的`namespace`中，另一个则位于宿主机的`namespace`中与 `docker0` 连接。每个`veth`接口都有各自的IP地址。`docker0`是位于宿主机上的网桥。

##### host

- 这种模式下容器的**网络性能更好**，适用于对网络要求极高的应用。

- 宿主机所有接口容器都可以使用。

- 容器的`hostname`与宿主机一致

- 在`host` 网络模式下，不能使用`--mac-address`

- 在`host` 网络模式下，容器也有自己的 UTS 命名空间。

- 在`host` 网络模式下，可以使用`--hostname` 和 `--domainname`

- `--add-host`, `--dns`, `--dns-search`也可执行，而且只会修改容器中的 `/etc/hosts` 和 `/etc/resolv.conf`文件，并不会修改宿主机的。

##### container:\<name|id\>

- 使用该标志的容器会公用另一个容器的网络栈。

- 这种模式下`--add-host` `--hostname` `--dns` `--dns-search` `--dns-option` 和 `--mac-address`不能使用，`--publish` `--publish-all` `--expose`也不能使用。

- 运行 Redis 容器，并让服务在`localhost`运行，然后运行redis客户端容器，使用redis容器的网络栈，并连接`localhost`。

```bash
# 运行redis服务，让Redis运行在容器的localhost
docker run -d --name redis example/redis --bind 127.0.0.1
# 使用redis容器的网络栈并连接localhost
docker run --rm -it --network co ntainer:redis example/redis-cli -h 127.0.0.1
```

##### 用户自定义网络（推荐）

- 可以通过`Docker network driver`或者`external network driver plugin`创建网络。

- 多个容器可以连接同一个网络，并且自动进行主机名和IP地址的转换。

```bash
# 以下示例使用内置`bridge`网络驱动程序创建网络并在创建的网络中运行容器
docker network create -d bridge my-net
docker run --network=my-net -itd --name=container3 busybox
```

##### 管理 /etc/hosts

- 容器的`/etc/hosts`文件内定义了自己的hostname和`localhost`。

- `--add-host`可以向该文件添加新的主机名

### 运行时特权和 Linux 功能

##### 选项

| 选项             | 描述                                   |
| -------------- | ------------------------------------ |
| `--cap-add`    | 添加 Linux 功能                          |
| `--cap-drop`   | 放弃 Linux 功能                          |
| `--privileged` | 授予此容器扩展权限，可访问宿主机所有设备                 |
| `--device=[]`  | 没有 --privileged 标志时，容器也可以访问指定宿主机的设备。 |

- Docker 容器默认情况下不允许访问任何设备，因此不能在 Docker 容器内运行 Docker 守护程序。

- 执行`docker run --privileged`后，Docker **可访问宿主机上所有设备**，并配置AppArmor 或 SELinux 使容器内的应用像宿主机的程序一样访问宿主机资源。

- 如需限制对特定设备的访问或仅访问部分设备，应该使用`--device`标志。它可以指定一个或多个可在容器内访问的设备。

```bash
# docker run --device=宿主机设备:Docker设备:rwm权限
docker run --device=/dev/snd:/dev/snd ...
```

- 容器默认对设备有`read`、`write`、 和`mknod`权限，可以在第三个位置设置权限`宿主机设备:Docker设备:rwm权限`。

```bash
docker run --device=/dev/sda:/dev/xvdc --rm -it ubuntu fdisk  /dev/xvdc
# 不允许修改分区表
docker run --device=/dev/sda:/dev/xvdc:r --rm -it ubuntu fdisk  /dev/xvdc
# crash
docker run --device=/dev/sda:/dev/xvdc:w --rm -it ubuntu fdisk  /dev/xvdc
# fdisk: unable to open /dev/xvdc: Operation not permitted
docker run --device=/dev/sda:/dev/xvdc:m --rm -it ubuntu fdisk  /dev/xvdc
```

- `--cap-add`和`--cap-drop`可以对功能进行细粒度控制，且支持变量ALL添加或去掉所有功能。

这两个标志都支持 value `ALL`，因此允许容器使用除以下之外的所有功能`MKNOD`：

```bash
# 允许容器使用MKNOD之外的所有功能
docker run --cap-add=ALL --cap-drop=MKNOD ...
```

- `--cap-add`和`--cap-drop`标志接受使用`CAP_`前缀指定的功能。因此，以下示例是等效的：

```bash
docker run --cap-add=SYS_ADMIN ...
docker run --cap-add=CAP_SYS_ADMIN ...
```

### 重启策略（--restart）

##### 选项

- `--restart`标志用于指定容器在退出时采用哪种重启策略。

- 如果重启策略启动，则容器在`docker ps`中只会显示`Up`或`Restarting`状态。

- Docker 支持以下重启策略：

| 策略                           | 结果                         |
| ---------------------------- | -------------------------- |
| **no**                       | 容器退出时不会重启（默认）。             |
| **on-failure**[:max-retries] | 容器非零状态退出时重启， 可以限制尝试重启的次数。  |
| **always**                   | Docker守护进程一旦启动就无限次尝试重启该容器。 |
| **unless-stopped**           | 同上，除非容器进入`stopped`状态       |

- 守护进程会每重启失败一次就将重启延迟加倍，初始延迟为100ms，直到达到`on-failure`限制，或者延迟达到 1 分钟的最大值不再变化。

- 容器重启成功并运行10s后，延迟被重置为100ms。

- `on-failure`可以指定重启容器最大次数，默认一直重启。

- 可以通过`docker inspect`获取重启次数和上次重启/启动的时间。

```bash
# 获取容器“my-container”的重启次数
docker inspect -f "{{ .RestartCount }}" my-container
# 容器上次（重新）启动的时间
docker inspect -f "{{ .State.StartedAt }}" my-container
```

- **`--restart`(restart policy) 与`--rm`(clean up) 标志不能同时使用**。

- 例子

```bash
# awlays
docker run --restart=always redis
# on-failure
docker run --restart=on-failure:10 redis
```

##### 退出状态

- 非零状态退出代码遵循`chroot`标准

- **125**：错误与 Docker 守护程序本身有关；

```bash
docker run --foo busybox; echo $?
# flag provided but not defined: --fooSee 'docker run --help'.125
```

- **126**：命令无法被调用

```bash
docker run busybox /etc; echo $?
# docker: Error response from daemon: Container command '/etc' could not be invoked.126
```

- **127**：无法找到命令

```bash
docker un busybox foo; echo $?
# docker: Error response from daemon: Container command 'foo' not found or does not exist.127
```

- **容器内运行程序返回的退出代码**

```bash
docker run busybox /bin/sh -c 'exit 3'
echo $?
# 3
```

### 覆盖 Dockerfile 映像默认值

- 使用Dockerfile构建镜像时可以设置默认参数，在容器启动时生效，其中4个Dockerfile命令不能用`run`命令覆盖：`FROM`、 `MAINTAINER`、`RUN`和`ADD`。

##### CMD（默认命令或选项）

```bash
docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]
```

- `docker run `命令末端的`COMMAND`是可选的，**默认运行Dockerfile`CMD`指令指定值**。

- 在`docker run` 命令末端指定新的`COMMAND`就能将Dockerfile`CMD`指定的默认值覆盖。

- 如果镜像指定了`ENTRYPOINT`，**那么`CMD`或`COMMAND` 将作为参数追加在`ENTRYPOINT`后**。

##### ENTRYPOINT（在运行时执行的默认命令）

```bash
    --entrypoint="": 覆盖镜像中指定的默认entrypoint
```

- `ENTRYPOINT`类似于 `COMMAND`，它指定了容器启动时运行的可执行文件，是容器的默认性质或行为。

- 指定`ENTRYPOINT`的容器可以像二进制可执行文件一样执行，此时的`CMD`或`COMMAND`用于执行选项。

- `--entrypoint=""`用于用户想要运行容器内其他程序时。

```bash
$ docker run -it --entrypoint /bin/bash example/redis
```

- 传递多个参数给该 ENTRYPOINT ：

```bash
$ docker run -it --entrypoint /bin/bash example/redis -c ls -l
$ docker run -it --entrypoint /usr/bin/redis-cli example/redis --help
```

- 传入空字符串可以重置容器入口点：

```bash
$ docker run -it --entrypoint="" mysql bash
```

> **笔记**
> 
> **指定`--entrypoint`会清除镜像上的默认命令集（即`CMD`指定的指令）**。

##### EXPOSE（传入端口）

```bash
--expose=[]: 指定容器内部要暴露给外部的端口，会覆盖Dockerfile中的EXPOSE设置。
-P         : 映射容器中所有应当暴露的端口到宿主机中的随机端口
-p=[]      : 映射容器中的端口到宿主机的指定端口
--link=""  : Add link to another container (<name or id>:alias or <name or id>)
```

- 格式: 
  
  - `ip:hostPort:containerPort` 
  
  - `ip::containerPort`  （随机）
  
  - `hostPort:containerPort` 
  
  - `containerPort`  （随机）

- 宿主机的端口和容器的端口都可以是一个范围，但两者的数量必须匹配
   -p 1234-1236:1234-1236/tcp

- 可以只指定宿主机的端口范围，容器的端口会映射到这个范围内，如
  
  - `-p 1234-1236:1234/tcp`

- `docker port` 可以查看实际端口映射

##### ENV（环境变量）

- Docker 在创建 Linux 容器时会自动设置一些环境变量。

| 变量         | 值                                                                        |
| ---------- | ------------------------------------------------------------------------ |
| `HOME`     | 根据`USER`确定                                                               |
| `HOSTNAME` | 主机名与容器ID有关                                                               |
| `PATH`     | 包括常用的目录，例如`/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin` |
| `TERM`     | 如果容器被分配一个伪终端，则为`xterm`                                                   |

- 可以通过一个或多个`-e`标志，设置或覆盖容器的环境变量。

```bash
$ export today=Wednesday
$ docker run -e "NAME=ruyi" -e NEWNAME --rm alpine env
```

##### VOLUME（共享文件系统）

```bash
-v, --volume=[host-src:]container-dest[:<options>]: 挂载一个volume。

The `nocopy` mode is used to disable automatically copying the requested volume
path in the container to the volume storage location.
For named volumes, `copy` is the default mode. Copy modes are not supported
for bind-mounted volumes.

--volumes-from="": 从给定容器中挂载所有volume
```

- `options` 可以是：
  
  - [rw|ro]
  
  - [z|Z]
  
  - [[r]shared|[r]slave|[r]private]
  
  - [nocopy]
  
  - 如果不指定`rw`或`ro`则默认为read-write模式

- `host-src`是一个宿主机上的绝对路径名

- 开发者（Dockerfile）可以定义一个或多个volume挂载到一个容器，但只有用户（`run`）可以指定多个容器共享一个volume。

##### 用户

```bash
-u="", --user="": 设置用户名/UID，也可以设置用户组名及GID

以下各种形式都是合法的:
--user=[ user | user:group | uid | uid:gid | user:gid | uid:group ]
```

- 默认用户为root。

- 开发镜像时可以创建其他用户或用户组。

- 运行容器时可以指定用户或用户组。

- Dockerfile 中的`USER`指令可以指定运行容器时的默认用户，而操作者可以使用`-u`命令修改所使用的用户。

### Docker日志驱动 (--log-driver)

- 在`docker run`命令后使用`--log-driver=VALUE`，可以配置日志驱动。

- 可以使用以下配置：

| 驱动           | 描述                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| `none`       | 禁用容器的所有日志。此选项不能使用 `docker logs` 查看容器日志。                                                                                        |
| `local`      | Logs are stored in a custom format designed for minimal overhead.                                                              |
| `json-file`  | Docker的默认日志驱动。日志数据被写入JSON文件。 No logging options are supported for this driver.                                                 |
| `syslog`     | 日志数据被写入syslog。                                                                                                                 |
| `journald`   | 日志数据被写入`journald`。                                                                                                             |
| `gelf`       | Graylog Extended Log Format (GELF) logging driver for Docker. Writes log messages to a GELF endpoint likeGraylog or Logstash.  |
| `fluentd`    | Fluentd logging driver for Docker. Writes log messages to `fluentd` (forward input).                                           |
| `awslogs`    | Amazon CloudWatch Logs logging driver for Docker. Writes log messages to Amazon CloudWatch Logs.                               |
| `splunk`     | Splunk logging driver for Docker. Writes log messages to `splunk` using Event Http Collector.                                  |
| `etwlogs`    | Event Tracing for Windows (ETW) events. Writes log messages as Event Tracing for Windows (ETW) events. Only Windows platforms. |
| `gcplogs`    | Google Cloud Platform (GCP) Logging. Writes log messages to Google Cloud Platform (GCP) Logging.                               |
| `logentries` | Rapid7 Logentries. Writes log messages to Rapid7 Logentries.                                                                   |

-  `docker logs`命令只能在 `json-file` 个 `journald`两个日志驱动下使用。其他情况日志被输出到各自的引擎，`docker logs`无法读取。

# docker history操作

### 用法

```bash
docker history [OPTIONS] IMAGE
```

### 选项

| 名称, 简称           | 默认     | 描述               |
| ---------------- | ------ | ---------------- |
| `--format`       |        | 使用 Go 模板格式化输出    |
| `--human` , `-H` | `true` | 适合人类习惯的单位输出日期和大小 |
| `--no-trunc`     |        | 不截断输出            |
| `--quiet` , `-q` |        | 只显示镜像ID          |

### 例子

- 查看 `docker:latest` 镜像构造过程:

```bash
$ docker history docker

IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
3e23a5875458        8 days ago          /bin/sh -c #(nop) ENV LC_ALL=C.UTF-8            0 B
8578938dd170        8 days ago          /bin/sh -c dpkg-reconfigure locales &&    loc   1.245 MBbe51b77efb42        8 days ago          /bin/sh -c apt-get update && apt-get install    338.3 MB
4b137612be55        6 weeks ago         /bin/sh -c #(nop) ADD jessie.tar.xz in /        121 MB
750d58736b4b        6 weeks ago         /bin/sh -c #(nop) MAINTAINER Tianon Gravi <ad   0 B
511136ea3c5a        9 months ago                                                        0 B                 Imported from -
```

### 格式化输出

| 占位符             | 描述                                   |
| --------------- | ------------------------------------ |
| `.ID`           | 镜像 ID                                |
| `.CreatedSince` | 创建以来经过的时间 if `--human=true`, else时间戳 |
| `.CreatedAt`    | 镜像被创建时的时间戳                           |
| `.CreatedBy`    | 用于创建镜像的命令                            |
| `.Size`         | 镜像大小                                 |
| `.Comment`      | 注释                                   |

When using the `--format` option, the `history` command will either output the data exactly as the template declares or, when using the `table` directive, will include column headers as well.

The following example uses a template without headers and outputs the `ID` and `CreatedSince` entries separated by a colon (`:`) for the `busybox` image:

```bash
$ docker history --format "{{.ID}}: {{.CreatedSince}}" busybox

f6e427c148a7: 4 weeks ago
<missing>: 4 weeks ago
```

# docker inspect操作

### 用法

```bash
$ docker inspect [OPTIONS] NAME|ID [NAME|ID...]
```

### 描述

- 提供构造镜像、容器的底层信息

- `docker inspect` 默认以 JSON array 形式返回。

### 选项

| 名称, 简写            | 默认  | 描述               |
| ----------------- | --- | ---------------- |
| `--format` , `-f` |     | 使用给定的 Go 模板格式化输出 |
| `--size` , `-s`   |     | 如果类型时容器，返回其大小    |
| `--type`          |     | 返回给定类型的JSON数据    |

### 例子

##### 获取实例的 IP 地址

```bash
$ docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $INSTANCE_ID
```

##### 获取实例的 MAC 地址

```bash
$ docker inspect --format='{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' $INSTANCE_ID
```

##### 获取实例的日志路径

```bash
$ docker inspect --format='{{.LogPath}}' $INSTANCE_ID
```

##### 获取实例的 image name

```bash
$ docker inspect --format='{{.Config.Image}}' $INSTANCE_ID
```

##### 列出所有绑定的端口

You can loop over arrays and maps in the results to produce simple text output:

```bash
$ docker inspect --format='{{range $p, $conf := .NetworkSettings.Ports}} {{$p}} -> {{(index $conf 0).HostPort}} {{end}}' $INSTANCE_ID
```

##### Find a specific port mapping[🔗](https://docs.docker.com/engine/reference/commandline/inspect/#find-a-specific-port-mapping)

The `.Field` syntax doesn’t work when the field name begins with a number, but the template language’s `index` function does. The `.NetworkSettings.Ports` section contains a map of the internal port mappings to a list of external address/port objects. To grab just the numeric public port, you use `index` to find the specific port map, and then `index` 0 contains the first object inside of that. Then we ask for the `HostPort` field to get the public address.

```bash
$ docker inspect --format='{{(index (index .NetworkSettings.Ports "8787/tcp") 0).HostPort}}' $INSTANCE_ID
```

##### Get a subsection in JSON format

If you request a field which is itself a structure containing other fields, by default you get a Go-style dump of the inner values. Docker adds a template function, `json`, which can be applied to get results in JSON format.

```bash
$ docker inspect --format='{{json .Config}}' $INSTANCE_ID
```

# docker top操作

- 查看容器内部运行进程

### 用法

```bash
$ docker top CONTAINER [ps OPTIONS]
```

- ps OPTIONS**怎么用**？

# docker stats操作

- 实时显示容器内进程的统计信息

### 用法

```bash
$ docker stats [OPTIONS] [CONTAINER...]
```

### 描述

- 不指定容器或容器ID则显示所有容器的实时统计信息。

- 可以用空格隔开容器ID， 输出多个容器的统计信息。

### 选项

| 名称，简写          | 默认  | 描述                      |
| -------------- | --- | ----------------------- |
| `--all` , `-a` |     | 显示所有容器数据（默认只显示running态） |
| `--format`     |     | 使用Go模板格式化输出             |
| `--no-stream`  |     | 禁用动态显示 只显示快照            |
| `--no-trunc`   |     | 不要截断输出                  |

### 例子

- 不使用 `--format`，输出全部字段时，会显示以下列：

| 列名                        | 描述               |
| ------------------------- | ---------------- |
| `CONTAINER ID` and `Name` | 容器 ID 和名字        |
| `CPU %` and `MEM %`       | 宿主机的CPU和内存使用率    |
| `MEM USAGE / LIMIT`       | 内存使用量及内存使用上限     |
| `NET I/O`                 | 容器通过其网络接口收发数据量   |
| `BLOCK I/O`               | 容器读写宿主机块存储设备的数据量 |
| `PIDs`                    | 容器建立的进程或线程数      |

- 使用 `docker stats` 显示多个容器的数据。

```bash
$ docker stats awesome_brattain 67b2525d8ad1
```

- 使用 `docker stats` 输出 `json` 格式信息。（**json输出的属性可用作go模板参数**）

```bash
$ docker stats nginx --no-stream --format "{{ json . }}"
```

使用 `docker stats` 输出格式化信息

```bash
$ docker stats --all --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" fervent_panini 5acfcb1b4fd1 drunk_visvesvaraya big_heisenberg
```

### 格式化

- 合法占位符如下：

| 占位符          | 描述                  |
| ------------ | ------------------- |
| `.Container` | 容器名称或ID             |
| `.Name`      | 容器名称                |
| `.ID`        | 容器 ID               |
| `.CPUPerc`   | CPU 使用率             |
| `.MemUsage`  | 内存使用率               |
| `.NetIO`     | 网络 IO               |
| `.BlockIO`   | 块存储设备 IO            |
| `.MemPerc`   | 内存使用量 (Windows不可用)  |
| `.PIDs`      | 进程/线程数 (Windows不可用) |

- 使用格式化输出时不会显示列名，但可以在前面添加`table`关键词显示列名。

```bash
# 不显示列名
$ docker stats --format "{{.Container}}: {{.CPUPerc}}"
# 显示列名
$ docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

# docker exec操作

- 在一个**running态**的容器中，以**开辟新进行/线程**的方式，执行指令。

- 可以执行后台任务和交互式任务两种。

### 用法

```bash
$ docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
```

### 描述

- 在容器中开启一个新进程/线程

- 只在容器主进程(`PID 1`)运行时运行，容器**重启不会再次执行**。

- 命令在容器默认工作路径下运行，镜像中如果通过`WORKDIR`指定，则在指定路径下运行。

- 命令应当是可执行文件，链接或带引号的字符串命令不会执行。
  
  -  `docker exec -ti my_container "echo a && echo b"`不会执行；
  
  -  `docker exec -ti my_container sh -c "echo a && echo b"`可执行。

### 选项

| 名称，简写                  | 默认  | 描述                                                  |
| ---------------------- | --- | --------------------------------------------------- |
| `--detach` , `-d`      |     | 后台运行                                                |
| `--detach-keys`        |     | Override the key sequence for detaching a container |
| `--env` , `-e`         |     | 设置环境变量                                              |
| `--env-file`           |     | 从文件中读取并设置环境变量                                       |
| `--interactive` , `-i` |     | 保持STDIN开启                                           |
| `--privileged`         |     | 授予容器特权                                              |
| `--tty` , `-t`         |     | 分配TTY                                               |
| `--user` , `-u`        |     | 用户名或UID (格式: <name\|uid>[:<group\|gid>])            |
| `--workdir` , `-w`     |     | 指定命令的工作路径                                           |

### 例子

- 对一个running态的容器使用`docker exec`

```bash
$ docker run --name ubuntu_bash --rm -i -t ubuntu bash
$ docker exec -d ubuntu_bash touch /tmp/execWorks
```

- 对一个paused态的容器使用`docker exec`
  
  - 如果容器处于paused态，会报错返回error

# docker stop

停止处于running态的容器

### 用法

```bash
$ docker stop [OPTIONS] CONTAINER [CONTAINER...]
```

### 描述

- 容器内的主进程会收到`SIGTERM`，并在grace period后收到`SIGKILL`。

- 第一个发送的信号可以在Dockerfile中通过`STOPSIGNAL`修改，或在`docker run`后通过`--stop-signal`选项修改。

- `docker kill`可以直接向容器发送`SIGKILL`信号

### 选项

| 名称，简写           | 默认   | 描述                |
| --------------- | ---- | ----------------- |
| `--time` , `-t` | `10` | 发送`SIGKILL`信号前的秒数 |

### 例子

```bash
$ docker stop my_container
```

# docker kill操作

- 杀死一个或多个处于running态的容器

### 用法

```bash
$ docker kill [OPTIONS] CONTAINER [CONTAINER...]
```

### 描述

- 默认发送`SIGKILL`信号

- 可以通过名称或数字来指定要发送的信号

- 信号的`SIG`前缀可以省略

### 选项

| 名称，简写             | 默认     | 描述        |
| ----------------- | ------ | --------- |
| `--signal` , `-s` | `KILL` | 要发送给容器的信号 |

### 例子

- 发送默认信号

```bash
$ docker kill my_container
```

- 向容器发送其他信号

```bash
$ docker kill --signal=SIGHUP  my_container
```

```bash
$ docker kill --signal=SIGHUP my_container      # 指定信号名
$ docker kill --signal=HUP my_container         # 省略前缀
$ docker kill --signal=1 my_container           # 指定信号数字
```

# docker network

- 管理Docker 网络

### 子命令

| 命令                        | 描述             |
| ------------------------- | -------------- |
| docker network connect    | 将容器连接到网络       |
| docker network create     | 创建一个网络         |
| docker network disconnect | 断开容器与网络的连接     |
| docker network inspect    | 显示一个或多个网络的详细信息 |
| docker network ls         | 列出网络           |
| docker network prune      | 移除所有未使用网络      |
| docker network rm         | 移除一个或多个网络      |

### docker network create

- 创建一个网络

##### 用法

```bash
$ docker network create [OPTIONS] NETWORK
```

##### 描述

- 默认创建 `bridge`网络，可以使用`--driver`选项指定`bridge`、`overlay`以及第三方网络驱动。

- 安装Docker Engine后会自动创建一个`bridge`网络，即`docker0`网桥。

- 所有新建容器默认自动连接`docker0`。

- 该网桥不可删除，但可以通过`network create`创建新网桥。

```bash
$ docker network create -d bridge my-bridge-network
```

- 网桥网络适用于单引擎单主机的情况。

- 多主机运行Docker Engine需要使用`overlay`网络，该网络需要预置条件如下：
  
  - 可以使用键值存储。引擎支持Consul、Etcd和ZooKeeper；
  
  - 主机集群与键值存储连接；
  
  - 在集群中正确配置引擎`daemon`；

- `dockerd`选项支持的`overlay`网络如下：
  
  - `--cluster-store`
  
  - `--cluster-store-opt`
  
  - `--cluster-advertise`

- 推荐使用Docker Swarm管理集群构建网络，在满足`overlay`网络前置条件后，在任意集群下执行以下命令即可创建网络：

```bash
$ docker network create -d overlay my-multihost-network
```

### Overlay 网络的限制

- `overlay`网络应当使用默认的 `/24`作为子网掩码，虽然这会限制IP个数为256个。

- 使用超过256个IP地址时，



You should create overlay networks with `/24` blocks (the default), which limits you to 256 IP addresses, when you create networks using the default VIP-based endpoint-mode. This recommendation addresses [limitations with swarm mode](https://github.com/moby/moby/issues/30820). If you need more than 256 IP addresses, do not increase the IP block size. You can either use `dnsrr` endpoint mode with an external load balancer, or use multiple smaller overlay networks. See [Configure service discovery](https://docs.docker.com/engine/swarm/networking/#configure-service-discovery) for more information about different endpoint modes.

For example uses of this command, refer to the [examples section](https://docs.docker.com/engine/reference/commandline/network_create/#examples) below.

## Options[](https://docs.docker.com/engine/reference/commandline/network_create/#options)

| Name, shorthand   | Default  | Description                                             |
| ----------------- | -------- | ------------------------------------------------------- |
| `--attachable`    |          | Enable manual container attachment                      |
| `--aux-address`   |          | Auxiliary IPv4 or IPv6 addresses used by Network driver |
| `--config-from`   |          | The network from which to copy the configuration        |
| `--config-only`   |          | Create a configuration only network                     |
| `--driver` , `-d` | `bridge` | Driver to manage the Network                            |
| `--gateway`       |          | IPv4 or IPv6 Gateway for the master subnet              |
| `--ingress`       |          | Create swarm routing-mesh network                       |
| `--internal`      |          | Restrict external access to the network                 |
| `--ip-range`      |          | Allocate container ip from a sub-range                  |
| `--ipam-driver`   |          | IP Address Management Driver                            |
| `--ipam-opt`      |          | Set IPAM driver specific options                        |
| `--ipv6`          |          | Enable IPv6 networking                                  |
| `--label`         |          | Set metadata on a network                               |
| `--opt` , `-o`    |          | Set driver specific options                             |
| `--scope`         |          | Control the network's scope                             |
| `--subnet`        |          | Subnet in CIDR format that represents a network segment |

## Examples[](https://docs.docker.com/engine/reference/commandline/network_create/#examples)

### Connect containers[](https://docs.docker.com/engine/reference/commandline/network_create/#connect-containers)

When you start a container, use the `--network` flag to connect it to a network. This example adds the `busybox` container to the `mynet` network:

```
$ docker run -itd --network=mynet busybox
```

If you want to add a container to a network after the container is already running, use the `docker network connect` subcommand.

You can connect multiple containers to the same network. Once connected, the containers can communicate using only another container’s IP address or name. For `overlay` networks or custom plugins that support multi-host connectivity, containers connected to the same multi-host network but launched from different Engines can also communicate in this way.

You can disconnect a container from a network using the `docker network disconnect` command.

### Specify advanced options[](https://docs.docker.com/engine/reference/commandline/network_create/#specify-advanced-options)

When you create a network, Engine creates a non-overlapping subnetwork for the network by default. This subnetwork is not a subdivision of an existing network. It is purely for ip-addressing purposes. You can override this default and specify subnetwork values directly using the `--subnet` option. On a `bridge` network you can only create a single subnet:

```
$ docker network create --driver=bridge --subnet=192.168.0.0/16 br0
```

Additionally, you also specify the `--gateway` `--ip-range` and `--aux-address` options.

```
$ docker network create \
  --driver=bridge \
  --subnet=172.28.0.0/16 \
  --ip-range=172.28.5.0/24 \
  --gateway=172.28.5.254 \
  br0
```

If you omit the `--gateway` flag the Engine selects one for you from inside a preferred pool. For `overlay` networks and for network driver plugins that support it you can create multiple subnetworks. This example uses two `/25` subnet mask to adhere to the current guidance of not having more than 256 IPs in a single overlay network. Each of the subnetworks has 126 usable addresses.

```
$ docker network create -d overlay \
  --subnet=192.168.10.0/25 \
  --subnet=192.168.20.0/25 \
  --gateway=192.168.10.100 \
  --gateway=192.168.20.100 \
  --aux-address="my-router=192.168.10.5" --aux-address="my-switch=192.168.10.6" \
  --aux-address="my-printer=192.168.20.5" --aux-address="my-nas=192.168.20.6" \
  my-multihost-network
```

Be sure that your subnetworks do not overlap. If they do, the network create fails and Engine returns an error.

### Bridge driver options[](https://docs.docker.com/engine/reference/commandline/network_create/#bridge-driver-options)

When creating a custom network, the default network driver (i.e. `bridge`) has additional options that can be passed. The following are those options and the equivalent docker daemon flags used for docker0 bridge:

| Option                                           | Equivalent  | Description                                           |
| ------------------------------------------------ | ----------- | ----------------------------------------------------- |
| `com.docker.network.bridge.name`                 | -           | Bridge name to be used when creating the Linux bridge |
| `com.docker.network.bridge.enable_ip_masquerade` | `--ip-masq` | Enable IP masquerading                                |
| `com.docker.network.bridge.enable_icc`           | `--icc`     | Enable or Disable Inter Container Connectivity        |
| `com.docker.network.bridge.host_binding_ipv4`    | `--ip`      | Default IP when binding container ports               |
| `com.docker.network.driver.mtu`                  | `--mtu`     | Set the containers network MTU                        |
| `com.docker.network.container_iface_prefix`      | -           | Set a custom prefix for container interfaces          |

The following arguments can be passed to `docker network create` for any network driver, again with their approximate equivalents to `docker daemon`.

| Argument     | Equivalent     | Description                                |
| ------------ | -------------- | ------------------------------------------ |
| `--gateway`  | -              | IPv4 or IPv6 Gateway for the master subnet |
| `--ip-range` | `--fixed-cidr` | Allocate IPs from a range                  |
| `--internal` | -              | Restrict external access to the network    |
| `--ipv6`     | `--ipv6`       | Enable IPv6 networking                     |
| `--subnet`   | `--bip`        | Subnet for network                         |

For example, let’s use `-o` or `--opt` options to specify an IP address binding when publishing ports:

```
$ docker network create \
    -o "com.docker.network.bridge.host_binding_ipv4"="172.19.0.1" \
    simple-network
```

### Network internal mode[](https://docs.docker.com/engine/reference/commandline/network_create/#network-internal-mode)

By default, when you connect a container to an `overlay` network, Docker also connects a bridge network to it to provide external connectivity. If you want to create an externally isolated `overlay` network, you can specify the `--internal` option.

### Network ingress mode[](https://docs.docker.com/engine/reference/commandline/network_create/#network-ingress-mode)

You can create the network which will be used to provide the routing-mesh in the swarm cluster. You do so by specifying `--ingress` when creating the network. Only one ingress network can be created at the time. The network can be removed only if no services depend on it. Any option available when creating an overlay network is also available when creating the ingress network, besides the `--attachable` option.

```
$ docker network create -d overlay \
  --subnet=10.11.0.0/16 \
  --ingress \
  --opt com.docker.network.driver.mtu=9216 \
  --opt encrypted=true \
  my-ingress-network
```

### 镜像操作

##### 1.docker pull：从仓库获取

```bash
# docker pull [选项] [Docker Registry 地址[:端口]/]仓库名[:标签]
docker pull ubuntu:16.04
```

- Docker 镜像仓库地址的格式一般是 <域名/IP>[:端口号]，默认地址是 Docker Hub。

- 仓库名是两段式名称，即 <用户名>/<软件名>，默认为 library，也就是官方镜像。

##### 2.docker image ls：列出镜像

- `docker image ls`列表包含了**仓库名、标签、镜像 ID、创建时间以及所占用的空间**。

```bash
# docker image ls [OPTIONS] [REPOSITORY[:TAG]]
# Options:
#   -a, --all             显示所有镜像 (默认隐藏中间镜像)
#       --digests         显示摘要
#   -f, --filter filter   根据给定条件过滤输出
#   -q, --quiet           只显示镜像的ID
```

##### 3.docker system df：显示所有镜像大小

- Docker Hub 中显示的体积是压缩后的体积。而`docker image df`显示的是镜像展开后的各层所占空间的总和。

### 及显示镜像大小   docker system df

- `docker image ls`列表包含了**仓库名、标签、镜像 ID、创建时间以及所占用的空间**。

-  Docker Hub 中显示的体积是压缩后的体积。而`docker image ls`显示的是镜像展开后的各层所占空间的总和。

```bash
docker image ls
docker system df
```

# Docker File

# Docker 数据共享与持久化

# Docker网络

### 容器默认允许的功能

| Capability Key   | Capability Description                                                                                                        |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| AUDIT_WRITE      | Write records to kernel auditing log.                                                                                         |
| CHOWN            | Make arbitrary changes to file UIDs and GIDs (see chown(2)).                                                                  |
| DAC_OVERRIDE     | Bypass file read, write, and execute permission checks.                                                                       |
| FOWNER           | Bypass permission checks on operations that normally require the file system UID of the process to match the UID of the file. |
| FSETID           | Don’t clear set-user-ID and set-group-ID permission bits when a file is modified.                                             |
| KILL             | Bypass permission checks for sending signals.                                                                                 |
| MKNOD            | Create special files using mknod(2).                                                                                          |
| NET_BIND_SERVICE | Bind a socket to internet domain privileged ports (port numbers less than 1024).                                              |
| NET_RAW          | Use RAW and PACKET sockets.                                                                                                   |
| SETFCAP          | Set file capabilities.                                                                                                        |
| SETGID           | Make arbitrary manipulations of process GIDs and supplementary GID list.                                                      |
| SETPCAP          | Modify process capabilities.                                                                                                  |
| SETUID           | Make arbitrary manipulations of process UIDs.                                                                                 |
| SYS_CHROOT       | Use chroot(2), change root directory.                                                                                         |

### 容器可以添加的功能

| Capability Key     | Capability Description                                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| AUDIT_CONTROL      | Enable and disable kernel auditing; change auditing filter rules; retrieve auditing status and filtering rules.           |
| AUDIT_READ         | Allow reading the audit log via multicast netlink socket.                                                                 |
| BLOCK_SUSPEND      | Allow preventing system suspends.                                                                                         |
| BPF                | Allow creating BPF maps, loading BPF Type Format (BTF) data, retrieve JITed code of BPF programs, and more.               |
| CHECKPOINT_RESTORE | Allow checkpoint/restore related operations. Introduced in kernel 5.9.                                                    |
| DAC_READ_SEARCH    | Bypass file read permission checks and directory read and execute permission checks.                                      |
| IPC_LOCK           | Lock memory (mlock(2), mlockall(2), mmap(2), shmctl(2)).                                                                  |
| IPC_OWNER          | Bypass permission checks for operations on System V IPC objects.                                                          |
| LEASE              | Establish leases on arbitrary files (see fcntl(2)).                                                                       |
| LINUX_IMMUTABLE    | Set the FS_APPEND_FL and FS_IMMUTABLE_FL i-node flags.                                                                    |
| MAC_ADMIN          | Allow MAC configuration or state changes. Implemented for the Smack LSM.                                                  |
| MAC_OVERRIDE       | Override Mandatory Access Control (MAC). Implemented for the Smack Linux Security Module (LSM).                           |
| NET_ADMIN          | Perform various network-related operations.                                                                               |
| NET_BROADCAST      | Make socket broadcasts, and listen to multicasts.                                                                         |
| PERFMON            | Allow system performance and observability privileged operations using perf_events, i915_perf and other kernel subsystems |
| SYS_ADMIN          | Perform a range of system administration operations.                                                                      |
| SYS_BOOT           | Use reboot(2) and kexec_load(2), reboot and load a new kernel for later execution.                                        |
| SYS_MODULE         | Load and unload kernel modules.                                                                                           |
| SYS_NICE           | Raise process nice value (nice(2), setpriority(2)) and change the nice value for arbitrary processes.                     |
| SYS_PACCT          | Use acct(2), switch process accounting on or off.                                                                         |
| SYS_PTRACE         | Trace arbitrary processes using ptrace(2).                                                                                |
| SYS_RAWIO          | Perform I/O port operations (iopl(2) and ioperm(2)).                                                                      |
| SYS_RESOURCE       | Override resource Limits.                                                                                                 |
| SYS_TIME           | Set system clock (settimeofday(2), stime(2), adjtimex(2)); set real-time (hardware) clock.                                |
| SYS_TTY_CONFIG     | Use vhangup(2); employ various privileged ioctl(2) operations on virtual terminals.                                       |
| SYSLOG             | Perform privileged syslog(2) operations.                                                                                  |
| WAKE_ALARM         | Trigger something that will wake up the system.                                                                           |
