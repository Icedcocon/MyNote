# kubeedge



## 架构

<img src="image\image-20230620134418449.png" alt="image-20230620134418449" />



### 云上部分

- [CloudHub](https://kubeedge.io/en/docs/architecture/cloud/cloudhub): CloudHub 是一个 Web Socket 服务端，负责监听云端的变化，缓存并发送消息到 EdgeHub。
- [EdgeController](https://kubeedge.io/en/docs/architecture/cloud/edge_controller): EdgeController 是一个扩展的 Kubernetes 控制器，管理边缘节点和 Pods 的元数据确保数据能够传递到指定的边缘节点。
- [DeviceController](https://kubeedge.io/en/docs/architecture/cloud/device_controller): DeviceController 是一个扩展的 Kubernetes 控制器，管理边缘设备，确保设备信息、设备状态的云边同步。


### 边缘部分

- [EdgeHub](https://kubeedge.io/en/docs/architecture/edge/edgehub): EdgeHub 是一个 Web Socket 客户端，负责与边缘计算的云服务（例如 KubeEdge 架构图中的 Edge Controller）交互，包括同步云端资源更新、报告边缘主机和设备状态变化到云端等功能。
- [Edged](https://kubeedge.io/en/docs/architecture/edge/edged): Edged 是运行在边缘节点的代理，用于管理容器化的应用程序。
- [EventBus](https://kubeedge.io/en/docs/architecture/edge/eventbus): EventBus 是一个与 MQTT 服务器 (mosquitto) 交互的 MQTT 客户端，为其他组件提供订阅和发布功能。
- [ServiceBus](https://kubeedge.io/en/docs/architecture/edge/servicebus): ServiceBus 是一个运行在边缘的 HTTP 客户端，接受来自云上服务的请求，与运行在边缘端的 HTTP 服务器交互，提供了云上服务通过 HTTP 协议访问边缘端 HTTP 服务器的能力。
- [DeviceTwin](https://kubeedge.io/en/docs/architecture/edge/devicetwin): DeviceTwin 负责存储设备状态并将设备状态同步到云，它还为应用程序提供查询接口。
- [MetaManager](https://kubeedge.io/en/docs/architecture/edge/metamanager): MetaManager 是消息处理器，位于 Edged 和 Edgehub 之间，它负责向轻量级数据库 (SQLite) 存储/检索元数据。



## kube-edge安装及试用

### 云端（cloud）服务部署（keadm）

#### 存在kubernetes集群，kubernetes集群部署云端服务

```shell
[root@node1 ~]# kubectl get node -owide
NAME    STATUS   ROLES                       AGE   VERSION   INTERNAL-IP      EXTERNAL-IP   OS-IMAGE                KERNEL-VERSION           CONTAINER-RUNTIME
node1   Ready    control-plane,master,node   9d    v1.20.5   192.168.43.130   <none>        CentOS Linux 7 (Core)   3.10.0-1160.el7.x86_64   docker://20.10.7

```

#### 部署keadm，load相关镜像，官方镜像在dockerhub中

```shell
[root@localhost ~]# tar -zxvf keadm-v1.12.1-linux-amd64.tar.gz
keadm-v1.12.1-linux-amd64/
keadm-v1.12.1-linux-amd64/version
keadm-v1.12.1-linux-amd64/keadm/
keadm-v1.12.1-linux-amd64/keadm/keadm

[root@localhost ~]# cp keadm-v1.12.1-linux-amd64/keadm/keadm /usr/bin/

[root@localhost ~]# keadm version
version: version.Info{Major:"1", Minor:"12", GitVersion:"v1.12.1", GitCommit:"919ad5378eaca3cb0c666c22a19db01261cbc9a6", GitTreeState:"clean", BuildDate:"2022-11-02T08:22:56Z", GoVersion:"go1.17", Compiler:"gc", Platform:"linux/amd64"}

[root@localhost ~]# docker load -i kube-edge-images.tar.gz
```

#### 若是重复安装，需要清理iptables-manager的ClusterRole

```
kubectl delete ClusterRoleBinding iptables-manager
kubectl delete ClusterRole iptables-manager
```

#### 初始化kube-edge，cloud端

advertise-address：k8s集群master节点ip，可以是vip。需要特别注意，高版本cloudcore为容器运行，需要保证cloudcore所在节点的IP，包含在advertise-address中。如果cloudcore可以被调度在多个节点 ，advertise-address也许要配置多个IP，例：`--advertise-address="192.168.43.130,192.168.43.131"`

iptablesManage：是否启用iptablesmanager，启用后才可以使用后续kubectl exec/log等功能。

```
keadm init --advertise-address="192.168.43.130" --profile version=v1.12.1 --set iptablesManager.mode=external

#初始化成功后，cloud端启动iptables-manager和cloudcore服务
[root@node1 ~]# kubectl get ds -n kubeedge
NAME                     DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
cloud-iptables-manager   1         1         1       1            1           <none>          4m7s
[root@node1 ~]#
[root@node1 ~]# kubectl get deploy -n kubeedge
NAME        READY   UP-TO-DATE   AVAILABLE   AGE
cloudcore   1/1     1            1           4m19s


[root@node1 ~]# kubectl logs -n kubeedge cloudcore-5876c76687-6zs4s
W0624 09:28:28.479086       1 validation.go:154] TLSTunnelPrivateKeyFile does not exist in /etc/kubeedge/certs/server.key, will load from secret
W0624 09:28:28.479199       1 validation.go:157] TLSTunnelCertFile does not exist in /etc/kubeedge/certs/server.crt, will load from secret
W0624 09:28:28.479207       1 validation.go:160] TLSTunnelCAFile does not exist in /etc/kubeedge/ca/rootCA.crt, will load from secret
I0624 09:28:28.479228       1 server.go:92] Version: v1.12.1
W0624 09:28:28.479254       1 client_config.go:615] Neither --kubeconfig nor --master was specified.  Using the inClusterConfig.  This might not work.
I0624 09:28:28.563481       1 module.go:52] Module cloudhub registered successfully
I0624 09:28:28.579177       1 module.go:52] Module edgecontroller registered successfully
I0624 09:28:28.579438       1 module.go:52] Module devicecontroller registered successfully
W0624 09:28:28.579449       1 module.go:55] Module nodeupgradejobcontroller is disabled, do not register
I0624 09:28:28.579588       1 module.go:52] Module synccontroller registered successfully
I0624 09:28:28.579628       1 module.go:52] Module cloudStream registered successfully
W0624 09:28:28.579633       1 module.go:55] Module router is disabled, do not register
I0624 09:28:28.579655       1 eventhandler.go:66] [metaserver/HandlerCenter] prepare a new resourceEventHandler(/v1, Resource=nodes)
I0624 09:28:28.579934       1 eventhandler.go:101] [metaserver/resourceEventHandler] handler(/v1, Resource=nodes) init, prepare informer...
I0624 09:28:28.579966       1 eventhandler.go:115] [metaserver/resourceEventHandler] handler(/v1, Resource=nodes) init, wait for informer starting...
I0624 09:28:28.681595       1 eventhandler.go:122] [metaserver/resourceEventHandler] handler(/v1, Resource=nodes) init successfully, start to dispatch events to it's listeners
I0624 09:28:28.681663       1 eventhandler.go:66] [metaserver/HandlerCenter] prepare a new resourceEventHandler(/v1, Resource=services)
I0624 09:28:28.681675       1 eventhandler.go:101] [metaserver/resourceEventHandler] handler(/v1, Resource=services) init, prepare informer...
I0624 09:28:28.681707       1 eventhandler.go:115] [metaserver/resourceEventHandler] handler(/v1, Resource=services) init, wait for informer starting...
I0624 09:28:28.781859       1 eventhandler.go:122] [metaserver/resourceEventHandler] handler(/v1, Resource=services) init successfully, start to dispatch events to it's listeners
W0624 09:28:28.781924       1 module.go:55] Module dynamiccontroller is disabled, do not register
I0624 09:28:28.781985       1 core.go:46] starting module cloudStream
I0624 09:28:28.782037       1 core.go:46] starting module cloudhub
I0624 09:28:28.782061       1 core.go:46] starting module edgecontroller
I0624 09:28:28.782082       1 core.go:46] starting module devicecontroller
I0624 09:28:28.782105       1 core.go:46] starting module synccontroller
I0624 09:28:28.784050       1 upstream.go:140] start upstream controller
I0624 09:28:28.784275       1 downstream.go:334] start downstream controller
I0624 09:28:28.784309       1 downstream.go:959] Start downstream devicecontroller
I0624 09:28:28.884226       1 server.go:247] Ca and CaKey don't exist in local directory, and will read from the secret
I0624 09:28:28.886787       1 server.go:251] Ca and CaKey don't exist in the secret, and will be created by CloudCore
I0624 09:28:28.902021       1 server.go:285] CloudCoreCert and key don't exist in local directory, and will read from the secret
I0624 09:28:28.904196       1 server.go:290] CloudCoreCert and key don't exist in the secret, and will be signed by CA
I0624 09:28:28.909135       1 streamserver.go:320] Prepare to start stream server ...
I0624 09:28:28.910160       1 tunnelserver.go:157] Succeed in loading TunnelCA from CloudHub
I0624 09:28:28.910272       1 tunnelserver.go:170] Succeed in loading TunnelCert and Key from CloudHub
I0624 09:28:28.910364       1 tunnelserver.go:190] Prepare to start tunnel server ...
I0624 09:28:28.913088       1 signcerts.go:101] Succeed to creating token
I0624 09:28:28.913158       1 server.go:44] start unix domain socket server
I0624 09:28:28.913399       1 uds.go:71] listening on: //var/lib/kubeedge/kubeedge.sock
I0624 09:28:28.913838       1 server.go:63] Starting cloudhub websocket server
I0624 09:28:30.785463       1 upstream.go:64] Start upstream devicecontroller

[root@node1 cloud]# iptables -t nat -nvL TUNNEL-PORT
Chain TUNNEL-PORT (2 references)
 pkts bytes target     prot opt in     out     source               destination
    0     0 DNAT       tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:10351 to:192.168.43.130:10003
    

[root@node1 cloud]# ss -nltp |grep 1000
LISTEN     0      128       [::]:10000                 [::]:*                   users:(("cloudcore",pid=25243,fd=11))
LISTEN     0      128       [::]:10002                 [::]:*                   users:(("cloudcore",pid=25243,fd=10))
LISTEN     0      128       [::]:10003                 [::]:*                   users:(("cloudcore",pid=25243,fd=7))
LISTEN     0      128       [::]:10004                 [::]:*                   users:(("cloudcore",pid=25243,fd=8))
```

#### 获取秘钥

```shell
[root@node1 ~]# keadm gettoken
7d7d19c25e82dab8af4c7de1c6ba92fa496f942c1d58e5769ddae2f6ba5b4b8e.eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODc2NTY1MDh9.tZXYOoHMzZiDRjhmBVMdZJF6O8LHPFiKe_745oE3l3k
```



### 云端（cloud）服务部署（高可用）

####  集成cloudcore相关yaml

```
01-ha-prepare.yaml
修改"resources: ["nodes",pods/status"]" 为"resources: ["nodes","nodes/status","pods/status"]"
不修改后续会报错权限错误，已知bug。

02-ha-configmap.yaml
以下修改为环境的VIP
modules:
 cloudHub:
  advertiseAddress:
   - 192.168.43.150
         
03-ha-deployment.yaml
增加secret挂载，修改volumes,volumeMounts
volumeMounts:
- name: certs
  mountPath: /etc/kubeedgee
 
volumes:
- name: certs
  secret:
    items:
    - key: stream.crt
      path: certs/stream.crt
    - key: stream.key
      path: certs/stream.key
    - key: streamCA.crt
      path: ca/streamCA.crt
    secretName: cloudcore
              
04-iptablesmanager-ds.yaml

```

#### 启动cloudcore

```
#CLOUDCOREIPS中指定master_ip,vip,待扩容的edge节点ip
export CLOUDCOREIPS="192.168.43.150,IP.3:192.168.43.130,IP.4:192.168.43.131,IP.5:192.168.43.132,IP.6:192.168.43.133"

#根据脚本重新生成秘钥
mkdir -p /etc/kubeedge/
bash certgen.sh stream

#生成secret
kubectl create secret generic cloudcore --from-file=/etc/kubeedge/certs/stream.crt --from-file=/etc/kubeedge/certs/stream.key --from-file=/etc/kubeedge/ca/streamCA.crt -n kubeedge

#启动resources
kubectl apply -f cloudcore/

#获取token
kubectl get secret -n kubeedge tokensecret -o=jsonpath='{.data.tokendata}' | base64 -d && echo
```



### 边缘（edge）节点加入

边缘节点加入前，先做好主机初始化，安装docker。

#### calico，kube-proxy新增节点亲和性

防止calico，kube-proxy部署到edge节点中。

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
        - matchExpressions:
          - key: node-role.kubernetes.io/edge
            operator: DoesNotExist
```

#### 安装keadm

```
[root@localhost ~]# tar -zxvf keadm-v1.12.1-linux-amd64.tar.gz
keadm-v1.12.1-linux-amd64/
keadm-v1.12.1-linux-amd64/version
keadm-v1.12.1-linux-amd64/keadm/
keadm-v1.12.1-linux-amd64/keadm/keadm

[root@localhost ~]# cp keadm-v1.12.1-linux-amd64/keadm/keadm /usr/bin/

[root@localhost ~]# keadm version
version: version.Info{Major:"1", Minor:"12", GitVersion:"v1.12.1", GitCommit:"919ad5378eaca3cb0c666c22a19db01261cbc9a6", GitTreeState:"clean", BuildDate:"2022-11-02T08:22:56Z", GoVersion:"go1.17", Compiler:"gc", Platform:"linux/amd64"}

[root@localhost ~]# docker load -i kube-edge-images.tar.gz
```

#### 重复安装时清理配置和容器

```shell
rm -rf /etc/kubeedge/
docker rm -f mqtt
```

#### 加入集群

token：为主节点keadm gettoken获取的内容

cloudcore-ipport：部署云端服务时指定的advertise-address，端口默认10000；

runtimetype：修改为docker，默认为containerd

cgroupdriver：修改为systemd

edgenode-name：节点名称

```shell
[root@localhost ~]# keadm join --cloudcore-ipport=192.168.43.130:10000 --runtimetype=docker --cgroupdriver=systemd --edgenode-name=edgenode1 --kubeedge-version=v1.12.1 --token=7d7d19c25e82dab8af4c7de1c6ba92fa496f942c1d58e5769ddae2f6ba5b4b8e.eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODc2NTY1MDh9.tZXYOoHMzZiDRjhmBVMdZJF6O8LHPFiKe_745oE3l3k
I0624 09:38:34.628087    2180 command.go:845] 1. Check KubeEdge edgecore process status
I0624 09:38:34.842070    2180 command.go:845] 2. Check if the management directory is clean
I0624 09:38:34.842143    2180 join.go:100] 3. Create the necessary directories
I0624 09:38:34.843138    2180 join.go:176] 4. Pull Images
Pulling kubeedge/installation-package:v1.12.1 ...
Pulling eclipse-mosquitto:1.6.15 ...
Successfully pulled eclipse-mosquitto:1.6.15
Pulling kubeedge/pause:3.1 ...
Successfully pulled kubeedge/pause:3.1
I0624 09:38:54.952640    2180 join.go:176] 5. Copy resources from the image to the management directory
I0624 09:38:56.415038    2180 join.go:176] 6. Start the default mqtt service
I0624 09:38:56.850648    2180 join.go:100] 7. Generate systemd service file
I0624 09:38:56.850727    2180 join.go:100] 8. Generate EdgeCore default configuration
I0624 09:38:56.850744    2180 join.go:230] The configuration does not exist or the parsing fails, and the default configuration is generated
W0624 09:38:56.851845    2180 validation.go:71] NodeIP is empty , use default ip which can connect to cloud.
I0624 09:38:56.853742    2180 join.go:100] 9. Run EdgeCore daemon
I0624 09:38:57.159660    2180 join.go:317]
I0624 09:38:57.159676    2180 join.go:318] KubeEdge edgecore is running, For logs visit: journalctl -u edgecore.service -xe
```

#### 检查edgecore日志

```
systemctl status edgecore
journalctl -u edgecore.service -xe
```

#### 云端master节点检查是否添加成功

```shell
[root@node1 cloud]# kubectl get node
NAME        STATUS   ROLES                       AGE   VERSION
edgenode1   Ready    agent,edge                  16m   v1.22.6-kubeedge-v1.12.1
node1       Ready    control-plane,master,node   9d    v1.20.5
```

#### 部署测试容器

```
[root@node1 cloud]# kubectl apply -f nginx-deploy.yaml

