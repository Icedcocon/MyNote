# 1.DNS服务器概述

### 1.1为什么使用域名

1. 互联网为什么要使用用域名(domain name)
   
   - 不好记忆
   
   - 计算机可能常常更换P地址，通过IP地址去访问会发生问题

2. 什么是DNS(Domain Name System)
   
   - DNS(Domain Name System)是“域名系统”的英文缩写，是一种组织成域层次结构的计算机和网络服务命名系统，它用于TCP/IP网络，它所提供的服务是用来将主机名和域名转换为P地址的工作。

3. 域的结构
   
   <img title="" src="file:///D:/Cache/MarkText/2022-08-24-08-28-14-image.png" alt="" data-align="center" width="427">
   
   - 根域
     
     - 全世界只有13组根服务器，名字分别为“A“至“M”，其中10台设置在美国，另外的三台设置于英国、瑞典和日本。
   
   - 顶级域
     
     - 顶级域有两种：通用域(generic)和国家域(country)
     
     - 顶级域名由ICANN委任的注册机构负责运行
   
   - 二级域名
     
     - 无需到ICANN进行申请，只需要到运行顶级域名的注册机构去检查待申请的名字是否可用。

4. 域名规则
   
   - 域名是大小写无关的，OD.CoM和od.com是一样的
   
   - 各组成部分的名字最多有63个字符长，整个路径不超过255个字符
   
   - 没有规则限制同时在两个或多个顶级域名下的注册(例如：sony.com和sony.net)
   
   - 要创建一个新的域，创建者必须得到该新域的上级域的许可，一旦创建成功，该新域就可创建子域，无需征得上级域的同意
   
   - 域名遵循的是组织的边界而不是物理网络的边界

5. DNS解析原理
   
   <img title="" src="file:///D:/Cache/MarkText/2022-08-24-08-38-17-image.png" alt="" data-align="center" width="458">
   
   - DNS查询时，会先检查本地hosts，随后才会发起DNS递归查询

# 2.bind9软件使用详解

### 2.1 /etc/named.conf

`named.conf`是`bind9`的最先读取的配置文件，`named`支持如下语句:

- **`acl`：定义IP 地址匹配列表，用于访问控制等。**

- **`controls`：定义`rndc`命令使用的控制通道。**

- **`include`：包含其他文件到配置文件。**

- **`key`：定义用于TSIG的授权密钥。**

- **`logging`：指定日志内容和位置。**

- **`options`：全局配置选项及置默认值。**

- **`view`：定义域名空间的一个视图。**

- **`zone`：定义一个区声明。**

- `dnssec-policy`：描述区域的 DNSSEC 密钥和签名策略。

- `masters`：定义一个命名的主列表以包含在存根和辅助区域`masters`或`also-notify`列表中。

- `server`：基于每个服务器设置某些配置选项。

- `statistics-channels`：声明获取`named`统计信息的通信渠道。

- `trust-anchors`：定义 DNSSEC 信任锚

- `managed-keys`：等同于`trust-anchors`; 此选项已弃用，取而代之的`trust-anchors`是`initial-key`关键字，并且可能会在将来的版本中删除。

- `trusted-keys`：定义永久受信任的 DNSSEC 密钥；此选项已弃用，取而代之的`trust-anchors`是`static-key`关键字，并且可能会在将来的版本中删除。

##### 2.1.1 acl

**acl** 用来对bind的访问进行限制，是一个全局的设置，前面配置的`acl`在整个`bind`中都适用，和路由器里面的`access-list`有同工之处，语法是

```markdown
acl acl-name {
    address_match_list};
```

其中的`address_match_list`是一个地址列表，如`192.168.0.0/24;`，记住最后一定得有分号，有多个的话中间用分号格开，如`192.168.0.0/32;192.168.1.0/24;`

bind内置了4个acl分别是:

- `any`:对应所有的，也就是0.0.0.0/0。
- `none`:对应为空。
- `localhost`:对应本地机器。
- `localnets`:对应本地网络。

##### 2.1.2 controls

**controls**主要用于对bind进行控制，如:

```cfg
key "rndc-key" {
    algorithm hmac-md5;
    secret "VkMaNHXfOiPQqcMVYJRyjQ==";
};
```

```cfg
controls {
    inet 127.0.0.1 port 953
    allow { 127.0.0.1; } keys { "rndc-key"; };
};
```

设置`rndc`控制的端口以及端口，`keys`用来设置控制的密钥

##### 2.1.3 include

**include**是一个非常有用的选项，如果需要写程序来读写bind的配置文件，这个将会用到，因为bind的配置文件很不规则，但是用了include后，就可以变的很规则，就和数据库一样了，功用和c语言里面的`include`一样。

用于导入拆分的配置文件。

##### 2.1.4 options

**options**是用于设置bind的一些选项，我们将重点介绍，BING9支持的选项如下:

