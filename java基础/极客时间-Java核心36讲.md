### 1、java程序执行步骤

1. javac编译器将源代码编译成字节码。
2. jvm类加载器加载字节码文件
3. 解释器逐行解释执行
4. 程序运行过程中部分热点代码可以通过**JIT**编译成机器码(不是逐行)并存在缓存里(运行时编译保证了可移植性)，下次运行可以直接从缓存里取机器码，效率更高。
5. **AOT**直接将字节码编译成机器代码，这样就避免了 JIT 预热等各方面的开销。

#### AOT:指运行前编译

优点：

1. 在程序运行前编译，可以避免在运行时的编译性能消耗和内存消耗
2. 可以在程序运行初期就达到最高性能
3. 可以显著的加快程序的启动

缺点：

1. 在程序运行前编译会使程序安装的时间增加
2. 牺牲 Java 的一致性
3. 将提前编译的内容保存会占用更多的外存

#### JIT:动态 (运行时) 编译

优点：

1. 可以根据当前硬件情况实时编译生成最优机器指令（ps. AOT 也可以做到，在用户使用是使用字节码根据机器情况在做一次编译）
2. 可以根据当前程序的运行情况生成最优的机器指令序列
3. 当程序需要支持动态链接时，只能使用 JIT
4. 可以根据进程中内存的实际情况调整代码，使内存能够更充分的利用

缺点：

1. 编译需要占用运行时资源，会导致进程卡顿
2. 由于编译时间需要占用运行时间，对于某些代码的编译优化不能完全支持，需要在程序流畅和编译时间之间做权衡
3. 在编译准备和识别频繁使用的方法需要占用时间，使得初始编译不能达到最高性能

Java 是**解释和编译**混合的一种模式

解释执行/编译执行区别

解释执行：类似同声传译，没有提前准备，看到一行解释一行。运行时效率一般。

编译执行：类似录音机 ，提前编译、优化，直接执行，运行时效率高，但是需要编译。

### 2、Exception和Error区别

Exception 和 Error 都是继承了 Throwable 类，在 Java 中只有 Throwable 类型的实例才可以被抛出（ throw ）或者捕获（ catch ），它是异常处理机制的基本组成类型。

#### Exception 和 Error 体现了 Java 平台设计者对不同异常情况的分类：

- Exception 是程序正常运行中，可以预料的意外情况，也就是要么捕获异常并作出处理，要么继续抛出异常。
- Error 是指在正常情况下，不大可能出现的情况，系统错误，虚拟机出错，我们处理不了，也不需要我们来处理。绝大部分的 Error 都会导致程序（比如 JVM 自身）处于非正常的、不可恢复状态。既然是非正常情况，所以不便于也不需要捕获，常见的比如 OutOfMemoryError 之类，都是 Error 的子类。

#### Exception又分为 可检查 （checked）异常和 不检查 （unchecked）异常:

- 可检查异常在源代码里必须显式地进行捕获处理，这是编译期检查的一部分。
- 不检查异常就是所谓的运行时异常，类似 NullPointerException 、 ArrayIndexOutOfBoundsException 之类，通常是可以编码避免的逻辑错误，具体根据需要来判断是否需要捕获，并不会在编译期强制要求。

