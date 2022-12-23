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



kubectl explain --api-version=networking.k8s.io/v1 ingress.spec.defaultBackend
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
| spec.containers.livenessProbe                       | Object
# 存活探针
| spec.containers.livenessProbe.exec                  | Object
# 通过执行指令探测
| spec.containers.livenessProbe.httpGet               | Object
# 通过执行HTTP GET请求探测
| spec.containers.livenessProbe.tcpSocket             | Object
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
        port: <string>     -required- # 容器暴露的端口
        host: <string>                # 默认pod的IP
      initialDelaySeconds: <integer> 
      failureThreshold: <integer> 
      successThreshold: <integer> 
      timeoutSeconds: <integer> 
      periodSeconds: <integer> 

# 就绪状态检测
| spec.containers.readinessProbe                      | Object
# # 就绪探针
| spec.containers.readinessProbe.exec                 | Object
# 通过执行指令探测
| spec.containers.readinessProbe.httpGet              | Object
# 通过执行HTTP GET请求探测
| spec.containers.readinessProbe.tcpSocket            | Object
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

# kube-scheduler 对 pod 进行调度包含两步：
# (1) predicate：将所有满足 Pod 调度需求的 Node 选出
# (2) Priorities：根据启用的打分规则对可调度节点打分，选出最合适Node
# predicate算法：
# (1) PodFitsResources：节点上剩余的资源是否大于pod请求的资源
# (2) PodFitsHost：如果pod指定了NodeName，坚持节点名称是否和NodeName匹配
# (3) PodFitsHostPorts：节点上已经使用的port是否和pod申请的port冲突
# (4) PodSelectorMatches：过滤掉和pod指定的label不匹配的节点
# (5) NoDiskConflict：已经mount的volume和pod指定的volume不冲突，除非他们只是只读
# priority优先级:由键值对组成，键是名称，值是权重
# (1) LeastRequestedPriority：计算CPU和Memory的使用率，使用率越低权重越高
# (2) BalancedResourceAllocation：CPU和Memory使用率接近，权重越高，与前者共用
# (3) ImageLocalityPriority：倾向于已经有要使用镜像的节点，镜像越大，权重越高


# 节点亲和性调度
# 规则说明
# (1) nodeName、nodeSelector和nodeAffinity 必须同时满足才能调度。
# (2) 同一nodeSelectorTerms下多个matchExpressions 只要一个满足就可以调度。
# (3) 同一matchExpressions下多个keys，必须同时满足时才能调度。
pod.spec.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution
# <Object> 硬限制，必须满足规则才能调度，IDE指Pod运行期间标签变更不影响运行
pod.spec.nodeAffinity.rDSIDE.nodeSelectorTerms     | <[]Object> 
# 定义规则
pod.spec.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution
# <[]Object> 软限制，调度器尝试调度Pod到Node，多个优先级规则可以设置权重
pod.spec.nodeAffinity.pDSIDE.weight                | <integer> -required-
# 值越高越先执行
pod.spec.nodeAffinity.pDSIDE.preference            | <Object>  -required-
# 定义规则
spec:
  affinity: <Object>
    nodeAffinity: <Object>
      requiredDuringSchedulingIgnoredDuringExecution: <Object>
        nodeSelectorTerms: <[]Object> -required-
        - matchExpressions: <[]Object>
          - key: <string> -required-
            operator: <string> -required- # 设置键值关系
            values: <[]string>
            - value1
            - value2
          matchFields: <[]Object> # 通过节点字段
          - key: <string> -required-
            operator: <string> -required- # 设置键值关系
            values: <[]string>
            - value1
            - value2
      preferredDuringSchedulingIgnoredDuringExecution: <[]Object>
      - weight: <integer> -required-
        preference: <Object> -required-
          matchExpressions: <[]Object> # 通过节点标签
          - key: <string> -required-
            operator: <string> -required- # 设置键值关系
            values: <[]string>
            - value1
            - value2
          matchFields: <[]Object> # 通过节点字段
          - key: <string> -required-
            operator: <string> -required- # 设置键值关系
            values: <[]string>
            - value1
            - value2


# 键值运算关系
# (1) In：            label 的值在某个列表中
# (2) NotIn：         label 的值不在某个列表中
# (3) Gt：            label 的值大于某个值
# (4) Lt：            label 的值小于某个值
# (5) Exists：        某个 label 存在
# (6) DoesNotExist：  某个 label 不存在

# Pod亲和性调度
# (1) 基于已经运行在节点的Pod及其标签来约束新调度的Pod可以调度到的节点。
# (2) 如果X上已运行一或多个满足规则Y的Pod，则新Pod应该/不应该运行在X上。
#       X可以是节点、机架、拓扑域
pod.spec.podAffinity.requiredDuringSchedulingIgnoredDuringExecution
# <Object> 硬限制，必须满足规则才能调度，IDE指Pod运行期间标签变更不影响运行
pod.spec.podAffinity.rDSIDE.namespaces      | <[]string> 
# 指定labelSelector要匹配的命名空间列表 默认为Pod亲和性/反亲和性定义所在的命名空间
pod.spec.podAffinity.rDSIDE.topologyKey     | <string> -required- 
# 只有具备指定拓扑域的节点才能满足Pod的调度规则
pod.spec.podAffinity.rDSIDE.labelSelector   | <string> -required- 
# 选择要匹配的标签
pod.spec.podAffinity.preferredDuringSchedulingIgnoredDuringExecution
# <[]Object> 软限制，调度器尝试调度Pod到Node，多个优先级规则可以设置权重
pod.spec.podAffinity.pDSIDE.weight                | <integer> -required-
# 取值范围1-100，找到满足其他规则的节点后，调度器将节点满足的所有偏好weight求和。
# 和与该节点其他优先级函数评分相加，调度器选择总分最高的Node作为最高优先级。
pod.spec.podAffinity.pDSIDE.preference            | <Object>  -required-
# 定义规则
spec:
  affinity: <Object>
    podAffinity: <Object>
      requiredDuringSchedulingIgnoredDuringExecution: <[]Object>
        namespaces: <[]string>
        topologyKey: <string> -required-
        labelSelector: <Object>
          matchLabels: <map[string]string>
            key1: value1
            key2: value2
          matchExpressions:
            key: <string> -required-
            operator: <string> -required- # 设置键值关系
            values: <[]string>
            - value1
            - value2
      preferredDuringSchedulingIgnoredDuringExecution: <[]Object>
      - weight: <integer> -required-
        podAffinityTerm: <Object> -required-
          namespaces: <[]string>
          topologyKey: <string> -required-
          labelSelector: <Object>
            matchLabels: <map[string]string>
              key1: value1
              key2: value2
            matchExpressions:
              key: <string> -required-
              operator: <string> -required- # 设置键值关系
              values: <[]string>
              - value1
              - value2

# Pod反亲和性调度
spec:
  affinity: <Object>
    podAntiAffinity: <Object>
      requiredDuringSchedulingIgnoredDuringExecution: <[]Object>
        namespaces: <[]string>
        topologyKey: <string> -required-
        labelSelector: <Object>
          matchLabels: <map[string]string>
            key1: value1
            key2: value2
          matchExpressions:
            key: <string> -required-
            operator: <string> -required- # 设置键值关系
            values: <[]string>
            - value1
            - value2
      preferredDuringSchedulingIgnoredDuringExecution: <[]Object>
      - weight: <integer> -required-
        podAffinityTerm: <Object> -required-
          namespaces: <[]string>
          topologyKey: <string> -required-
          labelSelector: <Object>
            matchLabels: <map[string]string>
              key1: value1
              key2: value2
            matchExpressions:
              key: <string> -required-
              operator: <string> -required- # 设置键值关系
              values: <[]string>
              - value1
              - value2

# matchExpressions的上层字段
# (1) nodeSelectorTerm
# (2) preference
# (3) labelSelector
# (4) podAffinityTerm.labelSelector

# topologyKey拓扑域
# (1) topology指拓扑域，是一个范围如Node、机柜、地区等，本质是Node上的标签。
# (2) topologyKey对应Node标签的Key（非Value）本质是用于筛选Node。
# 使用k8s.io/hostname作为拓扑域的范围，则k8s.io/hostname对应的值不同就时不同拓扑域。
#   Pod1在k8s.io/hostname=node1的Node上
#   Pod2在k8s.io/hostname=node2的Node上
#   Pod3在k8s.io/hostname=node1的Node上
#   则Pod2和Pod1、3 不在同一个拓扑域，而Pod1和Pod3在同一个拓扑域。

|     调度策略     |           操作符                    |         调度目标         |
| --------------- | ---------------------------------- | -----------------------|
| nodeAffinity    | In,NotIn,Exists,DoesNotExist,Gt,Lt | 指定主机                 |
| podAffinity     | In,NotIn,Exists,DoesNotExist       | POD与指定POD同一拓扑域    |
| podAnitAffinity | In,NotIn,Exists,DoesNotExist       | POD与指定POD不在同一拓扑域 |

