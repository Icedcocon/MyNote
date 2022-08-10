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

- starting 运行状态
- Exited 退出状态
- Paused 暂停状态
- healthy 健康状态
- unhealthy 非健康状态

# Docker操作

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

### 容器操作

##### docker run：建立并运行容器

```bash
# docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
# Options:
#   -a, --attach list        指定标准输入输出类型 STDIN/STDOUT/STDERR。
docker run -a stdin -a stdout -i -t ubuntu /bin/bash
#       --cidfile string     将容器ID写入该文件
#   -d, --detach             后台运行容器并输出容器ID
docker run -d nginx /bin/bash -c "while true; do echo 'He80llo world'; done"
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
#       --pid string         PID namespace to use
#       --privileged         Give extended privileges to this container
#   -p, --publish list       Publish a container's port(s) to the host
#   -P, --publish-all        Publish all exposed ports to random ports
#       --read-only          Mount the container's root filesystem as read only
#       --restart string     Restart policy to apply when a container exits (default "no")
#       --rm                 Automatically remove the container when it exits
#       --tmpfs list         Mount a tmpfs directory
#   -t, --tty                Allocate a pseudo-TTY
#   -u, --user string        Username or UID (format: <name|uid>[:<group|gid>])
#       --userns string      User namespace to use
#       --uts string         UTS namespace to use
#   -v, --volume list        Bind mount a volume
#       --volumes-from list  Mount volumes from the specified container(s)
#   -w, --workdir string     Working directory inside the containerrivate)


docker run -it --rm ubuntu:16.04 /bin/bash
# -i：交互式操作，让容器的标准输入保持打开。
# -t 让Docker分配一个伪终端（pseudo-tty）并绑定到容器的标准输入上
#--rm：这个参数是说容器退出后随之将其删除。默认情况下，为了排障需求，退出的容器并不会立即删除，除非手动 docker rm。我们这里只是随便执行个命令，看看结果，不需要排障和保留结果，因此使用--rm可以避免浪费空间。
# ubuntu:16.04：这是指用 ubuntu:16.04 镜像为基础来启动容器。
#bash：放在镜像名后的是命令，这里我们希望有个交互式 Shell，因此用的是 bash。
docker run ubuntu:16.04 /bin/echo 'Hello world'
```

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

发布端口和链接到其他容器仅适用于默认（网桥）。链接功能是一项遗留功能。您应该始终更喜欢使用 Docker 网络驱动程序而不是链接。

默认情况下，您的容器将使用与主机相同的 DNS 服务器，但您可以使用`--dns`.

默认情况下，MAC 地址是使用分配给容器的 IP 地址生成的。您可以通过`--mac-address`参数（格式：）提供 MAC 地址来显式设置容器的 MAC 地址。`12:34:56:78:9a:bc`请注意，Docker 不会检查手动指定的 MAC 地址是否唯一。

| Network                  | Description                                                                              |
| ------------------------ | ---------------------------------------------------------------------------------------- |
| **none**                 | No networking in the container.                                                          |
| **bridge** (default)     | Connect the container to the bridge via veth interfaces.                                 |
| **host**                 | Use the host's network stack inside the container.                                       |
| **container**:<name\|id> | Use the network stack of another container, specified via its *name* or *id*.            |
| **NETWORK**              | Connects the container to a user created network (using `docker network create` command) |

#### 网络：无

有了网络，`none`容器将无法访问任何外部路由。容器仍将 `loopback`在容器中启用一个接口，但它没有任何通往外部流量的路由。

#### 网桥

将网络设置为`bridge`容器将使用 docker 的默认网络设置。在主机上设置了一个桥，通常命名为 ，并且将为容器创建`docker0`一对接口。`veth`该对的一侧`veth`将保留在连接到网桥的主机上，而另一侧将放置在容器的命名空间内，除了`loopback`接口。将为网桥网络上的容器分配一个 IP 地址，并且流量将通过此网桥路由到容器。

默认情况下，容器可以通过其 IP 地址进行通信。要通过名称进行通信，它们必须被链接。

#### 网络：主机

将网络设置为`host`容器将共享主机的网络堆栈，并且来自主机的所有接口都将可用于容器。容器的主机名将与主机系统上的主机名匹配。注意`--mac-address`在网络模式下无效`host`。即使在`host` 网络模式下，默认情况下容器也有自己的 UTS 命名空间。因此， `--hostname`在网络模式下`--domainname`是允许的，`host`并且只会更改容器内的主机名和域名。与 类似`--hostname`，`--add-host`、`--dns`、`--dns-search`和 `--dns-option`选项可用于`host`网络模式。这些选项更新 `/etc/hosts`或`/etc/resolv.conf`在容器内。`/etc/hosts`主机上和主机上均未进行任何更改 `/etc/resolv.conf`。

与默认`bridge`模式相比，该`host`模式提供了*显着* 更好的网络性能，因为它使用主机的本机网络堆栈，而网桥必须通过 docker 守护进程经过一层虚拟化。当容器的网络性能至关重要时，建议在此模式下运行容器，例如生产负载均衡器或高性能 Web 服务器。

`--network="host"`使容器可以完全访问本地系统服务，例如 D-bus，因此被认为是不安全的。

#### 网络：容器

将网络设置为`container`一个容器将共享另一个容器的网络堆栈。其他容器的名称必须以`--network container:<name|id>`. 注意`--add-host` `--hostname` `--dns` `--dns-search` `--dns-option`and在 netmode`--mac-address`中无效，在`container`netmode`--publish` `--publish-all` `--expose`中也无效`container`。

运行 Redis 容器并绑定 Redis 的示例，`localhost`然后运行`redis-cli`命令并通过接口连接到 Redis 服务器 `localhost`。

```bash
$ docker run -d --name redis example/redis --bind 127.0.0.1
$ # use the redis container's network stack to access localhost
$ docker run --rm -it --network container:redis example/redis-cli -h 127.0.0.1
```

#### 用户自定义网络

您可以使用 Docker 网络驱动程序或外部网络驱动程序插件创建网络。您可以将多个容器连接到同一个网络。一旦连接到用户定义的网络，容器就可以仅使用另一个容器的 IP 地址或名称轻松通信。

对于`overlay`支持多主机连接的网络或自定义插件，连接到同一个多主机网络但从不同引擎启动的容器也可以通过这种方式进行通信。

以下示例使用内置`bridge`网络驱动程序创建网络并在创建的网络中运行容器

```
$ docker network create -d bridge my-net
$ docker run --network=my-net -itd --name=container3 busybox
```
