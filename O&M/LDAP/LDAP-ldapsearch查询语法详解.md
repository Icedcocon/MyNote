# ldapsearch查询语法详解

一般情况下，命令行中我们使用ldapsearch来进行搜索。

## 一、简单搜索

一般情况下，你可以直接运行如下命令执行搜索：

```bash
$ ldapsearch -x -b <search_base> -H <ldap_host> -D <bind_dn> -w 123456a? -W ...
```

- `-x`：表示简单的身份认证。
- `-b`：指定搜索的DC。
- `-H`：指定搜索的主机URL，如果你是在LDAP服务器上，则不需要带这个参数。比如我这里为 `ldap://192.168.31.76:389`
- `-D`：绑定的DN。
- `-w`：绑定的DN的密码。

如通过如下命令可以查询：

```bash
$ ldapsearch -x -b "dc=eryajf,dc=net" -H ldap://192.168.31.76:389 -D "cn=admin,dc=eryajf,dc=net"  -W


# eryajf.net
dn: dc=eryajf,dc=net
objectClass: top
objectClass: dcObject
objectClass: organization
o: eryajf.net
dc: eryajf

# admin, eryajf.net
dn: cn=admin,dc=eryajf,dc=net
objectClass: simpleSecurityObject
objectClass: organizationalRole
cn: admin
description: LDAP administrator
userPassword:: e1NTSEF9SXg2Zms0UnBLVVl4Y1JaVFZrZFNZN0tiVkZ1OGRYckQ=

# people, eryajf.net
dn: ou=people,dc=eryajf,dc=net
ou: people
description:: 55So5oi35qC555uu5b2V
objectClass: organizationalUnit

# dingtalkroot, eryajf.net
dn: ou=dingtalkroot,dc=eryajf,dc=net
ou: dingtalkroot
description:: 6ZKJ6ZKJ5qC56YOo6Zeo
objectClass: top
objectClass: organizationalUnit

# wecomroot, eryajf.net
dn: ou=wecomroot,dc=eryajf,dc=net
ou: wecomroot
description:: 5LyB5Lia5b6u5L+h5qC56YOo6Zeo
objectClass: top
objectClass: organizationalUnit

# feishuroot, eryajf.net
dn: ou=feishuroot,dc=eryajf,dc=net
ou: feishuroot
description:: 6aOe5Lmm5qC56YOo6Zeo
objectClass: top
objectClass: organizationalUnit

# search result
search: 2
result: 0 Success

# numResponses: 7
# numEntries: 6
```

## 二、使用过滤器搜索

我们可以通过在搜索命令末尾添加过滤条件，来实现符合条件的搜索。

```bash
$ ldapsearch <previous_options> "(object_type)=(object_value)" <optional_attributes>
```

其中的条件可以添加多个，并且支持一定的逻辑运算符，接下来一一介绍。

### 1. 查找目录树中的所有对象

通过添加 `"objectclass=*"`的条件，我们可以检索到所有的对象信息：

```bash
$ ldapsearch -x -b "dc=eryajf,dc=net" -H ldap://192.168.31.76:389 -D "cn=admin,dc=eryajf,dc=net"  -W "objectclass=*"
```

执行结果与上边默认的一致。

### 2. 缩小查询范围

比如上边有四个ou对应用户，钉钉，飞书，企业微信的组织，我们可以通过如下条件，将这四个组织过滤出来：

```bash
$ ldapsearch -x -b "dc=eryajf,dc=net" -H ldap://192.168.31.76:389 -D "cn=admin,dc=eryajf,dc=net"  -W "objectclass=organizationalUnit"

# people, eryajf.net
dn: ou=people,dc=eryajf,dc=net
ou: people
description:: 55So5oi35qC555uu5b2V
objectClass: organizationalUnit

# dingtalkroot, eryajf.net
dn: ou=dingtalkroot,dc=eryajf,dc=net
ou: dingtalkroot
description:: 6ZKJ6ZKJ5qC56YOo6Zeo
objectClass: top
objectClass: organizationalUnit

# wecomroot, eryajf.net
dn: ou=wecomroot,dc=eryajf,dc=net
ou: wecomroot
description:: 5LyB5Lia5b6u5L+h5qC56YOo6Zeo
objectClass: top
objectClass: organizationalUnit

# feishuroot, eryajf.net
dn: ou=feishuroot,dc=eryajf,dc=net
ou: feishuroot
description:: 6aOe5Lmm5qC56YOo6Zeo
objectClass: top
objectClass: organizationalUnit

# search result
search: 2
result: 0 Success

# numResponses: 5
# numEntries: 4
```

在过滤条件的后边，我们可以指定关心的属性进行查询：

