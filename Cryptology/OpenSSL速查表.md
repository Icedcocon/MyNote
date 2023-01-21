```bash
######################################################################
# 第 1 章：OpenSSL基础
######################################################################
# 1.1 配置文件位置
# 1.1.1 配置文件位置
/etc/pki/tls/openssl.cnf        # CentOS 7
/usr/lib/ssl/openssl.cnf        # Ubuntu

# 1.2 格式

# 1.2.0 格式-ASN.1
# (1) ASN.1抽象语法标记（Abstract Syntax Notation One）
# (2) ASN.1是一种标记语言，用于描述数据结构，可用于数据的表示、编码、传输和解码
#     PKCS协议组和X.509协议均采用ASN.1来定义密钥或证书的数据结构
# (3) 使用ASN.1的相关编码
#     1) 基本编码规则（BER, Basic Encoding Rules） -X.209
#     2) 规范编码规则（CER, Canonical Encoding Rules）
#     3) 识别名编码规则（DER, Distinguished Encoding Rules）
#     4) 压缩编码规则（PER， Packed Encoding Rules）
#     5) XML编码规则（XER， XML Encoding Rules）
#     其中BER、CER、DER、PER属于二进制编码，密钥文件和证书文件常用DER编码
# 
# 1.2.1 KEY、CRT、PEM
# (1) KEY:一般指PEM格式的私钥文件
# (2) CRT:证书文件,可以是PEM格式
# (3) PEM(Privacy-Enhanced Mail): 
#     1) 概念:存储、发送密码学秘钥、证书和其他数据的文件格式的事实标准
#     2) 原理:使用ASN.1的密码学标准(如X.509和PKCS)常用DER编码生成二进制内容
#        二进制内容不适合邮件传输(早期无附件),因此用PEM将二进制内容转换成ASCII码
#        本质将DER编码的二进制内容用base64编码，再加上字符开头行和结束行


# 1.2.2 CSR和x.509
# (1) CSR:证书签名请求(Certificate Signing Request)
#     0) 生成X509数字证书前,由用户提交CSR,然后CA根据CSR信息签发证书,过程如下
#     1) 用户生成自己的公私钥对;
#     2) 构造CSR,包括用户信息、公钥、可选属性信息,并用自己的私钥给该内容签名;
#     3) 用户将证书申请文件提交给CA;
#     4) CA验证签名,提取用户信息,附加额外信息(如颁发者),用CA的私钥签发数字证书;
# (2) X.509证书的格式(根据ASN.1语法定义)
#     1) X.509是密码学中公钥证书的格式标准,将用户身份与公钥绑定
#     2) 包含公钥信息、用户身份信息和CA私钥的签名信息,持有者除证书外还拥有对应私钥
#     3) X509v3数字证书主要内容:证书版本、证书序列号、签名算法、颁发者信息、有效时间、
#                            持有者信息、公钥信息、颁发者 ID、持有者 ID 和扩展项


# 1.2.3 DER、CER
# (1) 辨别编码规则 DER (Distinguished Encoding Rules)
#     1) 是基本编码规则(base encoding rules, BER)的一个子集
#     2) 可将秘钥、证书和其他信息编码为二进制文件
#     3) DER是多数浏览器默认格式，用ASN1语言描述并存储
#     4) PEM格式用文本开头和结尾包围用Base64编码为ASCII码的DER二进制内容
# (2) CER
#     DER编码或PEM编码的证书

# 1.2.4 PKCS
# The Public-Key Cryptography Standards (PKCS)
# 由美国RSA数据安全公司及其合作伙伴制定的一组公钥密码学标准
# 包括证书申请、证书更新、证书作废表发布、扩展证书内容及数字签名、数字信封格式等协议
# 到1999年底，PKCS已经公布了15个标准，其编号分别为PCKS#1~15
# PKCS #1 : RSA Cryptography Standard RSA密码编译标准
# PKCS #7 : Cryptographic Message Syntax Standard 密码消息语法标准
#           存放数据、签名数据、数字信封、签名数字信封、摘要数据和加密数据的格式标准
# PKCS #10 : Certification Request Standard 证书申请标准 x.509
# PKCS #12 : Personal Information Exchange Syntax Standard 个人消息交换标准
#           用于存放用户证书、CRL、用户私钥以及证书链的格式标准

# 1.2.5 OCSP
# (1) 在线证书状态协议(Online Certificate Status Protocol)用于实时表明证书状态
# (2) OCSP客户端查询OCSP服务可确定证书的状态获取证书的有效性资料
# (3) OCSP建立可实时响应机制,用户可实时确认每张证书有效性，解决CRL引发的安全问题
# (4) OCSP可通过HTTP协议来实现
# (5) rfc2560定义了OCSP客户端和服务端的消息格式

# 1.2.6 CRL
# (1) 证书吊销列表(Certification Revocation List)是含撤销证书列表签名的数据结构
# (2) CRL是证书撤销状态的公布形式,用于公布某些数字证书不再有效
# (3) CRL是离线证书状态信息,它以一定的周期进行更新
# (4) CRL可以分为完全CRL(含所有被撤销证书信息)和增量CRL(每次发布都是上次的增量扩充)
# (5) 基本CRL信息:被撤销证书序列号、撤销时间、撤销原因、签名者及CRL签名等
# (6) 基于CRL的验证是不严格的证书认证能证明被撤销证书无效,不能给出不在CRL中证书的状态
#      严格的认证需要采用在线方式认证,即OCSP认证

# 1.2.7 SCEP
# (1) 简单证书注册协议是基于文件的证书登记方式,需将文件从本地拷贝到证书发布中心或相反 
# (2) SCEP能自动处理而CRLs需要手动在本地计算机和CA发布中心间进行复制和粘贴


# 1.3 使用

# 1.3.1 CA证书（根证书）
# (0) 自签名的证书，不被浏览器信任，适合内部或者测试使用
# (1) 生成一个2048位素数的RSA私钥
openssl genrsa -out identify/ca/ca.key 2048  
# (2) 生成证书请求文件(签名请求)
openssl req -new -key identify/ca/ca.key \
            -out identify/ca/ca.csr \
            -config /etc/pki/tls/openssl.cnf
#  1) ① 国家(Country Name)
#     ② 地区(State or Privance Name)
#     ③ 城市(Locility Name)
#     ④ 组织(Organization Name)
#     ⑤ 组织部门(Organization Unit Name)
#     ⑥ FQDN/名字(Common Name)
#     ⑦ 邮件(Email)，若配置文件有默认值可以回车跳过
#  2) 要支持https则Common Name应该与域名一致
#  3) 可将证书发给CA验证并出具签名证书,或用OpenSSL实现自签名
#  4) -config bin/cnf/openssl.cnf 指定当前openssl配置文件位置
# (3) 生成签名证书(自签名)
openssl x509 -req -days 365 -in identify/ca/ca.csr \
             -signkey identify/ca/ca.key \
             -out identify/ca/ca.crt
# (4) 转换证书格式
openssl x509 -in identify/ca/ca.crt \
             -out identify/ca/ca.pem \
             -outform PEM

# 1.3.2 服务端证书
# (1) 生成证书密钥
openssl genrsa -out identify/server/server.key 2048
# (2) 生成证书请求文件(签名请求)
openssl req -new -out identify/server/server.csr \
            -key identify/server/server.key \
            -config /etc/pki/tls/openssl.cnf
# (3) 生成签名证书
openssl ca -in identify/server/server.csr \
           -out identify/server/server.crt \
           -cert identify/ca/ca.crt \
           -keyfile identify/ca/ca.key \
           -extensions v3_req \
           -config /etc/pki/tls/openssl.cnf\
           -policy policy_anything

# 1.3.3 客户端证书
# (1) 生成证书密钥
openssl genrsa -des3 -out identify/client/client.key 2048 # 需要输入密码
# (2) 生成证书请求文件(签名请求)
openssl req -new -key identify/client/client.key \
            -out identify/client/client.csr \
            -config /etc/pki/tls/openssl.cnf
# (3) 生成签名证书
openssl ca -in identify/client/client.csr \
           -cert identify/ca/ca.crt \
           -keyfile identify/ca/ca.key \
           -out identify/client/client.crt \
           -config bin/cnf/openssl.cnf\
           -policy policy_anything 
```