[root@node1 cloud]# kubectl get po -owide
NAME                                READY   STATUS    RESTARTS   AGE   IP             NODE        NOMINATED NODE   READINESS GATES
nginx-deployment-77f96fbb65-h954f   1/1     Running   0          24m   172.22.154.7   node1       <none>           <none>
nginx-deployment-77f96fbb65-rqp58   1/1     Running   0          24m   172.17.0.3     edgenode1   <none>           <none>
```



### 开启kubectl logs/exec功能

#### 开启cloudStream和edgeStream，并重启cloudcore，edgecore

cloudstream 在1.12版本后为cm，修改cloudStream:\n    enable: true\n

```
[root@node1 cloud]# kubectl get cm cloudcore -n kubeedge -oyaml
apiVersion: v1
data:
  cloudcore.yaml: "apiVersion: cloudcore.config.kubeedge.io/v1alpha2\nkind: CloudCore\nkubeAPIConfig:\n
    \ kubeConfig: \"\"\n  master: \"\"\nmodules:\n  cloudHub:\n    advertiseAddress:\n
    \   - 192.168.43.130\n    dnsNames:\n    - \n    nodeLimit: 1000\n    tlsCAFile:
    /etc/kubeedge/ca/rootCA.crt\n    tlsCertFile: /etc/kubeedge/certs/edge.crt\n    tlsPrivateKeyFile:
    /etc/kubeedge/certs/edge.key\n    unixsocket:\n      address: unix:///var/lib/kubeedge/kubeedge.sock\n
    \     enable: true\n    websocket:\n      address: 0.0.0.0\n      enable: true\n
    \     port: 10000\n    quic:\n      address: 0.0.0.0\n      enable: false\n      maxIncomingStreams:
    10000\n      port: 10001\n    https:\n      address: 0.0.0.0\n      enable: true\n
    \     port: 10002\n  cloudStream:\n    enable: true\n    streamPort: 10003\n    tunnelPort:
    10004\n  dynamicController:\n    enable: false\n  router:\n    enable: false\n
    \ iptablesManager:\n    enable: true\n    mode: external\n"
