# ESXi 快速开始

## 一、自定义镜像

### 1. 编译 Docker 镜像

- ESXi 构建工具 PowerCLI 的文档中有提到，运行它需要 Python 3.7 运行环境，所以我们使用 `python:3.7` 作为基础镜像。

```dockerfile
FROM python:3.7.9
```

- 安装需要的 Python 依赖软件包： `six psutil lxml pyopenssl`

```dockerfile
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && pip install six psutil lxml pyopenssl --no-cache-dir
```

- PowerCLI 运行需要的 .Net 运行环境和 PowerShell 环境： `packages-microsoft-prod powershell`

```dockerfile
RUN wget "https://packages.microsoft.com/config/debian/11/packages-microsoft-prod.deb" -O packages-microsoft-prod.deb && dpkg -i packages-microsoft-prod.deb && rm packages-microsoft-prod.deb

RUN sed -i -e "s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/" /etc/apt/sources.list ; apt-get update && apt-get install -y powershell
```

- 根据 [博通 VMWare 开发者文档](https://developer.broadcom.com/powercli/installation-guide)中的 `PowerCLI` 安装文档，采用离线方案安装完整的 `PowerCLI`：

```dockerfile
RUN curl -L 'https://developer.vmware.com/docs/17484/' \
  -H 'authority: developer.vmware.com' \
  -H 'accept: text/html' \
  -H 'referer: https://developer.vmware.com/powercli/installation-guide' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36' \
  --compressed \
  -o VMware-PowerCLI-13.0.0-20829139.zip
```

> 警告：上述方案已失效，在博通收购 VMWare 后下载 PowerCLI 需要注册并登录后下载，此处直接放入安装包。（或可直接从 PowerShell 库安装 PowerCLI。）

```dockerfile
ADD ./VMware-PowerCLI-13.2.1-22851661.zip /VMware-PowerCLI-13.2.1-22851661.zip
```

- 接下来的工作需要在 Powershell 环境中进行，所以需要设置 pwsh 为容器构建的 shell：

```dockerfile
SHELL ["/usr/bin/pwsh", "-c"]
```

- 搞定 pwsh 运行环境之后，进行 PowerCLI 的工具的解压及安装，并进行环境清理：

```dockerfile
RUN cd $($env:PSModulePath | awk -F ':' '{print $1}') && \
    mv /VMware-PowerCLI-13.2.1-22851661.zip . && \
    Expand-Archive ./VMware-PowerCLI-13.2.1-22851661.zip ./ && \
    rm -rf ./VMware-PowerCLI-13.2.1-22851661.zip
```

- 最后，告诉工具镜像用 pwsh 替代 python 作为入口即可：

```dockerfile
ENTRYPOINT pwsh
```

- 完整Dockerfile

```dockerfile
FROM python:3.7.9

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && pip install six psutil lxml pyopenssl --no-cache-dir

RUN wget "https://packages.microsoft.com/config/debian/11/packages-microsoft-prod.deb" -O packages-microsoft-prod.deb && dpkg -i packages-microsoft-prod.deb && rm packages-microsoft-prod.deb

RUN sed -i -e "s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/" /etc/apt/sources.list ; apt-get update && apt-get install -y powershell

ADD ./VMware-PowerCLI-13.2.1-22851661.zip /VMware-PowerCLI-13.2.1-22851661.zip

SHELL ["/usr/bin/pwsh", "-c"]

RUN cd $($env:PSModulePath | awk -F ':' '{print $1}') && \
    mv /VMware-PowerCLI-13.2.1-22851661.zip . && \
    Expand-Archive ./VMware-PowerCLI-13.2.1-22851661.zip ./ && \
    rm -rf ./VMware-PowerCLI-13.2.1-22851661.zip

ENTRYPOINT pwsh
```

- PowerCli安装说明

```bash
To use the VMware.ImageBuilder module, you must install Python 3.7 with four additional packages and configure PowerCLI.

Starting from VMware PowerCLI 13.0, Python 3.7 is a prerequisite for using the VMware.ImageBuilder module.

You must also install four additional packages in Python:

- six
- psutil
- lxml
- pyopenssl

To configure PowerCLI, you must set the path to the Python 3.7 executable by using the Set-PowerCLIConfiguration cmdlet.
```

### 2. 编辑镜像

- 准备 ESXi 的离线安装包
  
  - [VMware-ESXi-8.0U2b-23305546-depot.zip](https://cios.dhitechnical.com/VMware/VMware%20vSphere%208/VMware%20ESXi%208/VMware-ESXi-8.0U2b-23305546-depot.zip)

- 准备 ESXi 相关社区驱动
  
  - ESXi 的 PCIe 社区网络驱动程序：[Net-Community-Driver.zip](https://ia601806.us.archive.org/26/items/flings.vmware.com/Flings/Community%20Networking%20Driver%20for%20ESXi/Net-Community-Driver_1.2.7.0-1vmw.700.1.0.15843807_19480755.zip)
  - ESXi 的 USB 社区网络驱动程序：[ESXi80U2-VMKUSB-NIC.zip](https://ia601806.us.archive.org/26/items/flings.vmware.com/Flings/USB%20Network%20Native%20Driver%20for%20ESXi/ESXi80U2-VMKUSB-NIC-FLING-67561870-component-22416446.zip)
  - ESXi 的 NVMe 社区驱动程序：[nvme-community-driver.zip](https://ia601806.us.archive.org/26/items/flings.vmware.com/Flings/Community%20NVMe%20Driver%20for%20ESXi/nvme-community-driver_1.0.1.0-3vmw.700.1.0.15843807-component-18902434.zip)

- 将下载好的文件放置在当前目录，然后执行下面的命令，能够直接启动工具镜像

```bash
docker run --rm -it -v `pwd`:/data easy-esxi-builder:20240621
```

### 3. 容器中添加驱动

- 添加基础镜像和我们要附加到 ESXi 镜像中的驱动（命令中的文件名根据下载的文件名进行适当调整）：

```bash
# 加载基础镜像
Add-EsxSoftwareDepot /data/VMware-ESXi-8.0U2b-23305546-depot.zip

# 加载社区 NVMe 驱动
Add-EsxSoftwareDepot /data/drivers/nvme-community-driver_1.0.1.0-3vmw.700.1.0.15843807-component-18902434.zip

# 加载社区 PCIe 驱动
Add-EsxSoftwareDepot /data/drivers/Net-Community-Driver_1.2.7.0-1vmw.700.1.0.15843807_19480755.zip

# 加载社区 USB 驱动
Add-EsxSoftwareDepot /data/drivers/ESXi80U2-VMKUSB-NIC-FLING-67561870-component-22416446.zip

# 加载社区 AMD VGPU 驱动
Add-EsxSoftwareDepot /data/drivers/VMW-ESX-6.5.0-amdgpuv-1.05-offline_bundle-6159546.zip

# 如果你还需要更多驱动，参考上面的命令，继续操作即可。
```

- 执行 `Get-EsxImageProfile` 来查看系统加载了的 ESXi 基础镜像具体是什么版本：

```bash
Get-EsxImageProfile

# Name                           Vendor          Last Modified   Acceptance Level
# ----                           ------          -------------   ----------------
# ESXi-8.0U2b-23305546-standard  VMware, Inc.    02/29/2024 00:… PartnerSupported
# ESXi-8.0U2sb-23305545-no-tools VMware, Inc.    02/14/2024 06:… PartnerSupported
# ESXi-8.0U2b-23305546-no-tools  VMware, Inc.    02/14/2024 08:… PartnerSupported
# ESXi-8.0U2sb-23305545-standard VMware, Inc.    02/29/2024 00:… PartnerSupported
```

- 使用下面的命令，制作一个“镜像副本”

```bash
New-EsxImageProfile -CloneProfile "ESXi-8.0U2b-23305546-standard" -name "ESXi-8.0U2b-23305546-standard-nic" -vendor "soulteary"

# Name                           Vendor          Last Modified   Acceptance Level
# ----                           ------          -------------   ----------------
# ESXi-8.0U2b-23305546-standard… soulteary       02/29/2024 00:… PartnerSupported
```

- 使用命令 `Get-EsxSoftwarePackage` 来获得可以使用的驱动列表：

```bash
# 列出所有驱动
Get-EsxSoftwarePackage
# 过滤掉“VMware” 出品、和官方镜像一起构建于 “09/04/2023” 的内容：
Get-EsxSoftwarePackage | grep -v VMware | grep -v '09/04/2023'

# Name                     Version                        Vendor     Creation Date
# ----                     -------                        ------     -------------
# net-community            1.2.7.0-1vmw.700.1.0.15843807  VMW        03/10/2022 21:2…
# vmkusb-nic-fling         1.12-2vmw.802.0.0.67561870     VMW        09/07/2023 08:5…
# pensandoatlas            1.46.0.E.28.1.314-2vmw.802.0.… VMW        12/12/2023 20:3…
# nvme-community           1.0.1.0-3vmw.700.1.0.15843807  VMW        01/08/2020 12:0…
```

- 挑选出我们手动添加的驱动的名称，执行类似下面的命令，就完成了对 ESXi 镜像驱动的增加。

```bash
Add-EsxSoftwarePackage -ImageProfile "ESXi-8.0U2b-23305546-standard-nic" -SoftwarePackage "nvme-community"

Add-EsxSoftwarePackage -ImageProfile "ESXi-8.0U2b-23305546-standard-nic" -SoftwarePackage "net-community"

Add-EsxSoftwarePackage -ImageProfile "ESXi-8.0U2b-23305546-standard-nic" -SoftwarePackage "vmkusb-nic-fling"

Add-EsxSoftwarePackage -ImageProfile "ESXi-8.0U2b-23305546-standard-nic" -SoftwarePackage "amdgpuv"
```

- 最后，执行命令将附加好社区驱动的 ESXi 镜像进行导出即可：

```bash
Export-EsxImageProfile -ImageProfile "ESXi-8.0U2b-23305546-standard-nic" -ExportToIso -FilePath /data/ESXi8U2b.iso
```

### 4. 制作启动 U 盘

- 格式化 U 盘

```bash
#格式化之前需要先卸载U盘
umount /dev/sdd1
mkfs.vfat /dev/sdd -I
```

- 制作启动 U 盘（由于VMware的镜像不包含分区表，因此dd、etcher不可用）
  - 下载安装包，如 ventoy-1.0.00-linux.tar.gz
  - 执行脚本初始化 U 盘
  - 将镜像拷贝到 U 盘

```bash
# dd bs=4M if=./ of=/dev/sdd status=progress && sync
sudo sh Ventoy2Disk.sh -i /dev/XXX
# Ventoy2Disk.sh  命令  [选项]  /dev/XXX
#   命令含义:
#     -i   安装ventoy到磁盘中 (如果对应磁盘已经安装了ventoy则会返回失败)
#     -I   强制安装ventoy到磁盘中，(不管原来有没有安装过)
#     -u   升级磁盘中的ventoy版本
#     -l   显示磁盘中的ventoy相关信息
#     
#   选项含义: (可选)
#     -r SIZE_MB  在磁盘最后保留部分空间，单位 MB (只在安装时有效)
#     -s          启用安全启动支持 (默认是关闭的)
#     -g          使用GPT分区格式，默认是MBR格式 (只在安装时有效)
#     -L          主分区（镜像分区）的卷标 (默认是 Ventoy)
```

## 二、配置与插件

### 1.  解锁MacOS

- 下载 [DrDonk/*esxi-unlocker*](https://github.com/DrDonk/esxi-unlocker) 并解压执行

```bash
wget https://github.com/DrDonk/esxi-unlo
cker/archive/refs/tags/v4.0.6.tar.gz
tar -xzf v4.0.6.tar.gz
cd esxi-unlocker-4.0.6/
./unlock
```

### 2. S7150x2驱动

您需要在每个 VMware ESXi 主机上安装 Radeon Pro 驱动程序（amdgpuv 和 amdgpuv-cim），该插件会在主机的插件界面内显示。安装驱动程序，请执行以下操作：

- 下载相关用的版本的 ESXi 驱动 [FirePro™ S7150 X2 Drivers](https://www.amd.com/en/support/downloads/drivers.html/graphics/firepro/firepro-s-series/firepro-s7150-x2.html)：
  
  - `amdgpuv-1.05-1OEM.650.0.0.4598673.x86_64-CL1424097.vib`
  
  - `amdgpuv-cim-1.00-6.5.0-4598673.vib`

- 执行以下命令来安装驱动程序：

```bash
esxcli software vib install --no-sig-check -v /vmfs/volumes/NVME/Downloads/amdgpuv/amdgpuv-1.05-1OEM.650.0.0.4598673.x86_64-CL1424097.vib
esxcli software vib install --no-sig-check -v /vmfs/volumes/NVME/Downloads/amdgpuv/amdgpuv-cim-1.00-6.5.0-4598673.vib
```

- 设置 ESXi 启动时导入 amdgpuv 驱动

```bash
esxcli system module set -m amdgpuv -e true
```

- 重启服务器。
  - 无论每个 GPU 配置了多少虚拟 MxGPU，VMware ESXi 6.5上每个 GPU 会在总线显示 16 个 MxGPU 设备。
- 查看 AMD 设备

```bash
lspci | grep AMD

# 0000:06:00.0 VGA compatible controller: AMD Tonga S7150
# 0000:07:00.0 VGA compatible controller: AMD Tonga S7150
```

- 配置显卡

```bash
esxcfg-module -s "adapter1_conf=<bus>,<dev>,<func>,<num>,<fb>,<intv>" amdgpuv
```

• bus – the bus number: in decimal value
• dev – the device number: in decimal value
• func – the function number
• num – the number of enabled VFs
• fb – the size of framebuffer for each VF
• intv – the interval of VF switching.

如：

```bash
# 为设备 06:00.0 和 07:00.0 开启 vGPU 每个设备有 2 个 VF
# 每个 VF 有 4G 显存 时间分片为 7000ms 时间片
esxcfg-module -s "adapter1_conf=6,0,0,2,4096,7000 adapter2_conf=7,0,0,2,4096,7000" amdgpuv
```

• command: esxcfg-module -s "adapter1_conf=1,0,0,15,512,7000" amdgpuv
Enables 15 virtual functions, each VF with 512M FB, and 7 millisecond time slice for
switch for the adapter located @ 1.00.0
• command: esxcfg-module -s "adapter1_conf=5,0,0,8,256,7000
adapter2_conf=7,0,0,10,256,10000" amdgpuv
Enable 8 VF, each VF has 256M FB and 7 millisecond time slice for adapter located @
05:00.0
Enable 10 VF, each VF has 256M FB and 10 millisecond time slice for adapter located @
07:00.0
• command: esxcfg-module -s "adapter1_conf=14,0,0,6,1024,7000
adapter2_conf=130,0,0,4,1920,7000" amdgpuv
Enable 6 VF, each VF has 1024M FB and 7 millisecond time slice for adapter located @
0E:00.0
Enable 4 VF, each VF has 1920M FB and 7 millisecond time slice for adapter located @
82:00.0

- 重启

### 3. 网卡直通显示灰色

- 主机-管理-高级设置-搜索ACSCheck-设置为True

## 三、自定义 vib 文件

### 1. ar 指令

```bash
-t  查看文件
-x 解压文件
```

- 查看文件

```bash
ar -t amdgpuv.vib
```

### 2. vib 文件结构说明

- vib 文件说明

```bash
# ar tv file.vib 查看 vib 文件内容
descriptor.xml  # 元数据
sig.pkcs7       # 签名
scsi-meg        # 驱动程序
```

- 驱动程序说明

```bash
# ar vx file.vib --output vib-extract     解压 vib 文件
# tar -tzvf scsi-meg                      解压 scsi-meg 文件
```

### 3. 制作 ESXi 8.0 vib 包

- (1) 解压

```bash
unzip VMW-ESX-6.5.0-amdgpuv-1.05-offline_bundle-6159546.zip -d VMW-ESX-6.5.0-amdgpuv
cd VMW-ESX-6.5.0-amdgpuv/vib20/amdgpuv
mkdir vib-extract
ar vx AMD_bootbank_amdgpuv_1.05-1OEM.650.0.0.4598673.vib --output vib-extract
```

- (2) 修改

```bash
cd vib-extract
```

将xml修改为

```xml
PAYLOAD_SIZE=$(stat -c %s vib-extract/amdgpuv)
PAYLOAD_SHA256=$(sha256sum vib-extract/amdgpuv | awk '{print $1}')
PAYLOAD_SHA256_ZCAT=$(zcat vib-extract/amdgpuv | sha256sum | awk '{print $1}')
PAYLOAD_SHA1_ZCAT=$(zcat vib-extract/amdgpuv | sha1sum | awk '{print $1}')
<payloads>
  <payload name="payload1" type="tgz" size="${PAYLOAD_SIZE}">
      <checksum checksum-type="sha-256">${PAYLOAD_SHA256}</checksum>
      <checksum checksum-type="sha-256" verify-process="gunzip">${PAYLOAD_SHA256_ZCAT}</checksum>
      <checksum checksum-type="sha-1" verify-process="gunzip">${PAYLOAD_SHA1_ZCAT}</checksum>
  </payload>
</payloads>
```

如果存在依赖关系不满足需要修改依赖关系

vmkapi_2_4_0_0对应vmklinux驱动，在ESXi 6.7 以后得版本中以移除

-参考： [vmkapi version removal and Installing/upgrading implication with ESXi 7.0](https://knowledge.broadcom.com/external/article/318024/vmkapi-version-removal-and-installingupg.html)

- (3) 压制 vib

```bash
cd ..
ar r AMD_bootbank_amdgpuv_1.05-1OEM.650.0.0.4598673.vib vib-extract/descriptor.xml vib-extract/sig.pkcs7 vib-extract/amdgpuv
```

- (4) 解压 meta

```bash
 mkdir metadata
 unzip metadata.zip -d metadata
 cd metadata
```

- (5) 修改 `vmware.xml`

```xml
VIB_PATH="../vib20/amdgpuv/AMD_bootbank_amdgpuv_1.06-1OEM.800.0.0.23305546.vib"
VIB_SIZE=$(stat -c %s ${VIB_PATH})
VIB_SHA256=$(sha256sum ${VIB_PATH} | awk '{print $1}')
<relativePath>${VIB_PATH}</relativePath>
<packedSize>${VIB_SIZE}</packedSize>
<checksum>
  <checksumType>sha-256</checksumType> <checksum>${VIB_SHA256}</checksum>
</checksum>
```

- (6) 修改 `metadata/bulletins/VMW-ESX-6.5.0-amdgpuv-1.05.xml`
  
  - `<vibID>AMD_bootbank_amdgpuv_1.06-1OEM.800.0.0.23305546.vib</vibID>`

- (7) 修改 `metadata/vibs/amdgpuv--1652383825.xml`

```xml
<relative-path>${VIB_PATH}</relative-path>
<packed-size>${VIB_SIZE}</packed-size>
<checksum checksum-type="sha-256">${VIB_SHA256}</checksum>

<payload name="amdgpuv" type="vgz" size="${PAYLOAD_SIZE}">
    <checksum checksum-type="sha-256">${PAYLOAD_SHA256}</checksum>
    <checksum checksum-type="sha-256" verify-process="gunzip">${PAYLOAD_SHA256_ZCAT}</checksum>
    <checksum checksum-type="sha-1" verify-process="gunzip">${PAYLOAD_SHA1_ZCAT}</checksum>
</payload>
```

- (8) 创建 zip 包

```bash
cd metadata
zip -r ../metadata.zip *
cd ..
zip -r ../VMW-ESX-6.5.0-amdgpuv.zip *
```

## 四、重装ESXi系统

### 0. 关于虚拟闪存 OSData

- 在5s倒计时画面按下 Shift+O

```bash
runweasel cdromBoot autoPartitionOSDataSize=10240
```

### 1. 关于 ESXi 8.0 分区说明

ESXi 引导设备由多个分区组成。ESX-OSDATA 分区是引导分区之一，对 ESX 操作非常重要。OSData 包含作为关键区域的 VMTools 和暂存区域。

SD 卡在下一个主要版本中不可持续的一些原因是：

- 对系统存储的读取/写入继续增长，对 ESX-OSDATA 分区的读取/写入。OSDATA 分区是一个关键组件，需要始终可用，并且在重新启动后保持持久性。随着 vSAN 和 NSX 等服务和应用程序的发展，OSDATA 将以多种方式使用。OSDATA用于存储一些运行时状态，以及用于探测的备份项目，如配置、时间戳等。对 OSDATA 上其他区域（例如 VMTools 和 scratch 部分）的访问也将增加。随着每个新 vSphere 版本的发布，更多功能将开始依赖于 OSDATA 分区。

- SD 卡无法继续满足性能要求和 IO 负载。例如，对暂存区域的写入要求一直在增长。另一个问题是 IO 的高频率，带有日志或跟踪等突发。

- 没有办法可靠地检查和监控 SD 卡的耐用性，因为这些设备通常不支持诊断数据。磨损问题和剩余的耐久性或使用寿命可能不会被发现。此外，不仅写入，而且读取也会导致磨损问题。

- SD/USB 设备容易随着时间的推移而磨损，因此容易出现故障，它们不是为企业级用例设计的。

## 五、虚拟机安装

### 1. Windows11

- 跳过 TPM 检测

在 Windows 11 安装界面按 Shift + F10 打开命令行界面，执行如下命令：

```bash
REG ADD HKLM\SYSTEM\Setup\LabConfig /v BypassTPMCheck /t REG_DWORD /d 1
REG ADD HKLM\SYSTEM\Setup\LabConfig /v BypassSecureBootCheck /t REG_DWORD /d 1
```

- 跳过用户登录

新电脑开机在选择语言的界面按shift+F10弹出cmd窗口。在运行窗口里输入 `oobe\BypassNRO.cmd` 回车后电脑会重启。

- 升级 Win11 绕过 CPU 限制（可选）

```bash
REG ADD HKLM\SYSTEM\Setup\MoSetup /v AllowUpgradesWithUnsupportedTPMOrCPU /t REG_DWORD /d 1
```

## 六、风扇转速

### 1. 指令

### 2. 下载风扇控制客户端

dell_fans_controller_v1.0.0

## 七、0C63DV 万兆网卡解锁及配置

### 1.  场景

- 可识别为pcie设备，但不识别为网卡

```bash
root@ubuntu-ai:~/unlock-network-scripts# lspci | grep -i network
03:03.0 Ethernet controller: Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection (rev 01)
03:03.1 Ethernet controller: Intel Corporation 82599ES 10-Gigabit SFI/SFP+ Network Connection (rev 01)
```

- 检索 `ixgbe` 驱动日志查看故障原因

```bash
root@ubuntu-ai:~/unlock-network-scripts# dmesg | grep ixgbe
[    8.122078] ixgbe: Intel(R) 10 Gigabit PCI Express Network Driver
[    8.122729] ixgbe: Copyright (c) 1999-2016 Intel Corporation.
[    8.123894] ixgbe 0000:03:03.0: enabling device (0000 -> 0002)
[    8.222056] ixgbe 0000:03:03.0: failed to load because an unsupported SFP+ or QSFP module type was detected.
[    8.222658] ixgbe 0000:03:03.0: Reload the driver after installing a supported module.
[    8.264807] ixgbe: probe of 0000:03:03.0 failed with error -95
[    8.265496] ixgbe 0000:03:03.1: enabling device (0000 -> 0002)
[    8.363465] ixgbe 0000:03:03.1: failed to load because an unsupported SFP+ or QSFP module type was detected.
[    8.364153] ixgbe 0000:03:03.1: Reload the driver after installing a supported module.
[    8.372768] ixgbe: probe of 0000:03:03.1 failed with error -95
```

### 2. 解决方案

#### 2.1 解除网卡识别限制

- 在ESXi中开启网卡直通，将2张网卡直通至ubuntu24.04中

- 执行以下指令卸载内核驱动程序，使用选项`allow_unsupported_sfp=1`加载驱动程序。

```bash
rmmod ixgbe
modprobe ixgbe allow_unsupported_sfp=1
# 对于多个网络接口
modprobe ixgbe allow_unsupported_sfp=1,1,1,1
```

- （可选）持久化

打开 `/etc/default/grub` 并找到 `GRUB_CMDLINE_LINUX_DEFAULT=` 后添加以下参数

```bash
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash ixgbe.allow_unsupported_sfp=1"
```

保存并重启

```bash
update-grub
reboot now
```

#### 2.2 解锁原厂SFP限制

- 查看网卡信息

```bash
ls /sys/class/net/ | grep -v "`ls /sys/devices/virtual/net/`"
```

- 配置脚本

```python
#!/usr/bin/env python3

import os
import subprocess
import sys

try:
    intf = sys.argv[1]
except IndexError:
    print("%s <interface>" % sys.argv[0])
    sys.exit(255)

try:
    with open("/sys/class/net/%s/device/vendor" % intf) as f:
        vdr_id = f.read().strip()

    with open("/sys/class/net/%s/device/device" % intf) as f:
        dev_id = f.read().strip()
except IOError:
    print("Can't read interface data.")
    sys.exit(2)

if vdr_id not in ('0x8086') or dev_id not in ('0x10fb', '0x154d'):
    print("Not a recognized Intel x520 card.")
    sys.exit(3)


output = subprocess.check_output(['ethtool', '-e', intf, 'offset', '0x58', 'length', '1']).decode('utf-8')

val = output.strip().split('\n')[-1].split()[-1]
val_bin = int(val, 16)

print("EEPROM Value at 0x58 is 0x%s (%s)" % (val, bin(val_bin)))
if val_bin & 0b00000001 == 1:
    print("Card is already unlocked for all SFP modules. Nothing to do.")
    exit(1)
if val_bin & 0b00000001 == 0:
    print("Card is locked to Intel only SFP modules. Patching EEPROM...")
    new_val = val_bin | 0b00000001
    print("New EEPROM Value at 0x58 will be %s (%s)" % (hex(new_val), bin(new_val)))

magic = "%s%s" % (dev_id, vdr_id[2:])
cmd = ['ethtool', '-E', intf, 'magic', magic, 'offset', '0x58', 'value', hex(new_val), 'length', 1]
print("Running {}".format(cmd))
cmd = ' '.join(map(str, cmd))
os.system(cmd)
print("Reboot the machine for changes to take effect...")
```

- 执行脚本



## 参考资料

- 苏洋博客

https://soulteary.com/2023/01/29/how-to-easily-create-and-install-a-custom-esxi-image.html

- 下载地址

[index - powered by h5ai v0.30.0 (https://larsjung.de/h5ai/)](https://cios.dhitechnical.com/VMware/VMware%20vSphere%208/VMware%20ESXi%208/)

- 丁辉的博客下载地址

[VMware常用软件ISO下载汇总（2024年9月更新） &#8211; 丁辉博客](https://www.dinghui.org/vmware-iso-download.html)

- 直通说明

[[VMware]ESXI下硬盘的两种直通方式 - chenlife - 博客园](https://www.cnblogs.com/smartlife/articles/17287900.html)

- v-front社区插件（废弃）

[V-Front VIBSDepot Wiki](https://vibsdepot.v-front.de/wiki/index.php/Welcome)

https://www.v-front.de/

- flings 社区（NVME、网卡驱动讨论）

https://community.broadcom.com/developer-portal/communities/communityhomeblogs

- flings 文件服务器（NVME、网卡驱动下载）

[Index of /26/items/flings.vmware.com/Flings/](https://ia601806.us.archive.org/26/items/flings.vmware.com/Flings)

- 博通 Powercli 安装指南

[PowerCLI Installation Guide](https://developer.broadcom.com/powercli/installation-guide)

- 戴尔官方提供自定义ESXi镜像

[VMware ESXi 8.0U2 | Driver Details | Dell US](https://www.dell.com/support/home/en-us/drivers/driversdetails?driverid=p3h74)

https://drivers.amd.com/relnotes/mxgpu-setup-guide-part2-advanced-vmware-mxgpu-setup.pdf

- 7150x2 驱动

[FirePro™ S7150 X2 Drivers](https://www.amd.com/en/support/downloads/drivers.html/graphics/firepro/firepro-s-series/firepro-s7150-x2.html)

- 自定义 ESXi 8 vib

https://williamlam.com/2023/07/creating-a-custom-vib-for-esxi-8-x.html

https://www.yellow-bricks.com/2011/11/29/how-to-create-your-own-vib-files/

- Boot UEFI 使用 nvme 固态

https://winraid.level1techs.com/t/solved-no-nvme-booting-with-dell-poweredge-r730/93347/16

- R730XD 万兆网卡 0C63DV 解锁 原厂SFP限制

https://www.bilibili.com/read/cv34180390/

https://www.bilibili.com/read/cv25528637/

- R730 夹层网卡区分

https://www.bilibili.com/read/cv26404239/?from=search&spm_id_from=333.337.0.0
