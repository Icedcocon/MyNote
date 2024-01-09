# 网络文件系统(NFS)

### 一、NFS简介

- NFS（Network File System）可以挂载远程主机的目录并访问，类似文件服务器。
  
  - NFS服务用于unix-like系统间，但在unix-like和windows系统之间要用samba。
  
  - 用户/应用程序通过NFS可以访问远程系统上的文件，就像本地文件一样。

- NFS传输数据时使用的**端口随机**，但限制**端口号小于1024**，客户端调用RPC获取端口。

- **RPC（Remote Procedure Call）远程过程调用**
  
  - 定义了一种与系统无关的方法来实现进程间通信，通过portmap设定映射端口。
  
  - NFS Client发起请求，要先先通过**portmap得到端口**(port)

- NFS的优点：
  
  - 本地工作站可以使用更少的磁盘空间，常用数据可以被保存在另一台机器上。
  
  - 用户目录可以在NFS服务器上设置并使其在整个网络上可用。
  
  - 可以减少网络上移动存储的数量，USB设备、硬盘等可以被网络上其它机器使用。

### 二、与NFS相关的几个文件和命令

- `/etc/exports`
  
  - 对NFS服务的访问控制，exports枚举有权访问NFS服务器上文件系统的主机名。

- `/sbin/exportfs`
  
  - 管理维护NFS导出表（exports），可通过exportfs操作`/etc/exports`文件
  
  - 导出主表存放在`/var/lib/nfs/etab`文件，当客户端发送请求时，rpc.mountd进程会读取该文件
  
  - 导出主表是`exportfs -s`读取`/etc/exports`和`/etc/exports.d/*.exports`文件来初始化的。
  
  - 也可以使用exportfs命令直接向主表中添加或删除导出项

- `/usr/sbin/showmount` 
  
  - 上面的文件主要用在NFS Server端，而showmount则主要用在Client端，showmount可以用來查看NFS共享的目录资源。

- /var/lib/nfs/xtab
  
  - NFS的记录文档：通过它可以查看有哪些Client连接到NFS主机的记录。

下面这几个并不直接负责NFS，实际上它们是负责所有的RPC。

- /etc/default/portmap
  
  - 实际上，portmap负责映射所有的RPC服务端口，它的内容非常非常之简单。

- /etc/hosts.deny
  
  - 设定拒绝portmap服务的主机，即禁止访问的客户端IP列表。

- /etc/hosts.allow
  
  - 设定允许portmap服务的主机，即允许访问的客户端IP列表。

### 三、常用指令

- `exportfs -a`： 将`/etc/exports`和`/etc/exports.d/*.exports`中的导出项添加到文件`/var/lib/nfs/etab`

- `exportfs -r`： 使/etc/exports 配置生效

- `exportfs -ua`： 清空`/var/lib/nfs/etab`，用于关闭nfs服务时

- `exportfs -v`： 输出当前所有已导出目录的列表， -v 显示详细参数

- `exportfs -o insecure_locks client:/usr/tmp`： 导出目录/usr/tmp给client主机，且允许客户端发送不安全的文件锁请求

- `exportfs -u client:/usr/tmp`： 卸载目录/usr/tmp

- `exportfs  *:/home`： 所有用户均可访问/home目录但只有只读权限

- `exportfs  -o async *:/home/`： 允许匿名访问

- `exportfs  -o async 192.168.1.15:/home`： 指定IP可访问

### 四、常用选项

| 参数               | 效果                              |
| ---------------- | ------------------------------- |
| ro               | 只读访问                            |
| rw               | 读写访问                            |
| sync             | 同步写入硬盘                          |
| async            | 暂存内存                            |
| secure           | NFS通过1024以下的安全TCP/IP端口发送        |
| insecure         | NFS通过1024以上的端口发送                |
| wdelay           | 多个用户对共享目录进行写操作时，则按组写入数据（默认）     |
| no_wdelay        | 多个用户对共享目录进行写操作时，则立即写入数据         |
| hide             | 不共享其子目录                         |
| no_hide          | 共享其子目录                          |
| subtree_check    | 强制NFS检查父目录的权限                   |
| no_subtree_check | 不检查父目录权限                        |
| all_squash       | 任何访问者，都转为匿名用户                   |
| root_squash      | root用户访问此目录映射成如anonymous用户一样的权限 |
| no_root_squash   | root用户访问此目录，具有root操作权限          |

### 三、NFS安装

在主机上安装NFS服务软件，因为Debian/Ubuntu上默认是没有安装的。

