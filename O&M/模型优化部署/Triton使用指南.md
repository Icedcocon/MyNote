# Triton 使用指南

## 一、快速开始

### 1.镜像编译

1. **克隆仓库**

```bash
git clone  https://github.com/triton-inference-server/tensorrtllm_backend.git -b rel
```

2. **递归克隆依赖仓库**

```bash
cd tensorrtllm_backend
git lfs install
git submodule update --init --recursive
```

3. **镜像编译**

```bash
DOCKER_BUILDKIT=1 docker build -t triton_trt_llm:rel -f dockerfile/Dockerfile.trt_llm_backend .
```

### 2. 模型配置说明

- **模型存储库目录树如下**

```bash
triton_model_repo
`-- chatglm2_6b
    |-- 1
    |   |-- chatglm2_6b_float16_tp1_rank0.engine
    |   `-- config.json
    `-- config.pbtxt
```

- **模型配置 `config.pbtxt` 内容如下**
  - 其中 input 和 output 参数的名称可通过 `TensorRT-LLM/cpp/include/tensorrt_llm/batch_manager/inferenceRequest.h` 头文件查看。（大部分参数仅为可选项，最小配置见下文）
  - input 和 output 的数据类型
  - inpu

```json
name: "chatglm2_6b"
backend: "tensorrtllm"
max_batch_size: 8

input [
  {
    name: "input_ids"
    data_type: TYPE_INT32
    dims: [ -1 ]
  },
  {
    name: "request_output_len"
    data_type: TYPE_INT32
    dims: 1
  }
]
output [
  {
    name: "output_ids"
    data_type: TYPE_FP32
    dims: [ 65024 ]
  }
]
parameters: {
  key: "gpt_model_type"
  value: {
    string_value: "V1"
  }
}
parameters: {
  key: "gpt_model_path"
  value: {
    string_value: "/TRTDir/triton_model_repo/chatglm2_6b/1"
  }
}
parameters: {
  key: "max_tokens_in_paged_kv_cache"
  value: {
    string_value: "100"
  }
}
parameters: {
  key: "batch_scheduler_policy"
  value: {
    string_value: "guaranteed_no_evict"
  }
}
```

### 3. Triton 服务测试

- **验证 Triton Inference Server 是否正常运行**

```bash
curl -v localhost:8000/v2/health/ready
```

- **可以使用脚本启动 Triton Inference Server**

```bash
python3 scripts/launch_triton_server.py \
        --world_size=1 \
        --model_repo=/TRTDir/triton_model_repo
```

- 上述代码实际开启进行调用以下命令
  
  - 经验证在 tensorrt-llm模型中 `--strict-model-config`  不能被设置为False，及Triton不能完成模型配置 `config.pbtxt` 自动推导，原因是需要 `config.pbtxt` 在中指定 `gpt_model_path`

```bash
mpirun --allow-run-as-root -n 1 \
        /opt/tritonserver/bin/tritonserver \
        --strict-model-config=True\
        --grpc-port=8001 \
        --http-port=8000 \
        --metrics-port=8002 \
        --model-repository=/TRTDir/triton_model_repo
```

- 调用config接口可以查看该模型的模型配置（与`config.pbtxt` 类似）

```bash
/v2/models/${MODEL_NAME}[/versions/${MODEL_VERSION}]/config
```

### 4. GRPC-Client调用脚本如下

- 需要tensorrt-llm环境

- PS：存在冗余代码

```python
import os
import sys
import queue
import numpy as np

from functools import partial

import tritonclient.grpc as grpcclient
from transformers import AutoTokenizer
from tritonclient.utils import InferenceServerException, np_to_triton_dtype


def prepare_tensor(name, input):
    t = grpcclient.InferInput(name, input.shape,
                              np_to_triton_dtype(input.dtype))
    t.set_data_from_numpy(input)
    return t

def prepare_inputs(input_ids_data, input_lengths_data, request_output_len_data,
                   beam_width_data, temperature_data, repetition_penalty_data,
                   presence_penalty_data, streaming_data, end_id, pad_id,
                   prompt_embedding_table_data, prompt_vocab_size_data,
                   return_log_probs_data, top_k_data, top_p_data,
                   draft_ids_data):
    inputs = [
        prepare_tensor("input_ids", input_ids_data),
        prepare_tensor("request_output_len", request_output_len_data),
    ]
    return inputs

