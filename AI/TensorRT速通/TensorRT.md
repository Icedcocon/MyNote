# TensorRT基础

## 1 TensorRT 简介

### 1.1 TensorRT（最新版本 8.6.1）

- 用于高效实现已训练好的深度学习模型的推理过程的 SDK
- 内含推理优化器和运行时环境
- 使 DL 模型能以更高吞吐量和更低的延迟运行
- 有 C++ 和 python 的 API，完全等价可以混用

### 1.2 TensorRT 做的工作

- **构建期（推理优化器）**
  - **模型解析 / 建立**： 加载 Onnx 等其他格式的模型 / 使用原生 API 搭建模型
  - **计算图优化** ：横向层融合（Conv），纵向层融合（Conv+add+ReLU），……
  - **节点消除** ：去除无用层，节点变换（Pad，Slice，Concat，Shuffle），……
  - **多精度支持** ：FP32 / FP16 / INT8 / TF32（可能插入 reformat 节点）
  - **优选 kernel / format** ：硬件有关优化
  - **导入 plugin** ：实现自定义操作
  - **显存优化** ：显存池复用
- **运行期（运行时环境）**
  - **运行时环境** 对象生命期管理，内存显存管理，异常处理
  - **序列化反序列化** 推理引擎保存为文件或从文件中加载

## 2 TensorRT 基本流程

### 2.1 基本流程

- **构建期**
  - 前期准备（Logger，Builder，Config，Profile）
  - 创建 Network（计算图内容）
  - 生成序列化网络（计算图 TRT 内部表示）
- **运行期**
  - 建立 Engine 和 Context
  - Buffer 相关准备（申请+拷贝）
  - 执行推理（Execute）
  - 善后工作

### 2.2 Workflow

- (1) 使用框架自带 TRT 接口（TF-TRT，Torch-TensorRT）
- (2) 使用 Parser（TF/Torch/… → ONNX → TensorRT）
- (3) 使用 TensorRT 原生 API 搭建网络

| 方法       | 易用性 | 性能  | 兼容性 | 开发效率 | 遇到不支持的OP           |
| -------- | --- | --- | --- | ---- | ------------------ |
| 框架自带接口   | ★★★ | ★   | ★★  | ★★★  | 返回原框架计算            |
| 使用Parser | ★★  | ★★☆ | ★★☆ | ★★   | 改网/改Parser/写Plugin |
| API搭建    | ★   | ★★★ | ★★★ | ★    | 写Plugin            |

## 3 TensorRT API

### 3.1 Logger 日志记录器

要创建构建器，您需要首先创建一个记录器。 Python 绑定包括一个简单的记录器实现，它将高于特定严重性的所有消息记录到`stdout` 。

```python
logger = trt.Logger(trt.Logger.WARNING)
# int(trt.ILogger.Severity.VERBOSE) == 4
# int(trt.ILogger.Severity.INFO) == 3
# int(trt.ILogger.Severity.WARNING) == 2
# int(trt.ILogger.Severity.ERROR) == 1
# int(trt.ILogger.Severity.INTERNAL_ERROR) == 0
```

或者，可以通过从`ILogger`类派生来定义您自己的记录器实现：

```python
class MyLogger(trt.ILogger):
    def __init__(self):
        trt.ILogger.__init__(self)
    def log(self, severity, msg):
        pass # Your custom logging implementation here
logger = MyLogger()
```

然后，您可以创建一个构建器：

```python
print("构建期 Build time ---------------------------------------------")
# 在构建期将 logger 安全级别设置为 INFO
logger.min_severity = trt.ILogger.Severity.INFO  
builder = trt.Builder(logger)

print("运行期 Run time ------------------------------------------------")
# 在运行期将 logger 安全级别修改为 VERBOSE 
logger.min_severity = trt.ILogger.Severity.VERBOSE 
# 将 logger 分配给 Runtime
engine = trt.Runtime(logger).deserialize_cuda_engine(engineString)  
```

1. **trt.ILogger** ： 基类，自定义logger时可继承

2. **trt.ILogger.Severity** ：级别常亮：VERBOSE、INFO、WARNING、ERROR...

3. **logger.min_severity** ：日志级别

