# Xinference接口说明

### 0. 接口梳理

#### 0.1 接口对比

| Method | OpenAI                   | XInferencce              | 说明        |
| ------ | ------------------------ | ------------------------ | --------- |
| GET    | /v1/models               | /v1/models               | 列出模型      |
| GET    | /v1/models/gpt-3.5       | /v1/models/qwen          | 模型详情      |
| DELETE | /v1/models/gpt-3.5       | /v1/models/qwen          | 删除实例      |
| ANY    |                          | /v1/model_registrations  | 模型注册/删除   |
| ANY    | /v1/files                |                          | 文件操作      |
| POST   | /v1/chat/completions     | /v1/chat/completions     | 对话        |
| POST   | /v1/audio/transcriptions | /v1/audio/transcriptions | 语音转文字     |
| POST   | /v1/audio/speech         |                          | 文字转语音     |
| POST   | /v1/embeddings           | /v1/embeddings           | RAG/词向量映射 |
| POST   | /v1/images/generations   | /v1/images/generations   | 生成图片      |
| POST   | /v1/images/variations    | /v1/images/variations    | 图片修复      |
| POST   | /v1/images/edits         |                          | 图片编辑/扩展   |
| ANY    | /v1/fine_tuning          |                          | 微调        |

### 1. 模型列表`GET /v1/model_registrations/{{model_type}}?detailed=true`

##### 1.1 Query Params

- model_type 可以是 LLM 、rerank、 embedding、image

| 字段名      | 参数类型 | 参数例子 | 说明       |
| -------- | ---- | ---- | -------- |
| detailed | bool | true | 是否展示详细信息 |

##### 1.2 Response Body

| 字段名               | 参数类型            | 参数例子         | 说明                  |
| ----------------- | --------------- | ------------ | ------------------- |
| version           | int             | 1            | 模型版本信息              |
| context_length    | int             | 4096         | 上下文长度               |
| model_name        | str             | "baichuan"   | 模型名称                |
| model_lang        | List[str]       | ["en","zh"]  | 模型支持语言              |
| model_ability     | List[str]       | ["generate"] | 模型能力（generate、chat） |
| model_description | str             | "..."        | 模型描述信息              |
| model_family      | Union[str,None] | null         | 内置模型不需要设置，自定义模型需要指定 |
| model_specs       | struct          |              | 模型详细信息（从模型缓存中获取）    |

```json
[
    {
        "version": 1,
        "context_length": 4096,
        "model_name": "baichuan",
        "model_lang": [
            "en",
            "zh"
        ],
        "model_ability": [
            "generate"
        ],
        "model_description": "Baichuan is ...",
        "model_family": null,
        "model_specs": [
            {
                "model_format": "ggmlv3",
                "model_size_in_billions": 7,
                "quantizations": [ "q2_K", "q3_K_L", "q3_K_M", "q3_K_S",
                    "q4_0", "q4_1", "q4_K_M", "q4_K_S", "q5_0", "q5_1",
                    "q5_K_M", "q5_K_S", "q6_K", "q8_0"
                ],
                "model_id": "TheBloke/baichuan-llama-7B-GGML",
                "model_file_name_template": "baichuan-llama-7b.ggmlv3.{quantization}.bin",
                "model_hub": "huggingface",
                "model_uri": null,
                "model_revision": null,
                "cache_status": [
                    false, false, false, false, false, false, false, 
                    false, false, false, false, false, false, false
                ]
            },...
]
```

##### 1.3 说明

- 在 Xinference 的 Launch Models 页面查询所有内置或注册模型

