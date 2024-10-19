# EPAI镜像部署文档

本文档包含Dockerfile以及Python脚本，用于指导如何在Kubernetes中部署可通过健康检查的大模型服务。

> 注意：必须优先启动Web服务，再启动大模型。否则会被Kubernetes健康检查机制重启。

## 一、部署模型

### 1. Yuan2-M32

可部署无量化版本和GPTQ版本

> 注意： vLLM 仅支持部署无量化的 HF 模型。

#### 1.1 vLLM部署无量化版本 OpenAPI接口

##### 1.1.1 准备

- 拉取镜像

```bash
docker pull yuanmodel/vllm-v0.4.0:latest
```

- 拉取仓库代码

```bash
git clone https://github.com/IEIT-Yuan/Yuan2.0-M32.git
```

- 下载大模型权重

```bash
# 安装 git-lfs (可省略)
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
apt install git -lfs
# 下载镜像
git clone https://www.modelscope.cn/IEITYuan/Yuan2-M32-hf.git
cd Yuan2-M32-hf
git lfs pull
```

##### 1.1.2 镜像编译(Yuan2.0-M32路径下)

- 修改 `vllm/vllm/entrypoints/openai/api_server.py` 源码。请注意中文注释部分。
  
  - `vim vllm/vllm/entrypoints/openai/api_server.py`

