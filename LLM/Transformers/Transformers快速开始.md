# Transformer 快速开始

## 一、分词器 Tokenizer

### 1. 介绍

#### 1.1 数据预处理

- Step1 **分词**; 使用分词器对文本数据进行分词 (字、字词) ;

- Step2 **构建词典**: 根据数据集分词的结果，构建词典映射 这一步并不绝对，如果采用预训练词向量，词典映射要根据词向量文件进行处理) ;

- Step3 **数据转换**; 根据构建好的词典，将分词处理后的数据做映射，将文本序列转换为数字序列;

- Step4 **数据填充与截断**: 在以batch输入到模型的方式中，需要对过短的数据进行填充，过长的数据进行截断，保证数据长度符合模型能接受的范围，同时batch内的数据维度大小一致。

在Transformers中这个过程被称为**编码 (Encoding)**，其包含两个步骤：

1. 使用分词器 (tokenizer) 将文本按词、子词、字符切分为 tokens；
2. 将所有的 token 映射到对应的 token ID。

#### 1.2 分词策略

- **按词切分 (Word-based)**

这种策略的问题是会将文本中所有出现过的独立片段都作为不同的 token，从而产生巨大的词表。而实际上很多词是相关的，例如 “dog” 和 “dogs”、“run” 和 “running”，如果给它们赋予不同的编号就无法表示出这种关联性。

> 词表就是一个映射字典，负责将 token 映射到对应的 ID（从 0 开始）。神经网络模型就是通过这些 token ID 来区分每一个 token。

当遇到不在词表中的词时，分词器会使用一个专门的  token 来表示它是 unknown 的。显然，如果分词结果中包含很多  就意味着丢失了很多文本信息，因此一个好的分词策略，应该尽可能不出现 unknown token。

- **按字符切分 (Character-based)**

这种策略把文本切分为字符而不是词语，这样就只会产生一个非常小的词表，并且很少会出现词表外的 tokens。

但是从直觉上来看，字符本身并没有太大的意义，因此将文本切分为字符之后就会变得不容易理解。这也与语言有关，例如中文字符会比拉丁字符包含更多的信息，相对影响较小。此外，这种方式切分出的 tokens 会很多，例如一个由 10 个字符组成的单词就会输出 10 个 tokens，而实际上它们只是一个词。

- **按子词切分 (Subword)**

高频词直接保留，低频词被切分为更有意义的子词。例如 “annoyingly” 是一个低频词，可以切分为 “annoying” 和 “ly”，这两个子词不仅出现频率更高，而且词义也得以保留。

#### 1.3 基本操作

- 加载保存 (from_pretrained / save_pretrained)

- 句子分词 (tokenize)

- 查看词典 (vocab)

- 索引转换 (convert_tokens_to_ids / convert_ids_to_tokens)

- 填充截断 (padding /truncation)

- 其他输入 (attention_mask /token_type_ids)

### 2. 操作

#### 2.1 基本操作

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
sequence = "Using a Transformer network is simple"
```

##### 2.1.1 加载与保存

###### 2.1.1.1 指令

```python
# 从HuggingFace加载，输入模型名称，即可加载对于的分词器
tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
# tokenizer 保存到本地
tokenizer.save_pretrained("./roberta_tokenizer")
# 从本地加载tokenizer
tokenizer = AutoTokenizer.from_pretrained("./roberta_tokenizer/")

# 实际例子
tokenizer = AutoTokenizer.from_pretrained(
    model_path,
    use_fast=True,
    trust_remote_code=True,
    revision="revision",
    add_eos_token=False,
    add_bos_token=False,
    eos_token='<eod>'
)
```

**常见参数**

- **pretrained_model_name_or_path**: 可以是预训练模型的ID、包含词汇文件的目录路径,或单个词汇文件的路径/URL。

- **use_fast**: 是否使用基于Rust的快速tokenizer。

- **trust_remote_code**: 是否允许执行Hub上自定义模型的代码。

- **add_eos_token**: 是否在每个序列的末尾自动添加结束标记(EOS, End of Sequence)，可以通过配置文件 `tokenizer_config.json` 设置。

- **add_bos_token**: 是否在每个序列的开始自动添加开始标记(BOS, Beginning of Sequence)，可以通过配置文件`tokenizer_config.json`设置。

- **eos_token**: 定义了结束标记(EOS)的具体表示，，可以通过配置文件`tokenizer_config.json`设置`。

- inputs: 可选的额外位置参数,将传递给Tokenizer的__init__()方法。

- config: 可选的配置对象,用于确定要实例化的tokenizer类。

- cache_dir: 可选的缓存目录路径。

- force_download: 是否强制重新下载模型权重和配置文件。

- resume_download: 已弃用,将在v5版本中移除。

- proxies: 代理服务器字典。

- revision: 指定模型版本,可以是分支名、标签名或提交ID。

- subfolder: 指定相关文件在huggingface.co模型仓库中的子文件夹。

- tokenizer_type: 要加载的tokenizer类型。

- kwargs: 额外的关键字参数,用于设置特殊token等。

