### 1. 云服务器安装FRPS

- 云服务器开启至少两个端口
  
  - (1) 端口 7000 FRP服务端默认端口号
  - (2) 端口 6000 FRP客户端（内网服务器）映射端口，本次映射22(SSH)到6000

- 前往 https://github.com/fatedier/frp/releases 下载 `frp_0.49.0_linux_amd64.tar.gz`

```bash
wget https://github.com/fatedier/frp/releases/download/v0.54.0/frp_0.54.0_linux_amd64.tar.gz

tar -xzf frp_0.54.0_linux_amd64.tar.gz
mv frp_0.54.0_linux_amd64 /usr/local/bin/frp
chmod +x /usr/local/bin/frp/frps 
```

- 修改 `frps.ini` 配置文件，常用配置项如下

```bash
[common]
bind_port = 7000                         # frp服务的端口号，可改 (必填)
dashboard_port = 7500                    # frp的web界面的端口号，可改
dashboard_user = admin                   # web界面的登陆账户，可改
dashboard_pwd = ********                 # web界面的登陆密码，可改
authentication_method = token            #                     (最好填)
token = *******************************  # frp客户端连接时的密码，可改
vhost_http_port = 8080                   # 为frp指定的http端口
vhost_https_port = 8443                  # 为frp指定的https端口
```

- 在 `/etc/systemd/system/frps.service` 添加开机启动脚本

```bash
[Unit]
Description=Frp Server Daemon
After=syslog.target network.target
Wants=network.target
[Service]
Type=simple
ExecStart=/usr/local/bin/frp/frps -c /usr/local/bin/frp/frps.ini 
ExecStop=/usr/bin/killall frps
RestartSec=1min
KillMode=control-group
Restart=always
[Install]
WantedBy=multi-user.target 
```

- 执行以下指令启动FRP服务、设置开机自启并查看服务状态

```bash
sudo systemctl enable frps.service  # 开机自启
sudo systemctl start frps.service   # 启动服务
sudo systemctl status frps.service  # 查看服务状态
```

### 2. 内网服务器安装FRPC

- 前往 https://github.com/fatedier/frp/releases 下载 `frp_0.49.0_linux_amd64.tar.gz`

```bash
wget https://github.com/fatedier/frp/releases/download/v0.49.0/frp_0.49.0_linux_amd64.tar.gz

tar -xzf frp*.tar.gz && rm -f frp*.tar.gz
mv frp* /usr/local/bin/frp
chmod +x /usr/local/bin/frp/frpc
```

- 修改 `frpc.ini` 配置文件，常用配置项如下

```bash
[common]
server_addr = ****************     # 云服务器的公网ip (必填)
authentication_method = token
token = ************************** # 服务端frp连接密码
server_port = 7000                 # 服务端frp服务端口 (必填)
[example]
type = tcp
local_ip = 127.0.0.1               # 内网服务器在局域网的ip (必填)
local_port = 22                    # 内网需要穿透的端口 (必填)
remote_port = 6000                 # 外网映射端口  (必填)
```

```toml

```

- 在 `/etc/systemd/system/frpc.service` 添加开机启动脚本

```bash
[Unit]
Description=Frp Server Daemon
After=syslog.target network.target
Wants=network.target
[Service]
Type=simple
ExecStart=/usr/local/bin/frp/frpc -c /usr/local/bin/frp/frpc.ini 
ExecStop=/usr/bin/killall frpc
RestartSec=1min
KillMode=control-group
Restart=always
[Install]
WantedBy=multi-user.target 
```

- 执行以下指令启动FRP服务、设置开机自启并查看服务状态

```bash
sudo systemctl enable frpc.service  # 开机自启
sudo systemctl start frpc.service   # 启动服务
sudo systemctl status frpc.service  # 查看服务状态
```

### 3. 为内网http服务启用https

申请对应域名的证书，在本地服务器frp目录下新建/cert文件夹，上传nginx格式的ssl证书；

公网frps服务端必须指定https端口，如和nginx冲突，可指定其他端口；

修改frpc配置文件，重启frpc服务：

```bash
[https-example]
type = https    # 类型选择https，穿透出去使用公网frps指定的https端口
custom_domains = yourdomain  # 域名
plugin = https2http                       # 插件，将https请求转换为http请求
plugin_local_addr = 127.0.0.1:**** # 本地需要启用https服务的端口
plugin_crt_path = /usr/local/bin/frp/cert/***.pem # SSL证书地址
plugin_key_path = /usr/local/bin/frp/cert/***.key # SSL证书密钥
plugin_host_header_rewrite = 127.0.0.1
plugin_header_X-From-Where = frp 
```

## gost 端口转发

- 下载 gost

```bash
snap install gost
```

- 编辑 `/lib/systemd/system/gost.service`

```bash
[Unit]
Description=gost service
After=network.target

[Service]
Type=simple
User=root
ExecStart=/snap/bin/gost -L=tcp://:10082/<目标IP>:8081
ExecStop=/usr/bin/killall gost
Restart=always

[Install]
WantedBy=multi-user.target
```

- 启动服务

```bash
sudo systemctl enable gost.service  # 开机自启
sudo systemctl start gost.service   # 启动服务
sudo systemctl status gost.service  # 查看服务状态
```
