# Xinference-Ragflow部署指南

### xinference

- 克隆仓库并编译

```bash
git clone https://github.com/xorbitsai/inference.git
cd inference
git fetch origin v0.11.1:v0.11.1
git checkout v0.11.1
docker build --progress=plain -t xinference:v0.11.1 -f xinference/deploy/docker/Dockerfile .
```

### ragflow

- 克隆仓库并编译

```bash
git clone https://github.com/infiniflow/ragflow.git
cd ragflow/
docker build -t infiniflow/ragflow:v0.5.0 .
cd ragflow/docker
chmod +x ./entrypoint.sh
docker compose up -d
```
