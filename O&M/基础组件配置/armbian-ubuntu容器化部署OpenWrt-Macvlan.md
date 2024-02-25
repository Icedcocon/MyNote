# armbian-ubuntu容器化部署OpenWrt-macvlan

## 一、armbian 容器化部署OpenWrt

### 1. 下载 docker 和 docker-compose

- Step 1:  更新您的系统软件包列表。

```bash
apt update 
```

- Step 2:  使用 Aliyun 镜像源下载并安装 docker-ce。

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh --mirror Aliyun
```

- Step 3: 安装 docker-compose

```bash
apt install -y docker-compose
```

### 2. 配置网络

- Step 4:  开启网卡混杂模式

```bash
ip a  # 查看网卡名称
ip link set end0 promisc on
# ip link set <interface> promisc off
```

- Step 5: 创建并配置MACVLAN
  - `--subnet` 为需要监听的子网，设置为与路由器网段一致
  - `--gateway` 设置为路由器 IP

```bash
docker network create -d macvlan \
                      --subnet=192.168.124.0/24 \
                      --gateway=192.168.124.1 \
                      -o parent=end0 \
                      openwrt_network
```

### 3. 配置并运行 openwrt 镜像

- Step 6:  拉取 OpenWrt 镜像

```bash
docker pull registry.cn-shanghai.aliyuncs.com/suling/openwrt:armv8
#docker pull registry.cn-shanghai.aliyuncs.com/suling/openwrt:x86_64
```

- Step 7:  运行 OpenWrt 镜像

```bash
docker run --restart always --name openwrt -d \
            --network openwrt_network --privileged \
            --ip 192.168.124.110  \
            -v /root/OpenWrt/network:/etc/config/network \
            -v /root/OpenWrt/core:/etc/openclash/core \
            registry.cn-shanghai.aliyuncs.com/suling/openwrt:armv8 \
            /sbin/init
```

- 默认用户名 root； 默认密码 password

- `/etc/config/network` 配置文件内容

```yaml
config interface 'loopback'
    option ifname 'lo'
    option proto 'static'
    option ipaddr '127.0.0.1'
    option netmask '255.0.0.0'

config interface 'lan'
    option type 'bridge'
    option ifname 'eth0'
    option proto 'static'
    option netmask '255.255.255.0'
    option ip6assign '60'
    option ipaddr '192.168.124.111'
    option gateway '192.168.124.1'
    option dns '8.8.8.8'

config interface 'wan6'
    option ifname 'eth0'
    option proto 'dhcpv6'
###########################################
config interface 'loopback'
        option ifname 'lo'
        option proto 'static'
        option ipaddr '127.0.0.1'
        option netmask '255.0.0.0'

config globals 'globals'
        option packet_steering '1'

config interface 'lan'
        option type 'bridge'
        option ifname 'eth0'
        option proto 'static'
        option netmask '255.255.255.0'
        option ip6assign '60'
        option ipaddr '192.168.124.110'
        option gateway '192.168.124.1'
        option dns '192.168.124.1'

config interface 'vpn0'
        option ifname 'tun0'
        option proto 'none'
