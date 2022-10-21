# CentOS7.7平台Kubernetes部署指南

### 1.关闭firewall、selinux、swap

```bash
# 1 关闭防火墙
systemctl stop firewalld
systemctl disable firewalld

# 2 关闭selinux
sed -i s/SELINUX=enforcing/SELINUX=disabled/g /etc/selinux/config
setenforce 0    # 临时立即关闭
getenforce

# 3 关闭内存交换区
swapoff -a
if [ ! -e fstab_bak ];then
  cp /etc/fstab /etc/fstab_bak
  cat /etc/fstab_bak | grep -v swap > /etc/fstab
fi

# 4 设置主机名
hostnamectl set-hostname $HOST_NAME
hostname
```

### 2.安装Docker

```bash
# 安装yum工具
yum install -y yum-rhn-plugin
yum install -y yum-utils
# 下载基础组件
sudo yum install -y tar bzip2 make automake gcc gcc-c++ vim \
pciutils elfutils-libelf-devel libglvnd-devel iptables
# 添加官方的repo源
yum-config-manager --add-repo=\
https://download.docker.com/linux/centos/docker-ce.repo
# 默认未定义环境变量$releasever，因此对repo源进行修改
sed -ri 's/\$releasever/7/g' /etc/yum.repos.d/docker-ce.repo
# CentOS不支持最新的Docker CE所需的containerd.io因此需要单独下载
yum install -y https://download.docker.com/linux/centos/7\
/x86_64/stable/Packages/containerd.io-1.4.3-3.1.el7.x86_64.rpm
# 下载Docker CE
yum install docker-ce -y
# 确保Docker开机启动
systemctl --now enable docker
```

### 3. 配置

```bash
# 设置虚拟网桥
echo "1" >/proc/sys/net/bridge/bridge-nf-call-iptables

# 配置内核参数
cat > /etc/sysctl.d/k8s.conf <<-EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF
sysctl -p /etc/sysctl.d/k8s.conf
# 加载网桥过滤模块
modprobe br_netfilter
# 查看网桥过滤模块是否加载成功
lsmod | grep br_netfilter

## 二进制安装方式下不建议执行
## kubernetes中service有两种代理模型，一种是基于iptables的，一种是基于ipvs的
## 相比较的话，ipvs的性能明显要高一些，但是如果要使用它，需要手动载入ipvs模块
## 安装ipset和ipvsadm
#yum install ipset ipvsadmin -y
## 添加需要加载的模块写入脚本文件
#cat <<EOF > /etc/sysconfig/modules/ipvs.modules
##!/bin/bash
#modprobe -- ip_vs
#modprobe -- ip_vs_rr
#modprobe -- ip_vs_wrr
#modprobe -- ip_vs_sh
#modprobe -- nf_conntrack_ipv4
#EOF
## 为脚本文件添加执行权限
#chmod +x /etc/sysconfig/modules/ipvs.modules
## 执行脚本文件
#bash -x /etc/sysconfig/modules/ipvs.modules
## 查看对应的模块是否加载成功
#lsmod | grep -e ip_vs -e nf_conntrack_ipv4

# docker配置国内镜像仓库
# Docker的cgroupfs默认采用Cgroup Driver，而kubernetes使用systemd，必须替换
mkdir /etc/docker
cat > /etc/docker/daemon.json <<EOF
{
"exec-opts": ["native.cgroupdriver=systemd"],
"log-driver": "json-file",
"log-opts": {
"max-size": "100m"
},
"storage-driver": "overlay2",
"storage-opts": [
"overlay2.override_kernel_check=true"
],
"registry-mirrors": ["http://hub-mirror.c.163.com"]
}
EOF
systemctl restart docker
```

### 4.安装kubernetes

```bash
# 更换kubernetes的yum源
cat > /etc/yum.repos.d/kubernetes.repo <<-EOF
[kubernetes]
name=Kubernetes
baseurl=http://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF

# 安装kubernetes
# 查看可用版本  yum --showduplicates list kubelet
yum install --setopt=obsoletes=0 kubeadm-1.23.12-0 kubelet-1.23.12-0 \
kubectl-1.23.12-0 cri-tools-1.23.0-0 -y
systemctl enable kubelet.service
systemctl start kubelet.service

# 追溯原因，参考4.7配置ipvs和5.3配置Cgroup_Driver
#cat > /etc/sysconfig/kubelet <<-EOF
#KUBELET_CGROUP_ARGS="--cgroup-driver=systemd"
#KUBE_PROXY_MODE="ipvs" 
#EOF

# 配置一下主机名解析 master和node都要操作
sed -ri '/master/d' /etc/hosts
sed -ri '/node[0-9]/d' /etc/hosts
cat >> /etc/hosts <<-EOF
192.168.64.128 master
192.168.64.129 node1
192.168.64.130 node2
EOF
```

### 5. 初始化master节点

```bash
kubeadm init \
--apiserver-advertise-address=192.168.64.128 \
--image-repository registry.aliyuncs.com/google_containers \
--kubernetes-version=v1.25.2 \
--pod-network-cidr=10.244.0.0/16 \
--service-cidr=10.96.0.0/12 
```
