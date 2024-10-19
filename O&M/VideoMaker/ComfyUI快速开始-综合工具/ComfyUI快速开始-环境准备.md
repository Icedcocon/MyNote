# ComfyUI快速开始

## 一、环境准备

### 1. 启动指令

#### 1.1 启动指令

- 拉取镜像

```bash
docker pull yanwk/comfyui-boot:megapak
```

- 启动镜像

```bash
docker run -it --rm \
  --name comfyui \
  --gpus all \
  -p 8188:8188 \
  -v $PWD/storage:/home/runner \
  -v $PWD/ComfyUI:/root/ComfyUI \
  -e CLI_ARGS="" \
  yanwk/comfyui-boot:megapak
```

- 启动会下载模型到 `/root/ComfyUI/models` 路径下

#### 1.2 容器内路径说明

- **/builder-scripts**：存放构建过程中的依赖和安装脚本。
- **/runner-scripts**：存放容器运行时执行的启动和配置脚本。
- **/root/.download-complete**：标志下载是否完成的文件。
- **/root/ComfyUI**：存放 ComfyUI 程序代码的目录，也是容器的工作目录。
- **/root/user-scripts**：存放用户自定义脚本的目录，允许用户在启动时执行自定义任务。
- **/root/.config**：存放用户级别配置文件的目录。
- **/root/.cache**：用于缓存下载的包和编译文件，以加快操作速度。
- **/root/.cache/pycache**：集中存储 Python 字节码缓存文件的目录。

### 2. 脚本说明

#### 2.1 入口脚本 entrypoint.sh

##### 2.1.1 设置代理

```bash
# Run user's set-proxy script
cd /root
if [ ! -f "/root/user-scripts/set-proxy.sh" ] ; then
    mkdir -p /root/user-scripts
    cp /runner-scripts/set-proxy.sh.example /root/user-scripts/set-proxy.sh
else
    echo "[INFO] Running set-proxy script..."

    chmod +x /root/user-scripts/set-proxy.sh
    source /root/user-scripts/set-proxy.sh
fi ;
```

- 检查 `/root/user-scripts/set-proxy.sh` 文件是否存在。

- 如果文件不存在，创建 `/root/user-scripts` 目录。

- 将示例代理脚本复制到用户脚本目录。

- 执行代理设置脚本。

##### 2.1.2 安装 ComfyUI

```bash
# Install ComfyUI
cd /root
if [ ! -f "/root/.download-complete" ] ; then
    chmod +x /runner-scripts/download.sh
    bash /runner-scripts/download.sh
fi ;
```

- 检查是否存在 `.download-complete` 文件（用来标记 ComfyUI 是否已下载）。

- 如果文件存在，跳过下载步骤。

##### 2.1.3 运行用户的预启动脚本

```bash
cd /root
if [ ! -f "/root/user-scripts/pre-start.sh" ] ; then
    mkdir -p /root/user-scripts
    cp /runner-scripts/pre-start.sh.example /root/user-scripts/pre-start.sh
else
    echo "[INFO] Running pre-start script..."

    chmod +x /root/user-scripts/pre-start.sh
    source /root/user-scripts/pre-start.sh
fi ;
```

- 执行预启动脚本。

##### 2.1.4 启动 ComfyUI

```bash
# Let .pyc files be stored in one place
export PYTHONPYCACHEPREFIX="/root/.cache/pycache"
# Let PIP install packages to /root/.local
export PIP_USER=true
# Add above to PATH
export PATH="${PATH}:/root/.local/bin"
# Suppress [WARNING: Running pip as the 'root' user]
export PIP_ROOT_USER_ACTION=ignore

cd /root

python3 ./ComfyUI/main.py --listen --port 8188 ${CLI_ARGS}
```

