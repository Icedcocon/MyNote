1

### 1.  表1

| Model                       | Microarchitecture | CUDA Compute Capability |
| --------------------------- | ----------------- | ----------------------- |
| V100 GPU accelerator        | -                 | 7.0                     |
| T4 GPU accelerator          | Turing            | 7.5                     |
| A2 GPU accelerator          | -                 | 8.6                     |
| A10 GPU accelerator         | -                 | 8.6                     |
| A16 GPU accelerator         | Ampere            | 8.6                     |
| A30 GPU accelerator         | -                 | 8.0                     |
| A40 GPU accelerator         | -                 | 8.6                     |
| A100 GPU accelerator        | -                 | 8.0                     |
| H100 GPU accelerator (PCIe) | -                 | 9.0                     |
| H100 GPU accelerator (SXM)  | -                 | 9.0                     |
| H200 GPU accelerator (PCIe) | Hopper            | 9.0                     |
| H200 GPU accelerator (SXM)  | -                 | 9.0                     |
| H800 GPU accelerator (SXM)  | -                 | 9.0                     |
| L40 GPU accelerator         | Ada Lovelace      | 8.9                     |
| L4 GPU accelerator          | -                 | 8.9                     |

### 2. 表2

| CUDA Compute Capability | Example Devices       | TF32 | FP32 | FP16 | FP8 | FP4 | BF16   | INT8 | FP16 Tensor Cores | INT8 Tensor Cores | DLA |
| ----------------------- | --------------------- | ---- | ---- | ---- | --- | --- | ------ | ---- | ----------------- | ----------------- | --- |
| 12.0                    | NVIDIA RTX 5090       | Yes  | Yes  | Yes  | Yes | Yes | Yes    | Yes  | Yes               | Yes               | No  |
| 10.0                    | NVIDIA B200           | Yes  | Yes  | Yes  | Yes | Yes | Yes    | Yes  | Yes               | Yes               | No  |
| 9.0                     | NVIDIA H100           | Yes  | Yes  | Yes  | Yes | Yes | Yes[5] | Yes  | Yes               | Yes               | No  |
| 9.0                     | NVIDIA GH200 480 GB   | Yes  | Yes  | Yes  | Yes | Yes | Yes[5] | Yes  | Yes               | Yes               | No  |
| 8.9                     | NVIDIA L40S           | Yes  | Yes  | Yes  | Yes | Yes | Yes[5] | Yes  | Yes               | Yes               | No  |
| 8.7                     | NVIDIA DRIVE AGX Orin | Yes  | Yes  | Yes  | No  | No  | No     | Yes  | Yes               | Yes               | Yes |
| 8.6                     | NVIDIA A10            | Yes  | Yes  | Yes  | No  | No  | Yes    | Yes  | Yes               | Yes               | No  |
| 8.0                     | NVIDIA A100           | Yes  | Yes  | Yes  | No  | No  | Yes    | Yes  | Yes               | Yes               | No  |
| 7.5                     | NVIDIA T4             | No   | Yes  | Yes  | No  | No  | No     | Yes  | Yes               | Yes               | No  |

### 3. 表3

