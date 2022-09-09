# 

- 问题1
  
  - 现象：VMWare workstation 16.2.4 Pro 在外网33节点的centos上运行提示缺少必要modules
  
  - 方案：安装VMWare workstation 15.5.7 Pro

- 问题2
  
  - 现象：RedHat官网找不到镜像下载入口，注册个人账户和企业账户均不允许下载系统镜像
  
  - 方案：地址`http://calipso.linux.it.umich.edu/pulp/isos/UM/Library/content/dist/rhel/server/7/7Server/x86_64/iso/)`

- 问题3
  
  - 问题：断网方法
  
  - 方案：通过在/etc/resolv.conf中注释的方式，禁掉宿主机的nameserver，在虚拟机中执行`systemctl restart network`生效。

- 问题4
  
  - 问题：下载rpm包及其依赖的方法
  
  - 方案：`yum -y --downloadonly --downloaddir install ...`

- 问题5
  
  - 问题：STEP 2 中的应该使用的域名
  
  - 方案：只使用cluster manager的域名test.cluster43

- 问题6
  
  - 问题：RedHat7.4不能用passwd将root密码修改成弱密码
  - 方案：新建虚拟机重装系统，在vm中设置弱密码

- 问题7
  
  - 问题：~~不同操作系统的软件版本号可能命名规则不同~~
  
  - 方案：~~下载最新版试试~~

- 问题8
  
  - 记录需要修改的包
    
    - ./rpm/ntp
    
    - ./3rd/bind-dns/rpm
    
    - ./rpm/docker
    
    - ./rpm/nvidia-docker
    
    - ./3rd/nvidia-driver/gcc

- 问题9
  
  - 现象：执行STEP 3 时没有这个文件或目录
  
  - 原因：bind没装上

- 问题9.5
  
  - 现象：在rpm中放入新安装包后还是执行旧包
  
  - 方案：STEP1中将安装包复制到/home/ais目录下

- 问题10
  
  - 现象：docker.service启动不起来
  
  - 故障点：
    
    - /usr/lib/systemd/system/docker.service中的`-H tcp://0.0.0.0:2375-current`选项（默认没有该项配置）
    
    - /etc/docker/daemon.json中的`"default-runtime":"runc"`（默认是空的）
  
  - 原因及方法
  
  - ![](D:\Cache\MarkText\2022-08-23-16-02-33-image.png)
  
  - 将shell/ais-install.sh中的`dockerd`改为`dockerd-current`
  
  - ~~将config/daemon.json.cpu和config/daemon.json中的文件修改~~
  
  ![](D:\Cache\MarkText\2022-08-30-15-00-08-image.png)
  
  - ~~将AIS_12_HARBOR_DOMAIN_DOMAIN改成AIS_12_HARBOR_DOMAIN~~

- 问题11 
  
  - 现象：NVIDIA docker安装失败
  
  - 解决 添加repo下载docker-ce 
    
    ```bash
    yum install -y yum-rhn-plugin
    yum install -y yum-utils
    
    # ===================== 下载docker-ce        =================
    mv rpm/docker rpm/docker.bak2
    yum-config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
    
    sed -ri 's/\$releasever/7/g' /etc/yum.repos.d/docker-ce.repo
    
    yum install -y https://download.docker.com/linux/centos/7/x86_64/stable/Packages/containerd.io-1.4.3-3.1.el7.x86_64.rpm
    yum install docker-ce -y
    
    # ====================== 下载 docker-compose  ================
    #mkdir /root/aisha-install-v2.2.bak/rpm/docker-compose
    #mkdir /root/aisha-install-v2.2.bak/docker-compose/docker-compose
    #curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /root/aisha-install-v2.2.bakin/docker-compose/
    #chmod +x /root/aisha-install-v2.2.bakin/docker-compose/docker-compose
    #ln -s /root/aisha-install-v2.2.bakin/docker-compose/docker-compose /usr/bin/docker-compose
    
    # ====================== 下载 nvidia-docker2  =================
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
       && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.repo | sudo tee /etc/yum.repos.d/nvidia-container-toolkit.repo
    
    yum-config-manager --enable libnvidia-container-experimental
    
    yum clean expire-cache
    yum install -y nvidia-docker2
    
    mv rpm/nvidia-docker rpm/nvidia-docker.bak
    yum install -y nvidia-docker2
    ```
  
  - 地址：`https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html`

