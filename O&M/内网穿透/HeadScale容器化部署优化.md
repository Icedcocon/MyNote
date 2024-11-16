# HeadScale 容器化部署优化

### 0. 云服务器端口开启说明

```bash
# 以下端口信息可修改，在对应位置替换即可
Derper        HTTP  端口  30080  为 headsacle 提供流量转发的端口（可配置）
Derper        HTTPS 端口  30443  为 headsacle 提供流量转发的端口（可配置）
Derper        STUN  端口  3478   在NAT、路由等网络条件允许时进行p2p连接（可配置）
Headscale     HTTP  端口  8080   用于tailscale客户端登录、注册以及管理租户（可配置）
```

### 1. IP Derper 镜像编译

> 注意： Derper 镜像编译需要注意Derp端口、host域名

- 仓库克隆

```bash
git clone https://mirror.ghproxy.com/https://github.com/yangchuansheng/ip_derper.git
cd ip_derper
git submodule update --init --recursive
vim tailscale/cmd/derper/cert.go
```

- 源码修改-注释掉以下3行代码

```go
func (m *manualCertManager) getCertificate(hi *tls.ClientHelloInfo) (*tls.Certificate, error) {
        //if hi.ServerName != m.hostname {
        //      return nil, fmt.Errorf("cert mismatch with hostname: %q", hi.ServerName)
        //}
        ....
}
```

- 安装 docker （可省略）

```bash
# step 1: 安装必要的一些系统工具
sudo apt-get update
sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
# step 2: 安装GPG证书
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
# Step 3: 写入软件源信息
sudo add-apt-repository "deb [arch=amd64] https://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
# Step 4: 更新并安装Docker-CE
sudo apt-get -y update
sudo apt-get -y install docker-ce
```

- 国内docker镜像加速

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
    "registry-mirrors": [
        "https://dockerproxy.com",
        "https://docker.mirrors.ustc.edu.cn",
        "https://docker.nju.edu.cn"
    ]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

- 修改 Dockerfile

```dockerfile
FROM golang:latest AS builder

LABEL org.opencontainers.image.source https://github.com/yangchuansheng/ip_derper

WORKDIR /app

ADD tailscale /app/tailscale

# build modified derper
RUN cd /app/tailscale/cmd/derper && \
    CGO_ENABLED=0 /usr/local/go/bin/go build -buildvcs=false -ldflags "-s -w" -o /app/derper && \
    cd /app && \
    rm -rf /app/tailscale

FROM ubuntu:20.04
WORKDIR /app

# ========= CONFIG =========
# - derper args
ENV DERP_ADDR :30443
ENV DERP_HTTP_PORT 30080
ENV STUN_PORT 3478
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
    /app/derper -hostname=$DERP_HOST \
    -certmode=manual \
    -certdir=$DERP_CERTS \
    -stun=$DERP_STUN  \
    -stun-port $STUN_PORT \
    -a=$DERP_ADDR \
    -http-port=$DERP_HTTP_PORT \
    -verify-clients=$DERP_VERIFY_CLIENTS
```

- 编译镜像（并启动）

```bash
# curl -fsSL https://get.docker.com -o get-docker.sh
docker build -t ip_derper:1.76.1 .
# 可选
docker run \
            --restart always \
            --net host \
            --name derper \
            -d ip_derper:1.76.1 # ghcr.io/yangchuansheng/ip_derper
# 服务器放行 30443 和 30080 端口
# 访问 HTTPS 端口也就是 30443 显示 This is a Tailscale DERP server.
```

## 2. Headscale 部署

- 克隆仓库并配置挂载路径

```bash
mkdir container-config
mkdir -p container-data/data
mkdir -p web
git clone -b v0.23.0  https://ghproxy.net/https://github.com/juanfont/headscale.git headscale-repo
cp headscale-repo/config-example.yaml container-config/config.yaml
cd headscale-repo
```

- 在仓库中创建 `headscale-repo/init.sh`

请将 `Caddyfile` 挂在到 headscale 容器的 `/data/Caddyfile` 路径下，否则会采用镜像内置的配置文件

```bash
#!/bin/sh

#----#
# placeholder for testing
# while true; do sleep 1; done
#----#

# check if /data/Caddyfile exists, copy across if not
if [ ! -f /data/Caddyfile ];
then
  echo "no Caddyfile detected, copying across default config"
  cp /staging/Caddyfile /data/Caddyfile
fi

echo "Starting Caddy"
/usr/sbin/caddy run --adapter caddyfile --config /data/Caddyfile 2>&1 | sed 's/^/[Caddy] /' &

sleep 1

echo "Starting headscale"
/bin/headscale serve 2>&1 | sed 's/^/[Headscale] /' &

# 等待所有后台进程
wait
```

- 镜像内置 `headscale-repo/Caddyfile`

```bash
{
        skip_install_trust
        auto_https disable_redirects
        http_port {$HTTP_PORT}
        https_port {$HTTPS_PORT}
}

:{$HTTP_PORT} {
        redir / /web
        uri strip_prefix /web
        file_server {
                root /web
        }

        reverse_proxy /api/v1/* http://headscale:8080
}

:{$HTTPS_PORT} {
        redir / /web
        uri strip_prefix /web
        tls internal {
                on_demand
        }
        file_server {
                root /web
        }
}
```

- 内置默认 `headscale-repo/derper.json`

请将 `derper.json` 挂载到容器的 `/web/derper.json` 下，否则会采用默认的

