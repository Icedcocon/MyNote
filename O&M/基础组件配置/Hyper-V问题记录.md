# Hyper-V

### 配置静态IP地址

##### Default Switch存在的问题

- Hyper-v会自带一个`Default Switch`交换机，这个交换机使用NAT网络，并不允许修改。

- Hyper-v的`Default Switch`交换机的IP每次重启都会变化，而且不能设成不变的。这样每次windows重启后都需要将`Default Switch`交换机的IP改成我们配置的网关的地址，虚拟机才能正常访问网路。

##### 配置虚拟交换机

- 打开hyper-v管理器，点击虚拟交换机管理器，点击新建虚拟网络交换机，选择外部网络，点击创建。

- 确保“允许管理操作系统共享此网络适器”打钩，否则WiFi网卡会被虚拟机独占，宿主机没有网络。

- 在虚拟机的设置界面，点击网络适配器，选择我们新建的虚拟交换机

- 关闭宿主机、虚拟机的网络防火墙

- 打开“网络和Internet设置”，点击“网络和共享中心”，在连接处可以找到新建的虚拟交换机，点击并选择详细信息，记录信息
  
  - （推测详细信息中IP地址为家庭路由器分配地址，且会与WLAN适配器保持一致，因此如果修改新建虚拟交换机的IP到一个错误网段，会引起WLAN适配器所属的宿主机断网）

- 点击属性，设置IPv4信息，将IP地址、子网掩码等设置成上面记录的详细信息中的内容。

##### 配置虚拟机静态IP地址

- 根据操作系统版本不同，查找对应资料
