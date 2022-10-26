# 1 Kubernetes介绍

### 1.1 Kubernetes的功能

- **服务发现和负载均衡**
  
  Kubernetes 可以使用 DNS 名称或自己的 IP 地址来曝露容器。 如果进入容器的流量很大， Kubernetes 可以负载均衡并分配网络流量，从而使部署稳定。

- **存储编排**
  
  Kubernetes 允许你自动挂载你选择的存储系统，例如本地存储、公共云提供商等。

- **自动部署和回滚**
  
  你可以使用 Kubernetes 描述已部署容器的所需状态， 它可以以受控的速率将实际状态更改为期望状态。 例如，你可以自动化 Kubernetes 来为你的部署创建新容器， 删除现有容器并将它们的所有资源用于新容器。

- **自动完成装箱计算**
  
  你为 Kubernetes 提供许多节点组成的集群，在这个集群上运行容器化的任务。 你告诉 Kubernetes 每个容器需要多少 CPU 和内存 (RAM)。 Kubernetes 可以将这些容器按实际情况调度到你的节点上，以最佳方式利用你的资源。

- **自我修复**
  
  Kubernetes 将重新启动失败的容器、替换容器、杀死不响应用户定义的运行状况检查的容器， 并且在准备好服务之前不将其通告给客户端。

- **密钥与配置管理**
  
  Kubernetes 允许你存储和管理敏感信息，例如密码、OAuth 令牌和 ssh 密钥。 你可以在不重建容器镜像的情况下部署和更新密钥和应用程序配置，也无需在堆栈配置中暴露密钥。

### 1.2 Kubernetes组件

##### 控制平面组件（Control Plane Components）

控制平面组件会用于决策（资源调度）、检测和响应集群事件，虽可运行于任何节点，但通常在master节点上运行所有控制平面组件。 

- (1) kube-apiserver

- (2) etcd

- (3) kube-scheduler

- (4) kube-controller-manager

- (5) cloud-controller-manager

##### Node 组件

节点组件会在每个节点上运行，负责维护运行的 Pod 并提供 Kubernetes 运行环境。

- (1) kubelet

- (2) kube-proxy

##### 容器运行时（Container Runtime）

容器运行环境是负责运行容器的软件。

##### 插件（Addons）

插件使用 Kubernetes 资源（DaemonSet、 Deployment 等）实现集群功能。

- (1) DNS

- (2) Web 界面（仪表盘 Dashboard）

- (3) 集群层面日志
