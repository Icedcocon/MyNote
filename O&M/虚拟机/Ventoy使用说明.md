# Ventoy 使用说明

## 一、安装

### 1. OpenWrt

- 背景介绍

Ventoy 从 1.0.41 版本支持 OpenWrt 的 IMG 镜像的启动。但需要一些特殊处理，在这里进行说明。 

- ventoy_openwrt.xz 插件

由于目前 OpenWrt 镜像中并没有打包 Ventoy 所需的 dm 内核模块，所以需要下载 `ventoy_openwrt.xz` 这个插件放到U盘里才可以正常启动。  
这个插件其实就是把 OpenWrt 官网上的内核模块文件打包了一下而已，下载链接如下：  

https://github.com/ventoy/OpenWrtPlugin/releases  

注意随着OpenWrt版本更新，这个文件会经常更新，请保持使用最新版本。  

在U盘第1个分区（容量大的、保存镜像文件的分区）的根目录下**新建一个 `ventoy`（全小写）目录，然后把这个文件下载下来，放在这个目录下**。  

- 支持的 IMG 镜像类型

Ventoy 只支持 x86 类型的 `combined-ext4.img` 和 `combined-squashfs.img` 这两种 OpenWrt 镜像。  
对于 `combined-ext4.img` 类型，直接从官网下载到 gzip 压缩包解压后即可启动。  
对于 `combined-squashfs.img` 类型，从官网下载后需要处理一下才可以，详见本文后面的说明。  

- combined-squashfs.img 的处理

`combined-squashfs.img` 类型的镜像从官网下载之后，需要使用 `ventoy_openwrt_squashfs.sh` 脚本处理后才可以使用 Ventoy 启动。  
此脚本也是从上面那个链接中下载，使用方法如下：

sh ventoy_openwrt_squashfs.sh  openwrt-xxx-combined-squashfs.img.gz
例如：
sh ventoy_openwrt_squashfs.sh  openwrt-19.07.7-x86-64-combined-squashfs.img.gz

在上例中，脚本处理完之后会生成 `openwrt-19.07.7-x86-64-combined-squashfs.img` 文件，将此文件拷贝到 Ventoy U盘中即可启动。

## 参考文献

- OpenWrt 插件相关

[openwrt . Ventoy](https://www.ventoy.net/en/doc_openwrt.html)

https://github.com/ventoy/OpenWrtPlugin/releases