```

### 4. clash内核故障处理

```bash
# 进入内核安装目录
cd /etc/openclash/core/ 
# 下载内核安装包
wget https://down.clash.la/Clash/Core/Releases/clash-linux-armv7-v1.18.0.gz
#wget https://down.clash.la/Clash/Core/Releases/clash-linux-amd64-v3-v1.18.0.gzhttps://down.clash.la/Clash/Core/Releases/clash-linux-amd64-v3-v1.18.0.gz
# 解压内核安装包
tar -zxvf clash-linux-armv7-v1.18.0.gz
# 给予最高权限
chmod 777 clash
```

## 二、 LXD 部署最新 OpenWrt

### 0. 安装依赖

```bash
# ubuntu安装依赖
# curl -fsSL https://get.docker.com -o get-docker.sh
# sh get-docker.sh --mirror Aliyun
# snap install lxc lxd
# Armbian 安装
apt install -y lxc lxd-client lxd qemu-utils bridge-utils
```

### 1. 下载OpenWrt镜像并打包为rootfs

```bash
# 下载镜像，附上arm镜像下载地址
# https://fw.koolcenter.com/iStoreOS/r5s/
wget https://fw0.koolcenter.com/iStoreOS/r5s/istoreos-22.03.6-2024022310-r5s-squashfs-combined.img.gz
# 重命名简化名称
mv istoreos*.img.gz istoreos_rk3566.img.gz
# 解压镜像
gunzip istoreos_rk3566.img.gz
# 创建挂载路径
mkdir /mnt/openwrt
# 加载NBD模块让磁盘之类的镜像可以映射到本地路径
modprobe nbd
# 挂载指定格式及镜像
qemu-nbd -c /dev/nbd0 -f raw  istoreos_rk3566.img
# 查看分区，并选择squashfs或btrfs的分区挂载
lsblk -f /dev/nbd0
mount /dev/nbd0p2 /mnt/openwrt/
# 打包为rootfs
cd /mnt/openwrt/
tar -czf /root/openwrt.rootfs.tar.gz *
# 后处理
cd 
umount /mnt/openwrt
qemu-nbd -d /dev/nbd0
```

### 2. 将宿主机网络配置为网桥

- 编辑 `/etc/network/interfaces`

```bash
source /etc/network/interfaces.d/*
# Network is managed by Network manager
auto lo
iface lo inet loopback

# bridge interface
auto br0
iface br0 inet static
    address 192.168.0.111/24
    gateway 192.168.0.1
    bridge_ports end0
    bridge_stp off
    bridge_fd 0
    bridge_maxwait 0
    bridge_waitport 0
    dns-nameservers 1.1.1.1 8.8.8.8
```

- 执行 `systemctl restart networking.service`

### 3. 初始化 LXD 网络

- 初始化

```bash
root@NanoPC-T6:~# lxd init
Would you like to use LXD clustering? (yes/no) [default=no]:
Do you want to configure a new storage pool? (yes/no) [default=yes]:
Name of the new storage pool [default=default]:
Name of the storage backend to use (btrfs, ceph, dir, lvm) [default=btrfs]:
Create a new BTRFS pool? (yes/no) [default=yes]:
Would you like to use an existing empty block device (e.g. a disk or partition)? (yes/no) [default=no]:
Size in GiB of the new loop device (1GiB minimum) [default=10GiB]:
Would you like to connect to a MAAS server? (yes/no) [default=no]:
Would you like to create a new local network bridge? (yes/no) [default=yes]: no
Would you like to configure LXD to use an existing bridge or host interface? (yes/no) [default=no]: yes
Name of the existing bridge or host interface: br0
Would you like the LXD server to be available over the network? (yes/no) [default=no]:
Would you like stale cached images to be updated automatically? (yes/no) [default=yes]:
Would you like a YAML "lxd init" preseed to be printed? (yes/no) [default=no]:
```

### 4. 拉取 LXD 容器作为模板并替换文件系统

- (1) 添加镜像源

```bash
lxc remote add mirror-images https://mirrors.tuna.tsinghua.edu.cn/lxc-images/ --protocol=simplestreams --public
```

- (2) 列出可用 OpenWrt 镜像并创建实例

```bash
# 使用默认镜像源
# lxc image list images:openwrt
# 使用清华镜像源
lxc image list mirror-images:openwrt
# 创建容器
lxc launch mirror-images:openwrt/22.03 openwrt 
# 停止容器
lxc stop openwrt
```

- (3) 替换实例中的文件系统并重新启动容器
  
  - 在lxc默认在/var/lib/lxc/下新建openwrt文件夹
  - 在lxd默认在/var/lib/lxd/storage-pools/default/containers/下

```bash
# 覆盖实例中的文件系统
tar zxvf openwrt.rootfs.tar.gz -C /var/lib/lxd/storage-pools/default/containers/openwrt/rootfs

# 启动容器
lxc start openwrt
```

### 4. 进入 LXD 容器修改配置

- (0) 进入容器

```bash
lxc exec openwrt bash
```

- (1) 修改容器实例 `/etc/config/network` 配置文件内容

```yaml
config interface 'loopback'
    option ifname 'lo'
    option proto 'static'
    option ipaddr '127.0.0.1'
    option netmask '255.0.0.0'

config interface 'lan'
    option type 'bridge'
    option ifname 'eth0'
    option proto 'static'
    option netmask '255.255.255.0'
    option ip6assign '60'
    option ipaddr '192.168.124.111'
    option gateway '192.168.124.1'
    option dns '8.8.8.8'

config interface 'wan6'
    option ifname 'eth0'
    option proto 'dhcpv6'
```

- (2) 执行 `systemctl restart networking.service` 重启网络
  
  - 注意即使配置正确，重启网络后仍可能无法获取 IP ，此时需要手动重启黑豹X2
  - 这里可以采用 reboot now 重启系统代替

- (3) 关闭容器实例防火墙

```bash
/etc/init.d/firewall disable
/etc/init.d/firewall stop
```

- (4) 配置域名解析

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
```

- (5) 插件
  
  - `https://github.com/AUK9527/Are-u-ok`

- (6) 排错
  
  - OpenWrt 查看系统日志 `logread`

### 参考资料

[PVE里用LXC容器部署OpenWrt | Zen of hacking](https://zenofhacking.com/zh/posts/openwrt-from-kvm-to-lxc/)

https://www.cnblogs.com/tianpanyu/p/16012594.html

https://molezz.net/n1-debian-ubuntu-lxc-openwrt

https://openwares.net/2019/06/03/lxd-containers-bridged-host-network/

## ubuntu(x86)-宿主机部署yacd (不推荐)

### 1. 下载 Clash 及配置

- 下载clash
  - `https://github.com/Dreamacro/clash/releases`

```bash
cd && mkdir clash  # 在用户目录下创建 clash 文件夹
# 访问 https://github.com/Dreamacro/clash/releases 获取最新二进制文件
wget https://down.clash.la/Clash/Core/Releases/clash-linux-armv7-v1.18.0.gz
gzip -d  clash-linux-armv7-v1.18.0.gz
mv clash* /clash/clash
cd clash
# 下载配置文件
wget -O config.yaml https://****
chmod +x clash
cd ..
mv clash /usr/local/bin/
```

- 配置 config.yaml

```bash
port: 7890
socks-port: 7891
allow-lan: true
mode: Rule
log-level: info
secert: 123456 #  clash dashboard 密码
# external-ui: dashboard # UI程序，容器不需要
external-controller: 0.0.0.0:9090 # dashboard 访问的端口
```

- 配置 clash 服务
  - `vim /etc/systemd/system/clash.service`
  - `systemctl start clash.service`
  - `systemctl enable clash.service`
  - stop 后可能会断连数分钟

```bash
[Unit]
Description=clash service
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/clash/clash -d /usr/local/bin/clash
ExecStop=/usr/bin/killall frpc
Restart=always

[Install]
WantedBy=multi-user.target
```

### 2. 下载yacd clashboard

- 下载 yacd
  
  - `https://github.com/haishanh/yacd`
  
  - `https://hub.docker.com/r/haishanh/yacd`

```bash
docker run -p 10081:80 -d --name dashboard --restart=always ghcr.io/haishanh/yacd:master
```

### 3. 配置系统代理

- `vim /etc/bash.bashrc`

```bash
proxy_on() {
    export https_proxy=http://127.0.0.1:7890
    export http_proxy=http://127.0.0.1:7890
    export all_proxy=socks5://127.0.0.1:7891
    export no_proxy="localhost,127.0.0.1,::1"
    #echo 'Acquire::http::Proxy "http://127.0.0.1:7890"'  >  /etc/apt/apt.conf
    #echo 'Acquire::https::Proxy "http://127.0.0.1:7890"' >> /etc/apt/apt.conf
    echo "HTTP/HTTPS Proxy on"
}

# Close proxy
proxy_off() {
    unset http_proxy
    unset https_proxy
    unset all_proxy
    unset no_proxy
    echo "HTTP/HTTPS Proxy off"
}
```

## 参考资料

https://github.com/SuLingGG/OpenWrt-Docker

https://github.com/immortalwrt/immortalwrt/tree/openwrt-18.06-k5.4

https://www.2280129.xyz/article/000050/docker-openwrt.html

https://www.clash.la/archives/755/