只在 rpm/nvidia-docker 存在：libnvidia-container1-1.11.0-0.1.rc.2.x86_64.rpm
只在 rpm/nvidia-docker 存在：libnvidia-container-tools-1.11.0-0.1.rc.2.x86_64.rpm
只在 rpm/nvidia-docker 存在：nvidia-container-toolkit-1.11.0-0.1.rc.2.x86_64.rpm
只在 rpm/nvidia-docker 存在：nvidia-docker2-2.11.0-1.noarch.rpm

- 问题12
  
  - 现象：缺deliver-image文件
  
  ![](D:\Cache\MarkText\2022-08-24-16-57-07-b8e01067527952bb74cfce36f32de89.jpg)
  
  - 原因：太大没添加

- 问题13
  
  - 现象：缺少docker-compose.yml
  
  ![](D:\Cache\MarkText\2022-08-24-16-57-55-3035ac1cbe26963e3c9ee448c9b40ae.jpg)
  
  - 原因：脚本被设计为单个step可重复单独执行，该文件在setp 5 后会存在，因为重装docker后需要重启harbor。

- 问题14
  
  - 现象：hadoop没启动，显示datanode run as process ... stop it first
  
  ![](D:\Cache\MarkText\2022-08-24-17-30-26-image.png)
  
  ![](D:\Cache\MarkText\2022-08-24-17-29-39-image.png)
  
  - 方案：运行/usr/local/hadoop-3.2.2/sbin/stop-all.sh，随后在执行/usr/local/hadoop-3.2.2/sbin/start-all.sh，正常应该是inactive(dead)

- 问题15
  
  - 现象：
  
  ![](D:\Cache\MarkText\2022-08-26-16-54-21-image.png)

![](D:\Cache\MarkText\2022-08-26-16-56-59-image.png)

运行命令

```bash
 bash -x ais.sh root k8s 172.16.72.128 1; \
 bash -x ais.sh root test.cluster43 172.16.72.128 2; \
 bash -x ais.sh root k8s 172.16.72.128 3; \
 bash -x ais.sh root k8s 172.16.72.128 4;
```

- 问题16
  
  - 现象：harbor不能push镜像
  
  - 方案：先使用docker login登录harbor

- 问题17
  
  - 现象：docker login登录harbor失败，显示没有证书
  
  - 方案：修改/etc/docker/daemon.jason中的配置，添加`insecure-registries`

![](D:\Cache\MarkText\2022-08-30-14-26-29-image.png)

- 问题18
  
  - 现象：docker.service启动不起来，并显示配置文件有非法字符
  
  - 方案：观察配置文件中键名是否有双引号，域名和IP是否被替换。
    
    ```bash
    systemctl restart docker
    systemctl daemon-reload
    cd /home/harbor && docker-compose down -v
    docker-compose up -d
    docker login  harbor-infp.com:14444
    docker push harbor-infp.com:14444/ais-cluster43/coredns:1.7.0
    ```

- 问题19
  
  - kubelet不能启动
  
  ![](D:\Cache\MarkText\2022-08-30-15-42-03-image.png)
  
  ![](D:\Cache\MarkText\2022-08-30-15-38-57-image.png)
  
  - `journalctl -xefu kubelet`显示`/var/lib/kubelet/config.yaml`不存在
  - 方案：重新从STEP1执行，未复制master-images

- 问题20
  
  - 内网服务器可以ping通虚拟机，但是不能访问虚拟机端口，虚拟机内正常访问
  
  - 方案：关闭iptables

# 0 VMware虚拟机配置

