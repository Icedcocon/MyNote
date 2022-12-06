Netfilter可以理解为在IP层处理的各个节点插入检查点，执行到该阶段时，逐个执行检查点的函数指针列表。Netfilter设置了五个检查点，分别是:

- PREROUTING
- INPUT
- OUTPUT
- POSTROUTING
- FORWARD

这五个检查点主要是围绕着路由子系统来进行的。

### 网络层大蓝图

![](https://pic2.zhimg.com/v2-e8da51e1d45f0047497c42f391999651_b.jpg)

这是IP层内核处理的整体流程，图片来源于《[深入理解linux网络技术内幕](https://www.zhihu.com/search?q=%E6%B7%B1%E5%85%A5%E7%90%86%E8%A7%A3linux%E7%BD%91%E7%BB%9C%E6%8A%80%E6%9C%AF%E5%86%85%E5%B9%95&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22article%22%2C%22sourceId%22%3A%22322311354%22%7D)》。

**本文接下来所有的源代码均是基于linux2.6.0**，之所以选择linux2.6.0是因为代码比较老，相对而言代码复杂性没那么高，但是核心的思想又没怎么变。比较适合入手阅读。

Netfilter针对钩子定义了两个接口，nf_register_hook和nf_unregister_hooks，分别用来注册[钩子函数](https://www.zhihu.com/search?q=%E9%92%A9%E5%AD%90%E5%87%BD%E6%95%B0&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22article%22%2C%22sourceId%22%3A%22322311354%22%7D)和取消钩子函数注册。

```c
struct nf_hook_ops
{
    struct list_head list;

    /* User fills in from here down. */
    nf_hookfn *hook;
    struct module *owner;
    int pf;
    int hooknum;
    /* Hooks are ordered in ascending priority. */
    int priority;
};                                                                            
/* Function to register/unregister hook points. */
int nf_register_hook(struct nf_hook_ops *reg);
void nf_unregister_hook(struct nf_hook_ops *reg);
```

这两个接口的实现代码很短。

首先来看一下nf_register_hook这个接口的实现:

```c
int nf_register_hook(struct nf_hook_ops *reg)
{
    struct list_head *i;

    spin_lock_bh(&nf_hook_lock);
    list_for_each(i, &nf_hooks[reg->pf][reg->hooknum]) {
        if (reg->priority < ((struct nf_hook_ops *)i)->priority)
            break;
    }
    list_add_rcu(&reg->list, i->prev);
    spin_unlock_bh(&nf_hook_lock);

    synchronize_net();
    return 0;
}
```

nf_register_hook往nf_hooks这个[二维数组](https://www.zhihu.com/search?q=%E4%BA%8C%E7%BB%B4%E6%95%B0%E7%BB%84&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22article%22%2C%22sourceId%22%3A%22322311354%22%7D)插入nf_hook_ops这个结构，插入的位置按照优先级排序，priority越小，越靠前，在该hook点处理时优先级越高。priority的定义如下，这个优先级在后面文章当中会经常用到。

```c
enum nf_ip_hook_priorities {
    NF_IP_PRI_FIRST = INT_MIN,
    NF_IP_PRI_CONNTRACK = -200,
    NF_IP_PRI_BRIDGE_SABOTAGE_FORWARD = -175,
    NF_IP_PRI_MANGLE = -150,
    NF_IP_PRI_NAT_DST = -100,
    NF_IP_PRI_BRIDGE_SABOTAGE_LOCAL_OUT = -50,
    NF_IP_PRI_FILTER = 0,
    NF_IP_PRI_NAT_SRC = 100,
    NF_IP_PRI_LAST = INT_MAX,
};
```

nf_hooks结构:

```c
#define NPROTO        32        
#define NF_MAX_HOOKS 8

struct list_head nf_hooks[NPROTO][NF_MAX_HOOKS];

// HOOK点定义
// 跟iptables当中的链一样
/* IP Hooks */
/* After promisc drops, checksum checks. */
#define NF_IP_PRE_ROUTING    0
/* If the packet is destined for this box. */
#define NF_IP_LOCAL_IN        1
/* If the packet is destined for another interface. */
#define NF_IP_FORWARD        2
/* Packets coming from a local process. */
#define NF_IP_LOCAL_OUT        3
/* Packets about to hit the wire. */
#define NF_IP_POST_ROUTING    4
#define NF_IP_NUMHOOKS        5

// 地址协议族
/* Supported address families. */
#define AF_UNSPEC    0
#define AF_UNIX        1    /* Unix domain sockets         */
#define AF_LOCAL    1    /* POSIX name for AF_UNIX    */
#define AF_INET        2    /* Internet IP Protocol     */
#define AF_AX25        3    /* Amateur Radio AX.25         */
#define AF_IPX        4    /* Novell IPX             */
#define AF_APPLETALK    5    /* AppleTalk DDP         */
#define AF_NETROM    6    /* Amateur Radio NET/ROM     */
#define AF_BRIDGE    7    /* Multiprotocol bridge     */
#define AF_ATMPVC    8    /* ATM PVCs            */
#define AF_X25        9    /* Reserved for X.25 project     */
#define AF_INET6    10    /* IP version 6            */
#define AF_ROSE        11    /* Amateur Radio X.25 PLP    */
#define AF_DECnet    12    /* Reserved for DECnet project    */
#define AF_NETBEUI    13    /* Reserved for 802.2LLC project*/
#define AF_SECURITY    14    /* Security callback pseudo AF */
#define AF_KEY        15      /* PF_KEY key management API */
#define AF_NETLINK    16
#define AF_ROUTE    AF_NETLINK /* Alias to emulate 4.4BSD */
#define AF_PACKET    17    /* Packet family        */
#define AF_ASH        18    /* Ash                */
#define AF_ECONET    19    /* Acorn Econet            */
#define AF_ATMSVC    20    /* ATM SVCs            */
#define AF_SNA        22    /* Linux SNA Project (nutters!) */
#define AF_IRDA        23    /* IRDA sockets            */
#define AF_PPPOX    24    /* PPPoX sockets        */
#define AF_WANPIPE    25    /* Wanpipe API Sockets */
#define AF_LLC        26    /* Linux LLC            */
#define AF_BLUETOOTH    31    /* Bluetooth sockets         */
#define AF_MAX        32    /* For now.. */
```

nf_unregister_hook则执行链表节点删除操作：

```c
void nf_unregister_hook(struct nf_hook_ops *reg)
{
    spin_lock_bh(&nf_hook_lock);
    list_del_rcu(&reg->list);
    spin_unlock_bh(&nf_hook_lock);

    synchronize_net();
}
```

**至此可以将Netfilter执行过程总结为**: Netfilter通过协议族以及hook点确定一个执行入口，如果要使用netfilter钩子函数挂载自己的钩子，那么需要调用nf_register_hook方法，指明hook点以及优先级，当执行到该hook点时，根据优先级顺序调用挂在在该hook点的处理函数。这就是[netfilter](https://www.zhihu.com/search?q=netfilter&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22article%22%2C%22sourceId%22%3A%22322311354%22%7D)这个框架本身的作用，其他任何功能，iptables，ipvs都是基于这个基础之上开发的netfilter模块。

### 数据包接收

那么会有这么一个疑问，netfilter给谁用：答案是内核，或者说IP层协议栈，。要了解这一过程，需要以外部发往本机的数据包在IP[协议栈](https://www.zhihu.com/search?q=%E5%8D%8F%E8%AE%AE%E6%A0%88&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22article%22%2C%22sourceId%22%3A%22322311354%22%7D)当中是怎么逐层调用的。

协议栈在数据包的生命周期内，到达指定位置就会执行NF_HOOK这个宏

```c
#ifdef CONFIG_NETFILTER_DEBUG
#define NF_HOOK(pf, hook, skb, indev, outdev, okfn)            \
 nf_hook_slow((pf), (hook), (skb), (indev), (outdev), (okfn), INT_MIN)
#define NF_HOOK_THRESH nf_hook_slow
#else
#define NF_HOOK(pf, hook, skb, indev, outdev, okfn)            \
(list_empty(&nf_hooks[(pf)][(hook)])                    \
 ? (okfn)(skb)                                \
 : nf_hook_slow((pf), (hook), (skb), (indev), (outdev), (okfn), INT_MIN))
#define NF_HOOK_THRESH(pf, hook, skb, indev, outdev, okfn, thresh)    \
(list_empty(&nf_hooks[(pf)][(hook)])                    \
 ? (okfn)(skb)                                \
 : nf_hook_slow((pf), (hook), (skb), (indev), (outdev), (okfn), (thresh)))
#endif

int nf_hook_slow(int pf, unsigned int hook, struct sk_buff *skb,
         struct net_device *indev, struct net_device *outdev,
         int (*okfn)(struct sk_buff *), int thresh);
```

nf_hook_slow会迭代nf_hooks这个二维数组，顺讯执行每一个处理函数，知道遇到处理函数返回NF_ACCEPT或者NF_DROP，则结束。

```c
    elem = &nf_hooks[pf][hook];
 next_hook:
    verdict = nf_iterate(&nf_hooks[pf][hook], &skb, hook, indev,
                 outdev, &elem, okfn, hook_thresh);
    if (verdict == NF_QUEUE) {
        NFDEBUG("nf_hook: Verdict = QUEUE.\n");
        if (!nf_queue(skb, elem, pf, hook, indev, outdev, okfn))
            goto next_hook;
    }

    switch (verdict) {
    case NF_ACCEPT:
        ret = okfn(skb);
        break;

    case NF_DROP:
        kfree_skb(skb);
        ret = -EPERM;
        break;
    }
```

这里面有个NF_QUEUE操作，属于数据包往用户层发数据的一个机制，允许在用户层处理数据包。

内核首先在ip_rcv函数会调用NF_HOOK，进入Netfilter的`NF_IP_PRE_ROUTING`这个hook点处理，处理完成之后，会执行`ip_rcv_finish`这个[回调函数](https://www.zhihu.com/search?q=%E5%9B%9E%E8%B0%83%E5%87%BD%E6%95%B0&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra=%7B%22sourceType%22%3A%22article%22%2C%22sourceId%22%3A%22322311354%22%7D)。

```c
    return NF_HOOK(PF_INET, NF_IP_PRE_ROUTING, skb, dev, NULL,
               ip_rcv_finish);
```

在ip_rcv_finish当中，首先处理路由，然后处理选项，最后再决定数据包怎么发。

**处理路由:**

```c
    if (skb->dst == NULL) {
        if (ip_route_input(skb, iph->daddr, iph->saddr, iph->tos, dev))
            goto drop; 
    }
```

路由本身是个非常复杂，非常恶心的事，但是路由最终会使得skb-dst不为NULL，并设置下一步骤的回调函数:

- ip_forward
- ip_local_deliver  
  最后在dst_input时会调用这两者当中的一个。

**处理选项:**

```c
    if (iph->ihl > 5) {
        struct ip_options *opt;

        /* It looks as overkill, because not all
           IP options require packet mangling.
           But it is the easiest for now, especially taking
           into account that combination of IP options
           and running sniffer is extremely rare condition.
                                              --ANK (980813)
        */

        if (skb_cow(skb, skb_headroom(skb))) {
            IP_INC_STATS_BH(IpInDiscards);
            goto drop;
        }
        iph = skb->nh.iph;

        if (ip_options_compile(NULL, skb))
            goto inhdr_error;

        opt = &(IPCB(skb)->opt);
        if (opt->srr) {
            struct in_device *in_dev = in_dev_get(dev);
            if (in_dev) {
                if (!IN_DEV_SOURCE_ROUTE(in_dev)) {
                    if (IN_DEV_LOG_MARTIANS(in_dev) && net_ratelimit())
                        printk(KERN_INFO "source route option %u.%u.%u.%u -> %u.%u.%u.%u\n",
                               NIPQUAD(iph->saddr), NIPQUAD(iph->daddr));
                    in_dev_put(in_dev);
                    goto drop;
                }
                in_dev_put(in_dev);
            }
            if (ip_options_rcv_srr(skb))
                goto drop;
        }
    }
```

**投递到下一步骤:**

```c
static inline int dst_input(struct sk_buff *skb)
{
    int err;

    for (;;) {
        err = skb->dst->input(skb);

        if (likely(err == 0))
            return err;
        /* Oh, Jamal... Seems, I will not forgive you this mess. :-) */
        if (unlikely(err != NET_XMIT_BYPASS))
            return err;
    }
}
```

这里`skb->dst->input`会调用在上面提到的

- ip_forward
- ip_local_deliver  
  这两个函数。

首先来分析ip_local_deliver，这个是在路由时判断数据包是发往本地时会执行的流程，实现代码看起来也很短。。首先判断是否分片，分片则先处理分片先，之后又执行了NF_HOOK这个宏，不过hooknum现在到了`NF_IP_LOCAL_IN`了，并且处理完成之后执行`ip_local_deliver_finish`函数。

```c
int ip_local_deliver(struct sk_buff *skb)
{
    /*
     *    Reassemble IP fragments.
     */

    if (skb->nh.iph->frag_off & htons(IP_MF|IP_OFFSET)) {
        skb = ip_defrag(skb);
        if (!skb)
            return 0;
    }

    return NF_HOOK(PF_INET, NF_IP_LOCAL_IN, skb, skb->dev, NULL,
               ip_local_deliver_finish);
}
```

所以说netfilter只是一个框架，需要在此基础之上实现自身的处理函数，到时框架会自动调用你注册的钩子函数。这样我想起以前学windows消息模型时的一句话: `Dont call me, I will call you`

接下来分析数据包不是发往本地的，需要执行`ip_forward`，在ip_forward的最后，同样调用了NF_HOOK，不过hook点换成了NF_IP_FORWARD，处理完`nf_hooks[PF_INET][NF_IP_FORWARD]`下的回调函数列表之后，调用`ip_forward_finish`完成转发过程，并将数据包往外发。

```c
    return NF_HOOK(PF_INET, NF_IP_FORWARD, skb, skb->dev, rt->u.dst.dev,
               ip_forward_finish);
```

接下来是**往外转发**的过程。

```c
int ip_finish_output(struct sk_buff *skb)
{
    struct net_device *dev = skb->dst->dev;

    skb->dev = dev;
    skb->protocol = htons(ETH_P_IP);

    return NF_HOOK(PF_INET, NF_IP_POST_ROUTING, skb, NULL, dev,
               ip_finish_output2);
}

int ip_output(struct sk_buff *skb)
{
    IP_INC_STATS(IpOutRequests);

    if ((skb->len > dst_pmtu(skb->dst) || skb_shinfo(skb)->frag_list) &&
        !skb_shinfo(skb)->tso_size)
        return ip_fragment(skb, ip_finish_output);
    else
        return ip_finish_output(skb);
}
```

往外转发过程同样需要处理分片，最终会执行挂在`NF_IP_POST_ROUTING`上的钩子函数，至此进入这台机器的该数据包已经完成所有在Netfilter当中的行走路径。

### 数据包发送

在数据包接收过程当中，会经过netfilter的`NF_IP_PREROUTING`，`NF_IP_LOCAL_IN` ，`NF_IP_FORWARD`，`NF_IP_POST_ROUTING`四个hook点，还有另外一种数据包，不是从进入该机器的数据包，是从该机器往外发送的数据包，这类数据包会涉及`NF_IP_LOCAL_OUT`这个hook点，然后再经过`NF_IP_POST_ROUTING` hook点至此所有netfilter的五个hook点都有被调用到了，过程类似数据包接收，会在后续SNAT的实现详细说明。









Netfilter概述

Netfilter/IPTables是Linux2.4.x之后新一代的Linux防火墙机制，是linux内核的一个子系统。Netfilter采用模块化设计，具有良好的可扩充性。其重要工具模块IPTables从用户态的iptables连接到内核态的Netfilter的架构中，Netfilter与IP协议栈是无缝契合的，并允许使用者对数据报进行过滤、地址转换、处理等操作。

主要源代码文件

Linux内核版本：2.4.x以上

Netfilter主文件：net/core/netfilter.c

Netfilter主头文件：include/linux/netfilter.h

IPv4相关：

c文件：net/ipv4/netfilter/*.c

头文件：include/linux/netfilter_ipv4.h

include/linux/netfilter_ipv4/*.h

IPv4协议栈主体的部分c文件，特别是与数据报传送过程有关的部分：

ip_input.c，ip_forward.c，ip_output.c，ip_fragment.c等

## 具体功能模块

1. 数据报过滤模块

2. 连接跟踪模块（Conntrack）

3. 网络地址转换模块（NAT）

4. 数据报修改模块（mangle）

5. 其它高级功能模块

Netfilter实现

Netfilter主要通过表、链实现规则，可以这么说，Netfilter是表的容器，表是链的容器，链是规则的容器，最终形成对数据报处理规则的实现。

数据在协议栈里的发送过程中，从上至下依次是“加头”的过程，每到达一层数据就被会加上该层的头部；与此同时，接受数据方就是个“剥头”的过程，从网卡收上包来之后，在往协议栈的上层传递过程中依次剥去每层的头部，最终到达用户那儿的就是裸数据了。

![](https://pic1.zhimg.com/80/v2-0bee8a8a9d05f538e4a9f3fee5ad6d14_720w.webp)

对于收到的每个数据包，都从“A”点进来，经过路由判决，如果是发送给本机的就经过“B”点，然后往协议栈的上层继续传递；否则，如果该数据包的目的地是不本机，那么就经过“C”点，然后顺着“E”点将该包转发出去。

对于发送的每个数据包，首先也有一个路由判决，以确定该包是从哪个接口出去，然后经过“D”点，最后也是顺着“E”点将该包发送出去。

协议栈那五个关键点A，B，C，D和E就是我们Netfilter大展拳脚的地方了。

Netfilter是Linux 2.4.x引入的一个子系统，它作为一个通用的、抽象的框架，提供一整套的hook函数的管理机制，使得诸如数据包过滤、网络地址转换(NAT)和基于协议类型的连接跟踪成为了可能。Netfilter在内核中位置如下图所示：

![](https://pic2.zhimg.com/80/v2-b28289f9873b2680914a85feb5669961_720w.webp)

这幅图很直观的反应了用户空间的iptables和内核空间的基于Netfilter的ip_tables模块之间的关系和其通讯方式，以及Netfilter在这其中所扮演的角色。

Netfilter在netfilter_ipv4.h中将这个五个点重新命了个名，如下图所示：

![](https://pic3.zhimg.com/80/v2-8be6e648094e2b0bda661da967ca80f2_720w.webp)

在每个关键点上，有很多已经按照优先级预先注册了的回调函数(称为“钩子函数”)埋伏在这些关键点，形成了一条链。对于每个到来的数据包会依次被那些回调函数“调戏”一番再视情况是将其放行，丢弃还是怎么滴。但是无论如何，这些回调函数最后必须向Netfilter报告一下该数据包的死活情况，因为毕竟每个数据包都是Netfilter从人家协议栈那儿借调过来给兄弟们Happy的，别个再怎么滴也总得“活要见人，死要见尸”吧。每个钩子函数最后必须向Netfilter框架返回下列几个值其中之一：

1. NF_ACCEPT继续正常传输数据报。这个返回值告诉Netfilter：到目前为止，该数据包还是被接受的并且该数据包应当被递交到网络协议栈的下一个阶段。

2. NF_DROP丢弃该数据报，不再传输。

3. NF_STOLEN模块接管该数据报，告诉Netfilter“忘掉”该数据报。该回调函数将从此开始对数据包的处理，并且Netfilter应当放弃对该数据包做任何的处理。但是，这并不意味着该数据包的资源已经被释放。这个数据包以及它独自的sk_buff数据结构仍然有效，只是回调函数从Netfilter获取了该数据包的所有权。

4. NF_QUEUE对该数据报进行排队(通常用于将数据报给用户空间的进程进行处理)

5. NF_REPEAT 再次调用该回调函数，应当谨慎使用这个值，以免造成死循环。

为了让我们显得更专业些，我们开始做些约定：上面提到的五个关键点后面我们就叫它们为hook点，每个hook点所注册的那些回调函数都将其称为hook函数。

Linux 2.6版内核的Netfilter目前支持IPv4、IPv6以及DECnet等协议栈，这里我们主要研究IPv4协议。关于协议类型，hook点，hook函数，优先级，通过下面这个图给大家做个详细展示：

![](https://pic2.zhimg.com/80/v2-0ffb0448075b60eedc4cdd13b90e2ffd_720w.webp)

对于每种类型的协议，数据包都会依次按照hook点的方向进行传输，每个hook点上Netfilter又按照优先级挂了很多hook函数。这些hook函数就是用来处理数据包用的。

Netfilter使用NF_HOOK(include/linux/netfilter.h)宏在协议栈内部切入到Netfilter框架中。相比于2.4版本，2.6版内核在该宏的定义上显得更加灵活一些，定义如下：

#define NF_HOOK(pf, hook, skb, indev, outdev,okfn) \

NF_HOOK_THRESH(pf, hook, skb, indev, outdev, okfn, INT_MIN)2

关于宏NF_HOOK各个参数的解释说明：

1) pf：协议族名，Netfilter架构同样可以用于IP层之外，因此这个变量还可以有诸如PF_INET6，PF_DECnet等名字。

2) hook：HOOK点的名字，对于IP层，就是取上面的五个值；

3) skb：网络设备数据缓存区；

4) indev：数据包进来的设备，以struct net_device结构表示；

5) outdev：数据包出去的设备，以struct net_device结构表示；

(后面可以看到，以上五个参数将传递给nf_register_hook中注册的处理函数。)

6) okfn:是个函数指针，当所有的该HOOK点的所有登记函数调用完后，转而走此流程。

而NF_HOOK_THRESH又是一个宏：

#define NF_HOOK_THRESH(pf, hook, skb, indev,outdev, okfn,thresh) \

({int__ret; \

if ((__ret=nf_hook_thresh(pf, hook, &(skb),indev, outdev, okfn, thresh, 1)) == 1)\

__ret =(okfn)(skb); \

__ret;})

我们发现NF_HOOK_THRESH宏只增加了一个thresh参数，这个参数就是用来指定通过该宏去遍历钩子函数时的优先级，同时，该宏内部又调用了nf_hook_thresh函数：

static inline int nf_hook_thresh(int pf, unsignedint hook,

struct sk_buff **pskb,

struct net_device *indev,

struct net_device *outdev,

int (*okfn)(struct sk_buff *), int thresh,

int cond)

{undefined

if (!cond)

return 1;

#ifndef CONFIG_NETFILTER_DEBUG

if (list_empty(&nf_hooks[pf][hook]))

return 1;

#endif

return nf_hook_slow(pf, hook, pskb, indev, outdev,okfn, thresh);

}

这个函数又只增加了一个参数cond，该参数为0则放弃遍历，并且也不执行okfn函数；为1则执行nf_hook_slow去完成钩子函数okfn的顺序遍历(优先级从小到大依次执行)。

在net/netfilter/core.h文件中定义了一个二维的结构体数组，用来存储不同协议栈钩子点的回调处理函数。

struct list_head nf_hooks[NPROTO][NF_MAX_HOOKS];

其中，行数NPROTO为32，即目前内核所支持的最大协议簇；列数NF_MAX_HOOKS为挂载点的个数，目前在2.6内核中该值为8。nf_hooks数组的最终结构如下图所示。

![](https://pic1.zhimg.com/80/v2-1f4bbdf7808e2bb3c68399ec04afcbd0_720w.webp)

在include/linux/socket.h中IP协议AF_INET(PF_INET)的序号为2，因此我们就可以得到TCP/IP协议族的钩子函数挂载点为：

PRE_ROUTING： nf_hooks[2][0]

LOCAL_IN： nf_hooks[2][1]

FORWARD： nf_hooks[2][2]

LOCAL_OUT： nf_hooks[2][3]

POST_ROUTING： nf_hooks[2][4]

简单地说，数据报经过各个HOOK的流程如下：

数据报从进入系统，进行IP校验以后，首先经过第一个HOOK函数NF_IP_PRE_ROUTING进行处理；然后就进入路由代码，其决定该数据报是需要转发还是发给本机的；若该数据报是发被本机的，则该数据经过HOOK函数NF_IP_LOCAL_IN处理以后然后传递给上层协议；若该数据报应该被转发则它被NF_IP_FORWARD处理；经过转发的数据报经过最后一个HOOK函数NF_IP_POST_ROUTING处理以后，再传输到网络上。本地产生的数据经过HOOK函数NF_IP_LOCAL_OUT 处理后，进行路由选择处理，然后经过NF_IP_POST_ROUTING处理后发送出去。

- NF_IP_PRE_ROUTING (0)

数据报在进入路由代码被处理之前，数据报在IP数据报接收函数ip_rcv()（位于net/ipv4/ip_input.c，Line379）的最后，也就是在传入的数据报被处理之前经过这个HOOK。在ip_rcv()中挂接这个HOOK之前，进行的是一些与类型、长度、版本有关的检查。

经过这个HOOK处理之后，数据报进入ip_rcv_finish()（位于net/ipv4/ip_input.c，Line306），进行查路由表的工作，并判断该数据报是发给本地机器还是进行转发。

在这个HOOK上主要是对数据报作报头检测处理，以捕获异常情况。

涉及功能（优先级顺序）：Conntrack(-200)、mangle(-150)、DNAT(-100)

- NF_IP_LOCAL_IN (1)

目的地为本地主机的数据报在IP数据报本地投递函数ip_local_deliver()（位于net/ipv4/ip_input.c，Line290）的最后经过这个HOOK。

经过这个HOOK处理之后，数据报进入ip_local_deliver_finish()（位于net/ipv4/ip_input.c，Line219）

这样，IPTables模块就可以利用这个HOOK对应的INPUT规则链表来对数据报进行规则匹配的筛选了。防火墙一般建立在这个HOOK上。

涉及功能：mangle(-150)、filter(0)、SNAT(100)、Conntrack(INT_MAX-1)

- NF_IP_FORWARD (2)

目的地非本地主机的数据报，包括被NAT修改过地址的数据报，都要在IP数据报转发函数ip_forward()（位于net/ipv4/ip_forward.c，Line73）的最后经过这个HOOK。

经过这个HOOK处理之后，数据报进入ip_forward_finish()（位于net/ipv4/ip_forward.c，Line44）

另外，在net/ipv4/ipmr.c中的ipmr_queue_xmit()函数（Line1119）最后也会经过这个HOOK。（ipmr为多播相关，估计是在需要通过路由转发多播数据时的处理）

这样，IPTables模块就可以利用这个HOOK对应的FORWARD规则链表来对数据报进行规则匹配的筛选了。

涉及功能：mangle(-150)、filter(0)

- NF_IP_LOCAL_OUT (3)

本地主机发出的数据报在IP数据报构建/发送函数ip_queue_xmit()（位于net/ipv4/ip_output.c，Line339）、以及ip_build_and_send_pkt()（位于net/ipv4/ip_output.c，Line122）的最后经过这个HOOK。（在数据报处理中，前者最为常用，后者用于那些不传输有效数据的SYN/ACK包）

经过这个HOOK处理后，数据报进入ip_queue_xmit2()（位于net/ipv4/ip_output.c，Line281）

另外，在ip_build_xmit_slow()（位于net/ipv4/ip_output.c，Line429）和ip_build_xmit()（位于net/ipv4/ip_output.c，Line638）中用于进行错误检测；在igmp_send_report()（位于net/ipv4/igmp.c，Line195）的最后也经过了这个HOOK，进行多播时相关的处理。

这样，IPTables模块就可以利用这个HOOK对应的OUTPUT规则链表来对数据报进行规则匹配的筛选了。

涉及功能：Conntrack(-200)、mangle(-150)、DNAT(-100)、filter(0)

- NF_IP_POST_ROUTING (4)

所有数据报，包括源地址为本地主机和非本地主机的，在通过网络设备离开本地主机之前，在IP数据报发送函数ip_finish_output()（位于net/ipv4/ip_output.c，Line184）的最后经过这个HOOK。

经过这个HOOK处理后，数据报告入ip_finish_output2()（位于net/ipv4/ip_output.c，Line160）另外，在函数ip_mc_output()（位于net/ipv4/ip_output.c，Line195）中在克隆新的网络缓存skb时，也经过了这个HOOK进行处理。

涉及功能：mangle(-150)、SNAT(100)、Conntrack(INT_MAX)

同时我们看到，在2.6内核的IP协议栈里，从协议栈正常的流程切入到Netfilter框架中，然后顺序、依次去调用每个HOOK点所有的钩子函数的相关操作有如下几处：

1）、net/ipv4/ip_input.c里的ip_rcv函数。该函数主要用来处理网络层的IP报文的入口函数，它到Netfilter框架的切入点为：

NF_HOOK(PF_INET, NF_IP_PRE_ROUTING, skb, dev, NULL,ip_rcv_finish)

根据前面的理解，这句代码意义已经很直观明确了。那就是：如果协议栈当前收到了一个IP报文(PF_INET)，那么就把这个报文传到Netfilter的NF_IP_PRE_ROUTING过滤点，去检查在那个过滤点(nf_hooks[2][0])是否已经有人注册了相关的用于处理数据包的钩子函数。如果有，则挨个去遍历链表nf_hooks[2][0]去寻找匹配的match和相应的target，根据返回到Netfilter框架中的值来进一步决定该如何处理该数据包(由钩子模块处理还是交由ip_rcv_finish函数继续处理)。刚才说到所谓的“检查”。其核心就是nf_hook_slow()函数。该函数本质上做的事情很简单，根据优先级查找双向链表nf_hooks[][]，找到对应的回调函数来处理数据包：

struct list_head **i;

list_for_each_continue_rcu(*i, head) {undefined

struct nf_hook_ops *elem = (struct nf_hook_ops*)*i;

if (hook_thresh > elem->priority)

continue;

verdict = elem->hook(hook, skb, indev, outdev, okfn);

if (verdict != NF_ACCEPT) { …… }

return NF_ACCEPT;

}

上面的代码是net/netfilter/core.c中的nf_iterate()函数的部分核心代码，该函数被nf_hook_slow函数所调用，然后根据其返回值做进一步处理。

2）、net/ipv4/ip_forward.c中的ip_forward函数，它的切入点为：

NF_HOOK(PF_INET, NF_IP_FORWARD, skb, skb->dev,rt->[u.dst.dev](https://link.zhihu.com/?target=http%3A//u.dst.dev/),ip_forward_finish);

在经过路由抉择后，所有需要本机转发的报文都会交由ip_forward函数进行处理。这里，该函数由NF_IP_FOWARD过滤点切入到Netfilter框架，在nf_hooks[2][2]过滤点执行匹配查找。最后根据返回值来确定ip_forward_finish函数的执行情况。

3）、net/ipv4/ip_output.c中的ip_output函数，它切入Netfilter框架的形式为：

NF_HOOK_COND(PF_INET, NF_IP_POST_ROUTING, skb,NULL, dev,ip_finish_output,

!(IPCB(skb)->flags & IPSKB_REROUTED));

这里我们看到切入点从无条件宏NF_HOOK改成了有条件宏NF_HOOK_COND，调用该宏的条件是：如果协议栈当前所处理的数据包skb中没有重新路由的标记，数据包才会进入Netfilter框架。否则直接调用ip_finish_output函数走协议栈去处理。除此之外，有条件宏和无条件宏再无其他任何差异。

如果需要陷入Netfilter框架则数据包会在nf_hooks[2][4]过滤点去进行匹配查找。

4）、还是在net/ipv4/ip_input.c中的ip_local_deliver函数。该函数处理所有目的地址是本机的数据包，其切入函数为：

NF_HOOK(PF_INET, NF_IP_LOCAL_IN, skb, skb->dev,NULL,ip_local_deliver_finish);

发给本机的数据包，首先全部会去nf_hooks[2][1]过滤点上检测是否有相关数据包的回调处理函数，如果有则执行匹配和动作，最后根据返回值执行ip_local_deliver_finish函数。

5）、net/ipv4/ip_output.c中的ip_push_pending_frames函数。该函数是将IP分片重组成完整的IP报文，然后发送出去。进入Netfilter框架的切入点为：

NF_HOOK(PF_INET, NF_IP_LOCAL_OUT, skb, NULL,skb->dst->dev, dst_output);

对于所有从本机发出去的报文都会首先去Netfilter的nf_hooks[2][3]过滤点去过滤。一般情况下来来说，不管是路由器还是PC终端，很少有人限制自己机器发出去的报文。因为这样做的潜在风险也是显而易见的，往往会因为一些不恰当的设置导致某些服务失效，所以在这个过滤点上拦截数据包的情况非常少。当然也不排除真的有特殊需求的情况。

**整个Linux内核中Netfilter框架的HOOK机制可以概括如下：**

![](https://pic3.zhimg.com/80/v2-1bca0ee78ade539c7d87efefc5bd25e2_720w.webp)

在数据包流经内核协议栈的整个过程中，在一些已预定义的关键点上PRE_ROUTING、LOCAL_IN、FORWARD、LOCAL_OUT和POST_ROUTING会根据数据包的协议簇PF_INET到这些关键点去查找是否注册有钩子函数。如果没有，则直接返回okfn函数指针所指向的函数继续走协议栈；如果有，则调用nf_hook_slow函数，从而进入到Netfilter框架中去进一步调用已注册在该过滤点下的钩子函数，再根据其返回值来确定是否继续执行由函数指针okfn所指向的函数
