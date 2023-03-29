```javascript
// 0.基础概念

// 0.1 基础概念-Node.js
// (1) 基于Chrome V8引擎的Javascript代码运行环境，用于开发Web应用程序
// (2) 可以在服务器端(而非浏览器)运行JavaScript代码(用于JS编写的框架构建等)
// (3) 可以使用npm进行包管理

// 0.2 基础概念-NPM (Node Package Manager)
// (1) 是Node.js的包管理器
//     1) 重复的框架代码被称为“包”或“模块”
//     2) 一个包通常是含有package.json的文件夹里
// (2) 随同Node.js一起安装,用于node插件管理，包括安装、卸载、管理依赖等
// (3) 常见的使用场景有以下几种：
//     1) 允许用户从npm服务器下载别人编写的第三方包到本地使用。
//     2) 允许用户从npm服务器下载并安装别人编写的命令行程序到本地使用。
//     3) 允许用户将自己编写的包或命令行程序上传到npm服务器供别人使用。

// 0.3 基础概念-NVM (Node Version Manager)
// (1) Node.js的版本管理工具
// (2) 可以进行Node.js版本的切换、安装、查看等操作

// 0.4 基础概念-npx
// npm 5.2之后新增的npx命令
// (1) 可以直接到当前项目node_moudle/.bin/路径和$PATH下寻找命令
// (2) 避免全局安装仅在初始化时用一次的库，如脚手架
// (3) npx create-react-app将create-react-app下载到一个临时目录,用完后再删除
```

