### JavaScript 的数据类型，共有六种：

- 数值（number）
- 字符串（string）
- 布尔值（boolean）
- undefined：表示“未定义”或不存在 
- null：表示空值
- 对象（object）：各种值组成的集合

**JavaScript 引擎的工作方式是，先解析代码，获取所有被声明的变量，然后再一行一行地运行。这造成的结果，就是所有的变量的声明语句，都会被提升到代码的头部，这就叫做变量提升**

``` js
console.log(a);
var a = 1;
```

上面代码首先使用`console.log`方法，在控制台（`console`）显示变量 **a** 的值。这时变量  **a** 还没有声明和赋值，所以这是一种错误的做法，但是实际上不会报错。因为存在变量提升，

**typeof : 判断未定义变量**

```js
if (typeof v === "undefined") {} 
```

**null是一种数据类型，历史原因导致 typeof 时显示 object **

```js
typeof null // "object"
```

 **JavaScript 预期某个位置应该是布尔值，会将该位置上现有的值自动转为布尔值。转换规则是除undefined、null、false、0、NaN、""或''（空字符串）六个值被转为false，其他值都视为true。**



**字符串可以被视为字符数组，因此可以使用数组的方括号运算符，用来返回某个位置的字符（位置编号从0开始）。**

```js
var s = 'hello'; s[0] // "h" s[1] // "e" s[4] // "o" 
```

如果方括号中的数字超过字符串的长度，或者方括号中根本不是数字，则返回`undefined`

但是，字符串与数组的相似性仅此而已。实际上，无法改变字符串之中的单个字符。

V8 引擎规定，如果行首是大括号，一律解释为对象。不过，为了避免歧义，最好在大括号前加上圆括号。

这种差异在eval语句（作用是对字符串求值）中反映得最明显

```js
eval('{foo: 123}') // 123 eval('({foo: 123})') // {foo: 123} 
```

上面代码中，如果没有圆括号，eval将其理解为一个代码块；加上圆括号以后，就理解成一个对象。

读取对象的属性，有两种方法，一种是使用点运算符，还有一种是使用方括号运算符

```js
var obj = {   p: 'Hello World' };  obj.p // "Hello World" obj['p'] // "Hello World" 
```

查看一个对象本身的所有属性，可以使用 `Object.keys` 方法。

```js
var obj = {   key1: 1,   key2: 2 };  Object.keys(obj); // ['key1', 'key2'] 
```

`delete`命令用于删除对象的属性，删除成功后返回true。

```js
var obj = { p: 1 }; Object.keys(obj) // ["p"]  delete obj.p // true obj.p // undefined Object.keys(obj) // [] 
```

in 运算符用于检查对象是否包含某个属性

```js
var obj = { p: 1 }; 'p' in obj // true 'toString' in obj // true 
```

`` for...in``循环用来遍历一个对象的全部属性。

```js
var obj = {a: 1, b: 2, c: 3};  for (var i in obj) {   console.log('键名：', i);   console.log('键值：', obj[i]); } // 键名： a // 键值： 1 // 键名： b // 键值： 2 // 键名： c // 键值： 3 
```

函数参数如果是原始类型的值（数值、字符串、布尔值），传递方式是传值传递，函数体内修改参数值，不会影响到函数外部。

函数参数是复合类型的值（数组、对象、其他函数），传递方式是传址传递，函数内部修改参数，将会影响到原始值。



立即调用的函数表达式

```js
(function(){ /* code */ }()); // 或者 (function(){ /* code */ })(); 
```

``eval``命令接受一个字符串作为参数，并将这个字符串当作语句执行

```js
eval('var a = 1;'); a // 1 
```

JavaScript 使用一个**32**位整数，保存数组的元素个数。这意味着，数组成员最多只有 4294967295 个（232 - 1）个，也就是说length属性的最大值就是 4294967295。

只要是数组，就一定有length属性。该属性是一个动态的值，等于键名中的最大整数加上1。

数组是一种动态的数据结构，可以随时增减数组的成员。

length属性是可写的。如果人为设置一个小于当前成员个数的值，该数组的成员会自动减少到length设置的值。

清空数组的一个有效方法，就是将length属性设为0。

检查某个键名是否存在的运算符in，适用于对象，也适用于数组

```js
var arr = [ 'a', 'b', 'c' ]; 2 in arr  // true '2' in arr // true 4 in arr // false 
```

如果数组的某个位置是空位，in运算符返回false

JavaScript 共提供10个算术运算符，用来完成基本的算术运算。