4. **builder = trt.Builder(logger)** ： 分配logger

5. **trt.Runtime(logger)**： 分配logger

### 3.2 Builder 引擎构建器

#### 3.2.1 创建网络定义

创建构建器后，优化模型的第一步是创建网络定义：

```python
import tensorrt as trt
# 默认 Logger ，并设置显示安全级别为 ERROR
logger = trt.Logger(trt.Logger.ERROR)
# 将 logger 分配给 Builder
builder = trt.Builder(logger)
# 将 Builder 重置为默认参数（非必须）
builder.reset()  
# 创建 TensorRT 网络对象
network = builder.create_network(1 << 
    int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
```

为了使用 ONNX 解析器导入模型，需要`EXPLICIT_BATCH`标志。

- **Explicit Batch 为 TensorRT 主流 Network 构建方法**

- 需要使用 builder.create_network(1 << int(tensorrt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))

- Implicit Batch 模式（builder.create_network(0)）仅用作后向兼容

- 所有张量显式包含 Batch 维度、**比 Implicit Batch 模式多一维**

- Explicit Batch 模式能做、Implicit Batch 模式不能做的事情：
  
  - Batch Normalization（视频教程的录音中说成了 Layer Normalization）
  
  - Reshape/Transpose/Reduce over batch dimension
  
  - Dynamic shape 模式
  
  - Loop 结构
  
  - 一些 Layer 的高级用法（如 ShufleLayer.set_input）
  
  - **从 Onnx 导入的模型也默认使用 Explicit Batch 模式**

常用方法：

```python
# 创建 TensorRT 网络对象
builder.create_network(…)
# 创建用于 Dyanmic Shape 输入的配置器
builder.create_optimization_profile()
```

#### 3.2.2 导入或构建模型

现在，需要从 ONNX 表示中填充网络定义。您可以创建一个 ONNX 解析器来填充网络，如下所示：

```python
parser = trt.OnnxParser(network, logger)
```

然后，读取模型文件并处理任何错误：

```python
success = parser.parse_from_file(model_path)
for idx in range(parser.num_errors):
    print(parser.get_error(idx))
if not success:
    pass # Error handling code here
```

或者构造网络

```python
inputTensor = network.add_input("inputT0", trt.float32, [3, 4, 5])
identityLayer = network.add_identity(inputTensor)
network.mark_output(identityLayer.get_output(0))
```

常用获取网络信息的成员：

```python
network.name
network.num_layers
network.num_inputs
network.num_outputs
network.has_implicit_batch_dimension
network.has_explicit_precision
```

常用方法：

```python
# 标记网络输入张量
network.add_input( 'oneTensor' ,trt.float32, (3,4,5))
# 添加各种网络层
convLayer = network.add_convolution_nd(XXX)
# 标记网络输出张量
network.mark_output(convLayer.get_output(0))
```

#### 3.2.3 网络属性

下一步是创建一个构建配置，指定 TensorRT 应该如何优化模型：

```python
config = builder.create_builder_config()
```

这个接口有很多属性，你可以设置这些属性来控制 TensorRT 如何优化网络。一个重要的属性是最大工作空间大小。层实现通常需要一个临时工作空间，并且此参数限制了网络中任何层可以使用的最大大小。如果提供的工作空间不足，TensorRT 可能无法找到层的实现：

```python
config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 
                             1 << 20) # 1 MiB
```

指定配置后，可以使用以下命令构建和序列化引擎：

```python
serialized_engine = builder.build_serialized_network(network, config)
```

将引擎保存到文件以供将来使用可能很有用。你可以这样做：

```python
with open(“sample.engine”, “wb”) as f:
    f.write(serialized_engine)
```

指定不同模式

- FP16 模式
  
  - 建立 engine 时间比 FP32 模式更长（更多 kernel 选择，需要插入 Reformat 节点）
  
  - Timeline 中出现 nchwToNchw 等 kernel 调用
  
  - 部分层可能精度下降导致较大误
    
    - 找到误差较大的层（用 polygraphy等工具，见教程第二部分）
    
    - 强制该层使用 FP32 进行计算

```python
config.flags = 1<<int(trt.BuilderFlag.FP16)

# 强制使用FP32
config.set_flag(trt.BuilderFlag.OBEY_PRECISION_CONSTRAINTS)
layer.precision = trt.float32
```

