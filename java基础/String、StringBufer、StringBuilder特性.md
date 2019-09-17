# String

## (1) String的创建机理

由于String在Java世界中使用过于频繁，Java为了避免在一个系统中产生大量的String对象，引入了字符串常量池。其运行机制是：创建一个字符串时，首先检查池中是否有值相同的字符串对象，如果有则不需要创建直接从池中刚查找到的对象引用；如果没有则新建字符串对象，返回对象引用，并且将新创建的对象放入池中。但是，通过new方法创建的String对象是不检查字符串池的，而是直接在堆区或栈区创建一个新的对象，也不会把对象放入池中。上述原则只适用于通过直接量给String对象引用赋值的情况。
举例：

```java
String str1 = "123"; //通过直接量赋值方式，放入字符串常量池
String str2 = new String(“123”);//通过new方式赋值方式，不放入字符串常量池
```

注意：String提供了inter()方法。调用该方法时，如果常量池中包括了一个等于此String对象的字符串（由equals方法确定），则返回池中的字符串。否则，将此String对象添加到池中，并且返回此池中对象的引用。

## (2) String的特性

-   **不可变**。是指String对象一旦生成，则不能再对它进行改变。不可变的主要作用在于当一个对象需要被多线程共享，并且访问频繁时，可以省略同步和锁等待的时间，从而大幅度提高系统性能。不可变模式是一个可以提高多线程程序的性能，降低多线程程序复杂度的设计模式。
-   **针对常量池的优化**。当2个String对象拥有相同的值时，他们只引用常量池中的同一个拷贝。当同一个字符串反复出现时，这个技术可以大幅度节省内存空间。

# StringBufer/StringBuilder

## 相同:

StringBufer和StringBuilder都实现了AbstractStringBuilder抽象类，拥有几乎一致对外提供的调用接口；其底层在内存中的存储方式与String相同，都是以一个有序的字符序列（char类型
的数组）进行存储，不同点是**StringBufer/StringBuilder对象的值是可以改变的，并且值改变以后，对象引用不会发生改变;两者对象在构造过程中，首先按照默认大小申请一个字符数组，由于会不断加入新数据，当超过默认大小后，会创建一个更大的数组，并将原先的数组内容复制过来，再丢弃旧的数组。因此，对于较大对象的扩容会涉及大量的内存复制操作，如果能够预先评估大小，可提升性能。**

## 不同:

**StringBufer是线程安全的**，**StringBuilder是线程不安全的**。可参看Java标准类库的源代码，StringBufer类中方法定义前面都会有synchronize关键字。为此，StringBufer的性能要远低于StringBuilder。

# 其他

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