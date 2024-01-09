# 分布式推理基本操作-MPI-TRT

## 一、快速开始

### 1. 配置环境

- 在没有多节点的测试环境下，可使用 docker 容器代替
1. **创建网络**

```bash
docker  network  create --subnet=192.168.123.0/24 network_my
```

2. **创建容器**

```bash
docker run -d --name node1 --net network_my -h node1 \
           --ip 192.168.123.111 \
           --add-host node2:192.168.123.112 \
           --gpus "device=1" \
           -v /mnt/inaisfs/fry/TRTDir:/TRTDir \
           tensorrt_llm/release:latest sleep 8640000
docker run -d --name node2 --net network_my -h node2 \
           --ip 192.168.123.112 \
           --add-host node1:192.168.123.111 \
           --gpus "device=2" \
           -v /mnt/inaisfs/fry/TRTDir:/TRTDir \
           tensorrt_llm/release:latest sleep 8640000
```

3. **配置 ssh 及免密**

```bash
apt update 
apt install ssh 
mkdir /var/run/sshd 
echo "root:123456" |chpasswd 
nohup /usr/sbin/sshd -D &>/dev/null &

root@node1$: ssh-keygen -b 1024 -t rsa
root@node1$: ssh-copy-id node2
root@node2$: ssh-keygen -b 1024 -t rsa
root@node2$: ssh-copy-id node1
```

4. **编写 mpi 测试脚本 mpi-hello.py**
   
   - 注意：脚本需放在两容器共享存储下，或相同位置存在副本

```python
from mpi4py import MPI
import sys

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
name = MPI.Get_processor_name()

print(f"Hello, World! I am process {rank} of {size} on {name}.")
```

5. **执行测试**
   
   - `--allow-run-as-root` ：以root用户执行`mpirun`时需指定
   
   - `--host` ：格式 `${节点IP}:节点可并行服务数`
   
   - `-np/-n` ： 脚本需并行数

```bash
mpirun --allow-run-as-root 
       --host node2:2 
       --host node1:2  
       -np 4 
       python3 /TRTDir/mpi-demo/mpi-hello.py
```

### 2. 分布式推理

1. **编译 tensorrl-llm engine**
   
   - 此处采用 mpirun 并行编译报错，建议单机多卡时采用本地并行编译
   
   - `--model_name` ：指定模型名称，在 rel 分支中所有chatglm模型采用一个build.py，所以需要指定 `chatglm1_6b` 、 `chatglm2_6b` 、 `chatglm3_6b`
   
   - `--model_dir` ：HuggingFace 模型路径
   
   - `---output_dir` ： 引擎输出路径
   
   - `--tp_size` ： 张量并行数
   
   - `--world_size` ： 总并行数 = 张量并行数 x 流水线并行数
   
   - `--gpus_per_node` ： 每节点GPU数，默认为8（似乎不影响run.py引起bug）

```bash
mpirun --allow-run-as-root --host node1:1  -np 1 \
python3 /app/tensorrt_llm/examples/chatglm/build.py \
       --model_name=chatglm2_6b \
       --model_dir=/TRTDir/Models/chatglm2-6b \
       --output_dir=/TRTDir/engines/chatglm2-6b-float16 \
       --tp_size=2 --world_size=2  \
       --gpus_per_node=1
```

2. **分布式推理**
   
   - 出现错误 `RuntimeError: CUDA error: invalid device ordinal`  操作：
     
     - `vim /usr/local/lib/python3.10/dist-packages/tensorrt_llm/runtime/model_runner.py`
     
     - 并在 408 行前添加 `runtime_mapping.gpus_per_node=1`
   
   - `--engine_dir` ：编译的 engine 的路径
   
   - `--tokenizer_dir` ：HuggingFace 模型路径（也包含tokenizer）
   
   - `--input_text` ： 输入提示词
   
   - `--max_output_len` ： 最大输出 token ，决定输出多少字

```bash
mpirun --allow-run-as-root  --host node2:1 --host node1:1 -np 2 \
python3 /app/tensorrt_llm/examples/run.py \
       --engine_dir /TRTDir/engines/chatglm2-6b-int8 \
       --tokenizer_dir=/TRTDir/Models/chatglm2-6b \
       --input_text="Hello tell me about huawei" \
       --max_output_len=1000
```
