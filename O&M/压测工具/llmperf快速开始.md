# llmperf快速开始

## 一、环境准备

### 1. 克隆代码并编译镜像

- 克隆代码

```bash
git clone https://github.com/ray-project/llmperf.git
cd llmperf
touch Dockerfile
```

- Dockerfile

```dockerfile
FROM python:3.10

ADD . /workspace/llmperf

WORKDIR /workspace/llmperf

RUN  pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
&& pip install --upgrade pip \
&& pip install torch \
&& pip install -e .
```

- 编译镜像

```bash
docker build -t llmperf:v0.2 -f Dockerfile  .
```

## 二、使用指南

### 1. 启动容器

- 启动容器

网络与被测服务处于相同网络栈

```bash
docker run -itd --name llmperf \
                --network container:xinference-test \
                -v `pwd`:`pwd` \
                llmperf:v0.2 bash

docker exec -it llmperf
```

- 添加缓存

在内网或网络环境不好时，请下载 huggingface.tar.gz，并在容器中执行以下操作

```bash
cp huggingface.tar.gz ~/.cache
cd ~/.cache 
tar -xzf huggingface.tar.gz
```

### 2. 测试

#### 2.1 OpenAI接口

```bash
OPENAI_API_KEY=secret_abcdefg OPENAI_API_BASE="http://localhost:9997/v1"   \
python token_benchmark_ray.py \
--model "/sda/AIRepo/TRTDir/Models/Qwen-1_8B-Chat" \
--mean-input-tokens 550 --stddev-input-tokens 150 \
--mean-output-tokens 150 \
--stddev-output-tokens 10 \
--max-num-completed-requests 2 \
--timeout 600 --num-concurrent-requests 1 -\
-results-dir "result_outputs" \
--llm-api openai \
--additional-sampling-params '{}'
```

- `OPENAI_API_KEY`: 秘钥（必填）

- `OPENAI_API_BASE` : 服务地址（必填）

- `--model` Tokenizer地址

- `--max-num-completed-requests` : 总请求数量

- `--num-concurrent-requests` : 并发数量

- `--llm-api` : 接口类型

### 3. 故障处理

#### 3.1 注意 `llmperf` 库的文件位置

> hint: 如果需要在挂载的代码中调试，请重新安装该代码

- llmperf库的位置由安装位置决定

```bash
cd /workspace/llmperf
pip install -e .
```

#### 3.2 注意最后一个 `choice` 列表可能为空

```python
@ray.remote
class OpenAIChatCompletionsClient(LLMClient):
    """Client for OpenAI Chat Completions API."""
    ......
                    delta = data["choices"][0]["delta"]
```

修改为

```python
```python
@ray.remote
class OpenAIChatCompletionsClient(LLMClient):
    """Client for OpenAI Chat Completions API."""
    ......
                    try:
                        delta = data["choices"][0]["delta"]
                    except:
                        continue
```

```
## 参考资料

https://github.com/ray-project/llmperf
```