```bash
######################################################################
# 第 2 章：OpenSSL用法
######################################################################
# 2.1.1 OpenSSL概念及用途
# (1) OpenSSL 是一个开源项目，其组成主要包括一下三个组件：
#       1) openssl：多用途的命令行工具
#       2) libcrypto：加密算法库
#       3) libssl：加密模块应用库，实现了ssl及tls
# (2) openssl可以实现：秘钥证书管理、对称加密和非对称加密  

# 2.1.2 对称加密
# enc为对称加密指令，可用于加密和解密,其中Base64编码可以单独执行,用法如下：
openssl ciphername # 该指令在读取配置文件和加载任何引擎前执行,不能用引擎提供的密码
openssl enc -ciphername [-in filename] [-out filename] [-pass arg] \
        [-e] [-d] [-a/-base64] [-A] [-k password] [-kfile filename] \
        [-K key] [-iv IV] [-S salt] [-salt] [-nosalt] [-z] [-md] [-p] \
        [-P] [-bufsize number] [-nopad] [-debug] [-none] [-engine id]
# 常用选项有：
#     (1) -in/out filename：明文/密文存放路径，默认标准输入/输出
#     (2) -pass arg：指定密码的输入方式(5种)
#                     命令行输入(stdin)
#                     文件输入(file)
#                     环境变量输入(var)
#                     文件描述符输入(fd)
#                     标准输入(stdin)(默认)
#     (3) -md：生成秘钥的摘要算法,用户输入口令!=密钥,要用摘要算法做转换(md5)
#     (4) -salt：在加密/推导中使用salt(默认)(随机生成或-S指定)
#         -nosalt：不使用salt
#         -S：salt值(十六进制字符串)
#         为增强安全性，在密码转为加密密钥时候需要使用盐值，默认随机生成
#     (5) -k/iv：加密密钥的Key/初始变量IV默认由用户输入口令转化，但也可指定
#     (6) -e/d：加密(默认)/解密输入文件
#     (7) -a/-base64：密文为二进制格式-a可对密文编码更可读,解密时则先解码在解密
#     (8) -p/P：-p打印Key和IV的值
#     (9) -nopad：不使用补齐，这就需要输入的数据长度是使用加密算法的分组大小的倍数
openssl enc -e -des3 -a -salt -in fstab -out jiami  # 加密
openssl enc -d -des3 -a -salt -in fstab -out jiami  # 解密
openssl base64 -in file.bin -out file.b64            # 仅base64编码
openssl base64 -d -in file.b64 -out file.bin        # 仅base64解码

# 2.1.3 信息摘要（特点、用途、数字签名用途）
# (1) 信息摘要(杂凑码/哈希值)：将输入数据转变为固定长度的结果，其特点：
#    1) 输出长度固定。即输出长度和输入长度无关。
#    2) 不可逆。即由输出数据理论上不能推导出输入数据
#    3) 对输入数据敏感。当输入数据变化极小时，输出数据也会发生明显的变化
#    4) 防碰撞。即不同的数据数据得到相同输出数据的可能性极低。
# (2)用途：
#   1) 可保证数据的完整性,计算大文件摘要,文件传输过后验证摘要确认文件完整
#   2) 数字签名:1.计算明文文件的摘要值;2.使用公开密钥算法中的私钥对摘要值进行加密
# (3) 数字签名用途
#   1) 对发送信息进行数字签名，可以保证数字签名的完整性、真实性、不可抵赖性
#   2) 接收者可以确认消息的来源、消息的真实，发送者不可以抵赖自己发送的消息
# (4) openssl指令没有区分摘要的计算和加密,而是包含了签名和校验参数



# 2.1.4 单向加密和签名
# dgst为文件提供十六进制信息摘要(哈希值)，也可以用来生成和验证数字签名
# 签名私钥多为RSA或DSA,用RSA私钥时可直接用算法指令,DSA私钥则必须用dgst指令
# 因为DSA签名需使用自身的摘要算法,openssl并未提供该指令
openssl md5|md4|md2|sha1|sha|mdc2|ripemd160|dss1 # 可直接用算法指令也可用dgst
openssl dgst [-md5|-md4|-md2|-sha1|-sha|-mdc2|-ripemd160|-dss1] [-c] \
        [-d] [-hex] [-binary] [-out filename] [-sign filename] \
        [-keyform arg] [-passin arg] [-verify filename] \
        [-prverify filename] [-signature filename] [-hmac key] [file...]
# 常用选项有：
#     (1) [-md5|-md4|-md2|-sha1|-sha|-mdc2|-ripemd160|-dss1]：指定加密算法
#     (2) -out filename：将加密内容/签名保存到指定文件中
#     (3) -sign filename：执行签名操作,filename指定私钥文件
#     (4) -keyform：指定密钥文件格式,DER、PEM、P12或ENGINE
#     (5) -verify filename：执行验证操作,指定公钥文件,与prverfify冲突
#     (6) -prverify filename：执行验证操作,指定私钥文件,与verfify冲突
#     (7) -signature filename：要验证的签名文件
#     (8) file...：需要签名的文件(可以是多个)，未指定则使用标准输入
#     (9) -c/hex/binary：-c摘要信息分号隔开 -hex/binary指定输出结果的进制
# 单向加密除了openssl dgst工具还有：
#    md5sum，sha1sum，sha224sum，sha256sum ，sha384sum，sha512sum
openssl dgst -sha1 file.txt                     # 仅做摘要运算而不做签名操作
openssl dgst -sign RSA.pem -sha256 -out sign.txt file.txt
                                                # 用RSA秘钥进行签名
openssl dgst -prverify RSA.pem -sha256 -signature sign.txt file.txt 
                                                # 私钥验证签名                                        
openssl rsa -in RSA.pem -out pub.pem -pubout    # 提取公钥
openssl dgst -verify pub.pem -sha256 -signature sign.txt file.txt
                                                # 公钥验证签名 

# 2.1.5 生成密码
# 生成密码需要使用的标准命令为 passwd ，用法如下：
openssl passwd [-crypt] [-1] [-apr1] [-salt string] [-in file] \
        [-stdin] [-noverify] [-quiet] [-table] {password}
# 常用选项有：
#    (1) -1：使用md5加密算法
#    (2) -salt string：加入随机数，最多8位随机数
#    (3) -in file：对输入的文件内容进行加密
#    (4) -stdin：对标准输入的内容进行加密

# 2.1.6 生成随机数
# 生成随机数需要用到的标准命令为 rand ，用法如下：
openssl rand [-out file] [-rand file(s)] [-base64] [-hex] num
# 常用选项有：
#    (1) -out file：将生成的随机数保存至指定文件中
#    (2) -base64：使用base64 编码格式
#    (3) -hex：使用16进制编码格式

# 2.1.7 非对称加密算法概述
# (1) 定义：非对称加密算法也称公开密钥算法，解决了对称加密算法密钥分配问题
# (2) 特点：
#     1) 加密密钥和解密密钥不同
#     2) 密钥对中的一个密钥可以公开
#     3) 根据公开密钥很难推算出私人密钥
# (2) 用途：
#      1) 可用于数字签名、密钥交换、数据加密
#      2) 非对称加密算法较对称加密算法加密速度慢很多，故最长用于数字签名和密钥交换
#      3) 常用非对称加密算法有RSA, DH和DSA三种
#         RSA可用于数字签名和密钥交换
#         DH算法可用于密钥交换
#         DSA算法专门用户数字签名

# 2.1.7 非对称加密算法RSA命令
# (1) RSA最常用于数字签名和密钥交换
# (2) 公钥加密：用途是密钥交换，用户A使用用户B的公钥将少量数据加密发送给B
#              B用自己的私钥解密数据
# (3) 私钥签名：用途是数字签名，用户A使用自己的私钥将数据的摘要信息加密一并发送给B
#              B用A的公钥解密摘要信息并验证
# (3) openssl指令
#     1) genrsa  生成并输入一个RSA私钥
#     2) rsa     处理RSA密钥的格式转换等问题
#     3) rsautl  使用RSA密钥进行加密、解密、签名和验证等运算

# 2.1.7.1 genrsa
openssl genrsa [-out filename] [-passout arg] [-des] [-des3] [-idea] \
        [-f4] [-3] [-rand file(s)] [-engine id] [numbits]
# 常用选项有：
#    (1) -out filename：将生成的私钥保存至指定的文件中
#    (2) -des|-des3|-idea：加密秘钥的算法
#    (3) -seed|aes128|camellia128：加密PEM的算法
#    (4) -passout arg：指定秘钥文件的加密口令(env、file、stdin)
#    (4) numbits：指定生成私钥的大小，默认是512
#    (5) -rand file：生成随机数的种子文件
genrsa -out rsa.pem -aes128 -passout pass:123456 1024 # 生成秘钥文件

# 2.1.7.2 rsa
openssl rsa [-inform PEM|NET|DER] [-outform PEM|NET|DER] [-in filename] \
            [-passin arg] [-out filename] [-passout arg] [-sgckey] \
            [-des] [-des3] [-idea] [-text] [-noout] [-modulus] [-check] \
            [-pubin] [-pubout] [-engine id]
# 常用选项：
#      (1) -in/out/noout filename：输入/输出文件/不输出密钥到任何文件
#      (2) -inform/outform arg：输入/输出文件格式，默认pem格式
#      (3) -pubin/pubout：指定输入/输出文件是公钥(前者换格式,后者提取公钥)
#      (4) -passin/passout arg 指定输入/输出文件加密口令(env、file、stdin/stdout)
#      (5) -des|des3|seed|aes128：加密PEM文件的加密算法
#      (6) -text：以明文形式输出各个参数值
#      (7) -check：检查输入密钥的正确性和一致性
#      (8) -engine e：指定三方加密库或者硬件
#      (9) -modulus：输出模数指
# 应用：
# (1) rsa添加/去除密钥的保护口令
openssl genrsa -out RSA.pem                    # 生成不加密的RSA密钥
openssl rsa -in RSA.pem -des3 -passout pass:123456 -out E_RSA.pem
                                               # 为RSA密钥增加口令保护
openssl rsa -in E_RSA.pem -passin pass:123456 -out P_RSA.pem                                                                           # 为RSA密钥去除口令保护
# (2) 修改密钥的保护口令/算法
openssl genrsa -des3 -passout pass:123456 -out RSA.pem  # 生成RSA密钥
openssl rsa -in RSA.pem -passin pass:123456 -aes128 \
        -passout pass:123456 -out E_RSA.pem   # 修改加密算法为aes128,口令不变
# (3) 查看密钥对中的各个参数
openssl rsa -in RSA.pem -des -passin pass:123456 -text -noout
# (4) 提取密钥中的公钥
openssl rsa -in RSA.pem -passin pass:123456 -pubout -out pub.pem # 提取公钥
# (5) 转换密钥的格式
openssl rsa -in RSA.pem -passin pass:123456 -des -passout pass:123456 \
        -outform der -out rsa.der              # 把pem格式转化成der格式


# 2.1.7.3 rsautl
# genrsa、rsa是密钥的生成与管理,rsautl则用于密钥交换和数字签名(用RSA公钥或者私钥加密)
# 无论公钥或私钥加密，RSA每次能加密的数据长度不能超过RSA密钥长度
# 并且根据具体的补齐方式不同输入的加密数据最大长度也不一样，而输出长度则总是跟RSA密钥长度相等
# RSA不同的补齐方法对应的输入输入长度如下表

# 数据补齐方式         输入数据长度                    输出数据长度    参数字符串
# PKCS#1 v1.5         少于(密钥长度-11)字节           同密钥长度    -pkcs
# PKCS#1 OAEP         少于(密钥长度-11)字节           同密钥长度    -oaep
# PKCS#1 for SSLv23     少于(密钥长度-11)字节         同密钥长度    -ssl
# 不使用补齐              同密钥长度                      同密钥长度       -raw

-in file        input file                                           //输入文件
-out file       output file                                          //输出文件
-inkey file     input key                                            //输入的密钥
-keyform arg    private key format - default PEM                     //指定密钥格式
-pubin          input is an RSA public                               //指定输入的是RSA公钥
-certin         input is a certificate carrying an RSA public key    //指定输入的是证书文件
-ssl            use SSL v2 padding                                   //使用SSLv23的填充方式
-raw            use no padding                                       //不进行填充
-pkcs           use PKCS#1 v1.5 padding (default)                    //使用V1.5的填充方式
-oaep           use PKCS#1 OAEP                                      //使用OAEP的填充方式
-sign           sign with private key                                //使用私钥做签名
-verify         verify with public key                               //使用公钥认证签名
-encrypt        encrypt with public key                              //使用公钥加密
-decrypt        decrypt with private key                             //使用私钥解密
-hexdump        hex dump output                                      //以16进制dump输出
-engine e       use engine e, possibly a hardware device.            //指定三方库或者硬件设备
-passin arg    pass phrase source                                    //指定输入的密码

# 2.1.8 非对称加密算法DSA命令 


# 2.1.8 创建CA创建自签证书
# 创建CA证书和申请证书前先查看配置文件，文件对证书名称和存放位置等信息设置了默认值
# (1) 创建CA所需的目录及文件
mkdir -pv /etc/pki/CA/{certs,crl,newcerts,private}
touch /etc/pki/CA/{serial,index.txt}
# (2) 指明证书的开始编号
echo 01 >> serial 
# (3) 生成私钥,私钥文件名与路径要与配置文件匹配
# (4) 生成自签证书,自签证书路径要与配置文件匹配,生成证书时需要填写相应的信息；
# 命令中用到的选项解释：
#     -new：表示生成一个新证书签署请求
#     -x509：专用于CA生成自签证书，如果不是自签证书则不需要此项
#     -key：生成请求时用到的私钥文件
#     -out：证书的保存路径
#     -days：证书的有效期限，单位是day（天），默认是365天

（2）颁发证书
# 在需要使用证书的主机上生成证书请求，以 httpd 服务为例，步骤如下：
# 1) 在需要使用证书的主机上生成私钥，这个私钥文件的位置可以随意定
# 2) 生成证书签署请求
# 3) 将请求通过可靠方式发送给 CA 主机
# 4) CA 服务器拿到证书签署请求文件后颁发证书，这一步是在 CA 服务器上做的
查看证书信息的命令为：

（3）吊销证书

吊销证书的步骤也是在CA服务器上执行的，以刚才新建的 httpd.crt 证书为例，吊销步骤如下：

第一步：在客户机上获取要吊销证书的 serial 和 subject 信息

第二步：根据客户机提交的 serial 和 subject 信息，对比其余本机数据库 index.txt 中存储的是否一致

第三步：执行吊销操作

wKiom1fk8oqSxqlvAAAgT9Y4ODo373.png

第四步：生成吊销证书的吊销编号（第一次吊销证书时执行）

    ]# echo 01 > /etc/pki/CA/crlnumber

第五步：更新证书吊销列表

    ]# openssl ca -gencrl -out /etc/pki/CA/crl/ca.crl

查看 crl 文件命令：

    ]# openssl crl -in /etc/pki/CA/crl/ca.crl -noout -text
```

