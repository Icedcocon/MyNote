```bash
#######################################################################
# Kubernetes介绍
######################################################################
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

# 资源对象概述
# (1) 分类
# 某种资源对象：Node、Pod、Service、Volume
# 与资源对象相关事务与动作：Label、Annotation、Namespace、Deployment、HPA、PVC
# (2) 资源对象通用属性
# ①版本(apiVersion)：内涵对象所属资源组
# ②类别(kind)：资源对象类型
# ③名称、标签、注解：属于metadata元数据；名称唯一；标签筛选；注解扩展

# Kubernetes中的资源
# (1) 名称空间级别
# ①工作负载型资源（ workload）
#     Pod、ReplicaSet、Deployment、StatefulSet、DaemonSet、Job、CronJob
# ②服务发现及负载均衡型资源（ServiceDiscovery LoadBalance）
#     Service、Ingress、...
# ③配置与存储型资源
#     Volume（存储卷）、CSI（容器存储接口，可以扩展各种各样的第三方存储卷）
# ④特殊类型的存储卷
#     ConfigMap（当配置中心来使用的资源类型）、Secret（保存敏感数据）、
#    DownwardAPI（所外部环境中的信息输出给容器）
# (2)集群级别
#     Namespace、Node、Role、ClusterRole、RoleBinding、ClusterRoleBinding
# (3)元数据型
#     HPA、PodTemplate、LimitRange
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

```yaml
#######################################################################
# Pod
#######################################################################
# Pod 概念
# (1) Pod是一组紧密关联的容器集合
# (2) Pod内容器共享PID、IPC、Network和UTS namespace
# (3) Pod内容器共享网络和文件系统，可用进程间通信和文件共享这类高效方式完成服务
# (4) Pod是Kubernetes调度的基本单位
# (5) 每个Pod都有一个特殊的被称为"根容器"的Pause容器
# (6) Pause容器保存所有的容器状态，Kubernetes通过管理Pause容器管理Pod中所有容器

# Pod必填字段
| 参数名                   | 字段类型 | 说明                                       |
| ----------------------- | ------ | ------------------------------------------ |
| version                 | String | K8s API版本(v1) `kubectl api-versions`可查询 |
| kind                    | String | yaml 文件定义的资源类型和角色                  |
| metadata                | Object | 元数据对象                                   |
| metadata.name           | String | 元数据对象的名字，如 Pod 的名字                |
| metadata.namespace      | String | 元数据对象的命名空间，默认default               |
| spec                    | Object | 详细定义对象                                 |
| spec.containers[]       | List   | 容器列表的定义                               |
| spec.containers[].name  | String | 容器的名字                                   |
| spec.containers[].image | String | 容器镜像的名称                               |

# Pod主要字段
| spec.containers[].imagePullPolicy           | String 
# 镜像拉取策略，默认Always（总拉取）、Never（仅本地）、IfNotPresent（先本地）。
| spec.containers[].command[]                 | List   
# 指定容器启动命令，数组可指定多个，默认使用Dockerfile中的启动命令。
| spec.containers[].args[]                    | List   
# 指定容器启动命令参数，因为是数组可以指定多个。
| spec.containers[].workingDir                | String 
# 指定容器的工作目录 
| spec.containers[].volumeMounts[]            | List   
# 指定容器内部的存储卷位置
| spec.containers[].volumeMounts[].name       | String 
# 指定可以被容器挂载的存储卷的名称
| spec.containers[].volumeMounts[].mountPath  | String 
# 指定可以被挂载的存储卷的路径 
| spec.containers[].volumeMounts[].readOnly   | String 
# 设置存储卷路径的读写模式，true或者false，默认为读写模式
| spec.containers[].ports[]                   | List   
# 指定容器需要用到的端口列表
| spec.containers[].ports[].name              | String 
# 指定端口名称
| spec.containers[].ports[].containerPort     | String 
# 指定容器需要监听的端口号
| spec.containers[].ports[].hostPort          | String
# 指定容器所在主机需要监听的端口号，默认同上，设置后同主机不能存在容器副本
| spec.containers[].ports[].protocol          | String 
# 指定端口协议，支持TCP和UDP，默认为TCP 
| spec.containers[].env[]                     | List  
# 指定容器运行前需要设置的环境变量列表
| spec.containers[].env[].name                | String 
# 指定环境变量名称
| spec.containers[].env[].value               | String
# 指定环境变量值
| spec.containers[].resources                 | Object
# 指定资源限制和资源请求的值（这里开始就是设置容器的资源上限）
| spec.containers[].resources.limits          | Object 
# 指定设置容器运行时资源的运行上限
| spec.containers[].resources.limits.cpu      | String 
# 指定CPU限制，单位为core数，将用于docker run --cpu-shares参数
| spec.containers[].resources.limits.memory   | String 
# 指定MEM内存的限制，单位为MiB、GiB
| spec.containers[].resources.requests        | Object 
# 指定容器启动和调度时的限制设置 
| spec.containers[].resources.requests.cpu    | String 
# CPU请求，单位为core数，容器启动时初始化可用数量
| spec.containers[].resources.requests.memory | String 
# 内存请求，单位为MIB、GiB，容器启动时初始化可用数量

