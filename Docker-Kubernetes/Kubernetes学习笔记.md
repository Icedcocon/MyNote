### 基本概念与组件

##### 资源对象

- **Master节点**：是 Kubernetes 集群的控制节点，负责整个集群的管理和控制。Master 节点上包含以下组件：
  
  - **kube-apiserver**：集群控制的入口，提供 HTTP REST 服务
  
  - **kube-controller-manager**：Kubernetes 集群中所有资源对象的自动化控制中心
  
  - **kube-scheduler**：负责 Pod 的调度
  
  - **Node**：Node 节点是 Kubernetes 集群中的工作节点，Node 上的工作负载由 Master 节点分配，工作负载主要是运行容器应用。Node 节点上包含以下组件：
    
    - **kubelet**：负责 Pod 的创建、启动、监控、重启、销毁等工作，同时与 Master 节点协作，实现集群管理的基本功能。
    - **kube-proxy**：实现 Kubernetes Service 的通信和负载均衡
    - **运行容器化(Pod)应用**

- **Pod**: Kubernetes 最基本的部署调度单元。每个 Pod 可以由一个或多个业务容器和一个根容器(Pause 容器)组成。一个 Pod 表示某个应用的一个实例

- **ReplicaSet**：是 Pod 副本的抽象，用于解决 Pod 的扩容和伸缩

- **Deployment**：Deployment 表示部署，在内部使用ReplicaSet 来实现。可以通过 Deployment 来生成相应的 ReplicaSet 完成 Pod 副本的创建

- **Service**：Service 是 Kubernetes 最重要的资源对象。Kubernetes 中的 Service 对象可以对应微服务架构中的微服务。Service 定义了服务的访问入口，服务的调用者通过这个地址访问 Service 后端的 Pod 副本实例。Service 通过 Label Selector 同后端的 Pod 副本建立关系，Deployment 保证后端Pod 副本的数量，也就是保证服务的伸缩性。

<img title="" src="file:///D:/Cache/MarkText/k8s-basic.png" alt="" width="277" data-align="center">

##### Kubernetes 核心组件

- etcd 保存了整个集群的状态，就是一个数据库；
- apiserver 提供了资源操作的唯一入口，并提供认证、授权、访问控制、API 注册和发现等机制；
- controller manager 负责维护集群的状态，比如故障检测、自动扩展、滚动更新等；
- scheduler 负责资源的调度，按照预定的调度策略将 Pod 调度到相应的机器上；
- kubelet 负责维护容器的生命周期，同时也负责 Volume（CSI）和网络（CNI）的管理；
- Container runtime 负责镜像管理以及 Pod 和容器的真正运行（CRI）；
- kube-proxy 负责为 Service 提供 cluster 内部的服务发现和负载均衡；

##### 推荐插件

- kube-dns 负责为整个集群提供 DNS 服务
- Ingress Controller 为服务提供外网入口
- Heapster 提供资源监控
- Dashboard 提供 GUI

##### 组件通信

Kubernetes 多组件之间的通信原理：

- apiserver 负责 etcd 存储的所有操作，且只有 apiserver 才直接操作 etcd 集群

- apiserver 对内（集群中的其他组件）和对外（用户）提供统一的 REST API，其他组件均通过 apiserver 进行通信
  
  - controller manager、scheduler、kube-proxy 和 kubelet 等均通过 apiserver watch API 监测资源变化情况，并对资源作相应的操作
  - 所有需要更新资源状态的操作均通过 apiserver 的 REST API 进行

- apiserver 也会直接调用 kubelet API（如 logs, exec, attach 等），默认不校验 kubelet 证书，但可以通过 `--kubelet-certificate-authority` 开启（而 GKE 通过 SSH 隧道保护它们之间的通信）

##### 创建 Pod 的流程

<img title="" src="file:///D:/Cache/MarkText/k8s-pod-process.png" alt="" data-align="center" width="455">

- 用户通过 REST API 创建一个 Pod
- apiserver 将其写入 etcd
- scheduluer 检测到未绑定 Node 的 Pod，开始调度并更新 Pod 的 Node 绑定
- kubelet 检测到有新的 Pod 调度过来，通过 container runtime 运行该 Pod
- kubelet 通过 container runtime 取到 Pod 状态，并更新到 apiserver 中

`kubectl get pod -o wide`

`kubectl get deploment`

# Docker回顾

### 常用命令

##### MySQL启动

`sudo docker run --name=fryMySQL -tid -p 0.0.0.0:3306:3306 -e MYSQL_ROOT_PASSWORD=123456 mysql`    

- --name：指定镜像实例的名称，不能与当前已创建实例重复

- -i：容器的标准输入保持打开

- -t：让docker分配一个伪终端，并绑定到容器的标准输入上。

- -d：让容器后台运行，并返回容器ID

- -p：绑定容器实例的端口（后）到宿主机的端口（前）

- -e：设定环境变量，指定mysql登录密码

##### MySQL持久化

`-v /home/fry/conf:/etc/mysql/conf.d`    配置文件挂在到宿主机的/home/fry/conf

`-v /home/fry/data:/var/lib/mysql`          数据挂载到宿主机的/home/fry/data
