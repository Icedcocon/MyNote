# PVE 快速开始

## 一、环境准备

### 1. 系统安装

- 请使用ReFind和Ventoy配合安装（efi可在Clover处下载），在启用 zfs raid1 时添加 zfsbootmenu 进行引导。

### 2. 环境配置

#### 2.1 源

- 备份源

```bash
mkdir /etc/apt/sources_backup
cp /etc/apt/sources.list /etc/apt/sources_backup/sources.list.bak
cp /etc/apt/sources.list.d/ceph.list /etc/apt/sources_backup/ceph.list.bak
cp /etc/apt/sources.list.d/pve-enterprise.list /etc/apt/sources_backup/pve-enterprise.list.bak
```

- 换源（中科大）

```bash
# sources.list
sed -i 's|^deb http://ftp.debian.org|deb https://mirrors.ustc.edu.cn|g' /etc/apt/sources.list
sed -i 's|^deb http://security.debian.org|deb https://mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list
# ceph.list
echo "deb https://mirrors.ustc.edu.cn/proxmox/debian/ceph-quincy bookworm no-subscription" > /etc/apt/sources.list.d/ceph.list
# pve-enterprise.list
echo "" > /etc/apt/sources.list.d/pve-enterprise.list
apt update
```

- CT 模板换源

```bash
# 备份
cp /usr/share/perl5/PVE/APLInfo.pm /usr/share/perl5/PVE/APLInfo.pm.bak
sed -i 's|http://download.proxmox.com|https://mirrors.ustc.edu.cn/proxmox|g' /usr/share/perl5/PVE/APLInfo.pm
systemctl restart pvedaemon.service
# 回滚指令
# cp /usr/share/perl5/PVE/APLInfo.pm.bak /usr/share/perl5/PVE/APLInfo.pm
```

- 删除订阅提醒

```bash
sed -i.bak "s/data.status.toLowerCase() !== 'active'/false/g" /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js
```

#### 2.2 存储

- 删除 local-zfs 分区。该分区用于存放镜像等内容。

### 3 直通

#### 3.1 网卡直通

##### 3.1.1 开启 iommu (R730默认开启)

- 编辑 grub

```bash
#编辑grub，请不要盲目改。根据自己的环境，选择设置
vi /etc/default/grub
#在里面找到：
GRUB_CMDLINE_LINUX_DEFAULT="quiet"
#然后修改为：
GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on iommu=pt"
#如果是amd cpu请改为：
GRUB_CMDLINE_LINUX_DEFAULT="quiet amd_iommu=on iommu=pt"
#如果是需要显卡直通，建议在cmdline再加一句video=vesafb:off video=efifb:off video=simplefb:off，加了之后，pve重启进内核后停留在一个画面，这是正常情况
GRUB_CMDLINE_LINUX_DEFAULT="quiet amd_iommu=on iommu=pt video=vesafb:off video=efifb:off video=simplefb:off"
```

- 更新 grub

```bash
update-grub
```

- 加载相应的内核模块

```bash
echo vfio >> /etc/modules
echo vfio_iommu_type1 >> /etc/modules
echo vfio_pci >> /etc/modules
echo vfio_virqfd >> /etc/modules
```

- 使用`update-initramfs -k all -u`命令更新内核参数，并重启主机

- 验证是否开启iommu

```bash
dmesg | grep iommu
# [ 1.341100] pci 0000:00:00.0: Adding to iommu group 0
# [ 1.341116] pci 0000:00:01.0: Adding to iommu group 1
# [ 1.341126] pci 0000:00:02.0: Adding to iommu group 2
# [ 1.341137] pci 0000:00:14.0: Adding to iommu group 3
# [ 1.341146] pci 0000:00:17.0: Adding to iommu group 4
find /sys/kernel/iommu_groups/ -type l 
# 很多内容表示成功
```

> 注意：由于供应商的问题，可能一张物理网卡会有多个逻辑的网口，这些网口会在同一个PCIe地址上

- 确认网卡是否在同一个iommu组

