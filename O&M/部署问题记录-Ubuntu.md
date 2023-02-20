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
# Ubuntu20.04/18.04配置
cp /etc/netplan/*.yaml /etc/netplan/$(basename /etc/netplan/*.yaml).bak
cat > /etc/netplan/$(basename /etc/netplan/*.yaml) <<-EOF
# This is the network config written by 'subiquity'
network:
  ethernets:
    # 这里要改对应的网卡名
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

```bash
# Ubuntu22.04配置
cp /etc/netplan/*.yaml /etc/netplan/$(basename /etc/netplan/*.yaml).bak
cat > /etc/netplan/$(basename /etc/netplan/*.yaml) <<-EOF
# This is the network config written by 'subiquity'
network:
  ethernets:
    # 这里要改对应的网卡名
    ens33:
      dhcp4: False
      dhcp6: False
      addresses:
      - 192.168.160.100/20
      routes:
      - to: default
        via: 192.168.160.1
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
apt --fix-broken install      # 自动修复依赖关系

apt-cache madison {name}   # 查看仓库中可供下载的版本
apt-cache show {name}      # 查看详细信息
apt-cache depends {name}   # 查看文件所需依赖

apt-get --download-only install {name}    # 将安装包及其依赖下载到本地
apt-get install {name} --reinstall        # 重新安装
apt-get autoremove                        # 自动清理已安装但不被依赖的程序
apt-get install check                # 查看未被满足的依赖关系

dpkg -C                    # 检查已被解开但尚未配置的安装包(常用于dpkg安装冲突)
dpkg --force-overwrite -i {name}  # 高风险，强制覆盖
# 强制覆盖用于--fix-broken已经将安装包下载到/var/cache/apt/archives下
# 但因冲突未被安装的情况
dpkg --configure -a        # dpkg被中断后使用
```

- 由于apt-get下载deb包时不能指定下载路径，默认下载到`/var/cache/apt/archives`，因此需要使用脚本辅助：

```bash
#! /bin/bash
apt-get clean
apt-get --download-only install $1
cp /var/cache/apt/archives/*.deb .
apt-get clean

# 反向操作
apt-get clean
cp ./*deb /var/cache/apt/archives/
apt-get install $1
apt-get clean
```

# 2. ntp服务

### 2.1 安装ntp服务

- ubuntu server 20.04 默认使用time-daemon服务，该服务与ntp冲突导致其不能被dpkg正确安装，需要将ntp安装包放置在`/var/cache/apt/archives/`目录下，使用apt-get install安装。
  
  - 类似time-daemon这样的软件包被称为Virtual packages，不能被直接删除
  
  - “Virtual packages”是只包含对其他packages的引用的packages，或者是只包含自定义配置文件的packages。

```bash
sudo timedatectl set-ntp no

ssh root@${ip} "dpkg -i $AIS_1001_BASE_PATH/deb/ntp/*.deb"
# 改为
ssh root@${ip} "apt-get clean"
ssh root@${ip} "cp $AIS_1001_BASE_PATH/deb/ntp/*.deb /var/cache/apt/archives/"
ssh root@${ip} "apt-get install -y ntp="
ssh root@${ip} "apt-get clean"
```

### 2.2 修改ntpd=>ntp crond=>cron

- centos中的cornd.service在ubuntu中变为cron.service

- centos中的ntpd.service在ubuntu中变为ntp.service

```bash
sed -ri 's/crond/cron/g' ais.sh
sed -ri 's/ntpd/ntp/g' ais.sh
```

### 2.3 ntp正常启动但配置文件报错

- 错误1：ubuntu系统中默认不生成`keys /etc/ntp/key`文件，改文件用于ntp秘钥认证，可删除该行配置；

- 错误2：`/etc/`配置`fudge 127.127.1.0 startum 8`

- 错误3：公钥`/etc/ntp/crypto/pw`不存在，处理方式同错误1.

```bash
sed -ri 's/keys \/etc\/ntp\/keys/#keys \/etc\/ntp\/keys/g' config/ntp.conf
# 去掉第45、46行fudge 127.127.1.0 startum 8
sed -ri 's/includefile \/etc\/ntp\/crypto\/pw/#includefile \/etc\/ntp\/crypto\/pw/g' config/ntp.conf
```

### 2.4 新配置文件

```bash
# 指定误差记录文件
driftfile /var/lib/ntp/drift
# 限制默认IPV4 IPV6 允许获取时间，但禁止查看服务器状态信息
restrict -4 default kod notrap nomodify nopeer noquery limited
restrict -6 default kod notrap nomodify nopeer noquery limited
# 对环回地址不做限制。可以对其约束，但这样会影响对ntp的管理。
restrict 127.0.0.1                  # IPV4本地回环地址
restrict ::1                        # IPV6本地回环地址
# 只是用本地振荡频率计算时间
server 127.127.1.0 # local clock
fudge 127.127.1.0 stratum 8
```

# 3 BIND9 DNS服务

### 3.1 配置文件配置

- centos：
  
  - `/etc/named.conf`：主配置文件。
  
  - `/etc/named.rfc1912.zones`：自定义区域配置文件
  
  - `/etc/sysconfig/named`：是否启动chroot及额外的参数，就由这个文件控制。
  
  - `var/named/`：数据库文件默认放置在这个目录，由`named.conf`指定。
  
  - `var/run/named`：named这支程序执行时默认放置pid-fle在此目录内。
  
  - `/etc/resolv.conf`：文件而非链接

- ubuntu：
  
  - `/etc/bind/named.conf`：主配置文件，包含options、local、default-zones
  
  - `/etc/bind/named.conf.options`：DNS 全局选项配置文件
  
  - `/etc/bind/named.conf.local`：自定义区域配置文件
  
  - `/etc/bind/named.conf.default-zones`：默认区域，例如localhost，其反向和根提示
  
  - `/var/cache/bind`：数据库文件默认放置在这个目录，由`named.conf`指定。
  
  - `/etc/reslov.conf`符号链接到`/run/systemd/resolve/stub-resolv.conf`，但netplan影响`/run/systemd/resolve/resolv.conf`文件。
    
    - 在 `/run/systemd/resolve/stub-resolv.conf` 设置文件中会将 DNS 服务器设置为 `127.0.0.53`，这一个位址就是 `systemd-resolved` 在本机所提供的 DNS 服务器，这样就可以将 `systemd-resolved` 服务与既有的 `/etc/ resolv.conf` 集成在一起了。（PS: systemd-resolved服务与bind9类似，开启会占用53端口）

```bash
# 将/etc/named.rfc1912.zones替换为/etc/bind/named.conf.default-zones
sed -ri 's/etc\/named\.rfc1912\.zones/etc\/bind\/named\.conf\.local/g' 3rd/bind-dns/setup.sh
# 将/etc/named/替换为/etc还是var?/cache/bind/
sed -ri '26,30s/named/cache\/bind/g' 3rd/bind-dns/setup.sh
# 将named.conf替换为named.conf.options
sed -ri '32,34s/named\.conf/named\.conf\.options/g' 3rd/bind-dns/setup.sh
sed -ri '32,34s/etc/etc\/bind/g' 3rd/bind-dns/setup.sh
# 将cache/bind替换为bind
sed -ri '' 3rd/bind-dns/setup.sh
# 将文件3rd/bind-dns/name.conf替换为3rd/bind-dns/name.conf.options
```

### 3.2 文件对比

```bash
#################### Centos 7.7 /etc/named.conf ################
options {
        listen-on port 53 { any; };
        listen-on-v6 port 53 { ::1; };
        directory       "/var/cache/bind";
        version         "[no about your business]";
        dump-file       "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        recursing-file  "/var/named/data/named.recursing";
        secroots-file   "/var/named/data/named.secroots";
        allow-query     { any; };
        recursion no;
        dnssec-enable yes;
        dnssec-validation yes;
        bindkeys-file "/etc/named.root.key";
        managed-keys-directory "/var/named/dynamic";
        pid-file "/run/named/named.pid";
        session-keyfile "/run/named/session.key";
};

logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};

zone "." IN {
        type hint;
        file "named.ca";
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";

#################### Ubuntu20.04 /etc/bind/named.conf ####################
include "/etc/bind/named.conf.options";
include "/etc/bind/named.conf.local";
include "/etc/bind/named.conf.default-zones";

# /etc/bind/named.conf.options
options {
        directory "/var/cache/bind";
        dnssec-validation auto;
        listen-on-v6 { any; };
};

#################### Centos 7.7 /etc/named.rfc1912.zones ################

zone "localhost.localdomain" IN {
        type master;
        file "named.localhost";
        allow-update { none; };
};

zone "localhost" IN {
        type master;
        file "named.localhost";
        allow-update { none; };
};

zone "AIS_40_CLUSTER_DOMAIN" IN {
        type master;
        file "AIS_40_CLUSTER_DOMAIN.zone";
};

zone "1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa" IN {
        type master;
        file "named.loopback";
        allow-update { none; };
};

zone "1.0.0.127.in-addr.arpa" IN {
        type master;
        file "named.loopback";
        allow-update { none; };
};

zone "0.in-addr.arpa" IN {
        type master;
        file "named.empty";
        allow-update { none; };
};

############## Ubuntu20.04 /etc/bind/named.conf.default-zones ##############
zone "." {
        type hint;
        file "/usr/share/dns/root.hints";
};

zone "localhost" {
        type master;
        file "/etc/bind/db.local";
};

zone "127.in-addr.arpa" {
        type master;
        file "/etc/bind/db.127";
};

zone "0.in-addr.arpa" {
        type master;
        file "/etc/bind/db.0";
};

zone "255.in-addr.arpa" {
        type master;
        file "/etc/bind/db.255";
};
```

### 3.3 替换3rd/bind-dns/named.conf配置文件

```bash
################# 替换为 3rd/bind-dns/named.conf.options #############
options {
        listen-on port 53 { any; };
        listen-on-v6 port 53 { ::1; };
        directory       "/var/cache/bind";                           #
        allow-query     { any; };
        recursion no;
        dnssec-validation auto;
};
```

##### 生成秘钥

`dnssec-keygen -a HMAC-MD5 -b 128 -n HOST ruyi-key`

`dnssec-keygen -a RSASHA1 ruyi-key`

### 3.4 配置不同域名不同DNS服务器

- Ubuntu20.04及18.04相较于CentOS7.7的NetworkManager服务配置不同，其配置文件位于`/etc/NetworkManager/NetworkManager.conf`

- `/etc/resolv.conf`文件中设置`options rotate`参数不能解决该问题，推测根据域名的哈希值映射到固定位置域名服务器(可能不是第一个)。

- 参考链接  https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/configuring_and_managing_networking/using-different-dns-servers-for-different-domains_configuring-and-managing-networking

# 4 Docker

### 4.1 关闭防火墙

- Centos 中防火墙服务为`firewalld.service`，在Ubuntu中为`ufw.service`

```bash
#1 shutdown firewall
echo "1/99 shutdown ufw"
systemctl stop ufw.service
systemctl disable ufw.service
echo ""
```

### 4.2 关闭AppArmor（SeLinux）

- 在ubuntu中与Centos功能类似的组件称为AppArmor

```bash
#2 close apparmor
echo "2/99 shutdown apparmor"
systemctl stop apparmor.service
echo ""
```

### 4.3 更换deb包并修改

- 修改安装脚本

```bash
# rpm/docker
sed -ri 's/yum install -y \.\.\/rpm\/docker\/\*\.rpm/dpkg -i \.\.\/deb\/docker\/\*\.deb/g' shell/ais-install.sh
# 移除
sed -ri 's/yum remove -y kubectl kubeadm kubelet/dpkg -P kubectl kubeadm kubelet/g' shell/ais-install.sh
# rpm/kubernetes
sed -ri 's/yum install -y \.\.\/rpm\/kubernetes\/\*\.rpm/dpkg -i \.\.\/deb\/kubernetes\/\*\.deb/g' shell/ais-install.sh
# 复制dev/kubernetes/kubeadm
sed -ri 's/cp \.\.\/rpm\/kubernetes\/kubeadm \/usr\/bin\/kubeadm/cp \.\.\/deb\/kubernetes\/kubeadm \/usr\/bin\/kubeadm/g' shell/ais-install.sh
# 安装nvidia docker
sed -ri 's/yum install -y \.\.\/rpm\/nvidia-docker\/\*\.rpm/dpkg -i \.\.\/deb\/nvidia-docker\/\*\.deb/g' shell/ais-install.sh
```

- ubuntu18.04和ubuntu20.04的nvidia-docker以及kubernetes不能共用，在20.04中安装会使部分基础动态链接库降级，导致20.04中大部分指令失效。
  - 下载docker-ce
  - 下载nvdia-docker2
  - 下载kubernetes

```bash
# 安装docker-ce
# step 1: 安装必要的一些系统工具
sudo apt-get update
sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
# step 2: 安装GPG证书
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
# Step 3: 写入软件源信息
sudo add-apt-repository "deb [arch=amd64] https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
# Step 4: 更新并安装Docker-CE
sudo apt-get -y update
sudo apt-get -y install docker-ce
# 把docker-ce安装包从/var/cache/apt/archives/中移到当前文件夹

# 安装nvidia-docker
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
            sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2

# 安装kubeadm
apt update && sudo apt install -y apt-transport-https
curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | sudo apt-key add -
vim /etc/apt/sources.list.d/kubernetes.list
# 添加 
deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
sudo apt update
deb-get kubelet=1.20.5-00 kubeadm=1.20.5-00 kubectl=1.20.5-00
```

### 4.4 deb包冲突

- 在安装完docker后再安装kubernetes后产生冲突，在添加docker-ce、nvidia-docker的仓库后直接下载nvidia-docker2，由apt解决依赖冲突。
  
  - docker-ce-cli conflicts with docker.io
  
  - containerd.io conflicts with runc

```bash
# 下载完成后手动将docker-ce和nvidia-docker分开
mv nvidia-docker docker
mv docker/libnvidia-container1_1.10.0-1_amd64.deb nvidia-docker
mv docker/libnvidia-container-tools_1.10.0-1_amd64.deb nvidia-docker
mv docker/nvidia-container-toolkit_1.10.0-1_amd64.deb nvidia-docker
mv docker/nvidia-docker2_2.11.0-1_all.deb nvidia-docker
```

# 5 hadoop

### 5.1 修改脚本

```bash
sed -ri 's/systemctl stop firewalld/systemctl stop ufw\.service/' 3rd/hadoop/setup.sh
sed -ri 's/systemctl disable firewalld/systemctl disable ufw\.service/' 3rd/hadoop/setup.sh
sed -ri 's/echo "2\/10 close selinux"/echo "2\/99 shutdown apparmor"/' 3rd/hadoop/setup.sh
sed -ri '/sed -i s\/SELINUX=enforcing/d' 3rd/hadoop/setup.sh
sed -ri '/setenforce 0/d' 3rd/hadoop/setup.sh
sed -ri 's/getenforce/systemctl stop apparmor.service/' 3rd/hadoop/setup.sh
sed -ri 's/rpm -hiv \.\/rpm\/expect-5\.45.*/dpkg -i deb\/expect\/\*\.deb/g' 3rd/hadoop/setup.sh
sed -ri 's/systemctl restart hadoop/\/usr\/local\/hadoop-3\.2\.2\/sbin\/stop-all\.sh \&\& \/usr\/local\/hadoop-3\.2\.2\/sbin\/start-all\.sh/g' 3rd/hadoop/setup.sh
```

# 6 harbor

### 6.1 修改脚本

```bash
sed -ri 's/systemctl stop firewalld/systemctl stop ufw\.service/' 3rd/harbor/setup.sh
sed -ri 's/systemctl disable firewalld/systemctl disable ufw\.service/' 3rd/harbor/setup.sh
sed -ri 's/echo "2\/15 close selinux"/echo "2\/15 shutdown apparmor"/' 3rd/harbor/setup.sh
sed -ri '/sed -i s\/SELINUX=enforcing/d' 3rd/harbor/setup.sh
sed -ri '/setenforce 0/d' 3rd/harbor/setup.sh
sed -ri 's/getenforce/systemctl stop apparmor.service/' 3rd/harbor/setup.sh
sed -ri 's/yum install -y.*/dpkg -i \.\.\/\.\.\/deb\/docker\/\*\.deb/' 3rd/harbor/setup.sh
sed -ri 's/rpm -hiv \.\/rpm\/expect.*/dpkg -i \.\.\/\.\.\/deb\/expect\/\*\.deb/' 3rd/harbor/setup.sh
```

# 7 MariaDB

### 7.1 下载deb包

- 下载mariadb-server

```bash
deb-get mariadb-server=1:10.3.34-0ubuntu0.20.04.1
```

- MariaDB不能使用dpkg安装，会产生依赖问题，需要使用apt-get安装

```bash
sed -ri '/yum install.*/d' 3rd/mariadb/install/setup.sh
sed -ri '/1\/8 install mariadb/a \
apt-get clean \
cp ../deb/mariadb/*.deb /var/cache/apt/archives/ \
apt-get -y install mariadb-server=1:10.3.34-0ubuntu0.20.04.1 \
apt-get clean' 3rd/mariadb/install/setup.sh

