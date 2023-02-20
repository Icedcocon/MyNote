# 问题排查

### 网络不可达

- 打开浏览器检索模式，观察登录过程报错包，检查URL地址锁定服务

- `kubectl get pods` 检查该服务是否启动，未启动`kubectl logs podName`检查日志文件，如果存在报错，则解决报错

- 再排查该服务是否正常访问`curl serviceURL`，若不能正常访问，且`kubectl logs podName`检查日志文件不存在内容，则说明web并不能访问该服务，检查`kubectl logs cluster-manger`，根据其中的报错信息，分析可能的问题
  
  - (1)  /etc/resolv.conf不能正确解析
  
  - (2) /etc/hosts 不正确
  
  - (3) 某些服务未正确启动，如ldap

# Docker

### Docker & harbor重启过程

- docker在修改`/etc/docker/daemon.json`后需要执行`systemctl daemon-reload`，随后执行`systemctl restar docker`

- 重启harbor，`docker-compose down -v`、`docker-compose up -d`，并登录`docker login -uadmin --password-stdin https://IP:14444`，域名和IP都需要登录，一个用于平台，另一个用于访问。

- docker重启后，需要重启harbor并登录才能正常拉取镜像，`systemctl restart harbor.service`在harbor有残余容器时不会生效，因此执行`docker-compose up -d`后，harbor仍然使用原来的网络组件。

- 使用docker ps | grep goharbor可以看到harbor各组件，docker重启后要重启harbor的原因是，其中部分组件并没有跟随docker重启，组件之间不匹配harbor无法正常工作。

### harbor重启后docker login失败 14444端口未开启

- 执行完`docker-compose down -v`后不能保证所有containers都已杀死，通过`docker ps -a | grep goharbor`查看是否存在残留。

- 如果存在残留则再次执行`docker-compose down -v`，或`docker rm -f`杀死容器，再执行`docker-compose up -d`重启。

# 多集群部署

### 第二集群部署注意事项

- `config/hosts`中DB数据库需要与第一个集群共用

```bash
#AIStation DB
100.2.81.20 ais-db
#AIStation Storage
100.2.81.21 ais-hdfs
#AIStation ImageRepo
100.2.81.21 harbor-infp.com
#AIStation Master
100.2.81.21 ais-master2
```

- `config/ais.cfg`中DB与ldap需要与第一个集群共用

```bash
#database
AIS_21_DB_HOST=100.2.81.20
AIS_22_DB_PORT=3306
AIS_23_DB_USER=root
AIS_24_DB_PWD=root
AIS_25_DB_NAME=ais_system110
AIS_26_DB_CHARSET=utf8
#ldap
AIS_27_LDAP_IP=100.2.81.20
```

- `/etc/named.rfc1912.zones`需要配置两个集群的域名，`/var/named/`路径下需要包含`ais.cluster20.zone`和`ais.cluster21.zone`两个文件

- STEP6、7、11-13全部跳过

- 

# Nvidia-Docker升级

- 需下载`nvidia-docker2`以及`nvidia-container-runtime`两个程序

- 下载流程

```bash
# yum工具
yum install -y yum-rhn-plugin
yum install -y yum-utils

# 添加docker-ce仓库并下载
yum-config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
sed -ri 's/\$releasever/7/g' /etc/yum.repos.d/docker-ce.repo
#yum install -y https://download.docker.com/linux/centos/7/x86_64/stable/Packages/containerd.io-1.4.3-3.1.el7.x86_64.rpm
yum install docker-ce -y

# 添加仓库并下载nvidia-docker
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.repo | sudo tee /etc/yum.repos.d/nvidia-container-toolkit.repo

yum-config-manager --enable libnvidia-container-experimental
yum clean expire-cache
yum install -y nvidia-docker2
yum install -y 
```

# showmount指令

- 是nfs-common包的一部分

# Linux指令

### ssh执行本地函数的方式

- `typeset -f <funcName>`可以将函数的定义打印到标准输出

- `;` 可以分割语句

- 因为函数变量在定以后仅当前终端有效，因此函数的定义与执行必须在同一条ssh指令中

- `ssh IP "$(typeset -f <funcName>); <funcName> \"<params>\"`

# 网络配置修改

- `/etc/resolv.conf`修改后未能生效，这是由于gateway 容器中的配置从宿主机复制后独立于宿主机。

- 需要重新执行第11步，重启网关

# 修改集群域名

- 获取knative中knative-serving的congifMap信息并修改config-domain

`kubectl get cm -A`

`kubectl edit configmaps config-domain -n knative-serving`

