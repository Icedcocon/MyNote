# 容器化部署ws-scrcpy

## 步骤

- 克隆仓库

```bash
git clone https://github.com/NetrisTV/ws-scrcpy.git
cd ws-scrcpy
```

- Dockerfile文件

```bash
cat >> Dockerfile <<-EOF
FROM alpine:3.14 AS builder

ADD . /ws-scrcpy
RUN apk add --no-cache git nodejs npm python3 make g++

WORKDIR /ws-scrcpy
RUN npm install
RUN npm run dist

WORKDIR dist
RUN npm install

FROM alpine:3.14 AS runner
LABEL maintainer="Vitaly Repin <vitaly.repin@gmail.com>"

RUN apk add --no-cache android-tools npm
COPY --from=builder /ws-scrcpy /root/ws-scrcpy

WORKDIR /root/ws-scrcpy
CMD ["npm", "start"]
EOF
```

- 编译镜像并启动

```bash
docker build -t wsscrcpy:v0.8.1 .
docker run --rm -i -t --privileged -v /dev/bus/usb:/dev/bus/usb -p 0.0.0.0:8000:8000/tcp wsscrcpy:v0.8.1
```

## 参考资料

- 容器化相关Pr

[Added Dockerfile and ws-scrcpy startup script by vitalyrepin · Pull Request #150 · NetrisTV/ws-scrcpy · GitHub](https://github.com/NetrisTV/ws-scrcpy/pull/150)