sed -ri 's/rpm -hiv.*/dpkg -i \.\.\/deb\/expect\/\*\.deb/' 3rd/mariadb/install/setup.sh
```

### 7.2 部署脚本修改

- MariaDB的配置文件位置在CentOS中为`/etc/my.cnf`；而在Ubuntu中为`/etc/mysql/my.cnf`

```bash
sed -ri 's/!includedir.*/!includedir \/etc\/mysql\/conf\.d\/\
!includedir \/etc\/mysql\/mariadb\.conf\.d\//' 3rd/mariadb/install/mariadb-5.5.64-offline/my.cnf

sed -ri 's/etc\/my\.cnf/etc\/mysql\/my\.cnf/' 3rd/mariadb/install/setup.sh
sed -ri 's/.*mysql-clients.*/#&/' 3rd/mariadb/install/setup.sh
sed -ri 's/.*client.cnf.*/#&/' 3rd/mariadb/install/setup.sh
```

# 8 LDAP

### 8.0 slapd实现静默安装

- 在ubuntu下安装slapd需要在安装过程中输入Administrator password等信息，且输入过程并非命令行而是存在界面；（expect可能无法处理dpkg的操作。）

- 使用debconf
  
  - 安装slapd，并dpkg-reconfigure手动设置期望密码
  
  - 执行`debconf-show slapd`查看预配置项
  
  - 在脚本中添加

- 使用debconf-set-selections命令后，.ldif文件不再被需要，因此在setup.sh中删除

```bash
########################## 设置预配置项 ##########################
# CN_NAME=admin
# ADMIN_PASSWD=admin
# LDAP_DOT_DOMAIN=ldap.inspur.com
# LDAP_DOMAIN=dc=ldap,dc=inspur,dc=com
# 添加cn的变量
sed -ri '/ADMIN_USERNAME=`echo/a CN_NAME=`echo ${ADMIN_USERNAME#*=}`\
CN_NAME=`echo ${CN_NAME%%,*}`\
sed -ri s/AdminPasswd/$ADMIN_PASSWD/g debconf.conf\
sed -ri s/LdapDotDomain/$LDAP_DOT_DOMAIN/g debconf.conf\
sed -ri s/LdapDomain/$LDAP_DOMAIN/g debconf.conf\
' 3rd/openldap/install/setup.sh
# 
cat > 3rd/openldap/install/debconf.conf <<-EOF
slapd slapd/password1 password AdminPasswd
slapd slapd/password2 password AdminPasswd
slapd slapd/no_configuration select false
slapd slapd/domain password LdapDotDomain
slapd slapd/move_old_database select true
slapd shared/organization password LdapDomain
slapd slapd/purge_database select true
EOF
# 将配置替换为config/ais.cfg中的值
sed -ri '/#3/a cat < debconf.conf | debconf-set-selections' 3rd/openldap/install/setup.sh
# 注释执行.ldif的代码
sed -ri 's/.*ldapadd.*/#&/g' 3rd/openldap/install/setup.sh
sed -ri 's/.*ldapmodify.*/#&/g' 3rd/openldap/install/setup.sh
########################## 查看预配置项 ##########################  
#$ debconf-show slapd
#  slapd/internal/generated_adminpw: (password omitted)
#* slapd/password1: (password omitted)
#  slapd/internal/adminpw: (password omitted)
#* slapd/password2: (password omitted)
#* slapd/no_configuration: false
#* slapd/domain: ldap.inspur.com
#  slapd/password_mismatch:
#  slapd/upgrade_slapcat_failure:
#* slapd/move_old_database: true
#  slapd/dump_database: when needed
#* shared/organization: dc=ldap,dc=inspur,dc=com
#  slapd/unsafe_selfwrite_acl:
#* slapd/purge_database: true
#  slapd/ppolicy_schema_needs_update: abort installation
#  slapd/invalid_config: true
#  slapd/dump_database_destdir: /var/backups/slapd-VERSION

