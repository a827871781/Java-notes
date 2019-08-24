# JVM 方法调用

## 方法调用大致过程

1. 除非被调用的方法是类方法，每一次方法调用指令之前，JVM 先会把方法被调用的对象引用压入操作数栈中，除了对象的引用之外，JVM 还会把方法的参数依次压入操作数栈。
2. 在执行方法调用指令时，JVM 会将函数参数和对象引用依次从操作数栈弹出，并新建一个栈帧，把对象引用和函数参数分别放入新栈帧的局部变量表 slot0，1，2…。
3. JVM 把新栈帧 push 入虚拟机方法栈，并把 PC 指向函数的第一条待执行的指令。

方法调用不等同于方法执行，方法调用阶段的唯一任务就是确定被调用方法的版本（即确定具体调用那一个方法），不涉及方法内部具体运行。

java 虚拟机中提供了 5 条方法调用的字节码指令：

```java
invokestatic:调用静态方法
invokespecial:调用实例构造器<init>方法、私有方法、父类方法
invokevirtual:调用所有虚方法。
invokeinterface:调用接口方法，在运行时再确定一个实现该接口的对象
invokedynamic:运行时动态解析出调用的方法，然后去执行该方法。
```

Class 文件的编译过程中不包含传统编译中的连接步骤，**一切方法调用在 Class 文件里存储的都只是符号引用**，而不是具体的方法执行入口地址（即直接引用）。

所以对于 java 的方法调用过程就变的复杂起来，需要在类加载期间，甚至是运行期间才能确定目标方法的直接调用。

### 解析

Class 文件里所有的方法调用都是一个常量池中的符号引用，在类的解析阶段，会将其中一部分符号引用转化为直接引用。转化的这部分方法调用必须是：在程序运行之前就有一个可以确定的调用版本，并且这个调用版本在程序运行期间是不可改变的。

即：**编译期可知，运行期不变**的方法调用

这种类型的方法主要有：静态方法、私有方法。

只要能被 invokestatic 和 invokespecial 指令调用的方法都可以在解析阶段中确定唯一调用版本。**符合这个条件主要有：静态方法、私有方法、实例构造器方法、父类方法。他们在类加载的时候就会把符号引用解析为该方法的直接引用。**这些方法可以称为非虚方法。其余就是虚方法

```java
public static void main(String[] args) {
    //构造
    MyClass myClass = new MyClass();
    //虚方法
    myClass.test();
    //构造
    List<String> strings = new ArrayList<>();
    //接口
    strings.add("1");
    //静态
    Arrays.asList("2");

}
```

```java
//字节码
public static main([Ljava/lang/String;)V
   L0
    LINENUMBER 14 L0
    NEW easy/MyClass
    DUP
    INVOKESPECIAL easy/MyClass.<init> ()V  //构造
    ASTORE 1
   L1
    LINENUMBER 16 L1
    ALOAD 1
    INVOKEVIRTUAL easy/MyClass.test ()V   //虚方法
   L2
    LINENUMBER 18 L2
    NEW java/util/ArrayList
    DUP
    INVOKESPECIAL java/util/ArrayList.<init> ()V //构造
    ASTORE 2
   L3
    LINENUMBER 20 L3
    ALOAD 2
    LDC "1"
    INVOKEINTERFACE java/util/List.add (Ljava/lang/Object;)Z (itf) //接口
    POP
   L4
    LINENUMBER 22 L4
    ICONST_1
    ANEWARRAY java/lang/String
    DUP
    ICONST_0
    LDC "2"
    AASTORE
    INVOKESTATIC java/util/Arrays.asList ([Ljava/lang/Object;)Ljava/util/List; //静态
    POP
   L5
    LINENUMBER 24 L5
    RETURN
   L6
    LOCALVARIABLE args [Ljava/lang/String; L0 L6 0
    LOCALVARIABLE myClass Leasy/MyClass; L1 L6 1
    LOCALVARIABLE strings Ljava/util/List; L3 L6 2
    // signature Ljava/util/List<Ljava/lang/String;>;
    // declaration: strings extends java.util.List<java.lang.String>
    MAXSTACK = 4
    MAXLOCALS = 3
```

### 分派

就是如何确定执行哪个方法，这里详细解释了重载和重写。也就是说虚拟机如何确定正确的目标方法

思考以下代码输出？