```bash
1 数据编码格式
openssl的数据编码规则是基于ans.1的，ans.1是什么 ? 先上高大上的解释

ASN.1(Abstract Syntax Notation One), 是一种结构化的描述语言，包括两部分,数据描述语言和数据编码规则,数据描述语言标准：语言标准允许用户自定义的基本数据类型，并可以通过简单的数据类型组成更复杂的数据类型。数据编码规则：这些编码方法规定了将数字对象转换成应用程序能够处理、保存、传输的二进制形式的一组规则。标准ASN.1编码规则有规范编码规则（CER，Canonical Encoding Rules）、唯一编码规则（DER，Distinguished Encoding Rules）、压缩编码规则（PER，Packed Encoding Rules）和XML编码规则（XER，XML Encoding Rules）。

没看懂？好吧，我也没看懂。经过搜索无数资料后，现把自己的理解说一下，有不对的地方请大牛指正

我们知道在计算机语言中有很多的数据结构，有列表、集合、数组等等。但对应用程序特别是网络来说，这些数据结构都是二进制的数据流，那么如何把这些不同的数据结构变成数据流，又能让其他应用能够识别呢。这就需要一个标准，也就是我们说的ans.1，大家都遵守这个标准，自然可以和平共处。OK，这个标准到底是什么玩意？

这个问题一会再来回答。现在我们想想如何把一个二叉树中的数据以流的形式发出去，对于整型、字符串这些基本类型我们可以直接塞进数据流里，但对于这种复杂的结构，这种方法就不显示了，怎么办？我们引入一个数字对象的概念，把这些数据结构转化成一个数字对象，怎么转？这就用到了asn.1标准的第一部分--数据描述语言标准，这个标准定义了一些基本的数据类型，如果我们使用到复杂的数据结构，asn.1还允许通过简单数据类型组成复杂的数据类型(x.509)。

数字对象已经建立的，怎么把这个数据对象变成二进制流呢，这就需要用到ans.1的第二部分--编码规则，编码方法规定了将数字对象转换成应用程序能够处理、保存、传输的二进制形式的一组规则。

现在可以回答上面这个问题了，简单来说这个标准就是规定了把数据转化成数据对象，又规定数据对象编码为二进制流的方法。

openssl使用的是asn.1的der编码规则，保证每个asn.1对象使用der编码的出的二进制编码是唯一的。

openssl使用pem作为基本的文件编码格式，pem和der是什么关系，如下图所示，几种加密环节是可选的

image

从本质上来说，openssl是pem编码就是在der编码的技术上进行Base64编码，然后添加一些头尾信息组成，可以通过openssl指令对der和pem进行格式转换

2 证书编码格式
常见的证书编码格式有三种X.509证书，PKCS#12证书PKCS#7证书。

X.509证书：最常用的证书格式，它仅包含了公钥信息而没有私钥信息，一个openssl签发经过PEM编码的X.509证书看起来如下

-----BEGIN CERTIFICATE-----
XXX
-----END CERTIFICATE-----
中间部分就是经过PEM编码的X509证书。除了上述形式的头尾格式，还可能出现以下两种不同的标识符

-----BEGIN X.509 CERTIFICATE----
XXX
-----END X.509 CERTIFICATE-----
或者
-----BEGIN TRUSTED  CERTIFICATE-----
-----END TRUSTED  CERTIFICATE-----
X.509证书文件的后缀名经常是der,cer或者crt。openssl的指令x509提供了对X.509证书进行格式转换的方法。

PKCS#12证书：PKCS12证书可以包含一个或者多个证书，并且还可以包含证书对应的私钥。openssl的pkcs12指令可以将X.509格式的证书和私钥封装成PKCS#12格式的证书，也可以将PKCS#12证书转换成X.509证书

PKCS#12证书的后缀名通常是p12或者pdx

PKCS#7证书: PKCS#7可以封装一个或者多个X.509证书或者PKCS#6证书，并且可以包含CRL信息。PKCS#7证书中也不包含私钥信息。openssl提供了crl2pkcs7和pkcs7两个指令来生成和处理PKCS#7文件，可以使用他们在X.509证书和PKCS#7证书之间进行转换和处理

PKCS#7证书的后缀名是p7b

3 密钥编码
openssl有多种形式的密钥，openssl提供PEM和DER两种编码方式对这些密钥进行编码，并提供相关指令可以使用户在这两种格式之间进行转换

openssl密钥大致可以分为两种，一种是可以公开的，例如公钥，一种是不能公开的，比对私钥。反映在编码上，有的密钥需要加密，有的密钥就不需要加密。一个经过加密的PEM编码密钥文件会在PEM文件中增加一些头信息，表明密钥的加密状态，加密算法及初始化向量等信息

openssl指令提供了对密钥加密的功能，并提供了多种可选的对称加密算法，比如DES和DES3。当对密钥进行加密的时候通常需要用户输入口令，这里的口令并非直接用来作为加密的密钥，而是根据这个口令使用一系列HASH操作来生成一个用户加密密钥数据的密钥。当读取这类密钥的时候，同样需要输入同样的口令。
```

```bash
https://www.cnblogs.com/gordon0918/p/5237717.html
https://www.cnblogs.com/gordon0918/p/5436012.html
```
