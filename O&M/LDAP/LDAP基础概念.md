# LDAP 基础概念

## 一、介绍

LDAP是轻量目录访问协议，英文全称是Lightweight Directory Access Protocol，一般都简称为LDAP。

OpenLDAP 默认以 Berkeley DB 作为后端数据库，Berkeley DB 数据库主要以散列的数据类型进行数据存储，如以键值对的方式进行存储。Berkeley DB 是一类特殊的数据库，主要作用于搜索、浏览、更新查询操作，一般用于一次写入数据、多次查询和搜索有很好的效果。Berkeley DB 数据库时面向查询进行优化，面向读取进行优化的数据库。Berkeley DB 不支持事务性数据库（MySQL、MariDB、Oracle 等）所支持的高并发的吞吐量以及复杂的事务操作。

通常我们在ldap中维护的数据大概会像如下目录树：

![](http://t.eryajf.net/imgs/2022/07/fac18341872b59e7.png)

基于这张图，我们来展开相关的概念介绍。

## 二、目录树概念

- `目录树`
  
  在一个目录服务系统中，整个目录信息集可以表示为一个目录信息树，树中的每个节点是一个条目(Entry)。

- `条目（Entry）`
  
  条目，也叫记录项，是LDAP中最基本的颗粒，就像字典中的词条，或者是数据库中的记录。通常对LDAP的添加、删除、更改、检索都是以条目为基本对象的。
  
  > LDAP目录的条目（entry）由属性（attribute）的一个聚集组成，并由一个唯一性的名字引用，即**专有名称**（**distinguished name**，DN）。例如，DN能取这样的值："`cn=group,dc=eryajf,dc=net`"。

- `对象类（ObjectClass）`
  
  对象类是属性的集合，LDAP预想了很多人员组织机构中常见的对象，并将其封装成对象类。比如人员（`person`）含有姓（`sn`）、名（`cn`）、电话(`telephoneNumber`)、密码(`userPassword`)等属性，单位职工(`organizationalPerson`)是人员(`person`)的继承类，除了上述属性之外还含有职务（`title`）、邮政编码（`postalCode`）、通信地址(`postalAddress`)等属性。

- `属性 (Attribute)`
  
  每个条目都可以有很多属性（Attribute），比如常见的人都有姓名、地址、电话等属性。每个属性都有名称及对应的值，属性值可以有单个、多个。

## 三、属性详解

要注意，如下标识的字段，即ldap中可查询交互使用的字段，其中原有的大小写方式，需与之一致。

### 1. 基础字段

- `dc (Domain Component)`
  
  域名的部分，其格式是将完整的域名分成几部分，如域名为`eryajf.net`变成`dc=eryajf,dc=net`。

- `ou（Organization Unit）`
  
  组织单位，组织单位可以包含其他各种对象(包括其他组织单元)。

- `cn （Common Name）`
  
  常用名称，可用作分组的名字，或者用户的全名。（级别最低对应个人/分组）

- `dn （Distinguished Name）`
  
  每一个条目都有一个唯一的标识名，dn在ldap中全局唯一，相当于该条目的唯一ID，如上边示例中的：`cn=group,dc=eryajf,dc=net`就是该条目的dn。

- `rdn （Relative dn）`
  
  一般指dn逗号最左边的部分，如`cn=group,dc=eryajf,dc=net`的rdn就是 `cn=group`。

- `Base DN`
  
  LDAP目录树的最顶部就是根，比如上边示例中的base dn为 `dc=eryajf,dc=net`。

- `description`
  
  在不同类别中，对应不同类别的说明信息，比如用户的说明信息，分组的说明信息。

### 2. 用户字段

用户字段依然会用到基础字段，并不代表这部分内容与上边的内容是隔离的。

- `objectClass`：`top`、`person`、`organizationalPerson`、`inetOrgPerson`、`posixAccount`

- `uid (User Id)`
  
  用户的用户名，通常为中文拼音，或者用邮箱地址的用户名部分。

- `sn （Surname）`
  
  用户的姓氏，对于中文环境下，可以直接用姓名填充。

- `givenName`
  
  用户的名字，不包含姓，对于中文语境下，可灵活运用该字段。

- `displayName`
  
  用户的显示名字，全名。

- `mail`
  
  用户的邮箱。

- `title`
  
  用户的职位。

- `employeeNumber`
  
  用户的员工ID，也可以理解为工号。

- `employeeType`
  
  用户在单位中的角色。

- `departmentNumber`
  
  用户所在部门的名称，通常为部门名，而非部门号。

- `businessCategory`
  
  描述业务的种类，在中文语境中可灵活定义。

- `userPassword`
  
  用户密码。

- `jpegPhoto`
  
  用户的个人资料照片。

- `photo`
  
  用户的照片，如上这两个字段都可以用。

- `postalAddress`
  
  用户的邮政地址，也可以直接认为是用户地址。

- `entryUuid`
  
  此用户专属的固定通用标识符，类似union_id，通常用不到。

- `objectSid`
  
  此用户专属的通用标识符，与 Windows 安全标识符兼容。

- `uidNumber`
  
  用户的 POSIX UID 号码。如果为用户设置了 POSIX ID，这里则会显示此号码。否则，这里会显示专属的固定标识符。

- `gidNumber`
  
  用户主要群组的 POSIX GID 号码。如果为用户设置了 POSIX GID，这里则会显示此号码。否则，则会显示与用户的 UID 相同的号码。
  
  > **注意**：您无法按 *uidNumber* 或 *gidNumber* 搜索用户，除非管理员使用Admin SDK API设置了用户的 posixAccounts 属性。

- `homeDirectory`
  
  用户的 POSIX 主目录。默认为`/home/<用户名>`。

- `loginShell`
  
  用户的 POSIX 登录 shell。默认为`/bin/bash`。

- `carLicense`
  
  车牌，通常用不上这个字段。

- `homePhone`
  
  家庭固定电话，通常用不上这个字段。

- `homePostalAddress`
  
  邮编，通常用不上这个字段。

- `roomNumber`
  
  房间号码，通常用不上这个字段。

- `secretary`
  
  秘书，通常用不上这个字段。

### 3. 分组字段

- `objectClass`：`top`、`groupOfNames`、`posixGroup`

- `displayName`
  
  用户可理解的群组显示名称。

- `description`
  
  用户可理解的群组详细说明。

- `gidNumber`
  
  群组的 POSIX GID 号码。这是固定的专属 ID，但无法通过此 ID 高效地查找群组。

- `entryUuid`
  
  此群组专属的固定通用标识符。

- `member`
  
  此群组中成员的完全符合条件的名称列表。

- `memberUid`
  
  此群组中成员的用户名列表。

## 参考

- https://wiki.eryajf.net/pages/aa0651

- https://segmentfault.com/a/1190000014683418

- [https://support.google.com/cloudidentity/answer/9188164?hl=zh-Hans(opens new window)](https://support.google.com/cloudidentity/answer/9188164?hl=zh-Hans)

- [https://datatracker.ietf.org/doc/html/rfc4519(opens new window)](https://datatracker.ietf.org/doc/html/rfc4519)

- https://xujiyou.work/DevOps/LDAP/LDAP%E5%85%A5%E9%97%A8.html
