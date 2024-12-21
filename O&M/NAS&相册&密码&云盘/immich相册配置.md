# immich相册配置

> 建议使用非 root 账号操作

## 快速开始

### 1. 下载配置文件

```bash
mkdir ./immich-app
cd ./immich-app
curl -fsSL https://github.com/immich-app/immich/releases/latest/download/docker-compose.yml -o ./docker-compose.yml
curl -fsSL https://github.com/immich-app/immich/releases/latest/download/example.env -o ./.env
# 下载 docker-compose-v2
curl -L "https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

### 2. 修改配置文件

- `.env` 文件

```yaml
# You can find documentation for all the supported env variables at https://immich.app/docs/install/environment-variables

# The location where your uploaded files are stored
UPLOAD_LOCATION=./library
# The location where your database files are stored
DB_DATA_LOCATION=./postgres

# To set a timezone, uncomment the next line and change Etc/UTC to a TZ identifier from this list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List
TZ=Asia/Shanghai

# The Immich version to use. You can pin this to a specific version like "v1.71.0"
IMMICH_VERSION=release

# Connection secret for postgres. You should change it to a random password
# Please use only the characters `A-Za-z0-9`, without special characters or spaces
DB_PASSWORD=postgres

# The values below this line do not need to be changed
###################################################################################
DB_USERNAME=postgres
DB_DATABASE_NAME=immich
```

### 3. 开启cuda加速

- 下载文件

```bash
wget https://github.com/immich-app/immich/releases/latest/download/hwaccel.ml.yml
```

- 修改 `docker-compose.yaml` 配置

> 1. 取消 extends注释； 2. 在image 的 tag 后添加 `-cuda`

```yaml
  immich-machine-learning:
    container_name: immich_machine_learning
    # For hardware acceleration, add one of -[armnn, cuda, openvino] to the image tag.
    # Example tag: ${IMMICH_VERSION:-release}-cuda
    image: ghcr.io/immich-app/immich-machine-learning:${IMMICH_VERSION:-release}
    extends: # uncomment this section for hardware acceleration - see https://immich.app/docs/features/ml-hardware-acceleration
      file: hwaccel.ml.yml
      service: cuda # set to one of [armnn, cuda, openvino, openvino-wsl] for accelerated inference - use the `-wsl` version for WSL2 where applicable
```

- 多 GPU 处理

使用多张 GPU

```bash
MACHINE_LEARNING_DEVICE_IDS=0,1
MACHINE_LEARNING_WORKERS=2
```

仅使用 id 为 1 的GPU

```bash
MACHINE_LEARNING_DEVICE_IDS=1
```

- 添加 NVIDIA 仓库

```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# 安装 toolkit
apt update
apt install nvidia-container-toolkit
```

- 可选的 安装 cuda

```bash
apt install nvidia-cuda-toolkit
```

## 参考资料