1、安装端口映射器portmap（可选）
$ sudo apt-get install portmap

2、在终端提示符后键入以下命令安装NFS服务器
$ sudo apt-get install nfs-kernel-server

3、安装NFS客户端（可选）
$ sudo apt-get install nfs-common

注意：nfs- kernel-server和nfs-common都依赖于portmap。另外，在一些文档中提出还需要使用apt-get来手动安装NFS的客户端 nfs-common，以及端口映射器portmap，但其实这是没有必要的，因为在安装nfs-kernel-server时，apt会自动把它们安装 好。

这样，宿主机就相当于NFS Server。同样地，目标系统作为NFS的客户端，需要安装NFS客户端程序。如果是Debian/Ubuntu系统，则需要安装nfs-common（第3步）。

也可以使用`apt-get install nfs-utils`进行安装

四、NFS配置

1、配置portmap
方法1：编辑/etc/default/portmap，将"-i 127.0.0.1"去掉；
方法2：$ sudo dpkg-reconfigure portmap，出现“正在设定portmap”软件包设置界面，对Should portmap be bound to the loopback address？选择“否(No)”。

2、配置/etc/hosts.deny
禁止任何host（主机）能和你的NFS服务器进行NFS连接。在该文件中加入：

### NFS DAEMONS

portmap:ALL
lockd:ALL
mountd:ALL
rquotad:ALL
statd:ALL

3、配置/etc/hosts.allow
允许那些你想要的主机和你的NFS服务器建立连接。

下列步骤将允许任何IP地址以192.168.1开头的主机连接到NFS服务器上，具体要看你目标板的端口地址，也可以指定特定的IP地址。在该文件中加入：

### NFS DAEMONS

portmap: 192.168.1.
lockd: 192.168.1.
rquotad: 192.168.1.
mountd: 192.168.1.
statd: 192.168.1.

通过/etc/hosts.deny和/etc/hosts.allow设置对portmap的访问，采用这两个配 置文件有点类似"mask"的意思。先在/etc/hosts.deny中禁止所有用户对portmap的访问，再在/etc/hosts.allow中 允许某些用户对portmap的访问。

然后重启portmap daemon：
$ sudo /etc/init.d/portmap restart

4、配置/etc/exports

（1）共享的NFS目录在/etc/exports中列出，这个文件控制对目录的共享（NFS挂载目录及权限由该文件定义），书写规则是每个共享为一行）。

格式：[共享目录] [主机名或IP](参数,参数...)
第一个参数是要让客户机访问的目录，第二个是你允许的主机IP，最后的()内是访问控制方式。

注意：客户端可以使用主机名或者IP地址指定，在主机名中可以使用通配符(*)，IP地址后也可以跟掩码段(/24)，但出于安全原因这种情况应该尽量避免。客户端的说明后可在圆括号中加入一系列参数。很重要的一点，不要在最后一个客户端声明的后面留下任何空白或者没关闭括号，因为空白都被解释成客户端的分隔符。

例如我要将/opt/FriendlyARM/mini2440/root_nfs目录让用户的IP共享，则在该文件末尾添加下列语句：
/opt/FriendlyARM/mini2440/root_nfs *(rw,sync,no_root_squash)

其中：
/opt/FriendlyARM/mini2440/root_nfs 表示NFS共享目录，它可以作为开发板的根文件系统通过NFS挂接；

* 表示所有的客户机都可以挂接此目录；
  rw 表示挂接此目录的客户机对该目录有读写的权力；
  sync 表示所有数据在请求时写入共享，即数据同步写入内存和硬盘；
  no_root_squash 表示允许挂接此目录的客户机享有该主机的root身份。

注意：可以用主机名来代替*，尽量指定主机名以便使那些不想其访问的系统不能访问NFS挂载的资源。另外，最好加上sync, 否则$ sudo exportfs -r时会给出警告，sync是NFS的默认选项。

（2）下面是一些NFS共享的常用参数：
ro 只读访问
rw 读写访问
sync 所有数据在请求时写入共享
async NFS在写入数据前可以相应请求
secure NFS通过1024以下的安全TCP/IP端口发送
insecure NFS通过1024以上的端口发送
wdelay 如果多个用户要写入NFS目录，则归组写入（默认）
no_wdelay 如果多个用户要写入NFS目录，则立即写入，当使用async时，无需此设置
hide 在NFS共享目录中不共享其子目录
no_hide 共享NFS目录的子目录
subtree_check 如果共享/usr/bin之类的子目录时，强制NFS检查父目录的权限（默认）
no_subtree_check 和上面相对，不检查父目录权限
all_squash 共享文件的UID和GID映射匿名用户anonymous，适合公用目录
no_all_squash 保留共享文件的UID和GID（默认）
root_squash root用户的所有请求映射成如anonymous用户一样的权限（默认）
no_root_squash root用户具有根目录的完全管理访问权限
anonuid=xxx 指定NFS服务器/etc/passwd文件中匿名用户的UID
anongid=xxx 指定NFS服务器/etc/passwd文件中匿名用户的GID

