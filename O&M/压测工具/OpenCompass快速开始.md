# OpenCompass快速开始

## 一、环境准备

### 1. 克隆代码并编译镜像

- 克隆代码

```bash
git clone https://github.com/open-compass/opencompass.git
cd opencompass
vim Dockerfile
```

- Dockerfile

```dockerfile
FROM registry.cn-hangzhou.aliyuncs.com/xprobe_xinference/xinference:v0.13.0

ADD . /workspace/opencompass

WORKDIR /workspace/opencompass

RUN pip install -e . \
&& pip install -e dataset-requirements/human-eval
```

- 编译镜像

```bash
docker build -t opencompass:v0.2.6 -f Dockerfile .
```

- 下载数据集

```bash
 wget https://github.com/open-compass/opencompass/releases/download/0.2.2.rc1/OpenCompassData-core-20240207.zip
```

## 二、使用指南

### 1. 启动容器

- 启动容器

Models 中为HF格式模型文件

data中为 `OpenCompassData-core-20240207.zip` 解压后的内容

```bash
docker run -itd --gpus all \
           --name opencompass \
           -v `realpath Models`:/workspace/opencompass/models \
           -v `realpath Dataset/data`:/workspace/opencompass/data \
           opencompass:v0.2.6 bash
```

### 2. 测试

#### 2.1 配置

- 编辑 `config/models/others/hf_command_r.py`

```python
from opencompass.models import HuggingFacewithChatTemplate
# 修改路径为模型路径并调整其它参数
models = [
    dict(
        type=HuggingFacewithChatTemplate,
        abbr='command-r-hf',
        path='/workspace/opencompass/models/c4ai-command-r-v01',
        max_out_len=1024,
        batch_size=8,
        run_cfg=dict(num_gpus=2),
    )
]
```

- 编辑 `config/models/others/vllm_command_r.py`

```python
from opencompass.models import VLLMwithChatTemplate
# 修改路径为模型路径并调整其它参数
models = [
    dict(
        type=VLLMwithChatTemplate,
        abbr='command-r-hf',
        path='/workspace/opencompass/models/c4ai-command-r-v01',
        max_out_len=1024,
        batch_size=128,
        model_kwargs=dict(tensor_parallel_size=2),
        run_cfg=dict(num_gpus=2),
    )
]
```

- 编辑 `config/datasets/humaneval/humaneval_gen_66a7f4.py`

```python
from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import ZeroRetriever
from opencompass.openicl.icl_inferencer import GenInferencer
from opencompass.datasets import HumanevalDataset, HumanEvalEvaluator, humaneval_postprocess_v2

humaneval_reader_cfg = dict(input_columns=['prompt'], output_column='task_id', train_split='test')

HUMANEVAL_TEMPLATE = dict(
    round=[
        dict(role='HUMAN', prompt='You are an intelligent programming assistant to produce Python algorithmic solutions.\nCan you complete the following Python function?\n```python\n{prompt}\n```'),
    ]
)

humaneval_infer_cfg = dict(
    prompt_template=dict(type=PromptTemplate, template=HUMANEVAL_TEMPLATE),
    retriever=dict(type=ZeroRetriever),
    inferencer=dict(type=GenInferencer, max_out_len=1024),
)

humaneval_eval_cfg = dict(
    evaluator=dict(type=HumanEvalEvaluator),
    k=[1, 10, 100],
    pred_postprocessor=dict(type=humaneval_postprocess_v2),
)
# 修改数据集路径
humaneval_datasets = [
    dict(
        abbr='openai_humaneval',
        type=HumanevalDataset,
        path='/workspace/opencompass/data/humaneval/human-eval-v2-20210705.jsonl',
        reader_cfg=humaneval_reader_cfg,
        infer_cfg=humaneval_infer_cfg,
        eval_cfg=humaneval_eval_cfg,
    )
]
```

#### 2.2 开始测试

```bash
# 名称要与 .py 文件名称对应
python3 run.py --models vllm_command_r --datasets humaneval_gen_66a7f4
```

## 参考资料

- Github

[opencompass/README_zh-CN.md at main · open-compass/opencompass · GitHub](https://github.com/open-compass/opencompass/blob/main/README_zh-CN.md)
