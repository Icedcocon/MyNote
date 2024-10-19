## 容器化部署 IP Derper 服务器

### 0. docker-compose.yaml

- 配置文件

```bash
mkdir container-config
mkdir -p container-data/data
git clone -b v0.22.3  https://github.com/juanfont/headscale.git headscale-repo
cp headscale-repo/config-example.yaml container-config/config.yaml
```

- 编辑配置文件

```yaml
# container-config/config.yaml
server_url: http://<PUBLIC_ENDPOINT>:8080
randomize_client_port: true
ip_prefixes:
  # - fd7a:115c:a1e0::/48
  - 100.64.0.0/16
```

- 拉去镜像

```bash
docker pull headscale/headscale:0.22.3
docker pull ifargle/headscale-webui:latest
docker pull ghcr.io/yangchuansheng/ip_derper:latest
```

- docker-compose.yaml

```yaml
services:
  headscale:
    image: headscale/headscale:0.22.3
    container_name: headscale
    restart: unless-stopped
    environment:
      - TZ=Asia/Shanghai
    volumes:
      - ./container-config:/etc/headscale
      - ./container-data/data:/var/lib/headscale
    entrypoint: headscale serve
    networks:
      - external_net
    ports:
      - 8080:8080
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    sysctls:
      - net.ipv4.ip_forward=1

  headscale-webui:
    image: ifargle/headscale-webui:latest
    container_name: headscale-webui
    restart: unless-stopped
    networks:
      external_net:
    ports:
      - 8000:5000
    environment:
      - TZ=Asia/Shanghai
      - COLOR=blue-gray
      - HS_SERVER=http://headscale:8080       # IP 是headscle容器而非宿主机
      - DOMAIN_NAME=http://公网IP:8000 # 访问UI的域名
      - SCRIPT_NAME=/admin
      - KEY="....." # 生成指令: openssl rand -base64 32
      - AUTH_TYPE=Basic
      - LOG_LEVEL=info
      - BASIC_AUTH_USER=user
      - BASIC_AUTH_PASS=password
    volumes:
      - ./headscale-webui:/data:rw            # 执行 chown 1000:1000 ./headscale-webui
      - ./container-config:/etc/headscale/:ro # 这映射Headscale容器的配置文件位置


  ip-derper:
    image: ghcr.io/yangchuansheng/ip_derper:latest
    container_name: ip-derper
    restart: unless-stopped
    environment:
      - TZ=Asia/Shanghai
    network_mode: "host"

networks:
  external_net:
    external: true
```

### 1. 克隆ip_derper仓库并编译

```bash
git clone https://github.com/yangchuansheng/ip_derper.git
cd ip_derper
git clone --recurse-submodules https://github.com/tailscale/tailscale.git
docker build -t ip_derper:latest .

docker run --restart always --net host --name derper -d ghcr.io/yangchuansheng/ip_derper
```

### 2. Headscale 部署

```bash
# 或者容器化部署？
docker pull headscale/headscale:0.23.0-alpha5
git clone -b v0.23.0-alpha5  https://github.com/juanfont/headscale.git headscale-repo

mkdir -p /etc/headscale
mkdir -p /etc/headscale/conf
mkdir -p /etc/headscale/data
cd headscale-repo
cp config-example.yaml /etc/headscale/conf/config.yaml



# 常规部署
wget https://github.com/juanfont/headscale/releases/download/v0.23.0-alpha5/headscale_0.23.0-alpha5_linux_amd64
dpkg -i headscale_0.23.0-alpha5_linux_amd64
# 修改 Headscale 配置文件：
# 一定要用对应版本的配置文件 如 0.22.3
vim /etc/headscale/config.yaml
```

- 修改配置文件，将 `server_url` 改为公网 IP 或域名。**如果是国内服务器，域名必须要备案**。我的域名无法备案，所以我就直接用公网 IP 了。
- 如果暂时用不到 DNS 功能，可以先将 `magic_dns` 设为 false。
- `server_url` 设置为 `http://<PUBLIC_ENDPOINT>:8080`，将 `<PUBLIC_ENDPOINT>` 替换为公网 IP 或者域名。
- 建议打开随机端口，将 randomize_client_port 设为 true。
- 可自定义私有网段，也可同时开启 IPv4 和 IPv6：

```yaml
server_url: http://<PUBLIC_ENDPOINT>:8080
randomize_client_port: true
ip_prefixes:
  # - fd7a:115c:a1e0::/48
  - 100.64.0.0/16
```

### 3. headscale-admin部署（有bug）

```bash
# docker run -p 8000:80 --name headscale-admin -d --restart unless-stopped  goodieshq/headscale-admin:latest
docker run -p 8000:80 goodieshq/headscale-admin:latest

headscale apikey create --expiration 9999d
```

### 4. headscale-ui部署

```bash
docker pull ghcr.io/gurucomputing/headscale-ui:latest
docker run -p 8000:443 --name headscale-ui -d --restart unless-stopped  ghcr.io/gurucomputing/headscale-ui:latest
```

## 原教程

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
# -a                     指定 HTTPS 端口
# -http-port            指定 HTTP 端口
# --certmode=manual        手动指定证书文件
# --certdir                证书文件位置
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

## 参考资料

https://zhuanlan.zhihu.com/p/676818620

- 使用 ip 的 derper 容器

[GitHub - yangchuansheng/ip_derper: 无需域名的 derper](https://github.com/yangchuansheng/ip_derper)

[Tailscale 基础教程：部署私有 DERP 中继服务器 &#183; 云原生实验室](https://icloudnative.io/posts/custom-derp-servers/)

- headscale 使用教程

[Tailscale 基础教程：Headscale 的部署方法和使用教程 &#183; 云原生实验室](https://icloudnative.io/posts/how-to-set-up-or-migrate-headscale/)

- haedscale 及 webui 的容器化部署

[Docker 搭建 headscale 异地组网完整教程](https://www.nodeseek.com/post-37577-1)

https://github.com/iFargle/headscale-webui/issues/79

https://isedu.top/index.php/archives/192/
