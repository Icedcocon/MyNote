# vLLM 架构

## 一、

### 1. 项目结构

```bash
.
├── core                        # Scheduler、 BlockManager
├── engine                      # LLMEngine、 AsyncLLMEngine
├── entrypoints                 # Web Restful API 接口
│   └── openai
├── model_executor              # 支持模型
│   ├── layers
│   │   ├── quantization
│   │   └── triton_kernel
│   ├── models
│   └── parallel_utils
├── transformers_utils
│   ├── configs
│   └── tokenizers
└── worker                      # Worker
    └── spec_decode
```

### 2. 源码

#### 2.1 add_request

```python
# add_request函数是LLMEngine类的一个方法，它接受一个请求并将其加入到scheduler的请求池中。
# 这个请求在调用engine.step()函数时由调度器进行处理，具体的调度策略由调度器决定。
def add_request(
        self,
        request_id: str, # 请求的唯一ID。
        prompt: Optional[str], # prompt字符串。如果提供了prompt_token_ids，这个参数可以为None。
        sampling_params: SamplingParams, # 用于文本生成的采样参数。
        # prompt的token ID。如果它为None，则使用分词器将提示转换为token ID。
        prompt_token_ids: Optional[List[int]] = None, 
        arrival_time: Optional[float] = None, # 请求的到达时间。如果为None，则使用当前时间。
    ) -> None:
        if arrival_time is None:
            arrival_time = time.time()
        if prompt_token_ids is None:
            assert prompt is not None
            prompt_token_ids = self.tokenizer.encode(prompt)

        # Create the sequences.
        # 每一个序列代表一次独立的文本生成任务。它们的数量由sampling_params.best_of决定。
        # 每个序列都包含了唯一的seq_id，提示和标记ID，以及block_size（块大小）。
        block_size = self.cache_config.block_size
        seqs: List[Sequence] = []
        for _ in range(sampling_params.best_of):
            seq_id = next(self.seq_counter)
            seq = Sequence(seq_id, prompt, prompt_token_ids, block_size)
            seqs.append(seq)

        # 创建序列组（SequenceGroup）。一个序列组包含了一组相关的序列，
        # 它们共享相同的请求ID和采样参数，并且在同一时间到达。
        seq_group = SequenceGroup(request_id, seqs, sampling_params,
                                  arrival_time)

        # Add the sequence group to the scheduler.
        # 将序列组添加到调度器中。这样，当调用engine.step()函数时，
        # 调度器就可以根据它的调度策略处理这些序列组。
        self.scheduler.add_seq_group(seq_group)
```

## 参考资料

- 关于推理流程相关源码

https://zhuanlan.zhihu.com/p/643336063
