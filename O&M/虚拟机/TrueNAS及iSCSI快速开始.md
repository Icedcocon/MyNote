# TrueNAS快速开始

## 存储池

磁盘  -> VDEV -> 存储池

TrueNAS存储顺序为内存->缓存存储池->数据存储池。

一个存储池可以由多个（相同类型的）Vdev组成，而Vdev可以有多种类型。

### 1. Vdev有以下六种类型：

#### 1.1 Data

基础Vdev，用于存储数据，一个存储池至少有一个Data Vdev。

可以在一个池里添加多个Data Vdev，多个Data Vdev可以组成相关阵列，而一个Data Vdev又可以由多块硬盘组成的阵列构成。

#### 1.2 Cache

ZFS L2ARC读取缓存可与快速设备一起使用以加速读取操作。相当于二级缓存，保存从内存里面调出的数据，下次直接从固态硬盘中调出。建议64G内存以上的用户使用此Vdev，不要超过内存的5倍。推荐用固态硬盘当缓存Vdev，容量不需太大，64G存最好不要超过300G容量，多了反而会增加内存的消耗。

> How Does L2ARC Work?
> 
> 当系统收到读请求时，ZFS使用ARC (RAM)来处理这些请求。当ARC满了，并且有L2ARC驱动器分配给ZFS池时，ZFS使用L2ARC来处理从ARC溢出的读请求。这减少了使用较慢的硬盘驱动器，从而提高了系统性能。

#### 1.3 Log

ZFS日志设备，提高同步写速度，日志设备的最小大小与池中每个设备的最小大小 (64 MB) 相同。可能存储在日志设备中的相关的数据量相对较小。提交日志事务（系统调用）时将释放日志块。日志设备的最大大小应大约为物理内存大小的 1/2，因为这是可存储的最大潜在相关的数据量。例如，如果系统的物理内存为 16 GB，请考虑 8 GB 的最大日志设备大小。

ZFS intent log（ZIL）通常被称为日志，其主要目的是数据完整性。ZIL的存在是为了跟踪正在进行的同步写操作。如果系统崩溃或断电，ZIL可以重放操作。当您在电源故障时丢失一个标准的系统缓存时，一个ZIL在系统重新启动时仍然存在。

ZFS数据池使用一个存储在磁盘上的ZIL来记录同步写入，然后再刷新到存储中的最终位置。这意味着同步写操作以存储池的速度进行，并且必须写入存储池两次或两次以上(取决于磁盘冗余)。

#### 1.4 Hot Spare

热备盘是指当主用磁盘故障时，预留插入Data vdev的磁盘。热备盘用于临时替换故障驱动器，以防止出现更大的池和数据丢失的情况。 当新硬盘替换故障硬盘时，热备盘恢复为非激活状态，重新作为热备盘使用。 当故障驱动器仅从池中分离时，临时热备盘将被提升为Data vdev的成员，不再作为热备盘可用。

#### 1.5 Metadata

用于创建Fusion Pools的特殊分配类，以提高元数据和小块 i/o 性能。

#### 1.6 Dedup

Dedup vde用于存储ZFS池中的重复删除数据。需要为每X TiB的通用存储分配X GiB。例如，1 GiB的Dedup vdev容量对应1 TiB的Data vdev可用容量。

### 2. Vdev布局

根据特定的池用例，添加到vdev中的磁盘以不同的布局排列。不支持将多个具有不同布局的vdev添加到池中。当需要不同的vdev布局时，创建一个新的池。例如，pool1中有一个镜像布局的数据vdev，新创建一个poo2，将raid-z布局的vdev添加到pool2中。

#### 2.1 Stripe

条带类型vdev布局下的每个磁盘都用于存储数据。至少需要1块硬盘，且数据无冗余。

**注意：不要使用Stripe类型的vdev来存储关键数据!单个磁盘故障将导致vdev中所有数据丢失。**

#### 2.2 Mirror

镜像类型vdev中每个磁盘的数据完全相同。要求至少2块硬盘，冗余度最高，但相对的可使用的容量也最少。

#### 2.3 RAIDZ1

RAIDZ1使用一块磁盘进行奇偶校验，其他磁盘全部用来存储数据。至少需要3块硬盘。

#### 2.4 RAIDZ2

RAIDZ2使用两块磁盘进行奇偶校验，其他磁盘全部用来存储数据。至少需要4块硬盘。

#### 2.5 RAIDZ3

RAIDZ3使用三块磁盘进行奇偶校验，其他磁盘全部用来存储数据。至少需要5块硬盘。

## 驱动安装

### 0. 开启开发者模式

truenas scale 从24.04 beta1开始，/usr/bin下的东西变成了只读的了。不再是 `chmod +x /usr/bin/*`来解开apt了。

这里需要手动开启开发者模式：

```bash
install-dev-tools
```

用root用户，在shell下输入上面的命令开启

```bash
## Encountered Read-only file system problem, unable to create anything
```

如果你执行什么命令，出现了系统只读问题。执行下面命令：

```bash
zfs get readonly
```

查看哪些路径是只读的。需要把 on改成off

```bash
zfs set readonly=off [dataset]
```

例如 `zfs set readonly=off boot-pool/ROOT/24.04-BETA.1`

### 1. 10G网卡驱动

```bash
wget https://downloadmirror.intel.com/832293/ixgbe-5.21.5.tar.gz
```

## 参考资料

- 存储池

https://www.cnblogs.com/xzy186/p/16354498.html

- iSCSI

https://littlenewton.uk/2023/05/tutorial-iscsi-configuration-on-truenas-and-clients/

- TrueNAS安装万兆（82599）网卡驱动

[万兆网卡-驱动安装 - 雨中漫步](https://zoe.red/2024/640.html)