# expect 通配符 转义
#######################################################
```

### 8.1 下载安装包并修改setup.sh安装命令

- 需要expect、openldap、phpldapadmin三个安装包

```bash
mkdir -p 3rd/openldap/deb/openldap
cp -r deb/expect 3rd/openldap/deb
cd 3rd/openldap/deb/openldap && deb-get slapd ldap-utils phpldapadmin
```

- 修改部署脚本的firewalld、selinux以及安装包目录

```bash
sed -ri 's/systemctl stop firewalld/systemctl stop ufw\.service/' 3rd/openldap/install/setup.sh
sed -ri 's/systemctl disable firewalld/systemctl disable ufw\.service/' 3rd/openldap/install/setup.sh
sed -ri 's/echo "2\/11 close selinux"/echo "2\/11 shutdown apparmor"/' 3rd/openldap/install/setup.sh
sed -ri '/sed -i s\/SELINUX=enforcing/d' 3rd/openldap/install/setup.sh
sed -ri '/setenforce 0/d' 3rd/openldap/install/setup.sh
sed -ri 's/getenforce/systemctl stop apparmor.service/' 3rd/openldap/install/setup.sh

sed -ri 's/yum install -y.*/dpkg -i \.\.\/deb\/openldap\/\*\.deb/' 3rd/openldap/install/setup.sh
sed -ri 's/rpm -hiv.*/dpkg -i \.\.\/deb\/expect\/\*\.deb/' 3rd/openldap/install/setup.sh
```

### 8.2 Apache2、phpldapadmin、ldap配置文件修改

- CentOS下的主要配置文件（需要关注的）
  
  - apache2配置文件
    - `/etc/httpd.conf` 主配置文件
    - `/etc/httpd/conf/httpd.conf` 主配置文件另一个位置？
  - phpldapadmin配置文件
    - `/etc/httpd/conf.d/phpldapadmin.conf` phpldapadmin配置文件
    - `/etc/phpldapadmin/config.php` phpldapadmin配置文件
  - ldap 配置文件
    - `/etc/openldap/ldap.conf`
    - rootpwd.ldif
    - domain.ldif
    - basedomain.ldif
  - 数据库文件
    - `/var/lib/ldap/DB_CONFIG` 不确定

- Ubuntu下主要配置文件（需要关注的）
  
  - apache2配置文件
    
    - `/etc/apache2/apache2.conf`
    
    - `/etc/apache2/envvars` 需要的环境变量
  
  - phpldapadmin配置文件
    
    - `/etc/apache2/conf-enabled/phpldapadmin.conf` phpldapadmin配置文件
    
    - `/etc/phpldapadmin/config.php` phpldapadmin配置文件
  
  - ldap 配置文件
    
    - `/etc/ldap/ldap.conf`
  
  - 数据库文件
    
    - 无

- 修改setup.sh中的路径名及配置

```bash
# 修改apache2配置文件名及路径
sed -ri 's/cp httpd.*/cp apache2\.conf \/etc\/apache2\/apache2\.conf/' 3rd/openldap/install/setup.sh
sed -ri 's/httpd\/conf\/httpd\.conf/apache2\/apache2\.conf/g' 3rd/openldap/install/setup.sh