```python
import asyncio
import importlib
import inspect
import os
import threading
import ray
from contextlib import asynccontextmanager
from http import HTTPStatus

import fastapi
import uvicorn
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response, StreamingResponse
from prometheus_client import make_asgi_app

import vllm
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine
from vllm.entrypoints.openai.cli_args import make_arg_parser
from vllm.entrypoints.openai.protocol import (ChatCompletionRequest,
                                              CompletionRequest, ErrorResponse)
from vllm.entrypoints.openai.serving_chat import OpenAIServingChat
from vllm.entrypoints.openai.serving_completion import OpenAIServingCompletion
from vllm.logger import init_logger
from vllm.usage.usage_lib import UsageContext

TIMEOUT_KEEP_ALIVE = 5  # seconds

openai_serving_chat: OpenAIServingChat = None
openai_serving_completion: OpenAIServingCompletion = None
logger = init_logger(__name__)

# 全局变量
engine = None
model_config = None
openai_serving_chat = None
openai_serving_completion = None
openai_serving_embedding = None
engine_args = None
_running_tasks = set()

# 创建一个全局事件
engine_ready = asyncio.Event()

@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):

    async def _force_log():
        # 等待engine初始化完成
        await engine_ready.wait()
        while True:
            await asyncio.sleep(10)
            await engine.do_log_stats()

    if not engine_args.disable_log_stats:
        asyncio.create_task(_force_log())

    yield


app = fastapi.FastAPI(lifespan=lifespan)


def parse_args():
    parser = make_arg_parser()
    return parser.parse_args()


# Add prometheus asgi middleware to route /metrics requests
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc):
    err = openai_serving_chat.create_error_response(message=str(exc))
    return JSONResponse(err.model_dump(), status_code=HTTPStatus.BAD_REQUEST)


@app.get("/health")
async def health() -> Response:
    """Health check."""
    await openai_serving_chat.engine.check_health()
    return Response(status_code=200)


@app.get("/v1/models")
async def show_available_models():
    models = await openai_serving_chat.show_available_models()
    return JSONResponse(content=models.model_dump())


@app.get("/version")
async def show_version():
    ver = {"version": vllm.__version__}
    return JSONResponse(content=ver)


@app.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest,
                                 raw_request: Request):
    generator = await openai_serving_chat.create_chat_completion(
        request, raw_request)
    if isinstance(generator, ErrorResponse):
        return JSONResponse(content=generator.model_dump(),
                            status_code=generator.code)
    if request.stream:
        return StreamingResponse(content=generator,
                                 media_type="text/event-stream")
    else:
        return JSONResponse(content=generator.model_dump())


@app.post("/v1/completions")
async def create_completion(request: CompletionRequest, raw_request: Request):
    generator = await openai_serving_completion.create_completion(
        request, raw_request)
    if isinstance(generator, ErrorResponse):
        return JSONResponse(content=generator.model_dump(),
                            status_code=generator.code)
    if request.stream:
        return StreamingResponse(content=generator,
                                 media_type="text/event-stream")
    else:
        return JSONResponse(content=generator.model_dump())

# 在线程中异步导入模型（耗时较久）
def load_model(args, engine_args):
    global engine, model_config, openai_serving_chat, openai_serving_completion, openai_serving_embedding

    engine = AsyncLLMEngine.from_engine_args(
        engine_args, usage_context=UsageContext.OPENAI_API_SERVER)

    async def get_model_config():
        return await engine.get_model_config()

    if args.served_model_name is not None:
        served_model = args.served_model_name
    else:
        served_model = args.model


    openai_serving_chat = OpenAIServingChat(engine, served_model,
                                            args.response_role,
                                            args.lora_modules,
                                            args.chat_template)
    openai_serving_completion = OpenAIServingCompletion(
        engine, served_model, args.lora_modules)

    # 初始化完成后，设置事件
    engine_ready.set()
    logger.info("Model loaded successfully")


if __name__ == "__main__":
    args = parse_args()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=args.allowed_origins,
        allow_credentials=args.allow_credentials,
        allow_methods=args.allowed_methods,
        allow_headers=args.allowed_headers,
    )

    if token := os.environ.get("VLLM_API_KEY") or args.api_key:

        @app.middleware("http")
        async def authentication(request: Request, call_next):
            root_path = "" if args.root_path is None else args.root_path
            if not request.url.path.startswith(f"{root_path}/v1"):
                return await call_next(request)
            if request.headers.get("Authorization") != "Bearer " + token:
                return JSONResponse(content={"error": "Unauthorized"},
                                    status_code=401)
            return await call_next(request)

    for middleware in args.middleware:
        module_path, object_name = middleware.rsplit(".", 1)
        imported = getattr(importlib.import_module(module_path), object_name)
        if inspect.isclass(imported):
            app.add_middleware(imported)
        elif inspect.iscoroutinefunction(imported):
            app.middleware("http")(imported)
        else:
            raise ValueError(f"Invalid middleware {middleware}. "
                             f"Must be a function or a class.")

    logger.info(f"vLLM API server version {vllm.__version__}")
    logger.info(f"args: {args}")

    engine_args = AsyncEngineArgs.from_cli_args(args)

    if engine_args.image_input_type is not None and \
        engine_args.image_input_type.upper() != "PIXEL_VALUES":
        raise ValueError(
            f"Invalid image_input_type: {engine_args.image_input_type}. "
            "Only --image-input-type 'pixel_values' is supported for serving "
            "vision language models with the vLLM API server.")

    # 在主线程中初始化Ray
    ray.init(num_gpus=engine_args.tensor_parallel_size)

    # 创建一个线程来加载模型
    load_thread = threading.Thread(target=load_model, args=(args, engine_args))
    load_thread.start()

    app.root_path = args.root_path
    uvicorn.run(app,
                host=args.host,
                port=args.port,
                log_level=args.uvicorn_log_level,
                timeout_keep_alive=TIMEOUT_KEEP_ALIVE,
                ssl_keyfile=args.ssl_keyfile,
                ssl_certfile=args.ssl_certfile,
                ssl_ca_certs=args.ssl_ca_certs,
                ssl_cert_reqs=args.ssl_cert_reqs)
```

- 编写启动脚本
  - `vim vllm/run.sh`

