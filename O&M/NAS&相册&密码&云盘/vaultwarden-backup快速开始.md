# vaultwarden-backup 快速开始

> 建议使用非 root 账号操作

## 开始

### 1. 安装

#### 1.1 环境准备

- 安装 `rclone`

```bash
apt install rclone
```

- 下载 `docker-compose.yaml` 和 `.env`

```bash
mkdir ./vaultwarden-backup
cd ./vaultwarden-backup
curl -fsSL https://raw.githubusercontent.com/ttionya/vaultwarden-backup/master/docker-compose.yml -o ./docker-compose.yml
curl -fsSL https://raw.githubusercontent.com/ttionya/vaultwarden-backup/master/.env -o ./.env
```

- 下载 `docker-compose-v2` （可选）

```bash
curl -L "https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

### 2. 配置 vaultwarden（废弃）

#### 2.1 配置 rclone 及卷 vaultwarden-rclone-data

- 创建 volume

由于在docker-compose中显示为外置，因此需要手动创建并配置

```bash
docker volume create vaultwarden-rclone-data
```

- 进行配置

```bash
docker run --rm -it \
  --mount type=volume,source=vaultwarden-rclone-data,target=/config/ \
  ttionya/vaultwarden-backup:1.21.2 \
  rclone config
```

- rclone配置过程

```bash
2024/11/16 15:56:35 NOTICE: Config file "/config/rclone/rclone.conf" not found - using defaults
No remotes found, make a new one?
n) New remote
s) Set configuration password
q) Quit config
n/s/q> n

Enter name for new remote.
name> BitwardenBackup

Option Storage.
Type of storage to configure.
Choose a number from below, or type in your own value.
Storage> 46

Option host.
SMB server hostname to connect to.
E.g. "example.com".
Enter a value.
host> ${YOUR_SMB_SERVER_IP}

Option user.
SMB username.
Enter a value of type string. Press Enter for the default (root).
user> ${YOUR_SMB_USER}

Option port.
SMB port number.
Enter a signed integer. Press Enter for the default (445).
port>

Option pass.
SMB password.
Choose an alternative below. Press Enter for the default (n).
y) Yes, type in my own password
g) Generate random password
n) No, leave this optional password blank (default)
y/g/n> y
Enter the password:
password:
Confirm the password:
password:

Option domain.
Domain name for NTLM authentication.
Enter a value of type string. Press Enter for the default (WORKGROUP).
domain>

Option spn.
Service principal name.
Rclone presents this name to the server. Some servers use this as further
authentication, and it often needs to be set for clusters. For example:
    cifs/remotehost:1020
Leave blank if not sure.
Enter a value. Press Enter to leave empty.
spn>

Edit advanced config?
y) Yes
n) No (default)
y/n> n
```

- 配置测试

```bash
# 测试路径 /BitwardenBackup/ 是否存在
docker run --rm -it   --mount type=volume,source=vaultwarden-rclone-data,target=/config/   ttionya/vaultwarden-backup:1.21.2   rclone lsd BitwardenBackup:/BitwardenBackup/

# 测试该SMB账号可以使用哪些路径
docker run --rm -it   --mount type=volume,source=vaultwarden-rclone-data,target=/config/   ttionya/vaultwarden-backup:1.21.2   rclone lsd BitwardenBackup:

# 递归展示所有文件
docker run --rm -it   --mount type=volume,source=vaultwarden-rclone-data,target=/config/   ttionya/vaultwarden-backup:1.21.2   rclone ls BitwardenBackup:/BitwardenBackup/

