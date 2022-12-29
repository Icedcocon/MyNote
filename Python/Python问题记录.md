# Python问题记录

### 非阻塞IO

##### 问题描述

- 在项目中与shell进程交互，通过匿名管道收发数据，进程不终止则`stdout`管道保持打开，这导致尝试读取该管道的函数(如readline)挂起，直到出现新数据

- shell.py

```python
# 虚拟Shell进程，总是接受输入并返回到stdout，保持等待输入永不结束
import sys
while True:
    s = raw_input("Enter command: ")
    print "You entered: {}".format(s)
    sys.stdout.flush()
```

- client.py

```python
# 演示如何与子进程交互
from subprocess import Popen, PIPE
from time import sleep

# run the shell as a subprocess:
p = Popen(['python', 'shell.py'],
        stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)
# issue command:
p.stdin.write('command\n')
# let the shell output the result:
sleep(0.1)
# get the output
while True:
    output = p.stdout.read() # <-- Hangs here!
    if not output:
        print '[No more data]'
        break
    print output
```

##### 问题原因

- 除非将管道的O_NONBLOCK标志清除，否则Python中的read()函数将保持阻塞读取

- 

##### 解决思路

- 思路1：C语言中使用`fcntl.h`库设置O_NONBLOCK文件描述符的标志位，在Python中为fcntl模块

```python
from subprocess import Popen, PIPE
from time import sleep
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read

# run the shell as a subprocess:
p = Popen(['python', 'shell.py'],
        stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)
# set the O_NONBLOCK flag of p.stdout file descriptor:
flags = fcntl(p.stdout, F_GETFL) # get current p.stdout flags
fcntl(p.stdout, F_SETFL, flags | O_NONBLOCK)
# issue command:
p.stdin.write('command\n')
# let the shell output the result:
sleep(0.1)
# get the output
while True:
    try:
        print read(p.stdout.fileno(), 1024)
    except OSError:
        # the os throws an exception if there is no data
        print '[No more data]'
        break
```

- 思路2：开辟新线程进行读写操作（可被阻塞）
  
  - `nbstreamreader.py`:
    
    ```python
        from threading import Thread
    from Queue import Queue, Empty
    
    class NonBlockingStreamReader:
    
        def __init__(self, stream):
            '''
            stream: the stream to read from.
                    Usually a process' stdout or stderr.
            '''
    
            self._s = stream
            self._q = Queue()
    
            def _populateQueue(stream, queue):
                '''
                Collect lines from 'stream' and put them in 'quque'.
                '''
    
                while True:
                    line = stream.readline()
                    if line:
                        queue.put(line)
                    else:
                        raise UnexpectedEndOfStream
    
            self._t = Thread(target = _populateQueue,
                    args = (self._s, self._q))
            self._t.daemon = True
            self._t.start() #start collecting lines from the stream
    
        def readline(self, timeout = None):
            try:
                return self._q.get(block = timeout is not None,
                        timeout = timeout)
            except Empty:
                return None
    
    class UnexpectedEndOfStream(Exception): pass
    ```
  
  - `nbstreamreader.py`:
    
    ```python
    from subprocess import Popen, PIPE
    from time import sleep
    from nbstreamreader import NonBlockingStreamReader as NBSR
    
    # run the shell as a subprocess:
    p = Popen(['python', 'shell.py'],
            stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = False)
    # wrap p.stdout with a NonBlockingStreamReader object:
    nbsr = NBSR(p.stdout)
    # issue command:
    p.stdin.write('command\n')
    # get the output
    while True:
        output = nbsr.readline(0.1)
        # 0.1 secs to let the shell output the result
        if not output:
            print '[No more data]'
            break
        print output
    ```

##### 参考资料

http://eyalarubas.com/python-subproc-nonblock.html
