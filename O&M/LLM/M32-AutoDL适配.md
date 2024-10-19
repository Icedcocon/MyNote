# Yuan2-M32-AutoDL适配

## 一、流程

### 1. 环境配置

#### 1.1 硬件环境

```bash
+--------------------------------------------------AutoDL--------------------------------------------------------+
目录说明:
╔═════════════════╦════════╦════╦═════════════════════════════════════════════════════════════════════════╗
║目录             ║名称    ║速度║说明                                                                     ║
╠═════════════════╬════════╬════╬═════════════════════════════════════════════════════════════════════════╣
║/                ║系 统 盘║一般║实例关机数据不会丢失，可存放代码等。会随保存镜像一起保存。               ║
║/root/autodl-tmp ║数 据 盘║ 快 ║实例关机数据不会丢失，可存放读写IO要求高的数据。但不会随保存镜像一起保存 ║
╚═════════════════╩════════╩════╩═════════════════════════════════════════════════════════════════════════╝
CPU ：15 核心
内存：120 GB
GPU ：NVIDIA A100-SXM4-80GB, 1
存储：
  系 统 盘/               ：6% 1.7G/30G
  数 据 盘/root/autodl-tmp：1% 8.0K/100G
```

#### 1.2 配置加速

`source /etc/network_turbo`

#### 1.3 配置Python环境

- 编译 apex

```bash
git clone https://mirror.ghproxy.com/https://github.com/NVIDIA/apex
cd apex
pip install -v --disable-pip-version-check --no-cache-dir --no-build-isolation --config-settings "--build-option=--cpp_ext" --config-settings "--build-option=--cuda_ext" .
```

- 配置 Yuan2-M32 vLLM 环境

```bash
git clone https://github.com/IEIT-Yuan/Yuan2.0-M32.git
cd Yuan2.0-M32
pip install -r requirements-common.txt
pip install -r requirements-cuda.txt
pip install -r requirements-dev.txt
pip install -r requirements-build.txt
```

- 配置依赖

```bash
apt update
apt-get install -y ccache
CUDA_HOME=/usr/local/cuda MAX_JOBS=64 NVCC_THREADS=8 python setup.py install
cp build/lib.linux-x86_64-cpython-310/vllm/*.so vllm/

##
cp -r vllm vllm.egg-info rocm_patch humaneval /root/miniconda3/lib/python3.10/site-packages/
cp -r vllm vllm.egg-info rocm_patch humaneval /usr/local/lib/python3.10/dist-packages/
```

- 下载模型和代码

```bash
# 模型
git clone https://www.modelscope.cn/IEITYuan/Yuan2-M32-HF-INT4.git
# 代码
git clone https://github.com/IEIT-Yuan/Yuan2.0-M32.git
```

- 执行

```bash
python llm_engine_example.py  --model /root/autodl-tmp/Yuan2-M32-HF-INT4 --tokenizer /root/autodl-tmp/Yuan2-M32-HF-INT4 --enforce-eager  --trust-remote-code --quantization gptq --gpu-memory-utilization 0.8

python llm_engine_example.py  --model /mnt/Yuan2-M32-HF-INT4 --tokenizer /mnt/Yuan2-M32-HF-INT4 --enforce-eager  --trust-remote-code --quantization gptq --gpu-memory-utilization 0.9
```

```bash
docker run --gpus all -itd --network=host  -v /root:/mnt --cap-add=IPC_LOCK --privileged  --name yuan-vllm --ulimit core=0 --ulimit memlock=1 --ulimit stack=68719476736 --shm-size=1000G yuanmodel/vllm-v0.4.0:latest


 #pip config set global.index-url https://pypi.org/simple
 #pip install vllm-flash-attn

 CUDA_HOME=/usr/local/cuda MAX_JOBS=64 NVCC_THREADS=8 python setup.py install
 cp build/lib.linux-x86_64-3.10/vllm/*.so vllm/
```

## 参考资料

- 参考

https://github.com/IEIT-Yuan/Yuan2.0-M32/blob/main/vllm/README_Yuan_vllm.md
