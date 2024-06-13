# iptables快速开始

## 一、iptables介绍

### 1. 介绍

Linux系统中,**防火墙(Firewall)**,**网址转换(NAT)**,**数据包(package)记录**,**流量统计**,这些功能是由Netfilter子系统所提供的，而iptables是控制Netfilter的工具。iptables将许多复杂的规则组织成成容易控制的方式，以便管理员可以进行分组测试，或关闭、启动某组规则。

netfilter 组件位于内核空间，是内核的一部分； iptables 组件是一种工具，位于用户空间。

iptable能够为Unix、Linux和BSD个人工作站创建一个防火墙，也可以为一个子网创建防火墙以保护其它的系统平台。iptable只读取数据包头，不会给信息流增加负担，也无需进行验证。

### 2. iptables的结构

```
iptables -> Tables -> Chains -> Rules
```

简单地讲，tables由chains组成，而chains又由rules组成。iptables 默认有四个表Filter, NAT, Mangle, Raw，其对于的链如下图。

### 3. 五个链(chain)

```bash
       +------------+    +---------+    +--------+
IN  -> | PREROUTING | -> | ROUTING | -> | INPUT  |
       +------+-----+    +---+-----+    +---+----+
                             |              |
                             v              v
                         +---------+  +---------------+   
                         | FORWARD |  | Local Process |
                         +--+------+  +---------------+
                             |              |      
                             v              v      
       +------------+    +---------+    +--------+
OUT <- |POSTROUTING | <- | ROUTING | <- | OUTPUT |
       +------+-----+    +---+-----+    +---+----+
```

- **PREROUTING**: 来自网络接口(网卡)的数据包首先会经过 PREROUTING 链，经过 raw, mangle, nat 表中规则的处理然后进行路由判断。
  - 若数据包的目的地址为本机则会进入INPUT链
  - 若数据包的目的地址为其它地址则进入FORWARD链进行转发
- **INPUT**: 处理目标为本机的数据包, 经过 mangle,filter 表中规则的处理然后发给 nginx、mysql等上层进程处理 (此处存疑: nat 表中似乎也包括INPUT链, 望大佬指正)
- **FORWARD**: 处理转发的数据包，经过 mangle, filter 表中规则处理后进入POSTROUTING链
- **OUTPUT**: 处理本地进程发出的数据包, 经过 raw, mangle, nat, filter 表中规则的处理然后进入POSTROUTING链
- **POSTROUTING**: 处理来自 FORWARD 和 OUTPUT 链的数据包并发送给网络接口发出，可在 raw, mangle, nat 表中配置规则

在运行中 iptables 可能处理三种场景:

- 入站数据流: 网络接口 -> PREROUTING -> INPUT -> 本地
- 转发数据流: 网络接口 -> PREROUTING -> FORWARD -> POSTROUTING -> 网络接口
- 出站数据流: 本地 -> OUTPUT -> POSTROUTING -> 网络接口

>  注意: 链是每个数据包流需要经过的不同环节，你可以在不同的环节根据需要设置不同的过滤策略,每个链的默认策略都是Accept。

### 4. 四个表(table)

iptables 中有四张表, 优先级从高到低是：

- **raw**: 只使用在PREROUTING链和OUTPUT链上,因为优先级最高，从而可以对收到的数据包在连接跟踪前进行处理。一但用户使用了RAW表,在 某个链上,RAW表处理完后,将跳过NAT表和 ip_conntrack处理,即不再做地址转换和数据包的链接跟踪处理了。
- **mangle**: 主要用于对指定数据包进行更改，在内核版本2.4.18 后的linux版本中该表包含的链为：INPUT链（处理进入的数据包），RORWARD链（处理转发的数据包），OUTPUT链（处理本地生成的数据包）POSTROUTING链（修改即将出去的数据包），PREROUTING链（修改即将到来的数据包）。
- **nat**: 主要用于网络地址转换NAT，该表可以实现一对一，一对多，多对多等NAT 工作，iptables就是使用该表实现共享上网的，NAT表包含了PREROUTING链（修改即将到来的数据包），POSTROUTING链（修改即将出去的数据包），OUTPUT链（修改路由之前本地生成的数据包）。
- **filter**: 主要用于过滤数据包，该表根据系统管理员预定义的一组规则过滤符合条件的数据包。对于防火墙而言，主要利用在filter表中指定的规则来实现对数据包的过滤。Filter表是默认的表，如果没有指定哪个表，iptables 就默认使用filter表来执行所有命令，filter表包含了INPUT链（处理进入的数据包），RORWARD链（处理转发的数据包），OUTPUT链（处理本地生成的数据包）在filter表中只能允许对数据包进行接受，丢弃的操作，而无法对数据包进行更改。