# (1) 容忍度（Tolerations）应用于Pod，允许Pod调度到带有与之匹配的污点的节点上。
# (2) 污点和容忍度（Toleration）相互配合，可以用来避免 Pod 被分配到不合适的节点上
# (3) 污点(Taint)Node上的污点排斥Pod，可以让Node拒绝Pod的调度执行，甚至将Pod驱逐
# (4) 污点的组成：key=value:effect
# (5) 污点包含key、value，value可以为空，effect 描述污点的作用。
# (6) taint effect 支持如下三个选项：
#     ①NoSchedule：不会将Pod调度到具有该污点的 Node 上
#     ②PreferNoSchedule：避免将Pod调度到具有该污点的 Node 上
#     ③NoExecute：不会将Pod调度到具有该污点的Node上，同时驱逐Node上已经存在的Pod

spec:
  tolerations: <[]Object>
    effect: <string> # NoSchedule, PreferNoSchedule, NoExecute
    key: <string>
    value: <string>
    operator: <string> # Exists, Equal
    tolerationSeconds: <integer>
```

```yaml
spec:
  affinity: <Object>
    nodeAffinity: <Object>
      requiredDuringSchedulingIgnoredDuringExecution: <Object>
        nodeSelectorTerms: <[]Object> -required-
      preferredDuringSchedulingIgnoredDuringExecution: <[]Object>
      - weight: <integer> -required-
        preference: <Object> -required-
    podAffinity: <Object>
      requiredDuringSchedulingIgnoredDuringExecution: <[]Object>
        namespaces: <[]string>
        topologyKey: <string> -required-
        labelSelector: <Object>
      preferredDuringSchedulingIgnoredDuringExecution: <[]Object>
      - weight: <integer> -required-
        podAffinityTerm: <Object> -required-
          namespaces: <[]string>
          topologyKey: <string> -required-
          labelSelector: <Object>
```

```yaml
#######################################################################
# Service
#######################################################################
# 概念
# (1) Service 定义一种抽象：通过Selector，能够被Service访问的，逻辑上的一组Pod
# (2) 访问svc时通过Round Robin（轮询算法）访问所属Pod，有且只有此算法。
# (3) Service只提供4层负载均衡，ingress提供7层负载均衡

# 类型(ServiceTypes)
# (1) ClusterIp：自动分配一个仅Cluster内部可以访问的virtual IP    （默认）
# (2) NodePort：在(1)基础上为Service在各Node绑定一端口，用<NodeIP>:NodePort访问
# (3) LoadBalancer：在(2)的基础上，创建外部负载均衡器，将请求转发到对应NodePort
# (4) ExternalName：将集群外服务引入内部，并在内部使用，需k8s 1.7以上的kube-dns

# clusterIP
# (1) 在每个node节点用iptables将发向clusterIP对应端口的数据转发到kube-proxy中。
# (2) kube-proxy查询该service对应pod地址和端口，内部负载均衡方法转发数据到对应pod
# (3) 所需组件
#  1) apiserver
#       用户通过kubectl命令向apiserver发送创建service的命令
#       apiserver接收到请求后将数据存储到etcd中
#  2) kube-proxy
#       kubernetes各节点中都有一个kube-porxy的进程
#       kube-porxy感知service和pod的变化，并将变化信息写入本地iptables规则
#  3) iptables
#       使用NAT等技术将virtual IP的流量转至endpoint中
spec:  
    type: ClusterIP
    selector:    
        app: myapp
    ports:  
      - port: 80

# Headless Service
# (1) 不需要负载均衡和独立的Service IP时
# (2) 指定spec.clusterIP的值为 “None” 来创建 Headless Service
# (3) 这类Service不会分配Cluster IP; kube-proxy不会处理; 平台也不会为其负载均衡
spec:
  selector:
    app: myapp
  clusterIP: "None"
  ports:
    - port: 80

# NodePort
# (1) 在node上开启静态端口，将访问该端口的流量导入到 kube-proxy
# (2) kube-proxy将数据转发给对应pod
# (3) 访问<Node IP>: <Node Port>对<Pod IP>: <target Port>访问
spec:
  type: NodePort
  selector:
    app: myapp
  ports:
    - port: 80

# LoadBalancer
# (1) 来自外部负载均衡器的流量将直接重定向到后端 Pod 上
# (2) loadBalancer在nodePort基础上改用cloud-controller-manager组件
# (3) 配置外部负载均衡器，将流量转发到对应Node的端口。
spec:
  selector:
    app: myapp
  ports:
    - port: 80
  clusterIP: 10.0.171.239
  type: LoadBalancer
status:
  loadBalancer:
    ingress:
    - ip: 192.0.2.127

# ExternalName
# (1) 该类型将服务映射到域名（即externalName字段的值），而非selector对应pods
# (2) IPv4地址不能被CoreDNS或ingress-nginx解析，externalName只能使用域名（可含数字）
# (3) 集群DNS服务会返回CNAME记录，本类Service的重定向发生在 DNS 级别，而非proxy或转发
spec:
  type: ExternalName
  externalName: my.database.example.com

# Service资源配置（svc）
apiVersion: <string>
kind:        <string>
metadata:   <Object>
spec:        <Object>
   allocateLoadBalancerNodePorts: <boolean> # 外部LB是否自动分配NodePort(默认T)
   clusterIP:    <string>    # Cluster IP的值，None为Headless服务
   clusterIPs:    <[]string>  # 分配给该Service的IP地址列表，通常随机分配
                               # 若clusterIP被指定，则其与clusterIPs[0]必须一致
   externalIPs:    <[]string>
   externalName:<string>
   externalTrafficPolicy        <string>
   healthCheckNodePort  <integer>
   internalTrafficPolicy        <string>
   ipFamilies   <[]string>
   ipFamilyPolicy       <string>
   loadBalancerClass    <string>
   loadBalancerIP       <string>
   loadBalancerSourceRanges     <[]string>
   ports        <[]Object>
   publishNotReadyAddresses     <boolean>
   selector     <map[string]string>
   sessionAffinity      <string>
   sessionAffinityConfig        <Object>
   type <string>
status:     <Object>
  conditions:  <[]Object>
    lastTransitionTime: <string> -required- # 上次状态转变时间
    message:            <string> -required- # 适合人阅读的状态转换细节
    observedGeneration: <integer>  # 与.metadata.generation比较是否过时
    reason:             <string> -required- # 状态转换原因
    status:             <string> -required- # conditions的状态T、F、U
    type:               <string> -required- # conditions的类型
  loadBalancer:<Object>
    ingress: <[]Object> # 包含Ingress points的列表
      hostname: <string>   # 为基于DNS的负载均衡器入口 设置主机名
      ip:        <string>   # 为基于IP的负载均衡器入口  设置IP
      ports:    <[]Object> 
        error:      <string> # 记录LB服务的错误信息 
        port:      <integer> -required- # 记录状态的服务端口
        protocol: <string> -required-  # 记录状态的协议




apiVersion: v1
kind: Service
metadata:
spec:
  clusterIP: <string>        # 设置仅cluster内部可用的Virtual IP
  externalIPs: <[]string>    # 设置一个外部的 IP 地址，并且将流量导入到集群内部。
  externalName: <string>     # 配合ExternalName Type使用，指定外部服务
  ports: <[]Object>          # 端口信息
    - protocol: TCP 
      port: 3017  # service端口
      targetPort: 5003 # pod端口
      nodePort: 31122 # 主机端口
  selector: <map[string]string>
    key: value
  type: <string> # ExternalName, ClusterIP, NodePort, LoadBalancer

  externalTrafficPolicy: <string>    # 外部路由机制 Cluster（默认）, Local
  healthCheckNodePort: <integer>
  loadBalancerIP: <string>   # 
  loadBalancerSourceRanges: <[]string>
  publishNotReadyAddresses: <boolean>
  sessionAffinity: <string>
  sessionAffinityConfig: <Object>
    clientIP: <Object>
      timeoutSeconds: <integer>

# kube-proxy代理模块发展历程：
# (0) 三种模式： userspace、iptables、ipvs
# (1) kubernetes v1.0：services 仅是一个“4层”代理，代理模块只有 userspace
# (2) kubernetes v1.1：Ingress API 出现，代理“7层”服务，增加iptables代理模块
# (3) kubernetes v1.2：iptables 成为默认代理模式
# (4) kubernetes v1.8：引入 ipvs 代理模块
# (5) kubernetes v1.9：ipvs 代理模块成为 beta 版本
# (6) kubernetes v1.11：ipvs 代理模式 GA

# userspace 模式
# (1) 请求到达Node节点后，先进入内核iptables，再到用户空间由kube-proxy转发到pod
# (2) kube-proxy监听的随机端口在用户空间，该端口不是Port、nodePort或targetPort
# (3) 因此kube-proxy设置iptables规则，把访问服务的连接重定向给该端口
# (4) 流量从用户空间进出内核带来的性能损耗是不可接受的，所以也就有了 iptables 模式

