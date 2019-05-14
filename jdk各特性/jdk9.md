# jdk9  Java 平台 模块系统

### 1、模块系统 module 

模块就是代码和数据的封装体。模块的代码被组织成多个包，每个包中包含Java类和接口；模块的数据则包括资源文件和其他静态信息。

Java 9 模模块就是代码和数据的封装体。模块的代码被组织成多个包，每个包中包含Java类和接口；模块的数据则包括资源文件和其他静态信息。

Java 9 模块的重要特征是在其工件（artifact）的根目录中包含了一个描述模块的 module-info.class 文 件。 工件的格式可以是传统的 JAR 文件或是 Java 9 新增的 JMOD 文件。块的重要特征是在其工件（artifact）的根目录中包含了一个描述模块的 module-info.class 文 件。 工件的格式可以是传统的 JAR 文件或是 Java 9 新增的 JMOD 文件。

模块化的 JAR 文件都包含一个额外的模块描述器。在这个模块描述器中, 对其它模块的依赖是通过 “**requires**” 来表示的。另外, “**exports**” 语句控制着哪些包是可以被其它模块访问到的。所有不被导出的包默认都封装在模块的里面。

### 2、Java 9 REPL (JShell)

REPL(Read Eval Print Loop)意为交互式的编程环境。

JShell 是 Java 9 新增的一个交互式的编程环境工具。它允许你无需使用类或者方法包装来执行 Java 语句。它与 Python 的解释器类似，可以直接 输入表达式并查看其执行结果。

![1554884929738](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1554884929738.png)

1. Java9 提供了一个交互式环境，不用再创建一个 project 或是其他的模块，就可以直接用来执行 Java 代码，所见即所得；
2. 可以动态修改正在运行中的程序，
3. 方便测试。

### 3、Java 9 改进 Javadoc

javadoc 工具可以生成 Java 文档， Java 9 的 javadoc 的输出现在符合兼容 HTML5 标准。



### 4、Java 9 多版本兼容 jar 包

多版本兼容 JAR 功能能让你创建仅在特定版本的 Java 环境中运行库程序时选择使用的 class 版本。

通过 **--release** 参数指定编译版本。

具体的变化就是 META-INF 目录下 MANIFEST.MF 文件新增了一个属性：

 ```java
Multi-Release: true
 ```

 META-INF 目录下还新增了一个 versions 目录

```java
multirelease.jar
├── META-INF
│   └── versions
│       └── 9
│           └── multirelease
│               └── Helper.class
├── multirelease
    ├── Helper.class
    └── Main.class
```

通过不同命令编译不同版本jar包

```shell
C:\test > javac --release 9 java9/com/runoob/Tester.java

C:\JAVA > javac --release 7 java7/com/runoob/Tester.java
```



### 5、Java 9 集合工厂方法

Java 9 中，以下方法被添加到 List，Set 和 Map 接口以及它们的重载对象。

```java
static <E> List<E> of(E e1, E e2, E e3);
static <E> Set<E>  of(E e1, E e2, E e3);
static <K,V> Map<K,V> of(K k1, V v1, K k2, V v2, K k3, V v3);
static <K,V> Map<K,V> ofEntries(Map.Entry<? extends K,? extends V>... entries)
```

- List 和 Set 接口, of(...) 方法重载了 0 ~ 10 个参数的不同方法 。
- Map 接口, of(...) 方法重载了 0 ~ 10 个参数的不同方法 。
- Map 接口如果超过 10 个参数, 可以使用 ofEntries(...) 方法。

**注：长度也是不可变得 和Arrays,asList  类似**

### 6、Java 9 私有接口方法

Java 9 不仅像 Java 8 一样支持接口默认方法，同时还支持私有方法。

在 Java 9 中，一个接口中能定义如下几种变量/方法：

- **常量**
- **抽象方法**
- **默认方法**
- **静态方法**
- **私有方法**
- **私有静态方法**

