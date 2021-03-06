# Explain 详解与索引最佳实践

使用EXPLAIN关键字可以模拟优化器执行SQL语句，从而知道MySQL是 如何处理你的SQL语句的。分析你的查询语句或是结构的性能瓶颈  

下面是使用 explain 的例子： 

在 select 语句之前增加 explain 关键字，MySQL 会在查询上设置一个标记，执行查询时，会返回执行计划的信息，而不是执行这条SQL（如果 from 中包含子查询，仍会执行该子查询，将结果放入临时表中）

```sql
EXPLAIN SELECT * FROM T
```

在查询中的每个表会输出一行，如果有两个表通过 join 连接查询，那么会输出两行。表的意义相当广泛：可以是子查询、一个 union 结果等。

## explain 中的列

### 1. id列

id列的编号是 select 的序列号，有几个 select 就有几个id，并且id的顺序是按 select 出现的顺序增长的。MySQL将 select 查询分为简单查询(SIMPLE)和复杂查询(PRIMARY)。

复杂查询分为三类：简单子查询、派生表（from语句中的子查询）、union 查询。

id列越大执行优先级越高，id相同则从上往下执行，id为NULL最后执行

### 2. select_type列

select_type 表示对应行是简单还是复杂的查询。

-   **simple**：简单查询。查询不包含子查询和union
-   **primary**：复杂查询中最外层的 select
-   **subquery**：包含在 select 中的子查询（不在 from 子句中）
-   **derived**：包含在 from 子句中的子查询。MySQL会将结果存放在一个临时表中，也称为派生表（derived的英文含义）
-   **union**：在 union 中的第二个和随后的 select
-   **union result**：从 union 临时表检索结果的 select

### 3. table列

这一列表示 explain 的一行正在访问哪个表。

### 4.partitions列

版本 5.7 以前，该项是 explain partitions 显示的选项，5.7 以后成为了默认选项。该列显示的为分区表命中的分区情况。非分区表该字段为空（null）。

### 5. type列

这一列表示关联类型或访问类型，即MySQL决定如何查找表中的行，查找数据行记录的大概范围。

依次从最优到最差分别为：`system > const > eq_ref > ref > range > index > ALL`

一般来说，得保证查询达到range级别，最好达到ref

-   **NULL**：mysql能够在优化阶段分解查询语句，在执行阶段用不着再访问表或索引。例如：在索引列中选取最小值，可以单独查找索引来完成，不需要在执行时访问表

-   **const, system**：mysql能对查询的某部分进行优化并将其转化成一个常量（可以看show warnings 的结果）。用于 primary key 或 unique key 的所有列与常数比较时，所以**表最多有一个匹配行**，读取1次，速度比较快。**system是const**的特例，表里只有一条元组匹配时为**system**

-   eq_ref**：primary key 或 unique key 索引的所有部分被连接使用 ，最多只会返回一条符合条件的记录。这可能是在 const 之外最好的联接类型了，简单的 select 查询不会出现这种 type。**

-   ref：相比 eq_ref，不使用唯一索引，而是使用普通索引或者唯一性索引的部分前缀，索引要和某个值相比较，可能会找到多个符合条件的行。

-   **range**：范围扫描通常出现在 **in(), between ,> ,<, >=** 等操作中。使用一个索引来检索给定范围的行。

-   **index**：扫描全表索引，这通常比ALL快一些。（index是从索引中读取的，而all是从硬盘中读取）

-   **ALL**：即全表扫描，意味着mysql需要从头到尾去查找所需要的行。通常情况下这需要增加索引来进行优化了

    

### 6. possible_keys列

这一列显示查询可能使用哪些索引来查找。 

explain 时可能出现 possible_keys 有列，而 key 显示 NULL 的情况，这种情况是因为表中数据不多，mysql认为索引对此查询帮助不大，选择了全表查询。 

如果该列是NULL，则没有相关的索引。在这种情况下，可以通过检查 where 子句看是否可以创造一个适当的索引来提高查询性能，然后用 explain 查看效果。



### 7. key列

这一列显示mysql实际采用哪个索引来优化对该表的访问。

如果没有使用索引，则该列是 NULL。如果想强制mysql使用或忽视possible_keys列中的索引，在查询中使用 force index、ignore index。



### 8. key_len列

这一列显示了mysql在索引里使用的字节数，通过这个值可以算出具体使用了索引中的哪些列。 

举例来说，film_actor的联合索引 idx_film_actor_id 由 film_id 和 actor_id 两个int列组成，并且每个int是4字节。通过结果中的key_len=4可推断出查询使用了第一个列：film_id列来执行索引查找。

mysql> explain select * from film_actor where film_id = **2**;