| Model                       | Microarchitecture | CUDA Compute Capability | TF32 | FP32 | FP16 | FP8 | FP4 | BF16   | INT8 | FP16 Tensor Cores | INT8 Tensor Cores | DLA |
| --------------------------- | ----------------- | ----------------------- | ---- | ---- | ---- | --- | --- | ------ | ---- | ----------------- | ----------------- | --- |
| V100 GPU accelerator        | -                 | 7.0                     | No   | Yes* | Yes* | No  | No  | No     | Yes* | Yes*              | Yes*              | No  |
| T4 GPU accelerator          | Turing            | 7.5                     | No   | Yes  | Yes  | No  | No  | No     | Yes  | Yes               | Yes               | No  |
| A2 GPU accelerator          | -                 | 8.6                     | Yes  | Yes  | Yes  | No  | No  | Yes    | Yes  | Yes               | Yes               | No  |
| A10 GPU accelerator         | -                 | 8.6                     | Yes  | Yes  | Yes  | No  | No  | Yes    | Yes  | Yes               | Yes               | No  |
| A16 GPU accelerator         | Ampere            | 8.6                     | Yes  | Yes  | Yes  | No  | No  | Yes    | Yes  | Yes               | Yes               | No  |
| A30 GPU accelerator         | -                 | 8.0                     | Yes  | Yes  | Yes  | No  | No  | Yes    | Yes  | Yes               | Yes               | No  |
| A40 GPU accelerator         | -                 | 8.6                     | Yes  | Yes  | Yes  | No  | No  | Yes    | Yes  | Yes               | Yes               | No  |
| A100 GPU accelerator        | -                 | 8.0                     | Yes  | Yes  | Yes  | No  | No  | Yes    | Yes  | Yes               | Yes               | No  |
| H100 GPU accelerator (PCIe) | -                 | 9.0                     | Yes  | Yes  | Yes  | Yes | Yes | Yes[5] | Yes  | Yes               | Yes               | No  |
| H100 GPU accelerator (SXM)  | -                 | 9.0                     | Yes  | Yes  | Yes  | Yes | Yes | Yes[5] | Yes  | Yes               | Yes               | No  |
| H200 GPU accelerator (PCIe) | Hopper            | 9.0                     | Yes  | Yes  | Yes  | Yes | Yes | Yes[5] | Yes  | Yes               | Yes               | No  |
| H200 GPU accelerator (SXM)  | -                 | 9.0                     | Yes  | Yes  | Yes  | Yes | Yes | Yes[5] | Yes  | Yes               | Yes               | No  |
| H800 GPU accelerator (SXM)  | -                 | 9.0                     | Yes  | Yes  | Yes  | Yes | Yes | Yes[5] | Yes  | Yes               | Yes               | No  |
| L40 GPU accelerator         | Ada Lovelace      | 8.9                     | Yes  | Yes  | Yes  | Yes | Yes | Yes[5] | Yes  | Yes               | Yes               | No  |
| L4 GPU accelerator          | -                 | 8.9                     | Yes  | Yes  | Yes  | Yes | Yes | Yes[5] | Yes  | Yes               | Yes               | No  |

### 3. 表3

| AI Model                      | 参数规模 | 计算精度 | 最低存储需求 | 最低算力需求          |
| ----------------------------- | ---- | ---- | ------ | --------------- |
| DeepSeek-R1                   | 685B | FP8  | ≥890GB | ≥2XE9680(16H20) |
| DeepSeek-R1                   | 685B | INT4 | ≥450GB | ≥1XE9680(8H20)  |
| DeepSeek-V3                   | 671B | FP8  | ≥870GB | ≥2XE9680(16H20) |
| DeepSeek-V3                   | 671B | INT4 | ≥440GB | ≥1XE9680(8H20)  |
| DeepSeek-R1-Distill-Llama-70B | 70B  | BF16 | ≥180GB | ≥4L20 or ≥2H20  |
| DeepSeek-R1-Distill-Qwen-32B  | 32B  | BF16 | ≥80GB  | ≥3L20 or ≥1H20  |
| DeepSeek-R1-Distill-Qwen-14B  | 14B  | BF16 | ≥40GB  | ≥2L20           |
| DeepSeek-R1-Distill-Llama-8B  | 8B   | BF16 | ≥22GB  | ≥1L20           |
| DeepSeek-R1-Distill-Qwen-7B   | 7B   | BF16 | ≥20GB  | ≥1L20           |
| DeepSeek-R1-Distill-Qwen-1.5B | 1.5B | BF16 | ≥5GB   | ≥1A10           |

### 4. 表4

| GPU      | 支持数据类型              |
| -------- | ------------------- |
| RTX 4090 | FP8, FP16, bfloat16 |
| L20      | FP8, FP16, bfloat16 |
| L2       | FP8, FP16, bfloat16 |
| H20      | FP8, FP16, bfloat16 |
| A100     | FP16, bfloat16      |
| A800     | FP16, bfloat16      |
| T4       | FP16      |

## 参考文档

[Support Matrix &#8212; NVIDIA TensorRT Documentation](https://docs.nvidia.com/deeplearning/tensorrt/latest/getting-started/support-matrix.html#hardware-precision-matrix)

[List of Nvidia graphics processing units - Wikipedia](https://en.wikipedia.org/wiki/List_of_Nvidia_graphics_processing_units#Tesla)

[1. Introduction &mdash; CUDA C++ Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#compute-capability-12-0)

显存计算器

https://medium.com/@manuelescobar-dev/memory-requirements-for-llm-training-and-inference-97e4ab08091b