- 修改数据库中的信息

MySQL -> database(domainName) -> table(cluster_manager) -> set domain = newDomain

`update tableName set colName='newDomain' where id = num`

yaml/gpusharing-> controller 17571?修改域名

`kubectl edit cm inferenceservice-config -n knative` 修改域名

yaml/kserve/kserve-graph.yaml 修改域名 

yaml/aistaion 替换所有域名

egrep -r 'domainName' .

sed -r 's////' . | grep 'newDomain'

重启所有服务

# 旧集群镜像迁移

- 旧集群中镜像的`tag`由 模型服务-镜像管理 中的右侧模块处获取（显示不全可以用页面缩放）。

- 将镜像`tag`复制后，执行以下代码`bash XXX.sh tag`
  
  - save的镜像名称中不能带 ‘:‘

```bash
#! /bin/bash
cd $(dirname $0)

for item in $@; do
  docker pull $item
  img_name=${item##*/}
  img_name=${img_name/:/_}
  docker save $item | gzip > ${img_name}.tar.gz
  sshpass -p k8s scp ${img_name}.tar.gz root@10.23.177.143:/home/
done
```

- 复制到新平台后执行

```bash
#! /bin/bash
cd $(dirname $0)

for item in $@; do
  docker pull $item

  img_name=${item##*/}
  tag_name=${img_name%:*}
  img_name=${img_name/:/_}
  img_name=${img_name%-*}

  docker load < ${img_name}.tar.gz

  img_version_num=${item##*:}
  img_version=${img_version_num%-*}
  src="$(docker images | grep $tag_name  | grep ' '$img_version' ' | grep -v ' '${img_version_num}' ' | cut -d ' ' -f1)"
  dst="$(docker images | grep $tag_name  | grep ' '$img_version_num' ' | grep 'harbor-infp.com' | cut -d ' ' -f1)"
  # echo ${src}:${img_version}
  # echo ${dst}:${img_version_num}
  docker tag  ${src}:${img_version} ${dst}:${img_version_num}
  docker push ${dst}:${img_version_num}
done
```

# V2.2 HTTPS支持

# UI及ISTIO的证书更换

# 网关错误查询

- 页面存在 500 报错
  
  - `docker logs -f cluster_manager --tail 1000 > gateway.logs`
  
  - 在日志中搜索Exceptions

# 修改集群名称

- 进入数据库 表 cluster_manager 修改 name 字段

# CentOS7换源

```bash
# 确认系统发行版本
cat /etc/redhat-release
hostnamectl
# 备份repo
mv /etc/yum.repos.d/CentOS-Base.repo !#:1.bak
# 从阿里源下载repo
curl -sL https://mirrors.aliyun.com/repo/Centos-7.repo > \
/etc/yum.repos.d/CentOS-Base.repo
# 替换$releaserver
sed -ri 's#\$releaserver#7#' /etc/yum.repos.d/CentOS-Base.repo
```

# NFS重启后操作

- 前往`/home/aistation/ais/nfs`检查nfs路径是否与pv匹配

- 通过patch设置finalizer字段强制删除pvc

- 重启store服务、nfs-default-provisioner服务

# 节点添加

- 将/home/ais.tar.gz安装包复制到待添加节点/home路径下

- 如果是CentOS7.9（版本不匹配）则需要提前安装gcc等软件包

- 在**node节点**执行shell/join_node.sh

# pip安装与升级

```bash
yum -y install epel-release

python3 -m pip install --upgrade pip
```

# 配置集群共享yum源

- 需求：
  
  - CentOS镜像文件
  
  - httpd安装包

- 执行`cat  /etc/httpd/conf/httpd.conf | grep -v \#`，查看httpd配置文件

```bash
ServerRoot "/etc/httpd"    # 服务器根目录
Listen 8086                # 监听端口，默认8080
Include conf.modules.d/*.conf
User apache
Group apache
ServerAdmin root@localhost
ServerName 172.16.0.113:8086

<Directory />
     Options Indexes FollowSymLinks
     AllowOverride None
     Order deny,allow
     Allow from all
</Directory>

DocumentRoot "/var/www/html"    # 文件服务器根目录

<Directory "/var/www">
    AllowOverride None
    Require all granted
</Directory>

<Directory "/var/www/html">    # 路径访问权限设置
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>
```

- 执行`mount ./centos7.9.iso /var/www/html/sources/centos7.9`

- 配置`/etc/yum.repos.d/`路径下的.repo文件
  
  - 备份原始`.repo`文件
  
  - 创建新`new.repo`文件如下

