# LoadBalancer-MatelLB

## 1. 背景

在k8s中创建service时，需要指定`type`类型，可以分别指定`ClustrerIP,NodePort,LoadBalancer`三种，其中前面两种无论在内网还是公网环境下使用都很常见，只有`LoadBalancer`大部分情况下只适用于支持外部负载均衡器的云提供商（AWS,阿里云,华为云等）使用。

如果想要在内网环境中，使用`type=LoadBalancer`就需要部署另外的插件，下面主要介绍一下MetalLB组件。

## 2. MetalLB介绍

MetalLB部署在k8s中，为k8s集群提供了网络负载均衡器， 它主要提供两个功能：地址分配和外部通知。

### 2.1 地址分配

在公有云环境下，当购买或指定一个负载均衡器时，云平台将为用户分配一个IP地址，通过这个IP地址就能实现LoadBalancer，而在私有云集群中，MetalLB将负责IP地址的分配。

MetalLB无法凭空创建IP地址，因此需要在配置过程中为MetalLB指定一个IP地址池，当服务创建或者删除时，MetalLB负责从IP地址池中分配或者销毁服务对应的IP地址。

### 2.2 外部通知

一旦MetalLB为服务分配了外部IP地址，它就需要使群集之外的网络意识到该IP在群集中“存在”。MetalLB使用标准路由协议来实现此目的：ARP，NDP或BGP。

### 2.3 二层模式(ARP/NDP)

在二层模式下，一个节点承担向本地网络发布服务的责任。从网络的角度看，这台机器看起来好像已经为其网络接口分配了多个IP地址。

二层模式的主要优点是它的通用性,可以在任何以太网网络上运行，不需要特殊的硬件（路由器等）。

### 2.3.1 负载均衡

在二层模式下，**服务IP的所有流量都流向一个节**点。从那里， kube-proxy将流量传播到所有服务的Pod。

从这个意义上讲，二层没有实现负载平衡器。相反，它实现了**故障转移机制**，以便当当前的领导节点由于某种原因发生故障时，另一个节点可以接管。

如果领导节点由于某种原因失败，则故障转移是自动的，此时新节点将接管发生故障的节点的IP地址所有权。

### 2.3.2 局限性

- 单节点瓶颈

单个领导者当选节点接收服务IP的所有流量。这意味着服务的入口带宽被限制为单个节点的带宽。

在当前的实现中，节点之间的故障转移取决于客户端的合作。当发生故障转移时，MetalLB发送大量免费的二层数据包，以通知客户端与服务IP关联的MAC地址已更改。

- 故障转移速度慢

所有主要版本的现代操作系统（Windows，Mac，Linux）都能正确处理“免费”数据包，并迅速更新其邻居缓存。在这种情况下，故障转移将在几秒钟内发生。但是，某些系统要么根本不执行免费处理，要么存在错误的实现，从而延迟了缓存的更新。

### 2.4 BGP模型

在BGP模式下，群集中的每个节点都与网络路由器建立BGP对等会话，并使用该对等会话来通告外部群集服务的IP。

如果路由器配置为支持多路径，则可以实现真正的负载平衡，MetalLB发布的路由彼此等效，除了它们的下一跳。这意味着路由器将一起使用所有下一跳，并在它们之间进行负载平衡。

数据包到达节点后，`kube-proxy`负责流量路由的最后一跳，以将数据包到达服务中的一个特定容器。

