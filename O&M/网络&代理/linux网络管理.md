# Linux 网络管理

## 一、主流网络管理方案

目前Linux系统中主要采用以下几种网络管理方案:

1. **Netplan(YAML配置)** Ubuntu 18.04开始采用Netplan这个新的网络渲染引擎,使用YAML格式的配置文件，可以**统一声明网络接口到 NetworkManager 和 systemd-networkd 后端**，位于 `/etc/netplan/*.yaml`。
2. **NetworkManager** 这是最常用的网络管理工具,在RHEL 7+、CentOS 7+、Fedora、OpenSUSE等发行版中广泛使用。它提供了命令行和图形界面,可以轻松管理有线、无线、VPN等网络连接。
3. **systemd-networkd** 这是systemd项目引入的一个网络管理组件,在Arch Linux、Fedora 15+、Debian 8+等发行版中使用。它的优势是与systemd更好地集成,并支持更现代的网络功能。
4. **ifupdown(interfaces)** 这是基于Debian系统中较为传统的网络配置文件 `/etc/network/interfaces` 的管理方案,在Ubuntu、Linux Mint、Debian等发行版中仍在使用。
5. **network-scripts** 这是较老一代Red Hat系统的网络配置脚本,存放在 `/etc/sysconfig/network-scripts/` 目录下。现代RHEL版本已转向使用NetworkManager。
6. **OpenRC** Gentoo Linux使用OpenRC作为初始化系统,相应的网络配置文件在 `/etc/conf.d/net` 和 `/etc/init.d/net.*` 中。
7. **其他工具** 例如LCNC、BCNM、ifenslave等一些工具,提供特定的功能如网络绑定、VLAN管理等。

## 二、Debian 基本网络架构

让我们来回顾一下现代 Debian 操作系统中的基本网络架构。

**表 5.1. 网络配置工具一览表**

| 软件包                     | 类型              | 说明                                                              |
| ----------------------- | --------------- | --------------------------------------------------------------- |
| **`network-manager`**   | 配置：：NM          | NetworkManager（守卫进程）：自动管理网络                                     |
| `network-manager-gnome` | 配置：：NM          | NetworkManager（GNOME前端）                                         |
| **`netplan.io`**        | 配置：：NM+networkd | Netplan (生成器): 统一的，声明网络接口到 NetworkManager 和 systemd-networkd 后端 |
| **`ifupdown`**          | 配置：：ifupdown    | 用来启动/关闭网络的标准工具（Debian特有）                                        |
| **`isc-dhcp-client`**   | 配置：：底层          | DHCP客户端                                                         |
| `pppoeconf`             | 配置：：辅助          | 配置助手，以便于使用PPPoE连接                                               |
| `wpasupplicant`         | 配置：：辅助          | WPA和WPA2客户端支持（IEEE 802.11i)                                     |
| `wpagui`                | 配置：：辅助          | wpa_supplicant Qt 图形界面客户端                                       |
| `wireless-tools`        | 配置：：辅助          | 操控Linux无线扩展的工具                                                  |
| `iw`                    | 配置：：辅助          | 配置 Linux 无线设备的工具                                                |
| **`iproute2`**          | 配置：：iproute2    | iproute2, IPv6和其他高级网络配置：`ip`(8),`tc`(8)等等                       |
| **`iptables`**          | 配置：：Netfilter   | 封包过滤和网络地址转换管理工具（Netfilter）                                      |
| **`nftables`**          | 配置：：Netfilter   | 封包过滤和网络地址转换管理工具（Netfilter） ({ip,ip6,arp,eb}tables 的后续替代者)       |
| **`iputils-ping`**      | 测试              | 测试能否连接远程主机，通过主机名或IP 地址（iproute2）                                |
| `iputils-arping`        | 测试              | 测试能否连接远程主机，通过ARP地址                                              |
| `iputils-tracepath`     | 测试              | 跟踪访问远程主机的路径                                                     |
| **`ethtool`**           | 测试              | 显示或更改以太网设备的设定                                                   |
| `mtr-tiny`              | 测试：：底层          | 追踪连接远程主机的路径（文本界面）                                               |
| `mtr`                   | 测试：：底层          | 追踪连接远程主机的路径（文本界面和GTK界面）                                         |
| `gnome-nettool`         | 测试：：底层          | 获取常见网络信息的工具（GNOME)                                              |
| **`nmap`**              | 测试：：底层          | 网络映射/端口扫描（Nmap，控制台）                                             |
| **`tcpdump`**           | 测试：：底层          | 网络流量分析（Tcpdump，控制台）                                             |
| `wireshark`             | 测试：：底层          | 网络流量分析（Wireshark,GTK）                                           |
| `tshark`                | 测试：：底层          | 网络流量分析(控制台）                                                     |
| `tcptrace`              | 测试：：底层          | 根据`tcpdump`的输出生成的连接数据统计                                         |
| `snort`                 | 测试：：底层          | 灵活的网络入侵侦测系统（Snort）                                              |
| `ntopng`                | 测试：：底层          | 在网页浏览器中展示网络流量                                                   |
| **`dnsutils`**          | 测试：：底层          | BIND 软件包提供的网络客户端程序：`nslookup`(8),`nsupdate`(8),`dig`(8)         |
| `dlint`                 | 测试：：底层          | 利用域名服务器查询来查看 DNS 域信息                                            |
| `dnstracer`             | 测试：：底层          | 跟踪 DNS 查询直至源头                                                   |

## 参考资料

- Debian网络架构及对应工具（Debian参考手册）

[第 5 章 网络设置](https://www.debian.org/doc/manuals/debian-reference/ch05.zh-cn.html)

[Debian 参考手册](https://www.debian.org/doc/manuals/debian-reference/index.zh-cn.html)