class UserData:

    def __init__(self):
        self._completed_requests = queue.Queue()

def callback(user_data, result, error):
    print(result)
    if error:
        user_data._completed_requests.put(error)
    else:
        user_data._completed_requests.put(result)

if __name__ == "__main__":
    tokenizer_dir = "/TRTDir/Models/chatglm2-6b"
    text = "请介绍一下浪潮信息？"
    url = "localhost:8001"

    request_output_len = 100
    beam_width = 1
    top_k = 1
    top_p = 0
    temperature = 1.0
    return_log_probs = False

    streaming = False

    print('1.tokenizer')
    if not os.path.exists(tokenizer_dir):
        print("tokenizer 路径中不存在 tokenizer 文件: ",tokenizer_dir)
        exit()
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir,
                                                legacy=False,
                                                padding_side='left',
                                                truncation_side='left',
                                                trust_remote_code=True,
                                                use_fast=True)                           
    pad_id = tokenizer.encode(tokenizer.pad_token, add_special_tokens=False)[0]
    end_id = tokenizer.encode(tokenizer.eos_token, add_special_tokens=False)[0]

    input_ids = [tokenizer.encode(text)]
    print(f"Input Message:{text}\nInput IDs:{input_ids}")

    end_id_data = np.array([[end_id]], dtype=np.int32)
    pad_id_data = np.array([[pad_id]], dtype=np.int32)

    prompt_embedding_table_data = None
    prompt_vocab_size_data = None

    input_ids_data = np.array(input_ids, dtype=np.int32)
    input_lengths = [[len(ii)] for ii in input_ids]
    input_lengths_data = np.array(input_lengths, dtype=np.int32)
    request_output_len = [[request_output_len]]
    request_output_len_data = np.array(request_output_len, dtype=np.int32)
    beam_width = [[beam_width]]
    beam_width_data = np.array(beam_width, dtype=np.int32)
    max_output_len = [[65024]]
    max_output_len_data = np.array(max_output_len, dtype=np.int32)
    top_k = [[top_k]]
    top_k_data = np.array(top_k, dtype=np.int32)
    top_p = [[top_p]]
    top_p_data = np.array(top_p, dtype=np.float32)
    temperature = [[temperature]]
    temperature_data = np.array(temperature, dtype=np.float32)
    return_log_probs = [[return_log_probs]]
    return_log_probs_data = np.array(return_log_probs, dtype=bool)

    repetition_penalty_data = None
    presence_penalty_data = None

    streaming = [[streaming]]
    streaming_data = np.array(streaming, dtype=bool)

    draft_ids_data = None

    inputs = prepare_inputs(input_ids_data, input_lengths_data,
                            request_output_len_data, beam_width_data,
                            temperature_data, repetition_penalty_data,
                            presence_penalty_data, streaming_data, end_id_data,
                            pad_id_data, prompt_embedding_table_data,
                            prompt_vocab_size_data, return_log_probs_data,
                            top_k_data, top_p_data, draft_ids_data)

    outputs = None
    stop_inputs = None
    request_id = ""

    expected_output_ids = input_ids[0] + [21221, 290, 257, 4255, 379, 262, 1957, 7072,
                            11, 4689, 347, 2852, 2564, 494, 13, 679]

    actual_output_ids = []
    sequence_lengths = []
    cum_log_probs = None
    output_log_probs = None

    user_data = UserData()
    with grpcclient.InferenceServerClient(
            url=url,
            verbose=False,
            ssl=False,
            root_certificates=None,
            private_key=None,
            certificate_chain=None,
    ) as triton_client:
        try:
            # Send request
            infer_future = triton_client.async_infer('chatglm2_6b',
                                                     inputs,
                                                     outputs=outputs,
                                                     request_id=request_id,
                                                     callback=partial(callback, user_data),
                                                     parameters={'Streaming': False})
            expected_responses = 1
            processed_count = 0
            while processed_count < expected_responses:
                result = user_data._completed_requests.get()
                print("Got completed request", flush=True)

                if type(result) == InferenceServerException:
                    if result.status() == "StatusCode.CANCELLED":
                        print("Request is cancelled")
                    else:
                        print(f"Received an error from server:\{result}")
                        raise result
                else:
                    output_ids = result.as_numpy('output_ids')
                    sequence_lengths = result.as_numpy('sequence_length')
                    if output_ids is not None:
                        for beam_output_ids in output_ids[0]:
                            tokens = list(beam_output_ids)
                            actual_output_ids.append(tokens)
                    else:
                        print("Got cancellation response from server")

                processed_count = processed_count + 1
        except Exception as e:
            err = "Encountered error: " + str(e)
            print(err)
            sys.exit(err)

        for beam in range(1):
            seq_len = len(actual_output_ids[beam])
            output_ids_w_prompt = actual_output_ids[beam][:seq_len]
            output_ids_wo_prompt = output_ids_w_prompt[input_ids_data.shape[1]:]
            if tokenizer != None:
                output_text = tokenizer.decode(output_ids_wo_prompt)
                print(f'Input: {text}')
                print(f'Output beam {beam}: {output_text}')
