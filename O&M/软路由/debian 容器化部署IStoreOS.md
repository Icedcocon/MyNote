# debain 12 容器化部署 IStoreOS

## 一、 镜像准备

### 1. 安装依赖

```bash
# 镜像处理
apt install qemu-utils 
# LXC
apt install lxc lxc-templates bridge-utils uidmap
# netplan
apt install netplan.io
```

### 1. 下载并安装 rootfs

```bash
# 创建路径
mkdir IStoreOS
cd IStoreOSm
# 下载镜像，附上arm镜像下载地址
# https://fw.koolcenter.com/iStoreOS/r5s/
wget https://fw0.koolcenter.com/iStoreOS/r5s/istoreos-22.03.6-2024120615-r5s-squashfs-combined.img.gz
# 重命名简化名称
mv istoreos*.img.gz istoreos_rk3566.img.gz
# 解压镜像
gunzip istoreos_rk3566.img.gz
# 创建挂载路径
mkdir /mnt/istoreos
# 加载NBD模块让磁盘之类的镜像可以映射到本地路径
modprobe nbd
# 挂载指定格式及镜像
qemu-nbd -c /dev/nbd0 -f raw  istoreos_rk3566.img
# 查看分区，并选择squashfs或btrfs的分区挂载
lsblk -f /dev/nbd0
mount /dev/nbd0p2 /mnt/istoreos/
# 打包为rootfs
cd /mnt/istoreos/
tar -cf /root/IStoreOS/istoreos.rootfs.tar *
# 后处理
cd 
umount /mnt/istoreos
qemu-nbd -d /dev/nbd0
```

## 二、incus方案

### 0 请观看

