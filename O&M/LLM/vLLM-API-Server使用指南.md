# 部署问题记录-vLLM

## 一、 vLLM 仓库脚本自动构建镜像（推荐）

### 1. 环境

| 组件           | 版本                 |
| ------------ | ------------------ |
| Container OS | Ubuntu 22.04       |
| CUDA         | NVIDIA CUDA 12.1.0 |
| Python       | 3.10.12            |
| Pytorch      | 2.1.0              |

### 2. 镜像编译及运行

#### 2.1 克隆仓库并编译

1. 克隆仓库

```bash
git clone https://github.com/vllm-project/vllm.git
```

2. 拉取基础镜像

```bash
docker pull nvidia/cuda:12.1.0-devel-ubuntu22.04
```

3. 编译
   - Qwen7B 需要额外执行 `pip install tiktoken`

```bash
cd vllm
docker build -t vllm:v1 .
```

#### 2.2 dockerfile文件

```dockerfile
FROM nvidia/cuda:12.1.0-devel-ubuntu22.04 AS dev

RUN apt-get update -y \
    && apt-get install -y python3-pip

WORKDIR /workspace

# install build and runtime dependencies
COPY requirements.txt requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# install development dependencies
COPY requirements-dev.txt requirements-dev.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements-dev.txt

# image to build pytorch extensions
FROM dev AS build

# install build dependencies
COPY requirements-build.txt requirements-build.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements-build.txt

# copy input files
COPY csrc csrc
COPY setup.py setup.py
COPY requirements.txt requirements.txt
COPY pyproject.toml pyproject.toml
COPY vllm/__init__.py vllm/__init__.py

ARG torch_cuda_arch_list='7.0 7.5 8.0 8.6 8.9 9.0+PTX'
ENV TORCH_CUDA_ARCH_LIST=${torch_cuda_arch_list}
# max jobs used by Ninja to build extensions
ARG max_jobs=2
ENV MAX_JOBS=${max_jobs}
# number of threads used by nvcc
ARG nvcc_threads=8
ENV NVCC_THREADS=$nvcc_threads

RUN python3 setup.py build_ext --inplace

# image to run unit testing suite
FROM dev AS test

# copy pytorch extensions separately to avoid having to rebuild
# when python code changes
COPY --from=build /workspace/vllm/*.so /workspace/vllm/
COPY tests tests
COPY vllm vllm

ENTRYPOINT ["python3", "-m", "pytest", "tests"]

# use CUDA base as CUDA runtime dependencies are already installed via pip
FROM nvidia/cuda:12.1.0-base-ubuntu22.04 AS vllm-base

# libnccl required for ray
RUN apt-get update -y \
    && apt-get install -y python3-pip

WORKDIR /workspace
COPY requirements.txt requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

FROM vllm-base AS vllm
COPY --from=build /workspace/vllm/*.so /workspace/vllm/
COPY vllm vllm

EXPOSE 8000
ENTRYPOINT ["python3", "-m", "vllm.entrypoints.api_server"]

# openai api server alternative
FROM vllm-base AS vllm-openai
# install additional dependencies for openai api server
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install accelerate

COPY --from=build /workspace/vllm/*.so /workspace/vllm/
COPY vllm vllm

ENTRYPOINT ["python3", "-m", "vllm.entrypoints.openai.api_server"]
```

#### 2.3 运行

- vLLM的优点是可以直接使用HF仓库拉取的镜像，无需进行过多操作

```bash
docker run -d --name vllm --net host --gpus all 
           -v /sda/AIRepo/TRTDir:/TRTDir  
           vllm:v1 
           --model=/TRTDir/Models/chatglm2-6b 
           --trust-remote-code
           --max-model-len=1000
           --dtype half
           --enforce-eager
           --gpu-memory-utilization=1.0
           --served-model-name chatglm2-6b


docker run -d --name vllm --net host --gpus "device=0" -v /sda/AIRepo/TRTDir:/TRTDir vllm:v1 --model=/TRTDir/Models/CodeFuse-CodeLlama-34B-GPTQ --trust-remote-code --max-model-len=1024 --dtype half --enforce-eager --gpu-memory-utilization=1.0 --served-model-name code-fuse
```

#### 2.4 启动参数说明