```conf
options {
    // *allow-recursion允许递归查询的地址列表(allow-recursion)：
    // 设置允许进行递归查询的ip地址列表，缺省值是允许所有地址进行查询，
    // 需要注意的是当设置了不允许递归查询后，如果仍然能够查询部分外部
    // 的域名，那是因为dns的缓存在起作用，将缓存清除以后就可以了。
    allow-recursion { address_match_element; };
    allow-v6-synthesis { address_match_element; };

    // *allow-query 允许普通查询的地址列表（allow-query）:设置允
    // 许进行普通查询的ip地址列表，在域中的设置将覆盖全局设置，默认情
    // 况下是允许所有的地址进行普通查询。
    allow-query { address_match_element; };

    // *allow-transfer允许服务器进行区域传输的地址列表(Allow-transfer):
    // (注意的是视区和域中的设置将覆盖全局设置)
    allow-transfer { address_match_element; ... };

    // *allow-notify 允许更新通知的地址列表(allow-notify)，当服务器
    // 作为辅助服务器的时候，设置这个可以对收到的更新通知进行判断，只是
    // 接收该列表的更新通知.默认情况下，只是接收来自主服务器的更新通知。
    // 对于其他服务器的更新通知，会忽略掉。
    allow-notify { address_match_element; ... };

    // *auth-nxdomain 是否作为权威服务器回答域不存在（Auth-nxdomain）
    // 如果设置为'yes'，则允许服务器以权威性（authoritatively）的方式
    // 返回NXDOMAIN（该域不存在）的回答，否则就不会作权威性的回答，缺省值为”是”.
    auth-nxdomain boolean; // default changed

    // *blockhole 定义服务器不对查询进行反应的地址列表，也就是”黑名单”，
    // 比如说3721的ip段:218.244.44.0/24，当设置了黑名单后，对于这个段
    // 的请求查询，服务器将不会作出反应.
    blackhole { address_match_element; };

    // *directory 设置bind的数据文件的存放位置:如 directory “/var/named”.
    directory quoted_string;

    // *dump-file 设置当执行rndc dumpdb命令后的导出文件存放绝对路径，
    // 如果没有指定的话，缺省文件为named_dump.db，放在directory指定
    // 的目录下面.
    dump-file quoted_string;

    // *interface-interval 设置bind检查网卡变化的周期.
    interface-interval integer;

    // *listen-on 设置bind的绑定ip和端口，如listen-on 53 {192.168.0.1;};
    listen-on [ port integer ] { address_match_element; ... };
    listen-on-v6 [ port integer ] { address_match_element; ... };

    // *pid-file 设置bind的进程号pid文件.
    pid-file quoted_string;

    // *version 设置客户查询DNS版本好的返回信息，如果不想让客户探测到
    // 当前的版本号，就用这个好了，如version mydns1.0;
    version quoted_string;

    minimal-responses boolean;

    // *recursion 是否允许递规查询(recursion)如果设置为”yes”，则允许
    // 服务器采用递归的方式进行查询，也就是当要查询的地址不在服务器的数据
    // 库列表中时，服务器将一级一级的查询，直到查到为止（一般对局域网都打开）
    // 。设置为”no”，并不意味着服务器对于请求的递归查询不给予回答，而是对
    // 于请求的递归查询，不再向上级服务器请求，也不缓存，如果不对请求的递
    // 归查询回答，可以清空缓存，然后设置为“NO”。
    recursion boolean;

    // *max-cache-size 设置最大缓存的大小，如max-cache-size 5M
    max-cache-size size_no_default;

    // *notify 在主服务器更新时是否通知辅助服务器(notify)
    // 如果设置为”yes”，则在主服务器区域数据发生变化时，就会向在域的
    // ”域名服务器“中列出的服务器和“亦通知”中列出的服务器发送更新通知。
    // 这些服务器接受到更新通知后，就会向主服务器发送请求传输的消息，然后
    // 区域文件得以更新。
    notify notifytype;
    notify-source ( ipv4_address | * ) [ port ( integer | * ) ];
    notify-source-v6 ( ipv6_address | * ) [ port ( integer | * ) ];

    // *also-notify 更新时亦通知下列地址(also-notify)，设置发送更新
    // 通知的时候，不仅是域名服务器中列出的地址，亦通知此地址列表中的地址。
    also-notify [ port integer ] { ( ipv4_address | ipv6_address ) [ port integer ]; };
    dialup dialuptype;

    // *forward 值有first和only两项， first则首先转发到"forwarders"中
    // 的服务器，然后自己查询，only则仅转发到 "转发服务器列表"中的服务器，
    // 不再自己查询
    forward ( first | only );

    // *forwarders设置转发服务器地址列表，语法同acl中的语法.
    forwarders [ port integer ] { ( ipv4_address | ipv6_address ) [ port integer ]; };
};
```