```bash
# 1.
restful_api 
  -> list_model_registrations 
     -> SupervisorActor.list_model_registrations 
# 根据模型类型执行不同操作
if model_type == "LLM":
elif model_type == "embedding":
elif model_type == "image":
elif model_type == "audio":
elif model_type == "rerank":

# 2.
list_model_registrations 
  -> model.llm.llm_family.BUILTIN_LLM_FAMILIES: List["LLMFamilyV1"]
  -> model.llm.llm_family.get_user_defined_llm_families # 自定义模型家族

# 3.
LLMFamilyV1
# model.llm.llm_family.LLMFamilyV1 类与 Response Body 参数对应
class LLMFamilyV1(BaseModel):
    version: Literal[1]
    context_length: Optional[int] = DEFAULT_CONTEXT_LENGTH
    model_name: str
    model_lang: List[str]
    model_ability: List[Literal["embed", "generate", "chat", "tools", "vision"]]
    model_description: Optional[str]
    # reason for not required str here: legacy registration
    model_family: Optional[str]
    model_specs: List["LLMSpecV1"]
    prompt_style: Optional["PromptStyleV1"]

# 4.
BUILTIN_LLM_FAMILIES
# model.llm.__init__._install() 函数模块首次导入时自动添加模型家族列表 
# 配置文件位于 model/llm/llm_family.json 和 llm_family_modelscope.json
# 可通过添加配置来增加内置模型
json_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "llm_family.json"
)
for json_obj in json.load(codecs.open(json_path, "r", encoding="utf-8")):
    model_spec = LLMFamilyV1.parse_obj(json_obj)
    BUILTIN_LLM_FAMILIES.append(model_spec)
```

## 2. 模型详情`GET /v1/model_registrations/{{model_type}}/{{model_name}}`

##### 2.1 Query Params

- model_type 可以是 LLM 、rerank、 embedding、image
- model_name 可以是配置文件 `llm_family.json` 中对应类型模型的名称

##### 2.2 Response Body

| 字段名               | 参数类型            | 参数例子         | 说明                  |
| ----------------- | --------------- | ------------ | ------------------- |
| version           | int             | 1            | 模型版本信息              |
| context_length    | int             | 4096         | 上下文长度               |
| model_name        | str             | "baichuan"   | 模型名称                |
| model_lang        | List[str]       | ["en","zh"]  | 模型支持语言              |
| model_ability     | List[str]       | ["generate"] | 模型能力（generate、chat） |
| model_description | str             | "..."        | 模型描述信息              |
| model_family      | Union[str,None] | null         | 内置模型不需要设置，自定义模型需要指定 |
| model_specs       | struct          |              | 模型详细信息（从模型缓存中获取）    |

```json
{
    "version": 1,
    "context_length": 4096,
    "model_name": "baichuan",
    "model_lang": [
        "en",
        "zh"
    ],
    "model_ability": [
        "generate"
    ],
    "model_description": "Baichuan is a...",
    "model_family": null,
    "model_specs": [
        {
            "model_format": "ggmlv3",
            "model_size_in_billions": 7,
            "quantizations": [ "q2_K", "q3_K_L",...],
            "model_id": "TheBloke/baichuan-llama-7B-GGML",
            "model_file_name_template": "baichuan-llama-7b.ggmlv3.{quantization}.bin",
            "model_hub": "huggingface",
            "model_uri": null,
            "model_revision": null
        },
        {
            "model_format": "pytorch",
            "model_size_in_billions": 7,
            "quantizations": [
                "4-bit",
                "8-bit",
                "none"
            ],
            "model_id": "baichuan-inc/Baichuan-7B",
            "model_hub": "huggingface",
            "model_uri": null,
            "model_revision": "c1a5c7d5b7f50ecc51bb0e08150a9f12e5656756"
        },
        {
            "model_format": "pytorch",
            "model_size_in_billions": 13,
            "quantizations": [
                "4-bit",
                "8-bit",
                "none"
            ],
            "model_id": "baichuan-inc/Baichuan-13B-Base",
            "model_hub": "huggingface",
            "model_uri": null,
            "model_revision": "0ef0739c7bdd34df954003ef76d80f3dabca2ff9"
        }
    ],
    "prompt_style": null
}
```

##### 2.3 说明

- 在 Xinference 的 Launch Models 页面查询所有内置或注册模型，部分模型展示细节需要调用该接口

