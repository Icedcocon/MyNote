# NVM

### 概念

##### 易混淆的概念

- Node.js：基于Chrome V8引擎的Javascript代码运行环境 （运行环境）

- npm： 第三方JS插件包管理工具，会随着node一起安装（Node package Manager）

- npx：npm5.2之后新增的npx命令
  
  - 直接到当前项目node_moudle/.bin/路径和$PATH下，寻找命令
  
  - 避免全局安装，比如脚手架类型的库，通常只会在初始化时用一次,此时就可以通过npmx create-react-app这种方式调用，执行这个命令时，npx会将create-react-app下载到一个临时目录，使用完后再删除。

##### NVM是什么

- node的版本管理工具

- 可以进行node版本的切换、安装、查看等操作

- npm不同，npm是依赖包的管理工具

##### 安装

- NPM GitHub下载地址： https://github.com/coreybutler/nvm-windows/releases
- 安装前要讲node环境卸载干净

```bash
# 安装Node.js版本管理工具nvm
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.39.2/install.sh | bash
wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.39.2/install.sh | bash
git clone git://github.com/creationix/nvm.git ~/nvm
# 验证安装
command -v nvm
# 设施nvm自启动
echo "source ~/nvm/nvm.sh" >> ~/.bashrc
source ~/.bashrc
```

##### 下载Node.js

```bash
# 查看nvm版本
nvm --version
# 查看可用的node.js版本
nvm list-remote
nvm ls-remote
# 安装node.js
nvm install v7.6.0
# 切换node.js版本
nvm use v7.6.0
# 卸载node.js
nvm uninstall v7.6.0
```