![T.png](https://i.loli.net/2019/07/18/5d3045ebd844550122.png)

#### 异常处理原则

- 尽量不要捕获类似Exception这样的通用异常，而是应该捕获特定异常 ，如：Thread.sleep()抛出的InterruptedException。
- 不要仅仅捕获异常而不做任何处理，不便于将来维护
- 不要在fnally代码块中处理返回值。
- 函数返回值有两种类型：值类型与对象引用。对于对象引用，要特别小心，如果在fnally代码块中对函数返回的对象成员属性进行了修改，即使不在fnally块中显式调用return语句，这个修改也会作用于返回值上。
- 抛出异常时需要针对具体问题来抛出异常，抛出的异常要足够具体详细。
- 在捕获异常时需要对捕获的异常进行细分，这时会有多个 catch 语句块，这几个 catch 块中间泛化程度越低的异常需要越放在前面捕获，泛化程度高的异常捕获放在后面，这样的好处是如果出现异常可以近可能得明确异常的具体类型是什么
- try-catch代码段会产生额外的性能开销，或者换个角度说，它往往会影响JVM对代码进行优化，所以建议仅捕获有必要的代码段，尽量不要一个大的try包住整段的代码；与此同时，利用异常控制代码流程，也不是一个好主意，远比我们通常意义上的条件语句（ if/else 、 switch ）要低效。
- Null 的判断逻辑并不是一成不变的，当方法允许返回 null 的时候使用 if-else 控制逻辑，否则就抛出 NullPointerException
- 定义你自己的异常类层次，例如 UserException 和 SystemException 分别代表用户级别的异常信息和系统级别的异常信息，而其他的异常在这两个基类上进行扩展

### 3、谈谈final、finally、 finalize有什么不同？

**final** 可以用来修饰类、方法、变量，分别有不同的意义， final修饰的 class 代表不可以继承扩展， final的变量是不可以修改的，而 final的方法也是不可以重写的（ override ）。
**finally** 则是 Java 保证重点代码一定要被执行的一种机制。我们可以使用 try-finally或者 try-catch-finally来进行类似关闭 JDBC 连接、保证 unlock 锁等动作。
**finalize** 是基础类 java.lang.Object 的一个方法，它的设计目的是保证对象在被垃圾收集前完成特定资源的回收。 finalize机制现在已经**不推荐使用**，并且在 JDK 9 开始被标记为 deprecated 。

以下情况finally不会执行：

```java
//1. try-cach 异常退出。
try{
    system.exit(1)
}fnally{
	print(1)
}
//2. 无限循环
try{
    while(ture){
   		 print(1)
    }
}fnally{
	print(2)	
}
//3. 线程被杀死
//当执行 try，finally 的线程被杀死时。finally 也无法执行。

```

不要在 finally中使用 return 语句。使用不当可能会导致返回结果不可控

finalize代替方案 ：虚引用 + 引用队列

### 4、Java的对象引用

Java中根据其生命周期的长短，将引用分为4类。

1. 强引用（死都不清）
    特点：我们平常典型编码Object obj = new Object()中的obj就是强引用。通过关键字new创建的对象所关联的引用就是强引用。 当JVM内存空间不足，JVM会抛出OutOfMemoryError运行时错误（OOM），使程序异常终止，对于一个普通的对象，如果没有其他的引用关系，只要超过了引用的作用域或者显式地将相应（强）引用赋值为 null，就是可以被垃圾收集的了。

2.  软引用（满了才清）
    特点：软引用通过SoftReference类实现。 软引用的生命周期比强引用短一些。只有当 JVM 认为内存不足时，才会去试图回收软引用指向的对象：即JVM 会确保在抛出 OutOfMemoryError之前，清理软引用指向的对象。
    应用场景：一般用于做缓存。

3. 弱引用（一次就清）
    弱引用通过WeakReference类实现。 弱引用的生命周期比软引用短。在垃圾回收器线程扫描它所管辖的内存区域的过程中，一旦发现了具有弱引用的对象，不管当前内存空间足够与否，都会回收它的内存。由于垃圾回收器是一个优先级很低的线程，因此不一定会很快回收弱引用的对象。
    应用场景：也可以用于做缓存。

4.  虚引用（跟本没有）
    特点：虚引用也叫幻象引用，通过PhantomReference类来实现。无法通过虚引用访问对象的任何属性或函数。幻象引用仅仅是提供了一种确保对象被 fnalize 以后，做某些事情的机制。如果一个对象仅持有虚引用，那么它就和没有任何引用一样，在任何时候都可能被垃圾回收器回收。虚引用必须和引用队列 （ReferenceQueue）联合使用。当垃圾回收器准备回收一个对象时，如果发现它还有虚引用，就会在回收对象的内存之前，把这个虚引用加入到与之关联的引用队列中。

    ```java
    ReferenceQueue queue = new ReferenceQueue ();
    PhantomReference pr = new PhantomReference (object, queue);
    ```

    程序可以通过判断引用队列中是否已经加入了虚引用，来了解被引用的对象是否将要被垃圾回收。如果程序发现某个虚引用已经被加入到引用队列，那么就可以在所引用的对象的内存被回收之前采取一些程序行动。
    应用场景：可用来跟踪对象被垃圾回收器回收的活动，当一个虚引用关联的对象被垃圾收集器回收之前会收到一条系统通知。

### 5、理解Java的字符串，String、StringBufer、StringBuilder有什么区别？

1. String
    **(1) String的创建机理**
    由于String在Java世界中使用过于频繁，Java为了避免在一个系统中产生大量的String对象，引入了字符串常量池。其运行机制是：创建一个字符串时，首先检查池中是否有值相同的字符串对象，如果有则不需要创建直接从池中刚查找到的对象引用；如果没有则新建字符串对象，返回对象引用，并且将新创建的对象放入池中。但是，通过new方法创建的String对象是不检查字符串池的，而是直接在堆区或栈区创建一个新的对象，也不会把对象放入池中。上述原则只适用于通过直接量给String对象引用赋值的情况。
    举例：

    ```java
    String str1 = "123"; //通过直接量赋值方式，放入字符串常量池
    String str2 = new String(“123”);//通过new方式赋值方式，不放入字符串常量池
    ```

    注意：String提供了inter()方法。调用该方法时，如果常量池中包括了一个等于此String对象的字符串（由equals方法确定），则返回池中的字符串。否则，将此String对象添加到池中，并且返回此池中对象的引用。
    **(2) String的特性**
    [A] **不可变**。是指String对象一旦生成，则不能再对它进行改变。不可变的主要作用在于当一个对象需要被多线程共享，并且访问频繁时，可以省略同步和锁等待的时间，从而大幅度提高系统性能。不可变模式是一个可以提高多线程程序的性能，降低多线程程序复杂度的设计模式。
    [B] **针对常量池的优化**。当2个String对象拥有相同的值时，他们只引用常量池中的同一个拷贝。当同一个字符串反复出现时，这个技术可以大幅度节省内存空间。

2.  StringBufer/StringBuilder
    StringBufer和StringBuilder都实现了AbstractStringBuilder抽象类，拥有几乎一致对外提供的调用接口；其底层在内存中的存储方式与String相同，都是以一个有序的字符序列（char类型
    的数组）进行存储，不同点是**StringBufer/StringBuilder对象的值是可以改变的，并且值改变以后，对象引用不会发生改变;两者对象在构造过程中，首先按照默认大小申请一个字符数组，由于会不断加入新数据，当超过默认大小后，会创建一个更大的数组，并将原先的数组内容复制过来，再丢弃旧的数组。因此，对于较大对象的扩容会涉及大量的内存复制操作，如果能够预先评估大小，可提升性能。**
    唯一需要注意的是：StringBufer是线程安全的，但是StringBuilder是线程不安全的。可参看Java标准类库的源代码，StringBufer类中方法定义前面都会有synchronize关键字。为此，StringBufer的性能要远低于StringBuilder。

3. 其他
    Java字符串编译优化

    ```java
    //编译前 
    public void test(String str) {
            String a = "5" + "str";  // 1 
            String b = "5" + str;  // 2 
            String c = "";
            for (int i = 0; i < 10; i++) {
                c += "c" + i;   // 3
            }
        }
    //编译后
    public test(Ljava/lang/String;)V
        // parameter  str
       L0
        LINENUMBER 13 L0
        LDC "5str"   // 1 编译完就是一个完整的字符串，不需要 再进行拼接
        ASTORE 2
       L1
        LINENUMBER 14 L1
        NEW java/lang/StringBuilder
        DUP
        INVOKESPECIAL java/lang/StringBuilder.<init> ()V
        LDC "5"  
        INVOKEVIRTUAL java/lang/StringBuilder.append    // 2 StringBuilder 字符串 拼接
        (Ljava/lang/String;)Ljava/lang/StringBuilder;
        ALOAD 1
        INVOKEVIRTUAL java/lang/StringBuilder.append (Ljava/lang/String;)Ljava/lang/StringBuilder;
        INVOKEVIRTUAL java/lang/StringBuilder.toString ()Ljava/lang/String;
        ASTORE 3
       L2
        LINENUMBER 15 L2
        LDC ""
        ASTORE 4
       L3
        LINENUMBER 16 L3
        ICONST_0
        ISTORE 5
       L4
       FRAME FULL [com/syz/springtransaction/TestString java/lang/String java/lang/String java/lang/String java/lang/String I] []
        ILOAD 5
        BIPUSH 10
        IF_ICMPGE L5
       L6
        LINENUMBER 17 L6
        NEW java/lang/StringBuilder
        DUP
        INVOKESPECIAL java/lang/StringBuilder.<init> ()V //3 每次循环都实例化一个 新的StringBuilder对象，拼接字符串
        ALOAD 4
        INVOKEVIRTUAL java/lang/StringBuilder.append (Ljava/lang/String;)Ljava/lang/StringBuilder;
        LDC ""
        INVOKEVIRTUAL java/lang/StringBuilder.append (Ljava/lang/String;)Ljava/lang/StringBuilder;
        ILOAD 5
        INVOKEVIRTUAL java/lang/StringBuilder.append (I)Ljava/lang/StringBuilder;
        INVOKEVIRTUAL java/lang/StringBuilder.toString ()Ljava/lang/String;
        ASTORE 4
       L7
        LINENUMBER 16 L7
        IINC 5 1
        GOTO L4
       L5
        LINENUMBER 19 L5
       FRAME CHOP 1
        RETURN
       L8
        LOCALVARIABLE i I L4 L5 5
        LOCALVARIABLE this Lcom/syz/springtransaction/TestString; L0 L8 0
        LOCALVARIABLE str Ljava/lang/String; L0 L8 1
        LOCALVARIABLE a Ljava/lang/String; L1 L8 2
        LOCALVARIABLE b Ljava/lang/String; L2 L8 3
        LOCALVARIABLE c Ljava/lang/String; L3 L8 4
        MAXSTACK = 2
        MAXLOCALS = 6
    }
    
    ```

总结：代码中 可以直接用“ + ”来拼接字符串  ，但要记得循环内的字符串拼接一定要显示的用StringBuilder来拼接字符串。

### 6、动态代理

#### 1、反射

反射最大的作用之一就在于我们可以不在编译时知道某个对象的类型，而在运行时通过提供完整的”包名+类名.class”得到。注意：不是在编译时，而是在运行时。

##### 1.1、功能：

利用Java反射机制我们可以加载一个运行时才得知名称的class，获悉其构造方法，并生成其对象实体，能对其属性设值并调用其方法。

##### 1.2、缺点：

	反射会额外消耗一定的系统资源（慢），同时可能破坏类的封装性（不安全）。

#### 2、什么是动态代理

参考设计模式中代理模式，动态代理就是代理类不是由我们手动编码，而是由其他手段生成的。

1. 实现动态代理的手段

    -  Proxy （java动态代理）
    -  cglib

2. Proxy与cglib区别

   Proxy动态代理是利用反射机制生成一个实现代理接口的匿名类，在调用具体方法前调用InvokeHandler来处理。

   cglib动态代理是利用asm开源包，对代理对象类的class文件加载进来，通过修改其字节码生成子类来处理。

   - Proxy只能对实现了接口的类生成代理，而不能针对类
   - CGLIB是针对类实现代理，主要是对指定的类生成一个子类，覆盖其中的方法
          因为是继承，所以该类或方法最好不要声明成final 

   Spring AOP会自动在Proxy 和CGLIB 切换， 一般都是 目标对象有接口 默认用Proxy ，但可以强制使用CGLIB ，如果没有接口强制用CGLIB

   更推荐用Java动态代理，原因只有一个JDK 本身支持，升级平滑，代码阅读性、可维护性高。

   

### 7、List与Map

#### 1、集合特性相关

##### List

   特性：可以动态扩容的元素集合

| List       | 底层 | 效率                                                         | 线程 安全                              |      |
| ---------- | ---- | ------------------------------------------------------------ | -------------------------------------- | ---- |
| ArrayList  | 数组 | 随机读写高，插入删除慢（不包括尾插和尾删）影响效率的主要是移动元素 | 不安全                                 |      |
| LinkedList | 链表 | 随机读写慢，插入删除快，不移动元素。                         | 不安全                                 |      |
| Vector     | 数组 | 随机读写高，插入删除慢（不包括尾插和尾删）影响效率的主要是移动元素 | 安全，没人用，有性能更优秀的安全集合。 |      |
| Stack      | 数组 | 先进后出,一次一个元素，不允许随机读写。                      | 安全                                   |      |

##### Map

   特性：key / Value  键值对

| Map       | 元素特性                                                 | 顺序特性 | 线程 安全                              |      |
| --------- | -------------------------------------------------------- | -------- | -------------------------------------- | ---- |
| HashTable | key、value都不能为null                                   | 无序     | 安全，没人用，有性能更优秀的安全集合。 |      |
| HashMap   | key、value可以为null                                     | 无序     | 不安全                                 |      |
| TreeMap   | 默认不能为null，可以通过实现Comparator接口，自行处理null | 有序     | 不安全                                 |      |

   

####  2、线程安全相关

##### List

| 名称                  | 是否安全 | 如何实现安全                                               | 性能         |
| --------------------- | -------- | ---------------------------------------------------------- | ------------ |
| ArrayList、linkedList | N        | /                                                          | 快且不安全   |
| Vector                | Y        | 方法上有Synchronized关键字，锁Class                        | 最慢         |
| Stack                 | Y        | 方法上有Synchronized关键字，锁Class                        | 和Vector一致 |
| SynchronizedList      | Y        | 方法内部用Synchronized关键字，锁对象                       | 比Vector稍好 |
| CopyOnWriteArrayList  | Y        | 读不加锁，写的时候先加锁在copy原数组，进行操作。最后写入。 | 比较不错     |
|                       |          |                                                            |              |
|                       |          |                                                            |              |
|                       |          |                                                            |              |

#####   Map

| 名称              | 是否安全 | 如何实现安全                                          | 性能            |
| ----------------- | -------- | ----------------------------------------------------- | --------------- |
| HashMap           | N        | /                                                     | 快且不安全      |
| HashTable         | Y        | 方法上有Synchronized关键字，锁Class                   | 最慢            |
| SynchronizedMap   | Y        | 方法内部用Synchronized关键字，锁对象                  | 比HashTable稍好 |
| ConcurrentHashMap | Y        | CAS+Synchronized，写时先cas写如果失败就加锁写，读无锁 | 较好            |
|                   |          |                                                       |                 |
|                   |          |                                                       |                 |
|                   |          |                                                       |                 |



### 8、JavaIO

#### IO 常见分类：BIO、NIO、AIO

BIO：阻塞的 IO，在 java.io包下的。**同步、阻塞，是一个连接一个线程**。

NIO：同步非阻塞IO，Java 1.4中引入了NIO框架，在java.nio包下。**同步、非阻塞，是一个请求一个线程**。

AIO：对 NIO 有所改进，就是NIO 2，操作基于事件和回调机制，简单理解为：异步，就是应用操作直接返回，并不会阻塞。Java 7中引入,主要在 java.nio.channels 包下增加了下面四个异步通道。**异步、非阻塞，是一个有效请求一个线程**。

#### 用实际场景来描述三者：

| IO   | 场景                                                         |
| ---- | ------------------------------------------------------------ |
| BIO  | 一个银行，每来一位用户，都聘请一个新的客服来让你填写信息，等你好了，告诉你去哪个机器取钱。 |
| NIO  | 一个银行，只有一个客服，同时服务多个用户，你来了，客服让你填写信息，同时还有多个人在写个人信息，谁写完了就告诉客服好了，客服再告诉他去哪个机器取钱 |
| AIO  | 一个银行，一个客服，你带着一个小弟来，你让小弟填写信息，你接下来暂时自由，等小弟写完给你，你去取钱。 |

用户：用户线程

客服：处理线程

小弟：操作系统

你：用户

#### 同步/异步/阻塞/非阻塞

-   同步 ： 自己亲自出马持银行卡到银行取钱（使用同步 IO 时，Java 自己处理 IO 读写）；
-   异步 ： 委托一小弟拿银行卡到银行取钱，然后给你（使用异步 IO 时，Java 将 IO 读写委托给 OS 处理，需要将数据缓冲区地址和大小传给 OS (银行卡和密码)，OS 需要支持异步 IO 操作 API）；
-   阻塞 ： ATM 排队取款，你只能等待（使用阻塞 IO 时，Java 调用会一直阻塞到读写完成才返回）；
-   非阻塞 ： 柜台取款，取个号，然后坐在椅子上做其它事，等号广播会通知你办理，没到号你就不能去，你可以不断问大堂经理排到了没有，大堂经理如果说还没到你就不能去（使用非阻塞 IO 时，如果不能读写 Java 调用会马上返回，当 IO 事件分发器会通知可读写时再继续进行读写，不断循环直到读写完成）

