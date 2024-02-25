# 源码分析

## 一、项目结构

### 1. 一级目录

```bash
.
├── api
│   ├── restful_api.py  # 定义了 OpenAI API 风格接口路由及对应 handler
│   ├── ...
├── client
│   ├── __init__.py     # 定义了 RESTfulClient (Client 类)
│   ├── handlers.py     # 没啥用
│   ├── oscar           # 定义了 ActorClient 0.8.0版本似乎并未使用
│   ├── restful         # 定义了 Client 类用于访问Restful API推理服务（流式）
│   └── ...
├── core        # 定义了各类 Actor
│   ├── cache_tracker.py
│   ├── chat_interface.py
│   ├── __init__.py
│   ├── metrics.py
│   ├── model.py
│   ├── resource.py
│   ├── status_guard.py
│   ├── supervisor.py
│   ├── tests
│   ├── utils.py
│   └── worker.py
├── deploy     # 命令行入口函数
│   ├── cmdline.py     # 启动 Server 的命令行参数解析相关
│   ├── docker
│   ├── __init__.py
│   ├── local.py       # 启动 Xinference Server 和 Supervisor 相关
│   ├── supervisor.py  # 创建 Actor Pool 并创建 SupervisorActor服务
│   ├── test
│   ├── utils.py
│   └── worker.py      # 创建 Actor Pool 并创建 Actor 进程提供WorkerActor服务
├── locale
│   ├── __init__.py
│   ├── utils.py
│   └── zh_CN.json
├── model
│   ├── core.py
│   ├── embedding      # embedding模型
│   ├── image
│   ├── __init__.py
│   ├── llm            # 很重要，定义了ggml、pytorch、vllm和各种模型的类
│   ├── multimodal     # 多模态模型
│   ├── rerank         # 不知道是啥
│   └── utils.py
├── conftest.py
├── constants.py
├── fields.py
├── __init__.py
├── isolation.py
├── types.py
├── utils.py
├── _version.py
└── web
    └── ui
```

Client 类

### 2. deploy路径

```bash
├── deploy
│   ├── cmdline.py
│   ├── docker
│   ├── __init__.py
│   ├── local.py
│   ├── supervisor.py
│   ├── test
│   ├── utils.py
│   └── worker.py
```

#### 2.1 `cmdline.py`

    

- `local` 函数是一切的入口
  
  - 调用 `start_local_cluster` 函数
  
  - 通过 `@click.command` 装饰，可通过命令行调用
  
  - `--log-level`  日志等级
  
  - `--host` Xinference server 的地址
  
  - `--port` Xinference server 的端口
  
  - `--metrics-exporter-host` Xinference metrics exporter server 的地址
  
  - `--metrics-exporter-port` Xinference metrics exporter server 的端口
  
  - `--auth-config`

- `start_local_cluster` 函数启动本地服务器
  
  - 调用 `deploy/local.py` 中的`main`函数

#### 2.2 `local.py`