...

[root@node1 cloud]# kubectl delete po -n kubeedge cloudcore-5876c76687-6zs4s

```

```
[root@localhost ~]# vi /etc/kubeedge/config/edgecore.yaml
  edgeStream:
    enable: true
    handshakeTimeout: 30
    readDeadline: 15
    server: 192.168.43.130:10004
    tlsTunnelCAFile: /etc/kubeedge/ca/rootCA.crt
    tlsTunnelCertFile: /etc/kubeedge/certs/server.crt
    tlsTunnelPrivateKeyFile: /etc/kubeedge/certs/server.key
    writeDeadline: 15
[root@localhost ~]# systemctl restart edgecore
```

#### 新扩容edge节点时，更新证书，云端master节点执行

certgen.sh脚本为官方提供的秘钥生成工具

```
#CLOUDCOREIPS中新增扩容节点IP，IP.3为固定格式，多个节点，IP.4 IP.5 顺延
[root@node1 cloud]# export CLOUDCOREIPS="192.168.43.130,IP.3:192.168.43.131"

#根据脚本重新生成秘钥
[root@node1 cloud]# bash certgen.sh stream

[root@node1 cloud]# ls /etc/kubeedge/certs/
stream.crt  stream.csr  stream.key

#重新生成secret
[root@node1 cloud]# kubectl delete secret cloudcore -n kubeedge
secret "cloudcore" deleted
[root@node1 cloud]# kubectl create secret generic cloudcore --from-file=/etc/kubeedge/certs/stream.crt --from-file=/etc/kubeedge/certs/stream.key --from-file=/etc/kubeedge/ca/streamCA.crt -n kubeedge
secret/cloudcore created