```bash
$ ldapsearch -x -b "dc=eryajf,dc=net" -H ldap://192.168.31.76:389 -D "cn=admin,dc=eryajf,dc=net"  -W "objectclass=organizationalUnit" dn ou

# people, eryajf.net
dn: ou=people,dc=eryajf,dc=net
ou: people

# dingtalkroot, eryajf.net
dn: ou=dingtalkroot,dc=eryajf,dc=net
ou: dingtalkroot

# wecomroot, eryajf.net
dn: ou=wecomroot,dc=eryajf,dc=net
ou: wecomroot

# feishuroot, eryajf.net
dn: ou=feishuroot,dc=eryajf,dc=net
ou: feishuroot

# search result
search: 2
result: 0 Success

# numResponses: 5
# numEntries: 4
```

## 三、添加运算符

### 1. 逻辑与

ldapsearch使用`&`来表示逻辑与的运算，它的查询语法格式如下：

```bash
$ ldapsearch <previous_options> "(&(<条件_1>)(<条件_2>)...)"
```

注意上边的查询语法格式不要弄错。

比如，我们可以通过如下两个条件，来定位到feishu(只是为了展示语法，不必纠结场景用法)：

```bash
$ ldapsearch -x -b "dc=eryajf,dc=net" -H ldap://192.168.31.76:389 -D "cn=admin,dc=eryajf,dc=net"  -W "(&(objectclass=organizationalUnit)(ou=feishu))"
Enter LDAP Password:

# feishuroot, eryajf.net
dn: ou=feishuroot,dc=eryajf,dc=net
ou: feishu
ou: feishuroot
description:: 6aOe5Lmm5qC56YOo6Zeo
objectClass: top
objectClass: organizationalUnit

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
```

### 2. 逻辑或

ldapsearch使用`|`来表示逻辑或的运算，它的查询语法格式如下：

```bash
$ ldapsearch <previous_options> "(|(<条件_1>)(<条件_2>)...)"
```

比如，我们可以通过如下两个条件，来查询出飞书与钉钉的信息：

```bash
$ ldapsearch -x -b "dc=eryajf,dc=net" -H ldap://192.168.31.76:389 -D "cn=admin,dc=eryajf,dc=net"  -W "(|(ou=dingtalkroot)(ou=feishuroot))"
Enter LDAP Password:


# dingtalkroot, eryajf.net
dn: ou=dingtalkroot,dc=eryajf,dc=net
ou: dingtalkroot
description:: 6ZKJ6ZKJ5qC56YOo6Zeo
objectClass: top
objectClass: organizationalUnit

# feishuroot, eryajf.net
dn: ou=feishuroot,dc=eryajf,dc=net
ou: feishu
ou: feishuroot
description:: 6aOe5Lmm5qC56YOo6Zeo
objectClass: top
objectClass: organizationalUnit

# search result
search: 2
result: 0 Success

# numResponses: 3
# numEntries: 2
```

### 3. 逻辑非

ldapsearch使用!来表示逻辑非的运算，他的查询语法格式如下：

```bash
$ ldapsearch <previous_options> "(!(<条件_1>))"
```

1  

比如，查询ou不是钉钉的方法如下：

```bash
$ ldapsearch -x -b "dc=eryajf,dc=net" -H ldap://192.168.31.76:389 -D "cn=admin,dc=eryajf,dc=net"  -W "(!(ou=dingtalkroot))"
```

注意逻辑非不能直接多条件，如果想要多个条件，那么需要与其他逻辑进行嵌套使用，比如查询ou不是钉钉或者飞书，则可以用如下条件：

```bash
$ ldapsearch -x -b "dc=eryajf,dc=net" -H ldap://192.168.31.76:389 -D "cn=admin,dc=eryajf,dc=net"  -W "(!(|(ou=dingtalkroot)(ou=feishuroot)))"
```

注意如上嵌套的格式，那么更复杂的条件，就可以在此基础上进行扩展应用。

### 4. 通配符

ldap的搜索中也可以使用通配符，常用的是`*`，搜索语法如下：

```bash
$ ldapsearch <previous_options> "(object_type)=*(object_value)"

$ ldapsearch <previous_options> "(object_type)=(object_value)*"
```

比如，我们可以搜索ou以root结尾的内容：

```bash
$ ldapsearch -x -b "dc=eryajf,dc=net" -H ldap://192.168.31.76:389 -D "cn=admin,dc=eryajf,dc=net"  -W "ou=*root"

# dingtalkroot, eryajf.net
dn: ou=dingtalkroot,dc=eryajf,dc=net
ou: dingtalkroot
description:: 6ZKJ6ZKJ5qC56YOo6Zeo
objectClass: top
objectClass: organizationalUnit

# wecomroot, eryajf.net
dn: ou=wecomroot,dc=eryajf,dc=net
ou: wecomroot
description:: 5LyB5Lia5b6u5L+h5qC56YOo6Zeo
objectClass: top
objectClass: organizationalUnit

# feishuroot, eryajf.net
dn: ou=feishuroot,dc=eryajf,dc=net
ou: feishu
ou: feishuroot
description:: 6aOe5Lmm5qC56YOo6Zeo
objectClass: top
objectClass: organizationalUnit

# search result
search: 2
result: 0 Success

# numResponses: 4
# numEntries: 3
```