- 加法运算符：x + y
- 减法运算符： x - y
- 乘法运算符： x * y
- 除法运算符：x / y
- 指数运算符：x ** y
- 余数运算符：x % y
- 自增运算符：++x 或者 x++
- 自减运算符：--x 或者 x--
- 数值运算符： +x
- 负数值运算符：-x

数值运算符（+）同样使用加号，但它是一元运算符（只需要一个操作数），而加法运算符是二元运算符（需要两个操作数）。

数值运算符的作用在于可以将任何值转为数值（与Number函数的作用相同）

```js
+true // 1 +[] // 0 +{} // NaN var x = 1; -x // -1 -(-x) // 1 
```

负数值运算符（-），也同样具有将一个值转为数值的功能，只不过得到的值正负相反。连用两个负数值运算符，等同于数值运算符。

指数运算符（**）完成指数运算，前一个运算子是底数，后一个运算子是指数。

2 ** 4 // 16 3**4 // 81 

指数运算符是右结合，而不是左结合。即多个指数运算符连用时，先进行最右边的计算。



JavaScript 提供两种相等运算符：==和===。

简单说，它们的区别是相等运算符（==）比较两个值是否相等，严格相等运算符（===）比较它们是否为“同一个值”。如果两个值不是同一类型，严格相等运算符（===）直接返回false，而相等运算符（==）会将它们转换成同一个类型，再用严格相等运算符进行比较。



布尔运算符用于将表达式转为布尔值，一共包含四个运算符。

- 取反运算符：!
- 且运算符：&&
- 或运算符：||
- 三元运算符：?:

```js
't' ? 'hello' : 'world' // "hello" 0 ? 'hello' : 'world' // "world" 
```



```html
<a href="http://example.com" onclick="f(); return false;">点击</a>
<a href="javascript: void(f())">文字</a>
<a href="javascript: void(document.form.submit())">
  提交
</a>
```

上面代码中，点击链接后，会先执行onclick的代码，由于onclick返回false，所以浏览器不会跳转到 example.com。

Number()、String()和Boolean()手动将各种类型的值，分别转换成数字、字符串或者布尔值。

对于某些复合类型的数据，console.table方法可以将其转为表格显示。

```js
var languages = [   { name: "JavaScript", fileExtension: ".js" },   { name: "TypeScript", fileExtension: ".ts" },   { name: "CoffeeScript", fileExtension: ".coffee" } ];  console.table(languages); 
```

dir方法用来对一个对象进行检查（inspect），并以易于阅读和打印的格式显示。

```js
console.log({f1: 'foo', f2: 'bar'}) // Object {f1: "foo", f2: "bar"}  console.dir({f1: 'foo', f2: 'bar'}) // Object //   f1: "foo" //   f2: "bar" //   __proto__: Object 

console.time()，console.timeEnd()可以算出一个操作所花费的准确时间。

console.time('Array initialize');  var array= new Array(1000000); for (var i = array.length - 1; i >= 0; i--) {   array[i] = new Object(); };  console.timeEnd('Array initialize'); // Array initialize: 1914.481ms 
```

$_属性返回上一个表达式的值。

2 + 2 // 4 $_ // 4 

$0 - $4

控制台保存了最近5个在 Elements 面板选中的 DOM 元素，$0代表倒数第一个（最近一个），$1代表倒数第二个，以此类推直到$4。



debugger语句主要用于除错，作用是设置断点。如果有正在运行的除错工具，程序运行到debugger语句时会自动停下。如果没有除错工具，

debugger语句不会产生任何结果，JavaScript 引擎自动跳过这一句。

Chrome 浏览器中，当代码运行到debugger语句时，就会暂停运行，自动打开脚本源码界面。



### 数组

push方法用于在数组的末端添加一个或多个元素，并返回添加新元素后的数组长度。

pop方法用于删除数组的最后一个元素，并返回该元素。

push和pop结合使用，就构成了“后进先出”的栈结构（stack）。

shift()方法用于删除数组的第一个元素，并返回该元素。注意，该方法会改变原数组。

push和shift结合使用，就构成了“先进先出”的队列结构（queue）。

unshift()方法用于在数组的第一个位置添加元素，并返回添加新元素后的数组长度。

join()方法以指定参数作为分隔符，将所有数组成员连接为一个字符串返回。

```js
var a = [1, 2, 3, 4];  a.join(' ') // '1 2 3 4' a.join(' | ') // "1 | 2 | 3 | 4" a.join() // "1,2,3,4" 
```