#重启cloudcore
[root@node1 cloud]# kubectl delete po -n kubeedge      cloudcore-5876c76687-6zs4s
```

#### 检查logs功能

```
[root@node1 cloud]# kubectl get po -owide
NAME                                READY   STATUS    RESTARTS   AGE   IP             NODE        NOMINATED NODE   READINESS GATES
nginx-deployment-77f96fbb65-h954f   1/1     Running   0          23m   172.22.154.7   node1       <none>           <none>
nginx-deployment-77f96fbb65-rqp58   1/1     Running   0          23m   172.17.0.3     edgenode1   <none>           <none>
[root@node1 cloud]#
[root@node1 cloud]# kubectl logs nginx-deployment-77f96fbb65-rqp58
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2023/06/24 01:54:57 [notice] 1#1: using the "epoll" event method
2023/06/24 01:54:57 [notice] 1#1: nginx/1.25.1
2023/06/24 01:54:57 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14)
2023/06/24 01:54:57 [notice] 1#1: OS: Linux 3.10.0-1160.el7.x86_64
2023/06/24 01:54:57 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2023/06/24 01:54:57 [notice] 1#1: start worker processes
2023/06/24 01:54:57 [notice] 1#1: start worker process 29
2023/06/24 01:54:57 [notice] 1#1: start worker process 30
```



### EdgeMesh

#### nginx测试容器启动后，无法通过service访问到edge节点的pod

```
[root@node1 cloud]# curl 172.19.107.160:8080
curl: (7) Failed connect to 172.19.107.160:8080; No route to host