```javascript
// 1 Vue项目

// 1.1 Vue项目-项目初始化
// 已安装 16.0 或更高版本的 Node.js
$ npm init vue@latest
// 令将会安装并执行 create-vue，它是 Vue 官方的项目脚手架工具
// ✔ Project name     项目名称
// ✔ Add TypeScript?  项目使用 TypeScript 编写代码 
// ✔ Add JSX Support? 项目使用 JSX 语法编写代码
// ✔ Add Vue Router for Single Page Application development?
// ✔ Add Pinia for state management? 使用 Pinia 管理状态
// ✔ Add Vitest for Unit testing?    使用 Vitest 进行单元测
// ✔ Add Cypress for both Unit and End-to-End testing? 单元测试和端到端测试
// ✔ Add ESLint for code quality? … No/Yes 使用 ESLint 进行代码质量检查
// ✔ Add Prettier for code formatting?     使用 Prettier 进行代码格式化

// 1.2 Vue项目-项目结构
├── cypress                 端到端测试的相关代码
│   ├── e2e                 用例文件和配置文件
│   ├── fixtures            测试数据的JSON文件
│   └── support             支持代码，比如自定义命令、组件和钩子函数等
├── cypress.config.js       Cypress的一些全局配置
├── index.html              Vue应用的入口HTML文件
├── build                       构建脚本目录
│  ├── build-server.js          运行本地构建服务器，可以访问构建后的页面
│  ├── build.js                 生产环境构建脚本
│  ├── dev-client.js            开发服务器热重载脚本,开发阶段的页面自动刷新
│  ├── dev-server.js            运行本地开发服务器
│  ├── utils.js                 构建相关工具方法
│  ├── webpack.base.conf.js     wabpack基础配置
│  ├── webpack.dev.conf.js      wabpack开发环境配置
│  └── webpack.prod.conf.js     wabpack生产环境配置
├── package.json            应用依赖的npm包管理文件
├── public                  包含应用公共文件，如favicon.ico等
├── README.md               项目的说明文档
├── src                     Vue应用的主要代码目录
│   ├── App.vue             根组件
│   ├── assets              静态资源，会被wabpack构建
│   │   ├── base.css
│   │   ├── logo.svg
│   │   └── main.css
│   ├── components          应用的Vue组件
│   │   ├── HelloWorld.vue
│   │   ├── icons
│   ├── main.js             应用的入口文件
│   ├── router              前端路由配置
│   │   └── index.js
│   ├── store               应用级数据（state）
│   │   l└── index.js
│   └── views               视图组件/页面目录
│       ├── AboutView.vue
│       └── HomeView.vue
├── static                  纯静态资源，不会被wabpack构建
└── vite.config.js


// 1.3 Vue项目-npm(Node Package Manager)指令

// 1.3.1 Vue项目-npm(Node Package Manager)指令-版本、帮助、配置
$ npm -v               // 查看 npm 的版本号
$ npm -l               // 显示所有可用命令
$ npm help <command>   // 查看 <command> 命令的详细使用指南
$ npm <command> -h     // 查看 <command> 命令的简单使用帮助
$ npm config list -l   // 查看 npm 的配置

// 1.3.2 Vue项目-npm(Node Package Manager)指令-初始化
$ npm init  // 初始化生成一个新的package.json文件 -f 强制 -y 全部选是
$ npm init vue@latest

// 1.3.3 Vue项目-npm(Node Package Manager)指令-安装模块
// (1) 生产环境 
$ npm install package-name //       局部(cwd)安装模块;
$ npm i package-name       // (简写) 写入package.json的dependencies
// (2) 生产环境 
$ npm install --save-prod package-name  // 写入package.json的dependencies
$ npm install -P package-name           // 简写
// (3) 开发环境 
$ npm install --save-dev package-name // 写入package.json的devDependencies 
$ npm install -D package-name         // 简写
// (4) 全局安装 
$ npm install -g package-name         // 全局安装模块
// (5) 版本
$ npm install [<@scope>/]<name>           // 默认安装最新版本
$ npm install [<@scope>/]<name>@<version> // 安装指定模块的指定版本
$ npm install [<@scope>/]<name>@<version range>
//eg: npm install vue@">=1.0.28 < 2.0.0"
$ npm install <tarball url>               // 通过Github代码库地址安装

// 1.3.4 Vue项目-npm(Node Package Manager)指令-卸载模块
$ npm uninstall package-name      // 卸载局部模块
$ npm uninstall -g package-name   // 卸载全局模块

// 1.3.5 Vue项目-npm(Node Package Manager)指令-更新模块
$ npm update package-name            // 更新局部模块
$ npm update -g package-name         // 更新全局模块
$ npm install -g package-name@x.x.x  // 更新全局模块到x.x.x版本

// 1.3.6 Vue项目-npm(Node Package Manager)指令-查看模块
$ npm view package-name versions      // 查看某个模块的全部版本
$ npm search package-name [-g]        // 搜索模块,可以跟正则
$ npm list                            // 当前项目所有安装模块

// 1.3.7 Vue项目-npm(Node Package Manager)指令-引用模块
// 引用依赖 有些包是全局安装了，在项目里面只需要引用即可。
$ npm link [<@scope>/]<pkg>[@<version>]
//eg: 引用   npm link gulp gulp-ssh gulp-ftp
//eg: 解除引用 npm unlink gulp

// 1.3.8 Vue项目-npm(Node Package Manager)指令-执行脚本
$ npm run    // 会列出package.json里所有可执行的脚本和可配置参数
$ npm start  // start 可以省略run
$ npm test   // test 可以省略run
$ npm run build  // 在./dist文件夹中创建一个生产环境的构建版本
// npm run会创建一个Shell，执行指定的命令
// package.json的scripts字段，可以用于指定脚本命令，供npm直接调用。
"scripts": {
    "lint": "eslint --cache --ext .js --ext .jsx src",
    "test": "karma start --log-leve=error karma.config.js --single-run=true",
    "pretest": "npm run lint",
    "posttest": "echo 'Finished running tests'"
  }
$ npm run lint
//直接执行 npm run lint 结束
$ npm run test
//因为有定义了两个钩子pretest、posttest。
//所以先执行 npm run pretest
//然后执行 npm run test
//最后执行 npm run posttest


```