mangle表可以用来匹配并改变包的一些属性，比如 TOS（TYPE OF SERVICE),TTL (TIME TO LIVE),MARK(后续流量控制TC等)。

nat表仅用于NAT(DNAT,SNAT,MASQUERADE)，也就是转换包的源或目标地址。只有流的第一个包会被这个链匹配，其后的包会自动被做相同的处理。

filter表用来过滤数据包，我们可以在任何时候匹配包并过滤它们。 我们就是在这里根据包的内容对包做DROP或ACCEPT的。

Raw表优先级最高，设置raw时一般是为了不再让iptables做数据包的链接跟踪处理，提高性能。

>  注意：
> 
> 1. iptalbe中，要用 -t 参数指定要操作哪个表，如果没有 -t 参数，就默认对filter表操作。
> 
> 2. 表是规则的集合，每个表中的规则条目是按顺序匹配的，表的处理优先级：raw > mangle > nat > filter

### 5. 完整流程图

![packet_flow.png](https://img.linux.net.cn/data/attachment/album/201307/04/082455th9x65f9aqejz6ea.png)

## 二、iptables 命令

### 1. 命令格式

说明

- **-t 表**

表选项用于指定命令应用于哪个iptables内置表。

- **命令**

命令选项用于指定iptables的执行方式，包括插入规则，删除规则和添加规则，如下表所示

| 命令                       | 说明                      |
| ------------------------ | ----------------------- |
| -P  --policy        <链名> | 定义默认策略                  |
| -L  --list          <链名> | 查看iptables规则列表          |
| -A  --append        <链名> | 在规则列表的最后增加1条规则          |
| -I  --insert        <链名> | 在指定的位置插入1条规则，-I 等于 -I 0 |
| -D  --delete        <链名> | 从规则列表中删除1条规则            |
| -R  --replace       <链名> | 替换规则列表中的某条规则            |
| -F  --flush         <链名> | 删除表中所有规则                |
| -Z  --zero          <链名> | 将表中数据包计数器和流量计数器归零       |
| -X  --delete-chain  <链名> | 删除自定义链                  |
| -v  --verbose       <链名> | 与-L他命令一起使用显示更多更详细的信息    |

- **匹配规则**

| 匹配                            | 说明                                 |
| ----------------------------- | ---------------------------------- |
| -i --in-interface    <网络接口名>  | 指定数据包从哪个网络接口进入                     |
| -o --out-interface   <网络接口名>  | 指定数据包从哪个网络接口输出                     |
| -p --proto          <协议类型>    | 指定数据包匹配的协议,如TCP、UDP和ICMP等          |
| -s --source          <源地址或子网> | 指定数据包匹配的源地址，如192.168.10.0/24       |
| --sport           <源端口号>      | 指定数据包匹配的源端口号，如21000                |
| --dport           <目的端口号>     | 指定数据包匹配的目的端口号                      |
| -m --match           <匹配的模块>  | 指定数据包规则所使用的过滤模块                    |
| -j --jump           <目标>      | 指定对匹配数据包采取的行为,如ACCEPT、DROP、REJECT等 |
| --state                       | 匹配数据包的连接状态,如NEW、ESTABLISHED等       |
| -m multiport --dports  <端口范围> | 匹配多个目的端口，如21000-31000              |
| -m multiport --sports  <端口范围> | 匹配多个源端口，如21000-31000               |
| --icmp-type          <类型代码>   | 匹配ICMP消息类型                         |

匹配选项指定数据包与规则匹配所具有的特征，包括源地址，目的地址，传输协议和端口号，如下表所示

iptables执行规则时，是从规则表中从上至下顺序执行的，如果没遇到匹配的规则，就一条一条往下执行，如果遇到匹配的规则后，那么就执行本规则，执行后根据本规则的动作(accept，reject，log，drop等)，决定下一步执行的情况，后续执行一般有三种情况。

- 一种是继续执行当前规则队列内的下一条规则。比如执行过Filter队列内的LOG后，还会执行Filter队列内的下一条规则。
- 一种是中止当前规则队列的执行，转到下一条规则队列。比如从执行过accept后就中断Filter队列内其它规则，跳到nat队列规则去执行
- 一种是中止所有规则队列的执行。

### 2. iptables规则的动作

 iptables处理动作除了 ACCEPT、REJECT、DROP、REDIRECT 、MASQUERADE 以外，还多出 LOG、ULOG、DNAT、RETURN、TOS、SNAT、MIRROR、QUEUE、TTL、MARK等。

- **REJECT**    拦阻该数据包，并返回数据包通知对方，可以返回的数据包有几个选择：ICMP port-unreachable、ICMP echo-reply 或是tcp-reset（这个数据包包会要求对方关闭联机），进行完此处理动作后，将不再比对其它规则，直接中断过滤程序。 范例如下：

```bash
iptables -A  INPUT -p TCP --dport 22 -j REJECT --reject-with ICMP echo-reply
```

- **DROP**  丢弃数据包不予处理，进行完此处理动作后，将**不再比对其它规则**，直接中断过滤程序。

- **REDIRECT**   将封包重新导向到另一个端口（PNAT），进行完此处理动作后，将会继续比对其它规则。这个功能可以用来实作透明代理 或用来保护web 服务器。例如：

```bash
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT--to-ports 8081
```

- **MASQUERADE** 改写封包来源IP为防火墙的IP，可以指定port 对应的范围，进行完此处理动作后，直接跳往下一个规则链（mangle:postrouting）。这个功能与 SNAT 略有不同，当进行IP 伪装时，不需指定要伪装成哪个 IP，IP 会从网卡直接读取，当使用拨接连线时，IP 通常是由 ISP 公司的 DHCP服务器指派的，这个时候 MASQUERADE 特别有用。范例如下：

```bash
iptables -t nat -A POSTROUTING -p TCP -j MASQUERADE --to-ports 21000-31000
```

**LOG**   将数据包相关信息纪录在 /var/log 中，详细位置请查阅 /etc/syslog.conf 配置文件，进行完此处理动作后，将会继续比对其它规则。例如：

```bash
iptables -A INPUT -p tcp -j LOG --log-prefix "input packet"
```

**SNAT** 改写封包来源 IP 为某特定 IP 或 IP 范围，可以指定 port 对应的范围，进行完此处理动作后，将直接跳往下一个规则炼（mangle:postrouting）。范例如下：

```bash
iptables -t nat -A POSTROUTING -p tcp-o eth0 -j SNAT --to-source 192.168.10.15-192.168.10.160:2100-3200
```

**DNAT** 改写数据包包目的地 IP 为某特定 IP 或 IP 范围，可以指定 port 对应的范围，进行完此处理动作后，将会直接跳往下一个规则链（filter:input 或 filter:forward）。范例如下：

```bash
iptables -t nat -A PREROUTING -p tcp -d 15.45.23.67 --dport 80 -j DNAT --to-destination 192.168.10.1-192.168.10.10:80-100
```

**MIRROR**  镜像数据包，也就是将来源 IP与目的地IP对调后，将数据包返回，进行完此处理动作后，将会中断过滤程序。

**QUEUE**   中断过滤程序，将封包放入队列，交给其它程序处理。透过自行开发的处理程序，可以进行其它应用，例如：计算联机费用.......等。

**RETURN**  结束在目前规则链中的过滤程序，返回主规则链继续过滤，如果把自订规则炼看成是一个子程序，那么这个动作，就相当于提早结束子程序并返回到主程序中。

**MARK** 将封包标上某个代号，以便提供作为后续过滤的条件判断依据，进行完此处理动作后，将会继续比对其它规则。范例如下：

```bash
iptables -t mangle -A PREROUTING -p tcp --dport 22 -j MARK --set-mark 22
```

### 3. 常见命令

- 1. 删除iptables现有规则

```bash
iptables –F 
```

- 2. 查看iptables规则

```bash
iptables –L（iptables –L –v -n） 
```

- 3. 增加一条规则到最后

```bash
iptables -A INPUT -i eth0 -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT 
```

- 4.添加一条规则到指定位置

```bash
iptables -I INPUT 2 -i eth0 -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT 
```

- 5.  删除一条规则

```bash
iptabels -D INPUT 2 
```

- 6.修改一条规则

```bash
iptables -R INPUT 3 -i eth0 -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT 
```

- 7. 设置默认策略

```bash
iptables -P INPUT DROP 
```

- 8.允许远程主机进行SSH连接

```bash
iptables -A INPUT -i eth0 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT 
iptables -A OUTPUT -o eth0 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT 
```

- 9.允许本地主机进行SSH连接

```bash
iptables -A OUTPUT -o eth0 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT 
iptables -A INTPUT -i eth0 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT 
```

- 10.允许HTTP请求

```bash
iptables -A INPUT -i eth0 -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT 
iptables -A OUTPUT -o eth0 -p tcp --sport 80 -m state --state ESTABLISHED -j ACCEPT 
```

- 11.限制ping 192.168.146.3主机的数据包数，平均2/s个，最多不能超过3个

```bash
iptables -A INPUT -i eth0 -d 192.168.146.3 -p icmp --icmp-type 8 -m limit --limit 2/second --limit-burst 3 -j ACCEPT 
```

- 12.限制SSH连接速率(默认策略是DROP)

```bash
iptables -I INPUT 1 -p tcp --dport 22 -d 192.168.146.3 -m state --state ESTABLISHED -j ACCEPT  
iptables -I INPUT 2 -p tcp --dport 22 -d 192.168.146.3 -m limit --limit 2/minute --limit-burst 2 -m state --state NEW -j ACCEPT 
```

### 4. 如何正确配置iptables

- 1. 删除现有规则

```bash
iptables -F
```

- 2.  配置默认链策略

```bash
iptables -P INPUT DROP 
iptables -P FORWARD DROP 
iptables -P OUTPUT DROP 
```

- 3. 允许远程主机进行SSH连接

```bash
iptables -A INPUT -i eth0 -p tcp –dport 22 -m state –state NEW,ESTABLISHED -j ACCEPT 
iptables -A OUTPUT -o eth0 -p tcp –sport 22 -m state –state ESTABLISHED -j ACCEPT 
```

- 4. 允许本地主机进行SSH连接

```bash
iptables -A OUTPUT -o eth0 -p tcp –dport 22 -m state –state NEW,ESTABLISHED -j ACCEPT 
iptables -A INPUT -i eth0 -p tcp –sport 22 -m state –state ESTABLISHED -j ACCEPT 
```

- 5. 允许HTTP请求

```bash
iptables -A INPUT -i eth0 -p tcp –dport 80 -m state –state NEW,ESTABLISHED -j ACCEPT 
iptables -A OUTPUT -o eth0 -p tcp –sport 80 -m state –state ESTABLISHED -j ACCEPT 
```

### 5. 使用iptables抵抗常见攻击

- 1.防止syn攻击

思路一：限制syn的请求速度（这个方式需要调节一个合理的速度值，不然会影响正常用户的请求）

```bash
iptables -N syn-flood 

iptables -A INPUT -p tcp --syn -j syn-flood 

iptables -A syn-flood -m limit --limit 1/s --limit-burst 4 -j RETURN 

iptables -A syn-flood -j DROP 
```

思路二：限制单个ip的最大syn连接数

```
iptables –A INPUT –i eth0 –p tcp --syn -m connlimit --connlimit-above 15 -j DROP 
```

- 2. 防止DOS攻击

利用recent模块抵御DOS攻击

```bash
iptables -I INPUT -p tcp -dport 22 -m connlimit --connlimit-above 3 -j DROP 
```

单个IP最多连接3个会话

```bash
iptables -I INPUT -p tcp --dport 22 -m state --state NEW -m recent --set --name SSH  
```

只要是新的连接请求，就把它加入到SSH列表中

```bash
Iptables -I INPUT -p tcp --dport 22 -m state NEW -m recent --update --seconds 300 --hitcount 3 --name SSH -j DROP  
```

5分钟内你的尝试次数达到3次，就拒绝提供SSH列表中的这个IP服务。被限制5分钟后即可恢复访问。

- 3. 防止单个ip访问量过大

```bash
iptables -I INPUT -p tcp --dport 80 -m connlimit --connlimit-above 30 -j DROP 
```

- 4. 木马反弹

```bash
iptables –A OUTPUT –m state --state NEW –j DROP 
```

- 5. 防止ping攻击

```bash
iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/m -j ACCEPT 
```

## 三、iptables-restore命令及规则集语法

iptables-restore 命令用于从文件中恢复 iptables 防火墙规则。

### 1. 规则集语法

/etc/iptables/rules.v4 文件通常用于存储 IPv4 规则集。该文件遵循特定的语法格式,下面是一些主要语法元素:

1. **表和链**
   - 表语法: `*<table-name>`
     - 用于指定要操作的表,例如 filter、nat 或 mangle 表。
   - 链语法: `:<chain-name> <chain-policy> [<packet-counter>:<byte-counter>]`
     - <chain-name> 用于指定要操作的链,如 INPUT、FORWARD 或 OUTPUT。
     - <chain-policy> 是针对该链默认策略，如ACCEPT、DROP、REJECT。
     - <packet-counter> 是包记数器
     - <byte-counter> 是字节计数器，这两个计数器和 iptables -L -v 输出中用到的计数器一样。
     - 每个表的描述都以关键字 **COMMIT** 结 束：说明在这一点，就要把规则装入内核了
2. **规则规范**
   - 语法: `-m match --match-option [...]`
     - 用于指定匹配条件,如 `-p tcp` 表示匹配 TCP 协议数据包。
   - 语法: `-j target`
     - 用于指定规则目标,如 ACCEPT、DROP 或 REJECT 等。
3. **注释**
   - 语法: `#comment`
     - 以 `#` 开头的行被视为注释。
4. **提交更改**
   - 语法: `COMMIT`
     - 表示对当前表的操作完成,iptables-restore 会应用所做的更改。

### 2. 原则

应该遵循以下几个原则排列规则顺序:

1. **放行规则在前,拒绝规则在后** 例如,先允许SSH连接,最后才是拒绝所有其他规则。这样可以确保需要允许的流量获得优先处理。
2. **匹配范围小的规则在前,范围大的在后** 例如,先放行指定IP的SSH连接,再放行所有SSH连接。这种顺序可以避免过于宽泛的规则覆盖了更精确的规则。
3. **禁止在中间插入新规则** 应该将所有规则写在配置文件中,中间不要留有空位,否则手动临时插入的规则在重启后会消失。
4. **常用规则靠前,特殊规则靠后** 例如,SSH和HTTP规则应该放在前面,而一些特殊限制规则可以放在后面。
5. **采用模块化设计** 将一些相关的规则组合在一起,通过注释隔开,可以提高可读性和维护性。

## 脚本及服务

### 1. 服务

- 创建路径

```bash
sudo mkdir /etc/iptables
touch /etc/iptables/rules.v4
```

- `/etc/iptables/rules.v4` 规则示例

```bash
# 清空所有默认规则链
*filter

# 设置规则链的默认策略
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]

# 允许本地环回接口通信
-A INPUT -i lo -j ACCEPT
-A OUTPUT -o lo -j ACCEPT

# 允许接受已建立的连接
-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
-A OUTPUT -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT

# 允许 SSH 连接
-A INPUT -p tcp --dport 22 -j ACCEPT

# 允许 HTTP 和 HTTPS 连接
-A INPUT -p tcp --dport 80 -j ACCEPT 
-A INPUT -p tcp --dport 443 -j ACCEPT

# 允许 Ping
-A INPUT -p icmp --icmp-type 8 -j ACCEPT

# 允许特定网段访问
-A INPUT -s 192.168.1.0/24 -j ACCEPT

# 丢弃其他所有入站流量
-A INPUT -j DROP  

# 允许所有出站流量
-A OUTPUT -j ACCEPT
-A FORWARD -j ACCEPT

COMMIT
```

- 创建服务

```bash
[Unit]
Description=IPv4 IP Filter Administration
Before=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/sbin/iptables-restore --noflush /etc/iptables/rules.v4
ExecStop=/usr/sbin/iptables-save >/etc/iptables/rules.v4
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

- 启动服务

```bash
systemctl-daemon reload
systemctl start iptables
```

### 2. 添加脚本

- 过滤tcp

```bash
filter_input_tcp(){
    for (( i = 0; i < ${#port_list[@]}; i++ )); do
        port=${port_list[$i]}
        for (( j = 1; j < ${#cidr_list[@]}; j++ )); do
            pod_cidr=${cidr_list[$j]}            
            check_ip_exist=$(cat /etc/iptables/rules.v4 | grep -w "${pod_cidr} " | grep tcp | grep -w ${port})
            if [ -z "${check_ip_exist}" ];then
                sed -i "/:OUTPUT ACCEPT/a\-I INPUT -s ${pod_cidr} -p tcp --dport ${port} -j ACCEPT"   /etc/iptables/rules.v4
            fi
        done
        check_tcp_exist=$(cat /etc/iptables/rules.v4 | grep reject-with | grep tcp | grep -w ${port})
        if [ -z "${check_tcp_exist}" ];then
            sed -i "/:OUTPUT ACCEPT/a\-A INPUT -p ${protocl_list[$i]} --dport ${port} -j REJECT --reject-with tcp-reset"   /etc/iptables/rules.v4
        fi
    done
        systemctl restart iptables.service
        systemctl enable iptables.service
}
```

- 过滤udp

```bash
filter_input_udp(){
    for (( i = 0; i < ${#port_list[@]}; i++ )); do
        port=${port_list[$i]}
        for (( j = 1; j < ${#cidr_list[@]}; j++ )); do
            pod_cidr=${cidr_list[$j]}            
            check_ip_exist=$(cat /etc/iptables/rules.v4 | grep -w "${pod_cidr} " | grep tcp | grep -w ${port})
            if [ -z "${check_ip_exist}" ];then
                sed -i "/:OUTPUT ACCEPT/a\-I INPUT -s ${pod_cidr} -p tcp --dport ${port} -j ACCEPT"   /etc/iptables/rules.v4
            fi
        done
        check_udp_exist=$(cat /etc/sysconfig/iptables | grep DROP | grep udp | grep -w ${port})
        if [ -z "${check_udp_exist}" ];then
            sed -i "/:OUTPUT ACCEPT/a\-A INPUT -p udp --dport ${port} -j DROP"   /etc/sysconfig/iptables
        fi
    done
    systemctl restart iptables.service
    systemctl enable iptables.service
}
```

- 删除

```bash
# delete port config
delete_input_action(){
    for (( i = 0; i < ${#port_list[@]}; i++ )); do
        for (( j = 1; j < ${#param_list[@]}; j++ )); do
            clusterpod_cidr=${param_list[$j]}
            check_ip_exist=$(cat /etc/sysconfig/iptables | grep -w "${clusterpod_cidr} " | grep ${protocl_list[$i]} | grep -w ${port_list[$i]})
                        if [ ! -z "${check_ip_exist}" ];then
                            sed -i "/${clusterpod_cidr} \-p/d"   /etc/sysconfig/iptables
            fi
        done
    done
    systemctl restart iptables.service
    systemctl enable iptables.service
}
```

- 使用

```bash
# tcp
ips=$(cat ./ips)
port_list=(80 8080 443)
cidr_list=($ips 10.244.0.0/16 10.10.0.0/16 172.17.0.0/16 127.0.0.1)  

filter_input_tcp

# udp
ips=$(cat ./ips)
port_list=(80 8080 443)
cidr_list=($ips 10.244.0.0/16 10.10.0.0/16 172.17.0.0/16 127.0.0.1)  

filter_input_udp

# param number need more then 2
# if [[ $# -lt 2 ]]; then
#     echo "for example:config_port_filter.sh add 10.233.0.0/16 100.2.126.0/24"
#     echo "for example:config_port_filter.sh delete 10.233.0.0/16 100.2.126.0/24"
#     exit 1
# fi

# first param must be add or delete
# if [[ "$1" != "add" && "$1" != "delete" ]]; then
#     echo "$0 param:$1 must be 'add' or 'delete'"
#     exit 1
# fi

# if [ "$1" == "add" ]; then
#     add_input_action
# else
#     delete_input_action
# fi
```