（3）查看NFS Server的export list：
$ sudo showmount -e

若更改了/etc/exports，运行以下命令进行更新：
$ sudo exportfs -r

然后重启NFS服务：
$ sudo /etc/init.d/nfs-kernel-server restart

五、启动和停止NFS服务

1、启动NFS的方法和启动其他服务器的方法类似，首先需要启动portmap和NFS这两个服务，并且portmap服务一定要先于NFS服务启动。
$ sudo /etc/init.d/portmap start
$ sudo /etc/init.d/nfs-kernel-server start

2、停止NFS服务
在停止NFS服务的时候，需要先停止NFS服务再停止portmap服务，如果系统中还有其他服务需要使用portmap服务，则可以不停止portmap服务。
$ sudo /etc/init.d/nfs-kernel-server stop
$ sudo /etc/init.d/portmap stop

3、重新启动portmap和NFS服务
$ sudo /etc/init.d/portmap restart
$ sudo /etc/init.d/nfs-kernel-server restart

4、检查portmap和NFS服务状态
$ sudo /etc/init.d/portmap status（不知原文是否有误，我的ubuntu上portmap貌似没status这个命令参数）
$ sudo /etc/init.d/nfs-kernel-server status

5、设置自动启动NFS服务

（1）检查NFS的运行级别：
$ sudo chkconfig --list portmap      （我的电脑也没chconfig这个工具，不过没多大关系，如果有问题再回头）
$ sudo chkconfig --list nfs-kernel-server

（2）在实际使用中，如果每次开启计算机之后都手工启动NFS服务是非常麻烦的，此时可以设置系统在指定的运行级别自动启动portmap和NFS服务。
$ sudo chkconfig --level 235 portmap on  （由于没有chkconfig工具，所以我就用services-admin（也就是图形界面的“系统─>“服务”）来代替，至于level就不管了，用默认设置）
$ sudo chkconfig --level 235 nfs-kernel-server on

六、NFS客户端配置（NFS测试）

1、在NFS服务器启动后，还需要检查Linux服务器的防火墙设置（一般需要关闭防火墙服务），确保没有屏蔽 NFS使用的端口和允许通信的主机，主要是检查Linux服务器iptables、ipchains等选项的设置，以及/etc/hosts.deny， /etc/hosts.allow文件。通常都是在内部局域网中进行开发，再安装系统时最好不要安装防火墙等网络安全软件，以方便使用时的配置。

如果你有防火墙，请确保32771、111和2049端口保持开放。

2、手动挂载
使用mount命令来挂载其他机器共享的NFS目录。

格式：$ sudo mount [Server IP]:/[share dir] [local mount point]

例如：
$ sudo mount -t nfs [-o nolock] localhost:/opt/FriendlyARM/mini2440/root_nfs /mnt/root_nfs 或
$ sudo mount -t nfs -o nolock 192.168.1.101:/opt/FriendlyARM/mini2440/root_nfs /mnt/root_nfs

其中，localhost可以是具体的IP地址，同时挂载点/mnt/root_nfs目录必须已经存在，而且在/mnt/root_nfs目录中没有文件或子目录。

3、自动挂载

（1）另一个挂载其他机器的NFS共享的方式就是在/etc/fstab文件中添加一行，该行必须指明NFS服务器的主机名、服务器输出的目录名以及挂载NFS共享的本机目录，同时必须是根用户才能修改/etc/fstab文件（目标板上可能没有fstab，需要自己创建一个）。

格式(参考PC上的fstab)：host_ip:/nfs_path /target_path nfsrsize=8192,wsize=8192,timeo=14,intr,nolock  0   0

注意：可以根据实际情况修改NFS服务器共享文件夹"servername.mydomain.com:/usr/local/pub"和在本机的挂载点"/pub"，同时挂载点/pub在客户端机器上必须存在。

（2）NFS常见挂载参数:

intr 允许通知中断一个NFS调用。当服务器没有应答需要放弃的时候有用处。

