# Triton-ensamble使用指南

## 一、 配置

### 1. 模型仓库

#### 1.1 文件结构

```bash
chatglm_model_repo
├── chatglm2_6b          # chatglm推理模型
│   ├── 1                # 版本
│   │   ├── chatglm2_6b_float16_tp1_rank0.engine
│   │   ├── config.json  # TensorRT模型配置文件
│   │   └── model.py     # Python Backend
│   └── config.pbtxt     # triton配置文件
├── ensemble             # ensemble 模型配置
│   ├── 1
│   └── config.pbtxt     # triton配置文件
├── postprocessor        # 后处理操作
│   ├── 1
│   │   └── model.py     # Python Backend
│   └── config.pbtxt
└── preprocessor         # 预处理操作 
    ├── 1
    │   └── model.py     # Python Backend
    └── config.pbtxt     # triton配置文件
```

#### 1.2 Python Backend模板

```python
import json
import triton_python_backend_utils as pb_utils

class TritonPythonModel:

    def initialize(self, args):
        self.model_config = model_config = json.loads(args["model_config"])
        output0_config = pb_utils.get_output_config_by_name(model_config, "OUTPUT0")
        self.output0_dtype = pb_utils.triton_string_to_numpy(
        output0_config["data_type"]
        )

    def execute(self, requests):
        output0_dtype = self.output0_dtype
        responses = []
        for request in requests:
            in_0 = pb_utils.get_input_tensor_by_name(request, "INPUT0")
            out_0 = in_0.as_numpy()
            out_tensor_0 = pb_utils.Tensor("OUTPUT0", 
                out_0.astype(output0_dtype))
            inference_response = pb_utils.InferenceResponse(
                output_tensors=[out_tensor_0, out_tensor_1])
            responses.append(inference_response)
        return responses

    def finalize(self):
        print("Cleaning up...")
```

#### 1.3 config.pbtxt

```json
name: "add_sub"
backend: "python"

input [
  {
    name: "INPUT0"
    data_type: TYPE_FP32
    dims: [ 4 ]
  }
]
output [
  {
    name: "OUTPUT0"
    data_type: TYPE_FP32
    dims: [ 4 ]
  }
]

instance_group [{ kind: KIND_CPU }]
```

## 参考资料

- streaming inference说明及AI部署相关话题

https://ai.oldpan.me/t/topic/260
