# jdk8

### 1.允许在接口中有默认方法实现

Java 8 允许使用**default**关键字，为接口声明添加非抽象的方法实现。这个特性又被称为**扩展方法**。

```java
interface Formula {
    double calculate(int a);

    default double sqrt(int a) {
        return Math.sqrt(a);
    }
}
```

接口可以定义的范围

- **常量**
- **抽象方法**
- **默认方法**
- **静态方法**



**注：如果接口和父类都存在都存在同名方法的默认实现，则子类必须重写该接口**

### 2.Lambda表达式

**针对String排序并打印：**

 1.8之前代码 ：

```java
     List<String> names = Arrays.asList("a", "d", "b", "c");

        Collections.sort(names, new Comparator<String>() {
            @Override
            public int compare(String a, String b) {
                return b.compareTo(a);
            }
        });

        for (String name : names) {
            System.out.println(name);
        }
```

1.8之后代码 ：

```java
 List<String> names = Arrays.asList("a", "d", "b", "c");

        Collections.sort(names, ( a,  b) -> b.compareTo(a));

        names.forEach(name-> System.out.println(name));
```

**Java编译器能够自动识别参数的类型**

对于**lambda**表达式外部的变量，其访问权限的粒度与匿名对象的方式非常类似。可以访问局部对应的外部区域的局部**final**变量，以及成员变量和静态变量。

默认方法无法在**lambda**表达式内部被访问。

### 3.函数式接口

Lambda表达式能通过一个特定的接口，与一个给定的类型进行匹配。

**特定的接口：接口定义时加入@FunctionalInterface注解，并只定义了一个抽象方法的接口**

```java
@FunctionalInterface
interface Converter<F, T> {
   T convert(F from);
}
//实例化转换接口对象
Converter<String, Integer> converter = (from) -> Integer.valueOf(from);
Integer converted = converter.convert("123");
System.out.println(converted); // 123
```

### 4.方法和构造函数引用

> **Java 8 允许你通过 " :: "  关键字获取方法或者构造函数的的引用。**
>
> 

```java
//通过静态方法引用:
Converter<String, Integer> converter = Integer::valueOf;
Integer converted = converter.convert("123");
System.out.println(converted); // 123

List<String> names = Arrays.asList("peter", "anna", "mike", "xenia");
names.forEach(System.out::println);

//通过对象方法引用
class Something {
    String startsWith(String s) {
        return String.valueOf(s.charAt(0));
    }
}

Something something = new Something();
Converter<String, String> converter = something::startsWith;
String converted = converter.convert("Java");
System.out.println(converted); // "J"


//通过： 引用构造函数

 class User {
    private String name ;

    public User() {}

    public User(String name) {
        this.name = name ;
    }
     @Override
     public String toString() {
         return "User{" +
                 "name='" + name + '\'' +
                 '}';
     }
}


//User工厂接口
public interface UserFactory <U extends User> {
    U create(String name);
}
//通过构造函数引用 实例一个工厂
    UserFactory<User> userFactory = User::new;
    User user = userFactory.create("张三");
    System.out.println(user);  //User{name='张三'}
```

### 5.Optionals

**Optional**用来防止**NullPointerEception**产生。

**Optional**是一个简单的值容器，这个值可以是**null**，也可以是**non-null**。考虑到一个方法可能会返回一个**non-null**的值，也可能返回一个空值。为了不直接返回**null**，我们在Java 8中就返回一个**Optional**.

```java
Optional<String> optional = Optional.of("bam");

optional.isPresent(); // true
optional.get(); // "bam"
optional.orElse("fallback"); // "bam"

optional.ifPresent((s) -> System.out.println(s.charAt(0))); // "b"
```

### 6.时间日期API

Java 8的日期和时间类包含`LocalDate`、`LocalTime`、LocalDateTime、`Instant`、`Duration`以及`Period`，这些类都包含在`java.time`包中

Java 8日期/时间API是JSR-310的实现，它的实现目标是克服旧的日期时间实现中所有的缺陷，新的日期/时间API的一些设计原则是：

1. 不变性：新的日期/时间API中，所有的类都是不可变的，这对多线程环境有好处。
2. 关注点分离：新的API将人可读的日期时间和机器时间（unix timestamp）明确分离，它为日期（Date）、时间（Time）、日期时间（DateTime）、时间戳（unix timestamp）以及时区定义了不同的类。
3. 清晰：在所有的类中，方法都被明确定义用以完成相同的行为。举个例子，要拿到当前实例我们可以使用now()方法，在所有的类中都定义了format()和parse()方法，而不是像以前那样专门有一个独立的类。为了更好的处理问题，所有的类都使用了工厂模式，一旦你使用了其中某个类的方法，与其他类协同工作并不困难。
4. 实用操作：所有新的日期/时间API类都实现了一系列方法用以完成通用的任务，如：加、减、格式化、解析、从日期/时间中提取单独部分，等等。
5. 可扩展性：新的日期/时间API是工作在ISO-8601日历系统上的，但我们也可以将其应用在非IOS的日历上。