# iptables 模式
# (1) 默认方式，iptables基于netfilter实现。
# (2) 访问ClusterIP的流量根据iptables规则路由到各pod 上
# (3) iptables使用DNAT完成转发，用随机数实现负载均衡。
# (4) 与userspace区别是
#     1) 使用DNAT模块完成service入口地址到pod实际地址转换，少一次内核态到用户态切换
#     2) 如果iptables代理最初选择的那个pod没有响应，不会自动重试其他 pod。
# (5) 问题：service数量大时iptables规则过多，非增量式更新会引入一定的时延，降低性能。

# ipvs 模式
# (1) kube-proxy监视Kubernetes Service对象和Endpoints
# (2) kube-proxy调用netlink接口以创建ipvs规则，定期与Service、Endpoints对象同步 ipvs规则
# (3) 访问Service的流量被ipvs重定向到Service对应的一个后端 Pod
# (4) ipvs 支持的负载均衡算法：
#      1) rr：round-robin/轮询
#      2) lc：least connection/最少连接
#      3) dh：destination hashing/目标哈希
#      4) sh：source hashing/源哈希
#      5) sed：shortest expected delay/预计延迟时间最短
#      6) nq：never queue/从不排队

# ipvs 原理
# (1) ipvs是LVS的负载均衡模块，iptables和ipvs均基于netfilter框架
# (2) 但ipvs使用哈希表作为底层的数据结构并且工作在内核态
# (3) 因此ipvs在重定向流量和同步代理规则有着更好的性能，几乎允许无限的规模扩张。
# (4) ipvs 支持三种负载均衡模式：
#     1) DR模式（Direct Routing）
#     2) NAT 模式（Network Address Translation）
#     3) Tunneling（也称 ipip 模式）。
# (5) 三种模式中只有NAT支持端口映射，所以ipvs使用NAT模式
# (6) 原生ipvs只支持DNAT，在数据包过滤、SNAT和NodePort类型场景中ipvs调用iptables


# Netfilter
# (1) Netfilter通过协议族以及hook点确定一个执行入口
# (2) 用netfilter钩子函数挂载自定义钩子，需要调用nf_register_hook方法
# (3) 指明hook点以及优先级，到该hook点时，根据优先级调用挂载的处理函数
# (4) iptables，ipvs都是基于netfilter框架之上开发的netfilter模块

# 集群内Pod通信机制
# (1) Kubernetes支持两种基本的服务发现模式：环境变量、DNS.
# (2) 环境变量
#       1) Pod运行时，kubelet会在Pod内自动添加当前活跃的Service的一组环境变量。
#       2) 该机制支持
#            Docker
#            links
#            {SVCNAME}_SERVICE_HOST变量和{SVCNAME}_SERVICE PORT变量
#        3) 确保Pod需要访问的Service先于Pod创建，否则不会为Pod设置环境变量
说明：
当您具有需要访问服务的Pod时，并且您正在使用环境变量方法将端口和群集P发布到客户端
Pod时，必须在客户端Pod出现之前创建服务。否则，这些客户端Pod将不会设定其环境变
量。
```

```yaml
#######################################################################
# Ingress
#######################################################################
# Ingress概念
# (1) Ingress：为集群服务提供外部可访问的URL、L4/L7负载均衡、TLS卸载...
# (2) Ingress Resource：定义了转发规则
# (3) Ingress Controller：包含负载均衡器、进行控制逻辑转换
#                         将ingress resource配置转为负载均衡配置，并实时加载

# controller 控制器
# (1) Ingress Controller对Ingress资源进行控制，默认Ingress Nginx Controller
# (2) 同一个集群中可安装多个控制器
# (3) 第三方IC:
#            1) HAProxy Ingress：针对HAProxy的Ingress控制器
#            2) NGINX Ingress：与Ingress Nginx不同
#            3) Istio Ingress：基于Istio的Ingress控制器
#            4) Kong Ingress：用来驱动Kong Gateway的Ingress控制器
# (4) 集群必须存在Ingress控制器的Pod才能使Ingress正常运行，控制器需自行启动。



# 服务暴露模式
# AWS
# GCE
# Azure
# Bare-metal 的。


# pathType 路径类型
# (0) Ingress各路径需设置路径类型(Path Type)，支持的路径类型有三种：
# (1) ImplementationSpecific：匹配方法取决于IngressClass，可与后两者相同
# (2) Exact：精确匹配 URL 路径，且区分大小写。
# (3) Prefix：基于以 / 分隔的 URL 路径前缀匹配。
#          1) 匹配区分大小写，并且对路径元素(/分隔的URL中标签列表)逐个比对 
#             如果每个p都是请求路径p的元素前缀，则请求与路径p匹配。
#          2) 例：/, /aaa, /aaa/bbb <== /aaa/bbb : 匹配 /aaa/bbb 前缀

# 多重匹配和主机名通配符
# (1) 多重匹配:多条路径会匹配同一个请求，有限选择 最长 和 精确 匹配路径
# (2) 主机名通配符：
#    主机           host 头部        匹配与否？
#    *.foo.com     bar.foo.com        基于相同的后缀匹配
#    *.foo.com     baz.bar.foo.com    不匹配，通配符仅覆盖了一个 DNS 标签
#    *.foo.com     foo.com            不匹配，通配符仅覆盖了一个 DNS 标签

# Ingress 类
# Ingress可由不同的控制器实现，通过指定IngressClass指定控制器及配置
# .spec.parameters可提供额外配置内容，具体的值取决于IngressClass

# IngressClass 的作用域
# (1) Cluster 集群范围（默认）
#    通过将.spec.parameters.scope字段设置为Cluster指定，或保持默认
#    通过kind、apiGroup确定集群作用域的API（如：Service），name确定具体资源
# (2) Namespace 命名空间作用域
#    通过将.spec.parameters.scope字段设置为Namespace指定
#    通过kind、apiGroup确定集群作用域的API（如：ConfigMap），name确定具体资源
# (3) IngressClass API 本身是集群作用域的。

# TLS
# Ingress仅支持单个TLS端口443，仅外部流量到Ingress加密，Service及Pod间的流量明文传输
# TLS Secret必须包含以tls.crt指定的证书和tls.key指定的私钥
apiVersion: v1
kind: Secret
metadata:
  name: testsecret-tls
  namespace: default
data:
  tls.crt: base64 编码的证书
  tls.key: base64 编码的私钥
type: kubernetes.io/tls

# Ingress资源配置（ing）
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
spec:
  ingressClassName: # 省略将使用默认Ingress类
  rules: <[]Object>
    host: <string>  # 可选，用于限定rule适用的host
    http: <Object>
      paths: <[]Object> -required- # path对象数组
        backend: <Object> -required- # serviceName和servicePort的组合对象
          service
            name: <string> -required-
            port: <Object> -required-
              number: <integer> -required-
              name: <string> 
        path: <string> # 每个path对象都有与其对应的backend对象（服务）
        pathType: # Exact、Prefix等
  tls: <[]Object>
    hosts: <[]string>    # 指定需要tls保护的host
    secretName: <string> # 指定包含tls配置信息的Secret
  defaultBackend:   # 没有rules匹配时的默认路由后端，应在Ingress控制器中指定
    service:
       name: <string> -required-
       port:
           number: <integer> -required-
           name: <string> 
    resource:    # Resource后端指向某命名空间资源，与上方Service后端互斥
       apiGroup: 
       kind: 
       name: 
```

```yaml
#######################################################################
# Pod控制器概念
#######################################################################

# ReplicationContro1ler & ReplicaSet & Deployment
# (1) ReplicationController
#        1) 确保容器应用的副本数始终保持在用户定义范围内，少则创建，多则回收
# (2) ReplicaSet
#        1) 支持集合式的selector
#        2) 建议用其取代ReplicationController
# (3) Deployment 
#        0) 提供了一个声明式定义(declarative)方法，Deployment会创建ReplicaSet
#        2) 滚动升级和回滚应用     【Deployment自身特点】
#        3) 扩容和缩容            【RS特点 Deployment继承】
#        4) 暂停和继续Deployment  【Deployment自身特点】

# HPA (HorizontalPodAutoScale)
# (1) 仅适用于Deployment和ReplicaSet
# (2) 可根据Pod的CPU利用率、内存和用户自定义的metric扩缩容(Cpu>80,Max 10,Min 2)
# (3) HPA特性由Kubernetes API资源和控制器实现，资源决定了控制器的行为

# DaemonSet
# (1) 确保全部（或者某些）节点上各运行一个Pod的副本，添加节点建Pod，移除节点删Pod
# (2) 删除DaemonSet会删除它创建的所有Pod
# (3) DaemonSet 的一些典型用法：
#        1) 每个节点上运行存储守护进程，如glusterd或ceph
#        2) 每个节点上运行日志收集守护进程，如flunentd或logstash
#        3) 每个节点上运行监控守护进程，如Prometheus Node Exporter或collectd

