# React 教程

## 一、描述UI

### 01. 组件

### 01.01 定义组件

**React 组件是一段可以 使用标签进行扩展 的 JavaScript 函数**。

构建组件的方法：

- 第一步：`export default` 前缀到处组件

- 第二步：使用 `function Profile() { }` 定义函数

- 第三步：函数返回一个带有属性的标签

```jsx
// App.js
export default function Profile() {
  return (
    <img src="https://i.imgur.com/MK3eW3Am.jpg" alt="Katherine" />
  )
}
```

> 警告：没有**括号包裹**的话，任何在 `return` 下一行的代码都将被忽略

### 01.02 组件使用

React组件以大写字母开头，HTML组件以小写字母开头

```jsx
export default function Gallery() {
  return (
    <section>
      <h1>了不起的科学家</h1>
      <Profile />
      <Profile />
      <Profile />
    </section>
  );
}
```

> 警告：组件可以渲染其他组件，但是 **请不要嵌套他们的定义**。永远不要在组件中定义组件。当子组件需要使用父组件的数据时，你需要通过 **props** 的形式进行传递，而不是嵌套定义。

### 02. 组件的导入与导出

### 02.01 根组件文件

在此示例中，所有组件目前都定义在 **根组件** `App.js` 文件中。具体还需根据项目配置决定，有些根组件可能会声明在其他文件中。如果你使用的框架基于文件进行路由，如 Next.js，那你每个页面的根组件都会不一样。

### 02.02 组件的导入和导出

以下三个步骤对组件进行拆分：

- **创建** 一个新的 JS 文件来存放该组件。
- **导出** 该文件中的函数组件（可以使用默认导出或具名导出）
- 在需要使用该组件的文件中 **导入**（可以根据相应的导出方式使用默认导入或具名导入）。

```jsx
import Gallery from './Gallery.js';
// 默认导入Gallery +默认导出App
export default function App() {
  return ( <Gallery /> ;
}

export function Profile() {...}
// 具名导出Profile+具名导入Profile
import { Profile } from './Gallery.js';
}
```

### 03. 使用 JSX 书写标签语言

**在 React 中，渲染逻辑和标签共同存在于同一个地方——组件。** 将一个按钮的渲染逻辑和标签放在一起可以确保它们在每次编辑时都能保持互相同步。反之，彼此无关的细节是互相隔离的，例如按钮的标签和侧边栏的标签。这样我们在修改其中任意一个组件时会更安全。

每个 React 组件都是一个 JavaScript 函数，它会返回一些标签，React 会将这些标签渲染到浏览器上。React 组件使用一种被称为 JSX 的语法扩展来描述这些标签。

> 注意：[JSX and React 是相互独立的](https://reactjs.org/blog/2020/09/22/introducing-the-new-jsx-transform.html#whats-a-jsx-transform) 东西。但它们经常一起使用，但你 **可以** 单独使用它们中的任意一个，JSX 是一种语法扩展，而 React 则是一个 JavaScript 的库。

### 03.02 将 HTML 转化为 JSX

因为 JSX 语法更加严格并且相比 HTML 有更多的规则，直接复制不能正确工作。

> 注意：大部分情况下，React 在屏幕上显示的错误提示就能帮你找到问题所在，如果在编写过程中遇到问题就参考一下提示吧。

### 03.03 JSX 规则

- **只能返回一个根元素**：想要在一个组件中包含多个元素，**需要用一个父标签把它们包裹起来**，如`<></>`。
- **标签必须闭合**：JSX 要求标签必须正确闭合。
- **使用驼峰式命名法给 ~~所有~~ 大部分属性命名！**：由于 `class` 是一个保留字，所以在 React 中需要用 `className` 来代替。

> 警告：由于历史原因，[`aria-*`](https://developer.mozilla.org/docs/Web/Accessibility/ARIA) 和 [`data-*`](https://developer.mozilla.org/docs/Learn/HTML/Howto/Use_data_attributes) 属性是以带 `-` 符号的 HTML 格式书写的。

## 04 在 JSX 中通过大括号使用 JavaScript

### 04.01 如何使用引号传递字符串

### 04.02 在 JSX 的大括号内引用 JavaScript 变量

### 04.03 在 JSX 的大括号内调用 JavaScript 函数

### 04.04 在 JSX 的大括号内使用 JavaScript 对象

## 二、添加交互

## 三、状态管理

## 四、脱围机制
