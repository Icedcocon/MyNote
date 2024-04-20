# JPTV-box-RK3566-Armbain-Waydroid

## 安装步骤

### 一、操作系统下载地址

- 仓库地址 [Releases · ophub/amlogic-s9xxx-armbian · GitHub](https://github.com/ophub/amlogic-s9xxx-armbian/releases)

```bash
wget https://github.com/ophub/amlogic-s9xxx-armbian/releases/download/Armbian_bookworm_save_2024.03/Armbian_24.5.0_rockchip_jp-tvbox_bookworm_6.1.82_server_2024.03.16.img.gz
```

### 二、

#### 2.1 换源

```bash
sed -ri  's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
apt update
apt install curl ca-certificates vim -y
curl https://repo.waydro.id | sudo bash
apt install waydroid -y


#git clone https://ghproxy.net/https://github.com/choff/anbox-modules.git
#cd anbox-modules
#bash -x INSTALL.sh
```

### 参考资料

[Problems installing waydroid - missing &quot;binder&quot; kernel module - Software, Applications, Userspace - Armbian Community Forums](https://forum.armbian.com/topic/29396-problems-installing-waydroid-missing-binder-kernel-module/)

https://forum.radxa.com/t/waydroid-on-armbian-how-to-install-it-properly/14243