- 设置环境变量
  
  - `export PYTHONPYCACHEPREFIX="/root/.cache/pycache"`：将 Python 的 `.pyc` 缓存文件存放在指定目录。
  - `export PIP_USER=true`：设置 PIP 安装包到 `/root/.local` 目录。
  - `export PATH="${PATH}:/root/.local/bin"`：将 PIP 安装的包目录添加到系统 PATH 中。
  - `export PIP_ROOT_USER_ACTION=ignore`：抑制 PIP 作为 root 用户执行时的警告。

- 启动 ComfyUI 服务，监听端口 8188，并传递可能的命令行参数 `${CLI_ARGS}`。

#### 2.2 代理脚本 set-proxy.sh

- 未使用

#### 2.3 下载脚本 download.sh

##### 2.3.1 全局设置

```bash
set -euo pipefail
```

设置脚本选项：

- `-e`：一旦有任何命令返回非零退出状态，脚本将立即退出。
- `-u`：在脚本中使用未定义的变量将导致错误。
- `-o pipefail`：如果管道中的任何命令失败，整个管道的退出状态将是非零值。

##### 2.3.2 仓库克隆/更新函数

```bash
# Regex that matches REPO_NAME
# First from pattern [https://example.com/xyz/REPO_NAME.git] or [git@example.com:xyz/REPO_NAME.git]
# Second from pattern [http(s)://example.com/xyz/REPO_NAME]
# They all extract REPO_NAME to BASH_REMATCH[2]
function clone_or_pull () {
    if [[ $1 =~ ^(.*[/:])(.*)(\.git)$ ]] || [[ $1 =~ ^(http.*\/)(.*)$ ]]; then
        echo "${BASH_REMATCH[2]}" ;
        set +e ;
            git clone --depth=1 --no-tags --recurse-submodules --shallow-submodules "$1" \
                || git -C "${BASH_REMATCH[2]}" pull --ff-only ;
        set -e ;
    else
        echo "[ERROR] Invalid URL: $1" ;
        return 1 ;
    fi ;
}
```

定义了一个名为 `clone_or_pull` 的函数，该函数的作用是克隆或更新给定的 Git 仓库：

- `if [[ $1 =~ ^(.*[/:])(.*)(\.git)$ ]] || [[ $1 =~ ^(http.*\/)(.*)$ ]]; then`：检查输入的 URL 是否匹配特定模式：
  - 第一个模式匹配类似 `https://example.com/xyz/REPO_NAME.git` 或 `git@example.com:xyz/REPO_NAME.git` 的 URL。
  - 第二个模式匹配类似 `http(s)://example.com/xyz/REPO_NAME` 的 URL。
- `echo "${BASH_REMATCH[2]}"`：提取匹配模式中的 `REPO_NAME`。
- `set +e`：临时禁用 `-e` 选项，以允许 `git clone` 命令失败时继续执行。
- `git clone --depth=1 --no-tags --recurse-submodules --shallow-submodules "$1"`：尝试克隆仓库。
- `|| git -C "${BASH_REMATCH[2]}" pull --ff-only`：如果克隆失败，尝试在已有目录中进行 `git pull` 操作。
- `set -e`：恢复 `-e` 选项。
- `else`：如果 URL 不匹配预期模式：
- `echo "[ERROR] Invalid URL: $1"`：输出错误信息。
- `return 1`：返回非零状态表示失败。

##### 2.3.3 下载 ComfyUI 和管理器

```bash
cd /root
clone_or_pull https://github.com/comfyanonymous/ComfyUI.git

cd /root/ComfyUI/custom_nodes
clone_or_pull https://github.com/ltdrdata/ComfyUI-Manager.git
```

- 使用 `clone_or_pull` 函数克隆或更新 `https://github.com/comfyanonymous/ComfyUI.git` 仓库。
- 切换到 `ComfyUI/custom_nodes` 目录，克隆或更新 `https://github.com/ltdrdata/ComfyUI-Manager.git` 仓库。

##### 2.3.4 下载自定义节点

