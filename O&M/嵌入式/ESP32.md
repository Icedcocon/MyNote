# ESP32基础

## 1 开发环境搭建

### 1.1 PlatformIO

```bash
# conda 创建环境
conda create -n esp32 python=3.10
# 激活环境
conda activate esp32
# 安装 platformio
python -m pip install -U platformio
# 查询 esp32 有哪些 boards
pio boards esp32
# 初始化项目并安装依赖
pio project init --board esp32-c3-devkitm-1
```

### 1.2 乐鑫

#### 离线安装

- 下载5.1 IDF `https://dl.espressif.com/dl/esp-idf/?idf=5.1`

- 在VSCode中按`F1`选择configure ESP-IDF 完成配置导入

- 缺少`pip` 则下载并在对应路径执行`wget https://bootstrap.pypa.io/get-pip.py`

- 按下`F1`选择 ESP-IDF show examples并创建新示例

- 修改 

```json
// ./vscode/settings.json
{
    "cmake.cmakePath": "C:/Program Files/CMake/v3.18.3/bin/cmake.exe",
    "cmake.generator": "Visual Studio 16 2019",
}
```

### 1.3 Linux开发环境

https://zhuanlan.zhihu.com/p/604060721

https://zhuanlan.zhihu.com/p/399366057

## 2 配置

### 2.1 .vscode配置

#### 2.1.1 c_cpp_properties.json

- 在`configurations.compileCommands`中配置交叉编译环境(InteliSense)，添加
  
  - `"compileCommands": "${workspaceFolder}/build/compile_commands.json"`

```json
{
    "configurations": [
        {
            "name": "ESP-IDF",
            "compilerPath": "${config:idf.toolsPath}\\tools\\xtensa-esp32s2-elf\\esp-12.2.0_20230208\\xtensa-esp32s2-elf\\bin\\xtensa-esp32s2-elf-gcc.exe",
            "includePath": [...],
            "browse": {
                "path": [...],
                "limitSymbolsToIncludedHeaders": false
            },
            "compileCommands": "${workspaceFolder}/build/compile_commands.json"
        }
    ],
    "version": 4
}
```

## Ref

[MacOS下VScode安装PlatformIO Core卡死和新建项目速度慢的解决方法_vscode安装platformio很慢_SimonLiu009的博客-CSDN博客](https://blog.csdn.net/toopoo/article/details/126690401)

[Windows 平台工具链的标准设置 - ESP32 - &mdash; ESP-IDF 编程指南 latest 文档](https://docs.espressif.com/projects/esp-idf/zh_CN/latest/esp32/get-started/windows-setup.html)
