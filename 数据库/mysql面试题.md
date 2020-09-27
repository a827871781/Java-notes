## count (1)、count (*) 与 count (列名) 的执行区别

1、`count(1)`  and  `count(\*)` MySQL 官方文档这么说：

>   InnoDB handles SELECT COUNT(*) and SELECT COUNT(1) operations in the same way. There is no performance difference.

所以，对于 `count(1)` 和 `count(*)`，MySQL 的优化是完全一样的，根本不存在谁更快！

但依旧建议使用 `count(*)`，因为这是 SQL92 定义的标准统计行数的语法。

2、`count (1)` and `count (字段)`
两者的主要区别是
`count (1)` 会统计表中的所有的记录数，包含字段为 null 的记录。
`count (字段)` 会统计该字段在表中出现的次数，忽略字段为 null 的情况。即不统计字段为 null 的记录。

3、`count (*) `和` count (1)` 和 `count (列名)` 区别
  **执行效果：**

-   `count (*) ` 包括了所有的列，相当于行数，在统计结果的时候，不会忽略列值为 NULL。
-   `count (1)` 包括了忽略所有列，用 1 代表代码行，在统计结果的时候，不会忽略列值为 NULL 。
-   `count (列名) ` 只包括列名那一列，在统计结果的时候，会忽略列值为空（这里的空不是只空字符串或者 0，而是表示 null）的计数，即某个字段值为 NULL 时，不统计。

  **执行效率：**

-   列名为主键，`count (列名) `会比 `count (1) `快。
-   列名不为主键，`count (1) `会比 `count (列名) `快。
-   如果表多个列并且没有主键，则 `count（1）` 的执行效率优于` count（\*）`。
-   如果有主键，则 `select count（主键）`的执行效率是最优的。
-   如果表只有一个字段，则 `select count（\*）`最优。

  **执行速度：**

   `count(*) ` = `count(1)` > `count(列名)`