```bash
cd /root/ComfyUI/custom_nodes
clone_or_pull https://github.com/11cafe/comfyui-workspace-manager.git
clone_or_pull https://github.com/AIGODLIKE/AIGODLIKE-ComfyUI-Translation.git
...
```

- 依次克隆或更新多个自定义节点仓库，例如 `https://github.com/11cafe/comfyui-workspace-manager.git` 和 `https://github.com/cubiq/ComfyUI_essentials.git`。

##### 2.3.4 下载模型

```bash
cd /root/ComfyUI/models
aria2c \
  --input-file=/runner-scripts/download-models.txt \
  --allow-overwrite=false \
  --auto-file-renaming=false \
  --continue=true \
  --max-connection-per-server=5
```

- 切换到 `ComfyUI/models` 目录，使用 `aria2c` 命令从 `download-models.txt` 文件中列出的 URL 下载模型文件。
  
  - `--allow-overwrite=false`：不允许覆盖已存在的文件。
  
  - `--auto-file-renaming=false`：禁用自动文件重命名。
  
  - `--continue=true`：启用断点续传功能。
  
  - `--max-connection-per-server=5`：设置每个服务器的最大连接数为 5。

##### 2.3.5 完成标志

- 创建一个 `.download-complete` 文件，标记下载过程的完成。

#### 2.4 Dockerfile 说明

这个 Dockerfile 文件用于构建一个名为 `yanwk/comfyui-boot:cu121-megapak` 的 Docker 镜像。该镜像集成了许多自定义节点，并使用了 CUDA 12.1、Python 3.11 和 GCC 12，主要用于深度学习相关的应用，特别是在使用 ComfyUI 时。下面是对 Dockerfile 的详细解释：

##### 2.4.1 基础镜像

```dockerfile
FROM docker.io/opensuse/tumbleweed:latest
LABEL maintainer="YAN Wenkun <code@yanwk.fun>"
```

- 使用 OpenSUSE Tumbleweed 作为基础镜像，这是一个滚动更新的 Linux 发行版。
- 通过 `LABEL` 指定维护者的信息。

##### 2.4.2 基本设置

```dockerfile
RUN set -eu
```

- `set -eu` 用于确保脚本在遇到错误或使用未定义变量时立即退出。

##### 2.4.3 安装 NVIDIA CUDA 开发工具包

```dockerfile
RUN --mount=type=cache,target=/var/cache/zypp \
    printf "\
[cuda-opensuse15-x86_64]\n\
name=cuda-opensuse15-x86_64\n\
baseurl=https://developer.download.nvidia.com/compute/cuda/repos/opensuse15/x86_64\n\
enabled=1\n\
gpgcheck=1\n\
gpgkey=https://developer.download.nvidia.com/compute/cuda/repos/opensuse15/x86_64/D42D0685.pub\n" \
        > /etc/zypp/repos.d/cuda-opensuse15.repo \
    && zypper --gpg-auto-import-keys \
        install --no-confirm --no-recommends --auto-agree-with-licenses \
cuda-cccl-12-1 ...
```

- 添加 NVIDIA CUDA 软件库，并使用 `zypper` 安装一系列 CUDA 12.1 的开发工具和库文件。
- 设置环境变量，使得 CUDA 工具和库能够被正确使用。

##### 2.4.4 安装 Python 及工具

```dockerfile
RUN --mount=type=cache,target=/var/cache/zypp \
    zypper addrepo --check --refresh --priority 90 \
        'https://ftp.gwdg.de/pub/linux/misc/packman/suse/openSUSE_Tumbleweed/Essentials/' packman-essentials \
    && zypper --gpg-auto-import-keys \
        install --no-confirm --auto-agree-with-licenses \
python311-devel ...
```

- 使用 `zypper` 安装 Python 3.11 及其开发工具、常用库和其他实用工具。
- 安装完成后，移除 Python 3.11 的 `EXTERNALLY-MANAGED` 文件，并将 Python 3.11 设置为默认的 Python 版本。