```json
{
    "Regions": {
        "901": {
            "RegionID": 901,
            "RegionCode": "My Region",
            "RegionName": "My Region Derper",
            "Nodes": [
                {
                    "Name": "Node Name",
                    "RegionID": 901,
                    "DERPPort": 12443,
                    "HostName": "<DOMAIN>",
                    "IPv4": "<IP>",
                    "InsecureForTests": true
                }
            ]
        }
    }
}
```

- Dockerfile 文件 `headscale-repo/Dockerfile`

```dockerfile
# This Dockerfile and the images produced are for testing headscale,
# and are in no way endorsed by Headscale's maintainers as an
# official nor supported release or distribution.

FROM golang:1.23-bookworm AS build
ARG VERSION=dev
ENV GOPATH /go
WORKDIR /go/src/headscale

RUN apt-get update \
  && apt-get install --no-install-recommends --yes less jq \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get clean
RUN mkdir -p /var/run/headscale

COPY go.mod go.sum /go/src/headscale/
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go install -ldflags="-s -w -X github.com/juanfont/headscale/cmd/headscale/cli.Version=$VERSION" -a ./cmd/headscale && test -e /go/bin/headscale

# Need to reset the entrypoint or everything will run as a busybox script


FROM alpine:latest

# Ports that caddy will run on
ENV HTTP_PORT="80"
ENV HTTPS_PORT="443"

# Set the staging environment
WORKDIR /staging
WORKDIR /web
WORKDIR /data

# Copy default caddy config from project root
COPY ./Caddyfile /staging/Caddyfile
COPY ./derper.json /web/derper.json
COPY ./init.sh /staging/init.sh
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
&& apk add --no-cache caddy


COPY --from=build /go/bin/headscale /bin/headscale
ENV TZ UTC

RUN mkdir -p /var/run/headscale

EXPOSE 8080/tcp

CMD ["/bin/sh", "/staging/init.sh"]
```

- 编译镜像

```bash
docker build -t headscale/headscale:0.23.0 .
```

- 配置文件 `container-config/Caddyfile`

按需修改默认文件

- 配置文件 `container-config/config.yaml`

```bash
# 将 `server_url` 改为公网 IP 或域名。
server_url: http://<PUBLIC_ENDPOINT>:8080
# 修改接受任意IP请求
listen_addr: 0.0.0.0:8080
# 如果暂时用不到 DNS 功能，可以先将 `magic_dns` 设为 false。
magic_dns: false
# 打开随机端口
randomize_client_port: false
# `ip_prefixes` 注释掉 IPV6 地址
# 修改derper配置文件地址  `derper.urls`  
derper.urls http://localhost/web/derper.json
```

- 配置文件 `docker-compose.yaml`

```yaml
version: '3'

services:
  headscale:
    image: headscale/headscale:0.23.0
    container_name: headscale
    restart: unless-stopped
    environment:
      - TZ=Asia/Shanghai
    volumes:
      - ./container-config:/etc/headscale
      - ./container-data/data:/var/lib/headscale
      - ./Caddyfile:/data/Caddyfile
      - ./derper.json:/web/derper.json
    ports:
      - 8080:8080
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    sysctls:
      - net.ipv4.ip_forward=1
```

- 启动

```bash
docker-compose up -d 
```

补充说明

```go
type DERPNode struct {
    // Name is a unique node name (across all regions).
    // It is not a host name.
    // It's typically of the form "1b", "2a", "3b", etc. (region
    // ID + suffix within that region)
    Name string

    // RegionID is the RegionID of the DERPRegion that this node
    // is running in.
    RegionID int

    // HostName is the DERP node's hostname.
    //
    // It is required but need not be unique; multiple nodes may
    // have the same HostName but vary in configuration otherwise.
    HostName string

    // CertName optionally specifies the expected TLS cert common
    // name. If empty, HostName is used. If CertName is non-empty,
    // HostName is only used for the TCP dial (if IPv4/IPv6 are
    // not present) + TLS ClientHello.
    CertName string `json:",omitempty"`

    // IPv4 optionally forces an IPv4 address to use, instead of using DNS.
    // If empty, A record(s) from DNS lookups of HostName are used.
    // If the string is not an IPv4 address, IPv4 is not used; the
    // conventional string to disable IPv4 (and not use DNS) is
    // "none".
    IPv4 string `json:",omitempty"`

    // IPv6 optionally forces an IPv6 address to use, instead of using DNS.
    // If empty, AAAA record(s) from DNS lookups of HostName are used.
    // If the string is not an IPv6 address, IPv6 is not used; the
    // conventional string to disable IPv6 (and not use DNS) is
    // "none".
    IPv6 string `json:",omitempty"`

    // Port optionally specifies a STUN port to use.
    // Zero means 3478.
    // To disable STUN on this node, use -1.
    STUNPort int `json:",omitempty"`

    // STUNOnly marks a node as only a STUN server and not a DERP
    // server.
    STUNOnly bool `json:",omitempty"`

    // DERPPort optionally provides an alternate TLS port number
    // for the DERP HTTPS server.
    //
    // If zero, 443 is used.
    DERPPort int `json:",omitempty"`

    // InsecureForTests is used by unit tests to disable TLS verification.
    // It should not be set by users.
    InsecureForTests bool `json:",omitempty"`

    // STUNTestIP is used in tests to override the STUN server's IP.
    // If empty, it's assumed to be the same as the DERP server.
    STUNTestIP string `json:",omitempty"`

    // CanPort80 specifies whether this DERP node is accessible over HTTP
    // on port 80 specifically. This is used for captive portal checks.
    CanPort80 bool `json:",omitempty"`
}
```

## 参考资料