```bash
# 1.
restful_api 
  -> get_model_registrations
     -> SupervisorActor.get_model_registrations
# 根据模型类型执行不同操作，与前述相同

# 2.
get_model_registrations
  -> model.llm.llm_family.BUILTIN_LLM_FAMILIES: List["LLMFamilyV1"]
  -> model.llm.llm_family.get_user_defined_llm_families # 自定义模型家族

# 3.
LLMFamilyV1
# model.llm.llm_family.LLMFamilyV1 类与 Response Body 参数对应
class LLMFamilyV1(BaseModel):
    model_specs: List["LLMSpecV1"]
    ...

# 4.
LLMSpecV1
# model.llm.llm_family.LLMSpecV1 类的属性是一个 Union 根据后端不同参数不同
LLMSpecV1 = Annotated[
    Union[GgmlLLMSpecV1, PytorchLLMSpecV1],
    Field(discriminator="model_format"),
]

# 5. 
GgmlLLMSpecV1
# 使用 llama.cpp 后端时返回的 model_specs 参数
class GgmlLLMSpecV1(BaseModel):
    model_format: Literal["ggmlv3", "ggufv2"]       # 模型格式
    # Must in order that `str` first, then `int`    #
    model_size_in_billions: Union[str, int]         # 模型规模，如72
    quantizations: List[str]                        # 量化类型，如"4-bit"
    model_id: Optional[str]                         # 模型ID
    model_file_name_template: str
    model_hub: str = "huggingface"                  # 模型来源
    model_uri: Optional[str]
    model_revision: Optional[str]

# 6.
PytorchLLMSpecV1
# 使用 Pytorch 后端时返回的 model_specs 参数
class PytorchLLMSpecV1(BaseModel):
    model_format: Literal["pytorch", "gptq", "awq"]
    # Must in order that `str` first, then `int`
    model_size_in_billions: Union[str, int]
    quantizations: List[str]
    model_id: Optional[str]
    model_hub: str = "huggingface"
    model_uri: Optional[str]
    model_revision: Optional[str]
```

## 3. 提示词列表`GET /v1/models/prompts`

##### 3.1 Query Params

- 无

##### 3.2 Response Body

| 字段名               | 参数类型             | 参数例子           | 说明      |
| ----------------- | ---------------- | -------------- | ------- |
| style_name        | str              | "NO_COLON_TWO" | 提示词风格名称 |
| system_prompt     | str              | ""             | 系统提示词   |
| roles             | List[str]        | ["问","答"]      | 角色模板    |
| intra_message_sep | str              | "\n\n#"        | 多段文本分隔符 |
| inter_message_sep | int              | "</s>"         | 多段文本分隔符 |
| stop              | Union[str, None] | "</s>"         | 终止字符串   |
| stop_token_ids    | List[int]        | [2, 195]       | 终止字符词向量 |

```json
{
    "baichuan-chat": {
        "style_name": "NO_COLON_TWO",
        "system_prompt": "",
        "roles": [
            " <reserved_102> ",
            " <reserved_103> "
        ],
        "intra_message_sep": "",
        "inter_message_sep": "</s>",
        "stop": null,
        "stop_token_ids": [
            2,
            195
        ]
    },
    ...
}
```

##### 3.3 说明

```bash
# 1.
restful_api
  -> _get_builtin_prompts
     -> SupervisorActor.get_builtin_prompts

# 2.
get_builtin_prompts
  -> for k, v in BUILTIN_LLM_PROMPT_STYLE.items():

# 3.
BUILTIN_LLM_PROMPT_STYLE
# 内置的 LLM 风格模板
# model.llm.__init__._install() 函数模块首次导入时自动添加风格模板
# 配置文件位于 model/llm/llm_family.json 和 llm_family_modelscope.json
# 可通过添加配置来增加内置提示词风格模板
BUILTIN_LLM_PROMPT_STYLE: Dict[str, "PromptStyleV1"]
json_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "llm_family.json"
)
for json_obj in json.load(codecs.open(json_path, "r", encoding="utf-8")):
    # register prompt style
    if "chat" in model_spec.model_ability and isinstance(
        model_spec.prompt_style, PromptStyleV1
    ):
        # BUILTIN_LLM_PROMPT_STYLE 的 key 是模型名称
        # 因为同一个提示词风格名称(prompt style name) 会在多个模型中使用
        BUILTIN_LLM_PROMPT_STYLE[model_spec.model_name] = \
                                           model_spec.prompt_style

# 4.
PromptStyleV1
# model.llm.llm_family.PromptStyleV1 与返回体参数对应
class PromptStyleV1(BaseModel):
    style_name: str                        # 提示词风格名称
    system_prompt: str = ""                # 系统提示词
    roles: List[str]                       # 角色模板
    intra_message_sep: str = ""            # 多段文本分隔符
    inter_message_sep: str = ""            # 多段文本分隔符
    stop: Optional[List[str]]              # 终止字符串
    stop_token_ids: Optional[List[int]]    # 终止字符词向量
```