# 创建文件
docker run --rm -it   --mount type=volume,source=vaultwarden-rclone-data,target=/config/   ttionya/vaultwarden-backup:1.21.2   rclone touch BitwardenBackup:/BitwardenBackup/test.txt
```

#### 2.2 配置docker-compose.yaml 及环境变量

- 环境变量配置 .env

```bash
RCLONE_REMOTE_NAME="BitwardenBackup"
RCLONE_REMOTE_DIR="/BitwardenBackup/"
# RCLONE_GLOBAL_FLAG=""
# 每晚凌晨1点备份
CRON="0 1 * * *"
ZIP_ENABLE="TRUE"
ZIP_PASSWORD="WHEREISMYPASSWORD?"
ZIP_TYPE="zip"
BACKUP_FILE_SUFFIX="%Y%m%d"
BACKUP_KEEP_DAYS="365"
# PING_URL=""
# PING_URL_CURL_OPTIONS=""
# PING_URL_WHEN_START=""
# PING_URL_WHEN_START_CURL_OPTIONS=""
# PING_URL_WHEN_SUCCESS=""
# PING_URL_WHEN_SUCCESS_CURL_OPTIONS=""
# PING_URL_WHEN_FAILURE=""
# PING_URL_WHEN_FAILURE_CURL_OPTIONS=""
# MAIL_SMTP_ENABLE="FALSE"
# MAIL_SMTP_VARIABLES=""
# MAIL_TO=""
# MAIL_WHEN_SUCCESS="TRUE"
# MAIL_WHEN_FAILURE="TRUE"
# TIMEZONE="UTC"
```

- docker-commpose.yaml

```yaml
version: '3.4'

services:

  vaultwarden:
    image: vaultwarden/server:1.32.4
    restart: always
    environment:
      DOMAIN: 'https://your domain'
      LOGIN_RATELIMIT_SECONDS: '1'
      SIGNUPS_ALLOWED: 'false'
      ADMIN_TOKEN: 'your authentication token'
    ports:
      - '0.0.0.0:8200:80'
    volumes:
      - vaultwarden-data:/data/

  backup:
    image: ttionya/vaultwarden-backup:1.21.2
    restart: always
    # environment:
    #   RCLONE_REMOTE_NAME: 'BitwardenBackup'
    #   RCLONE_REMOTE_DIR: '/BitwardenBackup/'
    #   RCLONE_GLOBAL_FLAG: ''
    #   CRON: '5 * * * *'
    #   ZIP_ENABLE: 'TRUE'
    #   ZIP_PASSWORD: 'WHEREISMYPASSWORD?'
    #   ZIP_TYPE: 'zip'
    #   BACKUP_FILE_SUFFIX: '%Y%m%d'
    #   BACKUP_KEEP_DAYS: 0
    #   PING_URL: ''
    #   PING_URL_CURL_OPTIONS: ''
    #   PING_URL_WHEN_START: ''
    #   PING_URL_WHEN_START_CURL_OPTIONS: ''
    #   PING_URL_WHEN_SUCCESS: ''
    #   PING_URL_WHEN_SUCCESS_CURL_OPTIONS: ''
    #   PING_URL_WHEN_FAILURE: ''
    #   PING_URL_WHEN_FAILURE_CURL_OPTIONS: ''
    #   MAIL_SMTP_ENABLE: 'FALSE'
    #   MAIL_SMTP_VARIABLES: ''
    #   MAIL_TO: ''
    #   MAIL_WHEN_SUCCESS: 'TRUE'
    #   MAIL_WHEN_FAILURE: 'TRUE'
    #   TIMEZONE: 'UTC'
    volumes:
      - vaultwarden-data:/bitwarden/data/
      - vaultwarden-rclone-data:/config/
      - .env:/.env

volumes:
  vaultwarden-data:
    # Specify the name of the volume where you save the vaultwarden data,
    # use vaultwarden-data for new users
    # and bitwardenrs-data for migrated users
    name: vaultwarden-data
    # name: bitwardenrs-data
  vaultwarden-rclone-data:
    external: true
    # Specify the name of the volume where you save the rclone configuration,
    # use vaultwarden-rclone-data for new users
    # and bitwardenrs-rclone-data for migrated users
    name: vaultwarden-rclone-data
    # name: bitwardenrs-rclone-data
