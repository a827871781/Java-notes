# ES6

## let、const

`let` ：声明变量，更严谨，不允许重复声明，不存在变量提升

`const` ： 声明常量，不允许重复声明，不存在变量提升

`let` 完全可以取代 `var`，因为两者语义相同，而且 `let` 没有副作用。

## 对象的扩展运算符(``...``)

```js
//解构赋值：ES6 允许按照一定模式从数组和对象中提取值，然后对变量进行赋值，这被称为解构
const arr = [1, 2, 3, 4];

// bad
const first = arr[0];
const second = arr[1];

// good
const [first, second] = arr;

//函数的参数如果是对象的成员，优先使用解构赋值。
// bad
function getFullName(user) {
  const firstName = user.firstName;
  const lastName = user.lastName;
}

// good
function getFullName(obj) {
  const { firstName, lastName } = obj;
}

// best
function getFullName({ firstName, lastName }) {
}


//扩展运算符（...）用于取出参数对象的所有可遍历属性
let obj = { a: 3, b: 4 };

//扩展运算符（...）拷贝对象
let objCopy = { ...z };
n // { a: 3, b: 4 }

obj===objCopy // false 可以用来深拷贝对象

//扩展运算符（...）拷贝数组
let arr =  [1,2,3]
let arrCopy = [...arr];


//合并两个对象。
let ab = { ...a, ...b };
// 等同于
let ab = Object.assign({}, a, b);


```

## 模板字符串

模板字符串是增强版的字符串，用反引号（`）标识。它可以当作普通字符串使用，也可以用来定义多行字符串，或者在字符串中嵌入变量。

```js
// 普通字符串
`In JavaScript '\n' is a line-feed.`

// 多行字符串 
//模板字符串表示多行字符串，所有的空格和缩进都会被保留在输出之中
`In JavaScript this is
 not legal.`

console.log(`string text line 1
string text line 2`);

// 字符串中嵌入变量
let name = "Bob", time = "today";
`Hello ${name}, how are you ${time}?`

//大括号内部可以放入任意的 JavaScript 表达式，可以进行运算，以及引用对象属性。
let name = "Bob";
`Hello ${name.length}`
```



## 函数参数的默认值

```js
function log(x, y = 'World') {
  console.log(x, y);
}

log('Hello') // Hello World
log('Hello', 'China') // Hello China
log('Hello', '') // Hello
```

## 对象属性的简洁表示

### 1、允许直接写入变量和函数，作为对象的属性和方法。

```js
var foo = 'bar';
// bad
var baz = {foo: foo};

//good
var baz = {foo};
baz // {foo: "bar"}

```

### 2、允许在对象之中，直接写变量。

```js
// bad
function f(x, y) {
  return {x: x, y: y};
}

//good
function f(x, y) {
  return {x, y};
}

f(1, 2) // Object {x: 1, y: 2}

```

### 3、允许在对象之中，直接写定义方法。

```js
// bad
var o = {
  method: function() {
    return "Hello!";
  }
};

//good
var o = {
  method() {
    return "Hello!";
  }
};
```

## 箭头函数

ES6 标准新增了一种新的函数：Arrow Function（箭头函数）。

为什么叫 Arrow Function？因为它的定义用的就是一个箭头：

```js
//无参数箭头函数
let func = value => value;

//等同于
let func = function (value) {
    return value;
};

//多参数箭头函数
let func = (value, num) => value * num;

//等同于
let func = function (value ,num) {
    return value * num;
};

//数组过滤,取出所有大于3的数字
let arr = [1,2,3,4,5]
let filterArr = arr.filter(i => i > 3);

```

## set和map

set和map 知道其特性,并且可以在工作中应用即可.

#### set

ES6提供了新的数据结构Set。它类似于数组，但是成员的值都是唯一的，没有重复的值。

**Set本身是一个构造函数，用来生成Set数据结构。**

```js
var set = new Set();

[2, 3, 5, 4, 5, 2, 2].map(x => set.add(x));

for (let i of s) {
  console.log(i);
}
// 2 3 5 4

//Set函数可以接受一个数组（或类似数组的对象）作为参数，用来初始化
var set = new Set([1, 2, 3, 4, 4]);
[...set]
// [1, 2, 3, 4]

