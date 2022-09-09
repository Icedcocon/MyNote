# 1 操作系统配置

### 1.1 登录root账户

- ubuntu server 20.04 默认root用户密码为空，不能登录，因此需要利用创建的普通用户的sudo权限，修改root用户密码。（ps：ubuntu允许弱密码）

```bash
sudo passwd root
#输入新密码
su - root
```

### 1.2 使用SSH远程登录root账户

- ubuntu server 20.04 默认ssh中的配置为不允许root用户远程登录，因此需要修改/etc/ssh/sshd_config中的配置

```bash
sed -ri 's/#PermitRootLogin.*/PermitRootLogin yes/g' /etc/ssh/sshd_config
systemctl restart sshd.service
```

### 1.3 更换apt源

- ubuntu默认的apt速度较慢可以更换为阿里源

```bash
cp /etc/apt/sources.list /etc/apt/sources.list.bak
sed -ri 's/cn\.archive\.ubuntu\.com/mirrors\.aliyun\.com/g' /etc/apt/sources.list
```

### 1.4 禁用DHCP服务防止IP地址改变

- ubuntu默认会开启IPV4 DHCP服务获取IP地址，因此每次通过VMware开启虚拟机IP地址都会发生改变。

```bash
cp /etc/netplan/*.yaml /etc/netplan/$(basename /etc/netplan/*.yaml).bak
cat > /etc/netplan/$(basename /etc/netplan/*.yaml) <<-EOF
# This is the network config written by 'subiquity'
network:
  ethernets:
    ens33:
      dhcp4: False
      dhcp6: False
      addresses:
              - 172.16.72.129/24
      gateway4: 172.16.72.2
      nameservers:
              addresses: [114.114.114.114, 8.8.8.8]
  version: 2
EOF

netplan try
```

### 1.5 apt用法及定制

- 常见用法

```bash
apt install {name}   # 安装软件， apt install name=version
apt depends {name}   # 查看文件所需依赖
apt remove {name}    # 卸载软件
apt purage {name}    # 移除安装包及配置文件
apt update           # 刷新索引缓存
apt search {name}    # 搜索应用

apt-cache madison {name}   # 查看仓库中可供下载的版本
apt-cache show {name}      # 查看详细信息
apt-cache depends {name}   # 查看文件所需依赖

apt-get --download-only install {name}    # 将安装包及其依赖下载到本地
```

- 由于apt-get下载deb包时不能指定下载路径，默认下载到`/var/cache/apt/archives`，因此需要使用脚本辅助：

```bash
#! /bin/bash
apt-get clean
apt-get --download-only install $1
cp /var/cache/apt/archives/*.deb .
apt-get clean
```

# 2. ntp服务

### 1.1 安装ntp服务

- ubuntu server 20.04 默认使用time-daemon服务，该服务与ntp冲突导致其不能被dpkg正确安装，需要将ntp安装包放置在`/var/cache/apt/archives/`目录下，使用apt-get install安装。
  
  - 类似time-daemon这样的软件包被称为Virtual packages，不能被直接删除
  
  - “Virtual packages”是只包含对其他packages的引用的packages，或者是只包含自定义配置文件的packages。

```bash
sudo timedatectl set-ntp no

ssh root@${ip} "dpkg -i $AIS_1001_BASE_PATH/deb/ntp/*.deb"
# 改为
ssh root@${ip} "apt-get clean"
ssh root@${ip} "cp $AIS_1001_BASE_PATH/deb/ntp/*.deb /var/cache/apt/archives/"
ssh root@${ip} "apt-get install -y ntp"
ssh root@${ip} "apt-get clean"
```

### 1.2 修改ntpd=>ntp crond=>cron

- centos中的cornd.service在ubuntu中变为cron.service

- centos中的ntpd.service在ubuntu中变为ntp.service

```bash
sed -ri 's/crond/cron/g' ais.sh
sed -ri 's/ntpd/ntp/g' ais.sh
```

### 1.3 取消keys /etc/ntp/key

- ntp除允许使用restrict进行权限管理外，还可以通过为客户端发送秘钥的方式进行验证，这里的key文件中为空，因此可以注释掉该行。

```bash
sed -ri 's/keys \/etc\/ntp\/keys/#keys \/etc\/ntp\/keys/g' config/ntp.conf
```

### 1.4  syntax error in /etc/ntp.conf line 46, column 18

- 第46行代码`fudge 127.127.1.0 startum 8`重复

```bash

```

### 1.4 getconfig: Couldn't open </etc/ntp/crypto/pw>

- `/etc/ntp/crypto/pw`文件为空，可能为密钥认证中的公钥，可以去掉该行代码

```bash
sed -ri 's/includefile \/etc\/ntp\/crypto\/pw/#includefile \/etc\/ntp\/crypto\/pw/g' config/ntp.conf
```
