```bash
#######################################################################
# Kubernetes介绍
#######################################################################
# Kubernetes的功能
# (1) 服务发现和负载均衡
# (2) 存储编排
# (3) 自动部署和回滚
# (4) 自动完成装箱计算
# (5) 自我修复
# (6) 密钥与配置管理

# Kubernetes组件
# (1) apiserver
#     提供了资源操作的唯一入口，并提供认证、授权、访问控制、API 注册和发现等机制；
# (2) controller manager
#     负责维护集群的状态，比如故障检测、自动扩展、滚动更新等；
# (3) scheduler
#     负责资源的调度，按照预定的调度策略将 Pod 调度到相应的机器上；
# (4) etcd
#     一个可信赖的分布式键值存储服务，保存了整个集群的状态（持久化）；
# (5) kubelet
#     跟容器引擎交互，维护容器的生命周期，负责 Volume（CVI）和网络（CNI）的管理；
# (6) kube-proxy
#     负责为Service提供cluster内部的服务发现，通信和负载均衡
```

```bash
#######################################################################
# kubectl常用操作
#######################################################################
# (1) kubectl apply 以文件或sdtin部署或更新一个或多个资源
kubectl apply -f <deployment-filename|diretory|url>
kubectl apply -f example-service.yaml     # 创建一个Service资源
kubectl apply -f example-controller.yaml  # 创建一个Controller资源
kubectl apply -f <diretory>        # 使用目录下所有.yaml .yml .json创建

# (2) kubectl get pods 列出一个或多个pod的信息
kubectl get pods/pod/po        # 以文本格式列出所有pod
kubectl get pods -o wide/name  # wide 包含附加信息; name 仅输出名称 
kubectl get pods -o json/yaml  # -o json、-ojson、-o=json 以json格式输出
kubectl get pods -o custom-columns='NAME:.metadata.name,RSRC:\
.metadata.resourceVersion'     # -o=custom-columns=<spec> 自定义列名
kubectl get pods -n <namespace># -n --namespace 列出该命名空间中所有pods
kubectl -n <namespace> get pods# 同上
kubectl get pods -A            # 或--all-namespaces显示所有命名空间所有pods
kubectl get pods --field-selector=spec.nodeNmae=Node1
                               # 列出在节点Node1上运行的所有命名空间的所有Pod
kubectl get pods --sort-by=.metadata.name # 排序

# (3) kubectl describe 列出一个或多个pod的详细信息
kubectl describe <resource> <reosurce_name>
kubectl describe pods <pod-name1>   # 显示名为pod-name1的pod的详细信息     
kubectl describe pods1/<pod-name1>  # 同上
kubectl describe pods               # 显示所有pod的详细信息
kubectl describe nodes <node-name1> # 显示名为node-name1的node的详细信息
kubectl describe namespace <namespace> # 显示某个namespace的详细信息
kubectl describe service <service>  # 显示某个service的详细信息
```

```bash
#######################################################################
# Pod概念
#######################################################################
# (1) Pod是一组紧密关联的容器集合
# (2) Pod内容器共享PID、IPC、Network和UTS namespace
# (3) Pod内容器共享网络和文件系统，可用进程间通信和文件共享这类高效方式完成服务
# (4) Pod是Kubernetes调度的基本单位
# (5) 每个Pod都有一个特殊的被称为"根容器"的Pause容器
# (6) Pause容器保存所有的容器状态，Kubernetes通过管理Pause容器管理Pod中所有容器
```
