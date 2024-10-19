# 启动引导 Bootloader 快速开始

## 一、ReFind

### 1. 安装

- 安装 ubuntu 24.04

- 通过 apt 安装

```bash
apt-add-repository ppa:rodsmith/refind 
apt update
apt install -y refind
```

### 2. 配置

```bash
cp NvmExpressDxe.efi /boot/efi/EFI/refind/drivers_x64/
cp PartitionDxe.efi /boot/efi/EFI/refind/drivers_x64/
wget https://github.com/zbm-dev/zfsbootmenu/releases/download/v2.3.0/zfsbootmenu-release-x86_64-v2.3.0-vmlinuz.EFI
```

## 二、Clover

### 1. 配置分区

- 配置分区表并设置 EFI 分区

```bash
fdisk /dev/sdx

Command (m for help): g
Created a new GPT disklabel (GUID: 819FBD12-A0A3-0644-9E46-C56A6A720C00).
The device contains 'iso9660' signature and it will be removed by a write command. See fdisk(8) man page and --wipe option for more details.

Command (m for help): n
Partition number (1-128, default 1): 1
First sector (2048-62259166, default 2048): 2048
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-62259166, default 62259166): +256M
Created a new partition 1 of type 'Linux filesystem' and of size 256 MiB.

Command (m for help): t
Selected partition 1
Partition type or alias (type L to list all): 1
Changed type of partition 'Linux filesystem' to 'EFI System'.

Command (m for help): w
```

- 配置文件系统

```bash
mkfs.vfat /dev/sdx1
```

- 执行脚本

```bash
apt install p7zip-full
git clone https://mirror.ghproxy.com/https://github.com/m13253/clover-linux-installer.git
cd clover-linux-installer
wget https://github.com/CloverHackyColor/CloverBootloader/releases/download/5159/CloverV2-5159.zip
mv CloverV2-5159.zip CloverV2.zip
bash -x install.sh
```

## 参考资料

- plist编辑器

https://imacos.top/2022/07/26/config-plist-clover-opencore/

- plist 说明

https://solove.love/clover-clover-tutorial-the-clover-catalog-file-parameters-detailed.html

[3. DeviceProperties · 国光的黑苹果安装教程](https://apple.sqlsec.com/4-OC%E9%85%8D%E7%BD%AE/4-3.html)

https://blog.csdn.net/qq_17209641/article/details/129777654
