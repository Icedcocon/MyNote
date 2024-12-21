# memos 快速开始

## 开始

### 1. 环境准备

- 搭建开发脚手架

```bash
# 1. 使用 vite 搭建脚手架
npm create vite@latest
✔ Project name: … memos
✔ Select a framework: › React
✔ Select a variant: › TypeScript
# 安装依赖
cd memos
npm install 
# 启动服务
npm run dev
```

- 引入 ant design

```bash
# 安装依赖
npm install antd --save
```

### 2. 项目结构与说明

```bash
developer@ubuntu-ai:~/PrivateRepos/demo/memos$ tree -L 2
.
├── eslint.config.js
├── index.html
├── node_modules
├── package.json
├── package-lock.json
├── public
│   └── vite.svg
├── README.md
├── src
│   ├── App.css
│   ├── App.jsx
│   ├── App.tsx
│   ├── assets
│   ├── components
│   ├── index.css
│   ├── main.tsx
│   └── vite-env.d.ts
├── tsconfig.app.json
├── tsconfig.json
├── tsconfig.node.json
└── vite.config.ts

185 directories, 16 files
```

#### 2.0 主要目录结构

- /src: 源代码目录

- /public: 静态资源目录

- /node_modules: 依赖包目录

#### 2.1  重要配置文件解析

##### 2.1.1 package.json

> - 项目的核心配置文件
> 
> - 定义项目的依赖包、脚本命令和项目元数据
> 
> - 管理项目的依赖版本和开发依赖

- 1. 基础信息配置

```json
{
  "name": "项目名称",
  "version": "版本号",
  "description": "项目描述",
  "keywords": ["关键词"],
  "author": "作者信息",
  "license": "许可证类型",
  "private": true/false,  // 是否私有包
  "type": "module/commonjs"  // 模块类型
}
```

- 2. 依赖管理

```json
{
  "dependencies": {     // 生产环境依赖
    "package-name": "version"
  },
  "devDependencies": { // 开发环境依赖
    "package-name": "version"
  },
  "peerDependencies": { // 同伴依赖
    "package-name": "version"
  },
  "optionalDependencies": { // 可选依赖
    "package-name": "version"
  }
}
```

- 3. 脚本命令

```json
{
  "scripts": {
    "start": "启动命令",
    "build": "构建命令",
    "test": "测试命令",
    "custom-script": "自定义命令"
  }
}
```

- 4. 项目配置

```json
{
  "main": "入口文件",
  "module": "ES模块入口",
  "types": "类型声明文件",
  "files": ["需要发布的文件列表"],
  "bin": {  // 可执行文件配置
    "command-name": "path/to/file"
  }
}
```

- 5. 发布配置

```json
{
  "publishConfig": {
    "registry": "npm仓库地址",
    "access": "public/restricted",
    "tag": "latest"
  }
}
```

- 6. 项目配置项

```json
{
  "homepage": "项目主页",
  "repository": {
    "type": "git",
    "url": "仓库地址"
  },
  "bugs": {
    "url": "问题追踪地址",
    "email": "问题报告邮箱"
  }
}
```

- 7. 工作区配置（Monorepo）

```json
{
  "workspaces": [
    "packages/*",
    "apps/*"
  ]
}
```

- 8. 浏览器兼容性

```json
{
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
```

- 9. 引擎要求

```json
{
  "engines": {
    "node": ">=14.0.0",
    "npm": ">=6.0.0"
  }
}
```

- 10. 配置覆盖

```json
{
  "overrides": {
    "package-name": {
      "dependencies": {
        "other-package": "version"
      }
    }
  }
}
```

- 11. 项目设置

```json
{
  "config": {
    "port": "3000",
    "customKey": "customValue"
  }
}
```

> 版本号说明
> 
> - ^version: 兼容补丁和小版本更新
> 
> - ~version: 仅兼容补丁更新
> 
> - version: 完全匹配版本
> 
> - *: 接受任何版本
> 
> - latest: 最新版本
> 
> - \> = version: 大于等于某版本

这些配置可以根据项目需求灵活组合使用，不是所有字段都必须配置。通常会根据项目类型（库/应用）和具体需求选择相应的配置项。

##### 2.1.2 vite.config.ts

- Vite构建工具的配置文件

- 用于配置开发服务器、构建选项、插件等

- 支持TypeScript，可以提供更好的类型提示

##### 2.1.3 tsconfig.json 相关文件

  ├── tsconfig.app.json    # 应用特定的TypeScript配置

  ├── tsconfig.json        # 基础TypeScript配置

  ├── tsconfig.node.json   # Node环境下的TypeScript配置

- 配置TypeScript的编译选项

- 定义项目的模块解析规则

- 设置代码检查级别

##### 2.1.4 eslint.config.js

- ESLint的配置文件

- 定义代码规范和格式化规则

- 配置代码质量检查规则

## 参考资料