# phpldapadmin配置文件保持默认
#sed -ri '/config phpldapadmin/a sed -ri "/<IfModule mod_alias\.c>/a  Alias /ldapadmin /usr/share/phpldapadmin/htdocs" /etc/apache2/conf-enabled/phpldapadmin.conf' 3rd/openldap/install/setup.sh
sed -ri '/cp phpldapadmin\.conf.*/d' 3rd/openldap/install/setup.sh
sed -ri '/cat \/etc\/httpd\/conf\.d\/phpldapadmin\.conf/d' 3rd/openldap/install/setup.sh

# ubuntu不需要数据库文件进行配置，采用dpkg-reconfigure或者debconf
sed -ri 's/.*DB_CONFIG.*/#&/g'  3rd/openldap/install/setup.sh

# ldap.conf（以及rootpwd.ldif、domain.ldif、basedomain.ldif）配置文件路径修改
sed -ri 's/\/etc\/openldap/\/etc\/ldap/'  3rd/openldap/install/setup.sh
sed -ri 's/\/etc\/openldap/\/etc\/ldap/'  ais.sh.ha
sed -ri 's/\/etc\/openldap/\/etc\/ldap/'  ais.sh.single
sed -ri 's/\/etc\/openldap/\/etc\/ldap/'  ais.sh
```

- 将httpd.conf替换为以下apache2.conf

```bash
##################### /etc/apache2/apache2.conf #####################
cat > 3rd/openldap/install/apache2.conf <<-EOF
#ServerRoot "/etc/apache2"
############## 添加内容 #############
Listen HTTP_PORT                
ServerName LDAP_IP:HTTP_PORT   
###################################
#Mutex file:\${APACHE_LOCK_DIR} default
DefaultRuntimeDir \${APACHE_RUN_DIR}
PidFile \${APACHE_PID_FILE}
Timeout 300
KeepAlive On
MaxKeepAliveRequests 100
KeepAliveTimeout 5
# These need to be set in /etc/apache2/envvars
User \${APACHE_RUN_USER}
Group \${APACHE_RUN_GROUP}
HostnameLookups Off
ErrorLog \${APACHE_LOG_DIR}/error.log
LogLevel warn
IncludeOptional mods-enabled/*.load
IncludeOptional mods-enabled/*.conf
Include ports.conf

#</Directory>
############### 修改内容 ###############
<Directory />
     Options Indexes FollowSymLinks    
     AllowOverride None
     Order deny,allow                         
     Allow from all                    
</Directory>
######################################
<Directory /usr/share>
        AllowOverride None
        Require all granted
</Directory>
<Directory /var/www/>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
</Directory>
AccessFileName .htaccess
<FilesMatch "^\.ht">
        Require all denied
</FilesMatch>

LogFormat "%v:%p %h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" vhost_combined
LogFormat "%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" combined
LogFormat "%h %l %u %t \"%r\" %>s %O" common
LogFormat "%{Referer}i -> %U" referer
LogFormat "%{User-agent}i" agent
IncludeOptional conf-enabled/*.conf
IncludeOptional sites-enabled/*.conf
EOF
```

### 8.4 用户、用户组名称及服务名称修改修改

- 在Centos中用户及用户组名称为ldap，在ubuntu中变为openldap
- 在Centos中的httpd.service 变为 apache2.service

```bash
sed -ri 's/ldap:ldap/openldap:openldap/'  3rd/openldap/install/setup.sh
sed -ri 's/ httpd/ apache2/g' 3rd/openldap/install/setup.sh
```

### 8.5 解决页面显示password_hash存在问题

- 需要将`$servers->setValue('appearance','password_hash','');`注释掉

```bash
sed -ri 's/^\$servers.*password_hash.*/#&/' 3rd/openldap/install/config.php
```

- ubuntu默认配置与Centos配置对比

```bash
#################### ubuntu ##########################
<?php
$config->custom->commands['cmd'] = array(
      'entry_internal_attributes_show' => true,
      'entry_refresh' => true,
      'oslinks' => true,
      'switch_template' => true
);
$config->custom->commands['script'] = array(
      'add_attr_form' => true,
      'add_oclass_form' => true,
      'add_value_form' => true,
      'collapse' => true,
      'compare' => true,
      'compare_form' => true,
      'copy' => true,
      'copy_form' => true,
      'create' => true,
      'create_confirm' => true,
      'delete' => true,
      'delete_attr' => true,
      'delete_form' => true,
      'draw_tree_node' => true,
      'expand' => true,
      'export' => true,
      'export_form' => true,
      'import' => true,
      'import_form' => true,
      'login' => true,
      'logout' => true,
      'login_form' => true,
      'mass_delete' => true,
      'mass_edit' => true,
      'mass_update' => true,
      'modify_member_form' => true,
      'monitor' => true,
      'purge_cache' => true,
      'query_engine' => true,
      'rename' => true,
      'rename_form' => true,
      'rdelete' => true,
      'refresh' => true,
      'schema' => true,
      'server_info' => true,
      'show_cache' => true,
      'template_engine' => true,
      'update_confirm' => true,
      'update' => true
);
$config->custom->appearance['friendly_attrs'] = array(
      'facsimileTelephoneNumber' => 'Fax',
      'gid'                      => 'Group',
      'mail'                     => 'Email',
      'telephoneNumber'          => 'Telephone',
      'uid'                      => 'User Name',
      'userPassword'             => 'Password'
);
$servers = new Datastore();
$servers->newServer('ldap_pla');
$servers->setValue('server','name','My LDAP Server');
$servers->setValue('server','host','127.0.0.1');
$servers->setValue('server','base',array('dc=example,dc=com'));
$servers->setValue('login','auth_type','session');
$servers->setValue('login','bind_id','cn=admin,dc=example,dc=com');
?>