- `main`  函数
  
  - 开启新进程创建supervisor守护进程 `
  
  - `main` _> `run_in_subprocess`-> `run` -> `_start_local_cluster`
    
    - 启动各类 Woker 进程
  
  - 从 `api` 引入 `restful_api.run()` 函数，创建`RESTfulAPI` 建立后端服务器 

- `_start_local_cluster` 函数
  
  - 调用 `deploy/utils.py` 中的 `create_worker_actor_pool`  创建 `Actor Pool`
  
  - 调用 `deploy/worker.py` 中的 `start_worker_components` 创建属于上述 `Actor Pool` 的 `Actor`
    
    - `Actor` 为 `StatelessActor` 该类定义于 `core/worker.py` 中

#### 2.3 `worker.py`

- 导入 `WorkerActor` 并在子进程中启动

#### 2.4 `supervisor.py`

- 导入 `SupervisorActor` 并在子进程中启动

### 3. core路径

#### 3.1 `worker.py`-`WorkerActor` 类

- `get_devices_count` 函数
  
  - 返回所属`Actor Pool`所在节点的GPU数量

- `get_model_count` 函数
  
  - 返回模型数量，通常一个模型对应一个 `Actor`

- `is_model_vllm_backend` 函数
  
  - 会调用 `core/model.py` `ModelActor` 类中的 `is_vllm_backend` 函数

- `allocate_devices` 函数
  
  - 检查当前可用GPU数，并分配剩余GPU

- `release_devices` 函数
  
  - 释放GPU

- `register_model` 函数
  
  - 注册 Custom 模型
  
  - 通过字典 `_custom_register_type_to_cls` 确定模型参数
    
    - 分为`LLM` 、 `embedding` 、 `rerank` 三类
  
  - 不同类型的注册函数不同，实际注册函数位于`model/llm/llm_family.py`下
    
    - 如`register_llm`会判断是否重名
    - 如果是是已存在模型 `persist=True`  则校验路径(URI)是否合法

- `unregister_model` 函数
  
  - 删除 Custom 模型

- `launch_speculative_model` 函数
  
  - 导入 Custom 模型权重至显存
  
  - 调用自身的 `_create_subpool` 函数
    
    - `main_pool` 是 `MainActorPoolType` 实例（xoscar类）
    
    - 创建sub Pool 调用 `MainActorPoolType.append_sub_pool`函数
  
  - 调用`create_speculative_llm_model_instance` 函数建立模型实例
    
    - 调用`model/llm/core.py`下的`match_llm_cls` 匹配以下模型
      
      ```python
      from .ggml.chatglm import ChatglmCppChatModel
      from .ggml.ctransformers import CtransformersModel
      from .ggml.llamacpp import LlamaCppChatModel, LlamaCppModel
      from .pytorch.baichuan import BaichuanPytorchChatModel
      from .pytorch.chatglm import ChatglmPytorchChatModel
      from .pytorch.core import PytorchChatModel, PytorchModel
      from .pytorch.falcon import FalconPytorchChatModel, FalconPytorchModel
      from .pytorch.internlm2 import Internlm2PytorchChatModel
      from .pytorch.llama_2 import LlamaPytorchChatModel, LlamaPytorchModel
      from .pytorch.vicuna import VicunaPytorchChatModel
      from .vllm.core import VLLMChatModel, VLLMModel 
      ```
  
  - 为该模型创建 `ModelActor`

- `launch_builtin_model` 函数
  
  - 导入内置模型的权重至显存
  - 与上述过程类似

#### 3.2 `model.py` -`ModelActor`类

- `_get_worker_ref` 函数
  
  - 如果当前 Worker 的 Acotr Ref 为空就创建一个引用，否则返回引用（单例）

- `is_vllm_backend` 函数
  
  - 是否是vLLM后端

- `load` 函数 
  
  - 导入模型

- `model_uid` 函数 
  
  - 返回模型的UID

- `generate` 函数
  
  - 执行 `generate` 操作进行文字补全

- `chat` 函数
  
  - 进行chat

- `create_embedding` 函数
  
  - 创建 embedding 模型

- `rerank` 函数
  
  - 不知道是做什么的？？

--- 

- `oom_check` 函数检查是否内存超限

#### 3.3 `supervisor.py` - `SupervisorActor` 类

- `get_builtin_prompts` 不知道干啥的

- `get_builtin_families` 返回支持的模型家族

- `get_devices_count` 显卡数量

- `get_status` 状态更新时间和Worker状态

- `list_model_registrations` 列出自定义模型

- `register_model` 注册自定义模型
  
  - 引入  `Worker Actor`
  
  - 获取 `self._worker_address_to_worker` 列表中的 `Worker Actor`
  
  - 调用 worker 的 `worker.register_model(model_type, model, persist)` 函数
  
  - **为什么每个worker都要执行一次入册函数呢？**

- `unregister_model` 删除自定义模型
  
  - 调用 `worker.unregister_model(model_name)` 方法

- `launch_model_by_version` 
  
  - 调用  `launch_builtin_model`

- `launch_speculative_llm`
  
  - 调用 `worker_ref.launch_speculative_model` 

- `launch_builtin_model` 
  
  - 调用 worker `launch_builtin_model` 函数

- `_check_dead_nodes` 函数 
  
  - 维护`self._worker_address_to_worker` 列表中的 `Worker Actor`
  
  - 当worker进程异常时，将该worker从上述列表中移除

- `list_models` 函数
  
  - 执行每个worker上 `list_models` 函数
  
  - **每个Worker上有多个不同模型？**

- `is_local_deployment` 函数是不是单机/单卡环境？
  
  - 当worker数量为1 && `self._worker_address_to_worker` 列表首元素为本地地址 时返回真

- `add_worker` 
  
  - 向 `self._worker_address_to_worker` 列表添加worker

- `remove_worker` 
  
  - 移除 worker

- `report_worker_status` 函数
  
  - 更新指定 worker 的状态至 ` self._worker_status[worker_address]` 列表

### 4. Model-LLM路径

#### 4.0 `__init__.py`

-     定义 `_install()` 函数

- 从 `ggml`、 `pytorch` 、 `vllm` 中导入各种模型类，并放入 `LLM_CLASSES` 列表中

- 从 `llm_family.json` 导入内置模型的参数，包括模型能力等，参数如下
  
  ```json
  {
  "version": 1,
  "context_length": 4096,
  "model_name": "baichuan",
  "model_lang": [ "en", "zh" ],
  "model_ability": [ "generate" ],
  "model_description": "....",
  "model_specs": [....]
  }
  
  "model_specs": [
      {
        "model_format": "ggmlv3",
        "model_size_in_billions": 7,
        "quantizations": [ "q2_K", "q3_K_L", "q3_K_M", "q3_K_S",...],
        "model_id": "TheBloke/baichuan-llama-7B-GGML",
        "model_file_name_template": "baichuan-llama-7b.ggmlv3.{quantization}.bin"
      },
      {
        "model_format": "pytorch",
        "model_size_in_billions": 7,
        "quantizations": [ "4-bit", "8-bit", none" ],
        "model_id": "baichuan-inc/Baichuan-7B",
        "model_revision": "c1a5c7d5b7f50ecc51bb0e08150a9f12e5656756"
      }
    ]
  ```

#### 4.1 `core.py` -`LLM`类和`LLMDescription`类

- `LLM`类是一个抽象类

- `handle_model_size` 函数
  
  - 解析模型规模，如34B等字符串

- `_is_darwin_and_apple_silicon` 函数、 `_is_linux` 函数
  
  - 判断平台类型

- `_has_cuda_device` 函数
  
  - 判断显卡数量

- `load` 函数 和 `match` 函数
  
  - 抽象函数，子类实现
  
  - 用于导入模型和匹配模型家族

### 4.2 `llm/vllm/core.py` - VLLMModel类

- 引入 vllm的 `AsyncLLMEngine`

- 实现 `LLM` 类中的虚函数

### 4.3 `llm/ggml/core.py` - LlamaCppModel类

- 引入 llamacpp的 `llama_cpp.Llama`

- 实现 `LLM` 类中的虚函数

### 4.4 `llm/pytorch/core.py` - PytorchModel类

- 引入 pytorch

- 实现 `LLM` 类中的虚函数
