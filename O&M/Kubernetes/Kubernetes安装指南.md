## 1 基础安装

### 1.0 关闭防火墙和交换区

```bash
# 1 shutdown firewall
echo "1 shutdown ufw"
systemctl stop ufw.service
systemctl disable ufw.service

# 2 close apparmor
echo "2 shutdown apparmor"
systemctl stop apparmor.service

# 3 close swap
echo "3 close swap"
swapoff -a
```

### 1.1 安装docker-ce

```bash
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
# Step 5: 配置docker
cat > /etc/docker/daemon.json << EOF
{
  "registry-mirrors": ["https://b9pmyelo.mirror.aliyuncs.com"],
  "exec-opts": ["native.cgroupdriver=systemd"]
}
EOF
systemctl restart docker
```

### 1.2 安装 nvidia-docker

- nvidia-docker

```bash
# 安装nvidia-docker
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
            sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2
```

- nvidia-container-toolkit

```bash
# 配置仓库
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list \
  && \
    sudo apt-get update
# 安装
sudo apt-get install -y nvidia-container-toolkit
```

### 1.3 安装 kubeadm kubectl kubelet

```bash
# 安装kubeadm
apt update && sudo apt install -y apt-transport-https
curl https://mirrors.aliyun.com/kubernetes/apt/doc/apt-key.gpg | sudo apt-key add -
vim /etc/apt/sources.list.d/kubernetes.list
# 添加 
deb https://mirrors.aliyun.com/kubernetes/apt/ kubernetes-xenial main
sudo apt update
deb-get kubelet=1.28.2-00 kubeadm=1.28.2-00 kubectl=1.28.2-00
```

### 1.4 将网桥的ip4流量转接到iptables

```bash
cat > /etc/sysctl.d/k8s.conf << EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward                 = 1
EOF
```

## 2 Kubernetes 容器运行时CNI配置

### 2.1 crictl绑定containerd

- `crictl` 命令默认连接到 `unix:///var/run/dockershim.sock` 如果要连接到其他runtimes，需要设置 endpoint:
  - 可以通过命令行参数 `--runtime-endpoint` 和 `--image-endpoint`
  - 可以通过设置环境变量 `CONTAINER_RUNTIME_ENDPOINT` 和 `CONTAINER_RUNTIME_ENDPOINT`
  - 可以通过配置文件的endpoint设置 `--config=/etc/crictl.yaml`
- 创建配置文件 `/etc/crictl.yaml`即可（上面的记不清了）

```yaml
runtime-endpoint: unix:///var/run/containerd/containerd.sock
image-endpoint: unix:///var/run/containerd/containerd.sock
timeout: 10
#debug: true
debug: false
```

- 注意在`/etc/containerd/config.toml` 中的以下内容需要被注释

```toml
disabled_plugins = ["cri"]
```

### 2.2 kubeadm 指定镜像仓库

- 使用`kubeadm config print init-defaults`指令生成默认config文件

```bash
kubeadm config print init-defaults > kubeadm-config.yaml
```

- 在 `kubeadm-config.yaml` 设置仓库等信息
  - `localAPIEndpoint.advertiseAddress` 设置本地IP
  - `localAPIEndpoint.bindPort` 设置`api-server`端口号
  - `nodeRegistration.criSocket` 设置运行时（通过切换socket访问不同CNI）
  - `nodeRegistration.imagePullPolicy` 镜像拉取策略
  - `nodeRegistration.name` 管理节点名称
  - `apiServer.timeoutForControlPlane` api-server初始化超时时间
  - `kubernetesVersion` kubernetes版本
  - `imageRepository` 国内镜像仓库地址
  - `networking.dnsDomain` 集群域名
  - `networking.serviceSubnet` Service子网

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
bootstrapTokens:
- groups:
  - system:bootstrappers:kubeadm:default-node-token
  token: abcdef.0123456789abcdef
  ttl: 24h0m0s
  usages:
  - signing
  - authentication
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: 192.168.0.102
  bindPort: 6443
nodeRegistration:
  criSocket: unix:///var/run/containerd/containerd.sock
  imagePullPolicy: IfNotPresent
  name: home-master1
  taints: null
---
apiServer:
  timeoutForControlPlane: 4m0s
apiVersion: kubeadm.k8s.io/v1beta3
certificatesDir: /etc/kubernetes/pki
clusterName: kubernetes
controllerManager: {}
dns: {}
etcd:
  local:
    dataDir: /var/lib/etcd
imageRepository: registry.aliyuncs.com/google_containers
kind: ClusterConfiguration
kubernetesVersion: 1.26.3
networking:
  dnsDomain: cluster.local
  serviceSubnet: 10.96.0.0/12