####################### CentOS ###########################
<?php
$config->custom->session['blowfish'] = 'ae06e60c79b23490ae559baf66012ec6';  # Autogenerated for localhost.localdomain
$config->custom->appearance['hide_template_warning'] = true;
$config->custom->appearance['friendly_attrs'] = array(
        'facsimileTelephoneNumber' => 'Fax',
        'gid'                      => 'Group',
        'mail'                     => 'Email',
        'telephoneNumber'          => 'Telephone',
        'uid'                      => 'User Name',
        'userPassword'             => 'Password'
);
$servers = new Datastore();
$servers->newServer('ldap_pla');
$servers->setValue('server','name','Local LDAP Server');
$servers->setValue('server','host','LDAP_IP');
$servers->setValue('server','port',389);
$servers->setValue('server','base',array('LDAP_DOMAIN'));
$servers->setValue('login','auth_type','session');
$servers->setValue('login','bind_id','ADMIN_USERNAME');
$servers->setValue('login','bind_pass','ADMIN_PASSWD');
$servers->setValue('appearance','password_hash','');
$servers->setValue('login','attr','dn');
?>
```

### 8.6 配置cert.sh

- cert.sh与ldap认证有关，不执行并不影响主要功能
- slapd位于/etc/defalut/目录下，而非/etc/sysconfig/，在slapd中配置了`SLAPD_URLS`，而在/etc/defalut/slapd中存在类似选项`SLAPD_SERVICES`这里保持默认会导致636端口不能启动，因此将该步骤改为向/etc/defalut/slapd的SLAPD_SERVICES选项后添加 ldaps:///。

```bash
sed -ri 's/openldap/ldap/' 3rd/openldap/install/cert.sh
sed -ri 's/.*rpm -hiv.*/dpkg -i \.\.\/deb\/expect\/\*\.deb/' 3rd/openldap/install/cert.sh
sed -ri 's/ldap:ldap/openldap:openldap/' 3rd/openldap/install/cert.sh
#sed -ri 's/.*ldapadd.*/#&/g' 3rd/openldap/install/cert.sh
#sed -ri 's/.*ldapmodify.*/#&/g' 3rd/openldap/install/cert.sh