# Job & Cronjob
# (1) 负责批处理任务(仅执行一次)，保证批处理任务的一个或多个Pod成功结束
# (2) Cron Job创建基于时间调度的Jobs。
# (3) 典型的用法如下所示：
#        1) 在给定的时间点调度Job运行
#        2) 创建周期性运行的Job，例如：数据库备份、发送邮件

# StatefullSet
# (1) 管理有状态应用，为Pod提供序号（唯一固定ID）和唯一性保证
# (2) 保证部署和scale的顺序
# (3) 适用于有以下需求的程序
#        1) 稳定的、唯一的网络标识符。
#        2) 稳定的、持久的存储。
#        3) 有序的、优雅的部署和缩放。
#        4) 有序的、自动的滚动更新。
# (4) 对于mysql这些有状态服务不建议放入k8s中
```

```yaml
#######################################################################
# 资源控制器
#######################################################################

# ReplicaSet
apiVersion: apps/v1 
kind: ReplicaSet 
metadata:
  name:
  namespace:
  labels:               
spec:
  minReadySeconds:   <integer>      # 处于ready多久后认为available，默认0
  replicas:    <integer>            # 副本数量
  selector:    <Object> -required-
    matchExpressions:   <[]Object>
      key:  <string> -required-
      operator:  <string> -required- # In、NotIn、Exists、DoesNotExist
      values:  <[]string>
    matchLabels:  <map[string]string>
  template:  <Object>
    metadata:  <Object>
    spec: <Object>
      volumes:
      initcontainers:
      containers:
      - name:
          image:
        ports:
      affinity:
      tolerations:
status:                                  # 最近观测到的ReplicaSet状态
   availableReplicas:    <integer>       # 可用（满足minReadySeconds）副本数
   conditions:           <[]Object>      # 副本最新可用观察值
   fullyLabeledReplicas: <integer>       # 与template所有标签匹配的Pod数量
   observedGeneration:   <integer>       # 反应最近副本的生成
   readyReplicas:        <integer>       # 该ReplicaSet中处于ready状态的Pod数量
   replicas:     <integer> -required-    # 最近观测到的副本数


# Deployment
apiVersion:   <string>
kind: <string>
metadata:     <Object>
spec: <Object>
  minReadySeconds:      <integer>      # 处于ready多久后认为available，默认0
  paused:       <boolean>              # deployment是否暂停
  progressDeadlineSeconds:  <integer>  # 部署失败的等待秒数，默认600s
  replicas:     <integer>              # 副本数量
  revisionHistoryLimit: <integer>      # 保留的允许回滚的旧副本数量，默认10个
  selector: <Object> -required-    # 
    matchExpressions:   <[]Object>
      key:  <string> -required-
      operator:  <string> -required- # In、NotIn、Exists、DoesNotExist
      values:  <[]string>
    matchLabels:  <map[string]string>
  strategy: <Object>
    rollingUpdate:  <Object>  # 滚动升级的配置参数，Type为RollingUpdate时启用 
      maxSurge:     <string>  # 允许超过数量限制的Pod数量，数值/百分比，默认25%
      maxUnavailable: <string># 允许不可用(低于)Pod的数量，数值/百分比，默认25%
    type: <string>            # Recreate或RollingUpdate(默认)
  template: <Object> -required-
    metadata:
    spec:
status:       <Object>
  collisionCount:       <integer> # 哈希冲突数量，借此避免产生哈希冲突
  unavailableReplicas:  <integer> # 不可用副本数
  updatedReplicas:      <integer> # 该deployment控制的尚未停止的Pod数量
  availableReplicas:    <integer>       # 可用（满足minReadySeconds）副本数
  conditions:           <[]Object>      # 副本最新可用观察值
  fullyLabeledReplicas: <integer>       # 与template所有标签匹配的Pod数量
  observedGeneration:   <integer>       # 反应最近副本的生成
  readyReplicas:        <integer>       # 该ReplicaSet中处于ready状态的Pod数量
  replicas:     <integer> -required-    # 最近观测到的副本数

# --record参数可以记录命令
kubectl apply -f deployment.yaml --record  
# 扩容
kubectl scale deployment nginx-deployment --replicas=10
# 更新
kubectl set image deployment/nginx-deployment nginx=qianzai/k8s-myapp:v2 --record 
# 回滚
kubectl rollout undo deployment/nginx-deployment
# 回滚到指定版本
kubectl rollout undo deployment/nginx-deployment --to-revision=1
# 暂停 deployment的更新

# Deployment更新策略
# 支持：Recreate（重建）和RollingUpdate（滚动更新）
# Recreate：更新Pod时，先杀掉所有正在运行的Pod，然后创建新的Pod。   
# RollingUpdate：以滚动方式渐变更新Pod，即Pod新版本副本数递增而旧版本递减
#                  更新时存在两个RS，旧的RS一次减少25%的pod而新的RS一次创建25%

# Rollover（多个rollout并行）
# 执行创建5个app:v1的Deployment，已创建3个副本时更新创建5个app:v2的Deployment
# Deployment会立即杀掉已创建的3个app:v1 Pod，并开始创建myapp:v2的 Pod

# 清理策略
# 设置.spec.revisonHistoryLimit指定deployment最多保留多少revision历史记录。
# 默认的会保留所有的revision，如果将该项设置为0，Deployment 就不允许回退

# DaemonSet
apiVersion   <string>
kind         <string>
metadata     <Object>
spec         <Object>
  minReadySeconds:      <integer>      # 处于ready多久后认为available，默认0
  revisionHistoryLimit: <integer>      # 保留的允许回滚的旧副本数量，默认10个
  selector: <Object> -required-    # 
    matchExpressions:   <[]Object>
      key:  <string> -required-
      operator:  <string> -required- # In、NotIn、Exists、DoesNotExist
      values:  <[]string>
    matchLabels:  <map[string]string>
  template: <Object> -required-
    metadata:
    spec:
  updateStrategy:  <Object>
    rollingUpdate:  <Object>  # 滚动升级的配置参数，Type为RollingUpdate时启用 
      maxSurge:     <string>  # 允许超过数量限制的Pod数量，数值/百分比，默认25%
      maxUnavailable: <string># 允许不可用(低于)Pod的数量，数值/百分比，默认25%
    type: <string> # RollingUpdate(默认)或OnDelete
status       <Object>
  collisionCount  <integer>   # 哈希冲突数量，借此避免产生哈希冲突
  conditions      <[]Object>  # 副本最新可用观察值
  currentNumberScheduled <integer> -required- # 允许且正在运行Daemon的节点数
  desiredNumberScheduled <integer> -required- # 应当运行Daemon的节点数
  numberAvailable    <integer>            # Daemon已可用的节点数
  numberMisscheduled <integer> -required- # 不应运行Daemon但正在运行的节点数
  numberReady        <integer> -required- # Daemon已就绪的节点数
  numberUnavailable  <integer>            # 应当运行但未运行Daemon的节点数
  observedGeneration     <integer>        # 反应最近副本的生成
  updatedNumberScheduled <integer>        # 正在进行Daemon更新的节点数

# Job
apiVersion: <string>
kind: <string>
metadata: <Object>
spec: <Object>
  activeDeadlineSeconds <integer>   # 允许启动的最长秒数，suspend时计时暂停
  backoffLimit             <integer># Job失败前的重试次数，默认为6
  completionMode        <string>    # NonIndexed(默认)或Indexed
  completions              <integer># 完成多少次Pod后 Job成功
                               # nil:任何Pod成功所有Pod成功，并行度任意正整数
                               # 1  :1个Pod成功则Job完成，并行度为1
  manualSelector        <boolean>   # 是否手动指定Pod标签（最好不用）
  parallelism              <integer># 并行度，多数Pod完成后实际值可能低于该值
  selector                 <Object> #
  suspend                  <boolean># True未建Pod不建,已建Pod删除 False(默认)
  template    <Object> -required-   #
  ttlSecondsAfterFinished <integer> # 作业完成后的生存时间 不设不删除 设0立删除
status:  <Object>
  active:            <integer> # 处于pending和running的Pod数量
  completedIndexes: <string>  # completionMode为Indexed时，记录完成索引
  completionTime:   <string>  # Job成功时，记录完成时间
  conditions:       <[]Object># Job当前状态：
    lastProbeTime:      <string> # 最近一次价差状态的时间
    lastTransitionTime: <string> # 最近一次状态转变的时间
    message:              <string> # 上次状态转换的描述
    reason:               <string> # 上次状态转换的原因
    status:   <string> -required-# 状态的情况 True, False, Unknown
    type:       <string> -required-# 状态类型Failed、Suspended、Complete
  failed            <integer> # Failed状态的Pod数量
  ready            <integer> # 就绪状态Pod数量
  startTime        <string>  # 开始处理Job的时间，每次暂停-重启后重置
  succeeded        <integer> # 处于succeeded状态pod数量
  uncountedTerminatedPods  <Object> # 保存Pod的UIDs，结束但未统计的Pod

