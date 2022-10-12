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
docker create        # 创建容器但不启动它。
docker rename        # 用于重命名容器。
docker run           # 一键创建并同时启动该容器。
docker rm            # 删除容器。
docker update        # 调整容器的资源限制。

docker run -td container_id         # -t 分配终端 -d 后台运行
docker run --rm                     # --rm 容器停止后删除
docker run -v $HOSTDIR:$DOCKERDIR   # 映射宿主机 (host) 的目录到 Docker 容器
docker rm -v                        # -v 删除容器的同时删除卷标
docker run --log-driver=syslog      # --log-driver指定日志引擎（容器间独立）

# 启动和停止
docker start                        # 启动已存在的容器。
docker stop                         # 停止运行中的容器。
docker restart                      # 重启容器。
docker pause                        # 暂停运行中的容器，将其「冻结」在当前状态。
docker unpause                      # 结束容器暂停状态。
docker wait                         # 阻塞地等待某个运行中的容器直到停止。
docker kill                         # 向运行中的容器发送 SIGKILL 指令。
docker attach                       # 连接到运行中的容器。

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
docker ps         # 查看运行中的所有容器。
docker logs       # 从容器中读取日志。（自定义日志驱动，如json-file和journald）。
docker inspect    # 查看某个容器的所有信息（包括 IP 地址）。
docker events     # 从容器中获取事件 (events)。
docker port       # 查看容器的公开端口。
docker top        # 查看容器中活动进程。
docker stats      # 查看容器的资源使用量统计信息。
docker diff       # 查看容器文件系统中存在改动的文件。

docker ps -a         # 将显示所有容器，包括运行中和已停止的。
docker stats --all   # 同样将显示所有容器，默认仅显示运行中的容器。

# 导入 / 导出
```