##### 2.4.5 安装 GCC 12

```dockerfile
RUN --mount=type=cache,target=/var/cache/zypp \
    zypper --gpg-auto-import-keys \
        install --no-confirm --auto-agree-with-licenses \
gcc12 ...
```

- 安装 GCC 12 及相关工具，并通过 `update-alternatives` 设置为系统默认的编译器。

##### 2.4.6 安装 Python 包（包括 PyTorch 和 xFormers）

```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip list \
    && pip install \
        --upgrade pip wheel setuptools \
    && pip install \
        xformers torchvision torchaudio \
        --index-url https://download.pytorch.org/whl/cu121 \
        --extra-index-url https://pypi.org/simple
```

- 升级 `pip`、`wheel` 和 `setuptools`。
- 安装 PyTorch 及相关的包，如 xFormers、TorchVision、TorchAudio，使用了 CUDA 12.1 对应的 PyTorch 轮子（whl）。

##### 2.4.7 绑定库文件

```dockerfile
ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}\
:/usr/local/lib64/python3.11/site-packages/torch/lib\
...
:/usr/local/lib/python3.11/site-packages/nvidia/nvtx/lib"
```

- 设置 `LD_LIBRARY_PATH` 环境变量，确保 CUDA 和 PyTorch 相关的库文件能够被正确加载。

##### 2.4.8 复制构建脚本并安装依赖

```dockerfile
COPY builder-scripts/.  /builder-scripts/
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install \
        -r /builder-scripts/pak3.txt ...
```

- 将构建脚本复制到容器中，然后根据这些脚本安装特定的 Python 包和依赖项。
- 安装 ONNX Runtime 的 CUDA 12 支持，并解决 MediaPipe 的依赖问题。

##### 2.4.9 清理和最终设置

```dockerfile
RUN du -ah /root && rm -rf /root/* /root/.*
COPY runner-scripts/.  /runner-scripts/
```

- 显示 `/root` 目录的磁盘使用情况，并删除所有文件进行清理。
- 复制运行脚本到容器中。

##### 2.4.10 容器运行配置

```dockerfile
USER root
VOLUME /root
WORKDIR /root
EXPOSE 8188
ENV CLI_ARGS=""
CMD ["bash","/runner-scripts/entrypoint.sh"]
```

- 设置容器以 `root` 用户运行。
- 暴露 8188 端口（用于 ComfyUI 的 Web 服务）。
- 设置容器启动时执行的默认命令。

## 二、模型准备

模型存放路径为 `/ComfyUI/models`

### 1. EchoMimic

#### 1.1 模型存放位置

```bash
models/echo_mimic/
├── audio_processor
│   └── whisper_tiny.pt
├── denoising_unet_acc.pth
├── denoising_unet.pth
├── face_locator.pth
├── motion_module_acc.pth
├── motion_module.pth
├── reference_unet.pth
├── unet
│   ├── config.json
│   └── diffusion_pytorch_model.bin
└── vae
    ├── config.json
    └── diffusion_pytorch_model.safetensors
```

#### 1.2 节点依赖

- requirements.txt

```bash
ffmpeg-python
mediapipe
moviepy
IPython
av
```

- 安装依赖

```bash
pip install -r requirements.txt
pip install opencv-python facenet_pytorch --no-cache-dir --no-deps
```

### 2. LayerStyle

#### 2.2 模型存放位置