```

## 二、Triton基础

### 1. 模型存储库（Model Repository）

#### 1.1 整体结构

- `model-repository-path` ： 用于在服务启动时填写在`--model-repository`之后
- `model-name` ： 为模型名称
- `config.pbtxt` ： 模型配置文件，对于以下模型可省略，由Triton自动推导。
  - ONNXRuntime,
  - TensorFlow SavedModel
  - TensorRT
  - **需指定`--strict-model-config=false`**
  - 不能指定 `--disable-auto-complete-config`
  - triton-llm不支持自动推导

```bash
<model-repository-path>/
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

#### 1.2 多个文件

- 多个文件组成的 ONNX 模型必须包含在一个目录中。
- 目录名必须为 model.onnx，但模型配置中 default_model_filename 属性可修改。

```bash
<model-repository-path>/
  <model-name>/
    config.pbtxt
    1/
      model.onnx/
         model.onnx
         <other model files>
```

#### 1.3 多个模型文件

- 对于根据模型结构拆分成多个ONNX子模型的情况，需要添加model.py指定调度方式

### 2. 模型配置 `config.pbtxt`

- `config` 文件以 `json` 的形式进行构建, 但 `key` 不需要双引号

- `config.pbtxt` 自动推导需指定`--strict-model-config=false`

#### 2.1 最小模型配置实例

- 一个 TensorRT 模型，有两个输入 input0 和 input1，一个输出 output0

- 输入和输出类型为长 16 的 float32 张量数组。

- 隐藏的 batch 维度最大为 8 ，即可以传入`dims: [ 8, 16 ]`

```json
platform: "tensorrt_plan"
max_batch_size: 8
input [
  {
    name: "input0"
    data_type: TYPE_FP32
    dims: [ 16 ]
  },
  {
    name: "input1"
    data_type: TYPE_FP32
    dims: [ 16 ]
  }
]
output [
  {
    name: "output0"
    data_type: TYPE_FP32
    dims: [ 16 ]
  }
]
```

#### 2.2 Name, Platform 和 Backend

- `name` : 模型名，必须和模型文件路径中的模型名对应（可选）
  
  - 默认与路径中的 `<model-name>` 一致

- `platform/backend`: 平台/后端名通常只需要填写一个，TF部分模型需要两个都填写
  
  - 建议填写 `backend`  更通用
  
  - 支持后端可通过 `ls /opt/tritonserver/backends/` 查看
  
  - dali、 fil、identity、onnxruntime、openvino、python、pytorch、repeat、square、tensorflow、tensorrt、tensorrtllm

- 例子：

```json
name: "chatglm2_6b"
backend: "tensorrtllm"
```

#### 2.3 max_batch_size

- `max_batch_size` 表示模型支持的最大批处理尺寸，根据**显存大小**和算力填写。

- 模型批处理维度须为第一维度且所有输入/输入均含批处理维度。

- `max_batch_size` 应设置为`>=1`的值，调用时批处理数可动态在该范围动态调整。

- `max_batch_size` 为0表示关闭动态批处理。
  
  - 此时开启批处理须在input中明确指定批处理维度
  
  - 如`dims: [ -1, 16 ]`中如果第1维为批处理维度，表示可接受任意批次大小。