// 去除数组的重复成员
[...new Set(array)]
```

向Set加入值的时候，不会发生类型转换，所以`5`和`"5"`是两个不同的值。Set内部判断两个值是否不同，使用的算法叫做“Same-value equality”，它类似于精确相等运算符（`===`），主要的区别是`NaN`等于自身，而精确相等运算符认为`NaN`不等于自身,另外，**两个对象总是不相等的**。

#### Set结构的实例有四个遍历方法，可以用于遍历成员。

- `keys()`：返回键名的遍历器
- `values()`：返回键值的遍历器
- `entries()`：返回键值对的遍历器
- `forEach()`：使用回调函数遍历每个成员

```js
let set = new Set(['red', 'green', 'blue']);

for (let item of set.keys()) {
  console.log(item);
}
// red
// green
// blue

for (let item of set.values()) {
  console.log(item);
}
// red
// green
// blue

for (let item of set.entries()) {
  console.log(item);
}
// ["red", "red"]
// ["green", "green"]
// ["blue", "blue"]
```

#### Map

ES6提供了Map数据结构。它类似于对象，也是键值对的集合，但是“键”的范围不限于字符串，各种类型的值（包括对象）都可以当作键。也就是说，Object结构提供了“字符串—值”的对应，Map结构提供了“值—值”的对应，是一种更完善的Hash结构实现。

**对同一个键多次赋值，后面的值将覆盖前面的值**

**读取一个未知的键，则返回`undefined`。**

```js
var m = new Map();
var o = {p: 'Hello World'};

m.set(o, 'content')
m.get(o) // "content"

m.has(o) // true
m.delete(o) // true
m.has(o) // false
```

Map结构的实例有以下属性和操作方法

- **size ** 	 属性返回Map结构的成员总数。
- **set**   	  方法设置`key`所对应的键值，然后返回整个Map结构
- **get** 	    方法读取`key`对应的键值，如果找不到`key`，返回`undefined`。
- **has**  	  方法返回一个布尔值，表示某个键是否在Map数据结构中。
- **delete**	方法删除某个键，返回true。如果删除失败，返回false。
- **clear**	  方法清除所有成员，没有返回值。

Map原生提供三个遍历器生成函数和一个遍历方法。

- `keys()`：返回键名的遍历器。
- `values()`：返回键值的遍历器。
- `entries()`：返回所有成员的遍历器。
- `forEach()`：遍历Map的所有成员。

### module

ES6 模块不是对象，而是通过`export`命令显式指定输出的代码，再通过`import`命令输入。

`export`命令用于规定模块的对外接口，`import`命令用于输入其他模块提供的功能

```js
// ES6模块
import {getUUID} from '@/utils/util';
```

上面代码的实质是从`util`模块加载`getUUID`方法，其他方法不加载。这种加载称为“编译时加载”或者静态加载，即 ES6 可以在编译时就完成模块加载，效率要比 CommonJS 模块的加载方式高。

```js
// profile.js
var firstName = 'Michael';
var lastName = 'Jackson';
var year = 1958;

export {firstName, lastName, year};

// main.js
import {firstName, lastName, year} from './profile';

function setName(element) {
  element.textContent = firstName + ' ' + lastName;
}

//整体加载一个模块

// circle.js
export function area(radius) {
  return Math.PI * radius * radius;
}

export function circumference(radius) {
  return 2 * Math.PI * radius;
}

import * as circle from './circle';

console.log('圆面积：' + circle.area(4));
console.log('圆周长：' + circle.circumference(14));
```

如果想为输入的变量重新取一个名字，`import`命令要使用 **as** 关键字，将输入的变量重命名。

`import`后面的`from`指定模块文件的位置，可以是相对路径，也可以是绝对路径，`.js`路径可以省略。如果只是模块名，不带有路径，那么必须有配置文件，告诉 JavaScript 引擎该模块的位置。

## export default

使用`import`命令的时候，用户需要知道所要加载的变量名或函数名，否则无法加载。但是，用户肯定希望快速上手，未必愿意阅读文档，去了解模块有哪些属性和方法。

为了给用户提供方便，让他们不用阅读文档就能加载模块，就要用到`export default`命令，为模块指定默认输出。

```js
// export-default.js
export default function () {
  console.log('foo');
}
```