## 4.注册模型 `POST /v1/model_registrations/{{model_type}}`

##### 4.1 Body Params

| 字段名     | 参数类型 | 参数例子   | 说明                         |
| ------- | ---- | ------ | -------------------------- |
| model   | str  | "...." | json字符串风格的模型信息             |
| persist | bool | true   | 为true会保存上述model字符串并验证模型URL |

- `model` 字符串会存放在 `${HOME}/.xinference/model/llm` 以模型名称命名的路径下。（该路径由 `constant.XINFERENCE_MODEL_DIR` 控制）

```json
{
    "model": "{\"version\":1,\"context_length\":2048,\"model_name\":\"Yi-34B-Chat\",\"model_lang\":[\"en\",\"zh\"],\"model_ability\":[\"chat\"],\"model_description\":\"This is a custom model description.\",\"model_family\":\"Yi-chat\",\"model_specs\":[{\"model_format\":\"ggufv2\",\"model_size_in_billions\":34,\"quantizations\":[\"\"],\"model_id\":\"\",\"model_file_name_template\":\"yi-34b-chat.Q4_K_M.gguf\",\"model_uri\":\"/TRTDir/Models/Yi-34B-Chat-GGUF\"}],\"prompt_style\":{\"style_name\":\"CHATML\",\"system_prompt\":\"\",\"roles\":[\"<|im_start|>user\",\"<|im_start|>assistant\"],\"intra_message_sep\":\"<|im_end|>\",\"inter_message_sep\":\"\",\"stop\":[\"<|endoftext|>\",\"<|im_start|>\",\"<|im_end|>\",\"<|im_sep|>\"],\"stop_token_ids\":[2,6,7,8]}}",
    "persist": true
}
```

- `model` 字段中参数说明

| 字段名               | 参数类型            | 参数例子          | 说明                  |
| ----------------- | --------------- | ------------- | ------------------- |
| version           | int             | 1             | 模型版本信息              |
| context_length    | int             | 4096          | 上下文长度               |
| model_name        | str             | "Yi-34B-Chat" | 模型名称                |
| model_lang        | List[str]       | ["en","zh"]   | 模型支持语言              |
| model_ability     | List[str]       | ["generate"]  | 模型能力（generate、chat） |
| model_description | str             | "..."         | 模型描述信息              |
| model_family      | Union[str,None] | "Yi-chat"     | 内置模型不需要设置，自定义模型需要指定 |
| model_specs       | struct          |               | 模型详细信息（从模型缓存中获取）    |

##### 4.2 Response Body

- null

##### 4.3 说明

```bash
restful_api 
  -> register_model
     -> SupervisorActor.register_model
        if not self.is_local_deployment(): 
          # 多个节点需要通知其他节点worker注册
          -> WorkerActor.register_model
# 目前只能注册 llm 、 embedding 、 rerank 三类模型
# 如需注册其他类型，需要开发新代码

# 2.
SupervisorActor.register_model
# 根据模型类型参数，分别调用 llm 、 embedding 、 rerank 三类模型的注册函数
  -> model.llm.llm_family.register_llm
     model.embedding.custom.register_embedding
     model.rerank.custom.register_rerank
WorkerActor.register_model 
# 与 SupervisorActor.register_model 完全一致，仅在多个节点时通知其他节点 Worker
  -> model.llm.llm_family.register_llm
     model.embedding.custom.register_embedding
     model.rerank.custom.register_rerank

# 3.
register_llm
# model.llm.llm_family.register_llm 函数用于注册 LLM 类模型
  if not is_valid_model_name(llm_family.model_name):
    # 判断名称是否合法
  with UD_LLM_FAMILIES_LOCK:
    if llm_family.model_name == family.model_name:
    # 加锁判断名称是否重复
  if persist:
    # 如果 persist 为 true 则将 model 字段的模型配置保存到本地并校验模型 URL 
```

## 5. 删除模型`DELETE /v1/model_registrations/{{model_type}}/{{model_name}}`

##### 5.1 Query Params

- 无

##### 5.2 Response Body

- 无

##### 5.3 说明

