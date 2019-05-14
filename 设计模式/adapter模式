# 适配器模式

# UML

![1555587976595](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1555587976595.png)

```java
public interface Target {
	public void request();
}

/**
 * 适配器
 * 
 * @author amosli
 *
 */
public class Adapter implements Target {

	private Adaptee adaptee = new Adaptee();

	@Override
	public void request() {
		adaptee.specialRequest();
	}

}




public class Adaptee {
	public void specialRequest() {
		System.out.println("special...");
	}
}

/**
 * 客户端
 * 
 * @author amosli
 *
 */
public class Client {
	public static void main(String[] args) {
		Target adapter = new Adapter();
		adapter.request();
	}
}
```

# 使用场景

1.  系统需要使用现有的类，而这些类的接口不符合系统的接口。

2.  想要建立一个可以重用的类，用于与一些彼此之间没有太大关联的一些类，包括一些可能在将来引进的类一起工作。
3.　 两个类所做的事情相同或相似，但是具有不同接口的时候。
4.　 旧的系统开发的类已经实现了一些功能，但是客户端却只能以另外接口的形式访问，但我们不希望手动更改原有类的时候。
5.　 使用第三方组件，组件接口定义和自己定义的不同，不希望修改自己的接口，但是要使用第三方组件接口的功能。

# 总结

适配器模式两种情况

- 一个类继承一个类 并实现一个接口，重接接口方法，方法内调用父类方法（继承）

- 一个类继承一个类/接口并持有另一个类的实例，重写父类方法，调用实例方法（使用委托）

适配器模式一般用于对于已有的设计进行衔接，不要在系统设计之初就开始考虑使用适配器模式，尽量使用其他模式代替！



# 相关的设计模式

- Visitor模式（访问者）：iterator模式是从集合中取元素遍历，Visitor模式则可以在遍历元素过程中，对元素进行相同的处理。
- Factory Method模式（工厂方法）：在iterator方法中生成Iterator的实例可能使用Factory Method模式   