sed -ri '/^TLS_REQCERT_VALUE/a mkdir -p /etc/pki/CA\
mkdir -p /etc/pki/CA/private\
mkdir -p /etc/pki/CA/newcerts\
mkdir -p /etc/ldap/certs' 3rd/openldap/install/cert.sh
sed -ri 's/\.\/demoCA/\/etc\/pki\/CA/g' /usr/lib/ssl/openssl.cnf
# 不复制slapd，但修改/etc/defalut/slapd
sed -ri 's/.*sysconfig.*/sed -ri "s#ldap:\/\/\/ ldapi:\/\/\/\\\"#ldap:\/\/\/ ldapi:\/\/\/\ ldaps:\/\/\/\\\"#" \/etc\/default\/slapd/' 3rd/openldap/install/cert.sh
```

### 8.6 LDAP验证命令

```bash
ldapdelete -x -H ldap://172.16.72.129:389 -D "cn=admin,dc=ldap,dc=inspur,dc=com" -w admin "cn=12345678,cn=default,dc=ldap,dc=inspur,dc=com"
ldapsearch -x -H ldap://172.16.72.129:389 -D "cn=admin,dc=ldap,dc=inspur,dc=com" -w admin cn=12345678
ldapsearch -x -H ldap://172.16.72.129:389 -D "cn=admin,dc=example,dc=com" -w admin cn=12345678
```

# 9 iptables

### 9.1 修改setup.sh安装命令

- Centos为yum remove 应替换为apt-get purge

- Ubuntu默认没有iptables配置文件，需通过iptables-save将规则dump下来，重定向输出到`/etc/network/iptables.up.rules`文件，改文件为iptables-apply指令默认指向文件，可以通过-w选项修改。

- Ubuntu 没有重启iptables的命令，执行iptables-apply生效。

- 默认Ubuntu iptables的规则会在重启服务器后清空，需要使用iptables-restore命令重新加载规则。因此可以在`/etc/network/interfaces`里写入以下指令，实现开机生效`pre-up iptables-restore < /etc/network/iptables.up.rules`

```bash
# 无需安装iptables
sed -ri 's/.*yum.*/#&/g' 3rd/iptables/setup.sh