map方法将数组的所有成员依次传入参数函数，然后把每一次的执行结果组成一个新数组返回。

```js
var numbers = [1, 2, 3]; numbers.map(function (n) {   return n + 1; }); // [2, 3, 4]  numbers // [1, 2, 3] 
```

forEach方法不返回值，只用来操作数据。这就是说，如果数组遍历的目的是为了得到返回值，那么使用map方法，否则使用forEach方法。

forEach的用法与map方法一致，参数是一个函数，该函数同样接受三个参数：当前值、当前位置、整个数组。

```js
function log(element, index, array) {   console.log('[' + index + '] = ' + element); }  [2, 5, 9].forEach(log); // [0] = 2 // [1] = 5 // [2] = 9 
```

forEach方法也可以接受第二个参数，绑定参数函数的this变量。

```js
var out = [];  [1, 2, 3].forEach(function(elem) {   this.push(elem * elem); }, out);  out // [1, 4, 9] 
```

filter方法用于过滤数组成员，满足条件的成员组成一个新数组返回。

它的参数是一个函数，所有数组成员依次执行该函数，返回结果为true的成员组成一个新数组返回。该方法不会改变原数组。

```js
[1, 2, 3, 4, 5].filter(function (elem) {   return (elem > 3); }) // [4, 5]  var arr = [0, 1, 'a', false]; arr.filter(Boolean) // [1, "a"] 
```

some方法是只要一个成员的返回值是true，则整个some方法的返回值就是true，否则返回false。

```js
var arr = [1, 2, 3, 4, 5]; arr.some(function (elem, index, arr) {   return elem >= 3; }); // true 
```

every方法是所有成员的返回值都是true，整个every方法才返回true，否则返回false。

```js
var arr = [1, 2, 3, 4, 5]; arr.every(function (elem, index, arr) {   return elem >= 3; }); // false 
```

#### this

this就是属性或方法“当前”所在的对象。

this的指向是可变的。

this就是函数运行时所在的对象（环境）。 JavaScript 支持运行环境动态切换，也就是说，this的指向是动态的，没有办法事先确定到底指向哪个对象。

全局环境使用this，它指的就是顶层对象window。

构造函数中的this，指的是实例对象。

对象的方法里面包含 **this**，this的指向就是方法运行时所在的对象。该方法赋值给另一个对象，就会改变**this**的指向。

由于this的指向是不确定的，所以切勿在函数中包含多层的this。

解决方法是在第二层改用一个指向外层this的变量。

```js
var o = {   f1: function() {     console.log(this);     var that = this;     var f2 = function() {       console.log(that);     }();   } }  o.f1() 
```

JavaScript 继承机制的设计思想就是，原型对象的所有属性和方法，都能被实例对象共享。也就是说，如果属性和方法定义在原型上，那么所有实例对象就能共享，不仅节省了内存，还体现了实例对象之间的联系。

JavaScript 规定，每个函数都有一个prototype属性，指向一个对象。

```js
function Animal(name) {   this.name = name; } Animal.prototype.color = 'white';  var cat1 = new Animal('大毛'); var cat2 = new Animal('二毛');  cat1.color // 'white' cat2.color // 'white' 
```

上述代码，构造函数Animal的prototype属性，就是实例对象cat1和cat2的原型对象。原型对象上添加一个color属性，结果，实例对象都共享了该属性。

原型对象的属性不是实例对象自身的属性。只要修改原型对象，变动就立刻会体现在**所有**实例对象上。

实例对象自身就有某个属性或方法，它就不会再去原型对象寻找这个属性或方法。

```js
cat1.color = 'black';  cat1.color // 'black' cat2.color // 'yellow' Animal.prototype.color // 'yellow'; 

//use strict 严格模式

//use strict放在脚本文件的第一行，整个脚本都将以严格模式运行

//use strict放在函数体的第一行，则整个函数以严格模式运行。

```

avaScript 运行时，除了一个正在运行的主线程，引擎还提供多个任务队列（task queue），里面是各种需要当前程序处理的异步任务。



主线程会去执行所有的同步任务。等到同步任务全部执行完，就会去看任务队列里面的异步任务。如果满足条件，那么异步任务就重新进入主线程开始执行，这时它就变成同步任务了。等到执行完，下一个异步任务再进入主线程开始执行。一旦任务队列清空，程序就结束执行。



事件循环：引擎在不停地检查，一遍又一遍，只要同步任务执行完了，引擎就会去检查那些挂起来的异步任务，是不是可以进入主线程



setTimeout函数用来指定某个函数或某段代码，在多少毫秒之后执行

