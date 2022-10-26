```yaml
# 内容
'1. Collections': 
  - List
  - Dictionary
  - Set
  - Tuple
  - Range
  - Enumerate
  - Iterator
  - Generator
'2. Types':
  - Type
  - String
  - Regular_Exp
  - Format, Numbers
  - Combinatorics
  - Datetime
'3. Syntax':
  - Args, Inline
  - Import
  - Decorator
  - Class
  - Duck_Types
  - Enum, Exception
'4. System':
  - Exit
  - Print
  - Input
  - Command_Line_Arguments
  - Open
  - Path
  - OS_Commands
'5. Data':
  - JSON
  - Pickle
  - CSV
  - SQLite
  - Bytes
  - Struct
  - Array
  - Memory_View
  - Deque
'6. Advanced':
  - Threading
  - Operator
  - Introspection
  - Metaprograming
  - Eval
  - Coroutine
'7. Libraries':
  - Progress_Bar
  - Plot
  - Table
  - Curses
  - Logging
  - Scraping
  - Web
  - Profile
  - NumPy
  - Image
  - Audio
  - Games
  - Data
```

```python
#######################################################################
# 4. System
#######################################################################

# 4.1 Exit
# 通过引发SystemExit异常退出Python解释器。
import sys
sys.exit()                        # 退出 退出码为0 (success).
sys.exit(<el>)                    # 打印到stderr 并退出 退出码为1.
sys.exit(<int>)                   # 退出并指定退出码

# 4.6 Paths
from os import getcwd, path, listdir, scandir
from glob import glob
<str>  = getcwd()                   # 返回当前工作路径
<str>  = path.join(<path>, ...)     # 连接多个路径名组件
<str>  = path.abspath(<path>)       # 返回绝对路径名
<str>  = path.basename(<path>)      # 返回文件名
<str>  = path.dirname(<path>)       # 返回文件路径
<tup.> = path.split(<path>)            # (<dirname>,<basename>)
<tup.> = path.splitext(<path>)      # 分离扩展名(<pathname>,<ext>) .txt的扩展名为空
<list> = listdir(path='.')          # 列出path下的文件list
<list> = glob('<pattern>')          # 返回匹配的文件list
<bool> = path.exists(<path>)        # 或: <Path>.exists()
<bool> = path.isfile(<path>)        # 或: <DirEntry/Path>.is_file()
<bool> = path.isdir(<path>)         # 或: <DirEntry/Path>.is_dir()
<stat> = os.stat(<path>)            # 或: <DirEntry/Path>.stat()
<real> = <stat>.st_mtime/st_size/...# 修改时间, 大小(bytes), …
# 与listdir()不同，scandir()返回DirEntry对象
# DirEntry对象缓存isfile、isdir和Windows上的stat信息，提高性能。
<iter> = scandir(path='.')          # 返回指定path的DirEntry objects对象
<str>  = <DirEntry>.path            # 返回完整路径
<str>  = <DirEntry>.name            # 返回文件名
<file> = open(<DirEntry>)           # 打开并返回文件对象.

# Path Object
from pathlib import Path
<Path> = Path(<path> [, ...])       # 可以是strings,Paths或DirEntry对象
<Path> = <path> / <path> [/ ...]    # First or second path must be a Path object.
<Path> = Path()                     # Returns relative cwd. Also Path('.').
<Path> = Path.cwd()                 # Returns absolute cwd. Also Path().resolve().
<Path> = Path.home()                # Returns user's home directory (absolute).
<Path> = Path(__file__).resolve()   # Returns script's path if cwd wasn't changed.
<Path> = <Path>.parent              # Returns Path without the final component.
<str>  = <Path>.name                # Returns final component as a string.
<str>  = <Path>.stem                # Returns final component without extension.
<str>  = <Path>.suffix              # Returns final component's extension.
<tup.> = <Path>.parts               # Returns all components as strings.
<iter> = <Path>.iterdir()           # Returns directory contents as Path objects.
<iter> = <Path>.glob('<pattern>')   # Returns Paths matching the wildcard pattern.
<str>  = str(<Path>)                # Returns path as a string.
<file> = open(<Path>)               # Also <Path>.read/write_text/bytes().

# 4.7 OS 命令
import os, shutil, subprocess
os.chdir(<path>)                # 修改当前工作路径
os.mkdir(<path>, mode=0o777)    # 创建文件夹;八进制权限;目录存在抛OSerror
os.makedirs(<path>, mode=0o777) # 递归创建目录，`exist_ok=False` 存在报错
shutil.copy(from, to)           # 复制文件 'to' 是存在的文件或目录
shutil.copytree(from, to)       # 递归复制 'to' 必须不存在
os.rename(from, to)             # 重命名/移动文件或目录
os.replace(from, to)            # 同上，但'to'存在会被覆盖
os.remove(<path>)               # 删除文件
os.rmdir(<path>)                # 删除空目录
shutil.rmtree(<path>)           # 递归删除目录
# <path>可以使 strings, Paths 或者 DirEntry objects
# 上述函数抛出错误为 OSError 或其子类

<pipe> = os.popen('<command>')  # 在sh或cmd中执行指令;返回stdout pipe
<str>  = <pipe>.read(size=-1)   # 读取'size'字节或到EOF;似readline/s()
<int>  = <pipe>.close()         # 关闭pipe;成功返回None
# 用bc计算'1 + 1'并捕输出:
subprocess.run('bc', input='1 + 1\n', capture_output=True, text=True)
# > CompletedProcess(args='bc', returncode=0, stdout='2\n', stderr='')
# 将test.in中内容发送给bc (-s 标准模式)，将输出保存在test.out:
from shlex import split
os.popen('echo 1 + 1 > test.in')
subprocess.run(split('bc -s'), stdin=open('test.in'), \
stdout=open('test.out', 'w'))
# > CompletedProcess(args=['bc', '-s'], returncode=0)
open('test.out').read()
# > '2\n'
```

```python
#######################################################################
# 5. Data
#######################################################################


# 5.2 yaml
```