```bash
api_server.py [-h] [--host HOST] [--port PORT] [--allow-credentials]
                   [--allowed-origins ALLOWED_ORIGINS]
                   [--allowed-methods ALLOWED_METHODS]
                   [--allowed-headers ALLOWED_HEADERS]
                   [--served-model-name SERVED_MODEL_NAME]
                   [--chat-template CHAT_TEMPLATE]
                   [--response-role RESPONSE_ROLE]
                   [--ssl-keyfile SSL_KEYFILE] [--ssl-certfile SSL_CERTFILE]
                   [--model MODEL] [--tokenizer TOKENIZER]
                   [--revision REVISION]
                   [--tokenizer-revision TOKENIZER_REVISION]
                   [--tokenizer-mode {auto,slow}] [--trust-remote-code]
                   [--download-dir DOWNLOAD_DIR]
                   [--load-format {auto,pt,safetensors,npcache,dummy}]
                   [--dtype {auto,half,float16,bfloat16,float,float32}]
                   [--max-model-len MAX_MODEL_LEN] [--worker-use-ray]
                   [--pipeline-parallel-size PIPELINE_PARALLEL_SIZE]
                   [--tensor-parallel-size TENSOR_PARALLEL_SIZE]
                   [--max-parallel-loading-workers MAX_PARALLEL_LOADING_WORKERS]
                   [--block-size {8,16,32}] [--seed SEED]
                   [--swap-space SWAP_SPACE]
                   [--gpu-memory-utilization GPU_MEMORY_UTILIZATION]
                   [--max-num-batched-tokens MAX_NUM_BATCHED_TOKENS]
                   [--max-num-seqs MAX_NUM_SEQS]
                   [--max-paddings MAX_PADDINGS] [--disable-log-stats]
                   [--quantization {awq,gptq,squeezellm,None}]
                   [--enforce-eager]
                   [--max-context-len-to-capture MAX_CONTEXT_LEN_TO_CAPTURE]
                   [--engine-use-ray] [--disable-log-requests]
                   [--max-log-len MAX_LOG_LEN]
```

## 二、vLLM 架构说明

### 1. vLLM架构

#### 1.1 架构说明

vLLM针对GPT类模型推理过程中KVCache这个显存占用大头专门设计了block_table，将KVCache分段成多个block存储在GPU中。一方面，这种设计可以共用beam search多batch之间share prompt sequence（的KVCache），减少显存占用。另一方面，在gpu显存和cpu内存间调度这些block，可以在有限的gpu显存空间下同时推理更大batch的sequence，换句话说，就是尽可能拉满gpu显存使用率，提高吞吐。

