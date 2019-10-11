## Collection与Map比较

### 1、继承关系

#### Collection

**Collection 是对象集合**

1.  List 接口 : 内容允许重复
2.  Set 接口 : 内容不允许重复
3.  Queue接口 : 队列
4.  sortedSet 接口 : 单值排序接口

#### Map

**Map 是键值对集合**

1.  HashMap实现类 : key 可以为null
2.  HashTable实现类 : key不可以为null
3.  TreeMap实现类 : 排序Map
4.  LinkedHashMap实现类 : 有序Map

### 2、集合特性相关

#### Collection

   特性：可以动态扩容的元素集合

| Collection | 底层 | 效率                                                         | 线程 安全                              |      |
| ---------- | ---- | ------------------------------------------------------------ | -------------------------------------- | ---- |
| ArrayList  | 数组 | 随机读写高，插入删除慢（不包括尾插和尾删）影响效率的主要是移动元素 | 不安全                                 |      |
| LinkedList | 链表 | 随机读写慢，插入删除快，不移动元素。                         | 不安全                                 |      |
| Vector     | 数组 | 随机读写高，插入删除慢（不包括尾插和尾删）影响效率的主要是移动元素 | 安全，没人用，有性能更优秀的安全集合。 |      |
| Stack      | 数组 | 先进后出,一次一个元素，不允许随机读写。                      | 安全                                   |      |

#### Map

   特性：key / Value  键值对

| Map       | 元素特性                                                 | 顺序特性 | 线程 安全                              |      |
| --------- | -------------------------------------------------------- | -------- | -------------------------------------- | ---- |
| HashTable | key、value都不能为null                                   | 无序     | 安全，没人用，有性能更优秀的安全集合。 |      |
| HashMap   | key、value可以为null                                     | 无序     | 不安全                                 |      |
| TreeMap   | 默认不能为null，可以通过实现Comparator接口，自行处理null | 有序     | 不安全                                 |      |

   

### 3、线程安全相关

#### Collection

| 名称                  | 是否安全 | 如何实现安全                                               | 性能         |
| --------------------- | -------- | ---------------------------------------------------------- | ------------ |
| ArrayList、linkedList | N        | /                                                          | 快且不安全   |
| Vector                | Y        | 方法上有Synchronized关键字，锁Class                        | 最慢         |
| Stack                 | Y        | 方法上有Synchronized关键字，锁Class                        | 和Vector一致 |
| SynchronizedList      | Y        | 方法内部用Synchronized关键字，锁对象                       | 比Vector稍好 |
| CopyOnWriteArrayList  | Y        | 读不加锁，写的时候先加锁在copy原数组，进行操作。最后写入。 | 比较不错     |
|                       |          |                                                            |              |

#### Map

| 名称              | 是否安全 | 如何实现安全                                          | 性能            |
| ----------------- | -------- | ----------------------------------------------------- | --------------- |
| HashMap           | N        | /                                                     | 快且不安全      |
| HashTable         | Y        | 方法上有Synchronized关键字，锁Class                   | 最慢            |
| SynchronizedMap   | Y        | 方法内部用Synchronized关键字，锁对象                  | 比HashTable稍好 |
| ConcurrentHashMap | Y        | CAS+Synchronized，写时先cas写如果失败就加锁写，读无锁 | 较好            |
|                   |          |                                                       |                 |


