# TensorRT-LLM镜像构建

## 一、TensorRT-LLM仓库脚本自动构建镜像（推荐）

### 1. 使用场景

- 稳定可靠产出最小化镜像，且无需Triton等其他定制服务

- 对于Triton有要求可从以下镜像编译：
  
  - `nvcr.io/nvidia/tritonserver:23.10-trtllm-python-py3`

### 2. 需求

- 有良好的“网络”环境

- 安装docker buildx 插件

### 3. 构建过程

```bash
# 克隆仓库，并递归克隆依赖仓库
git clone https://github.com/NVIDIA/TensorRT-LLM.git -b rel
cd TensorRT-LLM
git submodule update --init --recursive
git lfs install
git lfs pull
# 安装 buildx插件（已安装可以直接执行make）

# 获取最新版本 https://github.com/docker/buildx/releases
wget https://github.com/docker/buildx/releases/download/v0.12.0/buildx-v0.12.0.linux-amd64
mkdir -p $HOME/.docker/cli-plugins
mv buildx-* $HOME/.docker/cli-plugins/docker-buildx
chmod +x ~/.docker/cli-plugins/docker-buildx
docker buildx version 
# github.com/docker/buildx v0.12.0 输出版本信息说明安装成功
make -C docker release_build
```

## 二、从AutoDL镜像构建

### 1.  基本环境

| 组件           | 版本                 |
| ------------ | ------------------ |
| Container OS | Ubuntu 22.04       |
| CUDA         | NVIDIA CUDA 12.2.2 |
| cuDNN        | 8.9.5              |
| TensorRT     | 9.2.0              |
| Python       | 3.10.12            |
| Pytorch      | 2.1.0              |
| TensorRT-LLM | 0.6.1              |

### 2. 构建过程

#### 2.0 说明

本教程参考https://www.codewithgpu.com/i/NVIDIA/TensorRT-LLM/tensorrt_llm

#### 2.1 准备工作

- 观察一下现有TensorRT-LLM容器中的系统配置。