```bash
models/
├── bert-base-uncased
│   ├── config.json
│   ├── model.safetensors
│   ├── tokenizer_config.json
│   ├── tokenizer.json
│   └── vocab.txt
├── BiRefNet
│   ├── BiRefNet-ep480.pth
│   ├── pvt_v2_b2(1).pth
│   ├── pvt_v2_b2(2).pth
│   ├── pvt_v2_b2.pth
│   ├── pvt_v2_b5.pth
│   ├── swin_base_patch4_window12_384_22kto1k.pth
│   └── swin_large_patch4_window12_384_22kto1k.pth
├── florence2
│   ├── base
│   │   ├── config.json
│   │   ├── configuration_florence2.py
│   │   ├── LICENSE
│   │   ├── modeling_florence2.py
│   │   ├── preprocessor_config.json
│   │   ├── processing_florence2.py
│   │   ├── pytorch_model.bin
│   │   ├── tokenizer_config.json
│   │   ├── tokenizer.json
│   │   └── vocab.json
│   ├── base-ft
│   │   ├── config.json
│   │   ├── configuration_florence2.py
│   │   ├── modeling_florence2.py
│   │   ├── preprocessor_config.json
│   │   ├── processing_florence2.py
│   │   ├── pytorch_model.bin
│   │   ├── tokenizer_config.json
│   │   ├── tokenizer.json
│   │   └── vocab.json
│   ├── base-PromptGen
│   │   ├── added_tokens(1).json
│   │   ├── added_tokens.json
│   │   ├── config.json
│   │   ├── configuration_florence2.py
│   │   ├── generation_config.json
│   │   ├── modeling_florence2.py
│   │   ├── model.safetensors
│   │   ├── preprocessor_config.json
│   │   ├── processing_florence2.py
│   │   ├── special_tokens_map.json
│   │   ├── tokenizer_config.json
│   │   ├── tokenizer.json
│   │   └── vocab.json
│   ├── CogFlorence-2.1-Large
│   │   ├── (1).gitattributes
│   │   ├── config.json
│   │   ├── configuration_florence2.py
│   │   ├── generation_config.json
│   │   ├── modeling_florence2.py
│   │   ├── model.safetensors
│   │   ├── preprocessor_config.json
│   │   ├── processing_florence2.py
│   │   ├── README.md
│   │   ├── tokenizer_config.json
│   │   ├── tokenizer.json
│   │   └── vocab.json
│   ├── CogFlorence-2-Large-Freeze
│   │   ├── config(1).json
│   │   ├── config.json
│   │   ├── configuration_florence2.py
│   │   ├── generation_config.json
│   │   ├── modeling_florence2.py
│   │   ├── model.safetensors
│   │   ├── preprocessor_config.json
│   │   ├── processing_florence2(1).py
│   │   ├── processing_florence2.py
│   │   ├── README.md
│   │   ├── tokenizer_config.json
│   │   ├── tokenizer.json
│   │   └── vocab.json
│   ├── DocVQA
│   │   ├── added_tokens.json
│   │   ├── config.json
│   │   ├── configuration_florence2.py
│   │   ├── generation_config.json
│   │   ├── modeling_florence2.py
│   │   ├── model.safetensors
│   │   ├── preprocessor_config.json
│   │   ├── processing_florence2.py
│   │   ├── processor_config(1).json
│   │   ├── processor_config.json
│   │   ├── special_tokens_map.json
│   │   ├── tokenizer_config.json
│   │   ├── tokenizer.json
│   │   └── vocab.json
│   ├── large
│   │   ├── config.json
│   │   ├── configuration_florence2.py
│   │   ├── generation_config.json
│   │   ├── LICENSE
│   │   ├── modeling_florence2.py
│   │   ├── preprocessor_config.json
│   │   ├── processing_florence2.py
│   │   ├── pytorch_model.bin
│   │   ├── sample_inference.ipynb
│   │   ├── tokenizer_config.json
│   │   ├── tokenizer.json
│   │   └── vocab.json
│   ├── large-ft
│   │   ├── config.json
│   │   ├── configuration_florence2.py
│   │   ├── generation_config.json
│   │   ├── LICENSE
│   │   ├── modeling_florence2.py
│   │   ├── preprocessor_config.json
│   │   ├── processing_florence2.py
│   │   ├── pytorch_model.bin
│   │   ├── tokenizer_config.json
│   │   ├── tokenizer.json
│   │   └── vocab.json
│   └── SD3-Captioner
│       ├── config.json
│       ├── configuration_florence2.py
│       ├── LICENSE
│       ├── modeling_florence2.py
│       ├── model.safetensors
│       ├── preprocessor_config.json
│       ├── processing_florence2.py
│       ├── tokenizer_config.json
│       ├── tokenizer.json
│       └── vocab.json
├── grounding-dino
│   ├── GroundingDINO_SwinB.cfg.py
│   ├── groundingdino_swinb_cogcoor.pth
│   ├── GroundingDINO_SwinT_OGC.cfg.py
│   └── groundingdino_swint_ogc.pth
├── lama
│   ├── big-lama.pt
│   ├── cond_stage_model_decode.pt
│   ├── cond_stage_model_encode.pt
│   ├── diffusion.pt
│   ├── erika.jit
│   ├── manga_inpaintor.jit
│   ├── Places_512_FullData_G.pth
│   ├── places_512_G.pth
│   ├── zits-edge-line-0717.pt
│   ├── zits-inpaint-0717.pt
│   ├── zits-structure-upsample-0717.pt
│   └── zits-wireframe-0717.pt
├── layerstyle
│   └── light_leak.pkl
├── LLavacheckpoints
│   └── files_for_uform_gen2_qwen
│       ├── cat.jpg
│       ├── config.json
│       ├── configuration_uform_gen.py
│       ├── generation_config.json
│       ├── interior.jpg
│       ├── model-00001-of-00002.safetensors
│       ├── model-00002-of-00002.safetensors
│       ├── modeling_uform_gen.py
│       ├── model.safetensors.index.json
│       ├── processing_uform_gen.py
│       ├── README.md
│       ├── temp.png
│       └── vision_encoder.py
├── mediapipe
│   └── selfie_multiclass_256x256.tflite
├── rmbg
│   └── RMBG-1.4
│       ├── model.pth
│       └── put model here.txt
├── sams
│   ├── mobile_sam.pt
│   ├── sam_hq_vit_b.pth
│   ├── sam_hq_vit_h.pth
│   ├── sam_hq_vit_l.pth
│   ├── sam_vit_b_01ec64.pth
│   ├── sam_vit_h_4b8939.pth
│   └── sam_vit_l_0b3195.pth
├── segformer_b2_clothes
│   ├── config.json
│   ├── handler.py
│   ├── model.safetensors
│   ├── optimizer.pt
│   ├── preprocessor_config.json
│   ├── pytorch_model.bin
│   ├── README.md
│   ├── rng_state.pth
│   ├── scheduler.pt
│   ├── trainer_state.json
│   └── training_args.bin
├── segformer_b3_clothes
│   ├── config.json
│   ├── model.safetensors
│   ├── preprocessor_config.json
│   └── README.md
├── segformer_b3_fashion
│   ├── config.json
│   ├── model.safetensors
│   ├── preprocessor_config.json
│   ├── pytorch_model_2.bin
│   ├── README.md
│   └── training_args.bin
├── transparent-background
│   ├── ckpt_base_nightly.pth
│   ├── ckpt_base.pth
│   ├── ckpt_fast.pth
│   ├── InSPyReNet_Clothing_latest4.pth
│   ├── InSPyReNet_SwinB_DIS5K.pth
│   ├── InSPyReNet_SwinB_HU.pth
│   └── InSPyReNet_SwinB_Plus_Ultra.pth
├── vitmatte
│   ├── config(1).json
│   ├── config.json
│   ├── model.safetensors
│   ├── preprocessor_config.json
│   ├── pytorch_model.bin
│   └── README.md
└── yolo
    ├── face_yolov8m.pt
    ├── face_yolov8n.pt
    ├── face_yolov8n_v2.pt
    ├── face_yolov8s.pt
    ├── face_yolov9c.pt
    ├── hand_yolov8n.pt
    ├── hand_yolov8s.pt
    ├── hand_yolov9c.pt
    ├── person_yolov8m-seg.pt
    ├── person_yolov8n-seg.pt
    └── person_yolov8s-seg.pt
```

