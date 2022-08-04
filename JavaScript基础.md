## 一.认识JS

### 1.1 概念

- HTML(骨架，元素，结构)CSS(表现，效果，状态)JS(响应行为，交互，复杂操作)

- JavaScript(JS)是基于原型，动态类型，解释型，弱类型 脚本语言。
  
  - 传统语言： OOL 基于类/对象=>实例
  
  - Javascript： 基于原型，对象(万物皆对象)，原型可以指定，方法可灵活使用
  
  - 脚本语言： 依赖环境(宿主环境)运行，浏览器可以使用DOM/BOM等，还有nodeJS(服务端)
  
  - 弱类型/动态类型： 变量声明不需要规定类型，并且可以相互转换
  
  - 解释型： 没有编译过程，不生成其他可执行文件，完成语法分析后逐行解析执行(暂时这么理解)

- JavaScript在`客户端`的三大组成： （语法，浏览器，页面元素）  
  
  - ECMAScript es5 6 7 语法，使用规则(等同于html里的<>和css里的{})，JS的本质
  
  - es是js的标准 js是es的实现
  
  - BOM BrowserObjectModel 浏览器对象模型，浏览器提供的工具箱
  
  - DOM DocumentObjectModel 文档对象模型，页面元素和方法的整合工具箱

<img title="" src="https://cdn.nlark.com/yuque/0/2020/png/335089/1578574917022-76618071-003e-43b2-89c7-ea3aa39e161d.png" alt="image.png" style="zoom:80%;" width="465" data-align="center">

### 1.2 三种书写位置

JS有3种书写位置，分别为行内、内嵌和外部

**行内JS**

- 可以将单行或少量JS代码写在HTML标签的事件属性中（以on开头的属性），如：`onclick`(不常用，不推荐)

```html
<input type="button" value="点击" onclick="alert('这是写在标签属性中的JS代码!')">
```

- 单双引号的使用：在HTML中推荐使用双引号，在JS中推荐使用单引号

- 行内JS的缺点：

- - 可读性差，在HTML中编写大量JS代码时，不方便阅读
  - 引号易错，引号多层嵌套匹配时，容易混淆

**内嵌JS**

- 可以将多行JS代码写到`<script></script>`标签中
- `<script></script>`标签可以放在HTML的`<body>`和`<head>`中，一般放在`<body>`中的最后
- JS代码中不能出现`</script>`字符串，可以通过转义字符来解决：`<\/script>`

```html
<script>
    alert('这是写在script标签中的JS代码!')
</script>
```

**外部JS**

- JS代码可以放在外部的.js文件中，通过src属性引入`<script src="example.js"></script>`

- 放在外部的好处：

- - 利于HTML页面代码结构化
  - 可维护性强、可缓存、适应未来

- Script标签如果引入了外部文件，则不能再在`<script></script>`标签中编写代码

```js
//test.js
alert('这是写在外部.js文件中的JS代码！')
```

在html文件中引用：

```html
<script src="test.js"></script>
```

### 1.3 输入

可以在JS中使用`prompt(info)`在浏览器弹出一个输入框，供用户输入

```html
<script>
    prompt('请输入您的姓名：')
</script>
```

### 1.4 输出

`**alert()**`：弹出一个警告框

```html
<script>
        alert('密码不能为空！')
</script>
```

`**document.write()**`：向body中输出内容

```html
<script>
        document.write('你好鸭~')
</script>
```

`**console.log()**`：向控制台输出内容

```html
<script>
    console.log('hello js'')
</script>
```

### 1.5 语句

- JS代码是从上往下执行的（而且是阻断式执行）
- 每行结尾的分号可有可无（建议写分号）
- JS对大小写敏感
- 字符串使用单引号或双引号均可
- 在文本字符串中使用反斜杠换行：`document.write("Hello\World!");`

### 1.6 注释

- 单行注释：//（默认快捷键：Ctrl+/）
- 多行注释：/**/（默认快捷键：ALt+Shitf+A）
- 一般在行末使用注释

```html
<script>
// 单行注释 
/* 多
   行
   注
   释 */
</script>
```

## 二.变量、数据类型

### 2.1 变量的使用

- 变量在使用时分为声明和赋值：
  
  - 声明变量  
    
    - 声明变量后，计算机会自动为变量分配内存空间
  
  - 赋值
    
    - = 用来把右边的值赋给左边的变量
  
  - 初始化：声明一个变量并赋值， 称之为变量的初始化

```js
var age; //  声明一个 名称为age 的变量 
age = 10; // 给 age  这个变量赋值为 10   
```

- 同时声明多个变量：写一个 var， 多个变量名之间使用英文逗号隔开

```js
var age = 20,  name = 'pikaka', sex = '男';
```

1. 声明变量特殊情况 

![image.png](https://cdn.nlark.com/yuque/0/2020/png/335089/1578573175253-8342d4fe-a0ee-43d6-b675-b1784611eaf4.png)

### 2.2 数据类型

- JS是一种弱类型语言，在定义变量时不需要指定类型，变量可以存储任何类型的值。

- JS数据类型分为**简单类型**与**复杂类型**

- **简单类型**：
  
  - 值类型：简单数据类型/基本数据类型，在存储时变量中存储的是值本身，因此叫做值类型，包括：
  
  - string ，number，boolean，undefined，null 

![image.png](https://cdn.nlark.com/yuque/0/2020/png/335089/1578574533110-e876d169-d26f-4a0e-907b-31b08cc79079.png)

- **复杂类型**
  
  - 引用类型：复杂数据类型，在存储时变量中存储的仅仅是地址（引用），因此叫做引用数据类型，通过 new 关键字创建的对象（系统对象、自定义对象），如 Object、Array、Date等 .

- **ES6新增**
  
  - Symbol ,  BigInt

- **类型检测**
  
  - 暂时用typeof操作符来检测数据类型

```js
    console.log( typeof 10 );       //number
    console.log( typeof "10" );     //string
    console.log( typeof true );     //boolean    
    console.log( typeof undefined );//undefined
    console.log( typeof [] );       //object
    console.log( typeof {} );       //object
    console.log( typeof window );   //object

    console.log( typeof null );     //object 需要注意的是其实null
    console.log( typeof function gd(){} ); //function
```