# Job的完成模式
# (1) 分为NonIndexed(默认)或Indexed
# (2) NonIndexed 无索引模式模式
#         1) 每个Job完成事件都是独立无关且同质的
#         2) 成功完成的Pod个数达到.spec.completions值时认为Job已经完成
#         3) 当.spec.completions取值null时，Job被隐式处理为NonIndexed
# (3) Indexed 索引模式
#        1) Job 的 Pod 会分配对应的完成索引
#        2) 索引取值为 0 到.spec.completions-1
#        3) 当每个索引都对应一个完成的 Pod 时，Job 被认为是已完成的
#        4) 同一索引值可能被分配给多个Pod，但是只有一个会被记入完成计数
#        5) 索引暴露于各Pod中batch.kubernetes.io/job-completion-index注释
#           和JOB_COMPLETION_INDEX环境变量。
# (4) Indexed模式下，索引有三种获取方式：
#         1) 基于注解
#            Pod索引在注解batch.kubernetes.io/job-completion-index中呈现
#            具体表示为一个十进制值字符串。
#         2) 基于主机名
#            索引作为Pod主机名的一部分，遵循模式 $(job-name)-$(index)
#            用Indexed Job和Service时,内部Pods可通过DNS使用具体主机名互相寻址
#         3) 基于环境变量，对于容器化的任务，在环境变量 JOB_COMPLETION_INDEX 中体现。

# Indexed模式发布自定义索引
# (1) 三种获取索引的方式：注解，主机名，环境变量。
# (2) Downward API可用 环境变量 或 卷文件 将Pod的字段信息呈现给Pod中运行的容器:
#     1) Job控制器为所有容器设置的内置JOB_COMPLETION_INDEX环境变量。
#     2) Init容器将索引映射为静态值，并写入文件通过emptyDir卷与容器共享


# Pod失效有两种形式: 1) Pod管理的部分容器失效;  2) Pod失效
# (1) Pod管理的部分容器失效可能原因
#     1) 容器内进程退出时返回值非零
#     2) 容器因为超出内存约束而被杀死等
# (2) 若重启策略为OnFailure，则Pod留在节点，但容器重新运行，程序需处理本地重启能力
#     否则将重启策略设置为Never
# (3) 即使parallelism为1、completions为1且重启策略为Never，程序能可能被启动两次
# (1) Pod失效可能原因：
#     1) Pod启动时，节点失效（被升级、被重启、被删除等）
#     2) 容器启动失败并且设置restartPolicy = "Never"
# (2) Pod失败时Job控制器启动新的Pod处理旧Pod未完成的工作，程序需处理新Pod重启能力
#     如：处理之前运行所产生的临时文件、锁、不完整的输出等问题。
# (3) 若parallelism和completions都大于1，则同一时间会存在多个Pod，程序需处理并发

# k8s建议在调试Job时将`restartPolicy`设置为"Never"
# (1) Job Pod 重启策略
#     1) backoffLimit设置Job Pod回退失效策略，标识Job失败重试次数（默认6)
#     2) Job Pod失效会被Job控制器重建，回退重试时间按指数增长(10s、20s...6min) 
#     3) Job Pod被删除，或Pod成功且其他Pod未失败，失效回退的次数会被重置为0
# (2) 原因：
#     若重启策略设置为OnFailure则Job Pod到达失效回退次数上限时自动被终止
#     因此可能出现调试过程中Pod终止造成信息丢失，因此建议采用Never
```

```yaml
#######################################################################
# Pod资源
#######################################################################

ObjectMeta
metadata:  <Object>
  annotations: <map[string]string> # 非结构化键值对 不用于查询和匹配 仅添加信息
  generateName:  <string> # 可选前缀 由服务器使用 未提供name时生成唯一名称 
  labels: <map[string]string> # 组织/分类(确定范围/选择)对象的 键值对
  name:          <string> # name 在命名空间内必须是唯一的。
  namespace:     <string> # 一个值空间内部名称唯一，非NS作用域对象该值为空
# 系统字段
  finalizers: <[]string> # 从注册表中删除对象之前该字段必须为空。
  managedFields: <[]Object> # 用于内部管理
  ownerReferences: <[]Object> # 所依赖的对象列表 为空则本对象被回收 
    apiVersion: <string> -required- # 被引用资源的 API 版本。
    blockOwnerDeletion: <boolean> # 删除此引用前无法从键值存储中删除属主(false)
    controller:    <boolean> # 若本对象由控制器管理则为true，且本引用指向控制器
    kind: <string> -required- # 被引用资源的类别
    name: <string> -required- # 被引用资源的名称
    uid:  <string> -required- # 被引用资源的 uid
# 只读字段
  creationTimestamp: <string> # (只读)建此对象时的服务器时间
  deletionGracePeriodSeconds: <integer> # （只读）对象被删除前允许正常终止的秒数
  deletionTimestamp: <string> # (只读) 删除此资源的RFC3339日期和时间
  generation:    <integer> # 表示期望状态的特定生成的序列号 由系统填充 只读
  resourceVersion: <string> # 对象的内部版本 系统填充 只读 应将值视为不透明
  uid: <string> # 该对象在时间和空间上的唯一值 由服务器在成功创建资源时生成
# 其他
  clusterName: <string> # 所属集群名 区分有相同名称和NS但属于不同集群的Pod(被忽略)

# (1) kubernetes垃圾收集
#   1) 垃圾收集器用ownerReferences标识属主和附属，属主资源删除，附属资源辉自动被回收
#   2) Kubernetes会自动设置ownerReference，如创建控制器时，也可以手动设置指定关系
#   3) 删除时可指定是否该删除其附属 自动删除附属级联删除(Cascading Deletion) 
#   4) Kubernetes有两种级联删除模式：后台(Background)模式和前台(Foreground)模式
#   5) 删除对象时，不自动删除它的附属，这些附属被称作 孤立对象（Orphaned）。
# (2) 前台级联删除
#     根对象进入deletion in progress状态：
#   1) 对象仍然可以通过REST API可见
#   2) 对象的deletionTimestamp字段被设置。
#   3) 对象的metadata.finalizers字段包含值foregroundDeletion
#   4) 开始删除附属并在删除所有有阻塞能力的附属后删除属主对象
#      有阻塞能力:ownerReference.blockOwnerDeletion=true
# (3) 后台级联删除
#       Kubernetes会立即删除属主对象，随后垃圾收集器在后台删除其附属对象：
# (4) 级联删除策略
#      设置属主对象deleteOptions.propagationPolicy字段控制级联删除策略
#       通过指令`kubectl get pods N -o yaml`可查看该字段
#      1.20以后可以通过`kubectl delete deployment N --cascade=foreground`
#      可能的取值包括：Orphan、Foreground 或者 Background



# Pod容器
spec:
  containers: <[]Object> -required- # 容器列表 至少有一个容器 无法更新(增删)
  enableServiceLinks: <boolean> # 是否将服务信息注入Pod环境变量中(True)
  ephemeralContainers: <[]Object> # 临时容器列表 创建时不能指定
  imagePullSecrets: <[]Object> # 同一NS中Secret的引用列表，用于拉取镜像时的认证
  initContainers: <[]Object> #  Init容器列表 顺序执行 一个故障则Pod失败
  os: <Object> # 指定 Pod 中容器的操作系统
# ephemeralContainers使用方法
# kubectl debug podName -ti --image=imageName
# kubectl debug node nodeName -it --image=imageName

# 容器-镜像
# 容器-Entrypoint
# 容器-端口
# 容器-环境变量

# 容器-卷
spec:
  containers:
    volumeMounts: <[]Object> 
      mountPath: <string> -required- # 容器内Volume的挂载路径 不能含':'
      mountPropagation: <string> # 挂载如何从主机传播到容器，及如何反向传播
      name: <string> -required- # 必须与Volume名称匹配
      readOnly: <boolean> # 为true则以只读方式挂载(False)
      subPath: <string>   # 指定所引用的卷内的子路径，而不是其根路径。
      subPathExpr: <string> # 指定${XXX}环境变量获取，与subPath互斥
    volumeDevices: <[]Object> # 容器要使用的块设备列表 描述容器原始块设备映射
      devicePath: <string> -required- # 设备将被映射到的容器内的路径
      name: <string> -required- # 必须与Pod中persistentVolumeClaim名称匹配