```bash
root@pve:/mnt/pve/SDA# for d in /sys/kernel/iommu_groups/*/devices/*; do n=${d#*/iommu_groups/*}; n=${n%%/*}; printf 'IOMMU Group %s ' "$n"; lspci -nns "${d##*/}"; done|grep Eth
IOMMU Group 10 84:00.0 Ethernet controller [0200]: Broadcom Inc. and subsidiaries NetXtreme BCM5719 Gigabit Ethernet PCIe [14e4:1657] (rev 01)
IOMMU Group 10 84:00.1 Ethernet controller [0200]: Broadcom Inc. and subsidiaries NetXtreme BCM5719 Gigabit Ethernet PCIe [14e4:1657] (rev 01)
IOMMU Group 10 84:00.2 Ethernet controller [0200]: Broadcom Inc. and subsidiaries NetXtreme BCM5719 Gigabit Ethernet PCIe [14e4:1657] (rev 01)
IOMMU Group 10 84:00.3 Ethernet controller [0200]: Broadcom Inc. and subsidiaries NetXtreme BCM5719 Gigabit Ethernet PCIe [14e4:1657] (rev 01)
IOMMU Group 32 01:00.0 Ethernet controller [0200]: Broadcom Inc. and subsidiaries NetXtreme BCM5720 Gigabit Ethernet PCIe [14e4:165f]
IOMMU Group 32 01:00.1 Ethernet controller [0200]: Broadcom Inc. and subsidiaries NetXtreme BCM5720 Gigabit Ethernet PCIe [14e4:165f]
IOMMU Group 33 02:00.0 Ethernet controller [0200]: Broadcom Inc. and subsidiaries NetXtreme BCM5720 Gigabit Ethernet PCIe [14e4:165f]
IOMMU Group 33 02:00.1 Ethernet controller [0200]: Broadcom Inc. and subsidiaries NetXtreme BCM5720 Gigabit Ethernet PCIe [14e4:165f]
```

上述由于多个网卡位于同一个PCI地址上(4张位于84:00 2张位于02:00 2张位于01:00)，可能会在一个iommu组里，只能将这些网卡同时直通给一个虚拟机，否则会报错。

- 如果同一个iommu组，那么就需要利用PCIe桥的ACS特性

##### 3.1.2 PCIe桥开启ACS

- 在`/etc/default/grub`文件里添加一个参数`pcie_acs_override=downstream`

```bash
GRUB_DEFAULT=0
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on  pcie_acs_override=downstream"
GRUB_CMDLINE_LINUX=""
```

- 执行以下指令

```bash
proxmox-boot-tool refresh
update-initramfs -k all -u 
```

##### 3.1.3 编译内核（上述操作失败后尝试）

- 编译内核

```bash
# download the file
wget https://dl.qiedd.com/Linux/pve-kernel/6.5.3-1.tar.gz
# extract the file
tar xvf 6.5.3-1.tar.gz
# install the modified kernel
dpkg -i *.deb
# reboot the system
proxmox-boot-tool kernel pin 6.5.3-1-pve
proxmox-boot-tool refresh
reboot
# check the kernel
uanme -a
```

> 如果使用了zfsbootmenu引导，请在引导时修改内核选项。

##### 3.1.4 ZFS 无法开启 iommu

- 这是因为 zfs 使用 system-boot 而非 grub 引导，因此修改 /etc/default/grub 不生效，需要将配置在 /etc/kernel/cmdline 修改

```bash
# vim /etc/kernel/cmdline
# root=ZFS=rpool/ROOT/pve-1 boot=zfs intel_iommu=on iommu=pt
pve-efiboot-tool refresh
```

- 设置 modprobe 黑名单及配置项

```bash
echo "options vfio_iommu_type1 allow_unsafe_interrupts=1" > /etc/modprobe.d/iommu_unsafe_interrupts.conf
```

## 二、虚拟机安装

### 1. img 类型

#### 1.1 IStoreOS

- 创建不带硬盘的虚拟机
- 执行以下指令
  - img2kvm img vm-index storage