#### 2.2 节点依赖

- requirements.txt

```bash
# ....
loguru
typer_config
google-generativeai
image-reward
blend_modes
blind-watermark
pyzbar
psd-tools
```

- 安装依赖

```bash
pip install -r requirements.txt
```

### 3. MimicMotionWrapper

#### 3.1 模型存放位置

```bash
custom_nodes/ComfyUI-MimicMotionWrapper/models/
├── DWPose
│   ├── dw-ll_ucoco_384_bs5.torchscript.pt
│   └── yolox_l.torchscript.pt
└── mimic_motion_pose_net.safetensors


models/mimicmotion/
└── MimicMotionMergedUnet_1-0-fp16.safetensors
```

#### 3.2 节点依赖

```bash
# diffusers>=0.28.0
# transformers>=4.32.1
# accelerate
```

#### 4. Flux

##### 4.1 模型安装位置

###### 4.1.1 原版

- flux.1 dev 或 flux.1 schnell

https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/flux1-dev.safetensors

- CLIP 文本编码器（可以仅下载clip_l和fp8模型）

https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/clip_l.safetensors

https://huggingface.co/comfyanonymous/flux_text_encoders/blob/main/t5xxl_fp8_e4m3fn.safetensors

- VAE 解码

https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/ae.safetensors

