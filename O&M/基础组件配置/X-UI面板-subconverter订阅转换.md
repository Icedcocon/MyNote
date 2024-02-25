# X-UI面板安装

### 1、购买服务器并解析域名： (https://dash.cloudflare.com/login)

- 创建一个子域名  A 记录

- 27640
  P6WTpG31NdFW

### 2、一键安装依赖包（适合Ubuntu/Debian系统，不一定需要）

```
apt update -y&&apt install -y curl&&apt install -y socat
```

### 3、安装X3-ui面板： (https://github.com/MHSanaei/3x-ui) 注意：建议用Debian或者Ubuntu系统

```
bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)
```

- 放行端口：选择20，然后输入你想放行的端口（端口要先放行，不然下面申请证书会报错）

- 安装证书：选择16，输入你解析好的域名

- 启用BBR加速：选择21（如果想单独安装，用下面的命令）

```
wget -N --no-check-certificate "https://raw.githubusercontent.com/chiakge/Linux-NetSpeed/master/tcp.sh" && chmod +x tcp.sh && ./tcp.sh
```

### 4、进入UI并配置公钥

- 在浏览器键入 IP:放行的第3个端口

- 输入用户名和密码

- 进入面板设置

```bash
# 公钥路径
/root/cert/***/fullchain.pem
# 私钥路径
/root/cert/****/privkey.pem
# 面板根路径
/mygia
```

- 点击保存配置-重启面板

- 输入域名:端口/mygia

### 5、配置入站列表

- 选择vless

- 端口选择443

- 安全选择 reality

- get new cert 

- 添加

# Subconverter订阅转换

### 1. 下载安装包

```bash
 wget https://github.com/tindy2013/subconverter/releases/download/v0.8.1/subconverter_armv7.tar.gz
tar -xzf subconverter_armv7.tar.gz
mv subconverter /usr/local/bin/
```

### 2. 配置systemctl

- 编辑 `/lib/systemd/system/subconverter.service`

```bash
[Unit]
Description=subconverter service

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/subconverter/subconverter
ExecStop=/usr/bin/killall subconverter
Restart=always

[Install]
WantedBy=multi-user.target
```

### 3. 转换

- 修改 `profiles/my_profile.ini` 文件

- 访问 `http://127.0.0.1:25500/getprofile?name=profiles/my_profile.ini&token=password`

# subscription converter

```bash
docker run -d -p 58080:80 --restart always --name subweb careywong/subweb:latest
```