```bash
[aistation_packages]
name=aistation_packages_repo
baseurl=http://${IP}:${port}/sources/centos7.9
gpgcheck=0
```

- 执行`yum clean all; yum makecache;`更新yum源

# Docker镜像路径修改

- 在/data/下新建路径

- 将/var/lib/docker中的内容转移到/data/新路径下

- 删除/var/lib/docker，并建立同名符号链接

# 高可用安装部署

### config/hosts

- 虚拟IP不能与已存在物理IP冲突
- master需按顺序配置三个节点IP

```bash
#AIStation ImageRepo
100.3.14.250 harbor-infp.com            # 不能与现有物理机IP相同

#AIStation Master
100.3.14.201 ais-master1
100.3.14.202 ais-master2
100.3.14.203 ais-master3

#AIStation CPU Node
100.3.14.214 ais-cpu-node1
100.3.14.215 ais-cpu-node2
100.3.14.216 ais-cpu-node3
```

### ais.cfg

- 确认关于用户名、密码、、虚拟IP、机器码、域名的要求

用户名 密码 可能回修该

```bash
#harbor
AIS_10_HARBOR_USER=admin
AIS_11_HARBOR_PASSWORD=Harbor12345
AIS_12_HARBOR_DOMAIN=harbor-infp.com:24444            # 不能选14444 推荐24444


#hadoop
AIS_17_HADOOP_IP=100.3.14.201,100.3.14.202            # master1 和 master2 的 IP地址
AIS_18_HADOOP_PORT=14000
AIS_19_HADOOP_LINK=http://100.3.14.201:14000,http://100.3.14.202:14000
AIS_20_HADOOP_USER=root


#database
AIS_21_DB_HOST=100.3.14.250
AIS_22_DB_PORT=13306                                # 13306

#license and system serving
AIS_36_LICENSE_MACHINECODE=b4:05:5d:5d:8c:a0        # machine code

#cluster manager
AIS_38_CLUSTER_CMSNODE=ais-master1
AIS_40_CLUSTER_DOMAIN=test.cluster250                # 域名可能修改
```

- disk.ha

```bash
ais-master1:/dev/sdb                                # lsblk
ais-master2:/dev/sdb                                # 第一级物理盘
ais-master3:/dev/sdb
```

- 每步检测指令

```bash
# Step 1
ssh IP                                                 #检测免密
cat /var/log/ntpdate/ntpdate.log                    # ntpdate
ip a | grep {virtual IP}        # 正常有一行字 尝试3个master节点 存在一个节点
systemctl status  keepalived & haproxy

# Step 2 
dig 

# Step 3
docker version
kubeadm version
kubectl version
systemctl status docker 、 kuberlet 

# Step 4 
http://[hadoop_IP]:50070        # master1 和 master2 的 IP ; 
                                # nodes 状态active  stand by

# Step 5
https://[harbor_IP]:14444        # 三个master节点实际IP x3
https://[harbor_IP]:24444        # 虚拟IP

# Step 6
mysql -uroot -proot -P port -h IP    # 三个master实际IP:3306 x 3
                                    # 虚拟IP:13306 

# Step 7
http://[openldap_IP]:8086/phpldapadmin # master1 master2 IP:8086 x 2
                                       # 虚拟IP:8086

# Step 8
ceph -s                                # 三个master节点执行 x 3
lsblk                                # 会多出一行内容 *ceph*

# Step 9
nvidia-smi

# Step 10

# Step 12
docker ps | grep -v goharbor | grep -v k8s            # 所有容器处于healthy状态打开UI界面

#Step 
```

### 待办事项

- 配置ntp服务，使用云平台指定ntp服务器，到/home/aistation/ais下修改
  
  - 111计算节点已修改/var/spool/cron/root 和 /etc/crontab
  
  - 112-114 master节点已修改/etc/crontab
  
  - 111-114节点修改config/ais.cfg文件

- 修改域名，与存储和云平台配合，到/home/aistation/ais下修改
  
  - 已修改所有节点/home/aistation/ais/config/ais.cfg
  
  - 已修改112节点/root/aisha-install-v2.3/config/ais.cfg
  
  - 已在112节点重新执行第二步

- 为gpu80-84安装寒武纪显卡驱动
  
  - 已在80-82三台master节点安装并验证
  
  - 

- 数据库修改
  
  - 修改完成

- 消除master节点的taint
  
  - 消除master1-3的node-role.kubernetes.io/master:NoSchedule的taint

### 问题

- 执行到第8步时修改/root/ais-install-v2.3 为 /root/aisha-install-v2.3