- 注: 如果设置 `dynamic_batching.preferred_batch_size` 这个参数的话, 需要确保 `max_batch_size` 大于等于 `preferred_batch_size` 的最大值

- 例子：

```json
max_batch_size: ${triton_max_batch_size}
max_batch_size: 8
```

#### 2.4 Inputs 和 Outputs

- `input`: **模型输入结构** (单个以 key/value 形式配置, 多个以 Array 嵌套 Key/Value 形式配置)
  
  - `name`:(必须的参数) 入参参数名, 与模型预测的入参相同
  
  - `data_type`:(必须的参数) 入参数据类型 (Tensorflow 的话需要解析 Tensor 类型)
  
  - `dims`:(必须的参数) 入参数据维度和模型预测输入的数据源有关.
  
  - `reshape`:(可选的参数) 如果模型入参需要 `reshape` 需参照 `batch_size` 进行 `reshape`
  
  - `is_shape_tensor`: (可选的参数) 对于支持形状张量的模型, 输入时必须设置`is_shape_tensor`, 输出时也必须设置`is_shape_tensor`

- `output`: **模型输出结构** (与 `input` 配置类似)

- 对于data_type类型的确认可以参考参考文献中的 Input-Output参数相关 Triton Inference Server 仓库

- 对于Input-Output参数名称和类型相关可以参考参考文献中的 Input-Output参数相关 FasterTransformer 仓库

- 例子：

```json
input [
  {
    name: "input_ids"
    data_type: TYPE_INT32
    dims: [ -1 ]
  },
  {
    name: "request_output_len"
    data_type: TYPE_INT32
    dims: 1
  }
]
output [
  {
    name: "output_ids"
    data_type: TYPE_FP32
    dims: [ 65024 ]
  }
]
```

#### 2.5 version_policy

- `version_policy`: **模型版本推断** (有三个参数)

- `all`: 模型存储库中可用的模型的所有版本都可用于推断

- `latest`: 最新版本. 模型的最新版本是数字上最大的版本号.

- `specific`: 只有特别列出的模型版本才可用于推断.

#### 2.6 instance_group

- `instance_group`: **实例组** (用于分配模型推断的 GPU 资源)
  
  - `count`: 当前实例的数量(模型数)
  
  - `kind`: `KIND_GPU` 或 `KIND_CPU`,
  
  - `gpus`: [ 0 ] 表示使用 0 号 GPU, [ 1, 2 ] 表示使用 1, 2 号 GPU; 默认全部使用

- 例子：

```json
instance_group [
  {
    count: 1
    kind : KIND_GPU
  }
]
```

#### 2.7 其他

- `dynamic_batching`: **动态批处理** (有一些其他的优先级配置, TIS 文档只有说明没有示例)

- `preferred_batch_size`: 动态批处理大小, 建议遵循 2 的 n 次幂进行设置(数组形式, 如: [1, 2, 4, 8])

- `max_queue_delay_microseconds`: 该参数设置以后会改变动态批处理在无法创建首选大小的批处理程序时的行为. 当无法从可用请求中创建一个首选大小的批次时, 只要没有请求的延迟时间超过配置的 `max_queue_delay_microseconds` , 那么动态批处理就会延迟发送该批次. 如果在这个延迟期间有新的请求到达, 并且允许动态批处理形成一个首选的批处理大小, 那么该批处理机将立即发送以进行推断. 如果延迟过期, 动态批处理机就会按原样发送该批处理, 即使它不是首选大小.

- `preserve_ordering`: 设置用于强制所有响应以收到请求时的相同顺序返回.

### 3 推理协议和API

- `health` ：为 HTTP/REST 和 GRPC 定义的运行状况终结点。对于 GRPC 终结点，此值还会公开 GRPC 运行状况检查协议。

- `metadata` ：为 HTTP/REST 和 GRPC 定义的服务器/模型元数据端点。

- `inference` ：为 HTTP/REST 和 GRPC 定义的推理端点。

- `shared-memory` ：共享内存终结点。

- `model-config` ：模型配置端点。

- `model-repository` ：模型存储库端点。

- `statistics` ：统计端点。

- `trace` ：跟踪终结点。

