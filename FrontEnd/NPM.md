# NPM

### 基础概念

##### NPM是什么

- NPM (Node Package Manager)
  
  - node.js 的包管理器
    
    - 重复的框架代码被称作`包(package)`或者`模块(module)`
    
    - 一个包可以是文件夹里的几个文件，含一个叫 `package.json`的文件
  
  - 用于node插件管理（包括安装、卸载、管理依赖等） 
  
  - 随同 node.js 一起安装

- 常见的使用场景有以下几种：
  
  - 允许用户从 npm 服务器下载别人编写的第三方包到本地使用。
  
  - 允许用户从 npm 服务器下载并安装别人编写的命令行程序到本地使用。
  
  - 允许用户将自己编写的包或命令行程序上传到 npm 服务器供别人使用。

##### NPM安装

```bash
# 可以通过NVM安装吗？
# 创建目录
mkdir /usr/local/node/
cd /usr/local/node/
# 下载
wget https://npm.taobao.org/mirrors/node/v14.17.6/node-v14.17.6-linux-x64.tar.gz
# 解压安装包
tar -zxvf node-v14.17.6-linux-x64.tar.gz
# 移除安装包并建立符号链接
rm -rf node-v14.17.6-linux-x64.tar.gz
ln -s /usr/local/node/node-v14.17.6-linux-x64/bin/npm /usr/local/bin/npm
ln -s /usr/local/node/node-v14.17.6-linux-x64/bin/node /usr/local/bin/node
# 检查版本
npm -v
```

### NPM操作

##### 配置操作

```bash
npm config ls                           # npm配置信息
npm config set prefix "complete_path"   # 修改npm的全局安装路径（添加环境变量）
npm config set cache "complete_path"    # 修改npm的缓存路径
npm config get prefix                   # 查看npm的全局安装路径
npm config get cache                    # 查看npm的缓存路径
npm config set registry http://registry.npm.taobao.org/
                                        # 修改npm远程仓库地址为淘宝镜像
                                        # 布自己的镜像需要修改回来
npm cache clean                         # 清除npm的缓存（版本7及以上不需要）
npm prune                               # 清除项目中没有被使用的包
```

##### npm包管理文件

- `package.json`
  
  - package.json是npm依赖包管理文件，用于定义项目所需的各种第三方前端依赖包，以及项目的各种配置信息（如名称、版本、描述、作者、许可证等等），类似于maven的pom.xml文件。
  
  - 在package.json文件目录终端执行npm install时，npm会自动下载package.json里面定义的各种第三方依赖包，放在当前目录的node_modules目录内部。

- `package-lock.json`
  
  - package-lock.json文件是在执行npm install命令时生成的文件，内部记录了当前状态下载安装package.json文件内部所有依赖包的版本号，下次执行npm install时重用package-lock.json文件保存的版本号。
  
  - 所以package-lock.json文件的作用就是锁定package.json依赖包的版本号，防止在不同时间执行npm install时下载安装的依赖包版本不一致，导致项目运行出现意料之外的问题。
  
  - 所以package-lock.json文件也需要上传到代码管理器，如git。

```bash
"dependencies": {
 "@types/node": "^8.0.33",
}
# 例如这里面的上标号^是定义了向后（新）兼容依赖
# 指如果types/node的版本是超过8.0.33，并在大版本号（8）上相同，就允许下载最新版本
# 的 types/node库包，例如实际上可能运行npm install时候下载的具体版本是8.0.35。
```

##### 运行命令

- `npm init` 初始化项目，其实就是创建一个`package.json`文件。
- `npm install` 安装所有项目依赖。
- `npm help xxx` 查看`xxx`命令的帮助信息。

### `npm search` 搜索（快捷方式：`find`, `s`）

- `xxx` 搜索`xxx` 如：`npm search jquery`。

### `npm install` 安装 （快捷方式：`i`）

- `xxx` 搜索并安装xxx（局部）。安装多个依赖可用空格分割，如`npm i jquery bootstrap`。
- `xxx -g` 搜索并安装xxx（全局）。安装多个同上。
- `xxx -D` 安装并将依赖信息写在`package.json`中的`devDependencies`中。
- 快捷方式 `i`均可，如`npm i jquery`。
- `xxx@版本号` 指定需要安装的版本号，若不指定将安装最新的稳定版本。

### `npm uninstall` 卸载（快捷方式：`rm`, `r`）

- `xxx` 卸载xxx。多个依赖可用空格分割。
- `xxx -D` 卸载xxx，并将依赖信息从`package.json`中的`devDependencies`中清除。

### `npm list` 列出已安装依赖（快捷方式：`ls`）

- 默认列出局部依赖。
- `npm list -g` 列出已安装的全局依赖。

### `npm outdated` 检查过期依赖

### `npm update` 更新依赖（快捷方式：`up`）

- `xxx` 局部更新xxx。
- `xxx -g` 全局更新xxx。

### `npm root` 查看依赖安装路径（也就是`node_modules`的路径）

- 默认查看局部安装路径。
- `-g` 查看全局安装路径。

### `npm view` 查看模块的注册信息

- `xxx versions` 列出`xxx`的所有版本， 如：`npm view jquery versions`。
- `xxx dependencies` 列出`xxx`的所有依赖， 如：`npm view gulp dependencies`。
