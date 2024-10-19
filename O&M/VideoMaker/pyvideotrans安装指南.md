# pyvideotrans 安装指南

## Dockerfile

```bash
# 使用Python 3.10作为基础镜像
FROM python:3.10

# 避免交互式提示
ENV DEBIAN_FRONTEND=noninteractive

# 安装必要的系统包
RUN sed -ri  's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
&& apt-get update && apt-get upgrade -y \
&& apt-get install -y ffmpeg libxcb-cursor0 git

# 设置工作目录
WORKDIR /app

# 设置pip镜像
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
&& pip config set install.trusted-host mirrors.aliyun.com

# 克隆项目并安装依赖
RUN git clone https://mirror.ghproxy.com/https://github.com/jianchang512/pyvideotrans . \
; pip install -r /app/pyvideotrans/requirements.txt --no-deps

# 如果需要CUDA支持，取消注释以下行（注意：这需要NVIDIA Container Toolkit支持）
RUN pip uninstall -y torch torchaudio \
&& pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu122 \
&& pip install nvidia-cublas-cu12 nvidia-cudnn-cu12

# 设置启动命令
CMD ["python", "/app/pyvideotrans/sp.py"]
```

## ChatTTS-UI

```bash
git clone https://github.com/jianchang512/ChatTTS-ui.git
cd ChatTTS-ui
docker-compose -f docker-compose.gpu.yaml up -d 
```

## 参考资料
