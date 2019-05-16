## JDK5

### 1.自动装箱与拆箱：

自动装箱的过程：每当需要一种类型的对象时，这种基本类型就自动地封装到与它相同类型的包装中。

自动拆箱的过程：每当需要一个值时，被装箱对象中的值就被自动地提取出来，没必要再去调用intValue()和doubleValue()方法。

自动装箱，只需将该值赋给一个类型包装器引用，java会自动创建一个对象。

自动拆箱，只需将该对象值赋给一个基本类型即可。

java——类的包装器

类型包装器有：Double,Float,Long,Integer,Short,Character和Boolean

### 2.枚举

把集合里的对象元素一个一个提取出来。枚举类型使代码更具可读性，理解清晰，易于维护。枚举类型是强类型的，从而保证了系统安全性。而以类的静态字段实现的类似替代模型，不具有枚举的简单性和类型安全性。

简单的用法：JavaEnum简单的用法一般用于代表一组常用常量，可用来代表一类相同类型的常量值。

复杂用法：Java为枚举类型提供了一些内置的方法，同事枚举常量还可以有自己的方法。可以很方便的遍历枚举对象。

### 3.静态导入

通过使用 import static，就可以不用指定 Constants 类名而直接使用静态成员，包括静态方法。

`import xxxx 和 import static xxxx的区别是前者一般导入的是类文件如import java.util.Scanner;后者一般是导入静态的方法，import static java.lang.System.out。`

### 4.可变参数（Varargs）

可变参数的简单语法格式为：

`methodName([argumentList], dataType...argumentName);`

### 5.内省（Introspector）

``是 Java语言对Bean类属性、事件的一种缺省处理方法。例如类A中有属性name,那我们可以通过getName,setName来得到其值或者设置新 的值。通过getName/setName来访问name属性，这就是默认的规则。Java中提供了一套API用来访问某个属性的getter /setter方法，通过这些API可以使你不需要了解这个规则（但你最好还是要搞清楚），这些API存放于包java.beans中。``
``一 般的做法是通过类Introspector来获取某个对象的BeanInfo信息，然后通过BeanInfo来获取属性的描述器 （PropertyDescriptor），通过这个属性描述器就可以获取某个属性对应的getter/setter方法，然后我们就可以通过反射机制来 调用这些方法。``

### 6.泛型(Generic) 

C++ 通过模板技术可以指定集合的元素类型，而Java在1.5之前一直没有相对应的功能。一个集合可以放任何类型的对象，相应地从集合里面拿对象的时候我们也 不得不对他们进行强制得类型转换。引入了泛型，它允许指定集合里元素的类型，这样你可以得到强类型在编译时刻进行类型检查的好处。

### 7.For-Each循环 

For-Each循环得加入简化了集合的遍历。假设我们要遍历一个集合对其中的元素进行一些处理。

### ８.　`JUC`

 `ConcurrentHashMap(简称CHM)是在Java 1.5作为Hashtable的替代选择新引入的,是concurrent包的重要成员。`

## `JDK6`

1. AWT新增加了两个类:Desktop和SystemTray，其中前者用来通过系统默认程序来执行一个操作，如使用默认浏览器浏览指定的URL,用默认邮件客户端给指定的邮箱发邮件,用默认应用程序打开或编辑文件(比如,用记事本打开以txt为后缀名的文件),用系统默认的打印机打印文档等。后者可以用来在系统托盘区创建一个托盘程序。（开发中基本没用过）
2. 使用JAXB2来实现对象与XML之间的映射，可以将一个Java对象转变成为XML格式，反之亦然 
3. StAX，一种利用拉模式解析(pull-parsing)XML文档的API。类似于SAX，也基于事件驱动模型。之所以将StAX加入到JAXP家族，是因为JDK6中的JAXB2和JAX-WS 2.0中都会用StAX。
4. 使用Compiler API，动态编译Java源文件，如JSP编译引擎就是动态的，所以修改后无需重启服务器。（刚知道是从这里开始可以动态编译的）
5. 轻量级Http Server API，据此可以构建自己的嵌入式HttpServer,它支持Http和Https协议。
6. 插入式注解处理API(PluggableAnnotation Processing API) 
7. 提供了Console类用以开发控制台程序，位于java.io包中。据此可方便与Windows下的cmd或Linux下的Terminal等交互。 
8. 对脚本语言的支持如: ruby,groovy, javascript 
9. Common Annotations，原是J2EE 5.0规范的一部分，现在把它的一部分放到了J2SE 6.0中 
10. 嵌入式数据库 Derby（这个也是刚知道，基本没用过）

## `JDK7`

1. **对Java集合（Collections）的增强支持，可直接采用[]、{}的形式存入对象，采用[]的形式按照索引、键值来获取集合中的对象。如：**

```java
    List<String>list=[“item1”,”item2”];//存
    Stringitem=list[0];//直接取
    Set<String>set={“item1”,”item2”,”item3”};//存
    Map<String,Integer> map={“key1”:1,”key2”:2};//存
    Intvalue=map[“key1”];//取12345
	//!!!!!!!!!!!!!多版本测试 并没有这功能 并查阅oracle官网也没有此特性
```

2. 在Switch中可用String
3. 数值可加下划线用作分隔符（编译时自动被忽略） `int one_million = 1_000_000;`
4. 支持二进制数字，如：`int binary= 0b1001_1001; `
5. 简化了可变参数方法的调用 
6. 调用泛型类的构造方法时，可以省去泛型参数，编译器会自动判断。
7. char类型的equals方法: `boolean Character.equalsIgnoreCase(char ch1, char ch2) `
8. Map集合支持并发请求，注`HashTable`是线程安全的，Map是非线程安全的。但此处更新使得其也支持并发。另外，Map对象可这样定义：`Map map = {name:”xxx”,age:18};`

### 9 、自动资源管理（try with resource）

```java
     try (BufferedReader br = new BufferedReader(new FileReader(path)) { 
             return br.readLine(); 
          } 
```
### 10 、Boolean类型反转，空指针安全,参与位运算 

```java
//类型反转，空指针安全
Boolean Booleans.negate(Boolean booleanObj) //True => False , False => True, Null => Null
//参与位运算
boolean Booleans.and(boolean[] array) 
boolean Booleans.or(boolean[] array) 
boolean Booleans.xor(boolean[] array) 
boolean Booleans.and(Boolean[] array) 
boolean Booleans.or(Boolean[] array) 
boolean Booleans.xor(Boolean[] array)
```

### 11 、安全的加减乘除: 

```java
int Math.safeToInt(long value)
int Math.safeNegate(int value)
long Math.safeSubtract(long value1, int value2)
long Math.safeSubtract(long value1, long value2)
int Math.safeMultiply(int value1, int value2)
long Math.safeMultiply(long value1, int value2)
long Math.safeMultiply(long value1, long value2)
long Math.safeNegate(long value)
int Math.safeAdd(int value1, int value2)
long Math.safeAdd(long value1, int value2)
long Math.safeAdd(long value1, long value2)
int  Math.safeSubtract(int value1, int value2)
```

