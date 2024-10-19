# incus快速开始

## 一、incus主体安装

- 添加 apt 仓库并安装 incus

```bash
sudo -i
mkdir -p /etc/apt/keyrings/
curl -fsSL https://pkgs.zabbly.com/key.asc -o /etc/apt/keyrings/zabbly.asc
sh -c 'cat <<EOF > /etc/apt/sources.list.d/zabbly-incus-stable.sources
Enabled: yes
Types: deb
URIs: https://pkgs.zabbly.com/incus/stable
Suites: $(. /etc/os-release && echo ${VERSION_CODENAME})
Components: main
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/zabbly.asc

EOF'
apt-get update
apt-get install incus -y
incus -h
```

- 初始化 incus

```bash
incus admin init
```

> 注意：提示带auto的更新image的选项记得选no，避免更新占用系统

## 二、基本操作

### 0.  初始化及配置国内镜像源

- 初始化（仅执行一次）

- 添加国内镜像仓库（似乎与 LXC 通用）

```bash
# 列出可用仓库
incus remote list
# 添加国内仓库
incus remote add mirror https://mirrors.bfsu.edu.cn/lxc-images/ --protocol=simplestreams --public
```

- 列出可用镜像

```bash
# 默认仓库
incus image list images:debian
# 添加的国内仓库
incus image list mirror:ubuntu/20.04
```

### 1.

Incus是基于图像的，可以从不同的图像服务器加载图像。在本教程中，我们将使用 images： server。

这个Incus服务器目前是空的，你可以通过以下方式确保这一点：

```bash
incus list
```

使用 Ubuntu 20.04 映像启动名为“first”的容器：请注意，启动此容器需要几秒钟，因为必须先下载并解压缩映像

使用相同的映像启动名为“second”的容器：启动此容器比启动第一个容器更快，因为该映像已经可用。

```bash
incus launch images:ubuntu/20.04 first
incus launch images:ubuntu/20.04 second
```

将第一个容器复制到名为“third”的容器中：

```bash
incus copy first third
```

使用 Alpine Edge 映像启动名为“alpine”的容器：

```bash
incus launch images:alpine/edge alpine
```

使用 Debian 12 映像启动一个名为 “debian” 的虚拟机：

```bash
incus launch images:debian/12 debian --vm
```

您可以通过以下方式启动第三个实例：

```bash
incus start third
```

查询更多信息

```bash
incus info third
```

停止第二个实例：

```bash
incus stop second
```

删除第二个实例：

```bash
incus delete second
```

删除第三个实例：由于此实例正在运行，因此您会收到一条错误消息，指出必须先停止它。或者，您可以强制删除它：

```bash
incus delete third --force
```

启动一个容器并将其限制为一个 vCPU 和 192 MiB 的 RAM：

```bash
incus launch images:ubuntu/20.04 limited -c limits.cpu=1 -c limits.memory=192MiB
```

检查当前配置并将其与第一个（无限制）实例的配置进行比较：

```bash
incus config show limited
incus config show first
```

检查父系统和两个实例上的可用内存量和已用内存量：请注意，父系统和第一个实例的内存总量相同，因为默认情况下，容器从其父环境继承资源。另一方面，有限的实例只有 192 MiB 可用。

```bash
free -m
incus exec first -- free -m
incus exec limited -- free -m
```

检查父系统和两个实例上可用的 CPU 数量：同样，请注意，父系统和第一个实例的 CPU 数量相同，但受限实例的数量会减少。

```bash
nproc
incus exec first -- nproc
incus exec limited -- nproc
```

您还可以在实例运行时更新配置。

为您的实例配置内存限制：

```bash
incus config set limited limits.memory=128MiB
# 检查是否已应用配置及实例可用的内存量：
incus config show limited
incus exec limited -- free -m
```

在实例中启动交互式 shell：

```bash
incus exec first -- bash
```

您可以从实例访问文件并与之交互。

从实例中提取文件：

```bash
incus file pull first/etc/hosts .
```

向文件添加条目：

```bash
echo "1.2.3.4 my-example" >> hosts
```

将文件推送回实例： 

```bash
incus file push hosts first/etc/hosts
```

使用相同的机制访问日志文件：

```bash
incus file pull first/var/log/syslog - | less
```

Incus支持创建和恢复实例快照。

1. Create a snapshot called "clean":  
   创建一个名为“clean”的快照：
   
   incus snapshot create first clean

2. Confirm that the snapshot has been created:  
   确认已创建快照：
   
   incus snapshot list first

3. Break the instance:  中断实例：
   
   incus exec first -- rm -Rf /etc /usr

4. Confirm the breakage:
   
   incus exec first -- bash
   
   Note that you do not get a shell, because you deleted the `bash` command.  
   确认破损：请注意，您没有获得 shell，因为您删除了该 `bash` 命令。

5. Restore the instance to the snapshotted state:  
   将实例恢复到快照状态：
   
   incus snapshot restore first clean

6. Confirm that everything is back to normal:  
   确认一切恢复正常：
   
   incus exec first -- bash
   exit

7. Delete the snapshot:  删除快照：
   
   incus snapshot delete first clean

## 参考资料

- 一键虚拟化项目

[incus主体安装 | 一键虚拟化项目](https://www.spiritlhl.net/guide/incus/incus_install.html)

- 基本操作

https://silverl.me/posts/hello-incus/

- lxc安装windows11

https://blog.awin.one/posts/2024/lxc-%E5%AE%89%E8%A3%9D-windows-11%E4%B8%A6%E5%88%86%E4%BA%AB-i915-%E5%85%A7%E9%A1%AF/
