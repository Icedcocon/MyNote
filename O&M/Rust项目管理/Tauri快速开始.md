# Tauri 快速开始

## 一、项目准备

### 1、 安装 rust 和 npm

#### 1.1 Windows安装 rustc、cargo、rustup等

- 下载安装包
  
  `https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe` 

- 配置代理，并开始安装

#### 1.2 Windows安装 nvm

略

### 2. 初始化项目（废弃）

#### 2.1 npm 安装 tauri-cli

##### 2.1.1 全局安装

- 安装位置：全局安装的包通常会被放置在Node.js的全局node_modules目录中。具体位置取决于你的操作系统和Node.js的安装方式。常见的路径有：

- Linux/macOS：/usr/local/lib/node_modules

- Windows：C:\Users\<你的用户名>\AppData\Roaming\npm\node_modules

```bash
npm install -g @tauri-apps/cli
```

##### 2.1.2 项目中安装

- Tauri CLI被本地安装在项目的node_modules中，你可以使用npx来运行它

```bash
npm install @tauri-apps/cli --save-dev
```

- npx 是Node.js的一个命令行工具，随Node.js的包管理器npm一起安装。它的主要功能是简化使用本地或远程npm包的命令行工具。

- npx 的主要功能：
  
  - 运行本地安装的包：当你在项目中本地安装了一个npm包（例如，安装在node_modules目录中），你可以使用npx来运行这个包的可执行文件，而不需要在全局安装它。
  
  - 运行未安装的包：npx 允许你直接运行未安装的npm包。它会临时下载并执行这个包，然后删除它。

#### 2.2 创建一个新的Tauri项目

- 创建一个新的前端项目（例如，使用React、Vue或Svelte）。

这里以React为例：

```bash
npx create-react-app my-tauri-app
cd my-tauri-app
```

- 11

```bash
npx tauri init
```

### 2. 初始化tauri项目

#### 2.1 项目文件创建

- 下载命令工具（可省略）

```bash
npm install -g create-tauri-app
create-tauri-app
```

- 不下载，由npx下载临时指令程序后执行，并在完成后删除

```bash
npx create-tauri-app
```

#### 2.2 项目编译并运行

- 安装依赖

```bash
cd tauri-app
npm install
```

- 编译并运行（安卓）

```bash
npm run tauri android init
npm run tauri android dev
```

- 编译并运行（桌面）

```bash
npm run tauri init
npm run tauri dev
```

### 3. 准备安卓开发环境

#### 3.1 Android SDK 组件

- Android 操作系统的 API 和库
  
  Android SDK 包含 Android 操作系统的 API 和库。这些 API 和库提供访问 Android 系统功能的途径，例如用户界面、网络、存储和位置。

- 编译器和工具链
  
  Android SDK 包含用于编译 Android 应用程序的编译器和工具链。这些工具可将您的代码转换为可以在 Android 设备上运行的二进制文件。

- 模拟器和设备驱动程序
  
  Android SDK 包含用于在模拟器或真实设备上运行 Android 应用程序的模拟器和设备驱动程序。模拟器可让您在没有实际设备的情况下测试您的应用程序。

- 测试框架

#### 3.2 安装SDK

##### 3.2.1 安装 Android studio

- 地址： https://developer.android.com/studio?hl=zh-cn
- 配置环境变量

##### 3.2.2 安装 Android SDK

- 通过 AS 安装说明地址： [命令行工具 &nbsp;|&nbsp; Android Studio &nbsp;|&nbsp; Android Developers](https://developer.android.com/tools?hl=zh-cn)

##### 3.2.3 配置开发者模式

在 Win11 设置中开启开发者模式

## 参考资料
