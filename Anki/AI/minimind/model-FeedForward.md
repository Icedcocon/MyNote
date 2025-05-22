### 1. FeedForward

#### 1.0 前馈网络

**前馈网络的作用**

1. **特征变换** - 在注意力层后进行非线性特征变换，增强模型表达能力

2. **信息整合** - 将注意力机制提取的信息进行整合和增强

3. **维度映射** - 通过先扩展维度再压缩回原始维度，实现信息的有效处理

#### 1.1 代码

```python
class FeedForward(nn.Module):
    def __init__(self, config: LMConfig):
        super().__init__()
        if config.hidden_dim is None:
            hidden_dim = 4 * config.dim
            hidden_dim = int(2 * hidden_dim / 3)
            config.hidden_dim = config.multiple_of * ((hidden_dim + config.multiple_of - 1) // config.multiple_of)
        self.w1 = nn.Linear(config.dim, config.hidden_dim, bias=False)
        self.w2 = nn.Linear(config.hidden_dim, config.dim, bias=False)
        self.w3 = nn.Linear(config.dim, config.hidden_dim, bias=False)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x):
        # x: [batch_size, seq_len, dim] -> w1(x): [batch_size, seq_len, hidden_dim]
        # w3(x): [batch_size, seq_len, hidden_dim]
        # SiLU激活与门控乘积后: [batch_size, seq_len, hidden_dim]  
        # w2输出: [batch_size, seq_len, dim]
        return self.dropout(self.w2(F.silu(self.w1(x)) * self.w3(x)))
```

#### 1.2 分析

##### 定义
FeedForward（前馈网络）是大型语言模型中的关键组件，位于Transformer架构中的每个层中。它是一个位置级（position-wise）前馈网络，在注意力机制之后应用，用于处理每个位置的特征表示。这个模块实现了基于SwiGLU（Swish Gated Linear Unit）的变体，是对标准前馈网络（FFN）的改进。

##### FeedForward初始化参数详解

在`__init__()`函数中，定义了前馈网络所需的关键组件和参数：

1. **维度相关参数**：
   - `config.dim`：模型的隐藏维度大小，通常为768、1024、2048等，表示输入向量的维度。
   - `config.hidden_dim`：前馈网络的中间维度，通常是输入维度的4倍左右，表示内部特征的维度。
   - `config.multiple_of`：确保hidden_dim是特定值的倍数（通常为8或16），有利于硬件加速。

2. **中间维度计算**：
   如果未指定`hidden_dim`，则使用一个启发式公式计算:
   - 首先设置为输入维度的4倍: `hidden_dim = 4 * config.dim`
   - 然后缩减到原来的2/3: `hidden_dim = int(2 * hidden_dim / 3)`，相当于约2.67倍输入维度
   - 最后调整为`multiple_of`的倍数

3. **网络层和激活函数**：
   - `self.w1`：第一个线性投影，从`dim`映射到`hidden_dim`，不使用偏置项
   - `self.w2`：第二个线性投影，从`hidden_dim`映射回`dim`，不使用偏置项
   - `self.w3`：第三个线性投影，用于门控机制，从`dim`映射到`hidden_dim`，不使用偏置项
   - `F.silu`：SiLU (Swish) 激活函数，形式为 $f(x) = x \cdot \sigma(x)$
   - `self.dropout`：丢弃层，应用于最终输出以防止过拟合

所有线性层都设置`bias=False`，这是大型语言模型中常见的简化设计，可以减少参数量而不显著影响性能。

##### 公式
给定输入向量 $x \in \mathbb{R}^{d}$，SwiGLU风格的FeedForward计算公式为：

$$\text{FFN}(x) = \text{Dropout}(W_2(\text{SiLU}(W_1x) \odot W_3x))$$

其中：
- $W_1, W_3 \in \mathbb{R}^{h \times d}$ 是将输入从维度 $d$ 映射到隐藏维度 $h$ 的权重矩阵
- $W_2 \in \mathbb{R}^{d \times h}$ 是将隐藏表示映射回原始维度 $d$ 的权重矩阵
- $\text{SiLU}(x) = x \cdot \sigma(x)$ 是Sigmoid Linear Unit激活函数，其中 $\sigma$ 是sigmoid函数
- $\odot$ 表示逐元素相乘（Hadamard积）
- Dropout应用在最终输出上，提供正则化效果

##### 计算步骤详解