# Pod 其他字段
spec.restartPolicy        | String
# Pod的重启策略，默认Always（终止即重启）、OnFailure（非0退出才重启）、Never
spec.nodeSelector         | Object
# 定义Node的Label过滤标签，以key:value格式指定
spec.imagePullSecrets     | Object
# 定义pull镜像时使用secret名称，以name:secretkey格式指定
spec.hostNetwork          | Boolean
# 是否使用主机网络模式，默认false使用docker网桥，true表示使用主机网络，同主机无副本

# Pod生命周期（5种）
# (1) 挂起(Pending)：apiserver已创建pod，但未调度或还有+个容器未创建或正下载
# (2) 运行中(Running)：所有容器均已创建，至少一个容器在运行、启动或重启
# (3) 成功(Succeed)：pod中所有容器都已成功执行后退出，并且不会被重启
# (4) 失败(Failed)： 所有容器都已退出，但至少有一个容器退出失败，即返回值非0
# (5) 未知(Unknown)： apiserver无法正常获取到pod对象的状态信息，如网络通信失败
# 容器的状态（3种）：Waiting（等待）、Running（运行中）和 Terminated（已终止）
kubectl describe pod <pod 名称>    # 检查container状态

# spec.containers.lifecycle
| spec.containers[].lifecycle                 | Object
| spec.containers[].lifecycle.postStart       | Object
| spec.containers[].lifecycle.preStop         | Object
spec:
  containers: <[]Object> 
    lifecycle: <Object>
      postStart: <Object>
        exec: <Object>
          command: <[]string>            # 要执行的指令
        httpGet: <Object>
        tcpSocket: <Object>
      preStop: <Object>
        exec: <Object>
          command: <[]string>
        httpGet: <Object>
        tcpSocket: <Object>

# Pod状况
# Pod有一个PodStatus对象，内有一个Kubelet管理的PodConditions数组，状态如下：
# (1) PodScheduled：Pod 已经被调度到某节点
# (2) PodHasNetwork：Pod 沙箱被成功创建且配置了网络（Alpha特性，需启用）
# (3) ContainersReady：Pod 中所有容器都已就绪
# (4) Initialized：所有的 Init 容器都已成功完成
# (5) Ready：Pod 可以为请求提供服务，并且应该被添加到对应服务的负载均衡池中

| type               | Pod 状况的名称                            |
| status             | 状况是否适用，True False Unknown           |
| lastProbeTime      | 上次探测 Pod 状况时的时间戳                 |
| lastTransitionTime | Pod 上次从一种状态转换到另一种状态时的时间戳   |
| reason             | 机器可读的、驼峰编码的文字，上次状况变化的原因  |
| message            | 人类可读的消息，给出上次状态转换的详细信息     |

# init容器
# (1) Init 容器总是运行到成功完成为止
# (2) 每个 Init 容器都必须在下一个 Init 容器启动之前成功完成
# (3) 指定资源限制和资源请求的值（这里开始就是设置容器的资源上限）
# (4) 支持应用容器的全部字段和特性，包括资源限制、数据卷和安全设置。
# (5) 不支持lifecycle、livenessProbe、readinessProbe和startupProbe
| spec.initContainers[]       | List   | init容器列表的定义  

