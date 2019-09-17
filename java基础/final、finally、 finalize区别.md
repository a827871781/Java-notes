### final、finally、 finalize区别

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