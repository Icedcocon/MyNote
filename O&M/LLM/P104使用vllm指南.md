# P04 使用 vllm 指南

## 编译安装

- 拉取仓库

```bash
git clone https://github.com/vllm-project/vllm.git
cd vllm
```

- 编辑 `vllm/CMakeLists.txt` 补充 6.1

```bash
 # Supported NVIDIA architectures. 
 set(CUDA_SUPPORTED_ARCHS "6.1;7.0;7.5;8.0;8.6;8.9;9.0") 
```

- 编译

```bash
pip install -e .
```

## 参考资料

[[Usage]: doesn&#39;t work on pascal tesla P100 · Issue #8626 · vllm-project/vllm · GitHub](https://github.com/vllm-project/vllm/issues/8626)

[Installation &#8212; vLLM](https://docs.vllm.ai/en/latest/getting_started/installation.html#build-from-source)