# 修改配置文件路径
sed -ri 's/sysconfig\/iptables/network\/iptables\.up\.rules/g' 3rd/iptables/setup.sh
# iptables-save > /etc/network/iptables.up.rules
sed -ri 's/systemctl status iptables/iptables -L/' 3rd/iptables/setup.sh

# 修改路径名
sed -ri 's/sysconfig\/iptables/network\/iptables\.up\.rules/g' 3rd/iptables/config_port_filter.sh
# 
sed -ri 's/.*systemctl restart iptables\.service/TMP_SCRIPT=tmp.sh\
echo  "\#! \/usr\/bin\/expect">\$TMP_SCRIPT\
echo  "spawn iptables-apply">>\$TMP_SCRIPT\
echo  "expect \"\*establish NEW connections\*\"">>$TMP_SCRIPT\
echo  \"send y\\r\">>\$TMP_SCRIPT\
echo  "interact">>\$TMP_SCRIPT\
chmod +x \$TMP_SCRIPT\
\/usr\/bin\/expect \$TMP_SCRIPT\
rm -rf \$TMP_SCRIPT/g'  3rd/iptables/config_port_filter.sh
# 开机自启 & 关机保存
sed -ri 's/.*systemctl enable iptables\.service/cat > \/etc\/network\/interfaces <<-EOF\
pre-up iptables-restore < \/etc\/network\/iptables\.up\.rules  #启动自动调用已存储的iptables\
post-down iptables-save > \/etc\/network\/iptables\.up\.rules  #关机时，把当前iptables 储存\
EOF/g'  3rd/iptables/config_port_filter.sh
```

#### 9.2 iptables关闭

# 10 Haproxy和KeepAlive

### 10.1 更换安装包

- 只需要下载安装包及修改安装指令即可

```bash
sed -ri 's/yum install -y/dpkg -i/' shell/ais-high-available.sh
sed -ri 's/rpm\/keepalived.*/deb\/keepalived\/\*\.deb/' shell/ais-high-available.sh
sed -ri 's/rpm -hiv/dpkg -i/' shell/ais-high-available.sh
sed -ri 's/rpm\/haproxy.*/deb\/haproxy\/\*\.deb/' shell/ais-high-available.sh
```

# 11 Nvidia-driver GCC

### 11.1 替换gcc路径中的安装包

- gcc中存在

```bash
sed -ri 's/yum localinstall -y.*/dpkg -i gcc\/\*\.deb/' 3rd/nvidia-driver/install-gpu-driver.sh
sed -ri 's/yum localinstall -y.*/dpkg -i gcc\/\*\.deb/' 3rd/nvidia-driver/install-gpu-driver-mimimize.sh
```

### 安装包记录

```bash
./deb/*
./config/?????
# ./3rd/bind-dns/deb/
# ./3rd/bind-dns/setup.sh
./3rd/bind-dns/*
./shell/ais-install.sh
./3rd/hadoop/setup.sh
./3rd/harbor/setup.sh
./3rd/mariadb/deb/*
./3rd/mariadb/install/mariadb-5.5.64-offline/my.cnf
./3rd/mariadb/install/setup.sh
./3rd/openldap/deb/*
./3rd/openldap/install/setup.sh
./3rd/openldap/install/apache2.conf
./3rd/nvidia-driver/gcc/*
```

### 问题记录

- apt-get install 本地安装最好指定版本，不然随着cache更新可能出现问题

- ntpdate在ubuntu中需要单独安装，检查下RedHat是否存在问题

- hadoop的activating现象出现在各类系统中，RedHat也需要执行stop-all.sh

```bash
sed -ri 's/yum install.*/dpkg -i \*\.deb/' 3rd/ipmitool/install_ipmitool.sh
```
