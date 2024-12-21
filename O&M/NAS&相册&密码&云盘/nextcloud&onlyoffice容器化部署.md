# nextcloud & onlyoffice 容器化部署

## 开始

### 1. docker-compose.yaml

#### 1.1 变量

```bash
# 路径配置
NEXTCLOUD_DATA_DIR=/NextCloud/nextcloud
ONLYOFFICEDATA_DIR=./onlyoffice/data
ONLYOFFICE_LOG_DIR=./onlyoffice/logs
MYSQL_DATA_DIR=./mysql
NGINX_CONF_PATH=./nginx.conf

# 端口配置
NEXTCLOUD_HTTP_PORT=2380
NEXTCLOUD_HTTPS_PORT=4433
ONLYOFFICE_HTTP_PORT=2280
ONLYOFFICE_HTTPS_PORT=4423

# OnlyOffice配置
JWT_ENABLED=true
JWT_SECRET=root123456

# 数据库配置
MYSQL_ROOT_PASSWORD=Mysql123
MYSQL_PASSWORD=Msql123
MYSQL_DATABASE=nextcloud
MYSQL_USER=nextcloud
```

#### 1.2 配置

```yaml
version: '3'
services:
  app:
    container_name: app-server
    image: nextcloud:fpm
    stdin_open: true
    tty: true
    restart: always
    expose:
      - '80'
      - '9000'
    networks:
      - onlyoffice
    volumes:
      - ${NEXTCLOUD_DATA_DIR}:/var/www/html

  onlyoffice-document-server:
    container_name: onlyoffice-document-server
    image: onlyoffice/documentserver:latest
    stdin_open: true
    tty: true
    restart: always
    networks:
      - onlyoffice
    expose:
      - '80'
      - '443'
    volumes:
      - ${ONLYOFFICE_DATA_DIR}:/var/www/onlyoffice/Data
      - ${ONLYOFFICE_LOG_DIR}:/var/log/onlyoffice
    ports:
      - ${ONLYOFFICE_HTTP_PORT}:80
      - ${ONLYOFFICE_HTTPS_PORT}:443
    environment:
      - JWT_ENABLED=${JWT_ENABLED}
      - JWT_SECRET=${JWT_SECRET}

  nginx:
    container_name: nginx-server
    image: nginx
    stdin_open: true
    tty: true
    restart: always
    ports:
      - ${NEXTCLOUD_HTTP_PORT}:80
      - ${NEXTCLOUD_HTTPS_PORT}:443
    networks:
      - onlyoffice
    volumes:
      - ${NGINX_CONF_PATH}:/etc/nginx/nginx.conf
      - ${NEXTCLOUD_DATA_DIR}:/var/www/html

  db:
    container_name: mariadb
    image: mariadb
    restart: always
    volumes:
      - ${MYSQL_DATA_DIR}:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
      - MYSQL_PASSWORD=${MYSQL_PASSWORD}
      - MYSQL_DATABASE=${MYSQL_DATABASE}
      - MYSQL_USER=${MYSQL_USER}
    networks:
      - onlyoffice

networks:
  onlyoffice:
    driver: 'bridge'
```

#### 1.3 创建路径及文件

```bash
# 创建所需目录
mkdir -p $(grep '_DIR=' .env | cut -d '=' -f2)
```

- 创建 `nginx.conf`

### 2. 页面配置

- 访问 `http://192.168.10.20:2280` onlyoffice页面

- 访问`http://192.168.10.20:2380` nextcloud页面

## 参考资料

- 博客

[Docker搭建nextcloud网盘-配合onlyoffice使用-实现在线编辑office-协同办公](https://www.ywsj365.com/archives/docker-da-jian-nextcloud-wang-pan---pei-he-onlyoffice-shi-yong---shi-xian-zai-xian-bian-ji-office--xie-tong-ban-gong#google_vignette)