```

- 生成密钥作为admin密码

```bash
openssl rand -base64 32
```

### 3  配置 vaultwarden（使用路径）

#### 3.1 配置 rclone 及卷 vaultwarden-rclone-data

- 进行配置

```bash
docker run --rm -it \
  -v ./vw-rclone-data/:/config/ \
  ttionya/vaultwarden-backup:1.21.2 \
  rclone config
```

- rclone配置过程

```bash
2024/11/16 15:56:35 NOTICE: Config file "/config/rclone/rclone.conf" not found - using defaults
No remotes found, make a new one?
n) New remote
s) Set configuration password
q) Quit config
n/s/q> n

Enter name for new remote.
name> BitwardenBackup

Option Storage.
Type of storage to configure.
Choose a number from below, or type in your own value.
Storage> 46

Option host.
SMB server hostname to connect to.
E.g. "example.com".
Enter a value.
host> ${YOUR_SMB_SERVER_IP}

Option user.
SMB username.
Enter a value of type string. Press Enter for the default (root).
user> ${YOUR_SMB_USER}

Option port.
SMB port number.
Enter a signed integer. Press Enter for the default (445).
port>

Option pass.
SMB password.
Choose an alternative below. Press Enter for the default (n).
y) Yes, type in my own password
g) Generate random password
n) No, leave this optional password blank (default)
y/g/n> y
Enter the password:
password:
Confirm the password:
password:

Option domain.
Domain name for NTLM authentication.
Enter a value of type string. Press Enter for the default (WORKGROUP).
domain>

Option spn.
Service principal name.
Rclone presents this name to the server. Some servers use this as further
authentication, and it often needs to be set for clusters. For example:
    cifs/remotehost:1020
Leave blank if not sure.
Enter a value. Press Enter to leave empty.
spn>

Edit advanced config?
y) Yes
n) No (default)
y/n> n
```

- 配置测试

```bash
# 测试路径 /BitwardenBackup/ 是否存在
docker run --rm -it -v ./vw-rclone-data/:/config/ ttionya/vaultwarden-backup:1.21.2 rclone lsd BitwardenBackup:/BitwardenBackup/

# 测试该SMB账号可以使用哪些路径
docker run --rm -it -v ./vw-rclone-data/:/config/ ttionya/vaultwarden-backup:1.21.2 rclone lsd BitwardenBackup:

# 递归展示所有文件
docker run --rm -it -v ./vw-rclone-data/:/config/ ttionya/vaultwarden-backup:1.21.2 rclone ls BitwardenBackup:/BitwardenBackup/

# 创建文件
docker run --rm -it -v ./vw-rclone-data/:/config/ ttionya/vaultwarden-backup:1.21.2 rclone touch BitwardenBackup:/BitwardenBackup/test.txt
```

#### 2.2 配置docker-compose.yaml 及环境变量

- 环境变量配置 .env

```bash
RCLONE_REMOTE_NAME="BitwardenBackup"
RCLONE_REMOTE_DIR="/BitwardenBackup/"
# RCLONE_GLOBAL_FLAG=""
# 每晚凌晨1点备份
CRON="0 1 * * *"
ZIP_ENABLE="TRUE"
ZIP_PASSWORD="WHEREISMYPASSWORD?"
ZIP_TYPE="zip"
BACKUP_FILE_SUFFIX="%Y%m%d"
BACKUP_KEEP_DAYS="365"
# PING_URL=""
# PING_URL_CURL_OPTIONS=""
# PING_URL_WHEN_START=""
# PING_URL_WHEN_START_CURL_OPTIONS=""
# PING_URL_WHEN_SUCCESS=""
# PING_URL_WHEN_SUCCESS_CURL_OPTIONS=""
# PING_URL_WHEN_FAILURE=""
# PING_URL_WHEN_FAILURE_CURL_OPTIONS=""
# MAIL_SMTP_ENABLE="FALSE"
# MAIL_SMTP_VARIABLES=""
# MAIL_TO=""
# MAIL_WHEN_SUCCESS="TRUE"
# MAIL_WHEN_FAILURE="TRUE"
# TIMEZONE="UTC"
```

- docker-commpose.yaml

```yaml
version: '3.4'

