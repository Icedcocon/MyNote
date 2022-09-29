```javascript
// #############################################################
// 语句（statement）与表达式（expression）
// #############################################################
var a = 1 + 3;                  // 声明并赋值；JS执行单位为行（line）;
var a = 1 + 3 ; var b = 'abc';  // 语句以分号结尾;多个语句可以写在一行内;
;;;                             // 空语句
1 + 3;'abc';                    // 表达式后加分号会让JS引擎视为语句，这无意义；

// ############################################################
// 变量
// #############################################################
var a = 1;                        // 声明变量a，在变量a与数值1间建立引用；
a = 1;                            // 等效（不推荐）；
var a;                            // 变量声明；该变量的值是undefined；
a = 1;                            // 变量赋值；变量是对“值”的具名引用；
var a, b;                         // 用var声明多个变量；
var a = 1; a = 'hello';           // 变量可以随意更改类型；
var x = 1; var x;                 // 用var对已经存在的变量的第二次声明是无效的；
var x = 1; var x = 2;             // 若第二次声明时还赋值，则覆盖之前的值；

// 所有变量的声明语句会被提升到代码的头部，这就叫做变量提升（hoisting）
console.log(a); var a = 1;        // undefined；变量a已声明，但还未赋值；
var a; console.log(a); a = 1;     // 实际执行顺序；

// #############################################################
// 标志符（变量名、函数名等）
// #############################################################
arg0                // 第一个字符可以是任意 Unicode 字母
_tmp                // 第一个字符可以是下划线（_）
$elem               // 第一个字符可以是美元符号（$）
π                   // 第一个字符可以是任意 Unicode 字母

1a                  // 第一个字符不能是数字
23                  // 同上
***                 // 标识符不能包含星号
a+b                 // 标识符不能包含加号
-d                  // 标识符不能包含减号或连词线

var 临时变量 = 1;    // 中文是合法的标识符，可以用作变量名

// #############################################################
// 注释
// #############################################################
//                               这是单行注释
/*
                                 这是多行注释
*/
x = 1; <!-- x = 2;            // 兼容 HTML 代码，<!--和-->也被视为单行注释。
--> x = 3;                    // -->只有在行首，才会被当成单行注释

// #############################################################
// 区块（block）
// #############################################################
{var a = 1;} a;              // a=1；对于var声明的变量，区块不构成单独的作用域

// #############################################################
// 条件语句（if...else 结构、switch 结构、三元运算符）
// #############################################################
if (m === 3) {              // if...else 结构
  // 满足条件时，执行的语句
} else {
  // 不满足条件时，执行的语句
}
if (m === 3) {m += 1;}      // if条件后加上大括号，将多个语句合并成一个
if (x = 2) {                // 不报错；将2赋值给x，判断x的值(2)的布尔值(true)
if (2 = x) {                // 报错
if (m !== 1)
if (n === 2) console.log('hello');    // 与下方else配对
else console.log('world'); // else代码块总是与离自己最近的那个if语句配对。

var x = 2;
switch (x+2) {              // switch 结构
  case "banana":
    // ...
    break;                  // 每个case都要有break语句，否则会向下继续执行
  case true:                // switch语句与case语句的比较为'==='不进行类型转换
    // ...
    break;
  case 2 + 2:               // switch语句部分和case语句部分都可以使用表达式
    // ...
    break;
  default:
    // ...
}

(条件) ? 表达式1 : 表达式2       // 条件为true返回表达式1的值，否则返回表达式2的值
var even = (n % 2 === 0) ? true : false;                     // 判断奇偶
var msg = '数字' + n + '是' + (n % 2 === 0 ? '偶数' : '奇数'); // 输出提示

// #############################################################
// 循环语句(while、for、do...while、label)
// #############################################################
while (条件) 语句;
while (条件) {
    语句;
}

for (初始化表达式; 条件; 递增表达式) {
  语句
}

do {                     // do...while循环至少运行一次
  语句
} while (条件);           // 分号不要省略

break;                   // break语句用于跳出代码块或循环。
continue;                // continue语句用于立即终止本轮循环，返回循环结构的头部

label:                   // JS允许语句的前面有标签（label），相当于定位符
  语句
top:                     // 标签通常与break语句和continue语句配合使用；
  for (var i = 0; i < 3; i++){
    for (var j = 0; j < 3; j++){
      if (i === 1 && j === 1) break top;
      console.log('i=' + i + ', j=' + j);
    }
  }
foo: {                   // 
  console.log(1);
  break foo;
  console.log('本行不会输出');
}
console.log(2);
```

# 数据类型-概述

