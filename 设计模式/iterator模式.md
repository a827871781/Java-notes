# 迭代器模式

### UML图

![1555503705127](https://github.com/a827871781/Java-notes/blob/master/images/8.png)

```java
public  abstract class Aggregate {
	public abstract Iterator ConcreteIterator();
}

public abstract class Iterator {
	public abstract Object first();

	public abstract Object last();

	public abstract Object next();

	public abstract Boolean isDone();

	public abstract Object currentItem();
}


public class ConcreteAggregate extends Aggregate {
	private List<Object> items = new ArrayList<Object>();

	@Override
	public Iterator ConcreteIterator() {
		return new ConcreteIterator(this);
	}

	public Object get(int index) {
		return items.get(index);
	}

	public int size() {
		return items.size();
	}

	public void add(Object obj) {
		items.add(obj);
	}

}

public class ConcreteIterator extends Iterator {
	private ConcreteAggregate concreteAggregate;

	public ConcreteIterator(ConcreteAggregate concreteAggregate) {
		this.concreteAggregate = concreteAggregate;
	}

	private int count=0;

	@Override
	public Object first() {
		return concreteAggregate.get(0);
	}

	@Override
	public Object last() {
		return concreteAggregate.get(concreteAggregate.size() - 1);
	}

	@Override
	public Object next() {
		return concreteAggregate.get(count++);
	}

	@Override
	public Object currentItem() {
		return concreteAggregate.get(count);
	}

	@Override
	public Boolean isDone() {
		return count >= concreteAggregate.size();
	}

}


public class Client {
	public static void main(String[] args) {
		ConcreteAggregate aggregate = new ConcreteAggregate();
		for (int i = 0; i < 10; i++) {
			aggregate.add("i" + i);
		}
		ConcreteIterator iterator = new ConcreteIterator(aggregate);

		System.out.println(aggregate.size());
		System.out.println("first:" + iterator.first());
		System.out.println("last:" + iterator.last());
		System.out.println("current:" + iterator.last());

		while (!iterator.isDone()) {
			System.out.println(iterator.next());
		}

		System.out.println("over");
	}
}
```

# 使用场景

1.  当你需要访问一个聚合对象，而且不管这些对象是什么都需要遍历的时候，就应该考虑使用迭代器模式。
2.  另外，当需要对聚集有多种方式遍历时，可以考虑去使用迭代器模式。

# 优缺点

### 1、优点

- 简化了遍历方式，对于对象集合的遍历，还是比较麻烦的，对于数组或者有序列表，我们尚可以通过游标来取得，但用户需要在对集合了解很清楚的前提下，自行遍历对象，但是对于hash表来说，用户遍历起来就比较麻烦了。而引入了迭代器方法后，用户用起来就简单的多了。
- 可以提供多种遍历方式，比如说对有序列表，我们可以根据需要提供正序遍历，倒序遍历两种迭代器，用户用起来只需要得到我们实现好的迭代器，就可以方便的对集合进行遍历了。
- 封装性良好，用户只需要得到迭代器就可以遍历，而对于遍历算法则不用去关心。

### 2、缺点

- 对于比较简单的遍历（像数组或者有序列表），使用迭代器方式遍历较为繁琐，大家可能都有感觉，像ArrayList，我们宁可愿意使用for循环和get方法来遍历集合。

# 总结
实际开发中可能会遇到**ArrayList** 完全足够。了解即可。 ArrayList 就是根据迭代器模式所设计。

引用迭代器模式可以将底层细节隐藏，无论底层使用数组实现 亦或是 链表实现，对于使用者而言，使用方式不变

```java

	while (!iterator.isDone()) {
			System.out.println(iterator.next());
    }

```

# 相关的设计模式

- Visitor模式（访问者）：iterator模式是从集合中取元素遍历，Visitor模式则可以在遍历元素过程中，对元素进行相同的处理。
- Factory Method模式（工厂方法）：在iterator方法中生成Iterator的实例可能使用Factory Method模式   