services:

  vaultwarden:
    image: vaultwarden/server:1.32.4
    restart: always
    environment:
      DOMAIN: 'https://your domain'
      LOGIN_RATELIMIT_SECONDS: '1'
      SIGNUPS_ALLOWED: 'false'
      ADMIN_TOKEN: 'your authentication token'
    ports:
      - '0.0.0.0:8200:80'
    volumes:
      - ./vw-data:/data/

  backup:
    image: ttionya/vaultwarden-backup:1.21.2
    restart: always
    # environment: "use .env file"
    volumes:
      - ./vw-data:/bitwarden/data/
      - ./vw-rclone-data:/config/
      - .env:/.env
```

- 生成密钥作为admin密码

```bash
openssl rand -base64 32
```

### 3.环境变量说明

#### 3.1. 数据存储相关

- DATA_FOLDER: 主数据文件夹路径

- DATABASE_URL: 数据库连接地址,支持 SQLite/MySQL/PostgreSQL

- DATABASE_MAX_CONNS: 数据库最大连接数

- ICON_CACHE_FOLDER: 图标缓存文件夹

- ATTACHMENTS_FOLDER: 附件存储文件夹

#### 3.2. 服务配置

- DOMAIN: 服务访问域名,建议配置以确保功能正常

- ROCKET_PORT: 服务监听端口(默认8000)

- ROCKET_ADDRESS: 服务监听地址(默认0.0.0.0)

- WEB_VAULT_ENABLED: 是否启用Web界面

- ADMIN_TOKEN: 管理界面访问令牌

- LOG_LEVEL: 日志级别设置

#### 3.3. 用户注册相关

- SIGNUPS_ALLOWED: 是否允许新用户注册

- SIGNUPS_VERIFY: 是否要求邮箱验证

- SIGNUPS_DOMAINS_WHITELIST: 允许注册的邮箱域名白名单

- INVITATIONS_ALLOWED: 是否允许邀请新用户

#### 3.4. 邮件服务配置

- SMTP_HOST: SMTP服务器地址

- SMTP_FROM: 发件人地址

- SMTP_PORT: SMTP端口

- SMTP_SECURITY: SMTP安全连接类型(starttls/force_tls/off)

- SMTP_USERNAME: SMTP用户名

- SMTP_PASSWORD: SMTP密码

#### 3.5. 安全相关

- IP_HEADER: 客户端IP识别头

- LOGIN_RATELIMIT_SECONDS: 登录速率限制

- PASSWORD_ITERATIONS: 密码哈希迭代次数

- DISABLE_2FA_REMEMBER: 是否禁用2FA记住功能

#### 3.6. 组织与权限

- ORG_CREATION_USERS: 控制哪些用户可以创建组织

- ORG_EVENTS_ENABLED: 是否启用组织事件日志

- ORG_ATTACHMENT_LIMIT: 组织附件存储限制

- EMERGENCY_ACCESS_ALLOWED: 是否允许紧急访问功能

### 3. 配置 nginx proxy manager

- 拉去镜像

```bash
docker pull jc21/nginx-proxy-manager:2.12.1
```

- docker-compose

> 其中81是管理端口，访问管理端口进行配置后请用防火墙关闭

```yaml
services:
  app:
    image: 'jc21/nginx-proxy-manager:2.12.1'
    restart: unless-stopped
    ports:
      - '80:80'
      - '81:81'
      - '443:443'
    volumes:
      - ./data:/data
      - ./letsencrypt:/etc/letsencrypt
```

## 参考资料

[1.配置概述 | Vaultwarden Wiki 中文版](https://rs.ppgg.in/configuration/configuration-overview)