```bash
./img2kvm ../template/iso/istoreos-22.03.6-2024061415-x86-64-squashfs-combined-efi.img 100 NVMEF
```

## 三、 命令

### 1. qm 虚拟机管理

qm 是 Proxmox Virtual Environment (PVE) 中用于管理虚拟机的命令行工具。这个命令行界面是专门为 Proxmox VE 的虚拟机管理设计的。虽然官方文档并没有详细说明 qm 名称的具体来源，但我们可以从其功能和命名习惯中进行一些合理的推测, 很可能是 “QEMU Manage” 的缩写。

QEMU 是一个开源的虚拟化技术，是 Proxmox VE 虚拟化环境的重要组成部分, 负责模拟 CPU 和执行虚拟机内的代码。Proxmox VE 结合了 QEMU 和 Linux Kernel-based Virtual Machine (KVM) 技术，为虚拟机提供硬件加速。

```bash
# 列出所有虚拟机
root@pve:~# qm list
      VMID NAME                 STATUS     MEM(MB)    BOOTDISK(GB) PID   
       100 WIN10                stopped    8192             100.00 0   
       103 WIN11                stopped    8192             100.00 0   
       104 iStoreOS             stopped    2048               2.38 0   
       105 Ubuntu2204-Desktop   stopped    8192              32.00 0

# 启动指定虚拟机
qm start <vm_id>

# 停止指定虚拟机
qm stop <vm_id>

# 强制停止指定虚拟机
# --kill: 强制停止选项
qm stop <vm_id> --kill

# 删除指定虚拟机
qm destroy <vm_id>

# 删除指定虚拟机
# --purge: 这个选项将删除所有与容器相关的配置和数据。
qm destroy <vm_id> --purge

# 克隆虚拟机: 执行前保证源虚拟机处于关闭状态避免未知问题
# <vm_id_src>: 源虚拟机ID
# <vm_id_dst>: 新虚拟机ID
# --name new_vm_clone: 新虚拟机的名称
qm clone <vm_id_src> <vm_id_dst> --name new_vm_clone


# 调整虚拟机设置
# 示例: 修改虚拟机的内存大小、CPU核心数
# 100: 虚拟机的 ID。
# --memory 4096: 设置虚拟机内存为 4096 MB。
# --cores 4: 设置虚拟机使用的 CPU 核心数。
qm set 100 --memory 4096 --cores 4


# 创建新的虚拟机
# 创建一个新的虚拟机。这通常是一个多步骤的过程，包括创建 VM、配置硬件等。
# 100: 虚拟机的 ID。
# --name myvm: 虚拟机的名称。
# --memory 2048: 分配给虚拟机的内存大小，单位是 MB。
# --net0 virtio,bridge=vmbr0: 网络适配器配置。
qm create 100 --name myvm --memory 2048 --net0 virtio,bridge=vmbr0
```

### 2. pct LXC容器管理

`pct` 是 Proxmox Virtual Environment (PVE) 中用于管理 Linux 容器 (LXC) 的命令行工具。这个命令行界面专门设计用于 Proxmox VE 的容器管理。关于 `pct` 名称的来源，可能是 * “Proxmox Container Toolkit” * 的缩写。

Linux 容器（LXC）是轻量级的虚拟化解决方案，用于在 Linux 内核上运行多个隔离的 Linux 系统（称为容器）。Proxmox VE 结合了 LXC 技术，提供了一个容器化平台，使用户能够轻松地部署和管理容器。

```bash
# 列出所有容器:
pct list

root@pve:~# pct list
VMID       Status     Lock         Name  
101        stopped                 Debian12-Docker   
102        stopped                 Debian12-BaoTa 

# 启动/停止/删除指定id的容器
pct start/stop/destroy <container_id>
root@pve:~# pct start 101

# 删除指定容器: 对应的配置与数据也会删除
# --purge: 这个选项将删除所有与容器相关的配置和数据。
pct destroy <container_id> --purge

# 创建容器
# <container_id>: 容器的 ID。
# <template>: 使用的模板。
# [options]: 其他可选参数。
pct create <container_id> <template> [options]

# 克隆容器
# 示例: 克隆源容器id=101,新容器id=102, 且新容器名字为newcontainer
pct clone 101 102 --name newcontainer
```

