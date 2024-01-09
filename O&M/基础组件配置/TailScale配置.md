## 1. Linux 安装tailscale

官网连接: `https://tailscale.com/download/linux`

### 1.1 脚本安装

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

### 1.2 手动安装

```bash
# 1. 添加 Tailscale 安装包的 signing key 和 repository
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.noarmor.gpg | sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg >/dev/null
curl -fsSL https://pkgs.tailscale.com/stable/ubuntu/jammy.tailscale-keyring.list | sudo tee /etc/apt/sources.list.d/tailscale.list
# 2. 安装 Tailscale
sudo apt-get update
sudo apt-get install tailscale
# 3. 连接节点到 Tailscale network 并在浏览器内登录
sudo tailscale up
# 4. 获取分配到的 IPv4 地址
tailscale ip -4
```

## 2. 安装Berp服务

- 参考连接1 `https://icloudnative.io/posts/custom-derp-servers/`
- 参考连接2 `https://www.youtube.com/watch?v=mgDpJX3oNvI`

### 2.1 下载源码

```bash
go install tailscale.com/cmd/derper@main
# 位于 /$GOHOME/pkg/mod 下
```

```go
// 修改 cmd/derper/cert.go 如下
func (m *manualCertManager) getCertificate(hi *tls.ClientHelloInfo) (*tls.Certificate, error) {
    //if hi.ServerName != m.hostname {
    //    return nil, fmt.Errorf("cert mismatch with hostname: %q", hi.ServerName)
    //}
    return m.cert, nil
}
```

### 2.2 创建自签名证书的脚本

```bash
# build_cert.sh

#!/bin/bash

CERT_HOST=$1
CERT_DIR=$2
CONF_FILE=$3

echo "[req]
default_bits  = 2048
distinguished_name = req_distinguished_name
req_extensions = req_ext
x509_extensions = v3_req
prompt = no

[req_distinguished_name]
countryName = XX
stateOrProvinceName = N/A
localityName = N/A
organizationName = Self-signed certificate
commonName = $CERT_HOST: Self-signed certificate

[req_ext]
subjectAltName = @alt_names

[v3_req]
subjectAltName = @alt_names

[alt_names]
IP.1 = $CERT_HOST
" > "$CONF_FILE"

mkdir -p "$CERT_DIR"
openssl req -x509 -nodes -days 730 -newkey rsa:2048 -keyout "$CERT_DIR/$CERT_HOST.key" -out "$CERT_DIR/$CERT_HOST.crt" -config $CONF_FILE"
```

### 2.3 Dockerfile

- 在编译镜像前需要在 tailscale 执行 `go mod vendor`

- 重新编写 Dockerfile，将 derper 的域名设置为 127.0.0.1：

```bash
FROM golang:1.20.2 AS builder

WORKDIR /app

# ========= CONFIG =========
# - download links
#ENV MODIFIED_DERPER_GIT=https://github.com/yangchuansheng/ip_derper.git
#ENV BRANCH=ip_derper
# ==========================

ADD tailscale tailscale

# build modified derper
#git clone -b $BRANCH $MODIFIED_DERPER_GIT tailscale --depth 1 && \
RUN cd /app/tailscale/cmd/derper && \
    /usr/local/go/bin/go build -ldflags "-s -w" -o /app/derper && \
    cd /app && \
    rm -rf /app/tailscale

FROM ubuntu:20.04
WORKDIR /app

# ========= CONFIG =========
# - derper args
ENV DERP_HOST=127.0.0.1
ENV DERP_CERTS=/app/certs/
ENV DERP_STUN true
ENV DERP_VERIFY_CLIENTS false
# ==========================

# apt
RUN apt-get update && \
    apt-get install -y openssl curl

COPY build_cert.sh /app/
COPY --from=builder /app/derper /app/derper

# build self-signed certs && start derper
CMD bash /app/build_cert.sh $DERP_HOST $DERP_CERTS /app/san.conf && \
    /app/derper --hostname=$DERP_HOST \
    -a :10450 \
    -http-port 10451 \
    --certmode=manual \
    --certdir=$DERP_CERTS \
    --stun=$DERP_STUN  \
    --verify-clients=$DERP_VERIFY_CLIENTS
# -a 					指定 HTTPS 端口
# -http-port			指定 HTTP 端口
# --certmode=manual		手动指定证书文件
# --certdir				证书文件位置
```

### 2.4 编译镜像并部署

- 防火墙需要放行相应端口（TCP 10450 与 UDP 3478）

```bash
docker build -t ip_derper .
docker run --restart always --net host --name derper -d ip_derper
```

- 访问 `https://you_ip:10450`

## 3 Tailscale 客户端

### 3.1 客户端跳过域名验证

- 进入 `https://login.tailscale.com/admin/acls/file` 页面，添加以下信息：
  - `OmitDefaultRegions`  为true 表示禁用官方其它服务器

```json
    "derpMap": {
        "OmitDefaultRegions": true,
        "Regions": {
            "901": {
                "RegionID":   901,
                "RegionCode": "Myself",
                "RegionName": "Myself Derper",
                "Nodes": [
                    {
                        "Name":             "901a",
                        "RegionID":         901,
                        "DERPPort":         10450,
                        "IPv4":   "服务器IP",
                        "HostName": "服务器IP",
                        "InsecureForTests": true,
                    },
                ],
            },
        },
    },


    "OmitDefaultRegions": true,
    "Regions": {
        "901": {
            "RegionID":   901,
            "RegionCode": "Myself",
            "RegionName": "Myself Derper",
            "Nodes": [
                {
                    "Name":             "901a",
                    "RegionID":         901,
                    "DERPPort":         10450,
                    "HostName":         "101.43.195.238",
                    "IPv4":             "101.43.195.238",
                    "InsecureForTests": true,
                },
            ],
        },
    },
```

## 4 防蹭网
### 4.1 服务器端安装 tailscale 并加入网络
```bash
curl -fsSL https://tailscale.com/install.sh | sh

tailscale up

docker run --restart always --net host -e "DERP_VERIFY_CLIENTS=true"  --name derper -d ip_derper
```
