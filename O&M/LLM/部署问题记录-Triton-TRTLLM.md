# HF模型编译为TensorRT模型说明

## 1. HF模型转为PyTorch模型

Huggingface的模型无法直接转为onnx（仅有部分支持），如果是huggingface的模型，需要先转成PyTorch

Huggingface本身的模型其实就是基于PyTorch的，但是格式不算通用。

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import AutoModel
import torch

# convert huggingface model to pytorch model

model = AutoModelForSeq2SeqLM.from_pretrained("../../opus-mt-zh-en")
print("model from huggingface loaded, now eval")
model.eval()
print("eval finished,now convert")
torch.save(model, 'opus-mt-zh-en.pt')
print("convert finished")
```

## 2. PyTorch模型转为ONNX模型

### 2.1 使用torch.onnx.export函数（失败）

这里面有几点需要注意：

1. 转换前需要调用eval函数
2. 如果模型很大，那么转换出来的文件会很多，因为存储onnx的文件大小不允许超过2G，这是正常的
3. export函数中，`input_names=["input"], output_names=["output"]`是自己定义的。`dynamic_axes={'input': {1:'tokenlength'},'output' : [0,1]}`是用来定义输入输出的可变长度的。比如，对于文本问答模型，每次输入的长度都不统一，如果按照这次转换的推理，那么input的维度就固定了，这样当再次加载模型推理的时候，就会报长度不一致的错误，所以这里要设置为可变长度。其中，1表示三维张量的第二维是可变的。`'output' : [0,1]`表示output张量（列表）的第一维和第二维，都是可变的。

```python
from transformers import AutoTokenizer
from transformers import AutoModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

src_text = "从时间上看，中国空间站的建造比国际空间站晚20多年。"
tokenizer = AutoTokenizer.from_pretrained("../../opus-mt-zh-en")
encoder_input_ids = tokenizer.encode(src_text, return_tensors="pt", 
                                     padding=True)
print(f"输入维度: {encoder_input_ids.shape}")
# decoder_input_ids = torch.randint_like(encoder_input_ids, 0, 
#                                        20000, dtype=torch.long)
# decoder_input_ids =  ['In terms of time, the Chinese space 
#                        station was built#  more than 20 years 
#                        later than the International Space Station.']
decoder_input_ids = tokenizer.encode('In terms of time, the aaaaaaaaab', 
                                     return_tensors="pt", padding=True) 
# decoder_input_ids = torch.randint_like(encoder_input_ids, 0, 20000, 
#                                        dtype=torch.long)
# decoder_input_ids = torch.ones( 1,  19)
print(f"输出类型: {decoder_input_ids.type}")
print(f"输出维度: {decoder_input_ids.shape}")
# # 构造encoder端和decoder端的attention mask
# encoder_attn_mask = torch.ones(1, encoder_input_ids.shape[1], 
#                                dtype=torch.long)  
# decoder_attn_mask = torch.ones(1, decoder_input_ids.shape[1], 
#                                dtype=torch.long)

pt_model = torch.load('opus-mt-zh-en.pt')
# print(f"输入层: {pt_model.model.shared}")
# print(f"输出层: {pt_model.lm_head}")
pt_model.eval()
# output = pt_model(input_ids=input_ids, 
#                   decoder_input_ids=decoder_input_ids)
# print(output)

torch.onnx.export(
    pt_model, 
    (encoder_input_ids,decoder_input_ids), 
    "opus-mt-zh-en.onnx",
    input_names=['encoder_input', 'decoder_input'], 
    output_names=["output"],
    opset_version=11,
    dynamic_axes={'input': {0:'tokenlength'},
                  'output' : {0:'outputlength'}}
    ) # 输入的第1为可变