###### 4.1.2 Comfy Org版本

- Unet + CLIP + VAE

https://huggingface.co/Comfy-Org/flux1-dev/blob/main/flux1-dev-fp8.safetensors

###### 4.1.3 Kijai版本

- Unet-fp8

https://huggingface.co/Kijai/flux-fp8/blob/main/flux1-dev-fp8.safetensors

- 其余同原版

###### 4.1.4 下载方式

```bash
 # wget （将 blob 改为 resolve）
 wget https://huggingface.co/Kijai/flux-fp8/resolve/main/flux1-dev-fp8.safetensors
 # 仓库
 GIT_LFS_SKIP_SMUDGE=1 git clone git@hf.co:black-forest-labs/FLUX.1-dev
 cd FLUX.1-dev
 git lfs pull -I ae.safetensors
```

###### 4.1.5 模型存放位置

```bash
models/
├── unet
│   └──  FLUX.1-dev-fp8.safetensors
├── vae
│   └──  FLUX.1-vae.safetensors
└── clip
    ├──  FLUX.1-clip_l.safetensors
    └──  FLUX.1-t5xxl_fp8_e4m3fn.safetensors
```

##### 4.2 节点依赖

```bash
# GitPython
# einops==0.8.0
# transformers
# diffusers
# sentencepiece
# opencv-python
```

#### 5. ComfyUI-UVR5

##### 5.1 模型存放位置

##### 5.2 节点依赖

```bash
# ffmpeg-python
# librosa
# onnxruntime-gpu
```

#### 6. Comfy-RVC

##### 6.1 模型存放位置

- 仓库

