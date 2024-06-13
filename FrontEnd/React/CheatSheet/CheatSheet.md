```json
{
    "date":"2019.01.02 14:33"，//最少需要
    "tags": ["BLOG"，"其它tag"]，//可以不填，不过最好添加一些tag，后面可以做一些好玩的东西。
    "title": "文章的标题，一般不用填写，默认使用文件名"，
    "description": "文章描述，不填写自动取正文200个字，可以在app.json中配置"，
    "author": "xusenlin"， //文章作者，可以不用填写，现在也没有使用到
    "musicId":"网易云的音乐ID" //阅读文章时可以播放的歌曲
}
```

# React速查表

## 一、 入门

### 01. 介绍及创建项目

React 是一个用于构建用户界面的 JavaScript 库

- [React 官方文档](https://reactjs.org/) *(reactjs.org)*
- [Styled Components 备忘清单](https://wangchujiang.com/reference/docs/styled-components.html) *(jaywcjlove.github.io)*
- [TypeScript JSX 备忘清单](https://wangchujiang.com/reference/docs/typescript.html#jsx) *(jaywcjlove.github.io)*

---

```jsx
// main.jsx
import {createRoot} from 'react-dom/client'
import App from './App'

const elm = document.getElementById('app')
const root = createRoot(elm);
root.render(<App />);
// 或
ReactDOM.createRoot(document.getElementById('app')).render(<App />)
```

---

- 项目结构

```bash
# 项目结构
.
├── index.html              # 入口 html 含根元素 <div id="app"></div>
├── package.json            # 依赖管理
├── package-lock.json
├── public                  # 静态文件
├── README.md
├── src
│   ├── App.css             # 根组件样式 使用 styled-component 时可省略
│   ├── App.jsx             # 根组件
│   ├── assets
│   ├── components          # 公共组件
│   ├── index.css
│   └── main.jsx            # 入口 jsx 将根组件渲染至入口 html
└── vite.config.js
```

---

- 快速创建 **React** 项目（CRA）

```bash
# 快速创建 **React** 项目（CRA）
npx create-react-app my-app
# 或
npm create vite@latest
```

### 02. 组件的导入导出

```jsx
import React, {Component} from 'react'
import ReactDOM from 'react-dom'
```

---

```jsx
export class Hello extends Component {
  ...
}
export default function World() {
  /* ... */
}
```

使用 `export` 导出 **`Hello`**，`export default` 导出 **`World`** 组件

```jsx
import World, { Hello } from './hello.js';
```

使用 `import` 导入 `Hello` 组件，在示例中使用。  

### 03. React组件中的CSS（styled-component）

- 导入全局样式

```jsx
import React from "react";
import "./Student.css";

export const Student = (
  <div className="Student"></div>
);
```

注意：类属性 `className`

---

内联 `style` 属性 使用驼峰命名法编写。

```jsx
const divStyle = {
  backgroundImage: 'url(' + imgUrl + ')',
  backgroundColor: 'black,
};
export const Student = (
  <div style={divStyle}></div>
);
```

### 04. props与参数传递

```jsx
<Student name="Julie" age={23}
  pro={true} />
```

函数组件 `Student` 中访问属性

```jsx
function Student(props) {
  return <h1>Hello, {props.name}</h1>;
}
// 或解构，props可以使用默认值
function Student({name, age, pro=false}) {...}
```

--- 

Class 组件 `Student` 中访问属性

```jsx
class Student extends React.Component {
  render() {
    return (
      <h1>Hello, {this.props.name}</h1>
    );
  }
}
```

`class` 组件使用 `this.props` 访问传递给组件的属性。

---

可以将props透传给子组件后，使用 ... 展开

```jsx
function Profile(props) {
  return (
    <div className="card">
      <Avatar {...props} />
    </div>
  );
}
```

> 注意：
> 
> - Props 是只读的时间快照：每次渲染都会收到新版本的 props。
> - 你不能改变 props。当你需要交互性时，你可以设置 state。

### 05 children与JSX传递

```jsx
function Example() {
  return (
    <AlertBox>
      <h1>您有待处理的通知</h1>
    </AlertBox>
  )
}
```

函数 `AlertBox` 组件

```jsx
function AlertBox(props) {
  return ( <div className="alert-box"> {props.children} </div> );
}
// 或
function AlertBox({children}){
    return (<div className="alert-box">{children}</div>)
}
```

---

Class `AlertBox` 组件，与函数组件 `AlertBox` 组件相同

```jsx
class AlertBox extends React.Component {
  render () {
    return ( <div className="alert-box"> {this.props.children} </div> );
  }
}
```

`children` 作为子组件的的属性传递。

### 06 条件渲染

在 React，你可以使用 JavaScript 来控制分支逻辑。

- 可以使用 `if` 语句来选择性地返回 JSX 表达式。

```jsx
function Item({ name, isPacked }) {
  if (isPacked) {
    return <li className="item">{name} ✔</li>;
  }
  return <li className="item">{name}</li>;
}
```

可以选择性地将一些 JSX 赋值给变量，然后用大括号将其嵌入到其他 JSX 中。

- 在 JSX 中，`{cond ? <A /> : <B />}` 表示 *“当 `cond` 为真值时, 渲染 `<A />`，否则 `<B />`”*。
- 在 JSX 中，`{cond && <A />}` 表示 *“当 `cond` 为真值时, 渲染 `<A />`，否则不进行渲染”*。

```jsx
return (
  <li className="item">
    {isPacked ? name + ' ✔' : name}
  </li>
);
// 或
return (
  <li className="item">
    {name} {isPacked && '✔'}
  </li>
);
```

### 07 列表渲染

```jsx
const elm = ['one', 'two', 'three'];
function Student() {
  return (
    <ul>
      {elm.map((value, index) => ( <li key={index}>{value}</li> ))}
    </ul>
  );
}
```

使用 JavaScript 的 `map()` 方法来生成一组相似的组件。

`key` 值在兄弟节点之间必须唯一

--- 

```jsx
const chemists = people.filter(person => person.profession === '化学家' );
```

使用 JavaScript 的 `filter()` 方法来筛选数组。

### 08 纯函数

```jsx
function addNumbers(x1, x2) {
  return x1 + x2;
}

const element = (
  <div>
    {addNumbers(2, 5)}
  </div>
);
```

- 一个组件必须是纯粹的，就意味着：
  - **只负责自己的任务。** 它不会更改在该函数调用前就已存在的对象或变量。
  - **输入相同，则输出相同。** 给定相同的输入，组件应该总是返回相同的 JSX。
- 渲染随时可能发生，因此组件不应依赖于彼此的渲染顺序。
- **不应该改变包括 props、state 和 context**在内用于组件渲染的输入。通过“设置” state来更新界面，而不要改变预先存在的对象。
- **在事件处理程序中“改变事物”**。 `useEffect`可以作为最后的手段使用。

### 09 UI树

```jsx
import { useState } from 'react'
import Avatar from './Avatar';
import Profile from './Profile';

function Student() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <Avatar src={count} />
      <Profile username={count} />
    </div>
  );
}
```

- 渲染树表示单次渲染中 React 组件之间的嵌套关系。

渲染树有助于识别顶级组件和叶子组件。顶级组件会影响其下所有组件的渲染性能，而叶子组件通常会频繁重新渲染。

- 依赖树表示 React 应用程序中的模块依赖关系。

构建工具使用依赖树来捆绑必要的代码以部署应用程序。依赖树有助于调试大型捆绑包带来的渲染速度过慢的问题，以及发现哪些捆绑代码可以被优化。

### 10 响应事件

- 事件会向上传播。通过事件的第一个参数调用 `e.stopPropagation()` 来防止这种情况。
- 事件可能具有不需要的浏览器默认行为。调用 `e.preventDefault()` 来阻止这种情况。
- 必须传递事件处理函数，**而非函数调用！** `onClick={handleClick}或onClick=()=>handleClick()` ，不是 `onClick={handleClick()}`。

```jsx
export default function Hello() {
  function handleClick(event) {
    event.preventDefault();
    event.stopPropagation();
    alert("Hello World");
  }

  return ( <a href="/" onClick={handleClick}> Say Hi </a> );
}
```

---

- 你可以通过将函数作为 prop 传递给元素如 `<button>` 来处理事件。
- 事件处理函数在组件内部定义，所以它们可以访问 props。
- 可以在父组件中定义一个事件处理函数，并将其作为 prop 传递给子组件。

```jsx
function Button({ onClick, children }) {
  return (
    <button onClick={onClick}>
      {children}
    </button>
  );
}
function PlayButton({ movieName }) {
  function handlePlayClick() { alert(`正在播放 ${movieName}！`); }
  return (
    <Button onClick={handlePlayClick}> 播放 "{movieName}" </Button>
  );
}
```

### 11 设置State

`useState` Hook 提供了这两个功能：

1. **State 变量** 用于保存渲染间的数据。
2. **State setter 函数** 更新变量并触发 React 再次渲染组件。

函数中的 State，Hook 是 React 16.8 的新增特性

`count` 是一个 state 变量，`setCount` 是对应的 setter 函数。

```jsx
import { useState } from 'react';

function Student() {
  const [count, setCount] = useState(0);
  let hasPrev = count > 0
  let hasNext = count < 10
  const add = () => setCount(count + 1);
  const sub = () => setCount(count + 1);
  return (
    <div>
      <p>您点击了 {count} 次（0<x<10）</p>
      <button onClick={add} disabled={!hasNext}> 增加 </button>
      <button onClick={sub} disabled={!hasPrev}> 减少 </button>
    </div>
  );
}
```

> Hooks ——以 use 开头的函数——**只能在组件或自定义 Hook 的最顶层调用**。 你**不能在条件语句、循环语句或其他嵌套函数内调用 Hook**。Hook 是函数，但将它们视为关于组件需求的无条件声明会很有帮助。在组件顶部 “use” React 特性，类似于在文件顶部“导入”模块。

> State 是屏幕上**组件实例内部的状态**。换句话说，如果你渲染同一个组件两次，每个副本都会有**完全隔离**的 state！改变其中一个不会影响另一个。

---

Class 中的 State

```jsx
import React from 'react';

class Student extends React.Component {
  constructor(props) {
    super(props);
    this.state = {count: 1};
    // 确保函数可以访问组件属性（ES2015）
    this.click = this.click.bind(this);
  }
  click() {
    const count = this.state.count;
    this.setState({ count: count + 1})
  }
  render() {
    return (
      <div>
        <button onClick={this.click}> 点击我 </button>
        <p>您点击了{this.state.count}次</p>
      </div>
    );
  }
}
```

### 12 渲染与状态更新

- 在一个 React 应用中一次屏幕更新都会发生以下三个步骤：
  1. 触发一次渲染
     - 组件的 **初次渲染。**
     - 组件（或者其祖先之一）的 **状态发生了改变。**
  2. 渲染组件
  3. 提交到 DOM
- 如果渲染结果与上次一样，那么 React 将不会修改 DOM

---

```jsx
import { useState } from 'react';

export default function Counter() {
  const [number, setNumber] = useState(0);

  return (
    <>
      <h1>{number}</h1>
      <button onClick={() => {
        setNumber(number + 5); // 0 + 5
        setNumber(number + 5); // 0 + 5
        alert(number);         // 0
      }}>+5</button>
    </>
  )
}
```

- useState 返回的Hook函数 setNumber 在组**件中代码执行结束后修改State**中的值
- 批处理可以**更新（自多个组件的）多个 state 变量而不会触发太多的重新渲染**。
- **React 不会跨 *多个* 需要刻意触发的事件（如点击）进行批处理**
- 需要即时生效的变量请使用JS变量，需要渲染时生效的变量可以使用State

---

- 在一次渲染中多次更新同一个 state可以传递**更新函数**。更新函数会被React添加至队列顺序执行（按照代码顺序）。

```jsx
import { useState } from 'react';

export default function Counter() {
  const [number, setNumber] = useState(0);

  return (
    <>
      <h1>{number}</h1>
      <button onClick={() => {
        setNumber(n => n + 1); // 1
        setNumber(2);          // 2
        setNumber(n => n + 1); // 3
      }}>+3</button>
    </>
  )
}
```

### 13 State中的对象和数组

- 将 React 中所有的 state 都视为不可直接修改的。
- 直接修改state 中存放对象并不会触发重渲染，而会改变前一次渲染“快照”中 state 的值。

```jsx
const [person, setPerson] = useState({
  name: 'Niki de Saint Phalle',
  artwork: {
    title: 'Blue Nana',
    city: 'Hamburg',
    image: 'https://i.imgur.com/Sd1AgUOm.jpg',
  }
});
```

---

- 不要直接修改一个对象，而要为它创建一个 **新** 版本，并通过把 state 设置成这个新版本来触发重新渲染。
- 你可以使用这样的 `{...obj, something: 'newValue'}` 对象展开语法来创建对象的拷贝。
- 想要减少重复的拷贝代码，可以使用 Immer。

```jsx
const nextArtwork = { ...person.artwork, city: 'New Delhi' };
const nextPerson = { ...person, artwork: nextArtwork };
setPerson(nextPerson);
// 或
setPerson({
  ...person, // 复制其它字段的数据 
  artwork: { // 替换 artwork 字段 
    ...person.artwork, // 复制之前 person.artwork 中的数据
    city: 'New Delhi' // 但是将 city 的值替换为 New Delhi！
  }
});
```

---

当你操作 React state 中的数组时，你需要避免使用左列的方法，而首选右列的方法：

|      | 避免使用 (会改变原始数组)             | 推荐使用 (会返回一个新数组）          |
| ---- | -------------------------- | ------------------------ |
| 添加元素 | `push`，`unshift`           | `concat`，`[...arr]` 展开语法 |
| 删除元素 | `pop`，`shift`，`splice`     | `filter`，`slice`         |
| 替换元素 | `splice`，`arr[i] = ...` 赋值 | `map`                    |
| 排序   | `reverse`，`sort`           | 先将数组复制一份                 |

```jsx
const [name, setName] = useState('');
const [artists, setArtists] = useState([]);
```

- 添加

```jsx
<button onClick={() => { 
     setArtists([ ...artists, { id: nextId++, name: name } ]);
}}>添加</button>
```

- 删除

```jsx
<button onClick={() => {
    setArtists( artists.filter(a => a.id !== artist.id ) );
}}> 删除 </button>
```

- 替换数组中元素

```jsx
const nextCounters = counters.map((c, i) => i === index?c + 1:c);
```

- 插入元素

```jsx
const nextArtists = [  ...artists.slice(0, insertAt),
                         { id: nextId++, name: name },
                       ...artists.slice(insertAt)
];
```

- 翻转、排序模型先复制

```jsx
function handleClick() {
  const nextList = [...list];
  nextList.reverse();
  setList(nextList);
}
```

### 14 声明式UI设计（基于状态）

- (1) 列出组件中所有的视图**状态**，如empty、typing、submiting、success、error。
- (2) 列出触发了这些 state 改变的**事件**。
- (3) 通过 `useState` 模块化内存中的 state。
- (4) 删除任何不必要的 state 变量。
- (5) 连接事件处理函数去设置 state。

```jsx
import {useState} from 'react'
export default function EditProfile() {
  const [isEditing, setIsEditing] = useState(false)
  const [name, setName] = useState({first:"Jane",last:"Jacobs"})
  return (
    <form>
      <label>
        First name:{' '}
        {isEditing?
        <input onChange={(e)=>setName({...name,first:e.target.value})}/>:
        <b>{name.first}</b>}
      </label>
      <label>
        Last name:{' '}
        {isEditing?
        <input onChange={(e)=>setName({...name,last:e.target.value})}/>:
        <b>{name.last}</b>}
      </label>
      <button type="submit" 
         onClick={(e)=>{e.preventDefault();setIsEditing(!isEditing)}}>
        {isEditing?"Save Profile":"Edit Profile"}
      </button>
      <p><i>Hello, {name.first} {name.last}!</i></p>
    </form>
```

### 15 State使用原则

- 如果两个 state 变量总是一起更新，请考虑将它们合并为一个。
- 避免矛盾、冗余和重复的 state以避免同步问题，以减少出错机会为原则。

```jsx
items = [{ id: 0, title: 'pretzels'}, ...]
selectedItem = {id: 0, title: 'pretzels'}
//改了之后是这样的：
items = [{ id: 0, title: 'pretzels'}, ...]
selectedId = 0
```

> 注意：如果你的 state 变量是一个对象时，请记住，你不能只更新其中的一个字段而不显式复制其他字段。

- 除非您特别想防止更新，否则不要将 props **放入** state 中。

```jsx
function Message({ messageColor }) {
  const [color, setColor] = useState(messageColor);
```

> **如果父组件稍后传递不同的 `messageColor` 值（例如，将其从 `'blue'` 更改为 `'red'`），则 `color`** state 变量**将不会更新！** state 仅在第一次渲染期间初始化。

- 对于选择类型的 UI 模式，请在 state 中保存 ID 或索引而不是对象本身。
- 如果深度嵌套 state 更新很复杂，请尝试将其展开扁平化。

```jsx
// 通过树状结构扁平化
export const initialTravelPlan = {
  0: {
    id: 0,
    title: '(Root)',
    childIds: [1, 42, 46],
  },
  1: {
    id: 1,
    title: 'Earth',
    childIds: [2, 10, 19, 26, 34]
  },
  2:....
}
```

### 16 状态提升与受控组件（组件间状态共享）

```jsx
export default function Accordion() {
  const [activeIndex, setActiveIndex] = useState(0);
  return (
    <>
      <h2>哈萨克斯坦，阿拉木图</h2>
      <Panel title="关于" isActive={activeIndex === 0} onShow={() => setActiveIndex(0)} >
        阿拉木图人口约200万，是哈萨克斯坦最大的城市。
      </Panel>
      <Panel title="词源" isActive={activeIndex === 1} onShow={() => setActiveIndex(1)} >
        它在 1929 年到 1997 年间都是首都。
      </Panel>
    </>
  );
}
```

- 状态提升：把 state 放到组件的公共父级，实现**任何时候只展开一个面板**类的效果。

- 然后在父组件中通过 `props` 传递信息，通过事件处理程序改变父组件的 state 。

- 非受控组件：包含不受父组件控制状态的组件

- 受控组件：组件中的重要信息是由 `props` 而不是其自身状态驱动

### 17 State的保存与重置

- 只要在相同位置渲染的是相同组件， React 就会保留状态。

```jsx
export default function App() {
  const [isFancy, setIsFancy] = useState(false);
  return (
    <div>
      {isFancy?(<Counter isFancy={true}/> ):(<Counter isFancy={false}/>)}
      <label>
        <input type="checkbox" checked={isFancy}
          onChange={e => { setIsFancy(e.target.checked) }} />
        使用好看的样式
      </label>
    </div>
  );
}
```

> **对 React 来说重要的是组件在 UI 树中的位置,而不是在 JSX 中的位置！** 下述两个组件切换后依然会保留状态。

```jsx
export default function App() {
  const [isFancy, setIsFancy] = useState(false);
  if (isFancy) {
    return ( <div> <Counter isFancy={true} />  </div> );
  }
  return ( <div> <Counter isFancy={false} /> </div> );
// 但下面将<div>替换为<section>会重置
return ( <section> <Counter isFancy={false} /> </section> );
```

- 在相同位置重置 state 的方法 : (1) 渲染在不同位置

```jsx
export default function Scoreboard() {
  const [isPlayerA, setIsPlayerA] = useState(true);
  return (
    <div>
      {isPlayerA && <Counter person="Taylor" /> }
      {!isPlayerA && <Counter person="Sarah" /> }
      <button onClick={() => { setIsPlayerA(!isPlayerA);}}> 下一位玩家！
      </button>
    </div>
  );
}
```

- 在相同位置重置 state 的方法 : (2)为一个子树指定不同的 **key 来重置**它的 state。

```jsx
export default function Scoreboard() {
  const [isPlayerA, setIsPlayerA] = useState(true);
  return (
    <div>
      {isPlayerA ? ( <Counter key="Taylor" person="Taylor" />  
                 : ( <Counter key="Sarah" person="Sarah" /> )}
      <button onClick={() => { setIsPlayerA(!isPlayerA); }}>
        下一位玩家！
      </button>
    </div>
  );
}
```

> 注意：请记住 key 不是全局唯一的。它们只能指定 **父组件内部** 的顺序。
> 
> 注意：key不仅可以用来重置state，还可以用来管理组件列表中state的顺序，如交换两组件时**状态一同交换**。

- 为被移除的组件保留 state
  
  - 把 **所有** 聊天都渲染出来，但用 CSS 把其他聊天隐藏起来。
  - 进行 **状态提升** 并在父组件中保存每个收件人的草稿消息
  - 让 `Chat` 组件通过读取 `localStorage` 对其 state 进行初始化

- 不要嵌套组件的定义，否则你会意外地导致 state 被重置。如下述代码中`<MyTextField/>` 组件会被按钮反复重置

```jsx
export default function MyComponent() {
  const [counter, setCounter] = useState(0);
  // 嵌套定义组件会导致内部状态在父组件重新渲染时被重置
  function MyTextField() {
    const [text, setText] = useState('');
    return (<input value={text} onChange={e=>setText(e.target.value)}/>);
  }

  return (
    <>
      <MyTextField />
      <button onClick={()=>{setCounter(counter+1)}}>点击{counter}次</button>
    </>
  );
}
```

### 18 Reducer

- `useReducer` 的参数为有限状态机函数和初始状态结构体，返回当前状态和dispatch函数。
  
  - 有限状态机函数第一个参数为当前状态结构体，第二个参数为动作结构体（动作类型和所需参数）
  
  - 初始状态结构体需要定义状态机的初始状态包括哪些变量

```jsx
// App.js
import { useReducer } from 'react';
import Chat from './Chat.js';
import ContactList from './ContactList.js';
import { initialState, messengerReducer } from './messengerReducer';

export default function Messenger() {
  const [state, dispatch] = useReducer(messengerReducer, initialState);
  const message = state.messages[state.selectedId];
  const contact = contacts.find((c) => c.id === state.selectedId);
  return (
    <div>
      <ContactList contacts={contacts} selectedId={state.selectedId}
        dispatch={dispatch} />
      <Chat key={contact.id} message={message} contact={contact}
        dispatch={dispatch} />
    </div>
  );
}

const contacts = [
  {id: 0, name: 'Taylor', email: 'taylor@mail.com'},
  {id: 1, name: 'Alice', email: 'alice@mail.com'},
  {id: 2, name: 'Bob', email: 'bob@mail.com'},
];
```

- 有限状态机函数内部返回动作执行的后的状态结构体
  - 通常采用switch () { case '':{}} 来匹配动作 

```jsx
// messengerReducer.js
export const initialState = {
  selectedId: 0,
  messages: {
    0: 'Hello, Taylor',
    1: 'Hello, Alice',
    2: 'Hello, Bob',
  },
};

export function messengerReducer(state, action) {
  switch (action.type) {
    case 'changed_selection': {
      return {
        ...state,
        selectedId: action.contactId,
      };
    }
    case 'edited_message': {
      return {
        ...state,
        messages: {
          ...state.messages,
          [state.selectedId]: action.message,
        },
      };
    }
    case 'sent_message': {
      return {
        ...state,
        messages: {
          ...state.messages,
          [state.selectedId]: '',
        },
      };
    }
    default: {
      throw Error('未知 action：' + action.type);
    }
  }
}
```

- dispatch 函数参数为自定义结构体，通常包含动作类型字段如 type 及该动作所需参数。

```jsx
export default function ContactList({contacts, selectedId, dispatch}) {
  return (
    <section className="contact-list">
      <ul>
        {contacts.map((contact) => (
          <li key={contact.id}>
            <button onClick={() => {
                dispatch({
                  type: 'changed_selection',
                  contactId: contact.id,
                });
              }}>
              {selectedId === contact.id ? <b>{contact.name}</b> : contact.name}
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}
```

```jsx
import { useState } from 'react';

export default function Chat({contact, message, dispatch}) {
  return (
    <section className="chat">
      <textarea value={message} placeholder={'和 ' + contact.name + ' 聊天'}
        onChange={(e) => {
          dispatch({
            type: 'edited_message',
            message: e.target.value,
          });
        }}
      />
      <br />
      <button
        onClick={() => {
          alert(`正在发送 "${message}" 到 ${contact.email}`);
          dispatch({ type: 'sent_message', });
        }}>
        发送到 {contact.email}
      </button>
    </section>
  );
}
```

### 19 Context

- **Context 让你可以编写“适应周围环境”的组件，并且根据 在哪 （或者说 在哪个 context 中）来渲染它们不同的样子。**
- **传递 Context 的方法**:
  1. 通过 `export const MyContext = createContext(defaultValue)` 创建并导出 context。
  2. 在无论层级多深的任何子组件中，把 context 传递给 `useContext(MyContext)` Hook 来读取它。
  3. 在父组件中把 children 包在 `<MyContext.Provider value={...}>` 中来提供 context。

```jsx
// App.jsx
import { useState, useContext } from 'react';
import { places } from './data.js';
import { getImageUrl } from './utils.js';
import { ImageSizeContext } from './Context.js';

export default function App() {
  const [isLarge, setIsLarge] = useState(false);
  const imageSize = isLarge ? 150 : 100;
  return (
    <ImageSizeContext.Provider value={imageSize} >
      <label>
        <input type="checkbox" checked={isLarge}
          onChange={e => { setIsLarge(e.target.checked); }}
        /> Use large images
      </label>
      <hr />
      <List />
    </ImageSizeContext.Provider>
  )
}

function List() {
  const listItems = places.map(place =>
    <li key={place.id}> <Place place={place} /> </li>
  );
  return <ul>{listItems}</ul>;
}

function Place({ place }) {
  return (
    <>
      <PlaceImage place={place} />
      <p> <b>{place.name}</b> {': ' + place.description} </p>
    </>
  );
}

function PlaceImage({ place }) {
  const imageSize = useContext(ImageSizeContext);
  return (
    <img
      src={getImageUrl(place)}
      alt={place.name}
      width={imageSize}
      height={imageSize}
    />
  );
}
```

```jsx
// Context.jsx
import { createContext } from 'react';

export const ImageSizeContext = createContext(500);
```

- Context 会穿过中间的任何组件，**useContext会寻找最近的Context获取参数**。

- 在使用 context 之前，**先试试传递 props 或者将 JSX 作为 `children` 传递**。
  
  - 直接传递 props 让数据流变得更加清晰。
  
  - **抽象组件并将 JSX 作为 `children` 传递给它们。** 如果你通过很多层不使用该数据的中间组件（并且只会向下传递）来传递数据，这通常意味着你在此过程中忘记了抽象组件。举个例子，你可能想传递一些像 `posts` 的数据 props 到不会直接使用这个参数的组件，类似 `<Layout posts={posts} />`。取而代之的是，让 `Layout` 把 `children` 当做一个参数，然后渲染 `<Layout><Posts posts={posts} /></Layout>`。这样就减少了定义数据的组件和使用数据的组件之间的层级。

- **Context 的使用场景**：
  
  - **主题：** 如果你的应用允许用户更改其外观（例如暗夜模式），你可以在应用顶层放一个 context provider，并在需要调整其外观的组件中使用该 context。
  - **当前账户：** 许多组件可能需要知道当前登录的用户信息。将它放到 context 中可以方便地在树中的任何位置读取它。某些应用还允许你同时操作多个账户（例如，以不同用户的身份发表评论）。在这些情况下，将 UI 的一部分包裹到具有不同账户数据的 provider 中会很方便。
  - **路由：** 大多数路由解决方案在其内部使用 context 来保存当前路由。这就是每个链接“知道”它是否处于活动状态的方式。如果你创建自己的路由库，你可能也会这么做。
  - **状态管理：** 随着你的应用的增长，最终在靠近应用顶部的位置可能会有很多 state。许多遥远的下层组件可能想要修改它们。通常将 reducer 与 context 搭配使用来管理复杂的状态并将其传递给深层的组件来避免过多的麻烦。

### 20 reducer 与 context 结合

- 为子组件提供 state 和 dispatch 函数：
  1. 创建两个 context (一个用于 state,一个用于 dispatch 函数)。
  2. 让组件的 context 使用 reducer。
  3. 使用组件中需要读取的 context。

```jsx
// App.js
import AddTask from './AddTask.js';
import TaskList from './TaskList.js';
import { TasksProvider } from './TasksContext.js';

export default function TaskApp() {
  return (
    <TasksProvider> <h1>Day off in Kyoto</h1>
      <AddTask />
      <TaskList />
    </TasksProvider>
  );
}
```

```jsx
import { createContext, useReducer } from 'react';

export const TasksContext = createContext(null);
export const TasksDispatchContext = createContext(null);

export function TasksProvider({ children }) {
  const [tasks, dispatch] = useReducer( tasksReducer, initialTasks );

  return (
    <TasksContext.Provider value={tasks}>
      <TasksDispatchContext.Provider value={dispatch}>
        {children}
      </TasksDispatchContext.Provider>
    </TasksContext.Provider>
  );
}

function tasksReducer(tasks, action) {
  switch (action.type) {
    case 'added': {
      return [...tasks, {id: action.id,text: action.text,done: false}];
    }
    case 'changed': {
      return tasks.map(t => {
        if (t.id === action.task.id) {return action.task;} 
        else {return t;}
      });
    }
    case 'deleted': {
      return tasks.filter(t => t.id !== action.id);
    }
    default: {
      throw Error('Unknown action: ' + action.type);
    }
  }
}

const initialTasks = [
  { id: 0, text: 'Philosopher’s Path', done: true },
  { id: 1, text: 'Visit the temple', done: false },
  { id: 2, text: 'Drink matcha', done: false }
];
```

- 你可以通过将所有传递信息的代码移动到单个文件中来进一步整理组件。
  - 你可以导出一个像 `TasksProvider` 可以提供 context 的组件。
  - 你也可以导出像 `useTasks` 和 `useTasksDispatch` 这样的自定义 Hook。
- 你可以在你的应用程序中大量使用 context 和 reducer 的组合。