```

#### 部署EdgeMesh

##### 在云端，开启 dynamicController 模块

```
[root@node1 cloud]# kubectl edit cm cloudcore -n kubeedge
modules:
  ...
  dynamicController:
    enable: true
```

##### 在边缘节点，打开 metaServer 模块，配置clusterDNS，clusterDomain

clusterDNS 设置的值 '169.254.96.16' 来自于commonConfig中 bridgeDeviceIP 的默认值

```shell
vi /etc/kubeedge/config/edgecore.yaml
modules:
  ...
  edgeMesh:
    enable: true
  ...
  metaManager:
    metaServer:
      enable: true


modules:
  ...
  edged:
    ...
    tailoredKubeletConfig:
      ...
      clusterDNS:
      - 169.254.96.16
      clusterDomain: cluster.local
```

##### 测试边缘节点api

```
curl 127.0.0.1:10550/api/v1/services
```

##### 给 Kubernetes API 服务添加过滤标签

不需要edgemesh代理的service，可以通过打标签处理

```
[root@node1 cloud]# kubectl label services kubernetes service.edgemesh.kubeedge.io/service-proxy-name=""

[root@node1 cloud]# kubectl get svc kubernetes -oyaml
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: "2023-06-14T05:54:49Z"
  labels:
    component: apiserver
    provider: kubernetes
    service.edgemesh.kubeedge.io/service-proxy-name: ""