![img](https://note.youdao.com/yws/public/resource/5b590cb82e7819dd439f8d0d27d2e8a7/xmlnote/OFFICE0D9E000970BB4A91B292F35F84F46A58/752)

key_len计算规则如下：

-   字符串

-   -   char(n)：n字节长度
    -   varchar(n)：2字节存储字符串长度，如果是utf-8，则长度 3n + 2

-   数值类型

-   -   tinyint：1字节
    -   smallint：2字节
    -   int：4字节
    -   bigint：8字节　　

-   时间类型　

-   -   date：3字节
    -   timestamp：4字节
    -   datetime：8字节

-   如果字段允许为 NULL，需要1字节记录是否为 NULL

索引最大长度是768字节，当字符串过长时，mysql会做一个类似左前缀索引的处理，将前半部分的字符提取出来做索引。



### 9. ref列

这一列显示了在key列记录的索引中，表查找值所用到的列或常量，常见的有：const（常量），字段名（例：film.id）



### 10. rows列

这一列是mysql估计要读取并检测的行数，注意这个不是结果集里的行数。



### 11. Extra列

这一列展示的是额外信息。常见的重要值如下： 

**Using index**：查询的列被索引覆盖，并且where筛选条件是索引的前导列，是性能高的表现。一般是使用了**覆盖索引**(索引包含了所有查询的字段)。对于innodb来说，如果是辅助索引性能会有不少提高

**Using where**：查询的列未被索引覆盖，where筛选条件非索引的前导列

**Using where Using index**：查询的列被索引覆盖，并且where筛选条件是索引列之一但是不是索引的前导列，意味着无法直接通过索引查找来查询到符合条件的数据

**NULL**：查询的列未被索引覆盖，并且where筛选条件是索引的前导列，意味着用到了索引，但是部分字段未被索引覆盖，必须通过“回表”来实现，不是纯粹地用到了索引，也不是完全没用到索引

**Using temporary**：mysql需要创建一张临时表来处理查询。出现这种情况一般是要进行优化的，首先是想到用索引来优化。

**Using filesort**：mysql 会对结果使用一个外部索引排序，而不是按索引次序从表里读取行。此时mysql会根据联接类型浏览所有符合条件的记录，并保存排序关键字和行指针，然后排序关键字并按顺序检索行信息。这种情况下一般也是要考虑使用索引来优化的。



## 索引最佳实践

**使用的表**

```sql
CREATE TABLE `employees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(24) NOT NULL DEFAULT '' COMMENT '姓名',
  `age` int(11) NOT NULL DEFAULT '0' COMMENT '年龄',
  `position` varchar(20) NOT NULL DEFAULT '' COMMENT '职位',
  `hire_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '入职时间',
  PRIMARY KEY (`id`),
  KEY `idx_name_age_position` (`name`,`age`,`position`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COMMENT='员工记录表';

INSERT INTO employees(name,age,position,hire_time) VALUES('LiLei',22,'manager',NOW());
INSERT INTO employees(name,age,position,hire_time) VALUES('HanMeimei', 23,'dev',NOW());
INSERT INTO employees(name,age,position,hire_time) VALUES('Lucy',23,'dev',NOW());
```



### 最佳实践

#### 1. 全值匹配

`EXPLAIN SELECT * FROM employees WHERE name= 'LiLei';`

![img](https://note.youdao.com/yws/public/resource/5b590cb82e7819dd439f8d0d27d2e8a7/xmlnote/OFFICE8ACFECC89985439B93AEF5FAF561D463/762)

`EXPLAIN SELECT * FROM employees WHERE name= 'LiLei' AND age = 22;`

![img](https://note.youdao.com/yws/public/resource/5b590cb82e7819dd439f8d0d27d2e8a7/xmlnote/OFFICE198D2A33545D4CB1997C9DBC2B7DE1EC/763)

`EXPLAIN SELECT * FROM employees WHERE name= 'LiLei' AND age = 22 AND position ='manager';`

![img](https://note.youdao.com/yws/public/resource/5b590cb82e7819dd439f8d0d27d2e8a7/xmlnote/OFFICE56C9330CF4BE4C729E498ABF02F3EB92/764)

#### 2.最佳左前缀法则

 如果索引了多列，要遵守最左前缀法则。指的是查询从索引的最左前列开始并且不跳过索引中的列。

```sql
EXPLAIN SELECT * FROM employees WHERE age = 22 AND position ='manager';
EXPLAIN SELECT * FROM employees WHERE position = 'manager';
EXPLAIN SELECT * FROM employees WHERE name = 'LiLei';
```

![img](https://note.youdao.com/yws/public/resource/5b590cb82e7819dd439f8d0d27d2e8a7/xmlnote/OFFICE5BDFEBCC1B0147CB801A54FE86046C5A/765)



#### 3.不在索引列上做任何操作（计算、函数、（自动or手动）类型转换），会导致索引失效而转向全表扫描

```sql
EXPLAIN SELECT * FROM employees WHERE name = 'LiLei';
EXPLAIN SELECT * FROM employees WHERE left(name,3) = 'LiLei';
```

![img](https://note.youdao.com/yws/public/resource/5b590cb82e7819dd439f8d0d27d2e8a7/xmlnote/OFFICEF96E002497AA4ECB85C9C59512D6D180/766)



#### 4.存储引擎不能使用索引中范围条件右边的列

```sql
EXPLAIN SELECT * FROM employees WHERE name= 'LiLei' AND age = 22 AND position ='manager';
EXPLAIN SELECT * FROM employees WHERE name= 'LiLei' AND age > 22 AND position ='manager';
```

![img](https://note.youdao.com/yws/public/resource/5b590cb82e7819dd439f8d0d27d2e8a7/xmlnote/OFFICE2357D8316F664B3593BE914B5D2E5D16/767)



#### 5.尽量使用覆盖索引（只访问索引的查询（索引列包含查询列）），减少select \*语句

`EXPLAIN SELECT name,age FROM employees WHERE name= 'LiLei' AND age = 23 AND position ='manager';`

![img](https://note.youdao.com/yws/public/resource/5b590cb82e7819dd439f8d0d27d2e8a7/xmlnote/OFFICEAAF9DB7E343044CDB25FF9041B26B8A4/768)

`EXPLAIN SELECT * FROM employees WHERE name= 'LiLei' AND age = 23 AND position ='manager';`

![img](https://note.youdao.com/yws/public/resource/5b590cb82e7819dd439f8d0d27d2e8a7/xmlnote/OFFICE89239C34BF364C6FB4F2659E1071701D/769)



#### 6.mysql在使用不等于（！=或者<>）的时候无法使用索引会导致全表扫描

`EXPLAIN SELECT * FROM employees WHERE name != 'LiLei'`

![img](https://note.youdao.com/yws/public/resource/5b590cb82e7819dd439f8d0d27d2e8a7/xmlnote/OFFICEC217F466DF024690BB7A8326FF731FD1/770)



#### 7.is null,is not null 也无法使用索引

`EXPLAIN SELECT * FROM employees WHERE name is null`

![img](https://note.youdao.com/yws/public/resource/5b590cb82e7819dd439f8d0d27d2e8a7/xmlnote/OFFICE9F559E4E9519481ABBF3D74D28B9F4C9/771)



#### 8.like以通配符开头（'$abc...'）mysql索引失效会变成全表扫描操作

`EXPLAIN SELECT * FROM employees WHERE name like '%Lei'`

![img](https://note.youdao.com/yws/public/resource/5b590cb82e7819dd439f8d0d27d2e8a7/xmlnote/OFFICE6056FD3E5F9848B783F1D362A48BA362/772)

`EXPLAIN SELECT * FROM employees WHERE name like 'Lei%'`

![img](https://note.youdao.com/yws/public/resource/5b590cb82e7819dd439f8d0d27d2e8a7/xmlnote/OFFICEBAED7AD506064EA6B90D64A6F58F67F5/773)

##### 8.1解决like'%字符串%'索引不被使用的方法？

-   使用覆盖索引，查询字段必须是建立覆盖索引字段

`EXPLAIN SELECT name,age,position FROM employees WHERE name like '%Lei%';`

![img](https://note.youdao.com/yws/public/resource/5b590cb82e7819dd439f8d0d27d2e8a7/xmlnote/OFFICE3A14ED1010F84ED2AA81ED6362099024/774)

-   当覆盖索引指向的字段是varchar(380)及380以上的字段时，覆盖索引会失效！



#### **9.**字符串不加单引号索引失效0

```sql
EXPLAIN SELECT * FROM employees WHERE name = '1000';
EXPLAIN SELECT * FROM employees WHERE name = 1000;
```

![img](https://note.youdao.com/yws/public/resource/5b590cb82e7819dd439f8d0d27d2e8a7/xmlnote/OFFICE09487C8ADED041C5B57F0688CE1ACECC/775)



#### 10.少用or,用它连接时很多情况下索引会失效

`EXPLAIN SELECT * FROM employees WHERE name = 'LiLei' or name = 'HanMeimei';`

![img](https://note.youdao.com/yws/public/resource/5b590cb82e7819dd439f8d0d27d2e8a7/xmlnote/OFFICE481AF40230364BA6AEEA62753C80E131/776)

## 总结：

![img](https://note.youdao.com/yws/public/resource/5b590cb82e7819dd439f8d0d27d2e8a7/xmlnote/OFFICE1AC2661D17284CF19A863CE60DCECB92/777)

 like KK% 相当于 = 常量，%KK和%KK% 相当于范围