###### 2.1.1.2 配置文件 tokenizer_config.json

- Qwen的Tokenizer （使用自定义QWenTokenizer）

> 注意： 自定义Tokenizer需要提供Python脚本实现，此处为`tokenization_qwen.py` 。
> 
> 注意： 当使用自定义Tokenizer时，因包含Python代码，因此需要指定 `trust_remote_code=True`

```json
{
  "model_max_length": 8192,
  "tokenizer_class": "QWenTokenizer",
  "auto_map": {
    "AutoTokenizer": [
      "tokenization_qwen.QWenTokenizer",
      null
      ]
  }
}
```

- Yuan2的Tokenizer（使用LlamaTokenizer）
  
  - add_bos_token 和 add_eos_token: 都设置为 false，意味着不会自动在序列开始和结束添加特殊标记。
  
  - sep_token: 分隔符标记设置为 "<sep>"。
  
  - eod_token: 文档结束标记设置为 "<eod>"。
  
  - chat_template: 定义了如何格式化对话消息。它使用 Jinja2 模板语法，根据消息的角色（system、user、assistant）来格式化内容，并在适当的位置添加分隔符。
  
  - bos_token、eos_token、unk_token: 这些是特殊标记的详细配置。它们都被定义为 AddedToken 类型，具有特定的属性（如 lstrip、rstrip、normalized 等）。
  
  - clean_up_tokenization_spaces: 设置为 false，表示不会清理标记化过程中的空格。
  
  - model_max_length: 设置了一个非常大的数值，实际上相当于没有限制模型的最大长度。
  
  - pad_token: 设置为 null，表示没有使用填充标记。
  
  - sp_model_kwargs: 空字典，可能用于存储 SentencePiece 模型的额外参数。
  
  - tokenizer_class: 指定使用 "LlamaTokenizer" 类。

```json
{
  "add_bos_token": false,
  "add_eos_token": false,
  "sep_token": "<sep>",
  "eod_token": "<eod>",
  "chat_template": "{% for message in messages %}{% if message['role'] == 'system' %}{{ message['content'].strip() + '\\n' }}{% elif message['role'] == 'user' %}{{ message['content'].strip() + (sep_token if loop.last else '<n>') }}{% elif message['role'] == 'assistant' %}{{ message['content'].strip() + (sep_token if loop.last else '<n>') }}{% endif %}{% endfor %}",
  "bos_token": {
    "__type": "AddedToken",
    "content": "<s>",
    "lstrip": false,
    "normalized": true,
    "rstrip": false,
    "single_word": false
  },
  "clean_up_tokenization_spaces": false,
  "eos_token": {
    "__type": "AddedToken",
    "content": "</s>",
    "lstrip": false,
    "normalized": true,
    "rstrip": false,
    "single_word": false
  },
  "model_max_length": 1000000000000000019884624838656,
  "pad_token": null,
  "sp_model_kwargs": {},
  "tokenizer_class": "LlamaTokenizer",
  "unk_token": {
    "__type": "AddedToken",
    "content": "<unk>",
    "lstrip": false,
    "normalized": true,
    "rstrip": false,
    "single_word": false
  }
}
```

##### 2.1.2 句子分词

- 此处使用字词切分策略

```python
tokens = tokenizer.tokenize(sequence)
print(tokens)
# ['using', 'a', 'transform', '##er', 'network', 'is', 'simple']
```

##### 2.1.3 查看词典

```python
tokenizer.vocab
tokenizer.vocab_size
```

##### 2.1.4 映射

文本编码 (Encoding) 过程包含两个步骤：

1. **分词：** 使用分词器按某种策略将文本切分为 tokens；
2. **映射：** 将 tokens 转化为对应的 token IDs。

```python
# 将词序列转换为id序列
ids = tokenizer.convert_tokens_to_ids(tokens)
print(ids)
# [7993, 170, 13809, 23763, 2443, 1110, 3014]

# 将id序列转换为token序列
tokens = tokenizer.convert_ids_to_tokens(ids)
print(tokens)
# ['using', 'a', 'transform', '##er', 'network', 'is', 'simple']

# 将token序列转换为string
str_sen = tokenizer.convert_tokens_to_string(tokens)
str_sen
```

- **编码 = 分词 + 映射**

可以通过 `encode()` 函数将这两个步骤合并，并且 `encode()` 会自动添加模型需要的特殊 token，例如 BERT 分词器会分别在序列的首尾添加  和 ：

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
sequence = "Using a Transformer network is simple"

sequence_ids = tokenizer.encode(sequence, add_special_tokens=True)
print(sequence_ids)
# [101, 7993, 170, 13809, 23763, 2443, 1110, 3014, 102]

str_sen = tokenizer.decode(ids, skip_special_tokens=False)
str_sen
```

>  注意： 其中 101 和 102 分别是  和  对应的 token IDs。

##### 2.1.5 填充与截断

```python
# 填充
ids = tokenizer.encode(sen, padding="max_length", max_length=15)

