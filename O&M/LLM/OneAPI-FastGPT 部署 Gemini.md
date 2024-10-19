# OneAPI-FastGPT 部署 Gemini

## 准备环境

### 1. 下载配置文件

```bash
mkdir fastgpt
cd fastgpt
curl -O https://raw.githubusercontent.com/labring/FastGPT/main/files/deploy/fastgpt/docker-compose.yml
curl -O https://raw.githubusercontent.com/labring/FastGPT/main/projects/app/data/config.json

openssl rand -base64 756 > ./mongodb.key
# 600不行可以用chmod 999
chmod 600 ./mongodb.key
chown 999:root ./mongodb.key
```

### 2. 拉取镜像（可选）

```bash
docker pull ankane/pgvector:v0.5.0
docker pull mongo:5.0.18
docker pull ghcr.io/labring/fastgpt:v4.6.8
docker pull justsong/one-api:v0.5.11
```

### 3.修改配置文件

- docker-compose.yml

```yaml
# 非 host 版本, 不使用本机代理
# (不懂 Docker 的，只需要关心 OPENAI_BASE_URL 和 CHAT_API_KEY 即可！)
version: '3.3'
services:
  pg:
    image: ankane/pgvector:v0.5.0 # git
    # image: registry.cn-hangzhou.aliyuncs.com/fastgpt/pgvector:v0.5.0 # 阿里云
    container_name: pg
    restart: always
    ports: # 生产环境建议不要暴露
      - 5432:5432
    networks:
      - fastgpt
    environment:
      # 这里的配置只有首次运行生效。修改后，重启镜像是不会生效的。需要把持久化数据删除再重启，才有效果
      - POSTGRES_USER=username
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=postgres
    volumes:
      - ./pg/data:/var/lib/postgresql/data
  mongo:
    image: mongo:5.0.18
    # image: registry.cn-hangzhou.aliyuncs.com/fastgpt/mongo:5.0.18 # 阿里云
    container_name: mongo
    restart: always
    privileged: true
    ports:
      - 27017:27017
    networks:
      - fastgpt
    command: mongod --keyFile /data/mongodb.key --replSet rs0
    environment:
      # 默认的用户名和密码，只有首次允许有效
      - MONGO_INITDB_ROOT_USERNAME=myname
      - MONGO_INITDB_ROOT_PASSWORD=mypassword
    volumes:
      - ./mongo/data:/data/db
      - ./mongodb.key:/data/mongodb.key
  fastgpt:
    container_name: fastgpt
    image: ghcr.io/labring/fastgpt:v4.6.8 # git
    # image: registry.cn-hangzhou.aliyuncs.com/fastgpt/fastgpt:latest # 阿里云
    ports:
      - 3000:3000
    networks:
      - fastgpt
    depends_on:
      - mongo
      - pg
    restart: always
    environment:
      # root 密码，用户名为: root
      - DEFAULT_ROOT_PSW=1234
      # 中转地址，如果是用官方号，不需要管。务必加 /v1
      - OPENAI_BASE_URL=http://one-api:3000/v1
      - CHAT_API_KEY=sk-KezPg1YHM5h1Ocnv44Bc3644642a405189B1FeDd344b50Bd
      - DB_MAX_LINK=5 # database max link
      - TOKEN_KEY=any
      - ROOT_KEY=root_key
      - FILE_TOKEN_KEY=filetoken
      # mongo 配置，不需要改. 用户名myname,密码mypassword。
      - MONGODB_URI=mongodb://myname:mypassword@mongo:27017/fastgpt?authSource=admin
      # pg配置. 不需要改
      - PG_URL=postgresql://username:password@pg:5432/postgres
    volumes:
      - ./config.json:/app/data/config.json
  one-api:
    container_name: one-api
    image: justsong/one-api:v0.5.11
    ports:
      - 3001:3000
    networks:
      - fastgpt
    restart: always
    environment:
      - TZ=Asia/Shanghai
    volumes:
      - ./one-api-data:/data
networks:
  fastgpt:
```

- config.json

```json
  "llmModels": [
    {
      "model": "gemini-pro",
      "name": "gemini-pro",
      "maxContext": 16000,
      "maxResponse": 4000,
      "quoteMaxToken": 13000,
      "maxTemperature": 1.2,
      "charsPointsPrice": 0,
      "censor": false,
      "vision": false,
      "datasetProcess": false,
      "toolChoice": true,
      "functionCall": false,
      "customCQPrompt": "",
      "customExtractPrompt": "",
      "defaultSystemChatPrompt": "",
      "defaultConfig": {}
    },
    {
      "model": "gemini-pro-vision",
      "name": "gemini-pro-vision",
      "maxContext": 128000,
      "maxResponse": 4000,
      "quoteMaxToken": 100000,
      "maxTemperature": 1.2,
      "charsPointsPrice": 0,
      "censor": false,
      "vision": true,
      "datasetProcess": false,
      "toolChoice": true,
      "functionCall": false,
      "customCQPrompt": "",
      "customExtractPrompt": "",
      "defaultSystemChatPrompt": "",
      "defaultConfig": {}
    }
  ],
```

### 5. 初始化MangoDB副本集

```bash
# 查看 mongo 容器是否正常运行
docker ps
# 进入容器
docker exec -it mongo bash

# 连接数据库
mongo -u myname -p mypassword --authenticationDatabase admin

# 初始化副本集。如果需要外网访问，mongo:27017 可以改成 ip:27017。但是需要同时修改 FastGPT 连接的参数（MONGODB_URI=mongodb://myname:mypassword@mongo:27017/fastgpt?authSource=admin => MONGODB_URI=mongodb://myname:mypassword@ip:27017/fastgpt?authSource=admin）
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo:27017" }
  ]
})
# 检查状态。如果提示 rs0 状态，则代表运行成功
rs.status()
```
