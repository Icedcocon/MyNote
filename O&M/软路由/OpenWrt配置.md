# OpenWrt安装配置Tailscale

Tailscale就是基于Wireguard的一个联网工具，无需公网地址，通过去中心化，实现各个节点之间点对点的连接。配置简单友好，支持的各类平台和客户端。下面介绍在OpenWrt上的配置过程。

## **1、下载软件**

将Tailscale软件包下载到指定目录。找到最新的软件包，下载到本地。然后使用Winscp工具将下载的软件上传到OpenWrt的/tmp目录下，也可以找到下载链接，直接使用wget命令下载。

```
wget https://github.com/adyanth/openwrt-tailscale-enabler/releases/download/v1.32.2-98e126e-autoupdate/openwrt-tailscale-enabler-v1.32.2-98e126e-autoupdate.tgz
```

## **2、解压缩软件**

```
tar x -zvC / -f openwrt-tailscale-enabler-v1.32.2-98e126e-autoupdate.tgz
```

## **3、安装依赖包**

```
opkg updateopkg install libustream-openssl ca-bundle kmod-tun
```

## **4、设置开机启动，验证开机启动**

```
/etc/init.d/tailscale enablels /etc/rc.d/S*tailscale*
```

## **5、启动tailscale**

```
/etc/init.d/tailscale start
```

## **6、获取登录链接，配置路由**

```
tailscale up
```

复制显示的地址，并在浏览器中打开，使用谷歌或微软帐号登录Tailscale的管理主页进行验证。

## **7、开启子网网路由**

在OpenWrt上输入以下命令，打开本地子路由。子网地址是OpenWrt的lan网络。

```
tailscale up --advertise-routes=192.168.18.0/24 --accept-dns=false
```

在Tailscale的管理页面上，单击设备列表右侧的更多图标，禁用密钥过期，并打开子网路由。

现在在OpenWrt上已经可以ping通其他Tailscale节点了，但其他节点还无法连接OpenWrt节点，还需要在OpenWrt上添加Tailscale接口。

## **8、添加接口**

在OpenWrt上新建一个接口，协议选静态地址，设备选tailscale0，地址为Taliscale管理页面上分配的地址，掩码255.0.0.0。防火墙区域选lan区域。

## **9、添加防火墙规则**

将以下内容，加到防火墙的自定义规则当中，并重启防火墙。

```
iptables -I FORWARD -i tailscale0 -j ACCEPTiptables -I FORWARD -o tailscale0 -j ACCEPTiptables -t nat -I POSTROUTING -o tailscale0 -j MASQUERADE
```

现在各个Tailscale节点之间已经可以正常互访了。