```java

//获取今天的日期
LocalDate today = LocalDate.now();

//获取年、月、日信息  
LocalDate today = LocalDate.now();
int year = today.getYear();
int month = today.getMonthValue();
int day = today.getDayOfMonth();

//处理特定日期    
LocalDate dateOfBirth = LocalDate.of(2020, 01, 14);

//判断两个日期是否相等
LocalDate today = LocalDate.now();
LocalDate date1 = LocalDate.of(2019, 01, 14);
if(date1.equals(today)){}

//判断日期是早于还是晚于另一个日期
LocalDate tomorrow = LocalDate.of(2019, 1, 15);
if(tommorow.isAfter(today)){}

if(today.isBefore(tomorrow)){}

//在现有的时间上增加小时
LocalTime time = LocalTime.now();
LocalTime newTime = time.plusHours(2); 

//一年后
LocalDate nextYear = time.plus(1, YEARS);

//获取时间戳  时间戳内包含日期 和时间
Instant timestamp = Instant.now();

//格式化 字符串转时间
String dayAfterTommorrow = "20140116";
LocalDate formatted = LocalDate.parse(dayAfterTommorrow,
                        DateTimeFormatter.BASIC_ISO_DATE);
//时间转字符串
LocalDateTime arrivalDate  = LocalDateTime.now();
try {
    DateTimeFormatter format = DateTimeFormatter.ofPattern("MMM dd yyyy  hh:mm a");
    String landing = arrivalDate.format(format);
    System.out.printf("Arriving at :  %s %n", landing);
} catch (DateTimeException ex) {
    System.out.printf("%s can't be formatted!%n", arrivalDate);
    ex.printStackTrace();
}
//时间差

LocalDateTime start1 = LocalDateTime.now();
LocalDateTime end1 = LocalDateTime.now();
Duration.between(start1, end1).toMillis();



```



### 7.Stream

**java.util.Stream**表示了某一种元素的序列，在这些元素上可以进行各种操作。**Stream**操作可以是中间操作，也可以是完结操作。完结操作会返回一个某种类型的值，而中间操作会返回流对象本身，并且你可以通过多次调用同一个流操作方法来将操作结果串起来。



```java
  		//查询id
		List<String> strArr = new ArrayList<>();
        for (Role role : roles) {
            strArr.add(role.getId();
        }

        List<String> roleIds = roleList.stream().map(role -> role.getId()).collect(Collectors.toList());
		
		//查询ID及name
		Map<String, String> map = null;
        List<Map<String, String>> listMap = new ArrayList<>();
        for (Brand brand : brands) {
            map = new HashMap<>();
            map.put("id",brand.getId());
            map.put("name",brand.getName());
            listMap.add(map);
        }

	List<Map<String, String>> listMap = list.stream().map(arry ->
		{
			Map<String, String> map = new HashMap<>();
			map.put("id", String.valueOf(arry[0]));
			map.put("name", String.valueOf(arry[1]));
			return map;
		}).collect(Collectors.toList());
		
   
   
   //性能比较
   
    public static void main(String[] args) {
        List<String> collect = new ArrayList<>();
        for (int i = 0; i < 1000000; i++) {
            collect.add("ab");
            collect.add("cd");
            collect.add("ef");
        }

		//stream
        LocalDateTime start1 = LocalDateTime.now();

        ArrayList<String> collect1 = collect.stream()
                .filter("ab"::contains)
                .map(e->e.toUpperCase()+ Instant.now().getNano())
                .collect(Collectors.toCollection(ArrayList::new));

        LocalDateTime end1 = LocalDateTime.now();
		//for
        LocalDateTime start2 = LocalDateTime.now();
        List<String> list = new ArrayList<>();
        for (String s  : collect1) {
            if ("ab".contains(s)){
                list.add(s);
            }
        }
        List<String> list1 = new ArrayList<>();
        for (String s : list) {
            list1.add( s.toUpperCase() + Instant.now().getNano());
        }
        LocalDateTime end2 = LocalDateTime.now();

        System.out.println("strem 所用时间 :" +Duration.between(start1, end1).toMillis());
        System.out.println("for 所用时间 :"+Duration.between(start2, end2).toMillis());
        //10000 Stream串行流
        //strem 所用时间 :27
        //for 所用时间 :17
        //strem 所用时间 :32
        //for 所用时间 :19
        //strem 所用时间 :32
        //for 所用时间 :21
        
        //10000000  Stream串行流
        //strem 所用时间 :3926
		//for 所用时间 :4142
        //strem 所用时间 :3818
		//for 所用时间 :3889
        //strem 所用时间 :4041
		//for 所用时间 :4129
        
        
        // 10000000 parallelStream 并行流
        //strem 所用时间 :3293
		//for 所用时间 :4265
        //strem 所用时间 :3613
		//for 所用时间 :4024
        //strem 所用时间 :2956
		//for 所用时间 :4639

    }
```

### 结果

1. 对于简单操作，比如最简单的遍历，Stream串行API性能明显差于显示迭代。
2. 对于复杂操作，Stream串行API性能可以和手动实现的效果匹敌，在并行执行时Stream API效果远超手动实现。









