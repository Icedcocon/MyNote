# LDAP用户及权限管理

openldap默认的账户是cn=Manager,dc=361way,dc=com这样的一个账户 ，其写在配置文件`/etc/openldap/slapd.conf` 或 `/usr/local/etc/openldap/slapd.ldif` 文件中，但这样的一个账户就像linux下的root一样，虽然好用，不过权限太大 。出于安全考量，我们需要根据具体应用的需要，建立只读账户或者可写用户。

## 禁止匿名访问LDAP

### 检查支持机制

- 当缺少 EXTERNAL 时会执行带有 `-Y EXTERNAL` 的指令会报错。

```bash
ldapsearch -x  -b "" -LLL -s base supportedSASLMechanisms
# dn:
# supportedSASLMechanisms: PLAIN
# supportedSASLMechanisms: GSSAPI
# supportedSASLMechanisms: ANONYMOUS
# supportedSASLMechanisms: CRAM-MD5
# supportedSASLMechanisms: DIGEST-MD5
# supportedSASLMechanisms: PLAIN
# supportedSASLMechanisms: OTP
# supportedSASLMechanisms: EXTERNAL
```

- 如果缺少以上机制，执行下述指令重新编译

```bash
apt install libsasl2-dev
./configure --with-cyrus-sasl
make depend
make
make install 
```

- 配置 `cn=admin,cn=config` 密码

```bash
# vim /usr/local/etc/openldap/slapd.d/cn\=config/olcDatabase\=\{0\}config.ldif
...
olcRootDN: cn=config
olcRootPW: secret        # 添加本行
...
```

- 修改配置文件 ` /usr/local/etc/openldap/slapd.d/cn\=config/olcDatabase\=\{0\}config.ldif`  以提升 ldap root 用户的权限

```bash
ldapmodify -D cn=config -w secret -H ldapi:/// <<EOF
dn: olcDatabase={0}config,cn=config
replace: olcrootdn
olcrootdn: gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth
-
delete: olcrootpw
-
EOF
```

- 重启slapd并监听

```bash
/usr/local/libexec/slapd -h "ldapi:// ldap://"
```

openldap默认都是可以进行匿名访问的，这个我们可以通过ldapadmin或者phpldapadmin等工具来进行查看。（登录或连接测试时，选择匿名连接）

要取消openldap的匿名访问功能，只需执行以下ldif脚本即可，而且是**无需重启openldap服务**。

- 配置脚本

```bash
cat > disable_anon.ldif <<-EOF
dn: cn=config
changetype: modify
add: olcDisallows
olcDisallows: bind_anon
-

dn: olcDatabase={-1}frontend,cn=config
changetype: modify
add: olcRequires
olcRequires: authc
EOF


# cat > disable_anon.ldif <<-EOF
# dn: cn=config
# changetype: modify
# add: olcDisallows
# olcDisallows: bind_anon
# 
# dn: cn=config
# changetype: modify
# add: olcRequires
# olcRequires: authc
# 
# dn: olcDatabase={-1}frontend,cn=config
# changetype: modify
# add: olcRequires
# olcRequires: authc
# EOF
```

- 使用 ldapadd 指令将配置导入 ldap

```bash
ldapadd -Y EXTERNAL -H ldapi:/// -f disable_anon.ldif
```

## 参考资料

- [ldap用户及权限管理 | 云原生之路](https://blog.361way.com/ldap-adduser-grants/2825.html)

- [OpenLDAP权限配置 - Poke - 博客园](https://www.cnblogs.com/ipoke/p/8866322.html)

禁止匿名访问

- https://blog.csdn.net/baidu_38844729/article/details/107200232

- [OpenLDAP 禁止匿名访问 | 凡间的精灵](https://chenzhonzhou.github.io/2020/11/03/openldap-jin-zhi-ni-ming-fang-wen/)

cd=config 权限

- [centos6 - ldap_modify: Insufficient access (50) for cn=config as -H ldapi:/// -Y EXTERNAL - Server Fault](https://serverfault.com/questions/737889/ldap-modify-insufficient-access-50-for-cn-config-as-h-ldapi-y-external)