```javascript
// #############################################################
// 6种数据类型
// #############################################################
typeof 1; typeof 3.14    //数值（number）：整数和小数
typeof 'Hello World'     //字符串（string）：文本
typeof false             //布尔值（boolean）：表示真伪的两个特殊值
typeof undefined         //undefined（undefined）：表示“未定义”或不存在
typeof null              //null（object）：表示空值，即此处的值为空。
typeof window            //对象（object）：分为狭义的对象、数组、函数

typeof {}                //狭义的对象（object）
typeof []                //数组（array）
typeof function () {}    //函数（function）

// 原始类型（primitive type）：数值、字符串、布尔值
// 合成类型（complex type）：对象
// 特殊值：undefined、null

// #############################################################
// typeof运算符
// #############################################################
typeof                    //运算符
instanceof                //运算符
Object.prototype.toString //方法

v                         // ReferenceError: v is not defined
typeof v                  // typeof可以用来检查一个没有声明的变量，而不报错。

var o = {}; o instanceof Array;    //false instanceof运算符可以区分数组和对象
var o = []; o instanceof Array;    //true
```

# 数据类型-null, undefined 和布尔值

```javascript
// #############################################################
// null, undefined
// #############################################################
Number(null)                  // 0
Number(undefined)             // NaN
null == undefined             // ture
null === undefined            // false

// null表示空值，即该处的值现在为空
// 调用函数时，某个参数未设置任何值，这时就可以传入null，表示该参数为空。

var i; i                      // undefined 变量声明了，但没有赋值
function f(x) return x; f()   // undefined 函数未传参，则该参数为undefined
var o = new Object(); o.p     // undefined 象没有赋值的属性
function f() {} f()           // undefined 数没有返回值时，默认返回undefined

// #############################################################
// 布尔值
// #############################################################
// 下列运算符会返回布尔值：
// (1) 前置逻辑运算符： ! (Not)
// (2) 相等运算符：===，!==，==，!=
// (3) 比较运算符：>，>=，<，<=

// 除了下面六个值被转为false，其他值都视为true。
// (1) undefined
// (2) null
// (3) false
// (4) 0
// (5) NaN
// (6) ""或''（空字符串）

if ('') console.log('true');        // 没有任何输出
if ([]) console.log('true');        // true 空数组（[]）对应的布尔值是true
if ({}) console.log('true');        // true 空对象（{}）对应的布尔值是true
```

# 数据类型-数值

