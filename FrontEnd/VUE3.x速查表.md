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

```javascript
// 2 HTML语法

// 2.1 HTML语法-网页的基本概念

// 2.1.1 HTML语法-网页的基本概念-标签（tag）
<title>网页标题</title>    // (1) 一对标签,位于尖括号里面,分成开始标签和结束标签
<meta charset="utf-8">    // (2) 也有一些标签不是成对使用
<div><p>hello</p></div>   // (3) 标签可以嵌套,必须保证正确的闭合顺序
                          // (4) HTML语言忽略缩进和换行(可以全部写进一行)

// 2.1.2 HTML语法-网页的基本概念-元素（element）
// (1) 渲染时HTML源码被解析成标签树,标签即一个树的节点,节点称为网页元素（element）
// (2) 上层元素又称为“父元素”，下层元素又称为“子元素”
// (3) 元素可以分成两大类：块级元素（block）和行内元素（inline）
<p>hello</p>        // 块级元素默认占据一个独立的区域,占据 100% 的宽度
<p>world</p>        // 在网页上会自动另起一行
<span>hello</span>  // 行内元素默认与其他元素在同一行，不产生换行
<span>world</span>  // 同一行

// 2.1.3 HTML语法-网页的基本概念-属性（attribute）
<img src="demo.jpg" width="50">  // <img>标签有两个属性：src和width
// (1) 属性是标签的额外信息,用空格与标签名分隔
// (2) 可用等号指定属性值,值一般在双引号里(非必需)
// (3) 属性名是大小写不敏感的，onclick和onClick是同一个属性

// 2.1.3 HTML语法-网页的基本概念-网页的基本标签
// 符合 HTML 语法标准的网页，应该满足下面的基本结构
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title></title>
</head>
<body>
</body>
</html>

// 2.1.3.1 HTML语法-网页的基本概念-网页的基本标签-<!doctype>
// 网页的第一个标签通常是<!doctype>，表示文档类型，告诉浏览器如何解析网页
<!doctype html>  // 声明doctype为html,浏览器就按照HTML 5的规则处理网页
<!DOCTYPE html>  // 有时采用完全大写以别于正常的 HTML 标签 
// <!doctype>本质上不是标签，更像一个处理指令

// 2.1.3.2 HTML语法-网页的基本概念-网页的基本标签-<html>
// (1) <html>标签是标签树结构的顶层节点，也称为根元素(root element);
//     其他元素都是它的子元素;一个网页只能有一个<html>标签;
<html lang="zh-CN">   // (2) lang属性，表示网页内容默认的语言

// 2.1.3.3 HTML语法-网页的基本概念-网页的基本标签-<head>简介
// (1) <head>标签是一个容器标签，用于放置网页的元信息。
// (2) 它的内容不会出现在网页上，而是为网页渲染提供额外信息。
// (3) <head>是<html>的第一个子元素，如果网页不包含<head>，浏览器会自动创建一个

// 2.1.3.4 HTML语法-网页的基本概念-网页的基本标签-<head>7种子元素
// <head>的子元素一般有下面七个:
// (1) <meta>:      设置网页的元数据。
// (2) <link>:      连接外部样式表。
// (3) <title>:     设置网页标题。
// (4) <style>:     放置内嵌的样式表。
// (5) <script>:    引入脚本。
// (6) <noscript>:  浏览器不支持脚本时，所要显示的内容。
// (7) <base>:      设置网页内部相对 URL 的计算基准。

// 2.1.3.5 HTML语法-网页的基本概念-网页的基本标签-<meta>简介
// (1) <meta>标签用于设置或说明网页的元数据，必须放在<head>里面;
// (2) 一个<meta>标签就是一项元数据，网页可以有多个<meta>;
// (3) <meta>标签约定放在<head>内容的最前面;
<head>
  <meta charset="utf-8">   // 网页采用 UTF-8 格式编码
  <meta name="viewport" content="width=device-width, initial-scale=1">
  // 网页在手机端可以自动缩放
  <title>Page Title</title>
</head>

// 2.1.3.6 HTML语法-网页的基本概念-网页的基本标签-<meta>标签的五个属性
// (1) charset 属性指定网页的编码方式
<meta charset="utf-8"> // 声明了utf-8，网页就应该使用UTF-8编码保存
// (2) name 属性表示元数据的名字，content 属性表示元数据的值，通常一起使用
//     大部分涉及浏览器内部工作机制，或者特定的使用场景
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="application-name" content="Application Name">
<meta name="generator" content="program">
<meta name="subject" content="your document's subject">
<meta name="referrer" content="no-referrer">
// (3) http-equiv 属性用来补充 HTTP 回应的头信息字段，服务器发回的 HTTP 回应
//     缺少该个字段就可以用 content 属性的内容补充
<meta http-equiv="Content-Type" content="Type=text/html; charset=utf-8">
<meta http-equiv="refresh" content="30">
<meta http-equiv="refresh" content="30;URL='http://website.com'">

// 2.1.3.7 HTML语法-网页的基本概念-网页的基本标签-<title>
// (1) <title>标签用于指定网页的标题，会显示在浏览器窗口的标题栏
// (2) 搜索引擎根据这个标签，显示每个网页的标题
// (3) <title>标签的内部，不能再放置其他标签，只能放置无格式的纯文本
<head>
  <title>网页标题</title>
</head>

// 2.1.3.8 HTML语法-网页的基本概念-网页的基本标签-<body>
// (1) <body>标签是一个容器标签，用于放置网页的主体内容
// (2) <html>的第二个子元素，紧跟在<head>后面<html>
<head>
    <title>网页标题</title>
  </head>
  <body>
    <p>hello world</p>
  </body>
</html>

// 2.1.4 HTML语法-网页的基本概念-空格和换行
// (1) 标签内容的头部和尾部的空格，一律忽略不计
<p>  hello world   </p>  // hello前面和world后面的空格忽略不计
// (2) 内容里面的多个连续空格（包含制表符\t），会被浏览器合并成一个
<p>hello      world</p>  // hello与world之间的多个连续空格会合并成一个
// (3) 换行符（\n）和回车符（\r），替换成空格
<p>hello

world
</p> // hello与world之间的多个换行替换成空格,再将多个空格合并成一个

// 2.1.5 HTML语法-网页的基本概念-注释
<!-- 这是一个注释 -->
<!--
  <p>hello world</p>
-->

// 2.2 HTML语法-网页元素的属性

// 2.2.1 HTML语法-网页元素的属性-简介
// (1) 属性名与标签名一样，不区分大小写
// (2) 属性名与属性值之间，通过等号=连接；属性值建议使用双引号
// (3) 布尔属性的属性值可以省略，只要添加了属性名，就表示打开该属性
<input type="text" required>

// 2.2.2 HTML语法-网页元素的属性-全局属性
// (1) 全局属性（global attributes）是所有元素都可以使用的属性
// (2) 全局属性可以加在任意一个网页元素上面，不过有些属性对某些元素可能不产生意义

// 2.2.3 HTML语法-网页元素的属性-id(全局属性)
// (1) id属性是元素在网页内的唯一标识符
// (2) 同一个页面不能有两个相同的id属性
// (3) id属性的值不得包含空格
// (4) id属性的值还可以在最前面加上#，放到 URL 中作为锚点
//     如 https://foo.com/index.html#bar
<p id="p1"></p>
<p id="p2"></p>
<p id="p3"></p>

// 2.2.4 HTML语法-网页元素的属性-class(全局属性)
// (1) class属性用来对网页元素进行分类;不同元素的class属性值相同表示同一类
<p class="para"></p>
<p></p> // 第一个<p>和第三个<p>是一类
<p class="para"></p>
// (2) 元素可以同时具有多个 class，它们之间使用空格分隔
<p class="p1 p2 p3"></p>  // p元素同时具有p1、p2、p3三个 class

// 2.2.5 HTML语法-网页元素的属性-title
// (1) title属性为元素添加附加说明；鼠标悬浮在元素上会将title属性值显示出来
<div title="版权说明">
  <p>本站内容使用创意共享许可证，可以自由使用。</p> // 浮现 版权说明
</div>

// 2.2.6 HTML语法-网页元素的属性-style
// style属性用来指定当前元素的 CSS 样式
<p style="color: red;">hello</p>  // 指定文字颜色为红色

// 2.2.7 HTML语法-网页元素的属性-data-属性
// data-属性用于放置自定义数据
// data-属性只能通过 CSS 或 JavaScript 利用
<a href="#" class="tooltip" data-tip="this is the tip!">链接</a>
// data-tip用于放置链接的提示文字
/* HTML 代码如下
<div data-role="mobile">
Mobile only content
</div>
*/
div[data-role="mobile"] {
  display:none;
}
/* HTML 代码如下
<div class="test" data-content="This is the div content">test</div>​
*/
.test {
  display: inline-block;
}
.test:after {
  content: attr(data-content);
}

// 2.2.8 HTML语法-网页元素的属性-tabindex
// tabindex属性的值是一个整数，表示用户按下 Tab 键的时候，网页焦点转移的顺序
// 0：该元素参与 Tab 键的遍历，顺序由浏览器指定，通常是按照其在网页里面出现的位置。

// 2.2.9 HTML语法-网页元素的属性-事件处理属性（event handler）
// 事件处理属性用来响应用户的动作,这些属性的值都是 JavaScript 代码
// onabort, onautocomplete, onautocompleteerror, onblur, oncancel, 
// oncanplay, oncanplaythrough, onchange, onclick, onclose, oncontextmenu, 
// oncuechange, ondblclick, ondrag, ondragend, ondragenter, ondragexit, 
// ondragleave, ondragover, ondragstart, ondrop, ondurationchange, 
// onemptied, onended, onerror, onfocus, oninput, oninvalid, onkeydown, 
// onkeypress, onkeyup, onload, onloadeddata, onloadedmetadata, 
// onloadstart, onmousedown, onmouseenter, onmouseleave, onmousemove, 
// onmouseout, onmouseover, onmouseup, onmousewheel, onpause, onplay, 
// onplaying, onprogress, onratechange, onreset, onresize, onscroll, 
// onseeked, onseeking, onselect, onshow, onsort, onstalled, onsubmit, 
// onsuspend, ontimeupdate, ontoggle, onvolumechange, onwaiting
```