# 卷的挂载传播由mountPropagation字段控制,值包含如下三种
# None: (默认)此卷挂载不会接收到任何后续挂载到该卷或是挂载到该卷的子目录下的挂载。
#       在宿主机上不会显示容器创建的挂载，容器内和宿主机的后续挂载完全隔离。
#       等同于Linux内核文档中所述的 private 传播。
# HostToContainer:此卷挂载将会接收到任何后续挂载到该卷或是挂载到该卷的子目录下的挂载。
#       如果宿主机在卷挂载点中挂载任何内容，则容器将看到新的挂在内容。
#       有Bidirectional的Pod挂载传播到该卷挂载上, HTC挂载传播也可以看见。
#       等同于Linux内核文档中描述的rslave挂载传播。
# Bidirectional:类似HTC
#       容器创建的所有卷挂载都将传播回主机和所有使用相同卷的Pod的所有容器。
#        Bidirectional挂载传播很危险，可能会危害到host 的操作系统。
#        因此只有特权 securityContext: privileged: true 容器在允许使用它。
#       等同于Linux内核文档中描述的rshared安装传播。
# subPath用途及与subPathExpr区别：
# (1) 一个共享卷, 挂载多个路径。
# (2) ConfigMap或Secret挂载到特定目录的特定路径, 且该目录下已有文件且不希望被覆盖掉。
# (1) subPath直接指定子目录的名字，subPathExpr则指定${XXX}，通过环境变量获取

# 容器-资源
# 容器-生命周期
# 容器-安全上下文
# 容器-调试
```

```yaml
#######################################################################
# 存储
#######################################################################
# 存储类型：
# (1) kubernetes资源对象映射为目录或文件: 
#     ConfigMap            (应用配置)
#     Secret               (加密数据)
#     DownwardAPI          (Pod或Container的元数据信息)
#     ServiceAccountToken  (Service Account中的Token数据)
#     Projected Volume     (将一个或多个上述资源挂载到容器内同一个目录下)
# (2) kubernetes管理的宿主机本地存储：
#     emptyDir             (临时存储)
#     hostPath             (宿主机目录)
# (3) 持久化存储PV和网络存储
#     NFS                  (网络文件系统)
#     Local                (本地化持久存储)
# (4) 存储厂商提供的存储卷
#     ScaleIO Volumes、StorageOS
# (5) 公有云提供的存储卷
#     AWSElasticBlockStore、AzureDisk

# emptyDir简介
# (1) Pod调度到节点后先创建emptyDir，只要Pod在该节点上运行，该卷就会存在。
# (2) emptyDir最初是空的。
# (3) Pod中容器可以读写emptyDir卷中的相同文件，尽管该卷在每个容器中挂在路径不同。
# (4) 从节点中删除Pod时，emptyDir中的数据将被永久删除。
# (5) 用法：
#         1) 暂存空间，例如用于基于磁盘的合并排序
#         2) 用作长时间计算崩溃恢复时的检查点
#         3) Web服务器容器提供数据时，保存内容管理器容器提取的文件

kind: Pod
spec:
  volumes:
    name: <string> -required- # 卷名 Pod内唯一
# 持久化存储
    persistentVolumeClaim: <Object> # 引用同一NS中的PVC 绑定PV并挂载
      claimName: <string> -required- # PVC名称
      readOnly:  <boolean> # 是否只读(False)
# 资源对象映射
spec:
  volumes:
    name: <string> -required- # 卷名 Pod内唯一
    configMap: <Object> # 将data中内容以文件形式放在卷中 键名为文件名
      defaultMode: <integer> # 文件权限 0000到0777之间
      items: <[]Object>     # 未指定时data每个字段一个文件，
        key: <string> -required- # 将键映射到路径 不指定不显示 指定不存在报错
        mode: <integer>             # 文件权限 0000到0777之间
        path: <string> -required-# 相对路径 但不能包含'..'也不能以此开头
      name: <string>         # 被引用资源的名称
      optional: <boolean>   # 指定是否所引用的ConfigMap或其键必须已经被定义
spec:
  volumes:
    name: <string> -required- # 卷名 Pod内唯一
    secret: <Object>
      defaultMode: <integer>  # 文件权限 0000到0777之间 默认0644
      items: <[]Object>
        key: <string> -required- # 将键映射到路径 不指定不显示 指定不存在报错
        mode: <integer>             # 文件权限 0000到0777之间
        path: <string> -required-# 相对路径 但不能包含'..'也不能以此开头
      optional: <boolean>     # 是否 Secret 或其键必须已经定义
      secretName: <string>    # 与Pod相同NS的Secret的名称
spec:
  volumes:
    name: <string> -required- # 卷名 Pod内唯一
    downwardAPI: <Object>
      defaultMode: <integer> # 文件权限 0000到0777之间 默认0644
      items: <[]Object>         # 卷文件的列表
        fieldRef: <Object>   # 选择Pod的字段：支持注解、标签、名称和NS、uid
          apiVersion: <string> # Pod的API版本 默认v1
          fieldPath: <string> -required- # 以'metadata.'、'status.'开头
        mode: <integer>         # 文件权限 0000到0777之间
        path: <string> -required- # 相对路径 但不能包含'..'也不能以此开头
        resourceFieldRef: <Object> # 选择容器的资源
          containerName: <string>       # 容器名称
          divisor: <string>             # 指定输出格式 默认为 "1"
          resource: <string> -required- # 资源类型
        # 仅支持limits.cpu、limits.memory、requests.cpu、requests.memory
spec:
  volumes:
    name: <string> -required- # 卷名 Pod内唯一
    projected: <Object> # 投射卷 可以将多种资源映射到同一个目录下
      defaultMode: <integer>  # 文件权限 0000到0777之间
      sources: <[]Object>   # 投射卷列表
        configMap: <Object> # 
          items: <[]Object>
            key: <string> -required- # 将键映射到路径
            mode: <integer>          # 文件权限 0000到0777之间
            path: <string> -required-# 相对路径 但不能包含'..'也不能以此开头
          name: <string>       # 与Pod相同NS的Secret的名称
          optional: <boolean>  # 是否 Secret 或其键必须已经定义
        downwardAPI: <Object>
          items: <[]Object>         # 卷文件的列表
            fieldRef: <Object>   # 选择Pod的字段：仅注解、标签、名称和NS、uid
            mode: <integer>         # 文件权限 0000到0777之间
            path: <string> -required- # 相对路径 但不能包含'..'也不能以此开头
            resourceFieldRef: <Object> # 选择容器的资源
        secret: <Object>
          items: <[]Object>
            key: <string> -required- # 将键映射到路径
            mode: <integer>             # 文件权限 0000到0777之间
            path: <string> -required-# 相对路径 但不能包含'..'也不能以此开头
          name: <string>       # 与Pod相同NS的Secret的名称
          optional: <boolean>  # 是否 Secret 或其键必须已经定义
        serviceAccountToken: <Object> # 服务账号令牌数据
          audience: <string> # 令牌的目标受众 默认为apiserver 
          expirationSeconds: <integer> # 请求的服务账号令牌的有效期 默认1h
          path: <string> -required- # 相对目标文件挂载点的路径

# 宿主机本地存储
spec:
  volumes:
    name: <string> -required- # 卷名 Pod内唯一
    emptyDir: <Object> # 空目录卷支持所有权管理和SELinux重新打标签
      medium:    <string> # 目录的存储介质 空字符串""(默认)或Memory
      sizeLimit: <string> # 卷所需的本地存储总量 默认nil未定义
spec:
  volumes:
    name: <string> -required- # 卷名 Pod内唯一
    hostPath: <Object> # 主机目录暴露给容器 用于系统代理或需要主机数据的特权操作
      path: <string> -required- # 目录在宿主机上的路径 符号链接会转为真实路径
      type: <string> # 卷的类型，默认为 ""

# emptyDir
# (1) 在Pod分配到Node上时被创建
# (2) 在Node上自动分配一个目录，无需指定宿主机Node上对应的目录文件
# (3) 这个目录的初始内容为空
# (4) Pod从Node上移除时，emptyDir中的数据会被永久删除
# (5) 容器的crashing事件并不会导致emptyDir中的数据被删除
# (6) emptyDir可以在以下几种场景下使用：
#      1) 临时空间，例如基于磁盘的合并排序
#      2) 设置检查点以从崩溃事件中恢复未执行完毕的长计算
#      3) 保存内容管理器容器从Web服务器容器提供数据时所获取的文件

# (1) hostPath 的一些用法有：
#     1) 运行需要访问Docker配置文件的容器，挂载 /var/lib/docker
#     2) 在容器中运行cAdvisor，以hostPath方式挂载/sys
# (2) 注意事项
#      1) 同配置pod(如template创建)在不同Node由于映射文件不同可能上表现不同
#      2) 设置资源敏感的调度器时，hostPath使用的资源不会被调度器统计在内
#      3) 宿主机创建的目录仅root有写权限 因此要privileged 或修改宿主机文件权限
# (3) hostPath.type取值
# ""                   向后兼容 安装hostPath卷前不执行检查(默认)
# DirectoryOrCreate    路径不存在则创建空目录,权限0755,kubelet相同组和属主信息
# Directory            在给定路径上必须存在的目录
# FileOrCreate         文件不存在则创建空文件 权限0644,kubelet相同组和所有权
# File                 在给定路径上必须存在的文件
# Socket               在给定路径上必须存在的UNIX套接字
# CharDevice           在给定路径上必须存在的字符设备
# BlockDevice          在给定路径上必须存在的块设备