scheduler: {}
---
kind: KubeletConfiguration
apiVersion: kubelet.config.k8s.io/v1beta1
cgroupDriver: systemd
```

- 使用 `kubeadm config` 查看和下载镜像

```bash
# 指定 kubernetes 版本查看
kubeadm config images list --kubernetes-version 1.26.3
# 根据配置文件信息查看
kubeadm config images list --config kubeadm-config.yaml

# 根据配置文件下载镜像
kubeadm config images pull --config kubeadm-config.yaml
```

- 使用 `kubeadm-config.yaml` 初始化集群

```bash
kubeadm init --config kubeadm-config.yaml
```

### 2.3 containerd 指定镜像仓库

- Kubernetes 允许容器运行时指定沙箱容器及其镜像仓库，因此kubeadm查询到的pause镜像与运行时所需镜像并不完全一致，且containerd的镜像仓库及所需运行时镜像需要独立指定。

- 推荐指令`/usr/bin/containerd config dump > config.toml`然后修改

```toml
[plugins."io.containerd.grpc.v1.cri"]
  sandbox_image = "registry.k8s.io/pause:3.9"

[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
  SystemdCgroup = true
```

- `vim /etc/containerd/config.toml` 配置containerd镜像仓库及沙箱运行时

```toml
[plugins."io.containerd.grpc.v1.cri"]
sandbox_image = "your-sandbox-image"
[plugins."io.containerd.grpc.v1.cri".registry]
  [plugins."io.containerd.grpc.v1.cri".registry.mirrors]
    [plugins."io.containerd.grpc.v1.cri".registry.mirrors."your-custom-repo1"]
      endpoint = ["https://your-custom-repo1"]
    [plugins."io.containerd.grpc.v1.cri".registry.mirrors."your-custom-repo2"]
      endpoint = ["https://your-custom-repo2"]
    [plugins."io.containerd.grpc.v1.cri".registry.mirrors."your-custom-repo3"]
      endpoint = ["https://your-custom-repo3"]
```

- 重启continerd
  
  ```bash
  systemctl restart containerd
  ```

### 2.3 crictl 与 ctr

#### 2.3.1 说明

- containerd 是一个高级容器运行时（容器管理器）在单个主机上管理完整的容器生命周期：创建、启动、停止容器、拉取和存储镜像、配置挂载、网络等。Docker 在底层使用 containerd 来运行容器。Kubernetes 可以通过 CRI 使用 containerd 来管理单个节点上的容器。
- ctr 是 containerd 项目的一部分提供的命令行客户端，十个二进制文件，通常与 containerd 一起安装。
- crictl 是遵循 CRI 接口规范的一个命令行工具，通常用它来检查和管理kubelet节点上的容器运行时和镜像。

#### 2.3.2 ctr 常用指令

```bash
# 列出所有容器：
ctr ns list
# 列出所有容器：
ctr containers list
# 获取容器信息：
ctr containers inspect <container-id>
# 打标签给镜像
ctr -n ns images tag <source-image> <target-image>
# 删除镜像标签
ctr -n ns images untag <image-name>:<tag>
# 列出某个ns下所有镜像：
ctr -n ns images list
# 获取镜像信息：
ctr images inspect <image-id>
# 启动容器：
ctr containers start <container-id>
# 停止容器：
ctr containers stop <container-id>
# 重启容器：
ctr containers restart <container-id>
# 删除容器：
ctr containers remove <container-id>
# 删除镜像：
ctr images remove <image-id>
# 下载镜像：
ctr images pull <image-name>
# 导出容器为tar文件：
ctr containers export <container-id> > <output-path>
# 导入容器：
ctr containers import <tar-file> <container-id>
```

## 3 Kubernetes配置

### 3.1 Kubernetes配置文件位置及内容

```bash
# 获取证书
clientcert=$(grep client-cert ~/.kube/config |cut -d" " -f 6)
# 获取秘钥
clientkey=$(grep client-key-data ~/.kube/config |cut -d" " -f 6)
# 获取授权
certauth=$(grep certificate-auth ~/.kube/config |cut -d" " -f 6)
# 加密
echo $clientcert | base64 -d > ./client.pem
echo $clientkey | base64 -d > ./client-key.pem
echo $certauth | base64 -d > ./ca.pem
# 查询服务器IP和port
hostPath=$(echo $(kubectl config view |grep server) | cut -d " " -f2)
# 访问API
curl --cert ./client.pem --key ./client-key.pem --cacert ./ca.pem \
${hostPath}/api/v1/pods
```

### 4. Calico

##### 4.1 安装部署

- 下载calico离线包

```bash
# https://github.com/projectcalico/calico/releases
wget 
```

- 解压并检查镜像后上传

```bash
grep image: calico.yaml
```
