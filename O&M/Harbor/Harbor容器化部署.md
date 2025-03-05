# Harbor容器化部署

### 1. 下载二进制文件

```bash
wget https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-linux-x86_64 \
&& mv docker-compose-linux-x86_64 /usr/local/bin/docker-compose \
&& chmod +x /usr/local/bin/docker-compose
```

### 2. 为 Harbor 生成证书

```bash
# 1、生成CA证书私钥。
#    创建目录保存证书（可选）
mkdir -p /home/harbor/ssl
cd /home/harbor/ssl
openssl genrsa -out ca.key 4096

# 2、生成CA证书。
#    如果使用IP地址，需要在执行命令前执行以下操作：
#    cd /root
#    openssl rand -writerand .rnd
#    cd -
#    调整-subj选项中的值以反映您的组织。
#    如果使用FQDN连接Harbor主机，则必须将其指定为通用名称（CN）属性。
openssl req -x509 -new -nodes -sha512 -days 3650 \
 -subj "/C=CN/ST=Beijing/L=Beijing/O=local/OU=Personal/CN=harbor-fry.com" \
 -key ca.key \
 -out ca.crt

# 3、生成服务器证书
#    证书通常包含一个.crt文件和一个.key文件，例如yourdomain.com.crt和yourdomain.com.key。
# (1) 生成私钥。
openssl genrsa -out harbor-fry.com.key 4096
# (2) 生成证书签名请求（CSR）。
#     调整-subj选项中的值以反映您的组织。
#     如果使用FQDN连接Harbor主机，则必须将其指定为通用名称（CN）属性，
#     并在密钥和CSR文件名中使用它。
openssl req -sha512 -new \
    -subj "/C=CN/ST=Beijing/L=Beijing/O=local/OU=Personal/CN=harbor-fry.com" \
    -key harbor-fry.com.key \
    -out harbor-fry.com.csr

# (3) 生成一个x509 v3扩展文件。
#     无论您使用FQDN还是IP地址连接到Harbor主机，都必须创建此文件，
#     以便可以为您的Harbor主机生成符合主题备用名称（SAN）和x509 v3的证书扩展要求。
#     替换DNS条目以反映您的域。
cat > v3.ext <<-EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names
[alt_names]
DNS.1=harbor-fry.com
DNS.2=harbor-fry
DNS.3=harbor-fry
EOF
#     如果使用ip，需要使用如下方式进行创建：
#     cat > v3.ext <<-EOF
#     authorityKeyIdentifier=keyid,issuer
#     basicConstraints=CA:FALSE
#     keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
#     extendedKeyUsage = serverAuth
#     subjectAltName = IP:192.168.93.9
#     EOF
# (4) 使用该v3.ext文件为您的Harbor主机生成证书。
#     将yourdomain.comCRS和CRT文件名中的替换为Harbor主机名。
openssl x509 -req -sha512 -days 3650 \
    -extfile v3.ext \
    -CA ca.crt -CAkey ca.key -CAcreateserial \
    -in harbor-fry.com.csr \
    -out harbor-fry.com.crt

# 4、提供证书给Harbor和Docker
#    生成后ca.crt，yourdomain.com.crt和yourdomain.com.key文件，
#    必须将它们提供给harbor和docker，和重新配置harbor使用它们。
# (1) 将服务器证书和密钥复制到Harbor主机上的certficates文件夹中。
mkdir -p /data/cert
cp harbor-fry.com.crt /data/cert/
cp harbor-fry.com.key /data/cert/
# (2) 转换yourdomain.com.crt为yourdomain.com.cert，供Docker使用。
#     Docker守护程序将.crt文件解释为CA证书，并将.cert文件解释为客户端证书。
cd /data/cert
openssl x509 -inform PEM -in harbor-fry.com.crt -out harbor-fry.com.cert
cp harbor-fry.com.cert /home/harbor/ssl
# (3) 将服务器证书，密钥和CA文件复制到Harbor主机上的Docker证书文件夹中。
#     您必须首先创建适当的文件夹。
mkdir -p /etc/docker/certs.d/harbor-fry.com:10084/
cd /home/harbor/ssl
cp harbor-fry.com.cert /etc/docker/certs.d/harbor-fry.com:10084/
cp harbor-fry.com.key /etc/docker/certs.d/harbor-fry.com:10084/
cp ca.crt /etc/docker/certs.d/harbor-fry.com:10084/
#     如果将默认nginx端口443映射到其他端口，
#     请创建文件夹/etc/docker/certs.d/yourdomain.com:port
#     或/etc/docker/certs.d/harbor_IP:port。(省略)
```

### 3. 下载 Harbor 安装包并配置

```bash
wget https://github.com/goharbor/harbor/releases/download/v2.8.2/harbor-offline-installer-v2.8.2.tgz \
&& tar -xf harbor-offline-installer-v2.8.2.tgz -C /usr/local/ \
&& cd /usr/local/harbor \
&& cp harbor.yml.tmpl harbor.yml \
&& sed -ri  "s/^hostname:.*/hostname: $(hostname)/"  harbor.yml \
&& sed -ri  "s/^  port: 80/  port: 10085/"  harbor.yml \
&& sed -ri  "s/^  port: 443/  port: 10084/"  harbor.yml \
&& sed -ri  "s#^  certificate: .*#  certificate: /data/cert/harbor-fry.com.crt#"  harbor.yml \
&& sed -ri  "s#^  private_key: .*#  private_key: /data/cert/harbor-fry.com.key#"  harbor.yml \
&& ./install.sh 
```

### 4. 配置域名解析

```bash
sed -ri '/harbor-fry/d' /etc/hosts
sed -ri '/127.0.0.1/a\192.168.0.106   harbor-fry.com' /etc/hosts
```
