# NAT 类型测试

## 一、快速开始

- 安装

```bash
apt install stun-client
```

- 测试

```bash
root@beijing-ubuntu:~# stun stun.sipgate.net 0
STUN client version 0.97
running test number 0
Primary: Independent Mapping, Independent Filter, random port, will hairpin
Return value is 0x000002


```

- 结果分析

```bash
Independent Mapping, Independent Filter = 完全锥型NAT 
Independent Mapping, Address Dependent Filter = 限制锥型NAT 
Independent Mapping, Port Dependent Filter = 端口限制锥型NAT 
Dependent Mapping = 对称型
```

- 地址

```bash
stun.stunprotocol.org
stun.sipgate.net
```