### 虚拟机版本及安装

- 在CentOS 7.7上请安装VMWare workstation 15.5.7 Pro，更高版本可能出现缺少modules的情况；
- 最好使用root用户进行安装，否则设置Edit-Virtual Network Editor中的网关和网段时会提示缺少权限；
- 使用root用户安装时，默认位置为/var/root/vmware，请注意该位置硬盘容量是否满足要求。

```bash
su - root
./VMware-Workstation-Full-15.5.7-17171714.x86_64.bundle
```

<img title="" src="file:///D:/Cache/MarkText/2022-09-06-13-54-23-image.png" alt="" data-align="center" width="267">

# 1 操作系统配置

### 1.1 弱密码

- RedHat 7.4 不允许设置弱密码，因此最好在虚拟机安装RedHat镜像时即设置密码为弱密码。

- 附镜像下载地址：`http://calipso.linux.it.umich.edu/pulp/isos/UM/Library/content/dist/rhel/server/7/7Server/x86_64/iso/`

### 1.2 更换yum源

- RedHat 7.4系统自身的yum源需要注册后才能使用，因此需要替换为Centos 7的yum源，此外yum和rpm等软件也需要重新安装。

```bash
# 删除自带yum包
rpm -qa | grep yum | xargs rpm -e --nodeps      # 不检查依赖，直接删除
rpm -qa | grep python-urlgrabber | xargs rpm -e --nodeps

# 下载并安装yum和rpm
files=("python-urlgrabber-3.10-10.el7.noarch.rpm" \
        "rpm-4.11.3-45.el7.x86_64.rpm" \
        "yum-3.4.3-168.el7.centos.noarch.rpm" \
        "yum-metadata-parser-1.1.4-10.el7.x86_64.rpm" \
        "yum-plugin-fastestmirror-1.1.31-54.el7_8.noarch.rpm")
mkdir "change-yum-source-packages" && cd "change-yum-source-packages"

for file in ${files[@]}
do
        wget -a wget.log "http://mirrors.163.com/centos/7/os/x86_64/Packages/${file}"
done

rpm -ivh --force *.rpm

# 下载并修改配置文件
repo_path="/etc/yum.repos.d/"
for i in `ls ${repo_path}`
do
        if [ `echo ${i} | awk -F '.' {print $NF}` != "bak"  ]
        then
                mv ${repo_path}${i} ${repo_path}${i}".bak"
        fi
done
cp CentOS7-Base-163.repo ${repo_path}
sed -ri 's/\$releasever/7/g' "${repo_path}CentOS7-Base-163.repo"

# 更新
yum clean all
yum makecache
```

# 2 适配工作

### 2.1 下载RPM包及其依赖

- RedHat 7.4 通过指令`yum -y --downloadonly --downloaddir install ...`更新rpm包，需要更新的rpm包如下：
  
  - ./rpm/ntp
  
  - ./3rd/bind-dns/rpm
  
  - ./rpm/docker
  
  - ./rpm/nvidia-docker
  
  - ./3rd/nvidia-driver/gcc

- docker-ce及nvidia-docker需要添加新的仓库下载

```bash
yum install -y yum-rhn-plugin
yum install -y yum-utils

# ===================== 下载docker-ce        =================
mv rpm/docker rpm/docker.bak2
yum-config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
sed -ri 's/\$releasever/7/g' /etc/yum.repos.d/docker-ce.repo
yum install -y https://download.docker.com/linux/centos/7/x86_64/stable/Packages/containerd.io-1.4.3-3.1.el7.x86_64.rpm
yum install docker-ce -y

# ====================== 下载 nvidia-docker2  =================
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.repo | sudo tee /etc/yum.repos.d/nvidia-container-toolkit.repo
yum-config-manager --enable libnvidia-container-experimental
yum clean expire-cache
yum install -y nvidia-docker2
mv rpm/nvidia-docker rpm/nvidia-docker.bak
yum install -y nvidia-docker2
```