```bash
# 1.
restful_api 
  -> unregister_model
     -> SupervisorActor.unregister_model
        if not self.is_local_deployment(): 
          # 多个节点需要通知其他节点worker注册
          -> WorkerActor.unregister_model
# 目前只能取消注册 llm 、 embedding 、 rerank 三类模型
# 如需取消注册其他类型，需要开发新代码

# 2.
SupervisorActor.unregister_model
# 根据模型类型参数，分别调用 llm 、 embedding 、 rerank 三类模型的取消注册函数
  -> model.llm.llm_family.unregister_llm
     model.embedding.custom.unregister_embedding
     model.rerank.custom.unregister_rerank
WorkerActor.unregister_model
# 与 SupervisorActor.register_model 完全一致，仅在多个节点时通知其他节点 Worker
  -> model.llm.llm_family.unregister_llm
     model.embedding.custom.unregister_embedding
     model.rerank.custom.unregister_rerank

# 3.
unregister_llm
# model.llm.llm_family.unregister_llm 函数用于取消注册 LLM 类模型

  with UD_LLM_FAMILIES_LOCK:
    # 加锁操作
    for i, f in enumerate(UD_LLM_FAMILIES: List["LLMFamilyV1"])
        # 从 UD_LLM_FAMILIES 列表中找出要删除模型的 llm_family
    UD_LLM_FAMILIES.remove(llm_family)
    # 删除对应 llm_family
    if os.path.exists(persist_path):
        os.remove(persist_path)
    # 删除注册时保存的 model json风格配置参数
    os.remove(cache_dir)
    # 删除 cache （条件删除）
```

## 6. 载入模型`POST /v1/models`

##### 6.1 Body Params

- 通用字段

| 字段名                    | 参数类型             | 参数例子          | 说明                                 |
| ---------------------- | ---------------- | ------------- | ---------------------------------- |
| model_format           | str              | "ggufv2"      | 常见有 pytorch、ggmlv3、ggufv2、gptq、awq |
| model_name             | str              | "Yi-34B-Chat" | 模型名称，与 register 时对应                |
| model_size_in_billions | int              | 34            | 模型规模，单位B                           |
| model_uid              | Union[str, None] | None          | 模型 UID                             |
| n_gpu                  | int              | 2             | 该模型分配GPU数量                         |

- LLM 可选字段

| 字段名          | 参数类型      | 参数例子 | 说明               |
| ------------ | --------- | ---- | ---------------- |
| n_gpu_layers | int       | 81   | 多少网络层装载至GPU中进行加速 |
| n_ctx        | int       | true | 上下文长度            |
| n_threads    | int       | true | 多少线程进行推理，不是越多越好  |
| tensor_split | List[int] | true | 多个GPU间如何分配模型占比   |

- 例子

```json
{
    "model_format": "ggufv2",
    "model_name": "Yi-34B-Chat",
    "model_size_in_billions": 72,
    "model_uid": null,
    "n_gpu": 2,
    "quantization": "",
    "n_gpu_layers": 38,
    "n_ctx": 1024,
    "n_threads": 3,
    "tensor_split": [0.8, 0.2]
}
```

##### 6.2 Response Body

- 无

##### 6.3 说明

