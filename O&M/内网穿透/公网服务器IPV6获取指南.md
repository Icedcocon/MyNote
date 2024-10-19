# 公网服务器 IPV6 获取指南

## 一、 开启HE隧道

### 1. Hurricane Electric 介绍

- 国内云厂商的 IPV6 策略

国内包括腾讯、阿里等轻量云及弹性云服务器产品都不提供 IPv6 地址或提供地址但不提供 IPv6 网关转发支持。如阿里云 ECS，默认不支持 IPv6，但 IPv6 CIDR 分配、VPC、VNIC 绑定等均可顺利完成，唯独需配置（**购买**）IPv6 网关带宽才能开启完整的 IPv6 功能，此处不做评价。

- IPv6 隧道服务

HE（Hurricane Electric）的 IPv6 隧道服务（tunnelbroker），可以获得近乎无穷的 IPv6 地址的同时还建立了一条专用的跨洲隧道。

~~即使在 HE IP 大量被“认证”的今天，HE ipv6 tunnel 也是不可多得的优质免费服务，既可以访问外网，也可以用于内网穿透发布内网服务。本文介绍 HE 隧道的创建与 vps/主机配置和排错方法，操作系统为 Debian 12 bookworm，网络管理工具为 netplan。~~

### 2. 免费隧道提供商

除 HE 之外，尚有几家厂商或机构提供 IPv6 隧道服务。

通过 IPv6 隧道作用：

- 可以访问外网，充当梯子的角色（不专业/不推荐）

- 实现内网穿透，通过 IPv6 隧道发布内网服务。