1. **线性投影与特征扩展**：
   对输入进行两个并行的线性变换，将维度从原始模型维度扩展到更大的隐藏维度。
   
   $$h_1 = W_1 x, \quad h_3 = W_3 x$$
   
   维度变化：
   - $x: [b \times n \times d]$，其中 $b$ 是批次大小，$n$ 是序列长度，$d$ 是模型维度
   - $W_1, W_3: [h \times d]$，其中 $h$ 是隐藏维度，通常 $h \approx 2.67d$
   - $h_1, h_3: [b \times n \times h]$，扩展到更大的表示空间

   代码实现：
   ```python
   # 线性投影，得到维度为：
   # x: [batch_size, seq_len, dim] -> [batch_size, seq_len, hidden_dim]
   h1 = self.w1(x)
   h3 = self.w3(x)
   ```

2. **SiLU激活与门控机制**：
   应用SiLU(Swish)激活函数到第一个线性变换的输出，并与第二个线性变换的输出进行逐元素相乘。
   
   $$h_{act} = \text{SiLU}(h_1) \odot h_3 = (h_1 \cdot \sigma(h_1)) \odot h_3$$
   
   其中：
   - $\text{SiLU}(x) = x \cdot \sigma(x)$ 是Sigmoid Linear Unit激活函数
   - $\sigma(x) = \frac{1}{1+e^{-x}}$ 是sigmoid函数
   - $\odot$ 表示逐元素乘法
   
   该步骤维度保持不变：$h_{act}: [b \times n \times h]$

   代码实现：
   ```python
   # SiLU激活函数：x * sigmoid(x)
   # h1: [batch_size, seq_len, hidden_dim] -> activated: [batch_size, seq_len, hidden_dim]
   activated = F.silu(h1)  # 相当于 h1 * torch.sigmoid(h1)
   
   # 与门控路径相乘（Hadamard积）
   # activated: [batch_size, seq_len, hidden_dim], h3: [batch_size, seq_len, hidden_dim]
   # 结果: [batch_size, seq_len, hidden_dim]
   gated = activated * h3
   ```

3. **维度下降与输出投影**：
   将门控后的特征通过最后一个线性层映射回原始模型维度。
   
   $$\text{output} = W_2 h_{act}$$
   
   维度变化：
   - $h_{act}: [b \times n \times h]$
   - $W_2: [d \times h]$
   - $\text{output}: [b \times n \times d]$，恢复到原始模型维度

   代码实现：
   ```python
   # 输出投影，从扩展的维度映射回原始维度
   # gated: [batch_size, seq_len, hidden_dim] -> output: [batch_size, seq_len, dim]
   output = self.w2(gated)
   ```

4. **Dropout正则化**：
   最后应用dropout来防止过拟合。
   
   $$\text{final\_output} = \text{Dropout}(\text{output})$$
   
   维度保持不变：$\text{final\_output}: [b \times n \times d]$

   代码实现：
   ```python
   # 应用dropout正则化
   # output: [batch_size, seq_len, dim] -> final_output: [batch_size, seq_len, dim]
   final_output = self.dropout(output)
   ```

完整的前向传播可以写为：
```python
def forward(self, x):
    h1 = self.w1(x)          # [batch, seq_len, hidden_dim]
    h3 = self.w3(x)          # [batch, seq_len, hidden_dim]
    activated = F.silu(h1)   # [batch, seq_len, hidden_dim]
    gated = activated * h3   # [batch, seq_len, hidden_dim]
    output = self.w2(gated)  # [batch, seq_len, dim]
    return self.dropout(output)
```

在实际代码中，为了效率，这些步骤被合并为一行：
```python
return self.dropout(self.w2(F.silu(self.w1(x)) * self.w3(x)))
```

##### 原理
这种FeedForward实现使用了门控机制，通过SiLU（也称为Swish）激活函数和另一个线性投影的乘积来控制信息流。这种设计相比于传统的使用ReLU激活函数的两层前馈网络，在性能上有显著提升。

具体来说：
1. 两个并行的线性变换 $W_1$ 和 $W_3$ 将输入映射到高维空间
2. 对第一个分支应用SiLU激活函数，作为"门控"机制
3. 两个分支相乘，实现特征选择与变换
4. 最后通过 $W_2$ 线性变换将结果映射回原始维度
5. 应用Dropout进行正则化

##### 作用