# 探针
# 两种探针
# (1) readinessProbe（就绪探测）: 探测容器是否可以处理服务请求
#      失败：          端点控制器将会把该Pod的IP从关联的Service中删除掉
#      未配置该探针： 默认返回成功状态
# (2) livenessProbe（存活探测）: 用于探测容器是否处于Running状态
#      失败：         kubelet杀掉容器，根据restart policy来决定是否重新创建
#      未配置该探针： 默认返回成功状态，只有容器crash，才会触发失败状态返回
# 三种操作
# (1) ExecAction: 在容器中执行命令行，若退出状态是0，则认为探针的状态是成功。
# (2) TCPSocketAction: 向容器指定端口发送TCP请求，若端口被监听，则认为成功。
# (3) HTTPGetAction: 向容器指定端口和路径发送HTTP GET请求，若状态码为200-400则成功
# 四种场景
# (1) Default:不配置探针，容器不健康也会被kubelet杀掉；容器正常初始化后则认为成功
# (2) Custom: 进程不能服务但容器仍健康，可用liveness探针杀掉容器；
#              进程初始化时间长，可用readiness探针实现服务可用
# (3) Reset: 进程处于中间过程状态，且希望从初始状态开始，可用liveness探针实现
#             同时提供复位接口，如请求复位接口，则探针返回失败状态，从而实现复位操作。
#             默认返回成功状态。
# (4) OutOfService: 服务升级，需将服务临时下线，可用readiness探针实现
#                    同时提供服务下线接口，如请求下线接口，则探针返回失败状态，实现下线。
#                    默认返回成功状态。
# 三种结果
# (1) 成功：容器通过了诊断
# (2) 失败：容器未通过诊断
# (3) 未知：诊断失败，不会采取任何行动

# 存活状态检测
| spec.containers.livenessProbe                		  | Object
# 存活探针
| spec.containers.livenessProbe.exec           		  | Object
# 通过执行指令探测
| spec.containers.livenessProbe.httpGet        		  | Object
# 通过执行HTTP GET请求探测
| spec.containers.livenessProbe.tcpSocket      		  | Object
# TCPSocket指定涉及TCP端口的操作
| spec.containers.livenessProbe.initialDelaySeconds   | Object
# 设置多少秒后开始探测
| spec.containers.livenessProbe.failureThreshold      | Object
# 设置连续探测多少次失败后，标记为失败，默认三次
| spec.containers.livenessProbe.successThreshold      | Object
# 设置失败后探测的最小连续成功次数，默认为1
| spec.containers.livenessProbe.timeoutSeconds        | Object
# 设置探测超时的秒数，默认1s
| spec.containers.livenessProbe.periodSeconds         | Object
# 设置执行探测的频率（以秒为单位），默认1s
spec:
  containers: <[]Object> 
    livenessProbe: <Object> # 存活探针
      exec: <Object>
        command: <[]string>
      httpGet: <Object>
        port: <string> -required- 
        path: <string>
        host: <string>
        httpHeaders: <[]Object>
          name: <string> -required-
          value: <string> -required-
        scheme: <string> 
      tcpSocket: <Object> 
        port: <string> 	-required- # 容器暴露的端口
        host: <string> 			   # 默认pod的IP
      initialDelaySeconds: <integer> 
      failureThreshold: <integer> 
      successThreshold: <integer> 
      timeoutSeconds: <integer> 
      periodSeconds: <integer> 
      
# 就绪状态检测
| spec.containers.readinessProbe                	  | Object
# # 就绪探针
| spec.containers.readinessProbe.exec           	  | Object
# 通过执行指令探测
| spec.containers.readinessProbe.httpGet        	  | Object
# 通过执行HTTP GET请求探测
| spec.containers.readinessProbe.tcpSocket      	  | Object
# TCPSocket指定涉及TCP端口的操作
| spec.containers.readinessProbe.initialDelaySeconds  | Object
# 设置多少秒后开始探测
| spec.containers.readinessProbe.failureThreshold     | Object
# 设置连续探测多少次失败后，标记为失败，默认三次
| spec.containers.readinessProbe.successThreshold     | Object
# 设置失败后探测的最小连续成功次数，默认为1
| spec.containers.readinessProbe.timeoutSeconds       | Object
# 设置探测超时的秒数，默认1s
| spec.containers.readinessProbe.periodSeconds        | Object
# 设置执行探测的频率（以秒为单位），默认1s
spec:
  containers: <[]Object> 
    readinessProbe: <Object> 
      exec: <Object>
        command: <[]string>
      httpGet: <Object>
        port: <string> -required- 
        path: <string>
        host: <string>
        httpHeaders: <[]Object>
          name: <string> -required-
          value: <string> -required-
        scheme: <string> 
      tcpSocket: <Object> 
        port: <string> -required- # 容器暴露的端口
        host: <string> # 默认pod的IP
      initialDelaySeconds: <integer> 
      failureThreshold: <integer> 
      successThreshold: <integer> 
      timeoutSeconds: <integer>
      periodSeconds: <integer> 


```