import torch.onnx 
# 转换的onnx格式的名称，文件后缀需为.onnx
onnx_file_name = "xxxxxx.onnx"
# 我们需要转换的模型，将torch_model设置为自己的模型
model = torch_model
# 加载权重，将model.pth转换为自己的模型权重
# 如果模型的权重是使用多卡训练出来，我们需要去除权重中多的module. 具体操作可以见5.4节
model = model.load_state_dict(torch.load("model.pth"))
# 导出模型前，必须调用model.eval()或者model.train(False)
model.eval()
# dummy_input就是一个输入的实例，仅提供输入shape、type等信息 
batch_size = 1 # 随机的取值，当设置dynamic_axes后影响不大
dummy_input = torch.randn(batch_size, 1, 224, 224, requires_grad=True) 
# 这组输入对应的模型输出
output = model(dummy_input)
# 导出模型
torch.onnx.export(model,        # 模型的名称
                  dummy_input,   # 一组实例化输入
                  onnx_file_name,   # 文件保存路径/名称
                  export_params=True,        #  如果指定为True或默认, 参数也
                                             #  会被导出. 如果你要导出一个没训
                                             #  练过的就设为 False.

                  opset_version=10,          # ONNX 算子集的版本，当前已更新
                                             #  到15
                  do_constant_folding=True,  # 是否执行常量折叠优化
                  input_names = ['input'],   # 输入模型的张量的名称
                  output_names = ['output'], # 输出模型的张量的名称
                  # dynamic_axes将batch_size的维度指定为动态，
                  # 后续进行推理的数据可以与导出的dummy_input的batch_size不同
                  dynamic_axes={'input' : {0 : 'batch_size'},    
                                'output' : {0 : 'batch_size'}})
```

**失败原因：** 对于**Seq2Seq**任务的**Encoder-Decoder**架构模型，需要用pytorch将模型拆分为Encoder和Decoder两个部分，然后进行导出，操作难度较大，可以参考以下T5导出代码

`https://github.com/Ki6an/fastT5/blob/8dda859086af631a10ad210a5f1afdec64d49616/fastT5/onnx_exporter.py#L45`

### 2.2 使用optimum-cli导出

```bash
#! /bin/bash
pip install optimum[exporters]
# pip install --upgrade diffusers
# optimum-cli export onnx --model opus-mt-zh-en onnx/   # 从 🤗 Hub 导出检查点的过程。
optimum-cli export onnx --model ../../opus-mt-zh-en --task text2text-generation onnx/
```

### 2.3 验证

模型校验

```python
import onnx
# 我们可以使用异常处理的方法进行检验
try:
    # 当我们的模型不可用时，将会报出异常
    onnx.checker.check_model(self.onnx_model)
except onnx.checker.ValidationError as e:
    print("The model is invalid: %s"%e)
else:
    # 模型可用时，将不会报出异常，并会输出“The model is valid!”
    print("The model is valid!")
```

# Triton使用指南

## Part1 如何部署模型推理服务？

### 0. 综述/背景

**(1) 任何深度学习推理服务解决方案都需要应对两个基本挑战：**

1. **管理多个模型。**

2. **版本控制、加载和卸载模型。**

(2) 部署一个**高性能的 (Performant)** 和**可扩展的 (Scalable)** 流水线 (Pipeline)包括如下 5 步：

1. 预处理 (Pre-process) 原始图像 (Raw image)

2. 检测 (Detect) 图像中包含文字的部分 (Text Detection Model)

3. 裁剪 (Crop) 包含文字的图像区域

4. 查找文本概率 (Text Recognition Model)

5. 转换概率值到实际文本

(3) **部署多个模型**

- 管理多个模型的关键挑战是，如何构建一个能够满足 (Cater to) 不同模型的不同需求的基础设施。
  
  - 例如，**用户可能需要在同一台服务器上同时部署一个 PyTorch Model 和一个 TensorFlow Model**，**而且模型的负载 (Have different loads) 也不同**，**需要在不同的硬件设备 (different devices) 上运行**，并且需要**独立管理服务配置（different serving configurations，模型队列 Model queues、版本 Versions、缓存 Caching、加速 Acceleration等）**。

- Triton Inference Server 能够满足 (Cater to) 上述所有需求、甚至更多。

### 1. 建仓、撸配置

0. 使用 Triton Inference Server 部署模型的第一步，是建立**一个存储这些模型 (Houes the models) 的模型仓库 (Model repository)**，以及**一堆配置 (Configuration schema)**。
   
   - 为了演示，**我们将利用一个文本检测模型** EAST **和一个文本识别模型**。这个工作流程在很大程度上是对OpenCV's Text Detection例子的改编。