**[HE（Hurricane Electric）](https://ipv6.he.net/)**

HE（Hurricane Electric，飓风电气）是著名的 Internet 基础设施提供商和全球最大的原生 IPv6 骨干网运营商。HE 提供的免费「[tunnelbroker](https://tunnelboker.net/)」IPv6 隧道服务，可以追溯到 2001 年。

**[August Internet](https://bgp.co/)**

August Internet 是一项非营利性计划，致力于支持不断增长的互联网社区，这些社区希望通过现实世界的 BGP 进行实验并获得实践经验。A.I. 的使命是为玩家建立一个更实用的社交环境，并鼓励年轻一代参与。August Internet 提供免费 BGP 隧道服务、RIPE PA/PI 分配、Internet 路由注册。但很不幸也很明确，某些目的地为中国的路由和流量会被丢弃。

[**Tunnelbroker.ch**](https://www.tunnelbroker.ch/)  **| [ip4market.ru](https://ip4market.ru/ru/) | [netassist.ua](https://netassist.ua/)**

分别来自德国、俄罗斯的隧道服务提供机构，均支持 v4tunnel 和 sit 隧道。

**[Oneclickvirt](https://github.com/oneclickvirt/6in4/blob/main/README_zh.md)**

托管于 github 的项目，一键式转发迁移 IPv6 网段。自建 sit、gre、ipip 协议的 IPv6 隧道，支持自定义要切分出来的 IPv6 子网大小，将自动计算出合适的 CIDR 格式的 IPv6 子网信息，自动识别服务端的 IPv6 子网大小。设置IPV6隧道的方法简单易懂，易于删除。

>  注意各类对等点信息及其服务商、服务方式，可通过 https://www.peeringdb.com/ 查询。

### 3. 注册账户、创建HE隧道

- (1) 完成注册后，点击左侧的『Create Regular Tunnel』即可创建隧道。

- (2) 填写计划作为端点的主机 IPv4 地址，HE Tunnelbroker 会进行检查其连通性
  
  - 如有问题可按照提示至主机管理后台放行 ICMP 入站。
  
  - 选择对端，国内用户切勿选择香港、日本和新加坡，受封锁环球旅行。
  
  - 国内主机可考虑选择阿什本、达拉斯节点，移动用户 HE 线路直连，非常稳定。

- (3) Peer 选定后点击『Create Tunnel』
  
  - 早期在一般情况下很快就会创建成功，当前国内很多 vps 会报 “network is restricted”错误，解决办法请参考后文。
  
  - 创建成功的 IPv6 隧道详细信息包括端点、前缀、DNS、rDNS 等内容。

- (4) 点击『Example Configurations』选项卡，根据主机选择相应的配置方式，拷贝配置内容，并按照提示操作。
  
  - 阿里云 vps debian 12 应选择『netplan 0.103+』，早期 debian/ubuntu 选择『Debian/Ubuntu』。

- (5) 将 HE 生成的配置拷贝后，登录主机，进入 /etc/netplan 目录，创建netplan yaml 配置文件。
  
  - 注意文件命名**确保最低优先级**，采用"99"开头。

```bash
cd /etc/netplan
nano 99-he-ipv6.yaml
```

- (6) 文件内容如下
  
  - 2001:::1 为远端 IPv6 地址
  
  - 2001:::2 为本地 IPv6 地址
  
  - remote、local 分别为远端和本地端的 IPv4 地址。
  
  - 类似国内 vps 、内网主机等设备，如创建隧道失败，需将 local 改为私网 IPv4 地址。

```yaml
network:
  version: 2
  tunnels:
    he-ipv6:
      mode: sit
      remote: 184.105.253.10
      local: 172.*.*.252
      addresses:
        - "2001:111::2/64"
      routes:
        - to: default
          via: "2001:111::1"
```

- (7) 配置文件创建完成后，运行 netplan apply 启用配置。
  
  - 运行 netplan apply 如出现警告 “Cannot call openvswitch: ovsdb-server.service is not running” 不影响实用，也可以使用以下命令安装 openvswitch-switch 解决。

```bash
apt install openvswitch-switch -y
```

应用配置后，使用 ip a 命令就可以看到 he-ipv6 和 sit 两个虚拟接口，也可以使用 ping 或 ping6 来进行网络检查。

### 4. 调试与应用

国内 vps/主机在创建与应用 HE 隧道过程中，可能会遇到的问题和对策如下：

- HE 检测不到端点：安全组、防火墙放行 vps 的入站、出站 icmp4 流量
- 网络严格、无法创建隧道：使用境外 vps/主机或其他可通过 HE 检查的 IPv4 地址创建隧道后，再修改隧道端点配置
- netplan报警：安装 openvswitch-switch 包
- 接口启动失败：vps 后台解绑已绑定 IPv6 地址、删除 IPv6 网关，ssh 登录后删除隧道，if up 重启启用激活：ifdown he-ipv6 && rm -f /etc/network/interfaces.d/he-ipv6
- 接口启动成功，但两端 ping 不通：修改配置文件中 local 为私有 IPv4 地址、放行 icmp6 入站和出站 echo reply 流量

最后一点，检查内核配置 sysctl.conf，确认IPv6 开启。可编辑 /etc/sysctl.conf 文件添加以下各项。

```bash
echo "net.ipv6.conf.all.disable_ipv6 = 0" >> /etc/sysctl.conf
echo "net.ipv6.conf.default.disable_ipv6 = 0" >> /etc/sysctl.conf
echo "net.ipv6.conf.lo.disable_ipv6 = 0" >> /etc/sysctl.conf
sysctl -p
```

在应用层面，本文示例中 IPv6 网络入口是 HE 达拉斯数据中心，因此需要注意如下要点：

- 内网穿透、发布内部服务，加速国外用户访问，可监听、使用 IPv6 接口/地址
- 本地用户访问外网，应配置代理为 vps 公网 IPv4 地址，仅 google 等境外访问目标（尤其是北美网站）转发通过 HE 隧道

更进一步地，可以充分利用 HE 提供的 /48 前缀的 IPv6 CIDR，自己创建一个玩具“互联网”，当然，涉及 BGP 是需要花一点银子的

## 参考资料

- HE 隧道相关

https://www.bilibili.com/video/BV1nD421N7Qt/?spm_id_from=333.337.search-card.all.click&vd_source=fefc74ddfb7b0b365d1b1d4af922a0ba

[配置HE隧道服务获取无穷IPv6地址、内网穿透、外网访问 - 老E的博客](https://appscross.com/blog/how-to-configure-he-ipv6-tunnel.html)