```bash
#! /bin/bash
cd $(dirname $0)

/usr/bin/python3 -m vllm.entrypoints.openai.api_server \
        --port ${PORT:-8080} \
        --model ${MODEL_PATH:-'/mnt/model'} \
        --trust-remote-code \
        --disable-custom-all-reduce \
        --tensor-parallel-size=${TP:-4} \
        --max-num-seqs=${MAX_NUM_SEQS:-1} \
        --gpu-memory-utilization=${GPU_MEMORY_UTILIZATION:-0.8}
```

- 编写 Dockerfile 文件
  
  - `vim Dockerfile`

```dockerfile
FROM yuanmodel/vllm-v0.4.0:latest

WORKDIR /mnt/inaisfs/user-fs/inf/llm/

ADD . /mnt/inaisfs/user-fs/inf/llm/Yuan2.0-M32

WORKDIR /mnt/inaisfs/user-fs/inf/llm/Yuan2.0-M32/vllm

ENV CUDA_HOME=/usr/local/cuda
ENV MAX_JOBS=64
ENV NVCC_THREADS=8

RUN python setup.py install

# 本段内容可挂载到容器手动执行，然后通过Dockerfile安装
RUN cp build/lib.linux-x86_64-3.10/vllm/*.so ./vllm

CMD ["/bin/sh", "run.sh"]
```

- 备用方案-手动编译

```bash
cd /mnt/inaisfs/user-fs/inf/llm #/Yuan2.0-M32
docker run --gpus '"device=4,5,6,7"' -it --rm -v `pwd`:`pwd` --name yuan_vllm yuanmodel/vllm-v0.4.0:latest bash
# 进入vLLM项目
cd /mnt/inaisfs/user-fs/inf/llm/Yuan2.0-M32/vllm
# 安装依赖
CUDA_HOME=/usr/local/cuda MAX_JOBS=64 NVCC_THREADS=8 python3 setup.py install
# 拷贝.so文件
cp build/lib.linux-x86_64-3.10/vllm/*.so vllm/
```

##### 1.2.3 EPAI镜像部署

- 通过 NFS 或 HostPath 存储类创建 PVC

NFS存储类创建时可指定子路径

external-default-sc 默认路径位于 `/mnt/inaisfs/loki/userrequest`

在宿主机找到对应的 PVC 并将模型移动到PVC中，如

```bash
cp -r ns_moe_case48_all-sft-20240708-8 /mnt/inaisfs/loki/userrequest/infer-yuanm32-model-pvc-de8d7865-86a5-42e3-8135-3ded5e7e4757/
```

- 部署镜像服务

```bash
# 业务:        yuan2m32
# CPU:        32
# 内存:        512 (PS: 64G = OOM)
# 加速卡:      A800 80G * 4
# PVC挂载路径: /mnt/model
# 端口:        http 8080
# 环境变量:
defualt_setting=[{"arg_name":"content_length","arg_dtype":"number", "arg_precision":0, "arg_value":2048,"arg_max":2048,"arg_min":2048,"arg_description":{"en":"","zh":""}}]
endpoint=/v1
model_name=yuan2m32-infer
protocol=OpenAI
MODEL_PATH=/mnt/model/ns_moe_case48_all-sft-20240708-8
PORT=8080
TP=4  # 这里等于GPU卡数量 80G 显存 >= 2 张
```

- 文件输出
  
  - 镜像： yuan-vllm-latest-build.tar.gz

##### 参考资料

- Github 部署指南