1. 首先，让我们克隆指南仓库 (https://github.com/triton-inference-server/tutorials) 并导航到该文件夹。

```text
git clone https://github.com/triton-inference-server/tutorials.git
cd Conceptual_Guide/Part_1-model_deployment
```

2. 接下来，我们将下载必要的模型，并确保他们是 Triton 兼容的格式 (Model format)。

#### 1.1. 下载 Model 1: Text Detection

1. 下载和解压 OpenCV 的 EAST Model 。

```text
wget https://www.dropbox.com/s/r2ingd0l3zt8hxs/frozen_east_text_detection.tar.gz
tar -xvf frozen_east_text_detection.tar.gz
```

#### 1.2. 导出到 ONNX 格式。

> Note: 下一步需要您安装好 TensorFlow 库。我们建议您在 **NGC TensorFlow 容器环境**中执行下一步，您可以使用以下命令启动该环境：*docker run -it --gpus all -v ${PWD}:/workspace http://nvcr.io/nvidia/tensorflow:-tf2-py3*

```text
pip install -U tf2onnx
python -m tf2onnx.convert --input frozen_east_text_detection.pb --inputs "input_images:0" --outputs "feature_fusion/Conv_7/Sigmoid:0","feature_fusion/concat_3:0" --output detection.onnx
```

### 2. 下载Model 2: Text Recognition

- 下载文本识别模型权重 (Text Recognition Model Weights)。

```text
wget https://www.dropbox.com/sh/j3xmli4di1zuv3s/AABzCC1KGbIRe2wRwa3diWKwa/None-ResNet-None-CTC.pth
```

- 将模型导出为 .onnx 文件，使用文件夹 utils/ 下模型定义文件 (Model definition file) 中的 model.py 文件。

> Note: 以下的 Python 脚本需要您已经安装 PyTorch 库。我们建议您在 NGC PyTorch 容器环境中执行以下步骤，您可以使用以下命令启动该环境：*docker run -it --gpus all -v ${PWD}:/workspace http://nvcr.io/nvidia/pytorch:-py3*

```text
import torch
from utils.model import STRModel


# Create PyTorch Model Object
model = STRModel(input_channels=1, output_channels=512, num_classes=37)

# Load model weights from external file
state = torch.load("None-ResNet-None-CTC.pth")
state = {key.replace("module.", ""): value for key, value in state.items()}
model.load_state_dict(state)

# Create ONNX file by tracing model
trace_input = torch.randn(1, 1, 32, 100)
torch.onnx.export(model, trace_input, "str.onnx", verbose=True)
```

### 3. 设置模型仓库 (Model repository)

- 模型仓库 (Model repository) 是 Triton 读取模型及其相关元数据（Metadata，如配置、版本文件等）的方式。

- **模型仓库可以存在于**
  
  - **本地 (Local)**
  - **网络连接的文件系统 (Network attached filesystem)**
  - **云对象存储 (Cloud object store)**
    - 像 AWS S3、Azure Blob Storage 或 Google Cloud Storage

- 有关模型仓库位置的详细信息，请参阅[文档](https://link.zhihu.com/?target=https%3A//docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html%23model-repository-locations)。

- **服务器 (Servers) 还可以使用多个不同的模型仓库**。

- 为了简单起见，本说明仅使用存储在本地文件系统 (Local filesystem) 中的单个仓库，结构如下：

```text
# Example repository structure
<model-repository>/
  <model-name>/
    [config.pbtxt]
    [<output-labels-file> ...]
    <version>/
      <model-definition-file>
    <version>/
      <model-definition-file>
    ...
  <model-name>/
    [config.pbtxt]
    [<output-labels-file> ...]
    <version>/
      <model-definition-file>
    <version>/
      <model-definition-file>
    ...
  ...
```

上面的模型仓库 (Model repository) 结构中，有三个重要组成部分：

1. **model-name: 模型的标识。**

2. **config.pbtxt**: 对于每个模型，用户可以定义一个模型配置 (Model configuration)。这个配置至少需要定义：后端，名称，形状，以及模型输入输出的数据类型 (the backend, name, shape, and datatype of model inputs and outputs)。对于大多数流行的后端 (backend)，这个配置文件会默认自动生成。配置文件的完整规范可以在这里找到 [model_config_protobuf_definition](https://link.zhihu.com/?target=https%3A//github.com/triton-inference-server/common/blob/main/protobuf/model_config.proto)。

3. version: 版本控制策略，能让同一个模型的多个版本可供使用，取决于你使用什么策略。[有关版本控制的更多信息](https://link.zhihu.com/?target=https%3A//docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/model_repository.html%23model-versions)。  

在这个例子中，您可以这样设置模型仓库 (Model repository) 的结构：

```text
mkdir -p model_repository/text_detection/1
mv detection.onnx model_repository/text_detection/1/model.onnx

mkdir -p model_repository/text_recognition/1
mv str.onnx model_repository/text_recognition/1/model.onnx
```

这些命令将给您一个看起来如下的存储库：

```text
# Expected folder layout
model_repository/
├── text_detection
│   ├── 1
│   │   └── model.onnx
│   └── config.pbtxt
└── text_recognition
    ├── 1
    │   └── model.onnx
    └── config.pbtxt
```

请注意，对于这个示例，我们已经创建了 config.pbtxt 文件，并将它们放在了必要的位置。在下一节中，我们将讨论这些文件的内容。

### 4. 模型配置 (Model configuration)

准备好了模型和文件结构之后，我们接下来需要查看的是 config.pbtxt 模型配置文件。首先，我们看下 EAST text detection 模型的模型配置，位于 /model_repository/text_detection/config.pbtxt 。这显示了 text_detection 是一个 ONNX 模型，有 1 个 Input 和 2 个 Output tensors。

```text
name: "text_detection"
backend: "onnxruntime"
max_batch_size : 256
input [
  {
    name: "input_images:0"
    data_type: TYPE_FP32
    dims: [ -1, -1, -1, 3 ]
  }
]
output [
  {
    name: "feature_fusion/Conv_7/Sigmoid:0"
    data_type: TYPE_FP32
    dims: [ -1, -1, -1, 1 ]
  }
]
output [
  {
    name: "feature_fusion/concat_3:0"
    data_type: TYPE_FP32
    dims: [ -1, -1, -1, 5 ]
  }
]
```

1. name: “name”是一个可选字段，其值应与模型目录的名称相匹配。

2. backend: 此字段表示使用哪个后端来运行模型。Triton 支持各种后端，例如 TensorFlow、PyTorch、Python、ONNX 等等。有关字段选择的完整列表，请参考这些[注释](https://link.zhihu.com/?target=https%3A//github.com/triton-inference-server/backend%23backends)。

3. max_batch_size: 如其名，该字段用于定义模型最多能支持的批处理大小。

4. input and output: 输入和输出部分指定了名称、形状、数据类型等信息，同时提供了 [reshaping](https://link.zhihu.com/?target=https%3A//github.com/triton-inference-server/server/blob/main/docs/user_guide/model_configuration.md%23reshape) 和 [ragged batches](https://link.zhihu.com/?target=https%3A//github.com/triton-inference-server/server/blob/main/docs/user_guide/ragged_batching.md%23ragged-batching)（动态 Batch） 等操作的支持。  

大多数情况下，可以省略输入和输出部分，让 Triton 直接从模型文件中提取这些信息。这里我们包含它们，是为了清晰起见，也因为以后在客户端应用程序 (in the client applications) 中需要知道输出张量的名称。

要获取所有支持的字段，及其值的详细信息，请参阅 [model config protobuf definition file](https://link.zhihu.com/?target=https%3A//github.com/triton-inference-server/common/blob/main/protobuf/model_config.proto)。

# MPI 与 NCCL 说明

## 1. 概述

**(1) MPI**

MPI，全称为消息传递接口（Message Passing Interface），是一个标准化和便携式的消息传递系统，设计用于并行计算中的进程间通信。MPI 提供了一种在分布式内存系统中进行进程间通信的方法，这是并行计算的一种常见模式。在这种模式中，每个进程都有自己的私有内存，进程之间的通信需要通过消息传递来完成。

**(2)  NCCL**

NCCL是Nvidia Collective multi-GPU Communication Library的简称，它是一个实现多GPU的collective communication通信（all-gather, reduce, broadcast）库，Nvidia做了很多优化，以在PCIe、Nvlink、InfiniBand上实现较高的通信速度。

## 2. NCCL

NCCL实现成CUDA C++ kernels，包含3种primitive operations： Copy，Reduce，ReduceAndCopy。目前NCCL 1.0版本只支持单机多卡，卡之间通过PCIe、NVlink、GPU Direct P2P来通信。NCCL 2.0会支持多机多卡，多机间通过Sockets (Ethernet)或者InfiniBand with GPU Direct RDMA通信。

- 并行任务的通信一般可以分为：
  
  - Point-to-point communication
  
  - Collective communication。

- P2P通信这种模式只有一个sender和一个receiver，实现起来比较简单。

- Collective communication包含多个sender多个receiver，一般的通信原语包括：
  
  - broadcastgather
  
  - all-gather
  
  - scatter
  
  - reduce：从多个sender那里接收数据，最终combine到一个节点上。
  
  - all-reduce：从多个sender那里接收数据，最终combine到每一个节点上。
  
  - reduce-scatter
  
  - all-to-all

而传统Collective communication假设通信节点组成的topology是一颗fat tree，这样通信效率最高。但实际的通信topology可能比较复杂，并不是一个fat tree。因此一般用ring-based Collective communication。

ring-base collectives将所有的通信节点通过首尾连接形成一个单向环，数据在环上依次传输。以broadcast为例， 假设有4个GPU，GPU0为sender将信息发送给剩下的GPU，按照环的方式依次传输，GPU0-->GPU1-->GPU2-->GPU3，若数据量为N，带宽为B，整个传输时间为（K-1）N/B。时间随着节点数线性增长，不是很高效。

GPU1接收到GPU0的一份数据后，也接着传到环的下个节点，这样以此类推，最后花的时间为

S*(N/S/B) + (k-2)*(N/S/B) = N(S+K-2)/(SB) --> N/B，条件是S远大于K，即数据的份数大于节点数，这个很容易满足。所以通信时间不随节点数的增加而增加，只和数据总量以及带宽有关。其它通信操作比如reduce、gather以此类推。

那么在以GPU为通信节点的场景下，怎么构建通信环呢？

# Triton23.10部署TensorRT-LLM

### 0. 概述

TensorRT-LLM发布了，继承自fastertransformer，是大语言版本的TensorRT，依赖TensorRT9.x版本去跑。主要介绍下新特性：

- 特殊版本的trt，**有些架构不支持，比如图灵**（来源 NVIDIA AI Inference Day 大模型推理线上研讨会），另外Torch-TensorRT目前继续使用trt-8.6，之后迁移到trt-10.0
- 写TensorRT-plugin更方便了，可以使用python写plugin
- 更新支持SD和NLP相关模型的支持和优化，与时俱进

### 1. 安装docker-ce 和 nvidia-container-toolkit

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
     && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
     && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
           sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
           sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
apt update
apt install nvidia-container-toolkit
```

### 2. 拉取镜像

```bash
docker pull nvcr.io/nvidia/tritonserver:23.10-trtllm-python-py3

# 运行镜像
docker run --gpus all -itd --network=host \
-v /sda/AIRepo/TRTDir:/TRTDir \
--name triton-trtllm \
nvcr.io/nvidia/tritonserver:23.10-trtllm-python-py3
# docker run --gpus all -itd --network=host \
# -v /sda/AIRepo/TRTDir:/TRTDir \
# --name triton-trtllm \
# --ulimit core=0 --ulimit memlock=-1 --ulimit stack=67108864 \
# --shm-size=100G \
# nvcr.io/nvidia/tritonserver:23.10-trtllm-python-py3
```

### 3. 配置镜像

```bash
cd /TRTDir
# 添加git-lfs仓库并下载
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh |  bash -
apt update
apt install -y git git-lfs
# 安装cmake
apt install -y cmake
pip3 install cmake

# 下载chatglm2-6b Hugging Face 预训练模型
# ps autodl 加速 source /etc/network_turbo
git clone https://huggingface.co/THUDM/chatglm2-6b
cd chatglm2-6b
git lfs install
git lfs pull
# 下载 TensorRT-LLM 源代码用于编译
git clone https://github.com/NVIDIA/TensorRT-LLM.git
cd TensorRT-LLM
git submodule update --init --recursive
git lfs install
git lfs pull


# 换源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 安装依赖（需连接网络）
pip install -e /TRTDir/TensorRT-LLM
# 安装依赖python包（需连接网络）并编译（6核12线程耗时58min）
python3 ./scripts/build_wheel.py --trt_root /usr/local/tensorrt
# 安装编译好的python包
pip install ./build/tensorrt_llm*.whl
# 退出容器并commit为镜像保存上下文
```

### 构建ChatGLM2 engine

```bash
python3 build.py \
--model_dir=/TRTDir/chatglm2-6b  \
--dtype=float16 \
--use_gpt_attention_plugin=float16 \
--use_gemm_plugin=float16

python3 build.py \
--model_dir=/TRTDir/chatglm2-6b \
--dtype=float16 \
--use_gpt_attention_plugin=float16 \
--use_gemm_plugin=float16 \
--output_dir=trtModel2 \
--use_weight_only \
--weight_only_precision=int8

python run.py --engine_dir=trtModel2
```

### 并发

```bash
python3 build.py --model_name=chatglm2_6b 
                 --model_dir=/root/autodl-tmp/chatglm2-6b 
                 --output_dir=trtModel 
                 --use_weight_only 
                 --weight_only_precision=int8 
                 --tp_size=2 --world_size=2

mpirun --allow-run-as-root -n 2 python run.py 
       --engine_dir=trtModel 
       --model_name=chatglm2_6b 
       --tokenizer_dir=/root/autodl-tmp/chatglm2-6b  
       --input_text="Hello tell me about Iphone"
```

### 千问7B

```bash
# 拉取镜像并运行
docker run -d \    
    --name triton2 \
    --net host \
    --shm-size=2g \
    --ulimit memlock=-1 \
    --ulimit stack=67108864 \
    --gpus all \
    -v ${PWD}/tensorrtllm_backend:/tensorrtllm_backend \
    #-v ${PWD}/Qwen-7B-Chat-TensorRT-LLM/qwen:/root/qwen \
    -v ${PWD}/Qwen-7B-Chat-TensorRT-LLM/chatglm2-6b:/root/chatglm2-6b \
    -v ${PWD}/TensorRT-LLM-build:/TensorRT-LLM-build \
    nvcr.io/nvidia/tritonserver:23.10-trtllm-python-py3 sleep 864000

# 进入容器，安装git-lfs
apt update
apt install git-lfs

# 安装TensorRT-LLM python版，方便待会编译Engine
# pip install git+https://github.com/NVIDIA/TensorRT-LLM.git
pip install -e  /TensorRT-LLM-build

# 复制lib库过去，否则无法运行
mkdir /usr/local/lib/python3.10/dist-packages/tensorrt_llm/libs/
cp /opt/tritonserver/backends/tensorrtllm/* /usr/local/lib/python3.10/dist-packages/tensorrt_llm/libs/

# 进入qwen目录
cd /root/qwen
# 安装依赖
pip install -r /root/qwen/requirements.txt
# 转smooth int8 权重（可选）
# 将Huggingface格式的数据转成FT(FastTransformer)需要的数据格式
python3 /root/qwen/hf_qwen_convert.py # 不要用 --smoothquant=0.5
# 编译
# qwen
python3 build.py --use_weight_only --weight_only_precision=int8
# chatgml2-6b
python3 build.py --model_dir=./chatglm2-6b --dtype float16 --use_gpt_attention_plugin float16 --use_gemm_plugin float16
# 运行测试
python3 run.py
```

### 参考文献

https://zhuanlan.zhihu.com/p/668548188

https://www.http5.cn/index.php/archives/55/

https://huggingface.co/THUDM/chatglm2-6b

[GitHub - triton-inference-server/tensorrtllm_backend: The Triton TensorRT-LLM Backend](https://github.com/triton-inference-server/tensorrtllm_backend)

https://ai.oldpan.me/t/topic/260

https://zhuanlan.zhihu.com/p/663338695

https://github.com/Tlntin/Qwen-7B-Chat-TensorRT-LLM

https://zhuanlan.zhihu.com/p/664545577

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