[【全网最全】OpenClash零基础入门教程 | openclash优缺点、网络设置、安装、内核更新与上传、基础设置，新手使用指南，openwrt软路由OpenClash从入门到精通系列教程之基础篇 - YouTube](https://www.youtube.com/watch?v=7wiu1YA8Pbc&list=PLSbqX2QvapHk7VYlbyHUIOonIl7q1n410)

### 1. 准备

#### 1.1 安装 incus

```bash
# 安装
apt install incus
# 查看源
incus remote list
# 添加国内源 其中 mirror 为地址名称，可自行指定
incus remote add mirror https://mirrors.bfsu.edu.cn/lxc-images/ --protocol=simplestreams --public
incus remote add mirror-images https://mirrors.tuna.tsinghua.edu.cn/lxc-images/ --protocol=simplestreams --public
incus remote add mirror-images https://mirrors.tuna.tsinghua.edu.cn/lxc-images/ --protocol=simplestreams --public
# 查看镜像
incus image list mirror:debian
incus image list mirror-images:openwrt
```

#### 1.2 配置网桥

> 网桥 IP 与 eth0 IP 不应相同

cat /etc/netplan/01-netcfg.yaml

```bash
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: false
      optional: true
      addresses: []
  bridges:
    br0:
      interfaces: [eth0]
      addresses: [192.168.2.2/24]
      routes:
        - to: default
          via: 192.168.2.1
          metric: 100
      nameservers:
        addresses: [1.1.1.1, 8.8.8.8]
```

#### 1.3 初始化 incus

```bash
root@NanoPC-T6:/etc/netplan# incus admin init
Would you like to use clustering? (yes/no) [default=no]:
Do you want to configure a new storage pool? (yes/no) [default=yes]:
Name of the new storage pool [default=default]:
Where should this storage pool store its data? [default=/var/lib/incus/storage-pools/default]:
Would you like to create a new local network bridge? (yes/no) [default=yes]: no
Would you like to use an existing bridge or host interface? (yes/no) [default=no]: yes
Name of the existing bridge or host interface: br0
Would you like the server to be available over the network? (yes/no) [default=no]: no
Would you like stale cached images to be updated automatically? (yes/no) [default=yes]:
Would you like a YAML "init" preseed to be printed? (yes/no) [default=no]:
```

#### 1.4 下载容器

```bash
# 创建容器
incus launch images:openwrt/23.05 openwrt -c security.privileged=true -c security.nesting=true
# 停止容器
incus stop openwrt
```

#### 1.5 覆盖文件系统

- 替换实例中的文件系统并重新启动容器
  
  - 在lxc默认在/var/lib/lxc/下新建openwrt文件夹
  - 在incus默认在/var/lib/incus/storage-pools/default/containers/下

```bash
# 覆盖实例中的文件系统
tar xvf rootfs.tar -C /var/lib/incus/storage-pools/default/containers/openwrt/rootfs/
# 如果有配置好的network
cp 
# 修改权限 无须
# chown -R 100000:100000 /var/lib/incus/storage-pools/default/containers/openwrt/rootfs/
# 启动容器
incus start openwrt
```

### 2. 进入 INCUS 容器修改配置

#### 2.1 关闭容器防火墙

```bash
# 进入容器
incus exec openwrt bash
# 关闭防火墙
/etc/init.d/firewall stop
/etc/init.d/firewall disable
```

#### 2.2 修改容器实例 `/etc/config/network` 配置文件内容

```yaml
config interface 'loopback'
        option device 'lo'
        option proto 'static'
        option ipaddr '127.0.0.1'
        option netmask '255.0.0.0'

config globals 'globals'
        option ula_prefix 'fda2:4244:30a1::/48'

config interface 'lan'
        option device 'eth0'
        option proto 'static'
        option ipaddr '192.168.2.10'
        option netmask '255.255.255.0'
        option ip6assign '60'
        option gateway '192.168.2.1'
        option dns '8.8.8.8 114.114.114.114'
```

#### 2.3 执行 `/etc/init.d/network restart` 重启网络

- 注意即使配置正确，重启网络后仍可能无法获取 IP ，此时需要手动重启黑豹X2
- 这里可以采用 reboot now 重启系统代替

#### 2.4 配置依赖

```bash
# 安装插件
opkg update
opkg install ca-certificates
# 需要配置
# opkg install luci-i18n-argon-config-zh-cn
# 不需要配置
opkg install luci-theme-argon

# 可选
opkg install luci-i18n-ttyd-zh-cn
opkg install luci-i18n-filebrowser-go-zh-cn
opkg install openssh-sftp-server
opkg install luci-i18n-samba4-zh-cn
# 安装iStore商店(ARM64 & x86-64通用)
wget -qO imm.sh https://cafe.cpolar.top/wkdaily/zero3/raw/branch/main/zero3/imm.sh && chmod +x imm.sh && ./imm.sh
# 安装网络向导和首页(ARM64 & x86-64通用)
is-opkg install luci-i18n-quickstart-zh-cn
```

#### 2.4 配置dnsmasq

- 修改配置文件
  
  - 

```bash
~ # cat /etc/config/dhcp

config dnsmasq
        .....
        option force '1'
        option resolvfile '/tmp/resolv.conf.d/resolv.conf.auto'
        option allservers '1'
        .....


~ # cat /tmp/resolv.conf.d/resolv.conf.auto
nameserver 8.8.8.8
nameserver 8.8.4.4
```

- 完全禁用 DNS 劫持

```bash
# 如果是 OpenClash
uci set openclash.config.enable=0
uci set openclash.config.dns_hijack='0'
uci commit openclash
/etc/init.d/openclash restart
```

- 废弃

```bash
# ubuntu 使用 resolvconf 控制域名解析文件
# apt install resolvconf
# 编辑 /etc/resolvconf/resolv.conf.d/head
# 结尾添加 nameserver 8.8.8.8
# 执行 `resolvconf -u`

# OpenWrt 防止 /etc/resolv.conf 被开机重置
# 配置域名解析
uci set dhcp.@dnsmasq[0].localuse="0"
uci commit dhcp
#重启dnsmasq
/etc/init.d/dnsmasq start
# 参考 https://wej.cc/142.html


# 或编辑 （没用）
#/etc/config/dhcp
#修改 list server
```

#### 2.5 插件

- `https://github.com/AUK9527/Are-u-ok`

#### 2.6 排错

```bash
iptables -P FORWARD ACCEPT
```

- OpenWrt 查看系统日志 `logread`

## 三、 docker 部署 ImmortalWRT 方案（与incus冲突）

### 0. 下载文件

```bash
mkdir ImmortalWrt
cd ImmortalWrt
# 下载
wget -O rootfs.tar.gz https://downloads.immortalwrt.org/releases/24.10.0-rc4/targets/armsr/armv8/immortalwrt-24.10.0-rc4-armsr-armv8-generic-squashfs-rootfs.img.gz
# 解压
gunzip rootfs.tar.gz
```

### 1. 安装docker及docker-compose

```bash
# 安装 docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh --mirror Aliyun
```

### 2. 配置编译docker镜像

```bash
# 切换工作路径
cd /root/ImmortalWrt/
# 创建Dockerfile
cat <<EOF >"Dockerfile"
FROM scratch
ADD rootfs.tar /
EOF
# 构建镜像
docker build -t immortalwrt .
```

### 3. 配置宿主机网络

#### 3.1 netplan

```bash
cat /etc/netplan/01-netcfg.yaml
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    eth0:
      dhcp4: false
      addresses:
        - 192.168.2.2/24
      routes:
        - to: 0.0.0.0/0
          via: 192.168.2.1
          metric: 100
      nameservers:
        addresses:
          - 8.8.8.8
          - 114.114.114.114
```

#### 3.2 macvlan

```bash
docker network create -d macvlan \
  --subnet=192.168.2.0/24 \
  --gateway=192.168.2.1 \
  -o parent=eth0 \
  macnet
# 检查是否创建成功
docker network ls
```

#### 3.3 创建macvlan子接口（在开启tailscale subnet时必须）

```bash
ip link add macvlan-shim link eth0 type macvlan mode bridge
ip addr add 192.168.2.3/24 dev macvlan-shim
ip link set macvlan-shim up
```

注意检查上述ip地址`192.168.66.2` 确保它没有被其他设备占用

- `macvlan-shim` 是虚拟接口的名称，你可以自定义。

- `192.168.2.3/24` 是给宿主机虚拟接口分配的 IP 地址，应位于 `192.168.2.0/24` 子网内，且不与宿主机网络（192.168.2.2）和其他设备冲突。

```bash
# 添加路由
ip route add 192.168.2.0/24 dev macvlan-shim
```

### 4. 启动容器并配置

#### 4.0 启动容器

```bash
# 启动容器
docker run --name immortalwrt \
  --restart always \
  -d \
  --network macnet \
  --ip 192.168.2.10 \
  --privileged \
  immortalwrt:latest /sbin/init
# 进入容器
docker exec -it immortalwrt bash
```

#### 4.1 配置网络

```bash
vim /etc/config/network
# 配置如下 cat /etc/config/network
config interface 'loopback'
        option device 'lo'
        option proto 'static'
        option ipaddr '127.0.0.1'
        option netmask '255.0.0.0'

config globals 'globals'
        option ula_prefix 'fda2:4244:30a1::/48'

config interface 'lan'
        option device 'eth0'
        option proto 'static'
        option ipaddr '192.168.2.10'
        option netmask '255.255.255.0'
        option ip6assign '60'
        option gateway '192.168.2.1'
        option dns '8.8.8.8 114.114.114.114'


# 重启网络
/etc/init.d/network restart
```

### 5. 安装依赖

```bash
# 安装插件
opkg update

opkg install luci-i18n-ttyd-zh-cn
opkg install luci-i18n-filebrowser-go-zh-cn
opkg install luci-i18n-argon-config-zh-cn
opkg install openssh-sftp-server
opkg install luci-i18n-samba4-zh-cn
# 安装iStore商店(ARM64 & x86-64通用)
wget -qO imm.sh https://cafe.cpolar.top/wkdaily/zero3/raw/branch/main/zero3/imm.sh && chmod +x imm.sh && ./imm.sh
# 安装网络向导和首页(ARM64 & x86-64通用)
is-opkg install luci-i18n-quickstart-zh-cn
```

#### 6. 保存镜像

```bash
docker commit immortalwrt immortalwrt:latest 
```

## 参考资料

https://www.bilibili.com/video/BV1fuc8eGEPa

[悟空的日常](https://wkdaily.cpolar.top/15)

[Linux 虚拟网卡技术：Macvlan &#183; 云原生实验室](https://icloudnative.io/posts/netwnetwork-virtualization-macvlan/)

[LXC容器：概念介绍及简单上手操作指导 - mini小新 - 博客园](https://www.cnblogs.com/onestarlearner/p/17605214.html)

[incus主体安装 | 一键虚拟化项目](https://www.spiritlhl.net/guide/incus/incus_install.html)