setInterval函数指定某个任务每隔一段时间就执行一次，也就是无限次的定时执行。

setTimeout和setInterval函数，都返回一个整数值，表示计数器编号。将该整数传入clearTimeout和clearInterval函数，就可以取消对应的定时器。

### document

DOM 的最小组成单位叫做节点（node）。文档的树形结构（DOM 树），就是由各种不同类型的节点组成。每个节点可以看作是文档树的一片叶子。

节点的类型有七种。

- Document：整个文档树的顶层节点
- DocumentType：doctype标签（比如`` <!DOCTYPE html>``）
- Element：网页的各种HTML标签（比如``<body>、<a>``等）
- Attribute：网页元素的属性（比如class="right"）
- Text：标签之间或标签包含的文本
- Comment：注释
- DocumentFragment：文档的片段

nodeName属性返回节点的名称。

var div = document.getElementById('d1'); div.nodeName // "DIV" 

不同节点的nodeName属性值如下。

- 文档节点（document）：#document
- 元素节点（element）：大写的标签名
- 属性节点（attr）：属性的名称
- 文本节点（text）：#text
- 文档片断节点（DocumentFragment）：#document-fragment
- 文档类型节点（DocumentType）：文档的类型
- 注释节点（Comment）：#comment

document.baseURI、window.location.href 、document.URL属性返回一个字符串，表示当前网页的绝对路径。浏览器根据这个属性，计算网页上的相对路径的 URL。该属性为只读。



document.links属性返回当前文档所有设定了href属性的<a>及<area>节点。

打印当前网址所有名称+连接

```js
var links = document.links; for(var i = 0; i < links.length; i++) {   console.log(links[i].text + links[i].href); } 
```



document.domain属性返回当前文档的域名，不包含协议和接口。比如，网页的网址是`http://www.example.com:80/hello.html`，那么domain属性就等于`www.example.com`。如果无法获取域名，该属性返回null。



为了解决脚本文件下载阻塞网页渲染的问题，一个方法是对<script>元素加入defer属性。它的作用是延迟脚本的执行，等到 DOM 加载生成后，再执行脚本。

<script src="a.js" defer></script>
<script src="b.js" defer></script>
defer属性的运行流程如下。

1. 浏览器开始解析 HTML 网页。
2. 解析过程中，发现带有defer属性的<script>元素。
3. 浏览器继续往下解析 HTML 网页，同时并行下载<script>元素加载的外部脚本。
4. 浏览器完成解析 HTML 网页，此时再回过头执行已经下载完成的脚本。

有了defer属性，浏览器下载脚本文件的时候，不会阻塞页面渲染。下载的脚本文件在DOMContentLoaded事件触发前执行（即刚刚读取完</html>标签），而且可以保证执行顺序就是它们在页面上出现的顺序。

只有IE可以使用

解决“阻塞效应”的另一个方法是对<script>元素加入async属性。

<script src="a.js" async></script>
<script src="b.js" async></script>
async属性的作用是，使用另一个进程下载脚本，下载时不会阻塞渲染。

1. 浏览器开始解析 HTML 网页。
2. 解析过程中，发现带有async属性的script标签。
3. 浏览器继续往下解析 HTML 网页，同时并行下载<script>标签中的外部脚本。
4. 脚本下载完成，浏览器暂停解析 HTML 网页，开始执行下载的脚本。
5. 脚本执行完毕，浏览器恢复解析 HTML 网页。

async属性可以保证脚本下载的同时，浏览器继续渲染。需要注意的是，一旦采用这个属性，就无法保证脚本的执行顺序。哪个脚本先下载结束，就先执行那个脚本。另外，使用async属性的脚本文件里面的代码，不应该使用document.write方法。

一般来说，如果脚本之间没有依赖关系，就使用async属性，如果脚本之间有依赖关系，就使用defer属性。如果同时使用async和defer属性，后者不起作用，浏览器行为由async属性决定。



不同的浏览器有不同的渲染引擎。

- Firefox：Gecko 引擎
- Safari：WebKit 引擎
- Chrome：Blink 引擎
- IE: Trident 引擎
- Edge: EdgeHTML 引擎

渲染引擎处理网页，通常分成四个阶段。

- 解析代码：HTML 代码解析为 DOM，CSS 代码解析为 CSSOM（CSS Object Model）。
- 对象合成：将 DOM 和 CSSOM 合成一棵渲染树（render tree）。
- 布局：计算出渲染树的布局（layout）。
- 绘制：将渲染树绘制到屏幕。