```java
public class Main2 {
    class A{
    }
    class B extends A{
    }
    public static void f(A a) {
        System.out.println("A");
    }
    public static void f(B b) {
        System.out.println("B");
    }
    public static void main(String[] args) {
        A a = new Main2().new B();
        f(a);
    }
}
```

输出：A

这里将 A 称为**静态类型**或者外观类型，B 称为**实际类型**。

编译器在运行前只知道一个对象的静态类型，并不知道对象的实际类型。

f 方法经过了重载，有两个不同的参数，虚拟机方法调用时，他会直接使用静态类型进行匹配。也就是说：**重载时是通过参数的静态类型而不是实际类型作为判定依据。**并且静态类型是在编译期可知的，因此在编译阶段，javac 编译器就可以根据参数类型确定具体使用哪个重载版本。

#### 静态分派

- **所有依赖静态类型来定位方法执行版本的分派动作称为静态分派**。
- **静态分派的典型应用就是方法重载**。
- **静态分派发生在编译阶段，因此确定静态分派的动作实际上不是由虚拟机来执行的**。

```java
  public static main([Ljava/lang/String;)V
   L0
    LINENUMBER 15 L0
    NEW easy/Main2$B
    DUP
    NEW easy/Main2
    DUP
    INVOKESPECIAL easy/Main2.<init> ()V
    DUP
    INVOKEVIRTUAL java/lang/Object.getClass ()Ljava/lang/Class;
    POP
    INVOKESPECIAL easy/Main2$B.<init> (Leasy/Main2;)V
    ASTORE 1
   L1
    LINENUMBER 16 L1
    ALOAD 1
    INVOKESTATIC easy/Main2.f (Leasy/Main2$A;)V  // A
   L2
    LINENUMBER 17 L2
    RETURN
   L3
    LOCALVARIABLE args [Ljava/lang/String; L0 L3 0
    LOCALVARIABLE a Leasy/Main2$A; L1 L3 1
    MAXSTACK = 4
    MAXLOCALS = 2
}

```

#### 动态分派

这个分派体现了**重写**

主要和 invokevirtual 方法调用字节码有关，运行过程如下：

1. 在方法调用指令之前，需要将对象的引用压入操作数栈
2. 找到操作数栈顶的第一个元素所指向的对象的实际类型，记为 C；
3. 在 C 中寻找与常量中的描述符合简单名都一致的方法，进行权限校验，如通过则返回这个方法的直接引用，查找结束；如果不通过，返回异常。
4. 否则，按照继承关系从下往上依次对 C 的各个父类进行第 2 步搜索和验证。
5. 如果始终没有找到合适的方法，则抛出java.lang.AbstractMethodError异常。

JVM 是通过继承关系从子类往上查找的对应的方法的，为了提高动态分派时方法查找的效率，JVM 为每个类都维护一个**方法表**。

方法表有如下特性:

1. 方法表的每一项是一个指针，指向实际的方法区的代码块的内存首地址
2. 父类的方法表在前，自己的在后面，由此可看出 Object 的方法会出现在所有类的最前面
3. 子类重写父类的方法，会把方法表中对应方法的指针由指向父类的代码块指向自身的代码块。

```java
public class Main2 {
    public static void main(String[] args) {
        A b = new B();
        A c = new C();
        b.print();
        c.print();
    }
}
abstract class A{
    protected abstract void print();
}
class B extends A{
    @Override
    protected void print() {
        System.out.println("B");
    }
}
class C extends A{
    @Override
    protected void print() {
        System.out.println("C");
    }
}
```

 用以下命令查看字节码：`javap -v -c -s -l Main2.class`

![1563784825544.png](https://i.loli.net/2019/07/22/5d3576c916cb465059.png)


以上我们可以知道，对于重写的方法 `print()`，在父类（A）和子类（B和 C）中的方法表的**偏移量都是相同的**，即 6，但里面的指针指向不同代码块。在编译期间，由于静态类型是 A，因此，查找 A方法表中的 `print()`，定位在 6，得到了 `invokevirtual #6` 这个指令；而在运行期间，根据对象的 this 指针知道实际的类型，找到实际类型的方法表，索引到 6 这个位置，由于方法表 `print()` 的偏移量都相同，因此 6 仍是对应 `sayHello()` 方法；继而找到指向子类的代码块的指针进行运行。