> 由于硬件环境的约束，作者没有在BGP模式下进行试验，因此，有关BGP模型更详细的介绍，请参见[MetalLB官方文档](https://link.zhihu.com/?target=https%3A//metallb.universe.tf/concepts/bgp/)

## 3. 部署MetalLB

### 3.1 部署

```text
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.9.3/manifests/namespace.yaml
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.9.3/manifests/metallb.yaml
# On first install only
kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)"
```

**注：有些网络环境不好朋友，不能下载yaml文档，本文也附上yaml文件对应的内容** - namespace.yaml

```text
apiVersion: v1
kind: Namespace
metadata:
  name: metallb-system
  labels:
    app: metallb
```

- metallb.yaml

```text
[root@t34 metallb]# cat metallb.yaml 
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  labels:
    app: metallb
  name: controller
  namespace: metallb-system
spec:
  allowPrivilegeEscalation: false
  allowedCapabilities: []
  allowedHostPaths: []
  defaultAddCapabilities: []
  defaultAllowPrivilegeEscalation: false
  fsGroup:
    ranges:
    - max: 65535
      min: 1
    rule: MustRunAs
  hostIPC: false
  hostNetwork: false
  hostPID: false
  privileged: false
  readOnlyRootFilesystem: true
  requiredDropCapabilities:
  - ALL
  runAsUser:
    ranges:
    - max: 65535
      min: 1
    rule: MustRunAs
  seLinux:
    rule: RunAsAny
  supplementalGroups:
    ranges:
    - max: 65535
      min: 1
    rule: MustRunAs
  volumes:
  - configMap
  - secret
  - emptyDir
---
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  labels:
    app: metallb
  name: speaker
  namespace: metallb-system
spec:
  allowPrivilegeEscalation: false
  allowedCapabilities:
  - NET_ADMIN
  - NET_RAW
  - SYS_ADMIN
  allowedHostPaths: []
  defaultAddCapabilities: []
  defaultAllowPrivilegeEscalation: false
  fsGroup:
    rule: RunAsAny
  hostIPC: false
  hostNetwork: true
  hostPID: false
  hostPorts:
  - max: 7472
    min: 7472
  privileged: true
  readOnlyRootFilesystem: true
  requiredDropCapabilities:
  - ALL
  runAsUser:
    rule: RunAsAny
  seLinux:
    rule: RunAsAny
  supplementalGroups:
    rule: RunAsAny
  volumes:
  - configMap
  - secret
  - emptyDir
---
apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    app: metallb
  name: controller
  namespace: metallb-system
---
apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    app: metallb
  name: speaker
  namespace: metallb-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    app: metallb
  name: metallb-system:controller
rules:
- apiGroups:
  - ''
  resources:
  - services
  verbs:
  - get
  - list
  - watch
  - update
- apiGroups:
  - ''
  resources:
  - services/status
  verbs:
  - update
- apiGroups:
  - ''
  resources:
  - events
  verbs:
  - create
  - patch
- apiGroups:
  - policy
  resourceNames:
  - controller
  resources:
  - podsecuritypolicies
  verbs:
  - use
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    app: metallb
  name: metallb-system:speaker
rules:
- apiGroups:
  - ''
  resources:
  - services
  - endpoints
  - nodes
  verbs:
  - get
  - list
  - watch
- apiGroups:
  - ''
  resources:
  - events
  verbs:
  - create
  - patch
- apiGroups:
  - policy
  resourceNames:
  - speaker
  resources:
  - podsecuritypolicies
  verbs:
  - use
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  labels:
    app: metallb
  name: config-watcher
  namespace: metallb-system
rules:
- apiGroups:
  - ''
  resources:
  - configmaps
  verbs:
  - get
  - list
  - watch
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  labels:
    app: metallb
  name: pod-lister
  namespace: metallb-system
rules:
- apiGroups:
  - ''
  resources:
  - pods
  verbs:
  - list
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  labels:
    app: metallb
  name: metallb-system:controller
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: metallb-system:controller
subjects:
- kind: ServiceAccount
  name: controller
  namespace: metallb-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  labels:
    app: metallb
  name: metallb-system:speaker
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: metallb-system:speaker
subjects:
- kind: ServiceAccount
  name: speaker
  namespace: metallb-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  labels:
    app: metallb
  name: config-watcher
  namespace: metallb-system
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: config-watcher
subjects:
- kind: ServiceAccount
  name: controller
- kind: ServiceAccount
  name: speaker
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  labels:
    app: metallb
  name: pod-lister
  namespace: metallb-system
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: pod-lister
subjects:
- kind: ServiceAccount
  name: speaker
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  labels:
    app: metallb
    component: speaker
  name: speaker
  namespace: metallb-system
spec:
  selector:
    matchLabels:
      app: metallb
      component: speaker
  template:
    metadata:
      annotations:
        prometheus.io/port: '7472'
        prometheus.io/scrape: 'true'
      labels:
        app: metallb
        component: speaker
    spec:
      containers:
      - args:
        - --port=7472
        - --config=config
        env:
        - name: METALLB_NODE_NAME
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
        - name: METALLB_HOST
          valueFrom:
            fieldRef:
              fieldPath: status.hostIP
    # 部署过程中有得节点7946端口被占用，导致节点上的pod运行失败，把METALLB_ML_BIND_ADDR注释掉之后，就能运行成功
      #  - name: METALLB_ML_BIND_ADDR 
      #    valueFrom:
      #      fieldRef:
      #        fieldPath: status.podIP
        - name: METALLB_ML_LABELS
          value: "app=metallb,component=speaker"
        - name: METALLB_ML_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: METALLB_ML_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: memberlist
              key: secretkey
        image: metallb/speaker:v0.9.3
        imagePullPolicy: IfNotPresent 
        name: speaker
        ports:
        - containerPort: 7472
          name: monitoring
        resources:
          limits:
            cpu: 100m
            memory: 100Mi
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            add:
            - NET_ADMIN
            - NET_RAW
            - SYS_ADMIN
            drop:
            - ALL
          readOnlyRootFilesystem: true
      hostNetwork: true
      nodeSelector:
        beta.kubernetes.io/os: linux
      serviceAccountName: speaker
      terminationGracePeriodSeconds: 2
      tolerations:
      - effect: NoSchedule
        key: node-role.kubernetes.io/master
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: metallb
    component: controller
  name: controller
  namespace: metallb-system
spec:
  revisionHistoryLimit: 3
  selector:
    matchLabels:
      app: metallb
      component: controller
  template:
    metadata:
      annotations:
        prometheus.io/port: '7472'
        prometheus.io/scrape: 'true'
      labels:
        app: metallb
        component: controller
    spec:
      containers:
      - args:
        - --port=7472
        - --config=config
        image: metallb/controller:v0.9.3
        imagePullPolicy: IfNotPresent 
        name: controller
        ports:
        - containerPort: 7472
          name: monitoring
        resources:
          limits:
            cpu: 100m
            memory: 100Mi
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
            - all
          readOnlyRootFilesystem: true
      nodeSelector:
        beta.kubernetes.io/os: linux
      securityContext:
        runAsNonRoot: true
        runAsUser: 65534
      serviceAccountName: controller
      terminationGracePeriodSeconds: 0
```

- config.yaml

```text
[root@t34 metallb]# cat config.yaml 
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: metallb-system
  name: config
data:
  config: |
    address-pools:
    - name: my-ip-space
      protocol: layer2
      addresses:
      - 192.168.5.5-192.168.5.9
```

其中，`192.168.5.5-192.168.5.9`是为MetalLB指定的IP资源池。

### 3.2 查看

```text
[root@t34 metallb]# kubectl get pod -n metallb-system
NAME                          READY   STATUS    RESTARTS   AGE
controller-59bf6b989f-82l4s   1/1     Running   0          34m
speaker-7x75j                 1/1     Running   0          2d22h
speaker-kbk5c                 1/1     Running   0          2d22h
speaker-lb8x7                 1/1     Running   0          2d22h
speaker-mblbt                 1/1     Running   0          2d22h
speaker-qnpsh                 1/1     Running   0          2d22h
[root@t34 metallb]# kubectl get cm -n metallb-system
NAME     DATA   AGE
config   1      3d
[root@t34 metallb]#
```

## 4. 测试

### 4.1 指定service的`type=LoadBalancer`

```text
[root@t34 metallb]# kubectl get svc |grep -i loadbalancer
NAME                                            TYPE           CLUSTER-IP      EXTERNAL-IP                                            PORT(S)                             AGE
myapp-svc                                       LoadBalancer   10.43.245.81    192.168.5.9                                            80:31714/TCP                        6d1h
webapp-svc                                      LoadBalancer   10.43.161.22    192.168.5.5                                            8000:32034/TCP                      28d
```

其中，`EXTERNAL-IP`为MetalLB分配的IP地址

### 4.2 不同的方式访问服务

以服务myapp-svc为例

```text
# cluserIP
[root@t32 python-client]# curl 10.43.245.81
Hello MyApp | Version: v2 | <a href="hostname.html">Pod Name</a>
# NodePort
[root@t32 python-client]# curl 192.168.4.32:31714
Hello MyApp | Version: v2 | <a href="hostname.html">Pod Name</a>
# LoadBalancer
[root@t32 python-client]# curl 192.168.5.9
Hello MyApp | Version: v2 | <a href="hostname.html">Pod Name</a>
```

### 4.3 验证MetalLB单节点的"负载均衡"

### 4.3.1 `service.spec.externalTrafficPolicy`

表示此服务是否希望将外部流量路由到节点本地或集群范围的端点。 有两个可用选项：Cluster（默认）和 Local。

- Cluster

使用Cluster流量策略，`kube-proxy`在收到流量的节点上进行负载平衡，并将流量分配到服务中的所有Pod。

此策略导致服务中所有Pod之间的流量均匀分布。但是，`kube-proxy`在进行负载平衡时，它将掩盖连接的源IP地址

- Local

使用Local流量策略，`kube-proxy`在收到流量的节点上，仅将流量发送到同一节点上的服务的pod 。节点之间没有“水平”流量。

由于`kube-proxy`不需要在群集节点之间发送流量，因此您的Pod可以看到传入连接的真实源IP地址。

该策略的缺点是传入流量仅流向服务中的某些Pod。当前不在领导者节点上的Pod不会接收任何流量，它们只是作为副本存在，以防需要进行故障转移。

### 4.3.2 `service.spec.externalTrafficPolicy=Cluster`

运行脚本

```text
for i in {1..10}; do curl 192.168.5.9; done
```

![](https://pic1.zhimg.com/80/v2-04fe4b58e02b13c11ab963f00354fb90_720w.webp)

service对应的4个pod,流量均匀地被分配到pod上。

### 4.3.3 `service.spec.externalTrafficPolicy=Local`

service对应的4个pod,分别运行在节点t90和t91上。

在节点t32上运行脚本，发现出现timeout,因为t32为非领导者，不会接受任何流量

在客户端上运行，MetalLB会将流量转发到t90(此时，t90为MetalLB选出的领导者)上。具体结果如下:

- 流量查看

![](https://pic3.zhimg.com/80/v2-82e92589f139a555a3148071a687b852_720w.webp)

- pod日志

![](https://pic2.zhimg.com/80/v2-d739e70e53e98bdb50987be6e9b85101_720w.webp)

![](https://pic3.zhimg.com/80/v2-abf4f3184b629ff8745c10bc64552152_720w.webp)

### 4.3.4 删除t90节点上的pod,并将t90设置为不可调度

```text
[root@t32 python-client]# kubectl cordon t90
node/t90 cordoned
[root@t32 python-client]# kubectl  delete pod myapp-deploy-v2-7fbfdfbb7b-lsdg6
pod "myapp-deploy-v2-7fbfdfbb7b-lsdg6" deleted
[root@t32 python-client]# kubectl  delete pod myapp-deploy-v3-6c67c5b878-89tq8
pod "myapp-deploy-v3-6c67c5b878-89tq8" deleted
[root@t32 python-client]# kubectl  get pod -o wide -l app=myapp
NAME                               READY   STATUS    RESTARTS   AGE    IP            NODE   NOMINATED NODE   READINESS GATES
myapp-deploy-v2-7fbfdfbb7b-qpkwd   1/1     Running   0          6d1h   10.42.15.25   t91    <none>           <none>
myapp-deploy-v2-7fbfdfbb7b-x9jzp   1/1     Running   0          57s    10.42.1.90    t32    <none>           <none>
myapp-deploy-v3-6c67c5b878-hjwg4   1/1     Running   0          34s    10.42.1.91    t32    <none>           <none>
myapp-deploy-v3-6c67c5b878-m9mzm   1/1     Running   0          6d1h   10.42.15.26   t91    <none>           <none>
[root@t32 python-client]# kubectl uncordon t90
node/t90 uncordoned
[root@t32 python-client]#
```

> btw: kubectl cordon/uncordon 的确非常好用，之前一直用taint打污点的方式  

查看结果，发现MetalLB选择的领导者为t32，并将全部的流量全部流向了t32上面的pod(这个层面上，t32上面的pod实现了负载均衡)。

![](https://pic2.zhimg.com/80/v2-8f031e02cbb498ca98d211afc01554f1_720w.webp)

![](https://pic4.zhimg.com/80/v2-d3c5c41fec56ac986e884ee03af7b657_720w.webp)

## 5. 其他特性

### 5.1 请求特定的资源池

要请求来自特定池的分配，请将`metallb.universe.tf/address-pool`注释添加 到service中，并将地址池的名称作为annotations值.

```text
apiVersion: v1
kind: Service
metadata:
  name: nginx
  annotations:
    metallb.universe.tf/address-pool: production-public-ips
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: nginx
  type: LoadBalancer
```

### 5.2 共享IP

如果service需要占用的MetalLB中IP地址池的资源比较多，可以设置将多个服务共享同一个IP地址。

默认情况下，服务不共享IP地址。如果需要将服务并置在单个IP上，则可以通过将`metallb.universe.tf/allow-shared-ip`注释添加到service来启用选择性IP共享。

注释的值是“共享密钥”。服务可以在以下情况下共享IP地址：

- 都有相同的共享密钥。
- 要求使用不同的端口（例如，一个使用tcp / 80，另一个使用tcp / 443）。
- 都使用Cluster外部流量策略，或者都指向 完全相同的Pod集（即Pod选择器相同）。

```text
[root@t32 python-client]# kubectl  get svc myapp-svc -o yaml
apiVersion: v1
kind: Service
metadata:
  annotations:
    ...
    metallb.universe.tf/allow-shared-ip: 192.168.5.9
  name: myapp-svc
  namespace: default
spec:
  clusterIP: 10.43.245.81
  externalTrafficPolicy: Cluster
  ports:
  - nodePort: 31714
    port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: myapp
  sessionAffinity: None
  type: LoadBalancer
[root@t32 python-client]# kubectl  get svc webapp-svc-2  -o yaml
apiVersion: v1
kind: Service
metadata:
    annotations
      metallb.universe.tf/allow-shared-ip: 192.168.5.9
  name: webapp-svc-2
  namespace: default
spec:
  clusterIP: 10.43.161.182
  externalTrafficPolicy: Cluster
  ports:
  - nodePort: 32698
    port: 8080
    protocol: TCP
    targetPort: 8080
  selector:
    app-pod: webapp-pod-2
  sessionAffinity: None
  type: LoadBalancer
```

其中，`metadata.annotations.metallb.universe.tf/allow-shared-ip`均为192.168.5.9,`spec.externalTrafficPolicy`为`Cluster`，同时，myapp-svc使用80端口，webapp-svc-2使用8080端口

- 结果查看

![](https://pic1.zhimg.com/80/v2-be414f31e1345eb37e13aa8a39ad6910_720w.webp)

## 6. 结语

K8S生态很庞大，需要学习的东西很多！！！

# ExternalName

一、ExternalName类型Service简介
externalName Service是k8s中一个特殊的service类型，它不需要指定selector去选择哪些pods实例提供服务，而是使用DNS CNAME机制把自己CNAME到你指定的另外一个域名上，你可以提供集群内的名字，比如mysql.db.svc这样的建立在db命名空间内的mysql服务，也可以指定http://mysql.example.com这样的外部真实域名。

二、ExternalName类型Service实例
编辑external_name.yaml文件如下：

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dev

---

apiVersion: v1
kind: Service
metadata:
  name: search
  namespace: dev
spec:
  type: ExternalName
  externalName: www.baidu.com
```

```bash
# 使用如下命令创建资源
kubectl apply -f external_name.yaml
# 查看资源如下：
kubectl get service -n dev
# 此时，在集群内部的pod中就可以通过 search.dev.svc.cluster.local 访问www.baidu.com了
# 下面验证一下，首先登录一个pod查看 /etc/resolve.conf
kubectl exec -it pod/pc-deployment-5ffc5bf56c-9bg6w -n dev /bin/bash
cat /etc/resolv.conf
# 然后使用dig命令验证
dig @10.96.0.10 search.dev.svc.cluster.local
# 使用如下命令删除即可
kubectl delete -f external_name.yaml
```