- `obsolete`是已经过时的选项，这里不用考虑，
- `not yet implemented`是尚未完成的选项，这里也不用考虑，下面详细介绍这里面的有用选项 

# 3.DNS正解、反解配置详解

### 3.1 DNS的自定义区域配置

##### 3.1.1

- 定义在`/etc/named.rfc1912.zones`里
  
  - 也可以配置在自定义的其他文件里，并在named.conf里include
  
  - 注意文件的权限，属主root属组named,640

- 格式：
  
  ```bash
  // 自定义了一个host.com的主机域(master)
  zone "host.com" IN {
      type master|slave|hint;    //自定义区域类型
      file /path-to-zonefile;    //区域数据库文件位置（绝对或相对路径）
      allow-update { ip|acl };   //是否允许动态更新
  };
  ```

- 主机域
  
  - 主机域和业务域无关，且建议分开
  - 主机域其实是一个假域，是不能解析到互联网上的，它只对局域网（内网）提供服务

##### 3.1.2 DNS服务器种类

- master(主DNS服务器)：拥有区域数据的文件，并对整个区域数据进行管理。

- slave（从服务器或知叫辅助服务器）：拥有主DNS服力器的区域文件的副本，辅助
  DNS服务器对客户端进行解析，当主DNS服务器坏了后，可以完全接替主服务器的工作。

- forward：将任何查间请求都转发给其他服务器。起到一个代理的作用。

- cache：缓存服务器。

- hint：根DNS internet服务器集。

##### 3.1.3 错误检查

- 使用`named-checkconf`

### 3.2 区域数据库文件（zonefile）配置

##### 3.2.1 资源记录格式

- 定义在`/var/named/zonefile-name`里，位置可通过`/etc/named.conf`修改。
  
  - 区域数据库文件中有且仅有**资源记录**、**宏定义**和**注释**
  
  - 以.zone结尾，属主root,属组named,权限640

- 资源记录(Resource Record)
  
  - 格式：`name [ttl(缓存时间)] IN 资源记录类型（RRtype） Value`
  
  - 常见资源记录(Resource Record)类型：(RR-type)
    
    - SOA:Start Of Authority,起始授权，必须有且只有一条
    
    - NS:域名服务器的标识记录
    
    - A:IPv4主机地址
    
    - AAAA:IPv6主机地址
    
    - MX:邮件交换记录
    
    - CNAME:Canonical Name,正式名称（别名），CDN里用的最多
    
    - TXT:文本字符串，长度限制512Byte,通常做SPF记录（反垃圾邮件）
    
    - PTR记录：指针记录，用来实现反向解析的

- 宏定义(以\$开头的部分)
  
  - \$TTL 60
  
  - \$ORIGIN.

- 注释(以；开头的部分)
  
  - 1 minute
  
  - serial

##### 3.2.2 常用资源记录类型（RR-type）

#### SOA记录

SOA: 起始授权，只能有一条

- name:只能是区域名称，通常可以简写为@，例如：od.com.
- value:有n个数值，最主要的是主DNS服务器的FQDN，点不可省略

**注意**：SOA必须是区域数据库文件第一条记录

```bash
@ 600 IN SOA  dns.host.com. 管理员邮箱 (dnsadmin.host.com.) (
     序列号(serial number) ;注释内容，十进制数据，不能超过10位，通常使用日期时间戳，例如2018121601
     刷新时间(refresh time);即每隔多久到主服务器检查一次
     重试时间(retry time)  ;应该小于refresh time
     过期时间(expire time) ;当辅助DNS服务器无法联系上主DNS服务器时，辅助DNS服务器可以在多长时间内认为其缓存是有效的，并供用户查询。
     netgative answer ttl ;非权威应答的ttl，缓存DNS服务器可以缓存记录多长时间
 )
```

#### NS记录

NS：可以有多条，每一个NS记录，**必须**对应一个A记录

- name:区域名称，通常可以简写为@
- value:DNS服务器的FQDN(可以使用相对名称)

```bash
@ 600 IN NS ns1
```

#### A记录

A：只能定义在正向区域数据库文件中（ipv4->FQDN）

- name:FQDN（可以使用相对名称)
- value:IP

```bash
www  600(单位s) IN A 10.4.7.11
www  600(单位s) IN A 10.4.7.12
```

**可以做轮询**，将一个域名解析成不同IP

##### 3.2.3 错误检查

- 使用`named-checkzone domainname pathname`

### 3.3 配置实战

- 配置完bind9的文件后
  
  - 修改`/etc/resolv.conf`
  
  - 或修改`/etc/sysconfig/network-scripts/ifcfg-网络名称(eth0)`增加'DNS1=10.4.7.11'
  
  - 执行`systemctl restart network`

# 4.DNS主辅同步配置详解

# 5.DNS工具软件使用和rndc远程管理

# 6.智能DNS实战

# 7.bind-chroot和dnssec技术实战

# 8.企业级web dns构建实战
