# OpenLDAP 2.5 快速开始指南

## 1. OpenLDAP介绍

使用中存在问题请访问：[OpenLDAP网站](http://www.OpenLDAP.org)，和[OpenLDAP的常见问题解答](http://www.OpenLDAP.org/faq/?file=2)。

### 1.1 LDAP 介绍

- LDAP：Lightweight Directory Access Protocol，轻量目录访问协议
- LDAP服务是一个为只读（查询、浏览、搜索）访问而优化的非关系型数据库，呈树状结构组织数据
- LDAP主要用做用户信息查询（如邮箱、电话等）或对各种服务访问做后台认证以及用户数据权限管控
- 与LDAP一样提供类似的目录服务软件还有ApacheDS、Active Directory、Red Hat Directory Service
- 自己理解：每一条DN可以由多个对象(objectClass)组成，每个对象又有不同的属性组成(必须+非必须)，其实就是以objectClass为标准，方便各个系统通用

### 1.2 LDAP 名词

- DC：domain component一般为公司名，例如：dc=163,dc=com
- OU：organization unit为组织单元，最多可以有四级，每级最长32个字符，可以为中文
- CN：common name为用户名或者服务器名，最长可以到80个字符，可以为中文
- DN：distinguished name为一条LDAP记录项的名字，有唯一性(类似绝对路径)，例如：dc： cn=admin,ou=developer,dc=163,dc=com"
- SN：suer name（真实名称）
- O：organization（组织-公司）
- C：countryName（国家）
- **ldif扩展名**：LDAP data Interchange Format (`LDIF`)，相当于mysql的sql语句
- **olc开头**：可以看到很多文件名和字段名都有前缀"olc" (OpenLDAP Configuration)， 理解就好。

### 1.3 LDAPS 对比 LDAP over TLS

- LDAPS：可以理解为https，加密所有数据
- TLS：它默认走389端口，通讯的数据会加密

## 2.快速开始指南

> 注意: 这个快速开始指南没有使用强验证或任何保密服务。这些服务在本OpenLDAP管理员指南的其它章节里有所描述。 

### 2.0 Docker容器准备

```bash
docker run  --name ldap -v  /root/Workload/LDAP/openldap-2.5.18:/ldap -itd ubuntu:22.04  bash
docker exec -it ldap bash
sed -ri  's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
sed -ri  's/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
apt update
```

### 2.1 编译安装

- 优势：可以安装最新的版本、快速bug修复

- 缺点：新人比较难以上手

#### 2.1.1.下载并解压

可以从[OpenLDAP软件下载页面](http://www.openldap.org/software/download/)获取下载地址。

```bash
wget https://mirror-hk.koddos.net/OpenLDAP/openldap-release/openldap-2.5.18.tgz
# 解压发行版
# gunzip -c openldap-*.tgz | tar xvfB
tar -xzf openldap-*.tgz
# 进入目录
cd openldap-2.5.18
```

可以阅读压缩包中的COPYRIGHT, LICENSE, README 和 INSTALL 文档。

#### 2.1.2 安装依赖

- (1) 安装 cyrus-sasl 依赖

```bash
apt install libsasl2-dev 
# libwrap0 sasl2-bin 
# libsasl2-2 libsasl2-modules  libsasl2-modules-gssapi-heimdal
```

- (2) 安装编译依赖

```bash
apt install  build-essential \
             libltdl-dev unixodbc-dev libssl-dev libgnutls30 groff-base
```

#### 2.1.3.配置编译选项

configure脚本用于配置 OpenLDAP 以进行编译。configure脚本接受很多命令行选项以打开或关闭可选的软件功能。通过 `--help` 可以获取选项列表。此处使用默认配置。

```bash
# 查看选项
./configure --help
# 配置
./configure [options] [var=value ...]
# 开始编译(请配置 cyrus-sasl 相关，否则会导致禁用匿名访问修改失败)
./configure --with-cyrus-sasl # --enable-modules --enable-overlays
```

编译过程中出现问题请参考[软件常见问题解答的安装一节](http://www.openldap.org/faq/?file=8)

- 静态编译说明

```bash
# 静态编译说明：https://www.openldap.org/doc/admin24/overlays.html
# Backend 后端相关，默认保存在mdb数据库
--enable-sql：支持mysql、PostgreSQL等，根据自身需求确定是否开启(当前编译备用)，依赖包：unixODBC-devel

# Overlay 相关
# 建议静态编译所有overlays，就不需要做加载步骤了，而slapd大小只增加了0.2M
--enable-modules：支持动态加载模块，这个建议开启，用于可能加载其它的overlays
--enable-overlays：将所有可用overlay编译成静态文件至启动文件(slapd)内，源码目录：servers/slapd/overlays/，包含下面的enable
# --enable-memberof：将memberof编译成静态文件至启动文件(slapd)内，也就是说不需要动态加载了，使用的时候定义overlay就行了
# --enable-dynacl：动态加载ACL
# --enable-accesslog：登录日志模块
# --enable-auditlog：密码审计模块(修改密码的时候，日志会被记录下来)
```

- 动态编译参数说明

```bash
# 注意：没有特殊需求建议编译成静态模块

# --enable-overlays=mod
# mod表示用动态模块(module)的方式编译模块
# --enable-modules 这个必须开启，否则配置dn: cn=module,cn=config会报错
./configure --prefix=/usr/local/openldap --enable-modules --enable-overlays=mod --enable-sql --with-tls

# 编译成功后，下面的目录有相关的la文件
ll /usr/local/openldap/libexec/openldap/*.la

# 查看编译成静态的overlays和backends模块
/usr/local/openldap/libexec/slapd -VVV

# 没有static overlays的数据了
# (env) [root@zaza-test openldap-2.6.2]# /usr/local/openldap/libexec/slapd -VVV
# @(#) $OpenLDAP: slapd 2.6.2 (Oct 15 2020 15:36:55) $
#     root@zaza-test:/usr/local/src/openldap-2.6.2/servers/slapd
# 
# Included static backends:
#     config
#     ldif
#     monitor
#     bdb
#     hdb
#     mdb
#     relay
#     sql
```

#### 2.1.4.编译、测试并安装软件

编译时先构建依赖，然后编译软件，最后为确保编译正确，需要运行测试套件: 

```bash
# 编译
make depend
make
# 测试
make test
# 安装
make install
```

所有文件应该都被安装在/usr/local目录下(或任何configure指定的安装目录下). 

> 出现如下错误时 `/bin/sh: 15: soelim: not found` 需使用apt下载 groff-base 

#### 2.1.5.配置环境变量

```bash
# 环境设置
grep -q openldap /etc/profile || echo 'export PATH=$PATH:/usr/local/bin/openldap:/usr/local/sbin/openldap' >> /etc/profile
source /etc/profile
# slapd 位于 /usr/local/libexec/slapd
# 查看编译成静态的overlays和backends模块
/usr/local/libexec/slapd -VVV
# @(#) $OpenLDAP: slapd 2.5.18 (Jun  5 2024 00:59:30) $
#         @4160aad199e6:/ldap/servers/slapd
# 
# Included static overlays:
#     syncprov
# Included static backends:
#     config
#     ldif
#     monitor
#     mdb
#     relay
```

### 2.2 安装包下载并安装

- 推荐场景：简单的账号认证

#### 2.2.1 安装

```bash
apt install ldap-utils slapd
```

#### 2.2.2 配置

```bash
dpkg-reconfigure slapd
# Omit OpenLDAP server configuration?    NO
# DNS domain name: zaza.com
# Organization name: ldap01
# Administrator password: 123456
# Confirm password: 123456
# Do you want the database to be removed when slapd is purged? YES
# Move old database? YES
```

### 2.3.编辑配置文件并导入数据库配置

#### 2.3.1 编辑配置文件（弃用）

编辑文件 `/usr/local/etc/openldap/slapd.conf` 来包含一个如下格式的 BDB 数据库定义:

```
database bdb
suffix "dc=<MY-DOMAIN>,dc=<COM>"
rootdn "cn=Manager,dc=<MY-DOMAIN>,dc=<COM>"
rootpw secret
directory /usr/local/var/openldap-data
```

确保以你的域名的适当部分替换`<MY-DOMAIN>`和`<COM>`。例如, 对于 new-domain.com, 使用: 

```
database bdb
suffix "dc=new-domain,dc=com"
rootdn "cn=Manager,dc=new-domain,dc=com"
rootpw secret
directory /usr/local/var/openldap-data
```

如果你的域包含额外的部分, 例如 eng.uni.edu.eu, 使用: 

```
database bdb
suffix "dc=eng,dc=uni,dc=edu,dc=eu"
rootdn "cn=Manager,dc=eng,dc=uni,dc=edu,dc=eu"
rootpw secret
directory /usr/local/var/openldap-data
```

#### 2.3.2 编辑配置文件（新版）

编辑文件 `/usr/local/etc/openldap/slapd.ldif` 来包含一个如下格式的 BDB 数据库定义:

```bash
# olcPidFile后面配置tls
# 配置后，同时支持tls和ssl
# 客户机生成请求，csr -> CA签发 -> crt -> 拷回客户机已签名的证书
# olcTLSCACertificateFile: /usr/local/openldap/etc/openldap/CA/ca.crt
# olcTLSCertificateFile: /usr/local/openldap/etc/openldap/CA/openldap.crt
# olcTLSCertificateKeyFile: /usr/local/openldap/etc/openldap/CA/openldap.pem
# olcTLSVerifyClient: never # 默认选项就是never

# Load dynamic backend modules:
# 这里只能配置后端模块，当前版本默认的是mdb后端

# 使用LMDB为backends后端存储模块
# 类似初始化数据库，数据库是空库(顶层根目录是：new-domain.com)，通常称为BaseDN
olcSuffix: dc=new-domain,dc=com
# 最高权限，管理员账号(用户名Manager可以自定义，例如admin、root)
olcRootDN: cn=Manager,dc=new-domain,dc=com
# 管理员密码
olcRootPW: secret
# 建议使用加密密码：slappasswd -s secret
# MD5加密方式：slappasswd -h {MD5} -s zaza
# olcRootPW: {SSHA}ea+EFdqmej+ORnCTwsEjD6clEa2HlMVv
```

#### 2.3.2 导入数据库配置

现在准备导入你的数据库配置（其实就是基于slapd.ldif初始化运行环境，类似mysql的mysql_install_db）
运行下面的命令：

```bash
# 创建配置和中间文件路径 slapd.d 以及数据库路径 openldap-data
mkdir -pv /usr/local/etc/openldap/slapd.d
mkdir -pv /usr/local/var/openldap-data # 路径可在 slapd.ldif 中查看
# install -m 777 -d /usr/local/var/openldap-data

# 生成配置数据库，这里必须：100.00% eta 才表示配置文件没有问题
# 注意此处使用的是新版配置文件 slapd.ldif， 而非 slapd.conf 导入配置
/usr/local/sbin/slapadd -n 0 -F /usr/local/etc/openldap/slapd.d  -l /usr/local/etc/openldap/slapd.ldif
```

其中

- `-F` 指定中间态 ldif 文件生成位置

- `-l` 指定配置文件位置

- `-n` 指定数据库编号，不填写时会初始化错误 

执行完上述指令后会在 `/usr/local/etc/openldap/slapd.d` 中生成 `cn=config` 和 `cn=config.ldif`

（可选）以下指令用于为 config 账号临时增加密码管理权限。 默认的情况下 cn=config 是没有密码的，会导致验证失败。

```bash
# 临时增加config密码管理权限
grep olcRootPW /usr/local/etc/openldap/slapd.d/cn\=config/olcDatabase\=\{0\}config.ldif || sed -i '/olcRootDN: cn=config/a\olcRootPW: secret' /usr/local/etc/openldap/slapd.d/cn\=config/olcDatabase\=\{0\}config.ldif
```

### 2.4.启动slapd

运行这个命令启动独立的LDAP守护进程: 

```bash
# 启动 slapd 指令
/usr/local/libexec/slapd -h "ldapi:// ldap://"
# 关闭指令 （apt install psmisc）
killall slapd
```

slapd 启动后默认监听 389 端口

为了检查服务器是否运行以及是否被正确地配置好，可以使用ldapsearch 运行一个搜索：
（ldapsearch被安装在 /usr/local/bin/ldapsearch）

```bash
ldapsearch -x -b '' -s base '(objectclass=*)' namingContexts
```

注意在命令参数周围使用单引号来避免shell被特殊字符中断. 它应该返回: 

```
dn:
namingContexts: dc=new-domain,dc=com
```

启动后用ldapmodify将 cn=config 的明文密码替换为SSHA加密密码

```bash
# 建议不要修改olcRootDN: cn=config为olcRootDN: cn=Manager,dc=zaza,dc=com，因为各库功能不同，用单独账号管理
slappasswd -s secret # 密码生成： {SSHA}mcXVoZ4BQ7bznWhMhZsfZ0akt1DDKuV4
ldapmodify -x -H ldap:/// -D "cn=config" -w secret << EOF
dn: olcDatabase={0}config,cn=config
changetype: modify
replace: olcRootPW
olcRootPW: {SSHA}mcXVoZ4BQ7bznWhMhZsfZ0akt1DDKuV4
EOF
```

### 2.5.添加初始条目到目录中

- 可以使用ldapadd 添加条目到LDAP目录. ldapadd期待的输入是LDIF格式。需要将分两步走: 
  1. 建立LDIF文件
  2. 运行ldapadd 

使用编辑器新建一个LDIF文件，包含如下内容: 

```
dn: dc=<MY-DOMAIN>,dc=<COM>
objectclass: dcObject
objectclass: organization
o: <MY ORGANIZATION>
dc: <MY-DOMAIN>

dn: cn=Manager,dc=<MY-DOMAIN>,dc=<COM>
objectclass: organizationalRole
cn: Manager
```

确保使用域名的适当部分替换`<MY-DOMAIN>`和`<COM>`，`<MY ORGANIZATION>`应该被机构名称替换掉。（PS：请确保前后无多余空格）

```
dn: dc=new-domain,dc=com
objectclass: dcObject
objectclass: organization
o: Example Company
dc: new-domain

dn: cn=Manager,dc=new-domain,dc=com
objectclass: organizationalRole
cn: Manager
```

运行 ldapadd 来添加这些条目到你的目录. 

```bash
ldapadd -x -D "cn=Manager,dc=<MY-DOMAIN>,dc=<COM>" -W -f example.ldif
```

确保用域名的适当部分替换`<MY-DOMAIN>`和`<COM>`。你将收到提示输入密码，也就是在slapd.conf中定义的"secret"。例如, 对于 new-domain.com, 使用: 

```bash
ldapadd -x -D "cn=Manager,dc=new-domain,dc=com" -W -f example.ldif
```

其中

- example.ldif就是你上面新建的文件。
- `-W` 使用交互式输入密码， 也可以使用 `-w secret` 代替
- `-D` 指定执行脚本的用户，这里必须使用 ldapsearch 查询得到的用户。

另外关于建立目录的信息可以在本文的数据库建立和维护工具一章找到。

### 2.6.检测添加结果

现在我们准备检验目录中添加的条目。你可使用任何LDAP客户端来做这件事,但我们的例子使用ldapsearch(1)工具。记住把 dc=new-domain,dc=com 替换成你的网站的正确的值: 

```bash
ldapsearch -x -b 'dc=new-domain,dc=com' '(objectclass=*)'
# 或查询自己是否存在
ldapwhoami -x -D cn=Manager,dc=new-domain,dc=com -w secret
```

本命令将搜索和接收这个数据库中的每一个条目。

默认情况任何人包括匿名用户都拥有阅读权利，除了超级用户(即配置文件中的rootdn参数)。建议开启访问控制和TLS。

## 3. phpldapadmin

### 3.1 安装包下载安装

- 安装 `apache2` 和 `phpLDAPadmin`

```bash
apt install apache2
apt install phpldapadmin
# 直接在ubuntu22.04安装 phpldapadmin 有问题。 php8.1语法变更导致。
apt install dialog
wget http://archive.ubuntu.com/ubuntu/pool/universe/p/phpldapadmin/phpldapadmin_1.2.6.7-1_all.deb
dpkg -i phpldapadmin_1.2.6.7-1_all.deb
```

### 3.2 配置

#### 3.2.1 配置 phpldapadmin

- 编辑配置文件 `/etc/phpldapadmin/config.php` 

```php
$servers->setValue('server','name','company LDAP Server');
$servers->setValue('server','host','0.0.0.0');
// 修改为 slapd.ldif 中的 olcSuffix 对应的值
$servers->setValue('server','base',array('dc=my-domain,dc=com'));
// Web界面自动填写的用户名，（可选）修改为对应的值
$servers->setValue('login','bind_id','cn=Manager,dc=my-domain,dc=com');
```

#### 3.2.2 配置apache2

- 修改配置文件 `/etc/apache2/ports.conf` 中的监听端口

```bash
Listen 8086

<IfModule ssl_module>
        Listen 8086
</IfModule>

<IfModule mod_gnutls.c>
        Listen 8086
</IfModule>
```

- 修改 apache2 站点配置文件 `/etc/apache2/sites-enabled/000-default.conf`

```bash
<VirtualHost *:8086>
```

修改`/etc/apache2/conf-enabled/phpldapadmin.conf`上的访问权限，以允许仅从你信任的子网进行访问：

#### 3.2.3 启动 apache2

```bash
apachectl start
```

## 4. SSL

## 参考资料

- [Openldap-教程（ubuntu） | zaza的博客](https://zazayaya.github.io/2021/05/20/openldap-tutorial-by-ubuntu.html)

- https://github.com/jt6562/LDAP-read-notes/blob/master/ldap-guide/OpenLDAP%E7%AE%A1%E7%90%86%E5%91%98%E6%89%8B%E5%86%8C.md

- [&#x6253;&#x9020;&#x7EDF;&#x4E00;&#x7684; Kerberos &#x548C; OpenLDAP &#x670D;&#x52A1; &#xB7; &#x98DB;&#x54E5;&#x306E;&#x6280;&#x672F;&#x535A;&#x5BA2;](https://blog.7v1.net/system/kerberos-openldap.html)

集成及实战

- https://www.infvie.com/ops-notes/openldap-2.html
