# 1 Ubuntu部署KVM

## 1.1 准备工作

运行KVM前，需要确定处理器是否支持硬件虚拟化，Intel或AMD处理器分别称其为 `VT-x` 和 `AMD-V`

```bash
# (1) 普通环境
egrep -c '(vmx|svm)' /proc/cpuinfo
# 为 `0` 表明处理器不支持硬件虚拟化。
# `1` 或以上责表示处理器支持，但是依然需要在BIOS中开启。

# (2) 操作系统使用了XEN内核
# 需要使用如下方法:
cat /sys/hypervisor/properties/capabilities
# 同样需要在输出中看到 `hvm` 标记。

# (3) 安装了 `cpu-checker` 软件包（包括`cpu-checker` 和 `msr-tools`）
# 可以使用 `kvm-ok` 命令:
kvm-ok
# 正常
INFO: /dev/kvm exists
KVM acceleration can be used
# 依然可以运行虚拟机，但是没有KVM扩展支持则运行缓慢。
INFO: Your CPU does not support KVM extensions
KVM acceleration can NOT be used
```

## 1.2 安装KVM

### 安装必要软件包

- Ubuntu 18.10及以上版本:
  
  ```bash
  sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst
  ```

- Ubuntu 16.04及以上版本:
  
  ```bash
  sudo apt install qemu-kvm libvirt-bin virtinst
  ```
  
  备注

我的安装命令中附加安装了 `virtinst` 工具包，原因是我习惯于redhat提供的 `virt-install` 安装工具

Ubuntu文档建议的安装方法和我上述不同：

- Lucid (10.04) 及以后版本:
  
  ```bash
  sudo apt-get install qemu-kvm libvirt-bin ubuntu-vm-builder bridge-utils
  ```

- Karmic (9.10) 或早期版本:
  
  ```bash
  sudo aptitude install kvm libvirt-bin ubuntu-vm-builder bridge-utils
  ```
  
  我做了修订是因为: `ubuntu-vm-builder` 命令行工具提供构建虚拟机，这个工具并不好用，所以我还是使用 `virt-install` ( `virtinst` 软件包 )

安装的软件包说明:

> - `libvirt-bin` / `libvirt-daemon-system` 提供 `libvirtd` 用于通过libvirt管理qemu和kvm
> 
> - 后端使用 `qemu-kvm` （早期Kamic及更早版本使用 `kvm` ）
> 
> - `bridge-utils` 提供虚拟机网络的网桥

### 添加用户到用户组

- Karmic(9.10)及以后版本（但不包括14.04 LTS）需要确保用户已经添加到组 `libvirt` 中:
  
  ```bash
  sudo adduser `id -un` libvirt
  ```
  
  然后需要重新登陆系统以便 `libvirt` 用户组成员身份生效。这个组的成员可以运行虚拟机。

- Karmic(9.10)之前版本加入 `kvm` 组:
  
  ```bash
  sudo adduser `id -un` kvm
  ```

- 检查:
  
  ```bash
  $ virsh list --all
  
  Id   Name   State
  --------------------
  ```
  
  如果看到报错，例如无法访问sock文件，可以检查 `/var/run/libvirt/libvirt-sock` 文件权限:
  
  ```bash
  $ sudo ls -la /var/run/libvirt/libvirt-sock
  srw-rw---- 1 root libvirt 0 Oct 12 15:51 /var/run/libvirt/libvirt-sock
  ```
  
  上述 `libvirt-sock` 文件对于 `libvirt` 组用户是可以读写执行的，所以才能够以普通用户身份运行 `virsh` 命令。

此外可能在创建虚拟机时遇到问题，则检查 `kvm` 设备的属主:

```bash
$ ls -lh /dev/kvm
crw-rw---- 1 root kvm 10, 232 Oct 12 04:05 /dev/kvm
```

可以看到 `kvm` 设备的组属主是 `kvm` 用户组，则需要调整成 `libivrt` 组（因为前面我们将自己的账号放入了 `libvirt` 组），或者将自己账号再放入到 `kvm` 组:

```bash
sudo adduser `id -un` kvm
```

注意：如果你采用修改 `/dev/kvm` 设备属主，则需要重新启动内核模块:

```bash
rmmod kvm
modprobe -a kvm
```

## 虚拟机bridge网络

上述创建虚拟机都采用了 `--network bridge:virbr0` 参数，这个参数是libvirt NAT型网络，设置简单，但是不方便对外提供服务，并且性能不如libvirt 网桥型网络。为了方便模拟生产环境，我在服务器内部管理网段 `192.168.6.x` 采用bridge网络，并且采用Systemd Networkd服务创建网桥 `br0` 。

### 创建网桥br0

- 修改 `/etc/netplan/00-installer-config.yaml` 中的配置文件

```bash
network:
  ethernets:
    enp7s0:
      dhcp4: False
      dhcp6: False
  version: 2

  bridges:
    br0:
      interfaces: [enp7s0]
      dhcp4: False
      addresses:
      - 192.168.5.3/24
      routes:
      - to: default
        via: 192.168.5.1
      nameservers:
        addresses: [114.114.114.114, 8.8.8.8]
```

- 执行`brctl show`查看是否存在`br0`网桥

111

### 修订libvirt配置绑定br0

- 执行 `virsh edit sles12-sp3` 修订虚拟机配置:

```html
<interface type='bridge'>
  <mac address='52:54:00:00:91:62'/>
  <source bridge='virbr0'/>
  <model type='virtio'/>
  <address type='pci' domain='0x0000' bus='0x01' slot='0x00' function='0x0'/>
</interface>

<!--修改成:-->

<interface type='bridge'>
  <mac address='52:54:00:00:91:62'/>
  <source bridge='br0'/>
  <model type='virtio'/>
  <address type='pci' domain='0x0000' bus='0x01' slot='0x00' function='0x0'/>
</interface>
<!-- 也就是只需要修改 `<source bridge='xxx'>` 就可以修改绑定的网桥-->
```

```bash
# - 重启虚拟机:
virsh shutdown sles12-sp3
virsh start sles12-sp3

# - 通过VNC登陆，修订网络配置
```

```bash
virt-install \
  --network bridge:virbr0 \
  --name ubuntu18.04 \
  --ram=2048 \
  --vcpus=1 \
  --os-type=ubuntu18.04 \
  --disk path=/var/lib/libvirt/images/ubuntu18.04.qcow2,format=qcow2,bus=virtio,cache=none,size=16 \
  --graphics none \
  --location=http://mirrors.163.com/ubuntu/dists/bionic/main/installer-amd64/ \
  --extra-args="console=tty0 console=ttyS0,115200"
```