[Yuan2.0-M32/vllm/README_Yuan_vllm.md at main · IEIT-Yuan/Yuan2.0-M32 · GitHub](https://github.com/IEIT-Yuan/Yuan2.0-M32/blob/main/vllm/README_Yuan_vllm.md)

### 2. c4ai-command-r-v01

#### 2.1 Transfomers部署int4量化版本 EPAI 接口

##### 2.1.1 准备

- 镜像： `yuanmodel_c4ai:V1`

- 代码： `yuanchatenterprise`

##### 2.1.2 镜像编译

- Python服务如下（未修改）

```python
import os
import sys
import torch
import json
from threading import Thread
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import TextIteratorStreamer, GenerationConfig
from typing import Optional
from pydantic import BaseModel

from logging import getLogger

log = getLogger(__name__)

model = any
tokenizer = any


class ChatMessageHTTPInfo(BaseModel):
    message: str
    session_id: Optional[str] = None
    knowledge_id: Optional[str] = None
    dialogs_history: Optional[list] = None   # 格式如[{"question"："xxx", "answer":"yyy"}, {"question"："hhh", "answer":"zzz"}]，用户最新问题不要加到list中
    setting: Optional[dict] = None
    content_setting: Optional[dict] = None


def load_model(device='', model_path='')->bool:
    """
    模型加载，
    Args:
        device: 模型运行要使用的设备CPU/GPU，默认为空，根据CUDA自行判断
        model_path:模型文件保存路径，精确到gguf文件
    Returns:
        加载后模型
    """
    global model
    global tokenizer
    # 判断模型文件是否存在
    if not os.path.exists(model_path):
        raise ValueError('请输入正确的模型路径')

    if device == '':
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # 设备

    tokenizer = AutoTokenizer.from_pretrained(model_path)

    if device == torch.device('cpu') or device == 'cpu':
        device_map = "cpu"
    else:
        device_map = "auto"

    model = AutoModelForCausalLM.from_pretrained(model_path, device_map=device_map).eval()
    model.generation_config.max_new_tokens = 2048  # For chat.

    return True


def call(reqeust:ChatMessageHTTPInfo):
    """
    模型生成答案，流式输出
    Args:
        reqeust: 包含用户问题、历史对话
        setting: 参数字典，包括 stream: True表示采用流式，否则非流式
    Returns:
        模型输出（流式、非流式）
    """
    global model
    global tokenizer
    print('-----------------------------------------------------')
    print('\nyuan2_hf input reqeust paras:{0}\n'.format(reqeust))
    setting = reqeust.setting
    content_setting = reqeust.content_setting
    input_text = reqeust.message.strip()
    his_dialogs = reqeust.dialogs_history[:setting.get("multi_turn", 0)]

    plugin_prompt = content_setting.get("input_prompt", "")
    if plugin_prompt == "":   #若没有调用插件，用用户输入
        plugin_prompt = input_text
    print('\nmodel input prompt:{0}'.format(plugin_prompt))

    messages = [{"role": "user", "content": "请使用中文进行对话"},
                {"role": "chatbot", "content": "好的，我可以尝试用中文与您交流。请问有什么可以帮助您吗"}]
    for QA in his_dialogs:
        messages.append({'role': 'user', 'content': QA["question"]})
        messages.append({'role': 'chatbot', 'content': QA["answer"]})
    messages.append({"role": "user", "content": plugin_prompt})
    print('\ninput conversation:{0}'.format(messages))

    input_ids = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt                                                           ").to(model.device)
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, timeout=60.0, skip_special_tokens=True)
    generation_config = GenerationConfig(
        temperature=setting.get("temperature", 0.3),
        top_p=setting.get("top_p", 0.8),
        top_k=setting.get("top_k", 3),
        num_beams=1,
    )
    generation_kwargs = dict(input_ids=input_ids,
                             streamer=streamer,
                             max_new_tokens=setting.get("response_length", 512),
                             do_sample=setting.get("do_sample", True),
                             generation_config=generation_config,
                             return_dict_in_generate=True,)

    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()
    generated_text = ""
    # position = 0
    # start = False
    # start_text = "<|START_OF_TURN_TOKEN|><|USER_TOKEN|>" + messages[-1]['content'] + "<|END_OF_TURN_TOKEN|><|START_                                                           OF_TURN_TOKEN|><|CHATBOT_TOKEN|>"
    try:
        for new_text in streamer:
            print(new_text, end='', flush=True)
            generated_text += new_text
            # yield generated_text
            content_setting["output_answer"] = generated_text
            yield json.dumps(content_setting)
    except Exception as e:
        print(e)
    finally:
        content_setting["is_end_streamout"] = True
        yield json.dumps(content_setting)


#from openai_utils import ChatCompletionRequest
#from openai_utils import ChatCompletionResponse, ChatCompletionUsage, ChatCompletionResponseStreamChoice, DeltaMessag                                                           e, ChatCompletionResponseChoice, ChatMessage
from typing import Union, List, Optional, Literal, Dict
from pydantic import BaseModel, Field
import time

# 请求类型
class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system", "function"]    # role 字符串类型，必填项。该消息作者的角色。可选值为 system、user 或 assistant。
    content: Optional[str]                                      # content 字符串类型，必填项。消息的内容。
    function_call: Optional[Dict] = None

class ChatCompletionRequest(BaseModel):
    model: str                              # model 字符串类型，必填项。要使用的模型的 ID。
    messages: List[ChatMessage]             # messages 数组类型，必填项。包含对话历史描述的消息列表。
    functions: Optional[List[Dict]] = None  #
    temperature: Optional[float] = None     # temperature 数字类型 Optional 默认是 ** 1 ** 要使用的采样温度(temperature)，介于0和2之间。高值如0.8会使输出更加随机，而低值如0.2会使其更加集中和确定性。
    top_p: Optional[float] = None           # top_p 为数字类型，可选。默认为 1。
    top_k: Optional[float] = None           ####### 待定
    max_tokens: Optional[int] = None        # max_tokens 为整数，可选。默认为 16, 提示文本加上 max_tokens 的 token 数量不能超过模型的上下文长度。大多数模型的上下文长度为 2048 个 token（除最新的模型支持 4096 个 token）。
    stream: Optional[bool] = False
    # logprobs 整数类型，可选。 默认是 null。 logprobs 的最大值为 5。
    # frequency_penalty 数字类型，可选。 默认是 0介于-2.0和2.0之间的数字。正值基于新标记在文本中的现有频率对其进行惩罚，降低模型重复相同行的可能性。
    # n 为整数类型，可选。默认为 1。每个提示生成的完整次数。 代表希望 AI 给我们生成几条内容提供选择。如果在一些辅助写作的场景里，可以设置成 3 或者更多，供用户在多个结果里面自己选择自己想要的。
    stop: Optional[List[str]] = None        # stop 字符串或数组类型，可选。默认为 null。API 最多将生成 4 个序列，这些序列将停止生成更多标记。

    plugins: Optional[List] = None

# 返回类型
# 非流式返回
class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Literal["stop", "length", "function_call"]

# 流式返回
class DeltaMessage(BaseModel):
    role: Optional[Literal["user", "assistant", "system"]] = None
    # system 初始时，我们让API作为AI助手进行响应，这有助于它以尽可能接近真实的方式响应。例如：告诉API作为一名从事生物学研究的女研究员回答，您将获得类似于具有该背景的人的智能和周到的回答。
    content: Optional[str] = None

    # function_call=None    # openai 支持
    # tool_calls=None       # openai 支持

class ChatCompletionResponseStreamChoice(BaseModel):
    index: int
    delta: DeltaMessage
    # stop: API返回完整的模型输出。
    # length: 由于max_tokens参数(opens in a new tab)或标记限制而导致的不完整模型输出
    # content_filter: 由于我们的内容过滤器中的标志而省略的内容
    # null: API响应仍在进行中或不完整
    finish_reason: Optional[Literal["stop", "length"]] = None
    logprobs: Optional[int] = None        # openai 支持 # 若要获得类别日志概率，可以在使用模型时指定logprobs=5（对于5个类别）。


class ChatCompletionUsage(BaseModel):
    prompt_tokens: Optional[int]
    completion_tokens: Optional[int]
    total_tokens: Optional[int]

class ChatCompletionResponse(BaseModel):
    model: str
    object: Literal["chat.completion", "chat.completion.chunk"]
    choices: List[
        Union[ChatCompletionResponseChoice, ChatCompletionResponseStreamChoice]
    ]
    # usage': {'prompt_tokens': 56, 'completion_tokens': 31, 'total_tokens': 87},
    usage: Optional[ChatCompletionUsage] = None
    created: Optional[int] = Field(default_factory=lambda: int(time.time()))


def chat(request, langue: str = "cn"):
    print("################################################ chat")
    global model
    global tokenizer
    log.info('\nget input setting paras')

    System_Message = "你是一个很有用的智能助手" if langue=="cn" else "You are a helpful assistant."
    messages = [{"role": "user", "content": "请使用中文进行对话"},
                {"role": "chatbot", "content": "好的，我可以尝试用中文与您交流。请问有什么可以帮助您吗"}]
    for chat_message in request.messages:
        print("commandr chat message::", chat_message.role, chat_message.content)
        if chat_message.role == "system":
            temp_prompt = f"{chat_message.content}。{C}" if langue=="cn" else f"{chat_message.content}.{C}"
            messages.append({"role":"chatbot", "content":temp_prompt})
        elif chat_message.role == "user":
            temp_prompt = f"{chat_message.content}？{C}" if langue=="cn" else f"{chat_message.content}?{C}"
            messages.append({"role":"user", "content":temp_prompt})
        elif chat_message.role == "assistant":
            temp_prompt = f"{chat_message.content}。{C}" if langue=="cn" else f"{chat_message.content}.{C}"
            messages.append({"role":"chatbot", "content":temp_prompt})
        elif chat_message.role == "function":
            pass

    top_k           = 3 if request.top_k is None else request.top_k
    temperature     = 0.3 if request.temperature is None else request.temperature
    top_p           = 0.8 if request.top_p is None else request.top_p
    max_tokens      = 512 if request.max_tokens is None else request.max_tokens
    # openai 没有这个参数
    # repeat_penalty  = 2 if request.repeat_penalty is None else request.repeat_penalty
    stop            = ["Q:", "\n"] if request.stop is None else request.stop
    # stream 默认值为 False
    # stream          = True if request.stream is None else request.stream
    # print("qwen chat::", top_k, temperature, top_p, max_tokens)
    # openai 没有这个参数
    # do_sample

    input_ids = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt                                                           ").to(model.device)
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, timeout=60.0, skip_special_tokens=True)
    generation_config = GenerationConfig(
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        num_beams=1,
    )
    generation_kwargs = dict(input_ids=input_ids,
                             streamer=streamer,
                             max_new_tokens=max_tokens,
                             do_sample=True,
                             generation_config=generation_config,
                             return_dict_in_generate=True,)

    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()
    response = ""
    # position = 0
    # start = False
    # start_text = "<|START_OF_TURN_TOKEN|><|USER_TOKEN|>" + messages[-1]['content'] + "<|END_OF_TURN_TOKEN|><|START_                                                           OF_TURN_TOKEN|><|CHATBOT_TOKEN|>"
    try:
        for new_text in streamer:
            print(new_text, end='', flush=True)
            response += new_text
            # # yield response
            # content_setting["output_answer"] = response
            # yield json.dumps(content_setting)

            # iid             = output["id"]            # 无返回 cmpl-8c4e9159-8490-45a5-846a-1644e3ff0f36
            imodel          = request.model             # 无返回  默认 "chatglm3_hf"
            iobject         = "chat.completion.chunk"   # 无返回
            icreated        = int(time.time())          # 无该参数  默认为 当前时间戳
            iindex          = 0                         # 无该参数  默认为 0
            ifinish_reason  = None                      # 无该参数  默认为 None
            ilogprobs       = None                      # 无该参数  默认为 None
            icontent        = response
            print("yuan2 chat response::", response)

            delta_message = DeltaMessage(role="assistant", content=icontent)
            choice_data = ChatCompletionResponseStreamChoice(index=iindex, delta=delta_message, finish_reason=ifinish                                                           _reason, logprobs=ilogprobs)
            chunk = ChatCompletionResponse(model=imodel, object=iobject, choices=[choice_data], created=icreated)
            yield chunk
    except Exception as e:
        print(e)
    finally:
        # content_setting["is_end_streamout"] = True
        # yield json.dumps(content_setting)
        pass


import uvicorn
import argparse
from fastapi import FastAPI, Request
from sse_starlette import EventSourceResponse
from fastapi.responses import StreamingResponse
app = FastAPI()


@app.post("/c4ai/hf/")
async def create_item(request: Request, item: ChatMessageHTTPInfo):
    # return EventSourceResponse(call(item))
    async def gene(request, item):
        for dd in call(item):
            if not await request.is_disconnected() == True:
                yield dd
    return StreamingResponse(gene(request, item))

@app.post("/c4ai/hf/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    print("chat_completions, request.stream:", request.stream)

    # return EventSourceResponse(chat(request))
    async def gene(request):
        for dd in chat(request):
            yield "{}".format(dd.model_dump_json(exclude_unset=True))
    return EventSourceResponse(gene(request))

if __name__ == '__main__':
    # from pkg.plugins.as_constants import *
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8900)
    parser.add_argument('--model_path', type=str, default="")
    args = parser.parse_args()
    load_model(device='', model_path=args.model_path)
    uvicorn.run(app, host="0.0.0.0", port=args.port)
```

- 编写启动脚本
  
  - `vim yuanchatenterprise/pkg/plugins/chat_model_plugin_http/start_c4ai_commandr_hf.sh`

```bash
DATETIME=`date +'%y-%m-%d_%H-%M-%S'`

MODEL_PATH=${MODEL_PATH:-"/mnt/model/c4ai_int4"}
PORT=${PORT:-8080}

python c4ai_commandr_hf.py \
  --port $PORT \
  --model_path $MODEL_PATH 2>&1 | tee logs/c4ai_hf_${DATETIME}.log
```

- Dockerfile

```dockerfile
FROM yuanmodel_c4ai:V1

WORKDIR /workspace

ADD ./yuanchatenterprise /workspace/yuanchatenterprise

WORKDIR /workspace/yuanchatenterprise/pkg/plugins/chat_model_plugin_http

CMD ["/usr/bin/bash", "start_c4ai_commandr_hf.sh"]
```

##### 2.1.3 EPAI镜像部署

- 通过 NFS 或 HostPath 存储类创建 PVC

NFS存储类创建时可指定子路径

external-default-sc 默认路径位于 `/mnt/inaisfs/loki/userrequest`

在宿主机找到对应的 PVC 并将模型移动到PVC中，如

```bash
cp -r c4ai_int4 /mnt/inaisfs/loki/userrequest/infer-command-model-pvc-41e17e55-84c5-4d83-bdef-ce3bfa7151fb/
```

- 部署镜像服务

```bash
# 业务:        yuan2m32
# CPU:        16
# 内存:        64G
# 加速卡:      A800 80G * 1
# PVC挂载路径: /mnt/model
# 端口:        http 8080
# 环境变量:
defualt_setting=[{"arg_name":"content_length","arg_dtype":"number", "arg_precision":0, "arg_value":2048,"arg_max":2048,"arg_min":2048,"arg_description":{"en":"","zh":""}}]
endpoint=/c4ai/hf/v1
model_name=commandr-infer
protocol=EPAI
MODEL_PATH=/mnt/model/c4ai_int4
PORT=8080
```

- 文件输出
  
  - 镜像： yuanmodel_c4ai_infer.tar.gz
