# CC9e快速开始

## 一、Android分区结构概述

本文内容基于高通开源Android Q(10.0),部分内容更新至Android S(12.0),仅涉及high-level-operating-system(Android)部分。

### 1.  传统分区结构(non-A/B 或 A-only)

#### 1.1 Android传统分区结构简介

- **bootloader**: 设备启动后首先进入,判断启动模式：Android系统、recovery模式（音量上键+电源键）、fastboot模式（音量下键+电源键）等
- **boot**: 包含Android的kernel（内核）和ramdisk（内存盘），日常启动Android系统，就是通过启动boot分区的kernel并加载ramdisk，完成内核启动，进入系统。
- **system**: 包含Android系统的可执行程序、库、系统服务和app等，在较新的安卓版本作为根路径。
- **vendor**: 包含厂商私有的可执行程序、库、系统服务和app等
- **userdata**: 用户存储空间
- **recovery**: 包含recovery系统的kernel和ramdisk
- **cache**: 存储系统或用户应用产生的临时数据
- **misc**: 一个非常小的分区，4 MB左右。recovery用这个分区来保存一些关于升级的信息，应对升级过程中的设备掉电重启的状况。 bootloader启动的时候，会读取这个分区里面的信息，以决定系统是否进 Recovery System 或 Main System。
- **ramdisk.img**: 根文件系统,包含在boot.img中
- **vbmetal**: 用于安全验证

#### 1.2 ramdisk、boot.img、recovery.img之间的关系

1. **ramdisk.img 会被打包到boot.img和recovery.img中**

> 注意: boot.img和recovery.img中的ramdisk.img不是同一个，在不同分区中ramdisk.img的作用不同

2. **ramdisk.img的重要文件"init"和"init.rc"**
   
   - init: 由system/core/init/init.c编译而来
   - init.rc位置:
     - boot.img中: system/core/init/init.rc
     - recovery.img中: bootable/recovery/etc/init.rc

3. **启动过程**
   
   - kernel加载后,第一个执行的用户态进程是init
   - init解析init.rc文件,启动相应服务
   - 正常开机和进入recovery模式启动的进程不同

4. **recovery.img和boot.img的相似性**
   
   - 两者结构相似度约90%
   - 都由Linux内核(zImage)和内存磁盘镜像(ramdisk.img)组成
   - Linux内核部分完全相同

5. **主要差异**
   
   - ramdisk.img中部分文件存在差异
   - recovery.img的ramdisk中sbin目录多了recovery命令
   - init.rc及相关配置文件内容略有不同

6. **启动原理**
   
   - Bootloader根据用户选择决定使用哪个镜像的Linux内核
   - 使用boot.img: 正常启动Android系统
   - 使用recovery.img: 进入Recovery选择菜单

通过这些差异,系统能够根据需要进入不同的模式,实现正常启动或进入恢复模式的功能。

#### 1.3 OTA升级流程

1. 下载OTA包至cache分区
2. 向misc分区写入指令
3. 重启进入recovery模式
4. 执行升级脚本
5. 清除misc分区
6. 重启进入新版本系统

### 2. A/B分区结构

Android O之后引入,将系统分区分成A和B两个槽(slot)

#### 2.1 主要特点:

- 实现无缝升级
- 提高系统可用性
- 不需要cache分区存储OTA包

#### 2.2 A/B分区标识:

- bootable: 槽是否可启动
- successful: 槽是否成功启动过
- active: 当前运行的系统槽

#### 2.3 A/B分区结构变化:

- bootloader: 选择启动槽
- boot_a/boot_b: 包含kernel和recovery的ramdisk
- system_a/system_b: 系统分区
- vendor_a/vendor_b: 厂商分区
- userdata: 用户数据(不区分A/B)
- misc: 不区分A/B
- persist: 存储持久化数据(不区分A/B)

### 3. Android Q的改动

#### 3.1 SSI (Shared System Image)

- 目的: 使设备代码移植更友好
- 概念: 多产品共用的、与具体硬件设备无关的系统镜像

#### 3.2 动态分区

- 将多个系统只读分区合并为一个super分区
- 支持用户态动态分配挂载
- 引入fastbootd程序
- 使用overlay文件系统解决空间不足问题

#### 3.3 system-as-root (SAR)

- Android Q强制使用SAR分区布局
- 两种SAR方案:
  1. legacy system-as-root (LSAR)
  2. two-stage-init (2SI)

## 二、刷机

### 0. 刷机测试

#### 0.1 软件

- **Treble Check** (Github)
  
  - 检测是否支持 Project Treble ： 刷入 sGSI 通用镜像或  unofficial 镜像
  
  - 检测A-only、A/B、vA/B分区： 采用何种镜像
  
  - 检测System-as-root： 支持 SAR 的手机即使为A-only分区也要使用A/B分区镜像

- **DevCheck Pro** (酷安)
  
  - 验机信息

### 1. 刷入第三方 recovery.img twrp

- 下音量键 + 关机键进入 fastboot 模式

- 下载合适版本的 img 文件（注意安卓版本与机型）

- 安装

```bash
# 查看设备
.\fastboot.exe devices
# 刷入固件
.\fastboot.exe flash recovery .\recovery-TWRP-3.3.2B-0620-XIAOMI_CC9E_10.0-CN-wzsx150.img
# 重启手机
.\fastboot.exe reboot
```

## 参考资料

https://xdaforums.com/t/rom-crdroid-from-mi-a3-working-on-cc9e.4121101/#post-87569835

[[GUIDE] [ROM] How to Flash BeastROM to Mi CC9e | XDA Forums](https://xdaforums.com/t/guide-rom-how-to-flash-beastrom-to-mi-cc9e.3970925/)

- nethunter

[[ROM][OFFICIAL] Kali NetHunter for the Xiaomi Mi A3 LinageOS 20 | XDA Forums](https://xdaforums.com/t/rom-official-kali-nethunter-for-the-xiaomi-mi-a3-linageos-20.4631001/)

- lineageOS20

[[UNOFFICIAL][ROM][13] LineageOS 20 | XDA Forums](https://xdaforums.com/t/unofficial-rom-13-lineageos-20.4552703/)