- Int8 模式 —— PTQ
  
  - 需要有校准集（输入范例数据）
  
  - 自己实现 calibrator

```python
config.set_flag(trt.BuilderFlag.INT8)
config.int8_calibrator = …
```

- Int8 模式 —— QAT
  
  - 在 pyTorch 网络中插入 Quantize/Dequantize 层

```python
config.set_flag(trt.BuilderFlag.INT8)
```

常用方法：

```python
# 指定构建期可用显存（单位：Byte）
config.config.set_memory_pool_limit(
    trt.MemoryPoolType.WORKSPACE, 1 << 30)
# 设置标志位开关，如启闭 FP16/INT8 模式，Refit 模式，手工数据类型限制等
config.flag = …
# 指定 INT8-PTQ 的校正器
config.int8_calibrator = …
# 添加用于 Dynamic Shape 输入的配置器
config.add_optimization_profile(…)
```

#### 3.2.4 Profile

Profile 可指定输入张量大小范围

```python
profile = builder.create_optimization_profile()
```

常用方法：

```python
# 给定输入张量的最小、最常见、最大尺寸
profile.set_shape(tensorName, minShape, commonShape, maxShape)
# 将设置的 profile 传递给 config 以创建网络
config.add_optimization_profile(profile)
```

### 3.3 进行推理

#### 3.3.1 反序列化

要执行推理，您首先需要使用Runtime接口反序列化引擎。与构建器一样，运行时需要记录器的实例。

```python
runtime = trt.Runtime(logger)
```

然后，您可以从内存缓冲区反序列化引擎：

```python
engine = runtime.deserialize_cuda_engine(serialized_engine)
```

如果您需要首先从文件加载引擎，请运行：

```python
with open(“sample.engine”, “rb”) as f:
    serialized_engine = f.read()
```

#### 3.3.2 运行期完整过程

```python
# 生成 TRT 内部表示
serializedNetwork = builder. build_serialized_network(network, config)

# 生成 Engine
engine = 
    trt.Runtime(logger).deserialize_cuda_engine(serializedNetwork)
lTensorName = 
    [engine.get_tensor_name(i) for i in range(engine.num_io_tensors)]

# 创建 Contex
context = engine.create_execution_context()

# 绑定输入输出（Dynamic Shape 模式必须）
context.set_input_shape(lTensorName[0], [3, 4, 5]) 
## TensorRT 8.5 开始 binding 系列 API 全部 deprecated，换成 tensor 系列 API

# 准备 Buffer
inputHost = np.ascontiguousarray(inputData.reshape(-1))
outputHost = np.empty(context.get_tensor_shape(iTensorName[i]), 
                    trt.nptype(engine.get_tensor_dtype(iTensorName[1])))
inputDevice = cudart.cudaMalloc(inputHost.nbytes)[1]
outputDevice = cudart.cudaMalloc(outputHost.nbytes)[1]
context.set_tensor_address(iTensorName[0], inputDevice) 
## 用到的 GPU 指针提前在这里设置，不再传入 execute_v3 函数
context.set_tensor_address(iTensorName[1], outputDevice)

# 执行计算
cudart.cudaMemcpy(inputDevice, inputHost.ctypes.data, 
                  inputHost.nbytes, 
                  cudart.cudaMemcpyKind.cudaMemcpyHostToDevice)
context.execute_async_v3(0) 
cudart.cudaMemcpy(outputHost.ctypes.data, outputDevice, 
                  outputHost.nbytes, 
                  cudart.cudaMemcpyKind.cudaMemcpyDeviceToHost)
```

#### 3.2.3 Context 推理进程

```python
context = engine.create_execution_context()
```

常用方法：

```python
# 设定第 i 个张量的形状（Dynamic Shape 模式中使用）
context. set_input_shape(iTensorName[i], shapeOfInputTensor) 
# 获取第 i 个张量的形状
context.get_tensor_shape(iTensorName[i]) 
# 设定输入输出张量的指针
context.set_tensor_address(iTensorName[i], address) 
# Explicit batch 模式的异步执行
context.execute_async_v3(srteam) 
```