这玩应有啥用，现在抽象类 就剩个意义作用了吧

### 7、Java 9 改进的进程 API

在 Java 9 之前，Process API 仍然缺乏对使用本地进程的基本支持，例如获取进程的 PID 和所有者，进程的开始时间，进程使用了多少 CPU 时间，多少本地进程正在运行等。

Java 9 向 Process API 添加了一个名为 ProcessHandle 的接口来增强 java.lang.Process 类。

ProcessHandle 接口的实例标识一个本地进程，它允许查询进程状态并管理进程。

ProcessHandle 嵌套接口 Info 来让开发者逃离时常因为要获取一个本地进程的 PID 而不得不使用本地代码的窘境。

我们不能在接口中提供方法实现。如果我们要提供抽象方法和非抽象方法（方法与实现）的组合，那么我们就得使用抽象类。

ProcessHandle 接口中声明的 onExit() 方法可用于在某个进程终止时触发某些操作。

### 8、Java 9 改进的 Stream API

Java 9 改进的 Stream API 添加了一些便利的方法，使流处理更容易，并使用收集器编写复杂的查询。

Java 9 为 Stream 新增了几个方法：dropWhile、takeWhile、ofNullable，为 iterate 方法新增了一个重载方法。

### 9、Java 9 改进的 try-with-resources

try-with-resources 是 JDK 7 中一个新的异常处理机制，它能够很容易地关闭在 try-catch 语句块中使用的资源。所谓的资源（resource）是指在程序完成后，必须关闭的对象。try-with-resources 语句确保了每个资源在语句结束时关闭。所有实现了 java.lang.AutoCloseable 接口（其中，它包括实现了 java.io.Closeable 的所有对象），可以使用作为资源。

try-with-resources 声明在 JDK 9 已得到改进。如果你已经有一个资源是 final 或等效于 final 变量,您可以在 try-with-resources 语句中使用该变量，而无需在 try-with-resources 语句中声明一个新变量。

```java
//9之前
public class Tester {
   public static void main(String[] args) throws IOException {
      System.out.println(readData("test"));
   } 
   static String readData(String message) throws IOException {
      Reader inputString = new StringReader(message);
      BufferedReader br = new BufferedReader(inputString);
      try (BufferedReader br1 = br) {
         return br1.readLine();
      }
   }
}
//9之后
public class Tester {
   public static void main(String[] args) throws IOException {
      System.out.println(readData("test"));
   } 
   static String readData(String message) throws IOException {
      Reader inputString = new StringReader(message);
      BufferedReader br = new BufferedReader(inputString);
      try (br) {
         return br.readLine();
      }
   }
}

//多数人使用方案
   static String readData(String message) {
      Reader inputString = new StringReader(message);
      BufferedReader br = new BufferedReader(inputString);
       String str ;
      try {
          str =  br.readLine();
      }catch (IOException e){
          str = "";
          e.printStackTrace();
      }finally {
          try {
              br.close();
          } catch (IOException e) {
              e.printStackTrace();
          }
      }
       return str;
   }

```

### 10、Java 9 改进的 @Deprecated 注解

注解 @Deprecated 可以标记 Java API 状态，可以是以下几种：

- 使用它存在风险，可能导致错误
- 可能在未来版本中不兼容
- 可能在未来版本中删除
- 一个更好和更高效的方案已经取代它。

Java 9 中注解增加了两个新元素：**since** 和 **forRemoval**。

- **since**: 元素指定已注解的API元素已被弃用的版本。
- **forRemoval**: 元素表示注解的 API 元素在将来的版本中被删除，应该迁移 API。

### 11、Java 9 改进的 Optional 类

Optional 类在 Java 8 中引入，Optional 类的引入很好的解决空指针异常。。在 java 9 中, 添加了三个方法来改进它的功能：

- stream()
- ifPresentOrElse()
- or()