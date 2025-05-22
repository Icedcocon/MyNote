## 快速开始
### 服务启动
**(1) 拉取镜像**
```bash
docker pull hujinbo23/dst-admin-go:1.5.0
```
**(2) 创建路径**
```bash
mkdir DST
cd DST
mkdir DoNotStarveTogether
mkdir app
```
**(3) 复制镜像中的文件**
```bash
docker run -itd --rm --name dst hujinbo23/dst-admin-go:1.5.0 bash
docker cp dst:/app .
docker rm -f dst
```
**(4) 配置docker-compose**
```yaml
services:
  dst-admin-go:
    image: hujinbo23/dst-admin-go:1.5.0
    restart: unless-stopped
    volumes:
      - ./DoNotStarveTogether:/root/.klei/DoNotStarveTogether
      - ./app/backup:/app/backup
      - ./app/mod:/app/mod
      - ./app/dst-admin-go.log:/app/dst-admin-go.log
      - ./app/dst-dedicated-server:/app/dst-dedicated-server
      - ./app/steamcmd:/app/steamcmd
    ports:
      - "8082:8082"
      - "10998-11018:10998-11018/udp"
```
**(5) 启动服务**
```bash
docker-compose up -d 
docker logs -f dst-dst-admin-go-1
```
### 配置 frpc 内网穿透
(1) 配置 frpc.ini
```ini
root@ubuntu-ai:/usr/local/bin/frp# cat frpc.ini
[common]
server_addr = 192.168.0.1
server_port = 7000
authentication_method = token
token = XXXXXX

[dst-udp-port-10998]
type = udp
local_ip = 127.0.0.1
local_port = 10998
remote_port = 10998

[dst-udp-port-10999]
type = udp
local_ip = 127.0.0.1
local_port = 10999
remote_port = 10999

[dst-udp-port-11000]
type = udp
local_ip = 127.0.0.1
local_port = 11000
remote_port = 11000

....
```
(2) 修改脚本
```bash
#!/bin/bash

INI_FILE="/usr/local/bin/frp/frpc.ini"  # 替换为实际文件路径
START_PORT=10998
END_PORT=11018
LOCAL_IP="127.0.0.1"
SECTION_PREFIX="dst-udp-port"

# 备份原文件
cp "$INI_FILE" "$INI_FILE.bak"

# 逐个端口追加配置
for ((port=START_PORT; port<=END_PORT; port++)); do
    SECTION="[${SECTION_PREFIX}-${port}]"
    
    # 判断 section 是否已存在
    if grep -q "$SECTION" "$INI_FILE"; then
        echo "跳过已存在的段: $SECTION"
        continue
    fi

    {
        echo ""
        echo "$SECTION"
        echo "type = udp"
        echo "local_ip = $LOCAL_IP"
        echo "local_port = $port"
        echo "remote_port = $port"
    } >> "$INI_FILE"
done

echo "端口映射已写入到 $INI_FILE（原始文件备份为 $INI_FILE.bak）"
```
## 参考资料