### 3. pvesm 存储管理

`pvesm` (Proxmox VE Storage Manager) 是 Proxmox Virtual Environment 的一个命令行工具，用于管理存储。这个工具允许管理员列出、添加、修改和删除存储资源。以下是一些常用的 `pvesm` 操作及其示例：

```bash
# 列出当前配置的所有存储及其状态
root@pve:~# pvesm status
Name             Type     Status           Total            Used       Available        %
local             dir     active       924183588       109812088       775768352   11.88%
local-lvm     lvmthin   inactive               0               0               0    0.00%
sda               dir     active      1952559676       619620312      1332939364   31.73%

# 删除指定存储节点local-lvm
root@pve:~# pvesm remove local-lvm
root@pve:~# pvesm status
Name         Type     Status           Total            Used       Available        %
local         dir     active       924183588       109812116       775768324   11.88%
sda           dir     active      1952559676       619620312      1332939364   31.73%

# 列出指定存储上的内容，如虚拟磁盘映像。
root@pve:~# pvesm list sda
Volid                                                                                         Format  Type             Size VMID
sda:backup/vzdump-lxc-100-2024_01_25-17_24_59.tar.zst                                         tar.zst backup     5592309954 100
sda:backup/vzdump-lxc-101-2024_01_25-17_27_16.tar.zst                                         tar.zst backup     2380639886 101
sda:backup/vzdump-qemu-102-2024_01_25-17_28_51.vma.zst                                        vma.zst backup    15411855266 102
sda:backup/vzdump-qemu-103-2024_01_25-17_31_07.vma.zst                                        vma.zst backup    25445120836 103
...
sda:iso/debian-12.4.0-amd64-netinst.iso                                                       iso     iso         658505728
sda:iso/rr_231110.img                                                                         iso     iso        1073741824
sda:iso/virtio-win-0.1.240.iso                                                                iso     iso         627519488
sda:iso/zh-cn_windows_11_consumer_editions_version_23h2_updated_dec_2023_x64_dvd_7cd2c9a8.iso iso     iso        6833309696
...

# 在指定存储节点上, 为虚拟机/容器分配存储空间
# * storage-name: 存储名称。
# * vmid: 虚拟机或容器的 ID。
# * size: 分配的大小，例如 10G 代表 10 GB。
pvesm alloc storage-name vmid size

# 释放为虚拟机/容器分配的存储空间
# * storage-name: 存储名称。
# * vmid: 虚拟机或容器的 ID。
# * volume: 要释放的卷名称。
pvesm free storage-name vmid volume

# 添加新的存储到 Proxmox VE。
# 存储类型可以是 LVM, NFS, iSCSI 等。
# 这里的示例展示了如何添加一个 NFS 存储。
# * mynfsstorage: 存储的名称。
* --server 192.168.1.100: NFS 服务器的 IP 地址。
* --export /path/to/nfs: NFS 上的共享路径。
pvesm add nfs mynfsstorage --server 192.168.1.100 --export /path/to/nfs
```

## 四、备份与还原

### 1. 备份磁盘

#### 1.1 虚拟机/LVM磁盘

> 注意：虚拟机的磁盘应放到第二块硬盘上。如果虚拟机在pve的系统盘上，则重装会清空系统盘。这会导致丢失数据。移动磁盘功能可将磁盘移动到另一个硬盘。

- 查询原有路径并创建 VG

```bash
# 查询 PV(physical volumes)（可以理解为 LVM）
root@pve:~# pvscan / pvs
  PV /dev/nvme0n1                      lvm2 [1.86 TiB]
  Total: 1 [1.86 TiB] / in use: 0 [0   ] / in no VG: 1 [1.86 TiB]

# 查询 VG(volume groups)
root@pve:~# vgscan / vgs

# 创建 VG
root@pve:~# vgcreate NVMEF /dev/nvme0n1
  Volume group "NVMEF" successfully created

# 修改 VG(volume groups) 属性此处激活
# 取消激活: vgchange -an your_volume_group
root@pve:~# vgchange  --activate y NVMEF / vgchange -ay NVMEF
  0 logical volume(s) in volume group "NVMEF" now active

# 查询 LV
root@pve:~# lvdisplay
```