...
```

##### 修改relayNodes

```
#生成psk
[root@node1 ~]# openssl rand -base64 32
91xZzGV90uUY2DR81H+Pur8QY5jf+uUoudrAuF5gULU=

#修改cm
[root@node1 ~]# vi build/agent/resources/04-configmap.yaml

apiVersion: v1
kind: ConfigMap
metadata:
  name: edgemesh-agent-cfg
  namespace: kubeedge
  labels:
    k8s-app: kubeedge
    kubeedge: edgemesh-agent
data:
  edgemesh-agent.yaml: |
    # For more detailed configuration, please refer to: https://edgemesh.netlify.app/reference/config-items.html#edgemesh-agent-cfg
    modules:
      edgeProxy:
        enable: true
      edgeTunnel:
        enable: true
        relayNodes:
        - nodeName: node1
          advertiseAddress:
          - 192.168.43.130
        - nodeName: edgenode1
          advertiseAddress:
          - 192.168.43.131
        - nodeName: edgenode2
          advertiseAddress:
          - 192.168.43.132

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: edgemesh-agent-psk
  namespace: kubeedge
  labels:
    k8s-app: kubeedge
    kubeedge: edgemesh-agent
data:
  # Generated by `openssl rand -base64 32`
  # NOTE: Don't use this psk, please regenerate it!!! Please refer to: https://edgemesh.netlify.app/guide/security.html
  psk: 91xZzGV90uUY2DR81H+Pur8QY5jf+uUoudrAuF5gULU=