### 5. 其他

ldapsearch还支持其他一些逻辑运算符，比如：

- `>=`：查找特定项，该项中包含的属性的数字或字母值大于或等于指定的值。
- `<=`：查找特定项，该项中包含的属性的数字或字母值小于或等于指定的值。
- `~=`：查找特定项，该项中所含属性的值约等于指定的值。

## 四、命令参数

ldapsearch还有丰富的命令参数，罗列如下：

| 参数           | 用途                                                                                                                                                                     |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| -a deref     | 指定别名反向引用。请输入 never、always、search 或 find。如果不使用此参数，缺省为 never。                                                                                                            |
| -A           | 只检索属性的名称，而不检索属性的值。                                                                                                                                                     |
| -b base dn   | 指定用作搜索起始点的专有名称。使用引号来指定该值，如："ou=Ops,dc=shuyun,dc=com". 如果要搜索的服务器需要指定搜索起点，则必须使用此参数。否则此参数是可选的。也可以同时使用 -b 和 -s 来确定搜索范围。没有 –s，-b 就会搜索指定为起始点的项以及该项的所有子项。                     |
| -B           | 允许打印非 ASCII 值                                                                                                                                                          |
| -D bind dn   | 指定服务器用于验证您的专有名称。名称必须与目录中的项相符，并且必须拥有搜索目录所需的权限。请使用引号来指定该名称，例如："cn=Manager,dc=shuyun,dc=com"。如果不使用此参数，则与服务器的连接是匿名的。如果服务器不允许匿名连接，则必须使用 -D。除了 -D，还必须使用 -w 参数来指定与专有名称相关联的口令。 |
| -f file      | 指定包含要使用的搜索过滤器的文件，如 -f 过滤器。请将每个搜索过滤器置于单独的一行。Ldapsearch 会对每一行执行一次搜索。可选择指定过滤模式。例如，指定 -f 过滤 "cn=%s"，并在文件的每一行中输入公用名称的值。                                                     |
| -F sep       | 在属性名称和值之间打印 sep 而不是等号 (=)。例如，如果读取 ldapsearch 输出的工具希望使用其他的分隔符时，可以使用此参数。                                                                                                 |
| -h host name | 指定要连接的服务器主机名，如 -h ldap.shuyun.com。                                                                                                                                     |
| -l timelimit | 指定完成搜索的时间限制（秒）。如果没有指定此参数或指定的限制为 0，那么搜索就没有时间限制。但是，ldapsearch 的等待时间决不会超过服务器上设置的搜索时间限制。                                                                                   |

| -L           | 指定以 LDIF 格式输出。LDIF 格式使用冒号 (:) 而不是等号 (=) 作为属性描述符。LDIF 对一次性添加或修改大量目录项很有帮助。例如，可以将输出内容引入兼容 LDAP 的目录中。                                                    |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| -M           | 将参考对象作为普通项进行管理，以使 ldapsearch 可返回参考项本身的属性，而不是所参考的项的属性。                                                                                                |
| -n           | 显示如何执行搜索，但不实际执行搜索                                                                                                                                    |
| -p port      | 指定服务器使用的端口。如果没有使用此参数，缺省情况下 ldapsearch 使用 389 端口。                                                                                                     |
| -R           | 不自动遵循服务器返回的搜索引用。请注意，Netscape 目录服务器将术语 referrals 用于搜索引用。                                                                                              |
| -s scope     | 指定使用 -b 参数时的搜索范围：base -- 仅搜索 -b 参数指定的项onelevel -- 仅搜索 -b 参数指定项的直接子项，而不搜索该项本身subtree -- 搜索 -b 参数指定的项以及它的所有子项。这是不带 -s 时使用 -b 的缺省行为。指定 -b 和 -s 的顺序并不重要。 |
| -S attribute | 按指定的属性排序结果。                                                                                                                                          |
| -z sizelimit | 指定返回项的最大数目。如果没有指定此参数或指定的限制为 0，那么返回的项没有数量限制。但是，ldapsearch 返回的项决不会多于服务器允许的数量。                                                                          |
| -u           | 指定 ldapsearch 以用户友好格式返回专有名称。                                                                                                                         |
| -v           | 指定 ldapsearch 以详尽模式运行。                                                                                                                               |

| -w password | 指定与 -D 参数一起使用的与专有名称关联的口令。                                                 |
| ----------- | ------------------------------------------------------------------------- |
| x           | 与 -S 一起使用时可指定 LDAP 服务器在将结果返回之前就对它们进行排序。如果使用 -S 而不使用 –x，ldapsearch 将对结果排序。 |

## 参考资料

- https://wiki.eryajf.net/pages/e78558
