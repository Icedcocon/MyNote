### 1. 下载 Clash 及配置

- 下载clash
  - `https://github.com/Dreamacro/clash/releases`

```bash
cd && mkdir clash  # 在用户目录下创建 clash 文件夹
# 访问 https://github.com/Dreamacro/clash/releases 获取最新二进制文件
wget https://github.com/Dreamacro/clash/releases/download/v1.16.0/clash-linux-amd64-v3-v1.16.0.gz
gzip -d  clash-linux-amd64-v3-v1.16.0.gz
mv clash* /clash/clash
cd clash
# 下载配置文件
wget -O config.yaml https://****
chmod +x clash
cd ..
mv clash /usr/local/bin/
```

- 配置 config.yaml

```bash
port: 7890
socks-port: 7891
allow-lan: true
mode: Rule
log-level: info
secert: 123456 #  clash dashboard 密码
# external-ui: dashboard # UI程序，容器不需要
external-controller: 0.0.0.0:9090 # dashboard 访问的端口
```

- 配置 clash 服务
  - `vim /etc/systemd/system/clash.service`
  - `systemctl start clash.service`
  - `systemctl enable clash.service`
  - stop 后可能会断连数分钟

```bash
[Unit]
Description=clash service
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/clash/clash -d /usr/local/bin/clash
ExecStop=/usr/bin/killall frpc
Restart=always

[Install]
WantedBy=multi-user.target
```

### 2. 下载yacd clashboard

- 下载 yacd
  
  - `https://github.com/haishanh/yacd`
  
  - `https://hub.docker.com/r/haishanh/yacd`

```bash
docker run -p 10081:80 -d --name dashboard --restart=always ghcr.io/haishanh/yacd:master
```

### 3. 配置系统代理

- `vim /etc/bash.bashrc`

```bash
proxy_on() {
    export https_proxy=http://127.0.0.1:7890
    export http_proxy=http://127.0.0.1:7890
    export all_proxy=socks5://127.0.0.1:7891
    export no_proxy="localhost,127.0.0.1,::1"
    #echo 'Acquire::http::Proxy "http://127.0.0.1:7890"'  >  /etc/apt/apt.conf
    #echo 'Acquire::https::Proxy "http://127.0.0.1:7890"' >> /etc/apt/apt.conf
    echo "HTTP/HTTPS Proxy on"
}

# Close proxy
proxy_off() {
    unset http_proxy
    unset https_proxy
    unset all_proxy
    unset no_proxy
    echo "HTTP/HTTPS Proxy off"
}
```