timeo 如果超时，客户端等待的时间，以十分之一秒计算
retrans 超时尝试的次数
bg 后台挂载（很有用）
hard 如果server端没有响应，那么客户端一直尝试挂载
rsize 读块大小
wsize 写块大小

4、使用autofs来挂载NFS

（1）挂载NFS共享的第三种方法是使用autofs，它使用automount守护进程来管理挂载点，只在文件系统被访问时才动态地挂载。

autofs访问主映射配置文件/etc/auto.master来决定要定义哪些挂载点，然后使用适用于各个挂载 点的参数来启动automount守护进程。主映射配置中的每一行都定义一个挂载点，一个分开的映射文件定义在该挂载点下要挂载的文件系统。如/etc /auto.misc文件可能会定义/misc目录中的挂载点，这种关系在/etc/auto.master文件中会被定义。

（2）/etc/auto.master文件中的每个项目都有3个字段，第1个字段是挂载点；第2个字段是映射文件的位置；第3个字段可选，可以包括超时数值之类的信息。

例如：要在机器上的/misc/myproject挂载点上挂载远程机penguin.example.net中的/project52目录。
在/etc/auto.master文件中添加以下行：
/misc /etc/auto.misc --timeout 60
在/etc/auto.misc文件中添加以下行：
myproject -rw,soft,intr,rsize=8192,wsize=8192 penguin.example.net:/proj52

/etc/auto.misc中的第1个字段是/misc子目录的名称，该目录被automount动态地创建，它不应该在客户端机器上实际存在；第2个字段包括挂载选项，如rw代表读写访问权，第3个字段是要导出的NFS的位置，包括主机名和目录。

（3）autofs是一种服务，要启动这项服务，在shell提示下键入以下命令：
$ sudo /sbin/service autofs restart
要查看活跃的挂载点，在shell提示下键入以下命令：
$ sudo /sbin/service autofs status
如果在autofs运行时修改了/etc/auto.master配置文件，则必须在shell提示下键入以下命令来通知automount守护进程重新载入配置文件：
$ sudo /sbin/service autofs reload

5、可以运行df命令查看是否挂载成功：
$ sudo df

取消挂载的命令如下：
$ sudo umount /mnt/root_nfs

七、目标板NFS配置操作

主机IP：192.168.1.101
目标板IP：192.168.1.230

将USB转串口连接上，在终端输入minicom与板子连起，作为“超级终端”使用。

启动目标板并连通网络后，首先查看目标板kernel自身是否支持NFS，在minicom中输入cat /proc/filesystems命令查看其中是否有NFS一行，若没有则表示内核不支持NFS，就需要重新编译和烧写内核；有则OK，接下来就可以直接进行mount操作了。

具体命令是：

# mount -t nfs -o nolock 192.168.1.101:/opt/FriendlyARM/mini2440/root_nfs /mnt/root_nfs

无任何提示表示成功，这时可以进入/mnt/root_nfs目录，对文件进行cp、mv等操作。

但是如果使用命令mount -t nfs 192.168.1.101:/opt/FriendlyARM/mini2440/root_nfs /mnt/root_nfs，则会有如下的错误提示（也就是省去了"-o nolock"）：

# mount -t nfs 192.168.1.101:/opt/FriendlyARM/mini2440/root_nfs /mnt/root_nfs

portmap: server localhost not responding, timed out
RPC: failed to contact portmap (errno -5).
portmap: server localhost not responding, timed out
RPC: failed to contact portmap (errno -5).
lockd_up: makesock failed, error=-5
portmap: server localhost not responding, timed out
RPC: failed to contact portmap (errno -5).

这时如果使用ls /mnt/root_nfs命令查看该目录内容时，你会发现此时NFS确确实实已经挂载成功了。

然后取消挂载的时候会出现如下的错误提示：

# umount /mnt/root_nfs/

lockd_down: no lockd running.

exportfs和它的搭档程序rpc.mountd以两种模式之一工作：传统模式用于Linux Kernel 2.4以及之前 的版本，新模式应用于内核2.6和之后的版本，新模式提供了nfsd虚拟文件系统，并将它们挂载在/proc/fs/nfsd或/proc/fs/nfs上。在kernel 2.6之后，如果未挂载nfsd虚拟文件系统，则表示工作在 传统模式下。
在新模式下，exportfs不会给内核任何信息，而是通过文件/var/lib/nfs/etab将信息交给rpc.mountd，然后rpc.mountd就可以按需管理关于导出信息的内核请求。  

传统模式下，exports文件只能识别主机，不能识别网段和网络组，且会直接将导出信息交给内核中的导出表，同时写入到文件/var/lib/nfs/etab文件中。