```

##### 启动部署 edgemesh-agent

```
# 安装 CRDs
[root@node1 ~]# kubectl apply -f build/crds/istio/
customresourcedefinition.apiextensions.k8s.io/destinationrules.networking.istio.io created
customresourcedefinition.apiextensions.k8s.io/gateways.networking.istio.io created
customresourcedefinition.apiextensions.k8s.io/virtualservices.networking.istio.io created

# 部署 edgemesh-agent
[root@node1 ~]# kubectl apply -f build/agent/resources/
serviceaccount/edgemesh-agent created
clusterrole.rbac.authorization.k8s.io/edgemesh-agent created
clusterrolebinding.rbac.authorization.k8s.io/edgemesh-agent created
configmap/edgemesh-agent-cfg created
configmap/edgemesh-agent-psk created
daemonset.apps/edgemesh-agent created

# 检查部署情况
[root@node1 ~]# kubectl get po -n kubeedge -owide
NAME                           READY   STATUS    RESTARTS   AGE    IP               NODE        NOMINATED NODE   READINESS GATES
cloud-iptables-manager-dwbvr   1/1     Running   0          121m   192.168.43.130   node1       <none>           <none>
cloudcore-5876c76687-ndgvv     1/1     Running   0          17m    192.168.43.130   node1       <none>           <none>
edgemesh-agent-45lpn           1/1     Running   0          101s   192.168.43.132   edgenode2   <none>           <none>
edgemesh-agent-f5bbd           1/1     Running   0          101s   192.168.43.131   edgenode1   <none>           <none>
edgemesh-agent-jxwm2           1/1     Running   0          101s   192.168.43.130   node1       <none>           <none>

```

##### cloud节点，edge节点分别测试

```
[root@node1 ~]# kubectl get svc
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
kubernetes   ClusterIP   172.19.0.1       <none>        443/TCP    9d
nginx-svc    ClusterIP   172.19.107.160   <none>        8080/TCP   62m

[root@node1 ~]# kubectl get ep
NAME         ENDPOINTS                                     AGE
kubernetes   192.168.43.130:6443                           9d
nginx-svc    172.17.0.3:80,172.17.0.3:80,172.22.154.8:80   63m

[root@node1 ~]# curl 172.19.107.160:8080
```



```
[root@node1 ~]# ip a |grep edgemesh0
58: edgemesh0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default
    inet 169.254.96.16/32 scope global edgemesh0