# 持久卷
  cephfs: <Object>
    monitors: <[]string> -required- # Ceph监测的集合
    path: <string>          # 挂载的根而非Ceph 树 默认"/"
    readOnly: <boolean>     # 是否只读 默认false
    secretFile: <string>    # User对应的密钥环路径 默认/etc/ceph/user.secret
    secretRef: <Object>        # 对用户身份认证Secret的引用 默认为空
    user <string>            # rados用户名 默认为 admin
  csi  <Object>
    driver: <string> -required- # 处理此卷的 CSI 驱动的名称
    fsType: <string>    # 要挂载的fsType 如ext4、xfs、ntfs等
    nodePublishSecretRef: <Object> # Secret的引用 传递到CSI驱动以完成发布
    readOnly: <boolean>               # 是否只读 默认false
    volumeAttributes: <map[string]string> # 存储传递给CSI驱动的属性
  nfs  <Object>


# ConfigMap字段列表
apiVersion: <string> # v1
kind: <string> # ConfigMap
metadata: <Object>
binaryData: <map[string]string> # 二进制数据 键仅由[alnum-_.]组成 值任意
data: <map[string]string>         # 配置数据 键名不能重复也不能与binaryData重复
immutable: <boolean>            # 为true则不会更新ConfigMap中存储的数据

# ConfigMap限制条件
# (1) ConfigMap必须在Pod之前创建，Pod才能引用它
# (2) 如果Pod使用envFrom基于ConfigMap定义环境变量，则无效的环境变量名称被忽略
#      并在事件中被记录为InvalidVariableNames
# (3) ConfigMap受命名空间限制，只有处于相同命名空间中的Pod才能引用
# (4) ConfigMap无法用于静态Pod

# Secret字段列表
apiVersion: <string>
kind:<string>
metadata: <Object>
data: <map[string]string>    # 含保密数据 键仅由[alnum-_.]组成
immutable: <boolean>         # 为true则不会更新Secret中存储的数据
stringData: <map[string]string> # 字符串数据 但写入时并入data字段并加密覆盖原字段
type <string>:                  
# Secret.type类型
# Opaque                                用户定义的任意数据
# kubernetes.io/service-account-token   服务账号令牌
# kubernetes.io/dockercfg               ~/.dockercfg文件的序列化形式
# kubernetes.io/dockerconfigjson        ~/.docker/config.json文件的序列化形式
# kubernetes.io/basic-auth              用于基本身份认证的凭据
# kubernetes.io/ssh-auth                用于SSH身份认证的凭据
# kubernetes.io/tls                     用于TLS客户端或者服务器端的数据
# bootstrap.kubernetes.io/token         启动引导令牌数据


# PersistentVolume 和 PersistentVolumeClaim概念
# (1) PV是由管理员设置的存储，是群集一部分，是集群中的资源。 
# (2) PV独立于使用PV的Pod 的生命周期，即使Pod被删除PV依然保留
# (1) PVC是用户存储的请求
# (2) 与Pod相似
#        Pod消耗Node资源，PVC消耗PV资源
#        Pod请求指定数量资源(CPU、内存)。PVC可以请求指定PV大小和访问模式

# PersistentVolume字段列表
apiVersion: <string>    # v1
kind:         <string>  # PersistentVolume
metadata:     <Object>
spec:         <Object>
  accessModes: <[]string>       # 访问模式 挂载卷的方式
  capacity: <map[string]string> # 卷的资源和容量
    storage: <string>
  claimRef: <Object>            # 所绑定PVC的信息
    apiVersion: <string>    # 被引用者的 API 版本
    fieldPath: <string>     # spec.containers[2] spec.containers{name}
    kind: <string>          # 被引用者的类别
    name: <string>          # 被引用对象的名称
    namespace: <string>     # 被引用对象的名字空间
    resourceVersion: <string> # 被引用对象的特定资源版本
    uid: <string>           # 被引用对象的UID
  mountOptions: <[]string>  # 挂载选项列表["ro","soft"]无合法性检查 无效只失败
  nodeAffinity: <Object>
    required: <Object>
      nodeSelectorTerms: <[]Object> -required-
        matchExpressions: <[]Object>
        matchFields: <[]Object>
  persistentVolumeReclaimPolicy: <string> # 释放持久卷时的操作 Retain/Delete
  storageClassName: <string> # 持久卷所属于的StorageClass的名称
  volumeMode: <string> # 文件系统还是块设备 spec不含该字段则取值为Filesystem
# Local
  hostPath: <Object> # 主机上的目录 仅用于单节点开发和测试
    path: <string> -required- # 目录在主机上的路径
    type: <string>              # 默认为 ""
  local: <Object>     # 具有节点亲和性的直连式存储 （Beta 特性）
    fsType: <string>           # 要挂载的文件系统类型
    path: <string> -required-  # 节点上卷的完整路径 可以是一个目录或块设备
# 持久卷
  cephfs: <Object>
  csi:    <Object>
  nfs:    <Object>
    path:     <string> -required- # 由NFS服务器允许访问的路径
    readOnly: <boolean>           # 是否只读
    server:   <string> -required- # NFS服务器IP
status: <Object>


# accessModes 访问模式
# (1) 种类
# 1) ReadWriteOnce    该卷可被单个节点以读/写模式挂载(可以被同一节点多个Pod访问)
# 2) ReadOnlyMany     该卷可被多个节点以只读模式挂载
# 3) ReadWriteMany    该卷可被多个节点以读/写模式挂载
# 4) ReadWriteOncePod 该卷可被单个节点以读/写模式挂载(确保集群仅1个Pod可读写该PVC)
# (2) 命令行接口（CLI）中的缩写
# 1) RWO - ReadWriteOnce
# 2) ROX - ReadOnlyMany
# 3) RWX - ReadWriteMany
# 4) RWOP - ReadWriteOncePod
# (3) 说明：
# 1) 卷的访问模式用来匹配PVC和PV
# 2) 卷访问模式会限制PV的挂载位置
# 3) 卷访问模式并不会在存储已经被挂载的情况下为其实施写保护
# 4) 每个卷同一时刻只能以一种访问模式挂载(到多个节点或pod)，即使该卷能支持多种访问模式


# persistentVolumeReclaimPolicy 回收策略
# Retain (保留)       不清理,保留Volume (需要手动清理)
# Recycle(回收)       删除数据，即rm -rf *     (废弃)
# Delete (删除)       删除存储资源
# 仅NFS和HostPath支持回收策略。AWS EBS、GCE PD、Azure Disk和Cinder卷支持删除策略

# PV的状态
# (1) Available        可用
# (2) Bound            已经分配给PVC
# (3) Released        PVC解绑但还未执行回收策略
# (4) Failed        发生错误

# 静态：集群管理员创建
# 动态：静态PV与PVC均不匹配时，群集尝试为PVC动态配置卷。
#      此配置基于StorageClasses：PVC必须请求存储类管理员必须已创建并配置该类
#      集群管理员需要启用API Server上的DefaultStorageClass[准入控制器]。
#      如确保DefaultStorageClass位于API Server组件的--admission-control列表中
# 绑定：PVC 跟 PV 绑定是一对一的映射 若没有匹配的PV，PVC将无限期地保持未绑定状态。
# PVC保护：确保pod使用中的PVC不会从系统中移除，否则可能导致数据丢失
#         pod为Pending且pod已调度到节点或pod为Running时 PVC处于活动状态
#         开启PVC保护 删除使用中的PVC，PVC的删除将被推迟 直到PVC不再被任何pod使用

# PVC
apiVersion: <string> # v1
kind:         <string> # PersistentVolumeClaim
metadata:     <Object>
spec:         <Object>
  accessModes: <[]string> # 预期的访问模式
  resources: <Object>     # 卷应拥有的最小资源
    limits:   <map[string]string> # 允许的最大计算资源量
    requests: <map[string]string> # 所需的最小计算资源量
  selector: <Object>      # 绑定时对卷进行选择所执行的标签查询
    matchExpressions: <[]Object>
    matchLabels:      <map[string]string>
  storageClassName: <string> # 绑定所用的SC名称
  volumeMode: <string>       # Volume的类别 默认Filesystem
  volumeName: <string>      # 所绑定PV的名称
# Beta
  dataSource: <Object> # VolumeSnapshot 还是 PVC
  dataSourceRef: <Object>
status:     <Object>

# PV和PVC生命周期
# (1) Provisioning 配置阶段。PV有静态和动态两种提供方式
#     1) 静态提供是K8s管理员创建多个PV，存储空间等属性确定，和存储设备完成关联
#     2) 动态提供需要StorageClass支持，K8s尝试为PVC动态创建PV。
#        优点：避免 低需求PVC绑定大容量PV、多个低容量PV不能满足一个大需求PVC
# (2) Binding PVC与PV绑定的过程
#        若PV都不能满足PVC需求，则PVC无法被创建，相应Pod也不会被创建
# (3) Using 绑定后Pod对存储空间的使用过程
# (4) Releasing Pod删除或不再使用PV后，K8s删除PVC对象并回收PV资源时的状态
#         但此时PV还要处理完Pod在该卷存储的信息后才能够被使用
# (5) Reclaiming PV的回收策略对被释放的PV的处理过程。
# (6) Recycling 根据配置，有时PV会删除掉空间中所有信息被再次使用

