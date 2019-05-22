## 桥接模式

将抽象部分与实现部分分离，使它们都可以独立的变化。
将抽象部分与实现部分分离，使它们都可以独立的变化。

增加新的功能，类的功能层次结构

增加新的实现，类的实现层次结构

将功能结构 和实现结构分离，就是桥接模式

### `UML`

![1558010618790](https://github.com/a827871781/Java-notes/blob/master/images/10.png)

```java
//功能层次
public class Display {
    private DisplayImpl impl ;

    public Display(DisplayImpl impl) {
        this.impl = impl;
    }
    public void open(){
        impl.rawOpen();
    }
    public void print(){
        impl.rawPrint();
    }
    public void close(){
        impl.rawClose();
    }
    public final void  display(){
        open();
        print();
        close();
    }
}
//实现层次抽象层
public abstract class DisplayImpl  {
    public abstract  void rawOpen();
    public abstract  void rawPrint();
    public abstract  void rawClose();
}
//新增功能类
public class CountDisplay extends  Display {
    public CountDisplay(DisplayImpl impl) {
        super(impl);
    }
    public void  muliDisplay(int times){
        open();
        for (int i = 0; i < times; i++) {
            print();
        }
        close();
    }
}
//实现层次 实现类
public class StringDisplayImpl extends DisplayImpl {
    private String str;
    private int width ;

    public StringDisplayImpl(String str) {
        this.str = str;
        this.width = str.length();
    }

    @Override
    public void rawOpen() {
        printLine();
    }

    @Override
    public void rawPrint() {
        System.out.println("|"+str+"|");
    }

    @Override
    public void rawClose() {
        printLine();

    }
    private void printLine(){
        System.out.print("+");
        for (int i = 0; i < width; i++) {
            System.out.print("-");
        }
        System.out.println("+");

    }

}

public class Main {
    public static void main(String[] args) {
        Display d1 = new Display(new StringDisplayImpl("AAAAA"));
        Display d2 = new CountDisplay(new StringDisplayImpl("BBBBBB"));
        CountDisplay d3 = new CountDisplay(new StringDisplayImpl("CCCCCCCC"));
        d1.display();
        d2.display();
        d3.muliDisplay(5);
    }
}

+-----+
|AAAAA|
+-----+
+------+
|BBBBBB|
+------+
+--------+
|CCCCCCCC|
|CCCCCCCC|
|CCCCCCCC|
|CCCCCCCC|
|CCCCCCCC|
+--------+
```

### **优点：**

1. 抽象和实现的分离。
2. 桥接模式有时类似于多继承方案，但是多继承方案违背了类的单一职责原则（即一个类只有一个变化的原因），复用性比较差，而且多继承结构中类的个数非常庞大，桥接模式是比多继承方案更好的解决方法。
3. 实现细节对客户透明。
4. 桥接模式提高了系统的可扩充性，在两个变化维度中任意扩展一个维度，都不需要修改原有系统。

### **缺点：**

桥接模式的引入会增加系统的理解与设计难度，由于聚合关联关系建立在抽象层，要求开发者针对抽象进行设计与编程。

**使用场景：** 1、如果一个系统需要在构件的抽象化角色和具体化角色之间增加更多的灵活性，避免在两个层次之间建立静态的继承联系，通过桥接模式可以使它们在抽象层建立一个关联关系。 2、对于那些不希望使用继承或因为多层次继承导致系统类的个数急剧增加的系统，桥接模式尤为适用。 3、一个类存在两个独立变化的维度，且这两个维度都需要进行扩展。

### 总结：

其实就是将 实现和 新增功能分开，如上面代码表现，我如果想要拓展功能只需要对Display  增加实现，拓展功能，而不用对`DisplayImpl `进行修改,

这就是一种委托关系，Display 委托 `DisplayImpl` ，如果说现在要换个形状打印，只需要针对`DisplayImpl` ` 做类的实现结构， Display  不变，反之，Display 要增加功能了，DisplayImpl` 不变。
