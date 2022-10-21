```bash
#########################################################################
# 系统环境
#########################################################################
docker version --format '{{.Server.Version}}'    # 查看运行的 Docker 版本
docker version --format '{{json .}}'             # 输出原始的 JSON 数据
```

```bash
#########################################################################
# 容器(Container)
#########################################################################

# 生命周期
# (1) docker create : 创建容器但不启动它。
docker container create -it --name demo alpine # -i 开标准输入; -t 开终端 
docker container start --attach -i demo          # 启动容器
docker create -v /data --name data ubuntu        # 创建容器的同时创建volume
docker run --rm --volumes-from data ubuntu       # 将volume挂载到容器
docker create -v /etc/cfg:/cfg --name cfg ubuntu # 创建本地映射的volume
docker run --rm --volumes-from cfg ubuntu        # 将volume挂载到容器
# (2) docker run    : 一键创建并同时启动该容器，等同于create并start。
docker run -it --name demo alpine                # -i 开标准输入; -t 开终端
docker run -d ubuntu /bin/bash -c \
"while true; do echo 'Hello world'; done"        # -d 后台运行容器
docker run -e "V1=val" -e V2="val" --rm ubuntu   # -e 设置容器内环境变量
docker run -d --expose 80 -P nginx               # --expose 指定端口 -P 暴露
docker run -it -h admin nginx /bin/bash          # -h 指定容器hostname
docker run --name demo -it nginx /bin/bash       # --name 指定容器名称
docker run --network none nginx                  # --network 指定网络种类
docker run -d -p 127.0.0.1:3306:3306 --rm mysql  # -p 指定端口映射
docker run --restart=on-failure:10 nginx         # --restart 容器重启策略
docker run -v $HOSTDIR:$DOCKERDIR   # 映射宿主机 (host) 的目录到 Docker 容器
docker rm -v                        # -v 删除容器的同时删除卷标
docker run --log-driver=syslog      # --log-driver指定日志引擎（容器间独立）
# (3) docker rename : 用于重命名容器。
docker rename old_name new_name                  # 重命名容器
# (4) docker rm     : 删除容器。
docker rm --force container                      # 强制删除运行中容器
# (5) docker update : 调整容器的资源限制。详见资源控制
docker update --cpu-shares 512 container         # 只能使用50%的cpu

# 启动和停止
# (1) docker start   : 启动已存在的容器。
docker container create -it --name demo alpine
docker container start --attach -i demo         # 启动容器
# (2) docker stop    : 停止运行中的容器。
docker stop -t 10 container                     # 10s后关闭容器 
# (3) docker restart : 重启容器。
docker restart container 
# (4) docker pause   : 暂停运行中的容器，将其「冻结」在当前状态。
docker pause container
# (5) docker unpause : 结束容器暂停状态。
docker pause container  
# (6) docker wait    : 阻塞地等待某个运行中的容器直到停止。
docker wait container  
# (7) docker kill    : 向运行中的容器发送 SIGKILL 指令。
docker kill --signal=SIGHUP container
docker kill --signal=HUP container
docker kill --signal=1 container
# (8) docker attach  : 连接到运行中的容器。
docker attach container  

# CPU限制：
# --cpu-shares 1024 表示100%CPU
docker run -ti --c 512 agileek/cpuset-test # 容器使用所有 CPU 内核的 50%
# --cpuset-cpus 可使用特定 CPU 内核；Docker 在容器内仍然能够 看到 全部 CPU
docker run -ti --cpuset-cpus=0,4,6 agileek/cpuset-test
# 内存限制：
docker run -it -m 300M ubuntu:14.04 /bin/bash
# 能力(Capabilities):
# 挂载基于 FUSE 的文件系统
docker run --rm -it --cap-add SYS_ADMIN --device /dev/fuse sshfs 
# 授予对某个设备的访问权限
docker run -it --device=/dev/ttyUSB0 debian bash
# 授予对所有设备的访问权限
docker run -it --privileged -v /dev/bus/usb:/dev/bus/usb debian bash

# 信息
docker ps -a      # 查看运行中的所有容器, -a 包括已停止。
docker logs       # 从容器中读取日志。（自定义日志驱动，如json-file和journald）。
docker inspect    # 查看某个容器的所有信息（包括 IP 地址）。
docker events     # 从容器中获取事件 (events)。
docker port       # 查看容器的公开端口。
docker top        # 查看容器中活动进程。
docker stats --all# 查看容器的资源使用量统计信息, --all 所有容器。
docker diff       # 查看容器文件系统中存在改动的文件。

# 导入 / 导出
docker cp                                         # 在容器和本地间复制文件
docker import                                     # 从标准输入中导入并生成容器
cat container.tar.gz | docker import - image:tag  # 从文件中导入容器镜像
docker export                                     # 将容器文件系统打包输出
docker export container | gzip > container.tar.gz # 打包输出至文件

# 执行命令
docker exec 在容器内执行命令。
```

```bash
#########################################################################
# 镜像(Images)
#########################################################################

# 生命周期
docker images                    # 查看所有镜像。
docker import                    # 从归档文件创建镜像。
docker build                     # 从 Dockerfile 创建镜像。
docker commit                    # 为容器创建镜像，如果容器正在运行则会临时暂停。
docker rmi                       # 删除镜像。
docker load                      # 从标准输入加载归档包作为镜像和标签。
docker load < image.tar.gz       # 从文件中加载镜像和标签。
docker save                      # 将镜像（父层、标签和版本）打包输出至标准输出。
docker save image:tag | gzip > image.tar.gz    # 打包至文件
# 其它信息
docker history         # 查看镜像的历史记录。
docker tag             # 给镜像打标签命名（本地或者仓库均可）。

# 清理
docker rmi             # 删除指定的镜像
docker image prune     # 删除未使用的镜像
```

```bash
#########################################################################
# 网络(Networks)
#########################################################################

# 生命周期
docker network create
docker network rm

# 其它信息
docker network ls
docker network inspect

# 建立连接
docker network connect
docker network disconnect

# 使用你自己的子网和网关创建一个桥接网络
docker network create --subnet 203.0.113.0/24 --gateway 203.0.113.254 iptastic

# 基于以上创建的网络，运行一个 Nginx 容器并指定 IP
$ docker run --rm -it --net iptastic --ip 203.0.113.2 nginx

# 在其他地方使用 CURL 访问这个 IP（假设该 IP 为公网）
$ curl 203.0.113.2
```