[SayanoAI/RVC-Studio at main](https://huggingface.co/datasets/SayanoAI/RVC-Studio/tree/main)

/root/models

```bash
models/
├── RVC/
|   ├── Claire.pth
|   ├── Fuji.pth
|   ├── Mae_v2.pth
|   ├── Monika.pth
|   └── Sayano.pth
|   └── .index/
|       ├── added_IVF1063_Flat_nprobe_1_Sayano_v2.index
|       ├── added_IVF522_Flat_nprobe_1_Monika_v2.index
|       ├── added_IVF985_Flat_nprobe_1_Fuji_v2.index
|       └── Monika_v2_40k.index
├── UVR/
|   ├── 5_HP-Karaoke-UVR.pth
|   ├── 6_HP-Karaoke-UVR.pth
|   ├── download_checks.json
|   ├── HP5-vocals+instrumentals.pth
|   ├── mdx_model_data.json
|   ├── model_bs_roformer_ep_317_sdr_12.9755.ckpt
|   ├── UVR-BVE-4B_SN-44100-1.pth
|   ├── UVR-DeEcho-DeReverb.pth
|   ├── UVR-DeNoise.pth
|   └── vr_model_data.json
├── content-vec-best.safetensors
└── rmvpe.pt
```

##### 6.2 节点依赖

```bash
# For RVC
fairseq==0.12.2
faiss-cpu==1.7.4
audio-separator[gpu]
ffmpy
samplerate
pyaudio
spacy
monotonic_align
textacy
spacytextblob
deep-translator
openmim
tensorboard
```

##### 6.3 修改

- 修改根路径为 /root/ComfyUI `lib/__init__.py` 

```python
@lru_cache
def get_cwd():
    CWD = os.getcwd()
    if not CWD.endswith('ComfyUI'):
        CWD = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))
    if CWD not in sys.path:
        sys.path.append(CWD)
    return CWD
```

#### 7. KwaiKolorsWrapper / ComfyUI-Kolors-MZ (Kolors)

> 建议： 作为 Inpainting使用 （3761MiB）

ComfyUI-Kolors-MZ 为国人制作 相比于官方需要下载更少的文件，且可以复用原生的节点。

##### 7.1 模型存放位置 (ComfyUI-Kolors-MZ)

```bash
models/
├── clip_vision
│   └── Kolors_ipa_plus_clip.bin
├── ipadapter
│   └── Kolors_ip_adapter_plus_general.bin
├── LLM
│   └── chatglm3-4bit.safetensors
├── unet
│   ├── Kolors.fp16.safetensors
│   └── Kolors_Inpainting.safetensors
├── vae
│   └── sdxl_vae.safetensors
```

##### 7.2 节点依赖

```bash
# diffusers>=0.28.2
# transformers>=4.26.1
# sentencepiece
# accelerate
cpm-kernels
```

#### 8. ComfyUI_MiniCPM-V-2_6-int4

> 建议： 用于反推提示词

##### 8.1 模型存放位置

自动下载

```bash
models/prompt_generator/
└── MiniCPM-V-2_6-int4
    ├── added_tokens.json
    ├── config.json
    ├── configuration_minicpm.py
    ├── generation_config.json
    ├── image_processing_minicpmv.py
    ├── merges.txt
    ├── model-00001-of-00002.safetensors
    ├── model-00002-of-00002.safetensors
    ├── modeling_minicpmv.py
    ├── modeling_navit_siglip.py
    ├── model.safetensors.index.json
    ├── preprocessor_config.json
    ├── processing_minicpmv.py
    ├── README.md
    ├── resampler.py
    ├── special_tokens_map.json
    ├── test.py
    ├── tokenization_minicpmv_fast.py
    ├── tokenizer_config.json
    ├── tokenizer.json
    └── vocab.json
```

##### 8.2 节点依赖

```bash
# torch
# torchvision
# torchaudio
# numpy
# pillow
# huggingface_hub
# transformers
# accelerate
decord
bitsandbytes
```

#### 9 comfyui-deploy

平行于 ComfyUI 的 workflow job 托管。用于后台长期执行的流程。

##### 9.1 模型存放（无）

##### 9.2 节点依赖

```bash
aiofiles
# pydantic
# opencv-python
# imageio-ffmpeg
brotli
```

#### 10 ComfyUI-Anyline

ControlNet 预处理器： 图片转线稿

##### 10.1 模型存放

自动下载

##### 10.2 节点依赖

```bash
pathlib
# huggingface_hub
# scikit-image
```

#### 11 ComfyUI-DepthAnythingV2

##### 11.1 模型存放位置

自动下载

```bash
ComfyUI\models\depthanything
```

##### 11.2 节点依赖

## 参考

- Dockernization Github

https://github.com/YanWenKun/ComfyUI-Docker
