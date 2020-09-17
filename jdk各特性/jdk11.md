# jdk11

## 1.字符串加强

Java 11 增加了一系列的字符串处理方法，如以下所示。

```java
// 判断字符串是否为空白  
" ".isBlank();                // true  

// 去除首尾空格  
" Javastack ".strip();          // "Javastack"  

// 去除尾部空格   
" Javastack ".stripTrailing();  // " Javastack"  

// 去除首部空格   
" Javastack ".stripLeading();   // "Javastack "  

// 复制字符串  
"Java".repeat(3);             // "JavaJavaJava"  

// 行数统计  
"A\nB\nC".lines().count();    // 3 
```

## 2.集合加强

自 Java 9 开始，Jdk 里面为集合（List/ Set/ Map）都添加了 of 和 copyOf 方法，它们两个都用来创建不可变的集合，来看下它们的使用和区别。

**示例 1：**

```java
var list = List.of("Java", "Python", "C");  

var copy = List.copyOf(list);  

System.out.println(list == copy);   // true 

```

**示例 2：**

```java
var list = new ArrayList<String>();  

var copy = List.copyOf(list);  

System.out.println(list == copy);   // false 

```

示例 1 和 2 代码差不多，为什么一个为 true, 一个为 false?

来看下它们的源码：

```java
static <E> List<E> of(E... elements) {  

    switch (elements.length) { // implicit null check of elements  

        case 0:  

            return ImmutableCollections.emptyList();  

        case 1:  

            return new ImmutableCollections.List12<>(elements[0]);  

        case 2:  

            return new ImmutableCollections.List12<>(elements[0], elements[1]);  

        default:  

            return new ImmutableCollections.ListN<>(elements);  

    }  

}  

static <E> List<E> copyOf(Collection<? extends E> coll) {  

    return ImmutableCollections.listCopy(coll);  

}  

static <E> List<E> listCopy(Collection<? extends E> coll) {  

    if (coll instanceof AbstractImmutableList && coll.getClass() != SubList.class) {  

        return (List<E>)coll;  

    } else {  

        return (List<E>)List.of(coll.toArray());  

    }  

} 

```

可以看出 copyOf 方法会先判断来源集合是不是 AbstractImmutableList 类型的，如果是，就直接返回，如果不是，则调用 of 创建一个新的集合。

示例 2 因为用的 new 创建的集合，不属于不可变 AbstractImmutableList 类的子类，所以 copyOf 方法又创建了一个新的实例，所以为 false.

注意：使用 of 和 copyOf 创建的集合为不可变集合，不能进行添加、删除、替换、排序等操作，不然会报 java.lang.UnsupportedOperationException 异常。

上面演示了 List 的 of 和 copyOf 方法，Set 和 Map 接口都有。

## 3.Stream 加强

Stream 是 Java 8 中的新特性，Java 9 开始对 Stream 增加了以下 4 个新方法。

1.  增加单个参数构造方法，可为 null

```java
Stream.ofNullable(null).count(); // 0 

```

1.  增加 takeWhile 和 dropWhile 方法 

```java
Stream.of(1, 2, 3, 2, 1)  

    .takeWhile(n -> n < 3)  

    .collect(Collectors.toList());  // [1, 2] 

```

从开始计算，当 n < 3 时就截止。

```java
Stream.of(1, 2, 3, 2, 1)  

    .dropWhile(n -> n < 3)  

    .collect(Collectors.toList());  // [3, 2, 1] 

```

这个和上面的相反，一旦 n < 3 不成立就开始计算。

3）iterate 重载

这个 iterate 方法的新重载方法，可以让你提供一个 Predicate (判断条件) 来指定什么时候结束迭代。

## 4.Optional 加强

Opthonal 也增加了几个非常酷的方法，现在可以很方便的将一个 Optional 转换成一个 Stream, 或者当一个空 Optional 时给它一个替代的。

```java
Optional.of("javastack").orElseThrow();     // javastack  

Optional.of("javastack").stream().count();  // 1  

Optional.ofNullable(null)  

    .or(() -> Optional.of("javastack"))  

    .get();   // javastack 
```

## 5.InputStream 加强

InputStream 终于有了一个非常有用的方法：transferTo，可以用来将数据直接传输到 OutputStream，这是在处理原始数据流时非常常见的一种用法，如下示例。

```java
var classLoader = ClassLoader.getSystemClassLoader();  

var inputStream = classLoader.getResourceAsStream("javastack.txt");  

var javastack = File.createTempFile("javastack2", "txt");  

try (var outputStream = new FileOutputStream(javastack)) {  

    inputStream.transferTo(outputStream);  

} 
```

## 6.HTTP Client API

这是 Java 9 开始引入的一个处理 HTTP 请求的的孵化 HTTP Client API，该 API 支持同步和异步，而在 Java 11 中已经为正式可用状态，你可以在 [java.net](http://java.net) 包中找到这个 API。

来看一下 HTTP Client 的用法：

```java
var request = HttpRequest.newBuilder()  

    .uri(URI.create("https://javastack.cn"))  

    .GET()  

    .build();  

var client = HttpClient.newHttpClient();  

// 同步  

HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());  

System.out.println(response.body());  

// 异步  

client.sendAsync(request, HttpResponse.BodyHandlers.ofString())  

    .thenApply(HttpResponse::body)  

    .thenAccept(System.out::println); 
复制代码
```

上面的 .GET () 可以省略，默认请求方式为 Get！

## 7.其他特性

**ZGC：可扩展的低延迟垃圾收集器**

ZGC 是一款号称可以保证每次 GC 的停顿时间不超过 10MS 的垃圾回收器，并且和当前的默认垃圾回收起 G1 相比，吞吐量下降不超过 15%。

**Epsilon：什么事也不做的垃圾回收器**

Java 11 还加入了一个比较特殊的垃圾回收器 ——Epsilon，该垃圾收集器被称为 “no-op” 收集器，将处理内存分配而不实施任何实际的内存回收机制。 也就是说，这是一款不做垃圾回收的垃圾回收器。这个垃圾回收器看起来并没什么用，主要可以用来进行性能测试、内存压力测试等，Epsilon GC 可以作为度量其他垃圾回收器性能的对照组。大神 Martijn 说，Epsilon GC 至少能够帮助理解 GC 的接口，有助于成就一个更加模块化的 JVM。

**增强 var 用法**

Java 10 中增加了本地变量类型推断的特性，可以使用 var 来定义局部变量。尽管这一特性被很多人诟病，但是并不影响 Java 继续增强他的用法，在 Java 11 中，var 可以用来作为 Lambda 表达式的局部变量声明。

**移除 Java EE 和 CORBA 模块**

早在发布 Java SE 9 的时候，Java 就表示过，会在未来版本中将 Java EE 和 CORBA 模块移除，而这样举动终于在 Java 11 中实施。终于去除了 Java EE 和 CORBA 模块。

**HTTP 客户端进一步升级**

JDK 9 中就已对 HTTP Client API 进行标准化，然后通过 JEP 110，在 JDK 10 中进行了更新。在本次的 Java 11 的更新列表中，由以 JEP 321 进行进一步升级。该 API 通过 CompleteableFutures 提供非阻塞请求和响应语义，可以联合使用以触发相应的动作。 JDK 11 完全重写了该功能。现在，在用户层请求发布者和响应发布者与底层套接字之间追踪数据流更容易了，这降低了复杂性，并最大程度上提高了 HTTP / 1 和 HTTP / 2 之间的重用的可能性。