(ps:下文中图片地址： https://github.com/zhanzy178/vllm/blob/main/framework.drawio)

##### 整体架构

- LLMEngine：是整个系统的入口，`add_request`负责输入prompt请求，`step`迭代推理，最终返回LLM生成的结果。其内部组合了一个Scheduler和一组Worker。

- Scheduler：在每个推理步调度可处理的Sequence输入信息，其组合包含了一个BlockSpaceManager

- BlockSpaceManager：维护gpu显存和cpu内存的使用情况，以及Sequence对应Cache的BlockTable信息。

- Worker：在每个推理步执行LlamaForCausalLM推理，并返回采样后结果。除一个LLM模型外，其另一个核心组件是CacheEngine。

- CacheEngine：负责执行相关gpu、cpu空间的换入、换出、拷贝等操作。

##### LLMEngine

从图中可以看到，从上到下按先后顺序LLMEngine分别进行了`__init__`、`add_request`、`step`。

在构造LLMEngine时，LLMEngine就会调用Worker中的CacheEngine，初始化gpu、cpu空间，计算能容纳多少个block。每个block包含`block_size`个token对应的各层KVCache大小。在后续的组织中都会将Sequence对应的KVCache分成block_size大小的cache block，以方便管理对应block的空间。

`add_request`接口执行多次，接收多个待处理的prompt，将prompt处理成对应token的Sequence。每个输入prompt构造一个SequenceGroup， 其中包含了多个重复的Sequence为后续beam search做准备。SequenceGroup会最终保存到Scheduler中，以进行后续的调度。

`step`执行一个推理步。首先Scheduler会调度一组SequenceGroup和相关信息作为当前推理步的执行输入，除了输入外，还会包含当前SequenceGroup所需KVCache的换入换出信息。然后，Worker会将执行一次LLM推理（当然会先执行CacheEngine先准备KVCache）。Worker采样的输出结果会再次更新到Scheduler中的SequenceGroup内，以更新其内部的状态。最后，多次`step`循环，直到所有prompt对应的SequenceGroup都生成结束。

##### Scheduler

Scheduler中包含了三个队列：waitting、running、swapped。每当新增一个SequenceGroup时，添加至waitting队列中。

- waitting：等待计算KVCache的SequenceGroup（也就是prompt序列）

- running：执行推理的SequenceGroup，会在当前step中作为输入，一共包含两类：

- prompt：来自waitting，未计算KVCache的SequenceGroup

- generate token：计算过KVCache的SequenceGroup，准备生成下一个token

- swapped：KVCache暂时换出到cpu内存的SequenceGroup

在每次`schedule`执行时，会调度几个队列之间的SequenceGroup，维护队列间的状态，使得当前执行推理尽可能占满显存空间。详细逻辑如上图中的数字标号顺序所示，值得注意的是，通过调度能实现两种解决显存不足的策略，一个是换出到cpu中，另一个就是重计算了（只有在SequenceGroup内只有一个Sequence的情况才能使用）。

当SequenceGroup推理新增了token时，`update`接口会更新一遍SequenceGroup内的状态。如下图所示，SequenceGroup内包含一组beam search的seq，每次执行推理的时候，每个seq采样s次，那么久会生成n*s个生成的token，根据这里面token保留置信度topn个生成结果。下图所示的结果就是n=4的情况，可以看到topn保留的output里seq1和seq3都来自原始输入seq1（parent_seq=1），此时需要BlockSpaceManager将原始的seq3释放（因为保留的output里没有seq3的输出），然后从seq1拷贝/fork到seq3，再讲新token添加到各个seq中。

##### BlockSpaceManager

BlockSpaceManager的功能是管理各个SequenceGroup对应KVCache存储信息。回顾LLMEngine提到过的，每个Sequence的KVCache序列会分成多个block_size长度的cache block，每个cache block的位置信息记录在BlocKspaceManager。如下图所示，BlockSpaceManager包含一个block_tables，其记录cache block到gpu显存或cpu内存物理地址的映射。

SequenceGroup刚加入Scheduler的时候并没有分配cache block空间，第一次进入running的时候需要向BlockSpaceManager申请可用的block空间。如下图所示，BlockSpaceManager分配block空间是以一个SequenceGroup作为一组输入，而且默认分配空间的时候，所有SequenceGroup内的token都是一样的（即是相同的prompt），因此会为所有Sequence都指向同一片cache block区域，该区域被引用数为Sequence数量。

当需要为一个Sequence新增token时，如下图所示，有两种情况：

- 当前cache block空间不足添加新token，则新增cache block。
- 当前空间足以添加新token，但last block与其他Sequence共用时（ref_count>1），如果新token还是添加到last block，那么会与共用last block的其他Sequence冲突，则需要释放掉last block（free不是真的释放，只是ref_count-1），分配一个新的last block。最后，返回信息标记原本last block内容需要拷贝到这个新的last block，即所谓的“copy-on-write”。

实际上，BlockSpaceManager只负责维护cache block到gpu/cpu空间的索引，真正进行换入、换出、拷贝操作都需要通过Worker中CacheEngine进行。因此在Scheduler调度的时候，也会收集BlockSpaceManager返回结果，得到当前step所需KVCache的block_to_swap_in、block_to_swap_out、block_to_copy，以供后续CacheEngine操作内存空间。

##### Worker

Worker负责缓存更新执行和LLM推理执行。关于Worker的这个图比较长，因此这里截断成两张图来看。

如上图所示，Worker在执行时首先进行两个操作。

- 缓存更新：SchedulerOutputs包含了前面提到的当前所需swap in/swap out/copy的cache block信息，然后通过CacheEngine自定义的ops去执行缓存搬运操作，得到cuda stream的event，后续会在推理LLM各层的时候用到。
- 准备输入token序列`__prepare_input`：上图右侧的框内是预处理的过程，将SequenceGroupMetadata包含Scehduler调度得到running的所有SequenceGroup组合一个flatten的token序列，作为LLM的初始输入。Scheduler那节中提到过，running队列中当前执行的SequenceGroup有两类：一类未计算prompt（前缀）的KVCache，这部分需要完整的prompt token输入去计算各层的KVCache（全量推理）。另一类已经计算并缓存前缀的KVCache，因此只需要last token作为输入计算下一个generation token的分布（增量推理）。如上图所示，输入token序列的前半部分是多个prompt的token全量推理序列，后半部分是各个增量推理序列的last token。此外，全量推理的SequenceGroup中多个Sequence共享prompt，因此只需要任意一个Sequence的prompt作用输入就行。

上图是Worker执行LLM模型的过程。由`__prepare_input`组装的flatten token在各层映射成flatten hidden state。 除了线性层、激活层等token独立计算的层以外，attention层的计算涉及不同token的hidden state依赖。上图主要展开了Attention层的四个主要步骤：

- prompt全量推理：prompt序列通过xformers的attention算子计算得到下个layer的hidden state。由于这里attention计算的输入是完整的tensor，不是KVCache中分散的cache block，所以可以用第三方的attention算子完成计算。
- 等待缓存事件：CacheEngine中发送了异步缓存操作，因此只有当前层序列的cache block完成缓存更新，才能进一步获取KVCache或者记录KVCache，这种异步的实现能通过overlap计算和缓存搬运，节省一部分缓存搬运时间。
- 记录当前KVCache：当前层输入的hidden state作为KVCache通过自定义算子记录到对应cache block内，这里记录所有有效token的hidden state，包括prompt和last token（last token是前几次step中新增的，所以也没有缓存hidden state到KVCache）。
- generation token增量推理：vLLM的核心PageAttention即在此实现，这里作者通过一个自定义算子（好像是参考Faster Transformer实现），实现了基于BlockTable分散KVCache的增量attention计算。

最后LLM内的采样器进行采样，将beam_search结果（新token）返回给Worker输出。

#### 1.2 架构与源码对照表

```bash
vllm
├── block.py
├── config.py
├── core
│   ├── block_manager.py      # BlockSpaceManager ...
│   ├── scheduler.py          # Scheduler ...
│   ├── ...
├── engine
│   ├── llm_engine.py         # LLMEngine
│   ├── async_llm_engine.py   # AsyncLLMEngine ...
│   ├── ray_utils.py          # 分布式推理相关
│   ├── ...
├── worker
│   ├── cache_engine.py       # CacheEngine(管理kvCache)
│   ├── worker.py             # Worker ...
│   ├── model_runner.py       # ModelRunner 及 CUDA Graph
│   └── ...
├── sequence.py               # Sequence、SequenceGroup
├── entrypoints
│   ├── api_server.py         # API Server入口
│   ├── llm.py                # LLM 批处理入口
│   └── openai
│       ├── api_server.py
│       ├── ...
├── ...
```

### 1. 代码示例

```python
from vllm import LLM, SamplingParams

prompts = [
    "Hello, my name is",
    "The president of the United States is",
    "The capital of France is",
]
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

llm = LLM(model="qwen/Qwen-7B-Chat", trust_remote_code=True)
outputs = llm.generate(prompts, sampling_params)
```

## 三、接口调用

## 1. 常用接口

### 1.0 通用请求体参数列表

- **n**：为给定提示返回的输出序列数量。  

- **best_of**：从提示中生成的输出序列数量。  
  
  - 从生成的`best_of`个序列中返回排名前`n`的序列。`best_of`必须大于等于`n`。
  - 当`use_beam_search`为True时，这被当作束宽。 
  - 默认情况下，`best_of`设置为`n`。  

- **presence_penalty**：浮点数，基于新词汇是否出现在迄今为止生成的文本中对其进行处罚。
  
  - 值大于0鼓励模型使用新词汇，小于0鼓励模型重复词汇。  

- **frequency_penalty**：浮点数，基于新词汇在迄今为止生成的文本中的频率对其进行处罚。  
  
  - 值大于0鼓励模型使用新词汇，小于0鼓励模型重复词汇。  

- **repetition_penalty**：浮点数，基于新词汇是否出现在提示以及迄今为止生成的文本中对其进行处罚。 
  
  - 值大于1鼓励模型使用新词汇，小于1鼓励模型重复词汇。  

- **temperature**：控制采样随机性的浮点数。较低的值使模型更确定性，较高的值使模型更随机。
  
  - 零代表贪婪采样。  

- **top_p**：控制要考虑的顶部词汇累积概率的浮点数。
  
  - 必须在(0, 1]之间。设置为1以考虑所有词汇。  

- **top_k**：控制要考虑的顶部词汇数量的整数。
  
  - 设置为-1以考虑所有词汇。  

- **min_p**：代表相对于最可能词汇概率的词汇被考虑的最小概率的浮点数。  
  
  - 必须在[0, 1]之间。设置为0以禁用此功能。  

- **use_beam_search**：是否使用束搜索替代采样。  

- **length_penalty**：基于序列长度对序列进行处罚的浮点数。用于束搜索。  

- **early_stopping**：控制束搜索的停止条件。它接受以下值：
  
  - `True`，生成停止当有`best_of`完整候选出现时；  
  - `False`，应用启发式方法并在找到更好的候选者变得非常不可能时停止生成；  
  - `"never"`，束搜索程序只在不可能有更好的候选者时停止（典型束搜索算法）。  

- **stop**：一系列字符串，当生成时停止生成。返回的输出将不包含停止字符串。  

- **stop_token_ids**：生成时停止生成的词汇列表。
  
  - 返回的输出将包含停止词汇，除非停止词汇是特殊词汇。  

- **include_stop_str_in_output**：是否在输出文本中包含停止字符串。默认为False。  

- **ignore_eos**：是否忽略EOS令牌并在生成EOS令牌后继续生成令牌。  

- **max_tokens**：每个输出序列生成的最大词汇数。  

- **logprobs**：返回每个输出词汇的对数概率数。  
  
  - 注意实现遵循OpenAI API：返回结果将包含在`logprobs`最可能词汇上的对数概率，以及选定的词汇。 
  - API总是返回采样词汇的对数概率，因此响应中可能有多达`logprobs+1`个元素。  

- **prompt_logprobs**：返回每个提示词汇的对数概率数。  

- **skip_special_tokens**：是否在输出中跳过特殊词汇。  

- **spaces_between_special_tokens**：在输出中是否在特殊词汇间添加空格。默认为True。  

- **logits_processors**：一系列函数，基于先前生成的词汇修改logits。

### 1.1 Completions 续写

#### 1.1.1 接口说明

- `POST http://{{ip}}:{{port}}/v1/completions`

- 请求

```bash
curl http://{{ip}}:{{port}}/v1/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "text-davinci-003",
    "prompt": "Say this is a test",
    "max_tokens": 7,
    "temperature": 0
  }'
```

- 响应

```json
{
  "id": "cmpl-uqkvlQyYK7bGYrRHQ0eXlWi7",
  "object": "text_completion",
  "created": 1589478378,
  "model": "text-davinci-003",
  "choices": [
    {
      "text": "\n\nThis is indeed a test",
      "index": 0,
      "logprobs": null,
      "finish_reason": "length"
    }
  ],
  "usage": {
    "prompt_tokens": 5,
    "completion_tokens": 7,
    "total_tokens": 12
  }
}
```

##### 1.1.2. 入参详解

- **`model` （string，必填）**

要使用的模型的 ID。可以使用 [列表模型API](https://link.juejin.cn?target=https%3A%2F%2Fplatform.openai.com%2Fdocs%2Fapi-reference%2Fmodels%2Flist "https://platform.openai.com/docs/api-reference/models/list") (GET [api.openai.com/v1/models](https://link.juejin.cn?target=https%3A%2F%2Fapi.openai.com%2Fv1%2Fmodels "https://api.openai.com/v1/models")) 查看所有可用模型，或参阅 [模型概述](https://link.juejin.cn?target=https%3A%2F%2Fplatform.openai.com%2Fdocs%2Fmodels%2Foverview "https://platform.openai.com/docs/models/overview") 了解它们的描述。

- **`prompt` （string or array，选填，Defaults to <|endoftext|>）**

用于生成完成、编码为字符串、字符串数组、标记数组或标记数组数组的提示。

注意 |endoftext| 是模型在训练期间看到的文档分隔符，因此如果未指定提示，模型将生成，就像从新文档的开头一样。

- **`suffix` （string，选填，Defaults to null）**

完成插入文本后的后缀。

- **`max_tokens` （integer，选填，Defaults to 16）**

完成时要生成的最大 [token](https://link.juejin.cn?target=https%3A%2F%2Fplatform.openai.com%2Ftokenizer "https://platform.openai.com/tokenizer") 数。

提示 `max_tokens` 的 token 计数不能超过模型的上下文长度。大多数模型的上下文长度为 2048 个令牌（最新模型除外，它支持 4096）

- **`temperature` （number，选填，Defaults to 1）**

使用哪个采样温度，在 **0和2之间**。

较高的值，如0.8会使输出更随机，而较低的值，如0.2会使其更加集中和确定性。

我们通常建议修改这个（`temperature` ）为 `top_p` 但两者不能同时存在，二选一。

- **`top_p` （number，选填，Defaults to 1）**

一种替代温度采样的方法叫做核心采样，模型会考虑到具有 top_p 概率质量的标记结果。因此，0.1 表示只有占前 10% 概率质量的标记被考虑。

我们通常建议修改这个（`top_p` ）或者 `temperature`，但不要同时修改两者。

- **`n` （integer，选填，Defaults to 1）**

每个 `prompt` 生成的完成次数。

注意：由于此参数会生成许多完成，因此它会快速消耗您的令牌配额。小心使用，并确保对 `max_tokens` 和 `stop` 进行合理的设置。

- **`stream` （boolean，选填，Defaults to false）**

是否返回部分进度流。如果设置，令牌将作为数据服务器推送事件随着它们变得可用而发送，流通过 `data: [DONE]` 消息终止。

- **`logprobs` （integer，选填，Defaults to null）**

在 `logprobs` 返回的最有可能的标记列表中，包括所选标记和对应的对数概率。

例如，如果 `logprobs` 为 5，则 API 将返回一个由 5 个最有可能的标记组成的列表。API 总是会返回采样标记的对数概率，因此响应中可能会有多达 `logprobs+1` 个元素。

`logprobs` 的最大值为 5。如果您需要更多，请通过我们的 [帮助中心](https://link.juejin.cn?target=https%3A%2F%2Fhelp.openai.com%2Fen%2F "https://help.openai.com/en/") 联系我们并描述您的用例。

- **`echo` （boolean，选填，Defaults to false）**

除了完成之外，还回显提示

- **`stop` （string or array，选填，Defaults to null）**

最多生成4个序列，API将停止生成更多的标记。返回的文本不包含停止序列。

- **`presence_penalty` （number，选填，Defaults to 0）**

介于 **-2.0 和 2.0 之间**的数字。正值会根据它们是否出现在文本中迄今为止来惩罚新令牌，从而增加模型谈论新主题的可能性。

[请参阅有关频率和状态惩罚的更多信息](https://link.juejin.cn?target=https%3A%2F%2Fplatform.openai.com%2Fdocs%2Fapi-reference%2Fparameter-details "https://platform.openai.com/docs/api-reference/parameter-details")

- **`frequency_penalty` （number，选填，Defaults to 0）**

介于-2.0和2.0之间的数字。正值会根据文本中新令牌的现有频率对其进行惩罚，从而降低模型重复相同行的可能性。

[请参阅有关频率和存在惩罚的更多信息](https://link.juejin.cn?target=https%3A%2F%2Fplatform.openai.com%2Fdocs%2Fapi-reference%2Fparameter-details "https://platform.openai.com/docs/api-reference/parameter-details")

- **`best_of` （integer，选填，Defaults to 1）**

在生成服务器端生成 `best_of` 完成，并返回“最佳”（每个标记具有最高对数概率的那一个）。结果无法流式传输。

当与 `n` 一起使用时，`best_of` 控制候选完成的数量，`n` 指定要返回多少个 - `best_of` 必须大于 `n`。

注意：由于此参数生成许多完成，因此可能会快速消耗您的令牌配额。请小心使用并确保 `max_tokens` 和 `stop` 设置合理。

- **`logit_bias` （map，选填，Defaults to null）**

修改指定标记在完成中出现的可能性。

接受一个JSON对象，将标记（由GPT分词器中的标记ID指定）映射到从 -100 到 100 的相关偏差值。您可以使用此 [分词器工具](https://link.juejin.cn?target=https%3A%2F%2Fplatform.openai.com%2Ftokenizer%3Fview%3Dbpe "https://platform.openai.com/tokenizer?view=bpe")（适用于GPT-2和GPT-3）将文本转换为令牌ID。数学上，在采样之前，模型生成的 logits 会添加偏差。确切的效果因模型而异，但是介于-1和1之间的值应该会减少或增加选择的可能性；像 -100 或 100 这样的值应该会导致相关令牌被禁止或独占选择。

例如，您可以传递 `{"50256": -100}` 来防止生成

- **`user` （string，选填）**

一个唯一的标识符，代表您的终端用户，可以帮助OpenAI监测和检测滥用。[了解更多信息](https://link.juejin.cn?target=https%3A%2F%2Fplatform.openai.com%2Fdocs%2Fguides%2Fsafety-best-practices%2Fend-user-ids "https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids")。

### 1.2 Chat 对话

#### 1.2.1 接口说明

- `POST http://{{ip}}:{{port}}/v1/chat/completions`

- 请求

```bash
curl http://{{ip}}:{{port}}/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

- 响应

```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 167765288,
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "\n\nHello there, how may I assist you today?",
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}
```

#### 1.2.2 入参详解

- **`model` （string，必填）**
  
  要使用的模型ID。有关哪些模型适用于Chat API的详细信息，请查看 [模型端点兼容性表](https://link.juejin.cn?target=https%3A%2F%2Fplatform.openai.com%2Fdocs%2Fmodels%2Fmodel-endpoint-compatibility "https://platform.openai.com/docs/models/model-endpoint-compatibility")

- **`messages` （array，必填）**
  
  迄今为止描述对话的消息列表
  
  - **`role` （string，必填）**
    
    此消息的作者角色。`system` 、`user` 或 `assistant` 之一
  
  - **`content` （string，必填）**
    
    消息的内容
  
  - **`name` （string，选填）**
    
    此消息的作者的姓名。可以包含 a-z、A-Z、0-9 和下划线，最大长度为 64 个字符

- **`temperature` （number，选填，Defaults to 1）**
  
  使用哪个采样温度，在 **0和2之间**。
  
  较高的值，如0.8会使输出更随机，而较低的值，如0.2会使其更加集中和确定性。
  
  我们通常建议修改这个（`temperature` ）为 `top_p` 但两者不能同时存在，二选一。

- **`top_p` （number，选填，Defaults to 1）**
  
  一种替代温度采样的方法叫做核心采样，模型会考虑到具有 top_p 概率质量的标记结果。因此，0.1 表示只有占前 10% 概率质量的标记被考虑。
  
  我们通常建议修改这个（`top_p` ）或者 `temperature`，但不要同时修改两者。

- **`n` （integer，选填，Defaults to 1）**
  
  每个输入消息要生成多少聊天完成选项数

- **`stream` （boolean，选填，Defaults to false）**
  
  如果设置了，将发送部分消息增量，就像在 ChatGPT 中一样。令牌将作为数据 [服务器推送事件](https://link.juejin.cn?target=https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FAPI%2FServer-sent_events%2FUsing_server-sent_events%23event_stream_format "https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#event_stream_format") 随着它们变得可用而被发送，流通过 `data: [DONE]` 消息终止。请参阅OpenAI Cookbook 以获取 [示例代码](https://link.juejin.cn?target=https%3A%2F%2Fgithub.com%2Fopenai%2Fopenai-cookbook%2Fblob%2Fmain%2Fexamples%2FHow_to_stream_completions.ipynb "https://github.com/openai/openai-cookbook/blob/main/examples/How_to_stream_completions.ipynb")。

- **stop （string or array，选填，Defaults to null）**
  
  最多生成4个序列，API将停止生成更多的标记。

- **`max_tokens` （integer，选填，Defaults to inf）**
  
  在聊天完成中生成的最大 [tokens](https://link.juejin.cn?target=https%3A%2F%2Fplatform.openai.com%2Ftokenizer "https://platform.openai.com/tokenizer") 数。
  
  输入令牌和生成的令牌的总长度受模型上下文长度的限制。

- **`presence_penalty` （number，选填，Defaults to 0）**
  
  介于 **-2.0 和 2.0 之间**的数字。正值会根据它们是否出现在文本中迄今为止来惩罚新令牌，从而增加模型谈论新主题的可能性。
  
  [请参阅有关频率和状态惩罚的更多信息](https://link.juejin.cn?target=https%3A%2F%2Fplatform.openai.com%2Fdocs%2Fapi-reference%2Fparameter-details "https://platform.openai.com/docs/api-reference/parameter-details")

- **`frequency_penalty` （number，选填，Defaults to 0）**
  
  介于-2.0和2.0之间的数字。正值会根据文本中新令牌的现有频率对其进行惩罚，从而降低模型重复相同行的可能性。
  
  [请参阅有关频率和存在惩罚的更多信息](https://link.juejin.cn?target=https%3A%2F%2Fplatform.openai.com%2Fdocs%2Fapi-reference%2Fparameter-details "https://platform.openai.com/docs/api-reference/parameter-details")

- **`logit_bias` （map，选填，Defaults to null）**
  
  修改完成时指定标记出现的可能性。
  
  接受一个JSON对象，将标记（由分词器中的标记ID指定）映射到从 -100 到 100 的相关偏差值。在采样之前，模型生成的logits会加上这个偏差。确切的影响因模型而异，但是 -1 到 1 之间的值应该会减少或增加选择概率；像 -100 或 100 这样的值应该会导致相关标记被禁止或独占选择。

- **`user` （string，选填）**
  
  一个唯一的标识符，代表您的终端用户，可以帮助OpenAI监测和检测滥用。

### 1.3 Edit 修改

- `POST http://{{ip}}:{{port}}/v1/edits`

- 请求

```bash
curl http://{{ip}}:{{port}}/v1/edits \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "text-davinci-edit-001",
    "input": "What day of the wek is it?",
    "instruction": "Fix the spelling mistakes"
  }'
```

- 相应

```json
{
  "object": "edit",
  "created": 1589478378,
  "choices": [
    {
      "text": "What day of the week is it?",
      "index": 0,
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 32,
    "total_tokens": 57
  }
}
```

#### 1.3.2 入参详解

- **`model` （string，必填）**
  
  要使用的模型ID。您可以在此端点中使用 `text-davinci-edit-001` 或 `code-davinci-edit-001` 模型。

- **`input` （string，选填，Defaults to ''）**
  
  用作编辑起点的输入文本。

- **`instruction` （string，必填）**
  
  指导模型如何编辑提示的说明。

- **`n` （integer，选填，Defaults to 1）**
  
  输入和指令需要生成多少次编辑。

- **`temperature` （number，选填，Defaults to 1）**
  
  使用哪个采样温度，在 **0和2之间**。
  
  较高的值，如0.8会使输出更随机，而较低的值，如0.2会使其更加集中和确定性。
  
  我们通常建议修改这个（`temperature` ）为 `top_p` 但两者不能同时存在，二选一。

- **`top_p` （number，选填，Defaults to 1）**
  
  一种替代温度采样的方法叫做核心采样，模型会考虑到具有 top_p 概率质量的标记结果。因此，0.1 表示只有占前 10% 概率质量的标记被考虑。
  
  我们通常建议修改这个（`top_p` ）或者 `temperature`，但不要同时修改两者。

### 2. 错误处理

- 计算能力不足
  
  - 解决方案： `docker run ... --dtype half`

```bash
ValueError: Bfloat16 is only supported on GPUs with compute capability \
of at least 8.0. Your NVIDIA GeForce RTX 2080 Ti GPU has compute \
capability 7.5.
```

- 导入模型的显存不足
  
  - 解决方案： 减少 `max-model-len` 长度

```bash
torch.cuda.OutOfMemoryError: CUDA out of memory. Tried to allocate \
4.03 GiB. GPU 0 has a total capacty of 21.66 GiB of which 3.23            GiB is free. Process 37747 has 18.44 GiB memory in use. Of the allocated memory 17.24 GiB is allocated by PyTorch, and 890.53 MiB            is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting max_split_size_mb to avoid fragmen           tation.  See documentation for Memory Management and PYTORCH_CUDA_ALLOC_CONF
```

- cache的显存不足
  
  - 解决方案：`docker run ... -q awq --enforce-eager --gpu-memory-utilization=1`

```bash
ValueError: No available memory for the cache blocks. \
Try increasing `gpu_memory_utilization` when initializing the engine.
```

# 参考资料

- vLLM 官方文档

[Welcome to vLLM! &#8212; vLLM](https://docs.vllm.ai/en/latest/)

[Quickstart &#8212; vLLM](https://docs.vllm.ai/en/latest/getting_started/quickstart.html)

[Distributed Inference and Serving &#8212; vLLM](https://docs.vllm.ai/en/latest/serving/distributed_serving.html)

- OpenAI API 相关

[OpenAI-API 接口文档(中文版) - 掘金](https://juejin.cn/post/7225126264663605309)

- vLLM目前不支持 pp 并行

https://github.com/vllm-project/vllm/issues/387

- vLLM架构

https://zhuanlan.zhihu.com/p/645251151

https://github.com/zhanzy178/vllm/blob/main/framework.drawio