- `logging` ：日志记录端点。

```bash
tritonserver --grpc-restricted-protocol=shared-memory,model-config,model-repository,statistics,trace:<admin-key>=<admin-value> \
             --http-restricted-api=shared-memory,model-config,model-repository,statistics,trace:<admin-key>=<admin-value> ...
```

## 4 部署实例-预/后处理由 Python backend 执行

### 4.1 文件结构

```bash
triton_model_repo
└── chatglm2_6b
    ├── 1
    │   ├── chatglm2_6b_float16_tp1_rank0.engine
    │   ├── config.json
    │   ├── model.py
    │   └── utils.py
    └── config.pbtxt
```

### 4.1 Python Backend 实现字符串输入输出

- model.py

```python
import torch
import argparse
import json

import tensorrt_llm
from tensorrt_llm.logger import logger
from tensorrt_llm.models import ChatGLMHeadModel
from tensorrt_llm.runtime import PYTHON_BINDINGS, ModelRunner
import numpy as np

from utils import read_model_name, load_tokenizer, throttle_generator
import triton_python_backend_utils as pb_utils

if PYTHON_BINDINGS:
    from tensorrt_llm.runtime import ModelRunnerCpp

class TritonPythonModel:

    @staticmethod
    def auto_complete_config(auto_complete_model_config):
        pass

    def initialize(self, args):
        # You must parse model_config. JSON string is not parsed here
        self.model_config = model_config = json.loads(args["model_config"])
        # Get OUTPUT0 configuration
        output_ids_config = pb_utils.get_output_config_by_name(model_config, "output_ids")
        # Convert Triton types to numpy types
        self.output_ids_dtype = pb_utils.triton_string_to_numpy(
            output_ids_config["data_type"]
        )

        # 解析参数
        self.parse_arguments()

        self.runtime_rank = tensorrt_llm.mpi_rank()
        model_name = read_model_name(self.args.engine_dir)
        self.tokenizer, self.pad_id, self.end_id = load_tokenizer(
            tokenizer_dir=self.args.tokenizer_dir,
            vocab_file=None,
            model_name=model_name,
            tokenizer_type=None,
        )

        if not PYTHON_BINDINGS and not self.args.use_py_session:
            logger.warning( "Python bindings of C++ session is unavailable, fallback to Python session." )
            self.args.use_py_session = True
        runner_cls = ModelRunner if self.args.use_py_session else ModelRunnerCpp
        runner_kwargs = dict(engine_dir=self.args.engine_dir,
                            lora_dir=None,
                            rank=self.runtime_rank,
                            debug_mode=False,
                            lora_ckpt_source="hf")

        if not self.args.use_py_session:
            runner_kwargs.update(
                max_batch_size=len(batch_input_ids),
                max_input_len=max(input_lengths),
                max_output_len=self.args.max_output_len,
                max_beam_width=self.args.num_beams,
                max_attention_window_size=self.args.max_attention_window_size)
        self.runner = runner_cls.from_dir(**runner_kwargs)

        # self.runner
        # self.args
        # self.tokenizer
        # self.pad_id
        # self.end_id
        # self.runtime_rank


    def execute(self, requests):
        output_ids_dtype = self.output_ids_dtype

        responses = []

        # Every Python backend must iterate over everyone of the requests
        # and create a pb_utils.InferenceResponse for each of them.
        for request in requests:
            # Get INPUT0
            input_text = pb_utils.get_input_tensor_by_name(request, "input_text").as_numpy()
            for i in range(len(input_text)):
                for j in range(len(input_text[i])):
                    input_text[i][j] = input_text[i][j].decode('utf-8')
            # Get INPUT1
            request_output_len = pb_utils.get_input_tensor_by_name(request, "request_output_len").as_numpy()

            print(f"input_text: {self.args.input_text}")
            self.args.input_text = input_text[0]
            print(f"input_text: {self.args.input_text}")


            print(f"request_output_len: {self.args.max_output_len}")
            self.args.max_output_len = request_output_len[0][0]
            print(f"request_output_len: {self.args.max_output_len}")

            stop_words_list = None
            bad_words_list = None
            prompt_template = None

            batch_input_ids = self.parse_input(tokenizer=self.tokenizer,
                                        input_text=self.args.input_text,
                                        prompt_template=prompt_template,
                                        add_special_tokens=True,
                                        max_input_length=self.args.max_input_length,
                                        pad_id=self.pad_id,
                                        num_prepend_vtokens=[])
            input_lengths = [x.size(1) for x in batch_input_ids]

            with torch.no_grad():
                outputs = self.runner.generate(
                    batch_input_ids,
                    max_new_tokens=self.args.max_output_len,
                    max_attention_window_size=self.args.max_attention_window_size,
                    end_id=self.end_id,
                    pad_id=self.pad_id,
                    temperature=self.args.temperature,
                    top_k=self.args.top_k,
                    top_p=self.args.top_p,
                    num_beams=self.args.num_beams,
                    length_penalty=self.args.length_penalty,
                    repetition_penalty=self.args.repetition_penalty,
                    stop_words_list=stop_words_list,
                    bad_words_list=bad_words_list,
                    lora_uids=None,
                    prompt_table_path="",
                    prompt_tasks=[],
                    streaming=self.args.streaming,
                    output_sequence_lengths=True,
                    return_dict=True)
                torch.cuda.synchronize()

            if self.runtime_rank == 0:
                if self.args.streaming:
                    for curr_outputs in throttle_generator(outputs, self.args.streaming_interval):
                        output_ids = curr_outputs['output_ids']
                        sequence_lengths = curr_outputs['sequence_lengths']
                else:
                    output_ids = outputs['output_ids']
                    sequence_lengths = outputs['sequence_lengths']
                    context_logits = None
                    generation_logits = None
                    if self.runner.gather_all_token_logits:
                        context_logits = outputs['context_logits']
                        generation_logits = outputs['generation_logits']
                    output_ids = self.get_output(self.tokenizer,
                                                output_ids,
                                                input_lengths,
                                                sequence_lengths)

            # print(output_ids)  
            print(type(output_ids))    
            output_ids_tensor = pb_utils.Tensor("output_ids", output_ids.astype(output_ids_dtype))

            inference_response = pb_utils.InferenceResponse(
                output_tensors=[output_ids_tensor]
            )
            responses.append(inference_response)

        return responses


    def finalize(self):
        del self.runner
        del self.tokenizer
        print('Cleaning up...')


    def parse_arguments(self, args=None):
        parser = argparse.ArgumentParser()
        parser.add_argument('--log_level', type=str, default='error')
        parser.add_argument('--engine_dir', type=str, default="/TRTDir/triton_model_repo/chatglm2_6b/1")
        parser.add_argument('--tokenizer_dir', help="HF tokenizer config path", 
                            default='/TRTDir/Models/chatglm2-6b')
        parser.add_argument('--input_text',type=str,nargs='+',default=["请介绍一下浪潮信息？"])
        parser.add_argument('--max_input_length', type=int, default=923)
        parser.add_argument('--max_output_len', type=int, default=300)
        parser.add_argument('--use_py_session', default=False, action='store_true', 
                            help="Whether or not to use Python runtime session")
        parser.add_argument('--num_beams', type=int, help="Use beam search if num_beams >1", default=1)
        parser.add_argument('--max_attention_window_size', type=int, default=None, 
                            help='The attention window size that controls the sliding window attention / cyclic kv cache behaviour')
        parser.add_argument('--streaming', default=False, action='store_true')
        parser.add_argument('--streaming_interval', type=int, help="How often to return tokens when streaming.", default=5)
        
        # 还不理解的
        parser.add_argument('--temperature', type=float, default=1.0)
        parser.add_argument('--top_k', type=int, default=1)
        parser.add_argument('--top_p', type=float, default=0.0)
        parser.add_argument('--length_penalty', type=float, default=1.0)
        parser.add_argument('--repetition_penalty', type=float, default=1.0)
        self.args =  parser.parse_args(args=args)


    def parse_input(self, 
                    tokenizer,
                    input_text=None,
                    prompt_template=None,
                    add_special_tokens=True,
                    max_input_length=923,
                    pad_id=None,
                    num_prepend_vtokens=[]):
        if pad_id is None:
            pad_id = tokenizer.pad_token_id

        batch_input_ids = []
        for curr_text in input_text:
            if prompt_template is not None:
                curr_text = prompt_template.format(input_text=curr_text)
            input_ids = tokenizer.encode(curr_text,
                                        add_special_tokens=add_special_tokens,
                                        truncation=True,
                                        max_length=max_input_length)
            batch_input_ids.append(input_ids)

        if num_prepend_vtokens:
            assert len(num_prepend_vtokens) == len(batch_input_ids)
            base_vocab_size = tokenizer.vocab_size - len(
                tokenizer.special_tokens_map.get('additional_special_tokens', []))
            for i, length in enumerate(num_prepend_vtokens):
                batch_input_ids[i] = list(
                    range(base_vocab_size,
                        base_vocab_size + length)) + batch_input_ids[i]

        batch_input_ids = [
            torch.tensor(x, dtype=torch.int32).unsqueeze(0) for x in batch_input_ids
        ]
        return batch_input_ids


    def get_output(self,
                    tokenizer,
                    output_ids,
                    input_lengths,
                    sequence_lengths,
                    context_logits=None,
                    generation_logits=None,
                    output_logits_npy=None):
        batch_size, num_beams, _ = output_ids.size()
        
        output_text_matrix = np.empty(batch_size, dtype=object) 
        for batch_idx in range(batch_size):
            inputs = output_ids[batch_idx][0][:input_lengths[batch_idx]].tolist(
            )
            input_text = tokenizer.decode(inputs)
            output_text_array = np.empty(num_beams, dtype=object) 
            # print(f'Input [Text {batch_idx}]: \"{input_text}\"')
            for beam in range(num_beams):
                output_begin = input_lengths[batch_idx]
                output_end = sequence_lengths[batch_idx][beam]
                outputs = output_ids[batch_idx][beam][
                    output_begin:output_end].tolist()
                output_text = tokenizer.decode(outputs)
                output_text_array[beam] = output_text
                # print(f'Output [Text {batch_idx} Beam {beam}]: \"{output_text}\"')
            output_text_matrix[batch_idx] = output_text_array

        return output_text_matrix



```