- 通过观察该[文件](https://github.com/NVIDIA/TensorRT-LLM/blob/rel/docker/Dockerfile.multi)

```bash
ARG BASE_IMAGE=nvcr.io/nvidia/pytorch
ARG BASE_TAG=23.10-py3
```

- 可以看出目前基础容器是`nvcr.io/nvidia/pytorch:23.10-py3`

- 再去官网看看这个容器里面的详细信息，官网

- 下面是23.10-py3对应的系统组件版本

| 组件           | 版本                 |
| ------------ | ------------------ |
| Container OS | Ubuntu 22.04       |
| CUDA         | NVIDIA CUDA 12.2.2 |
| cuDNN        | 8.9.5              |
| Python       | 3.10.12            |

- TensorRT在编译的时候会另外安装，根据下面这个[文件](https://github.com/NVIDIA/TensorRT-LLM/blob/rel/docker/common/install_tensorrt.sh)，可以看出TensorRT版本需要的是9.2.0.5

#### 2.2 在autoDL选择合适的显卡和镜像

- miniconda的镜像满足以下要求（内置了cuda11.8和python3.10）
  
  - 需要选择系统为ubuntu 22.04的镜像
  
  - 最好python也是3.10

- 建议到~/autodl-tmp路径下面操作，这个地方不会占用系统空间。

#### 2.3 安装cuda环境

1. 下载cuda 12.2.2

```bash
wget https://developer.download.nvidia.com/compute/cuda/12.2.2/local_installers/cuda_12.2.2_535.104.05_linux.run
```

2. 给予可执行权限

```bash
chmod +x cuda_12.2.2_535.104.05_linux.run
```

3. 正式执行

```bash
./cuda_12.2.2_535.104.05_linux.run
```

- 输入accept，然后回车，按空格勾选或者取消勾选和上下方向键上下移动。

- 只勾选CUDA Toolkit 12.2，其他均取消勾选，然后选中Install即可。

```bash
CUDA Installer                          
│ - [ ] Driver                          │
│      [ ] 535.86.10                    │
│ + [X] CUDA Toolkit 12.2               │
│   [ ] CUDA Demo Suite 12.2            │
│   [ ] CUDA Documentation 12.2         │
│ - [ ] Kernel Objects                  │
│      [ ] nvidia-fs                    │
│   Options                             │
│   Install                             │
```

- 输入Yes确定。
4. 再次确认cuda版本，看输出已经是cuda12.2.140了

```bash
nvcc -V
# nvcc: NVIDIA (R) Cuda compiler driver
# Copyright (c) 2005-2023 NVIDIA Corporation
# Built on Tue_Aug_15_22:02:13_PDT_2023
# Cuda compilation tools, release 12.2, V12.2.140
# Build cuda_12.2.r12.2/compiler.33191640_0
```

5. 删除安装包（可选）

```bash
rm cuda_12.2.2_535.104.05_linux.run
```

6. 删除已存在的cuda11.8（可选）

```bash
rm -rf /usr/local/cuda-11.8
rm -rf /usr/local/cuda-11
```

#### 2.4 安装cudnn

- 去英伟达官网下载cudnn，需要登陆英伟达账号（邮箱/微信登陆，没有就注册一个）。
  
  - 官网链接：https://developer.nvidia.com/cudnn

- 由于系统也内置了cudnn，并且看样子是通过cudnn安装的，所以选择安装包的时候也选择Deb格式,用来覆盖旧版安装会更好。

- 点击Local Installer for Ubuntu22.04 x86_64 (Deb)下载cudnn 8.9.5 for cuda 12.x & ubuntu 22.04 deb格式的cudnn。
1. 安装cudnn

```bash
dpkg -i cudnn-local-repo-ubuntu2204-8.9.5.30_1.0-1_amd64.deb
cd /var/cudnn-local-repo-ubuntu2204-8.9.5.30/
dpkg -i *.deb
# 删除安装包
rm -rf /var/cudnn-local-repo-ubuntu2204-8.9.5.30/
```

2. 验证cudnn版本

```bash
$ldconfig -v | grep cudnn
# libcudnn.so.8 -> libcudnn.so.8.9.5
# libcudnn_cnn_infer.so.8 -> libcudnn_cnn_infer.so.8.9.5
# libcudnn_adv_train.so.8 -> libcudnn_adv_train.so.8.9.5
# libcudnn_ops_train.so.8 -> libcudnn_ops_train.so.8.9.5
# libcudnn_ops_infer.so.8 -> libcudnn_ops_infer.so.8.9.5
# libcudnn_cnn_train.so.8 -> libcudnn_cnn_train.so.8.9.5
# libcudnn_adv_infer.so.8 -> libcudnn_adv_infer.so.8.9.5
```

- 至此AutoDL镜像与`nvcr.io/nvidia/pytorch:23.10-py3`镜像环境基本一致，后续与从PyTorch镜像构建完全一致

### 三、从PyTorch镜像构建

### 1 说明

- 本地从 pytorch 镜像构建时，可通过映射宿主机路径保存下载文件，路径可以自定义。

- 后续为方便说明，采用路径依然与autoDL中镜像一致

- Pytorch镜像为`nvcr.io/nvidia/pytorch:23.10-py3`

### 2. 构建过程

#### 2.1 安装TensorRT

参考该[文档](https://github.com/NVIDIA/TensorRT-LLM/blob/rel/docker/common/install_tensorrt.sh)

1. 设置环境变量

```bash
export TRT_VER="9.2.0.5"
export CUDA_VER="12.2"
export CUDNN_VER="8.9.4.25-1+cuda12.2"
export NCCL_VER="2.18.3-1+cuda12.2"
export CUBLAS_VER="12.2.5.6-1"
export ARCH="x86_64"
export TRT_CUDA_VERSION="12.2"
export OS="linux"

export RELEASE_URL_TRT=https://developer.nvidia.com/downloads/compute/machine-learning/tensorrt/9.2.0/tensorrt-${TRT_VER}.${OS}.${ARCH}-gnu.cuda-${TRT_CUDA_VERSION}.tar.gz;
```

2. 下载TensorRT并且解压TensorRT

```bash
wget ${RELEASE_URL_TRT} -O /tmp/TensorRT.tar
tar -xf /tmp/TensorRT.tar -C /usr/local/
# 移动解压后的文件到/usr/local/tensorrt/目录
# 和官方容器保持一致，然后删除tensorrt的压缩包
mv /usr/local/TensorRT-${TRT_VER} /usr/local/tensorrt
rm -rf /tmp/TensorRT.tar
# 配置ldconfig,然后lib可以被系统找到
echo "/usr/local/tensorrt/lib" > /etc/ld.so.conf.d/tensorrt.conf
```

3. 确定tensorrt版本是9.1.0

```bash
ldconfig -v | grep nvinfer
# libnvinfer_vc_plugin.so.9 -> libnvinfer_vc_plugin.so.9.2.0
# libnvinfer_dispatch.so.9 -> libnvinfer_dispatch.so.9.2.0
# libnvinfer.so.9 -> libnvinfer.so.9.2.0
# libnvinfer_plugin.so.9 -> libnvinfer_plugin.so.9.2.0
# libnvinfer_lean.so.9 -> libnvinfer_lean.so.9.2.0
```

4. 设置环境

```bash
echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/tensorrt/lib:/usr/local/cuda/lib64/" >> /etc/profile

echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/tensorrt/lib:/usr/local/cuda/lib64/" >> ~/.bashrc

source /etc/profile
source ~/.bashrc
```

5. 测试lib库能否找到

```bash
echo ${LD_LIBRARY_PATH}
# 输出结果：
# /usr/local/tensorrt/lib:/usr/local/cuda/lib64/
```

#### 2.2 安装并测试mpi4py

1. 安装

```bash
conda install mpi4py openmpi
```

2. 测试

```bash
$python3
Python 3.10.8 (main, Nov 24 2022, 14:13:03) [GCC 11.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from mpi4py import MPI
>>> MPI.COMM_WORLD.Get_rank()
>>> 0
>>> MPI.COMM_WORLD.Get_size()
>>> 1
```

#### 2.3 编译TensorRT-LLM

- AutoDl镜像中建议还是在/root/autodl-tmp目录编译
1. 下载TensorRT-LLM源码，目前rel为最新稳定分支

```bash
cd /root/autodl-tmp
git clone https://github.com/NVIDIA/TensorRT-LLM.git -b rel
# 或通过代理
# git clone https://ghproxy.net/https://github.com/NVIDIA/TensorRT-LLM.git -b  rel
```

2. 安装依赖

```bash
# 进入编译目录路径
cd /root/autodl-tmp/TensorRT-LLM/docker/common
# 安装基础依赖
apt update
sudo apt-get install -y --no-install-recommends ccache wget gdb git-lfs libffi-dev libopenmpi-dev
# 安装tensorrt-python，选择和python3.10有关的whl文件。
cd /usr/local/tensorrt/python/
pip install tensorrt-9.2.0.post12.dev5-cp310-none-linux_x86_64.whl
pip install tensorrt_dispatch-9.2.0.post12.dev5-cp310-none-linux_x86_64.whl
pip install tensorrt_lean-9.2.0.post12.dev5-cp310-none-linux_x86_64.whl
# 测试python tensorrt版本，输出9.2.0.post12.dev5则表示正常
python3 -c "import tensorrt as trt; print(trt.__version__)"
# 安装polygraphy
cd /root/autodl-tmp/TensorRT-LLM/docker/common/
chmod +x install_polygraphy.sh
./install_polygraphy.sh
```

3. 一键编译whl文件
- 编译过程中发现/tmp目录大量占用空间，而AutoDL附赠的30G系统空间不太够用，所以需要指定一个大点的路径来充当tmp路径。
- 设置数据盘为tmp路径，这个有免费50G空间

```bash
cd /root/autodl-tmp/TensorRT-LLM
export TMPDIR=/root/autodl-tmp
# 拉取第三方子项目代码
git submodule update --init --recursive
# 修改一下.git/config，加上代理源，否则可能会卡住。
# 手动拉取lfs大文件
git lfs install && git lfs pull
# 一键编译，大概需要1个小时左右
export BUILD_WHEEL_ARGS="--clean --trt_root /usr/local/tensorrt"
python3 scripts/build_wheel.py ${BUILD_WHEEL_ARGS}
```

4. 安装whl文件

```bash
cd /root/autodl-tmp/TensorRT-LLM/build
pip install tensorrt_llm-0.6.1-py3-none-any.whl
安装后清理一下cache。
rm ~/.cache/ -rf
```

5. 测试安装后tensorrt-llm版本

```bash
pip list | grep tensorrt-llm
# 输出
# tensorrt-llm             0.6.1
```

6. 测试tensorrt-llm

```bash
python3 -c "import tensorrt_llm; print(tensorrt_llm.__path__)"
```

7. 环境验证代码
- 将刚刚下载的仓库再下载一份到/root路径，防止后续有发生更新，导致你编译的和它不一样而报错
- 此时可以不用管第三方仓库和lfs大文件了，因为这个只有编译的时候采用

```bash
cd /root
git clone https://ghproxy.net/https://github.com/NVIDIA/TensorRT-LLM.git -b rel
# 测试tensorrt-llm中的attention
# 观察tensort-llm可否正常使用（这个操作可能需要显卡）
cd /root/TensorRT-LLM/tests/attention
pip install parameterized
python3 test_bert_attention.py
# 返回下面这个说明成功了，大概需要5-10分钟才能测试完成，请耐心等待。
# Ran 49 tests in 255.221s
# OK
```

## 四、 从TritonServer镜像构建

### 1 说明

- 本段构建过程可能存在遗漏，请根据二、三章内容进行检查

### 2 engine构建

1. 拉取官方镜像和仓库

```bash
docker pull nvcr.io/nvidia/tritonserver:23.10-trtllm-python-py3

git clone https://github.com/triton-inference-server/tensorrtllm_backend.git -b release/0.5.0
cd tensorrtllm_backend
git submodule update --init --recursive
git lfs install
git lfs pull
git clone https://ghproxy.net/https://github.com/NVIDIA/TensorRT-LLM.git -b rel
```

2. 运行容器

```bash
docker run -d \    
    --name triton2 \
    --net host \
    --shm-size=2g \
    --ulimit memlock=-1 \
    --ulimit stack=67108864 \
    --gpus all \
    -v ${PWD}/tensorrtllm_backend:/tensorrtllm_backend \
    -v ${PWD}/TensorRT-LLM/qwen:/root/TensorRT-LLM \
    nvcr.io/nvidia/tritonserver:23.10-trtllm-python-py3 sleep 864000
```

3. 进入容器，安装git-lfs

```bash
apt update
apt install git-lfs cmake
```

4. 安装依赖

```text
pip install -e /root/TensorRT-LLM
pip install -e /tensorrtllm_backend
```

5. 编译 TensorRT-LLM
- 其实Triton里面已经内置了TensorRT-LLM，所以建议在Triton容器里面进行编译，防止环境不一致问题。

- 因为这个镜像中**只有运行需要的lib**，模型还是需要自行编译的

- 参考第三章 2.3 节
6. 复制lib库过去，否则无法运行

```bash
mkdir /usr/local/lib/python3.10/dist-packages/tensorrt_llm/libs/
cp /opt/tritonserver/backends/tensorrtllm/* /usr/local/lib/python3.10/dist-packages/tensorrt_llm/libs/
```

7. 编译engine

```bash
cd /root/TensorRT-LLM/examples/chatglm
python3 build.py --model_name=chatglm2_6b 
                 --model_dir=/root/autodl-tmp/chatglm2-6b 
                 --output_dir=trtModel 
                 --use_weight_only 
                 --weight_only_precision=int8 
                 --tp_size=2 --world_size=2
```

8. 运行engine测试

```bash
mpirun --allow-run-as-root -n 2 python run.py 
       --engine_dir=/root/autodl-tmp/chatglm2-6b-trtModel 
       --model_name=chatglm2_6b 
       --tokenizer_dir=/root/autodl-tmp/chatglm2-6b  
       --input_text="Hello tell me about Iphone"
```

- 此时镜像准备完成，可将容器commit为镜像

### 3. 启动服务

1. 复制Engine文件

```bash
cd /root/autodl-tmp/chatglm2-6b-trtModel
mkdir /tensorrtllm_backend/triton_model_repo/tensorrt_llm/1/
cp -r ./* /tensorrtllm_backend/triton_model_repo/tensorrt_llm/1/
```

2. 复制tokenzer文件

```bash
cd /root/autodl-tmp
cp -r chatglm2-6b /tensorrtllm_backend/triton_model_repo/tensorrt_llm/
```

3. 启动服务

```bash
cd /tensorrtllm_backend
python3 scripts/launch_triton_server.py --world_size=2 
    --model_repo=/tensorrtllm_backend/triton_model_repo
```

4. http请求

```bash
# 发送post请求
curl -X POST localhost:8000/v2/models/ensemble/generate \
-d '{"text_input": "<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n<|im_start|>user\n你好，请问你叫什么？<|im_end|>\n<|im_start|>assistant\n", "max_tokens": 50, "bad_words": "", "stop_words": "", "end_id": [151643], "pad_id": [151643]}'
# 返回结果
#   {
#       "model_name": "ensemble",
#       "model_version": "1",
#       "sequence_end": false,
#       "sequence_id": 0,
#       "sequence_start": false,
#       "text_output": "<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n<|im_start|>user\n你好，请问你叫什么？<|im_end|>\n<|im_start|>assistant\n你好，我是通义千问，由阿里云开发的AI助手。<|im_end|>\n\n"
#   }
```

5. 关闭服务

```bash
pgrep tritonserver | xargs kill -9
```

## 参考资料

https://zhuanlan.zhihu.com/p/668548188

https://www.http5.cn/index.php/archives/55/

https://huggingface.co/THUDM/chatglm2-6b

[GitHub - triton-inference-server/tensorrtllm_backend: The Triton TensorRT-LLM Backend](https://github.com/triton-inference-server/tensorrtllm_backend)

https://ai.oldpan.me/t/topic/260

https://zhuanlan.zhihu.com/p/663338695

https://github.com/Tlntin/Qwen-7B-Chat-TensorRT-LLM

https://zhuanlan.zhihu.com/p/664545577https://zhuanlan.zhihu.com/p/668548188

https://www.http5.cn/index.php/archives/55/

https://huggingface.co/THUDM/chatglm2-6b

[GitHub - triton-inference-server/tensorrtllm_backend: The Triton TensorRT-LLM Backend](https://github.com/triton-inference-server/tensorrtllm_backend)

https://ai.oldpan.me/t/topic/260

https://zhuanlan.zhihu.com/p/663338695

https://github.com/Tlntin/Qwen-7B-Chat-TensorRT-LLM

https://zhuanlan.zhihu.com/p/664545577

https://zhuanlan.zhihu.com/p/663378231

https://www.yuque.com/tlntin/lg8kzc/gl5g1t9o11lna7u6

Triton

https://zhuanlan.zhihu.com/p/660990715

分布式推理

[大模型推理——分布式技术相关 - AI大模型 - 老潘的AI社区](https://ai.oldpan.me/t/topic/172)

https://www.zhihu.com/question/63219175/answer/206697974

[大模型推理——FasterTransformer + TRITON - AI大模型 - 老潘的AI社区](https://ai.oldpan.me/t/topic/177)

[TensorRT-9.0和TensorRT-LLM快要出来啦 - 部署不内卷 - 老潘的AI社区](https://ai.oldpan.me/t/topic/199)

https://www.bilibili.com/video/BV1h44y1c72B/?spm_id_from=333.788&vd_source=eec038509607175d58cdfe2e824e8ba2

[大大大大大模型部署方案抛砖引玉 - AI大模型 - 老潘的AI社区](https://ai.oldpan.me/t/topic/118)

https://juejin.cn/post/7219245946739179578

https://zhuanlan.zhihu.com/p/626008090

分布式推理-大模型推理框架-综述

https://zhuanlan.zhihu.com/p/665089816

镜像编译

https://zhuanlan.zhihu.com/p/663915644

Pytorch教程

[9.1 使用ONNX进行部署并推理 — 深入浅出PyTorch](https://datawhalechina.github.io/thorough-pytorch/%E7%AC%AC%E4%B9%9D%E7%AB%A0/9.1%20%E4%BD%BF%E7%94%A8ONNX%E8%BF%9B%E8%A1%8C%E9%83%A8%E7%BD%B2%E5%B9%B6%E6%8E%A8%E7%90%86.html)

深度学理论基础

[Attention 注意力机制 | 鲁老师](https://lulaoshi.info/deep-learning/attention/attention.html#attention%E6%9C%BA%E5%88%B6)

编译器、模型优化及AI相关博客

http://giantpandacv.com/project/%E9%83%A8%E7%BD%B2%E4%BC%98%E5%8C%96/

vLLM

[使用Docker、vllm和Gradio部署开源LLM，以Qwen-7B-Chat为例 | LittleFish’Blog](https://www.xiaoiluo.com/article/vllm-docker-server)

ONNX

https://zhuanlan.zhihu.com/p/453084182

https://zhuanlan.zhihu.com/p/641975976https://zhuanlan.zhihu.com/p/668548188

[Triton23.10部署TensorRT-LLM,实现http查询 - 技术视野](https://www.http5.cn/index.php/archives/55/)

[THUDM/chatglm2-6b · Hugging Face](https://huggingface.co/THUDM/chatglm2-6b)

[GitHub - triton-inference-server/tensorrtllm_backend: The Triton TensorRT-LLM Backend](https://github.com/triton-inference-server/tensorrtllm_backend)

https://ai.oldpan.me/t/topic/260

https://zhuanlan.zhihu.com/p/663338695

https://github.com/Tlntin/Qwen-7B-Chat-TensorRT-LLM

https://zhuanlan.zhihu.com/p/664545577

Triton

https://zhuanlan.zhihu.com/p/660990715

分布式推理

[大模型推理——分布式技术相关 - AI大模型 - 老潘的AI社区](https://ai.oldpan.me/t/topic/172)

https://www.zhihu.com/question/63219175/answer/206697974

[大模型推理——FasterTransformer + TRITON - AI大模型 - 老潘的AI社区](https://ai.oldpan.me/t/topic/177)

[TensorRT-9.0和TensorRT-LLM快要出来啦 - 部署不内卷 - 老潘的AI社区](https://ai.oldpan.me/t/topic/199)

https://www.bilibili.com/video/BV1h44y1c72B/?spm_id_from=333.788&vd_source=eec038509607175d58cdfe2e824e8ba2

[大大大大大模型部署方案抛砖引玉 - AI大模型 - 老潘的AI社区](https://ai.oldpan.me/t/topic/118)

https://juejin.cn/post/7219245946739179578

https://zhuanlan.zhihu.com/p/626008090

分布式推理-大模型推理框架-综述

https://zhuanlan.zhihu.com/p/665089816

镜像编译

https://zhuanlan.zhihu.com/p/663915644

Pytorch教程

[9.1 使用ONNX进行部署并推理 — 深入浅出PyTorch](https://datawhalechina.github.io/thorough-pytorch/%E7%AC%AC%E4%B9%9D%E7%AB%A0/9.1%20%E4%BD%BF%E7%94%A8ONNX%E8%BF%9B%E8%A1%8C%E9%83%A8%E7%BD%B2%E5%B9%B6%E6%8E%A8%E7%90%86.html)

深度学理论基础

[Attention 注意力机制 | 鲁老师](https://lulaoshi.info/deep-learning/attention/attention.html#attention%E6%9C%BA%E5%88%B6)

编译器、模型优化及AI相关博客

[专栏介绍 - GiantPandaCV](http://giantpandacv.com/project/%E9%83%A8%E7%BD%B2%E4%BC%98%E5%8C%96/)

vLLM

[使用Docker、vllm和Gradio部署开源LLM，以Qwen-7B-Chat为例 | LittleFish’Blog](https://www.xiaoiluo.com/article/vllm-docker-server)

ONNX

https://zhuanlan.zhihu.com/p/453084182

https://zhuanlan.zhihu.com/p/641975976

Triton

https://zhuanlan.zhihu.com/p/660990715

分布式推理

https://ai.oldpan.me/t/topic/172

https://www.zhihu.com/question/63219175/answer/206697974

https://ai.oldpan.me/t/topic/177

https://ai.oldpan.me/t/topic/199

https://www.bilibili.com/video/BV1h44y1c72B/?spm_id_from=333.788&vd_source=eec038509607175d58cdfe2e824e8ba2

[大大大大大模型部署方案抛砖引玉 - AI大模型 - 老潘的AI社区](https://ai.oldpan.me/t/topic/118)

https://juejin.cn/post/7219245946739179578

https://zhuanlan.zhihu.com/p/626008090

分布式推理-大模型推理框架-综述

https://zhuanlan.zhihu.com/p/665089816

镜像编译

https://zhuanlan.zhihu.com/p/663915644

Pytorch教程

[9.1 使用ONNX进行部署并推理 &#8212; 深入浅出PyTorch](https://datawhalechina.github.io/thorough-pytorch/%E7%AC%AC%E4%B9%9D%E7%AB%A0/9.1%20%E4%BD%BF%E7%94%A8ONNX%E8%BF%9B%E8%A1%8C%E9%83%A8%E7%BD%B2%E5%B9%B6%E6%8E%A8%E7%90%86.html)

深度学理论基础

[Attention 注意力机制 | 鲁老师](https://lulaoshi.info/deep-learning/attention/attention.html#attention%E6%9C%BA%E5%88%B6)

编译器、模型优化及AI相关博客

http://giantpandacv.com/project/%E9%83%A8%E7%BD%B2%E4%BC%98%E5%8C%96/

vLLM

[使用Docker、vllm和Gradio部署开源LLM，以Qwen-7B-Chat为例 | LittleFish’Blog](https://www.xiaoiluo.com/article/vllm-docker-server)

ONNX

https://zhuanlan.zhihu.com/p/453084182

https://zhuanlan.zhihu.com/p/641975976

GPU 架构对算力影响

https://zhuanlan.zhihu.com/p/258196004

TensorRT Python API

[ICudaEngine &mdash; NVIDIA TensorRT Standard Python API Documentation 8.6.1 documentation](https://docs.nvidia.com/deeplearning/tensorrt/api/python_api/infer/Core/Engine.html)