```bash
restful_api 
  -> launch_model
     -> SupervisorActor.launch_builtin_model
       -> StatusGuardActor.set_instance_info # 有限状态机切换状态
       -> WorkerActor.launch_builtin_model   # 载入模型返回 worker_ref
       self._replica_model_uid_to_worker[_replica_model_uid] = worker_ref
       # 将模型的 worker 加入 SupervisorActor 管理的 worker 列表

# 2.
WorkerActor.launch_builtin_model
# core.worker.WorkerActor.launch_builtin_model 函数创建模型实例并返回引用
  subpool_address, devices = await self._create_subpool(...)
  # 为模型创建子资源池 (_create_subpool 为 xoscar 包内置二进制函数无法分析)
  model, model_description = await asyncio.to_thread(...)
    -> model.core.create_model_instance # 创建模型实例
      -> create_llm_model_instance
         create_embedding_model_instance
         create_image_model_instance
         create_rerank_model_instance
         create_audio_model_instance
  # 在当前 Worker 进程下创建新线程运行模型
  model_ref = await xo.create_actor(ModelActor, model...)
  # 创建模型引用并返回该引用（用于调用模型推理接口）


# 3.
create_llm_model_instance
# model.core.create_llm_model_instance 函数创建 LLM 模型实例
  llm_family, llm_spec, quantization = match_llm()
  # 获取匹配的模型家族
  llm_cls = match_llm_cls(llm_family, llm_spec, quantization)
  # 获取匹配的模型类，此处为
  model = llm_cls(model_uid, llm_family,..., kwargs)

# 4.
match_llm_cls
# model.llm.llm_family.match_llm_cls
for cls in LLM_CLASSES:List[Type[LLM]]:
    if cls.match(family, llm_spec, quantization):
        return cls

# 5.
LLM_CLASSES
# model.llm.llm_family.LLM_CLASSES 列表在 model.llm.__init__.py 中被添加
LLM_CLASSES.extend(
    [
        LlamaCppChatModel,
        LlamaCppModel,
    ]
)
LLM_CLASSES.extend(
    [
        ChatglmCppChatModel,
    ]
)
LLM_CLASSES.extend(
    [
        CtransformersModel,
    ]
)
LLM_CLASSES.extend([VLLMModel, VLLMChatModel])
LLM_CLASSES.extend(
    [
        BaichuanPytorchChatModel,
        VicunaPytorchChatModel,
        FalconPytorchChatModel,
        ChatglmPytorchChatModel,
        LlamaPytorchModel,
        LlamaPytorchChatModel,
        PytorchChatModel,
        FalconPytorchModel,
        Internlm2PytorchChatModel,
        QwenVLChatModel,
        YiVLChatModel,
        PytorchModel,
    ]
)
```

## 7. 模型续写`POST /v1/completions`

##### 7.1 Body Params

## 8. 模型聊天`POST /v1/chat/completions`

##### 8.1 Body Params

| 字段名      | 参数类型         | 参数例子          | 说明         |
| -------- | ------------ | ------------- | ---------- |
| model    | str          | "Yi-34B-Chat" | 模型名称与注册时对应 |
| messages | List[Object] | [...]         | 对话信息       |
| stream   | bool         | true          | 是否开启流式对话   |

```json
{
    "model": "Yi-34B-Chat",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Hello!"
        }
    ],
    "stream": true
}
```

##### 8.2 Response Body

```json
{
    "id": "chatcmpl-0d3cd210-8f08-49f8-bea3-5464e7122a2d",
    "object": "chat.completion",
    "created": 1708587766,
    "model": "/root/.xinference/cache/Yi-34B-Chat-ggufv2-34b/yi-34b-chat.Q4_K_M.gguf",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Hello there! How can I assist you today? If you have any questions or"
            },
            "finish_reason": "length"
        }
    ],
    "usage": {
        "prompt_tokens": 24,
        "completion_tokens": 16,
        "total_tokens": 40
    }
}
```

##### 8.3 说明

```bash
restful_api 
  -> create_chat_completion
  # 判断 body.max_tokens 是否指定，否则填写默认值
  # 判断 body.logit_bias 是否指定，否则报错
  # 判断 body.messages[-1]中的角色是否为 "user", "system", "tool" 中的一个
  if msg["role"] == "system":
      system_messages.append(msg)      # 添加 system_messages
  else:
      non_system_messages.append(msg)  # 添加 non_system_messages
  # 判断是否含有 tool message 
  if has_tool_message:
      prompt = SPECIAL_TOOL_PROMPT
      ...
  model = await (await self._get_supervisor_ref()).get_model(model_uid)
    -> SupervisorActor.get_model -> xo.ActorRefType["ModelActor"]
      -> WorkerActor.get_model -> xo.ActorRefType["ModelActor"]
           model_ref = self._model_uid_to_model.get(model_uid, None)
           # _model_uid_to_model 为启动模型时添加的模型列表
  # 获取模型引用
  data = await model.chat(prompt, chat_history, kwargs)
  # 这里的 model 是 ModelActor 的引用
    -> ModelActor.chat
    # 开启新线程调用 model.llm.ggml.llamacpp.LlamaCppChatModel.chat
      -> LlamaCppChatModel.chat


# 2.
LlamaCppChatModel.chat
# model.llm.ggml.llamacpp.LlamaCppChatModel.chat 函数调用 LLama 
  -> LlamaCppChatModel.generate
     self._llm = Llama(model_path=model_path,...) # 调用 Llama.cpp 库
     for _completion_chunk in self._llm(prompt=_prompt,...):
         yield _completion_chunk
```