1. **特征变换**：通过非线性变换增强模型的表达能力
2. **维度扩展**：通过扩展到更高维的隐藏状态，捕获更丰富的特征表示
3. **信息过滤**：门控机制帮助模型选择性地保留和强调重要特征
4. **降低过拟合**：Dropout机制减少模型对训练数据的过度拟合
5. **参数效率**：相比传统FFN，这种设计在相同参数量下通常能获得更好的性能

#### 1.3 延伸

##### 1.3.1 其他FFN变体

1. **标准FFN**：
   使用ReLU激活函数的简单两层前馈网络。
   ```python
   def forward(self, x):
       # x: [batch_size, seq_len, dim] -> [batch_size, seq_len, hidden_dim] -> [batch_size, seq_len, dim]
       return self.dropout(self.w2(F.relu(self.w1(x))))
   ```
   
2. **GEGLU (Gated GLU)**：
   使用GELU激活函数的门控变体，将隐藏表示分成两半，一半用于变换，一半用于门控。
   ```python
   def forward(self, x):
       # x: [batch_size, seq_len, dim] -> hidden: [batch_size, seq_len, 2*hidden_dim]
       hidden = self.w1(x)
       # 将隐藏状态分成两半: chunks[0], chunks[1]: [batch_size, seq_len, hidden_dim]
       chunks = hidden.chunk(2, dim=-1)
       # 应用GELU激活和门控乘法: [batch_size, seq_len, hidden_dim]
       return self.dropout(self.w2(F.gelu(chunks[0]) * chunks[1]))
   ```
   
3. **ReGLU**：
   使用ReLU激活函数的门控线性单元变体。
   ```python
   def forward(self, x):
       # x: [batch_size, seq_len, dim] -> hidden: [batch_size, seq_len, 2*hidden_dim]
       hidden = self.w1(x)
       # 将隐藏状态分成两半: chunks[0], chunks[1]: [batch_size, seq_len, hidden_dim]
       chunks = hidden.chunk(2, dim=-1)
       # 应用ReLU激活和门控乘法: [batch_size, seq_len, hidden_dim]
       return self.dropout(self.w2(F.relu(chunks[0]) * chunks[1]))
   ```

4. **MOE (Mixture of Experts)**：
   使用多个"专家"网络（通常是前馈网络）的混合，由门控机制选择激活特定专家。
   ```python
   class MOEFeedForward(nn.Module):
       def forward(self, x):
           # 1. 使用门控网络选择专家
           # topk_idx: 每个token选用的专家索引, topk_weight: 对应权重
           topk_idx, topk_weight, aux_loss = self.gate(x)
           
           # 2. 根据专家索引，分配输入到不同专家并收集输出
           outputs = []
           for i, expert in enumerate(self.experts):
               # 为每个专家选择对应的输入子集
               mask = (topk_idx == i)
               if mask.any():
                   # 仅处理分配给当前专家的token
                   expert_output = expert(x[mask])
                   outputs.append((mask, expert_output))
           
           # 3. 合并所有专家的输出，按原始顺序重组
           y = torch.zeros_like(x)
           for mask, expert_output in outputs:
               y[mask] = expert_output
               
           # 4. 可选：添加共享专家的输出
           if hasattr(self, 'shared_expert'):
               y = y + self.shared_expert(x)
               
           return y
   ```
   
   **MOE前馈网络的优势**：
   1. **计算效率**：只激活部分专家网络，减少推理和训练的计算量
   2. **参数效率**：以较小的推理计算成本增加模型容量
   3. **任务适应性**：不同专家可以处理不同类型的输入或任务
   4. **扩展性**：易于扩展到更大规模的模型，通过增加专家数量而不是整体宽度

##### 1.3.2 在模型中的集成

```python
class MiniMindBlock(nn.Module):
    def __init__(self, layer_id: int, config: LMConfig):
        super().__init__()
        self.attention = Attention(config)
        self.attention_norm = RMSNorm(config.dim, eps=config.norm_eps)
        self.ffn_norm = RMSNorm(config.dim, eps=config.norm_eps)
        self.feed_forward = FeedForward(config) if not config.use_moe else MOEFeedForward(config)

    def forward(self, x, pos_cis, past_key_value=None, use_cache=False):
        h_attn, past_kv = self.attention(
            self.attention_norm(x),
            pos_cis,
            past_key_value=past_key_value,
            use_cache=use_cache
        )
        h = x + h_attn
        out = h + self.feed_forward(self.ffn_norm(h))
        return out, past_kv
```

FeedForward模块在Transformer架构中通常与注意力层一起构成基本的处理单元，并采用了残差连接和层归一化来确保梯度流动和训练稳定性。