# storageClass
apiVersion:  <string> # storage.k8s.io/v1
kind:         <string> # StorageClass
metadata:     <Object>
provisioner: <string> -required- # PV制造者(制备器)的类别
allowVolumeExpansion: <boolean>  # 存储类是否允许卷扩充
allowedTopologies:   <[]Object>  # 限制可以动态制备卷的节点拓扑
  matchLabelExpressions: <[]Object>
    key: <string> -required-
    values: <[]string> -required-
mountOptions: <[]string>  # 挂载选项如 ["ro", "soft"]
parameters: <map[string]string>  # 创建此存储类卷的制备器的参数
reclaimPolicy:    <string>       # 回收策略默认delete
volumeBindingMode: <string>      # 绑定模式 默认VolumeBindingImmediate
```

```yaml
######################################################################
# 集群安全
######################################################################
# API Server的安全策略
# (1) 认证（Authentication）
# (2) 鉴权（Authorization）
# (3) 准入控制（Admission Control）

# 认证（Authentication）
# (1) HTTP Token认证: 通过Token来识别合法用户
#  1) Token是复杂字符串，对应一个用户名。
#  2) 客户端发起API调用请求时，需要在HTTP Header里放入Token
# (2) HTTP Base认证 : 通过 用户名+密码 的方式认证
#  1) 格式为 用户名:密码 
#  2) BASE64算法编码的字符串放在HTTP Request中的Heather Authorization域里
# (3) HTTPS 证书认证 : 双向认证

# 认证组件的两种类型：
# (1) Kubenetes组件对API Server的访问：
#     kubectl、Controller Manager、Scheduler、kubelet、kubeproxy
# (2) Kubernetes管理的Pod对容器的访问：
#     Pod（dashborad 也是以 Pod 形式运行）

# 端口访问说明
# Controller Manager、Scheduler为本机组件与API Server在同一node用非安全端口访问
# 1) 默认为端口 8080，使用 --insecure-port 进行更改
# 2) 默认 IP 为 localhost，使用 --insecure-bind-address 进行更改
# 3) 请求 绕过 身份认证和鉴权模块 由准入控制模块处理的请求
# kubectl、kubelet、kube-proxy 为远程组件访问API Server要证书进行HTTPS双向认证
# 1) 默认端口 6443，使用 --secure-port 更改
# 2) 默认 IP 是第一个非本地网络接口，使用 --bind-address 更改
# 3) 请求须经身份认证和鉴权组件处理 请求须经准入控制模块处理

# 证书颁发的两种方式
# (1) 手动签发：通过k8s集群的根ca进行签发HTTPS证书
# (2) 自动签发：kubelet首次访问API Server时，使用token做认证，通过后
#               Controller Manager会为kubelet生成一个证书后续访问以此认证

# kubeconfig（一个文件类型）
# (0) 包含了怎么访问服务的信息以及认证信息
# (1) 集群参数（CA证书、API Server地址）
# (2) 客户端参数（上面生成的证书和私钥）
# (3) 集群 context 信息（集群名称、用户名）
# (e) Kubenetes组件通过启动时指定不同的kubeconfig文件可以切换到不同的集群


# ServiceAccount要解决的问题
# Pod中容器访问API Server的问题：因为Pod的创建、销毁是动态的，难以手动生成证书
# 解决方案：Kubenetes使用Service Account解决Pod访问API Server的认证问题

# ServiceAccount（SA）（给Pod颁发证书）
# (1) 默认 每个NS都会有一个ServiceAccount，Pod创建时未指定SA则使用NS的SA
# (2) SA自动创建自动挂载到Pod的/run/secrets/kubernetes.io/serviceaccount
# (3) ServiceAccount 中包含三个部分：
#  1) Token:  使用API Server私钥签名的JWT 用于访问API Server时Server 端认证
#  2) ca.crt: 根证书 用于Client端验证API Server发送的证书
#  3) namespace: 标识这个service-account-token的作用域名空间
# (4) Secret 与 SA 的关系
#     Secret对象的类型有保存用户自定义保密信息的Opaque和ServiceAccountToken等

# Json web token (JWT)
# Json web token (JWT)是为了在网络应用环境间传递声明而执行的一种基于JSON的开放标准
# 该token被设计为紧凑且安全的，特别适用于分布式站点的单点登录（SSO）场景。
# JWT的声明一般用于在身份提供者和服务提供者间传递被认证的用户身份信息，以便于获取资源
# 也可以增加一些额外的其它业务逻辑所必须的声明信息， token也可直接被用于认证，可被加密



# 授权（Authorization）
# 认证确认通信的双方可信可以通信 鉴权确定请求方有哪些资源的权限
# API Server支持以下几种授权策略 通过API Server启动参数--authorization-mode设置
# (1) AlwaysDeny： 表示拒绝所有的请求，一般用于测试
# (2) AlwaysAllow：允许接收所有请求，如果集群不需要授权流程，则可以采用该策略
# (3) ABAC（Attribute-Based Access Control）：基于属性的访问控制
#      表示使用用户配置的授权规则对用户请求进行匹配和控制
# (4) Webbook：通过调用外部 REST 服务对用户进行授权
# (5) RBAC（Role-Based Access Control）（默认）：基于角色的访问控制

# RBAC（Role-Based Access Control）基于角色的访问控制
# RBAC优势及概述：
# (1) 对集群中的资源和非资源均拥有完整的覆盖
#  1) RBAC由几个API对象实现，可用kubectl或API操作、可运行时调整无需重启API Server
#  2) RBAC引入4个资源对象：Role、ClusterRole、RoleBinding、ClusterRoleBinding
#  3) Role和RoleBinding是名称空间级别资源
#        ClusterRole 和 ClusterRoleBinding 是集群级别资源
#  4) Role指定一些角色，不同角色对资源的权限不同
#      RoleBinding将这些角色赋予给用户、组和SA 

# k8s不会提供用户管理，那么User、Group、ServiceAccount 指定的用户又是从哪里来的呢？ 
# k8s组件(kubectl、kube-proxy)或自定义的用户向CA申请证书时，需要提供证书请求文件：
{
  "CN": "admin",    # Common Name(CN)，公用名，一般是主机名+网站域名
  "hosts": [],
  "key": {
    "algo": "rsa",
    "size": 2048
  },
  "names": [
    {
      "C": "CN",        # Country Code(C)：国家，只能是两个字母的国家码
      "ST": "HangZhou",            # State or Province(S)，省名或者州名
      "L": "XS",                # Locality(L)，城市名
      "O": "system:masters",    # Organization Name(O)，单位名称
      "OU": "System"    # Organization Unit(OU)，部门
    }
  ]
}
# (1) API Server会把客户端证书的CN字段作为User把names.O字段作为Group
# (2) kubelet使用TLS Bootstaping认证时，API Server可用Bootstrap Tokens或者
#     Token authentication file验证=token，k8s为token绑定默认的User和Group
# (3) Pod使用ServiceAccount认证时，service-account-token中的JWT会保存User信息
#     再创建一对 角色/角色绑定（集群角色/集群角色绑定）资源对象，就可以完成权限绑定了


# 准入控制
# 准入控制概念
# 准入控制是API Server的插件集合，通过添加不同的插件，实现额外的准入控制规则
# API Server的一些主要的功能都需要通过Admission Controllers实现，比如SA

# 几个插件的功能：
# (1) NamespaceLifecycle： 防止在不存在的namespace上创建对象防止删除系统预置
#       namespace，删除 namespace 时，连带删除它的所有资源对象。
# (2) LimitRanger：确保请求资源不超过资源所在Namespace的LimitRange的限制。
# (3) ServiceAccount：实现了自动化添加 ServiceAccount。
# (4) ResourceQuota：确保请求的资源不会超过资源的 ResourceQuota 限制。

# 准入控制的操作
# (1) 启用 NamespaceLifecycle 和 LimitRanger 准入控制插件：
kube-apiserver --enable-admission-plugins=NamespaceLifecycle,LimitRanger
# (2) 禁用插件
kube-apiserver --disable-admission-plugins=PodNodeSelector,AlwaysDeny ...
# (3) 查看默认启用的插件
kube-apiserver -h | grep enable-admission-plugins
```

```bash
######################################################################
# kubectl常用指令
#######################################################################

source <(kubectl completion bash) # 指令补全
cat > ~/.vimrc <<-EOF              # 自定义vim
set expandtab
set ts=2            # tabstop的缩写
set shiftwidth=2    # 每级缩进
set autoindent         # 自动缩进
EOF
```

### 参考资料

https://jimmysong.io/kubernetes-handbook/guide/using-kubectl.html
https://lib.jimmysong.io/