[root@node1 ~]# iptables -t nat -nvL KUBE-PORTALS-CONTAINER
Chain KUBE-PORTALS-CONTAINER (1 references)
 pkts bytes target     prot opt in     out     source               destination
    0     0 DNAT       tcp  --  *      *       0.0.0.0/0            172.19.192.248       /* kube-system/calico-typha:calico-typha */ tcp dpt:5473 to:169.254.96.16:50001
    0     0 DNAT       udp  --  *      *       0.0.0.0/0            172.19.0.3           /* kube-system/coredns:dns */ udp dpt:53 to:169.254.96.16:55951
    0     0 DNAT       tcp  --  *      *       0.0.0.0/0            172.19.0.3           /* kube-system/coredns:dns-tcp */ tcp dpt:53 to:169.254.96.16:52977
    0     0 DNAT       tcp  --  *      *       0.0.0.0/0            172.19.0.3           /* kube-system/coredns:metrics */ tcp dpt:9153 to:169.254.96.16:57998
    0     0 DNAT       tcp  --  *      *       0.0.0.0/0            172.19.165.19        /* kubeedge/cloudcore:cloudhub */ tcp dpt:10000 to:169.254.96.16:50002
    0     0 DNAT       tcp  --  *      *       0.0.0.0/0            172.19.165.19        /* kubeedge/cloudcore:cloudhub-quic */ tcp dpt:10001 to:169.254.96.16:50003
    0     0 DNAT       tcp  --  *      *       0.0.0.0/0            172.19.165.19        /* kubeedge/cloudcore:cloudhub-https */ tcp dpt:10002 to:169.254.96.16:51720
    0     0 DNAT       tcp  --  *      *       0.0.0.0/0            172.19.165.19        /* kubeedge/cloudcore:cloudstream */ tcp dpt:10003 to:169.254.96.16:60156
    0     0 DNAT       tcp  --  *      *       0.0.0.0/0            172.19.165.19        /* kubeedge/cloudcore:tunnelport */ tcp dpt:10004 to:169.254.96.16:50004
    0     0 DNAT       tcp  --  *      *       0.0.0.0/0            172.19.174.182       /* kube-system/metrics-server:https */ tcp dpt:443 to:169.254.96.16:56031
    0     0 DNAT       tcp  --  *      *       0.0.0.0/0            172.19.107.160       /* default/nginx-svc:http-0 */ tcp dpt:8080 to:169.254.96.16:54222


```



## 网络连通

同一个VLAN中通过mDNS发现，不同VLAN通过中继节点发现。

![image-20230624181635451](image\image-20230624181635451.png)



![image-20230624181953054](image\image-20230624181953054.png)



`Cloud`为云端，`kubernetes`集群，其中kube-master1存在外网IP，做为整个集群的中继节点

Edge1集群和Edge2集群网络不通，但都可以连接kube-master1外网IP

Edge1集群的node1、node2在一个VLAN，通过mDNS发现

Edge1集群-->Edge集群2、Edge1、Edge2集群-->Cloud 端通过中继节点kube-master1进行通信，中继节点在`relayNodes`配置

<img src="image\image-20230624184530763.png" alt="image-20230624184530763" style="zoom:67%;" />



## 其他问题

### 单机环境master重启

部署在`edge`节点的实际容器个数，与`kubectl get po` 个数不一致，长时间不恢复。

`edgemesh`与`cloudcore`端口冲突，必须先启动`cloudcore`，再启动`edgemesh`

kube-proxy必须在edgemesh之前启动，否则edgemesh无法截流。

master宕机不影响访问edgemesh代理的clusterIP

### 扩容edge节点

执行`keadm join `添加边缘节点机器，相关`stream`证书没有更新，影响`kubectl logs/exec`，需要手动生成证书，生成`secret`，重启`cloudcore`。

### mDNS，同一个边缘网络里应用的互访

a. mDNS协议本身是基于UDP协议的，需要确保网络放通了UDP数据包的传输

b. 由于mDNS是多播(组播)协议，因此要求节点在同一个网段里面；节点也必须得在同一个VLAN里面，不同VLAN之间是隔离广播域的

c. edgemesh-agent的tunnel模块监听在20006，确保安全组/防火墙对20006端口放开

d. 所有节点应该具备内网IP（10.0.0.0/8、172.16.0.0/12、192.168.0.0/16），否则mDNS的数据包会被丢弃，导致不能互相发现

