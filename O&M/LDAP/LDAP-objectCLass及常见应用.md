# objectClass 及常见应用

## 一、理解

我们可以把objectCLass的属性值理解为是ldap中的一种模板，模板定义哪些信息可以存取，哪些信息不可以存储在目录树中。

因此，我们在实际使用过程中会发现，声明了不同的objectCLass时，可能添加某个字段就会报错了。

### 1. objectClass 的分类

- 结构型（structural）：如 person 和 oraganizationUnit
- 辅助型（auxiliary）：如 extensibleObject
- 抽象型（abstract）：如 top，抽象型的 objectClass 不能直接使用。

> 不同的 objectClass 间可能存在面向对象中的**继承**关系，因此不同 objectClass 的部分属性可能相同。抽象型可以理解为虚基类。
> 
> 结构性的 objectClass 又分为**用户**型和**分组**型。

### 2. objectCLass的列表

常见 objectCLass 的列表（PS：没那么常见，但需要了解）：

- alias
- applicationEntity
- dSA
- applicationProcess
- bootableDevice
- certificationAuthority
- certificationAuthority-V2
- country
- cRLDistributionPoint
- dcObject
- device
- dmd
- domain
- domainNameForm
- extensibleObject
- groupOfNames
- groupOfUniqueNames
- ieee802Device
- ipHost
- ipNetwork
- ipProtocol
- ipService
- locality
- dcLocalityNameForm
- nisMap
- nisNetgroup
- nisObject
- oncRpc
- organization
- dcOrganizationNameForm
- organizationalRole
- organizationalUnit
- dcOrganizationalUnitNameForm
- person
- organizationalPerson
- inetOrgPerson
- uidOrganizationalPersonNameForm
- residentialPerson
- posixAccount
- posixGroup
- shadowAccount
- strongAuthenticationUser
- uidObject
- userSecurityInformation

## 二、应用

实际应用中，其实根本不需要理解，或者认识那么多的概念，你只需要记住一种适合自己场景的objectCLass即可。

### 1. 用户

比如inetOrgPerson这个模板，就声明的这些属性我们就可以对照着[openLDAP的基础概念](https://wiki.eryajf.net/pages/aa0651/)里边的内容进行查阅分析了。

> 属性分为必须存在的属性和可选使用的属性。可以在 phpldapadmin 中查阅。

objectCLass就可以类比为数据库中提前约定设计好的表字段，只不过openLDAP已经默认集成了许多固定的模板，我们只需要选择其中的模板进行应用即可。

使用命令行参数创建用户属性方式如下：

```bash
# 创建一个用户 zhangsan
cat << EOF | ldapadd -x -D cn=admin,dc=eryajf,dc=net -w 123456
dn: uid=zhangsan,ou=people,dc=eryajf,dc=net
objectClass: inetOrgPerson
uid: zhangsan
cn: zhangsan
sn: zhang
displayName: 张三
userPassword: zhangsan
mobile: 15638888888
mail: zhangsan@eryajf.net
postalAddress: Hangzhou
businessCategory: 运维部
departmentNumber: 10
description: 测试用户
employeeNumber: 001
givenName: zhangsan
EOF
```

### 2. 分组

本例用到的分组分了两类：`organizationalUnit`和 `groupOfUniqueNames`。

#### 2.1 top（抽象类）

其中的 `top`是一个顶级的属性，我们先来看下它的定义。

因为top的必须项是一个属性，而我们创建的用户与分组都会附带对应的属性，因此这里的top事实上可以忽略，亦即不带。

#### 2.2 organizationalUnit

organizationalUnit必须项为ou，我们从基础概念中知道，ou是一个组织单位，组织单位可以包含其他各种对象(包括其他组织单元)。

所以这里ou的意义在于作为一个分组目录树的顶级组织，而非作为包含用户的实际分组。在go-ldap-admin的推荐用法中也是如此。

通过命令行创建一个`organizationalUnit`属性的条目：

```bash
cat << EOF | ldapadd -x -D "cn=admin,dc=eryajf,dc=net" -w 123456
dn: ou=group,dc=eryajf,dc=net
objectClass: organizationalUnit
ou: group
description: 分组的组织
EOF
```

#### 2.3 groupOfUniqueNames

可以看到必须项属性为cn，亦即此项objectCLass创建时必须包含属性cn。

另外一项必须项为：uniqueMember。

该属性代表用户在分组中的一个条目。

通过命令行创建一个`groupOfUniqueNames`属性的条目：

```bash
cat << EOF | ldapadd -x -D "cn=admin,dc=eryajf,dc=net" -w 123456
dn: cn=yunweibu,ou=group,dc=eryajf,dc=net
objectClass: groupOfUniqueNames
cn: yunweibu
description: 运维部
uniqueMember: cn=admin,dc=eryajf,dc=net
EOF
```

需要注意对应的属性以及字段，其中必填项如果没有，执行命令则会报错。

## 三、常用的 objectClass

### 0. 常见类的字段属性

- PosixAccount：https://ldapwiki.com/wiki/PosixAccount
- PosixGroup：https://ldapwiki.com/wiki/PosixGroup
- shadowAccount：https://ldapwiki.com/wiki/shadowAccount

### 1. top

#### 1.1 描述

| Description: **top of the superclass chain** |
| -------------------------------------------- |
| Type: **abstract**                           |
| Inherits from: **(none)**                    |
| Parent to: **all**                           |

#### 1.2 Required Attributes

- objectClass

#### 1.3 Optional Attributes

- none

### 2. organization

#### 2.1 描述

| Description: **RFC2256: an organization** |
| ----------------------------------------- |
| Type: **structural**                      |
| Inherits from: **top**                    |
| Parent to: **(none)**                     |

#### 2.2 Required Attributes

- o

#### 2.3 Optional Attributes

- businessCategory
- description
- destinationIndicator
- facsimileTelephoneNumber
- internationaliSDNNumber
- l
- physicalDeliveryOfficeName
- postOfficeBox
- postalAddress
- postalCode
- preferredDeliveryMethod
- registeredAddress
- searchGuide
- seeAlso
- st
- street
- telephoneNumber
- teletexTerminalIdentifier
- telexNumber
- userPassword
- x121Address

### 3. organizationUnit

#### 3.1 描述

| Description: **RFC2256: an organizational unit** |
| ------------------------------------------------ |
| Type: **structural**                             |
| Inherits from: **top**                           |
| Parent to: **(none)**                            |

#### 3.2 Required Attributes

- ou

#### 3.3 Optional Attributes

- businessCategory
- description
- destinationIndicator
- facsimileTelephoneNumber
- internationaliSDNNumber
- l
- physicalDeliveryOfficeName
- postOfficeBox
- postalAddress
- postalCode
- preferredDeliveryMethod
- registeredAddress
- searchGuide
- seeAlso
- st
- street
- telephoneNumber
- teletexTerminalIdentifier
- telexNumber
- userPassword
- x121Address

### 4. inetOrgPerson

### 5. posixAccount

### 6. dcObject

### 7. device

### 8. pwdPolicy

### 9. pwdPolicyChecker

## 参考资料

- https://wiki.eryajf.net/pages/ea10fa/#%E7%90%86%E8%A7%A3
