# Lora-Scripts快速开始

## 一、基本流程

### 1.

#### 1.1 容器创建

进入 AutoDL  在镜像处选择社区镜像，输入lora，找到Lora-Scripts v1.9。 

等待机器创建完成后，进入JupyterLab。

#### 1.2 GUI启动并进行端口映射到本地

然后检查是否处于lora-scripts文件夹；

执行 jupyternodebook中的运行指令

```bash
!export HF_HOME=huggingface && export HF_ENDPOINT=https://hf-mirror.com && source /etc/network_turbo && python gui.py
```

端口映射

```bash
ssh -CNgv -L 28000:localhost:28000 -p 18676 root@connect.westb.seetacloud.com
wCzrFaqChG8I
```

#### 1.3 下载基础模型

配置加速

```bash
source /etc/network_turbo
```

清理模型

```bash
# 清理sdxl模型
cd /root/lora-scripts/sd-models/
rm -rf sd_xl_base_1.0.safetensors model.safetensors
rm -f vae/sdxl_vae.safetensors
```

下载SD14模型用于打标签（非必须）

> 注意： 模型下载位置为 `/root/lora-scripts/huggingface/hub`。

> 注意： 模型名称由 models--{用户名}--{仓库名} 组成，如 `models--SmilingWolf--wd-v1-4-convnextv2-tagger-v2`

```bash
# 下载tagger模型（自动下载） （添加代理 export HF_ENDPOINT=https://hf-mirror.com）
#模型位置： /root/lora-scripts/huggingface/hub
# 下载 flux 基础模型
cd autodl-container-738045a6b5-f46f91d8
wget https://huggingface.co/Kijai/flux-fp8/resolve/main/flux1-dev-fp8-e4m3fn.safetensors
```

下载FLUX1.dev模型

```bash
autodl-tmp/models/
|-- FLUX.1-clip_l.safetensors
|-- FLUX.1-t5xxl_fp8_e4m3fn.safetensors
|-- FLUX.1-vae.safetensors
`-- flux1-dev-fp8-e4m3fn.safetensors
# 下载 flux 基础模型
cd autodl-container-738045a6b5-f46f91d8
wget https://huggingface.co/Kijai/flux-fp8/resolve/main/flux1-dev-fp8-e4m3fn.safetensors
```

上传训练图片

```bash
cd /root/lora-scripts/train
mkdir -p ${name}/${repitition}_${name}
```

## 参考资料

- bilibili

https://www.bilibili.com/read/cv24050162/
