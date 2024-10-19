# TensorRT-Triton学习指南及镜像使用说明

## 一、 TensorRT 学习指南

- NVIDIA 官方人员录制视频
  
  - 建议学习范围：Part1
  
  - 地址： https://www.bilibili.com/video/BV1jj411Z7wG/?spm_id_from=333.337.search-card.all.click&vd_source=fefc74ddfb7b0b365d1b1d4af922a0ba
  
  - 资料下载地址：  https://github.com/NVIDIA/trt-samples-for-hackathon-cn.gi

- 镜像 `triton_trt_llm:rel` 中的脚本
  
  - 建议学习范围： build.py 、 run.py
  
  - 地址： 进入容器 /app/tensorrt_llm/examples/chatglm
  
  - 完成资料： /app/tensorrt_llm 路径下即为github仓库源码

- TensorRT Python API
  
  - 建议学习范围： 对核心类如 `# ICudaEngine` 、 `Runtime` 、 `Builder` 了解即可
  - 地址： [ICudaEngine &mdash; NVIDIA TensorRT Standard Python API Documentation 8.6.1 documentation](https://docs.nvidia.com/deeplearning/tensorrt/api/python_api/infer/Core/Engine.html)

- TensorRT C++ API 及 CUDA 相关
  
  - 建议学习范围： 不建议学习

## 二、 Triton 学习指南

- NVIDIA 官方指南
  
  - 建议学习范围： 建议从编程入门开始，开始的产品介绍不建议学习
  
  - 网址： https://www.bilibili.com/video/BV1234y157Xh/?spm_id_from=333.788&vd_source=fefc74ddfb7b0b365d1b1d4af922a0ba

- 镜像 `triton_trt_llm:rel` 中的脚本
  
  - 建议学习范围：对照视频了解参数含义即可
  
  - 地址: 进入容器 /app/scripts/launch_triton_server.py
  
  - 完整资料：/opt/tritonserver为其大部分源码

- Python Backend
  
  - 建议学习范围： 根据上述视频入门即可，资料用于查阅
  
  - 资料： https://github.com/triton-inference-server/python_backend

## 三、 镜像及模型使用指南

- 镜像和模型位置：
  
  - 10.151.11.52:/fry/downloads
  
  - 10.151.11.61:/mnt/inaisfs/fry/downloads

- 镜像使用说明
  
  - triton_trt_llm.tar.gz 包含triton和tensort依赖的镜像（强烈推荐）
  
  - tensorrt_llm_release.tar.gz 仅包含tensort
  
  - vllm.tar.gz 包含vllm依赖
  
  - chatglm2_6b.tar.gz HuggingFace模型仓库，内涵模型权重，请解压使用
  
  - internlm-chat-20b.tar.gz 同上

- 容器运行说明

```bash
```bash
docker run -d \    
    --name tritonllm \
    --net host \
    --gpus all \
    -v /${Models}:/${Models} \
    triton_trt_llm:rel sleep 864000
```