- 数据中心 > 存储 > 添加 > LVM，卷组自动填写 `NVMEF` ，ID按照需求，节点选择对应节点。

#### 1.2 路径

- 将原有路径挂载（临时）

```bash
mount /dev/nvme1n1p1 /mnt/pve/NVMEC
```

- 数据中心 > 存储 > 添加 > 目录，路径填写 `/mnt/pve/NVMEF` ，ID按照需求，节点选择对应节点。

- 修改 `/etc/fstab`
  
  - `/dev/nvme1n1p1`: 设备名称
  - `/mnt/pve/NVMEF`: 挂载点
  - `xfs`: 文件系统类型
  - `defaults,nofail`: 挂载选项
    - `defaults`: 使用默认选项
    - `nofail`: 如果设备不存在,开机时不报错
  - `0`: 不进行备份
  - `2`: 文件系统检查顺序(0表示不检查,1为根目录,2为其他文件系统)

```bash
/dev/nvme1n1p1  /mnt/pve/NVMEC  xfs  defaults,nofail  0  2
```

### 2. 备份PVE本身的信息

#### 2.1 备份

- 挂载U盘到/media。

```bash
cp -r /var/lib/pve-cluster /media
```

> 注意： PVE的存储信息，虚拟机信息，集群的设置比如标签、SDN、用户信息之类都存储在`/var/lib/pve-cluster/config.db`中。

我们只需要备份这个db文件就可以，这里为了方便，就全部备份了。

#### 2.2 还原

> 注意：备份之前的主机名必须和重装后的主机名一致，比如你原来的主机名叫做pve，那你新装了之后也要叫pve。如果你前后的主机名不一样。则会在web上看到2个节点，一个新的机器，一个老的主机，虚拟机都在老主机上。所以一定要确保重装前后主机名一致。

- 在新装的PVE上，挂载U盘到/media。将config.db拷贝回去。

```
cp /media/pve-cluster/config.db /var/lib/pve-cluster
```

- 重启pve即可。

### 3. 备份额外的配置

#### 3.1 备份启动/模块配置

- 备份

```bash
mkdir /media/{boot,modprobe}
cp /etc/modules-load.d/* /media/modprobe/
cp /etc/default/grub /media/boot/
cp /etc/modules /media/
```

- 还原

```bash
cp /media/modprobe/*  /etc/modules-load.d/
cp /media/boot/grub /etc/default/
cp /media/modules /etc/
# 更新grub
update-grub
# 更新内核参数
update-initramfs -k all -u
```

#### 3.2 备份网络（可选）

- 备份

```bash
cp -r /etc/netowork /media/
```

- 还原

```bash
cp -r /media/netowork/* /etc/netowork/
# 重启主机/网络
systemctl restart networking
```

> 注意：增加、变换了网卡的槽位，就不要无脑还原网卡了。

## 参考资料

- loading inital ramdisk

https://github.com/ventoy/Ventoy/issues/2782

https://forum.proxmox.com/threads/ventoy-install-of-proxmox-8-1-halts-at-loading-initial-ramdisk.143196/

- promox常用脚本

[Proxmox VE Helper-Scripts](https://tteck.github.io/Proxmox)

- 备份相关

[佛西博客 - 备份PVE的配置信息，重装后快速恢复。](https://foxi.buduanwang.vip/virtualization/pve/3022.html/)

- 命令相关

https://www.xrgzs.top/posts/pve-cm

https://zoe.red/2024/282.html

- 直通相关

https://foxi.buduanwang.vip/virtualization/pve/561.html/

- IOMMU分组

https://post.smzdm.com/p/axz8rv2w/

https://qiedd.com/1894.html
