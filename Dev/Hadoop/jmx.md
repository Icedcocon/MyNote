### 1. JMX监控和预警

##### 1.1 Hadoop集群监控的方式

Hadoop集群监控的方式很多，比如Restful API，具体Hadoop组件内置的API、JMX等

##### 1.2 JMX监控

Hadoop的JMX提供了Metrics信息如

- Cluster

- NameNode

- JVM

- FSQueue

### 2. 从JMX获取信息

##### 2.1 从JMX获取信息方式

- 获取NameNode相关的JMX
  
  - `${ip}`为HDFS集群中active NameNode所在节点IP地址

- 获取Yarn相关的的JMX
  
  - `${ip}`为HDFS集群中active ResourceManager节点所在节点地址（端口8088?）

```bash
curl http://${ip}:50070/jmx
```

- JMX相关信息的接口是在类`org.apache.hadoop.jmx.JMXJsonServlet`中实现的，返回的信息是json结构

##### 2.2 JMXJsonServlet支持的参数

- qry    过滤内容
  
  - 直接调用/jmx会返回多个service, name字典，qry可仅返回一个字典内容
  
  - `http://127.0.0.1:50070/jmx?qry=Hadoop:service=NameNodeStatus, name=NameNodeInfo`

```json
{
    "beans": [
        {
            "name": "Hadoop:service=NameNode,name=NameNodeStatus",
            "modelerType": "org.apache.hadoop.hdfs.server.namenode.NameNode",
            "NNRole": "NameNode",
            "HostAndPort": "ais-master1:8020",
            "SecurityEnabled": false,
            "LastHATransitionTime": 1675395854899,
            "BytesWithFutureGenerationStamps": 0,
            "SlowPeersReport": null,
            "SlowDisksReport": null,
            "State": "active"
        }
    ]
}
```

- callback 用于需要JSONP的请求，解决跨域问题

- get    获取某个属性
  
  - 相比于qry，get可以返回字典中的某各个属性，但依然有“name”等字段
  
  - `http://172.16.0.112:50070/jmx?get=Hadoop:service=NameNode, name=NameNodeInfo::LiveNodes`

```json
{
    "beans": [
        {
            "name": "Hadoop:service=NameNode,name=NameNodeInfo",
            "modelerType": "org.apache.hadoop.hdfs.server.namenode.FSNamesystem",
            "LiveNodes": "{\"ais-master3:9866\":{\"infoAddr\":\"172.16.0.114:9864\",\"infoSecureAddr\":\"172.16.0.114:0\",\"xferaddr\":\"172.16.0.114:9866\",\"lastContact\":2,\"usedSpace\":236105728,\"adminState\":\"In Service\",\"nonDfsUsedSpace\":57759977472,\"capacity\":7641759744000,\"numBlocks\":42,\"version\":\"3.2.2\",\"used\":236105728,\"remaining\":7583763660800,\"blockScheduled\":0,\"blockPoolUsed\":236105728,\"blockPoolUsedPercent\":0.0030896775,\"volfails\":0,\"lastBlockReport\":83},\"ais-master1:9866\":{\"infoAddr\":\"172.16.0.112:9864\",\"infoSecureAddr\":\"172.16.0.112:0\",\"xferaddr\":\"172.16.0.112:9866\",\"lastContact\":0,\"usedSpace\":236105728,\"adminState\":\"In Service\",\"nonDfsUsedSpace\":153601298432,\"capacity\":7641759744000,\"numBlocks\":42,\"version\":\"3.2.2\",\"used\":236105728,\"remaining\":7487922339840,\"blockScheduled\":0,\"blockPoolUsed\":236105728,\"blockPoolUsedPercent\":0.0030896775,\"volfails\":0,\"lastBlockReport\":170},\"ais-master2:9866\":{\"infoAddr\":\"172.16.0.113:9864\",\"infoSecureAddr\":\"172.16.0.113:0\",\"xferaddr\":\"172.16.0.113:9866\",\"lastContact\":0,\"usedSpace\":236105728,\"adminState\":\"In Service\",\"nonDfsUsedSpace\":55951761408,\"capacity\":7641759744000,\"numBlocks\":42,\"version\":\"3.2.2\",\"used\":236105728,\"remaining\":7585571876864,\"blockScheduled\":0,\"blockPoolUsed\":236105728,\"blockPoolUsedPercent\":0.0030896775,\"volfails\":0,\"lastBlockReport\":130}}"
        }
    ]
}
```


