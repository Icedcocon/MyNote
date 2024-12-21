# OpenSSL生成证书快速开始

### 1. openssl req 概述

#### 1.1. 基本功能

伪命令 openssl req 大致有3个功能：

- (1) 生成证书请求文件
- (2) 验证证书请求文件
- (3) 创建根CA

#### 1.2. 准备工作及流程

- (1) 申请者需要将自己的信息及其公钥放入证书请求中。

> 注意： 但在实际操作过程中，需要提供私钥而非公钥，因为 OpenSSL 会自动从私钥中提取公钥。

- (2) 将提供的数据进行数字签名(使用单向加密)，保证该证书请求文件的完整性和一致性，防止他人盗取后进行篡改

## 2. 快速开始

### 2.1 生成根CA证书

#### 2.1.1 （可选）准备 .conf 配置文件

- 当不使用该配置文件时 openssl 会要求用户交互输入相应信息。

- 模板如下

```bash
[ req ]
default_bits       = 4096
distinguished_name = req_distinguished_name

[ req_distinguished_name ]
countryName                 = Country Name (2 letter code)
countryName_default         = CN
stateOrProvinceName         = State or Province Name (full name)
stateOrProvinceName_default = JiangSu
localityName                = Locality Name (eg, city)
localityName_default        = NanJing
organizationName            = Organization Name (eg, company)
organizationName_default    = Sheld
commonName                  = Common Name (e.g. server FQDN or YOUR name)
commonName_max              = 64
commonName_default          = Ted CA Test
```

### 2.1.2 （可选）生成根证书私钥 ca.key

- 私钥文件是非必需的，因为openssl req在需要它的时候会自动创建在特定的路径下

```bash
openssl genrsa -out ca.key 4096
```

#### 2.1.3 生成根证书签名请求文件 ca.csr

其中

- "-new"表示新生成一个新的证书请求文件

- "-key"指定私钥文件

- "-out"指定输出文件

- "-sha256" 指定签名算法，默认使用 `-sha1` ，常见有 `-md5` 、`-sha512`

> 注意：更多签名算法可通过指令 `openssl dgst -list` 查看

```bash
openssl req \
  -new \
  -sha256 \
  -out ca.csr \
  -key ca.key \
  -config ca.conf
```

使用以下指令可以查看生成的证书内容

其中

- "-text" 表示完整输出证书内容

- "-notout" 表示不输出内容，与 `-text` 配合表示只输出请求的文件头

- "-subject" 表示只输出subject部分，需要和 `-noout` 配合使用

- "-pubkey"表示只输出公钥部分，需要和 `-noout` 配合使用

```bash
openssl req -in ca.csr -text
openssl req -in ca.csr -text -noout
openssl req -in ca.csr -subject -noout
openssl req -in ca.csr -pubkey -noout
```

#### 2.1.4 校验请求文件 ca.csr 的数字签名

其中

- "-noout" 表示不输出请求文件内容

```bash
openssl req -in ca.csr -verify -noout
# Certificate request self-signature verify OK
```