```javascript
// #############################################################
// 数值概述（整数/浮点、数值精度、数值范围）
// #############################################################
// JS的整数、小数都是浮点数，且不是精确值
1 === 1.0                       // true 数字以64位浮点数形式储存（包括整数）
0.1 + 0.2 === 0.3               // false 浮点数不是精确的值
(0.3 - 0.2) === (0.2 - 0.1)     // false 
0.3 / 0.1                       // 2.9999999999999996 浮点数不是精确的值

// JavaScript 浮点数的64个二进制位，从最左边开始，是这样组成的。
// 第1位：符号位（0表示正数、1表示负数）           符号位决定了一个数的正负
// 第2位到第12位(11位)：指数部分                 指数部分决定了数值的大小
// 第13位到第64位(52位)：小数部分/有效数字        小数部分决定了数值的精度
// 若指数部分为0-2047，则有效数字首位默认为1，小数保存在52位小数部分，共计53位
(-1)^符号位 * 1.xx...xx * 2^指数部分

// 精度最多只能到53个二进制位
Math.pow(2, 53)            // 9007199254740992 小于2的53次方的值可以精确计算
Math.pow(2, 53) + 1        // 9007199254740992 大于该值，则整数运算出现错误
9007199254740992111        // 9007199254740992000 多出的有效数字无法保存变为0

// 数值范围为2^1024到2^-1023（开区间）
Math.pow(2, 1024)          // Infinity ≥2^1024次方，发生“正向溢出”
Math.pow(2, -1075)         // 0 ≤2^-1075（指数-1023+小数52位），发生“负向溢出”
Number.MAX_VALUE           // 1.7976931348623157e+308
Number.MIN_VALUE           // 5e-324  返回可以表示的具体的最小(大)值

// #############################################################
// 数值的表示法（进制、科学计数法及其自动转换）
// #############################################################
// 进制
35                         // 字面值十进制
0xFF                       // 字面值十六进制

// 科学计数法
123e3                      // 123000
123e-3                     // 0.123  
-3.1E+12                   //        
.1e-23                     //        

//两种情况，JavaScript 会自动将数值转为科学计数法表示，其他情况都采用字面形式直接表示
1234567890123456789012     // 1.2345678901234568e+21 小数点前的数字多于21位
123456789012345678901      // 123456789012345680000  小数点前的数字少于21位
0.0000003                  // 3e-7                   小数点后的零多于5个
0.000003                   // 0.000003               小数点后的零少于5个

// #############################################################
// 数值的进制（进制、自动转化、基数错误、前导0）
// #############################################################
// JavaScript 对整数提供四种进制的表示方法：十进制、十六进制、八进制、二进制。
// 十进制：没有前导0的数值。
// 八进制：有前缀0o或0O的数值，或者有前导0、且只用到0-7的八个阿拉伯数字的数值。
// 十六进制：有前缀0x或0X的数值。
// 二进制：有前缀0b或0B的数值。

// JS会自动将八进制、十六进制、二进制转为十进制
0xff         // 255    
0o377        // 255    
0b11         // 3     

// 八进制、十六进制、二进制出现不属于该进制的数字会报错
0xzz         // 报错    
0o88         // 报错
0b22         // 报错

// 通常，有前导0的数值会被视为八进制，如果前导0后面有数字8和9，则该数值被视为十进制
077          // 63     
088          // 88     
// 前导0表示八进制容易造成混乱。ES5 的严格模式和 ES6，已经废除了这种表示法


// #############################################################
// 特殊数值（正零和负零、NaN、Infinity）
// #############################################################
// 正零和负零
// (1)64位浮点数中存在一个二进符号位，因此JS存在一个+0和一个-0，仅符号位不同，二者等价
-0 === +0            // true
0 === -0             // true
0 === +0             // true
// (2)几乎所有场合，正零和负零都会被当作正常的0
+0                   // 0     
-0                   // 0 
(-0).toString()      // '0'        
(+0).toString()      // '0'
// (3)只有+-0当作分母时，除以正零得到+Infinity，反之为负
(1 / +0) === (1 / -0)// false 

// NaN 表示“非数字”（Not a Number）
// (1)常见于将字符串解析成数字出错的场合。
5 - 'x'              // NaN 
// (2)一些数学函数的运算结果会出现NaN
Math.acos(2)         // NaN 
Math.log(-1)         // NaN
Math.sqrt(-1)        // NaN
// (3)0除以0也会得到NaN
0 / 0                // NaN 
// (4)NaN不是独立的数据类型
typeof NaN           // 'number' 
// (5)NaN运算规则
NaN === NaN          // false NaN不等于任何值，包括它本身
[NaN].indexOf(NaN)   // -1 数组的indexOf方法内部使用的是严格相等运算符，因此不等
Boolean(NaN)         // false NaN在布尔运算时被当作false
NaN + 32             // NaN NaN与任何数（包括它自己）的运算，得到的都是NaN

// Infinity 
// (1)三种出现Infinity 的情况：
Math.pow(2, 1024)    // Infinity 正的数值太大
0 / 0                // NaN      负的数值太小
1 / 0                // Infinity 非0数值除以0
// (2)Infinity有正负之分
Infinity === -Infinity // false        
1 / -0                 // -Infinity    Infinity表示正的无穷
-1 / -0                // Infinity     -Infinity表示负的无穷
// (3)Infinity的比较运算
Infinity > 1000        // true         Infinity大于一切数值（除了NaN）
-Infinity < -1000      // true         -Infinity小于一切数值（除了NaN）
Infinity > NaN         // false        Infinity与NaN比较，总是返回false
-Infinity > NaN        // false
Infinity < NaN         // false
-Infinity < NaN        // false
// (4)Infinity运算规则
5 * Infinity           // Infinity    四则运算，符合无穷的数学计算规则
5 - Infinity           // -Infinity
Infinity / 5           // Infinity
5 / Infinity           // 0
0 * Infinity           // NaN
0 / Infinity           // 0
Infinity / 0           // Infinity
Infinity + Infinity    // Infinity  Infinity加上Infinity，返回的还是Infinity
Infinity * Infinity    // Infinity  Infinity乘以Infinity，返回的还是Infinity
Infinity - Infinity    // NaN       Infinity减去Infinity，得到NaN
Infinity / Infinity    // NaN       Infinity除以Infinity，得到NaN
null * Infinity        // NaN       Infinity与null计算时，null会转成0
null / Infinity        // 0
Infinity / null        // Infinity
undefined + Infinity   // NaN        Infinity与undefined计算，返回的都是NaN
undefined - Infinity   // NaN
undefined * Infinity   // NaN
undefined / Infinity   // NaN
Infinity / undefined   // NaN

// #############################################################
// 与数值相关的全局方法
// #############################################################
// parseInt()
// (1)头部空格与非字符串
parseInt('123')     // 123 parseInt方法用于将字符串转为整数
parseInt('   81')   // 81  如果字符串头部有空格，空格会被自动去除
parseInt(1.23)      // 1 如果parseInt的参数不是字符串，则会先转为字符串再转换。
parseInt('1.23')    // 1 等同于上面
// (2)首字符不能转换
parseInt('abc')     // NaN 若字符串首字符不能转化为数字返回NaN。
parseInt('.3')      // NaN parseInt要么返回十进制整数，要么返回NaN
parseInt('')        // NaN
parseInt('+')       // NaN 
parseInt('+1')      // 1   后面跟着数字的正负号除外 
// (3)不同进制
parseInt('0x10')    // 16 字符串以0x或0X开头，parseInt会将其按照十六进制数解析
parseInt('011')     // 11 字符串以0开头，将其按照10进制解析。
// (4)对于会自动转为科学计数法的数字，parseInt会先转化后变为字符串
parseInt(1000000000000000000000.5) // 1 
parseInt('1e+21')                  // 1 等同于上面
parseInt(0.0000008)                // 8 
parseInt('8e-7')                   // 8 等同于上面
// (5)parseInt第二个参数（2到36之间），表示被解析的值的进制，默认是十进制转十进制。
parseInt('1000')                  // 1000
parseInt('1000', 10)              // 1000 等同于上面
parseInt('1000', 2)               // 8
parseInt('1000', 6)               // 216
parseInt('1000', 8)               // 512
// (6)parseInt第二个参数的异常情况
parseInt('10', 37)                // NaN 超出2到36之间，则返回NaN
parseInt('10', 1)                 // NaN 第二个参数不是数值，会被转为一个整数
parseInt('10', 0)                 // 10  第二个参数是0则直接忽略
parseInt('10', null)              // 10  第二个参数是null则直接忽略
parseInt('10', undefined)         // 10  第二个参数是undefined则直接忽略
// (7)parseInt第一个参数与第二个参数不匹配
parseInt('1546', 2)               // 1   从最高位开始，只返回可以转换的数值
parseInt('546', 2)                // NaN 如果最高位无法转换，则直接返回NaN。
// (8)第一个参数不是字符串，结果会出人意料
parseInt(0x11, 36)                // 43  
parseInt(0x11, 2)                 // 1
parseInt(String(0x11), 36)        // 等同于43
parseInt(String(0x11), 2)         // 等同于1
parseInt('17', 36)                // 等同于43
parseInt('17', 2)                 // 等同于1
parseInt(011, 2)                  // NaN 因此八进制的前缀0，尤其需要注意
parseInt(String(011), 2)          // 等同于上面
parseInt(String(9), 2)            // 等同于上面

// parseFloat() 
// (1)parseFloat方法用于将一个字符串转为浮点数
parseFloat('3.14')           // 3.14 
// (2)如果字符串符合科学计数法，则会进行相应的转换。
parseFloat('314e-2')         // 3.14 
parseFloat('0.0314E+2')      // 3.14
// (3)包含不能转换的字符，则返回最后一个能转换的字符之前的部分，之后截断
parseFloat('3.14more non-digit characters') // 3.14 
parseFloat('\t\v\r12.34\n ') // 12.34 自动过滤字符串前导的空格。
// (4)参数不是字符串，则会先转为字符串再转换。
parseFloat([1.23])           // 1.23 
parseFloat(String([1.23]))   // 1.23 等同于上面
// (5)字符串首字符不能转化为浮点数，返回NaN。
parseFloat([])               // NaN 
parseFloat('FF2')            // NaN
parseFloat('')               // NaN
// (6)parseFloat与Number的区别
parseFloat(true)             // NaN
Number(true)                 // 1
parseFloat(null)             // NaN
Number(null)                 // 0
parseFloat('')               // NaN parseFloat会将空字符串转为NaN
Number('')                   // 0
parseFloat('123.45#')        // 123.45
Number('123.45#')            // NaN

// isNaN()
// (1)可以用来判断一个值是否为NaN
isNaN(NaN)                   // true  
isNaN(123)                   // false
// (2)isNaN只对数值有效，其他值会被先转成数值
isNaN('Hello')               // true 
isNaN(Number('Hello'))       // true 等同于上面
// (3)对于对象和数组，isNaN也返回true
isNaN({})                    // true 
isNaN(Number({}))            // true 等同于上面
isNaN(['xzy'])               // true
isNaN(Number(['xzy']))       // true 等同于上面
// (4)对于空数组返回false
isNaN([])                    // false 
isNaN([123])                 // false 对于只有一个数值成员的数组返回false
isNaN(['123'])               // false 能被Number函数转成数值的数组
// (5)使用前先判断类型
function myIsNaN(value) {
  return typeof value === 'number' && isNaN(value);
}
// (6)判断NaN更可靠的方法是，利用NaN为唯一不等于自身的值的这个特点，进行判断。
function myIsNaN(value) {
  return value !== value;
}

// isFinite()
// (1)isFinite方法返回一个布尔值，表示某个值是否为正常的数值
isFinite(Infinity)         // false   
isFinite(-Infinity)        // false   
// (2)除了Infinity、-Infinity、NaN和undefined这几个值会返回false
isFinite(NaN)              // false   
isFinite(undefined)        // false   
isFinite(null)             // true    
isFinite(-1)               // true    
```

# 数据类型-字符串

```javascript

```
