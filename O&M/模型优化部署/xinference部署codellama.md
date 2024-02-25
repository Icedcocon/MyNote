# xinference部署codellama

## 一、资源获取

### 1.0 HF 模型文件说明

```bash
chatglm2-6b
├── config.json                         # 模型配置文件
├── configuration_chatglm.py            # ChatGLMConfig类
├── modeling_chatglm.py                 # 模型的Pytorch定义
├── MODEL_LICENSE
├── pytorch_model-00001-of-00007.bin    # Pytorch模型/权重
├── pytorch_model-00002-of-00007.bin    # Pytorch模型/权重
├── pytorch_model-00003-of-00007.bin    # Pytorch模型/权重
├── pytorch_model-00004-of-00007.bin    # Pytorch模型/权重
├── pytorch_model-00005-of-00007.bin    # Pytorch模型/权重
├── pytorch_model-00006-of-00007.bin    # Pytorch模型/权重
├── pytorch_model-00007-of-00007.bin    # Pytorch模型/权重
├── pytorch_model.bin.index.json        # 模型各层权重到上述bin文件映射
├── quantization.py                     # 模型量化脚本
├── README.md
├── tokenization_chatglm.py             # Tockenizer脚本
├── tokenizer_config.json               # Tockenizer配置
└── tokenizer.model                     # Tockenizer映射文件
```

#### 1.1

```bash
git clone https://github.com/xorbitsai/inference.git
cd inference
docker build --progress=plain -t test -f xinference/deploy/docker/Dockerfile .
```

## 二、故障排除

### 1. Bfloat及显存不足问题

- 修改`/opt/conda/lib/python3.10/site-packages/xinference/model/llm/vllm/core.py` 第134行

```python
self._model_config["gpu_memory_utilization"] = 1.0
self._model_config["max_model_len"] = 1024
engine_args = AsyncEngineArgs(model=self.model_path, **self._model_config,
                              dtype="half", enforce_eager=True)
self._engine = AsyncLLMEngine.from_engine_args(engine_args)
```

- 参数列表位于 `vllm/vllm/engine/arg_utils.py 19 dtype: str`

`/opt/conda/lib/python3.10/site-packages/xinference/api/restful_api.py` 836行

`/opt/conda/lib/python3.10/site-packages/xinference/core/model.py`  250行

- ModelActor import VLLM 并导入和初始化模型

`/opt/conda/lib/python3.1/site-packages/xinference/model/llm/vllm/core.py` 324行

`VLLMModel->async_generate` 存在问题 

```python
assert self._engine is not None
results_generator = self._engine.generate(prompt, sampling_params, request_id)

async def stream_results() -> AsyncGenerator[CompletionChunk, None]:
    previous_texts = [""] * sanitized_generate_config["n"]
    async for _request_output in results_generator:
        chunk = self._convert_request_output_to_completion_chunk(
            request_id=request_id,
            model=self.model_uid,
            request_output=_request_output,
        )
        for i, choice in enumerate(chunk["choices"]):
            delta = choice["text"][len(previous_texts[i]) :]
            previous_texts[i] = choice["text"]
            choice["text"] = delta
        yield chunk
```

- 容器故障排除

```bash
CUDA: Check failed: e == cudaSuccess (803 vs. 0) : system has unsupported display driver / cuda driver combination
```

此问题的根本原因：

主机和 Docker 之间的 CUDA 驱动程序不匹配

删除所有兼容文件 /usr/local/cuda/compat/

如果主机有足够新的驱动程序，则无需使用 compat lib。

## 一、部署指南

### 1. xinference 部署

- 容器启动指令

```bash
docker run --gpus "device=0" \
           -p 9997:9997 \
           -p 8082:8082 \
           -itd \
           --restart unless-stopped \
           -v /sda/AIRepo/TRTDir/:/TRTDir \
           -v /root/code-server/config:/config \
           --name xinference \
           --env PASSWORD=""
           xinference:code-server xinference-local --host 0.0.0.0 --port 9997
```

- 修改Bfloat及显存不足问题

### 2. One API 部署

- 部署 one api

```bash
docker run --name one-api -d --restart unless-stopped -p 3000:3000 -e TZ=Asia/Shanghai -v /root/one-api/data/data justsong/one-api:latest
```

- 初始账号用户名为 root，密码为 123456。
- 添加 Xinference 的模型渠道，这里的 Base URL 需要填 Xinference 服务的端点，并且注册 `qwen-chat` (模型的 UID) 。
- 离线部署现需要修改`TIKTOKEN_CACHE_DIR` 环境变量以备份编码器缓存
  - 默认程序启动时会联网下载一些通用的词元的编码，如：gpt-3.5-turbo，在一些网络环境不稳定，或者离线情况，可能会导致启动有问题，可以配置此目录缓存数据，可迁移到离线环境。

### 3. FastGPT 部署

- 部署 FastGPT

```bash

```

- 如果遇到mango连不上，可以看一下docker 的 dns 配置文件

```bash
cat /etc/systemd/system/docker.service.d/docker-dns.conf
```

## 参考文档

- awq、gptq、guff等类型模型下载位置

https://huggingface.co/TheBloke

- 量化策略说明

https://hub.baai.ac.cn/view/30383

- xinference仓库

https://github.com/xorbitsai/inference/blob/main/README_zh_CN.md

- xinference文档

https://inference.readthedocs.io/zh-cn/latest/getting_started/installation.html

- 比较有用的博客 lamma.cpp部署

https://www.bingal.com/posts/codefuse-llama.cpp-usage/#%E5%AE%89%E8%A3%85-llama-cpp-python

[Code Llama 本地部署使用指南，并在 VSCode 和 chatbox 中使用 | BUG王](https://www.bingal.com/posts/code-llama-usage/#%E4%B8%8B%E8%BD%BD%E6%A8%A1%E5%9E%8B)

- 可部署的仓库

https://huggingface.co/TheBloke/CodeFuse-CodeLlama-34B-GPTQ/tree/main

- FastGPT + Xinference：一站式本地 LLM 私有化部署和应用开发

https://zhuanlan.zhihu.com/p/677208959

- FastGPT 官方文档

https://doc.fastgpt.in/docs/development/docker/

- 容器cuda环境不兼容说明

https://github.com/NVIDIA/nvidia-docker/issues/1256