- config.pbtxt

```json
name: "chatglm2_6b"
backend: "python"
max_batch_size: 8

input [
  {
    name: "input_text"
    data_type: TYPE_STRING
    dims: [ -1 ]
  },
  {
    name: "request_output_len"
    data_type: TYPE_INT32
    dims: 1
  }
]
output [
  {
    name: "output_ids"
    data_type: TYPE_STRING
    dims: [ -1 ]
  }
]
parameters: {
  key: "gpt_model_type"
  value: {
    string_value: "V1"
  }
}
parameters: {
  key: "gpt_model_path"
  value: {
    string_value: "/TRTDir/triton_model_repo/chatglm2_6b/1"
  }
}
parameters: {
  key: "max_tokens_in_paged_kv_cache"
  value: {
    string_value: "100"
  }
}
parameters: {
  key: "batch_scheduler_policy"
  value: {
    string_value: "guaranteed_no_evict"
  }
}
```

## 参考文献

Triton

https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/performance_tuning.html

https://zhuanlan.zhihu.com/p/366555962

查看模型结构

[TensorRT: Inspecting A TensorRT Engine](https://www.ccoderun.ca/programming/doxygen/tensorrt/md_TensorRT_tools_Polygraphy_examples_cli_inspect_02_inspecting_a_tensorrt_engine_README.html)

https://github.com/NVIDIA/TensorRT/tree/release/8.6/tools/experimental/trt-engine-explorer

Restful API相关

https://github.com/triton-inference-server/server/blob/main/docs/protocol/extension_model_configuration.md

TensorRT Python API

[ICudaEngine — NVIDIA TensorRT Standard Python API Documentation 8.6.1 documentation](https://docs.nvidia.com/deeplearning/tensorrt/api/python_api/infer/Core/Engine.html)

Input-Output参数相关

https://github.com/triton-inference-server/server/blob/main/docs/user_guide/model_configuration.md

https://github.com/NVIDIA/FasterTransformer/blob/main/docs/gpt_guide.md

Python Backend 说明

https://github.com/triton-inference-server/python_backend

Python Backend Utils 源码

https://github.com/triton-inference-server/python_backend/blob/main/src/resources/triton_python_backend_utils.py
