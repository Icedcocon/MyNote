```bash
#! /bin/bash

ST=$(date +%s)

[ -e /tmp/fd1 ] || mkfifo /tmp/fd1 # 创建有名管道
exec 5<>/tmp/fd1 # 创建文件描述符，以可读（<）可写（>）的方式关联管道文件，文件描述符5拥有有名管道文件的所有特性
rm -rf /tmp/fd1 # 文件描述符关联后拥有管道的所有特性，所有删除管道
NUM=$1 # 获取输入的并发数

for (( i=1;i<=${NUM};i++ ))
do
  echo >&5 # &5表示引用文件描述符5，往里面放置一个令牌
done

for i in $(seq 1 100)
do
  read -u 5
  {
    echo $i
    sleep 1 # 模拟程序、命令
    echo >&5 # 执行完把令牌放回管道
  }& # 把循环体放入后台运行，相当于是起一个独立的线程，在此处的作用就是相当于起来10个并发
done
wait # wait命令的意思是，等待（wait命令）上面的命令（放入后台的）都执行完毕了再往下执行，通常可以和&搭配使用

ET=$(date +%s)
TIME=$(( ${ET} - ${ST} ))
echo "time: ${TIME}"
```