# 截断
ids = tokenizer.encode(sen, max_length=5, truncation=True)
```

##### 2.1.6 其他部分

- 分部生成推理需要参数

```python
ids = tokenizer.encode(sen, padding="max_length", max_length=15) # tokens
attention_mask = [1 if idx != 0 else 0 for idx in ids]           # mask
token_type_ids = [0] * len(ids)                                  # 分句
ids, attention_mask, token_type_ids
```

- 快速调用

```python
inputs = tokenizer.encode_plus(sen, padding="max_length", max_length=15)
```

## 二、模型 AutoModel

AutoModelFor类让你可以加载给定任务的预训练模型（参见这里获取可用任务的完整列表）。例如，使用AutoModelForSequenceClassification.from_pretrained()加载用于序列分类的模型。

### 1. 介绍

#### 1.1 文本生成

- Next token logits

一个用于因果语言建模训练的语言模型，将文本tokens序列作为输入，并返回下一个token的概率分布。（"你好呀"  -> List[下一个字为字典中某个 token_id 的概率)]）

- Token Selection

使用LLM进行自回归生成的一个关键方面是如何从这个概率分布中选择下一个`token`。这个步骤可以随意进行，只要最终得到下一个迭代的`token`。这意味着可以简单的从概率分布中选择最可能的`token`，也可以复杂的在对结果分布进行采样之前应用多种变换，这取决于你的需求。

上述过程是迭代重复的，直到达到某个停止条件。理想情况下，停止条件由模型决定，该模型应学会在何时输出一个结束序列（`EOS`）标记。如果不是这种情况，生成将在达到某个预定义的最大长度时停止。

### 2. 操作

#### 2.1 基本操作

##### 2.1.1 加载模型

- 将模型创建为空壳，然后只有在加载预训练权重时才实例化其参数。

使用 `low_cpu_mem_usage=True` 激活此选项。最大使用的内存占用仅为模型的完整大小。

```python
from transformers import AutoModelForSeq2SeqLM
t0pp = AutoModelForSeq2SeqLM.from_pretrained("bigscience/T0pp",
                                              low_cpu_mem_usage=True)
```

如果内存不足以放下加载整个模型（目前仅适用于推理），您可以直接将模型放置在不同的设备上。使用 `device_map="auto"`，Accelerate 将确定将每一层放置在哪个设备上，以最大化使用最快的设备（GPU），并将其余部分卸载到 CPU，甚至硬盘上（如果您没有足够的 GPU 内存 或 CPU 内存）。

> 注意: 在传递 `device_map` 时，`low_cpu_mem_usage` 会自动设置为 `True`

```python
from transformers import AutoModelForSeq2SeqLM
t0pp = AutoModelForSeq2SeqLM.from_pretrained("bigscience/T0pp", 
                                               device_map="auto")
```

##### 2.1.2 查看模型分割/存放方式

可以通过 `hf_device_map` 属性来查看模型是如何在设备上分割的。

```python
t0pp.hf_device_map
{'shared': 0,
 'decoder.embed_tokens': 0,
 'encoder': 0,
 'decoder.block.0'
  .....
 'decoder.block.20': 1,
 'decoder.block.21': 1,
 'decoder.block.22': 'cpu',
 'decoder.block.23': 'cpu',
 'decoder.final_layer_norm': 'cpu',
 'decoder.dropout': 'cpu',
 'lm_head': 'cpu'}
```

您还可以按照相同的格式（一个层名称到设备的映射关系的字典）编写自己的设备映射规则。它应该将模型的所有参数映射到给定的设备上，如果该层的所有子模块都在同一设备上，您不必详细说明其中所有子模块的位置。例如，以下设备映射对于 T0pp 将正常工作（只要您有 GPU 内存）：

```python
device_map = {"shared": 0, "encoder": 0, "decoder": 1, "lm_head": 1}
```

##### 2.1.3 模型实例化 dtype

另一种减少模型内存影响的方法是以较低精度的 dtype（例如 `torch.float16`）实例化它，或者使用下面介绍的直接量化技术。

在 PyTorch 下，模型通常以 `torch.float32` 格式实例化。可以使用 `torch_dtype` 参数显式传递所需的 `dtype`：

```python
# 加载权重为 fp16 的模型
model = T5ForConditionalGeneration.from_pretrained("t5", 
                                                      torch_dtype=torch.float16)

# 以最优的内存模式加载，则可以使用特殊值 `"auto"`，然后 `dtype` 将自动从模型的权重中推导出：
model = T5ForConditionalGeneration.from_pretrained("t5", 
                                                   torch_dtype="auto")
```

也可以通过以下方式告知从头开始实例化的模型要使用哪种 `dtype`：

```python
config = T5Config.from_pretrained("t5")
model = AutoModel.from_config(config)
```

由于 PyTorch 的设计，此功能仅适用于浮点类型。

### 配置



## 参考资料

- B站PPT

https://github.com/zyds/transformers-code

- 快速入门

https://transformers.run/

- Transformer 手册

https://huggingface.co/docs/transformers/v4.42.0/zh
