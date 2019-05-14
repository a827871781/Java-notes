1. from  查询的基表
2.  join  关联另一张表
3.  on  与另一张表关联关系
4.  where  筛选条件
5. group by  分组 (开始使用select中的别名，后面的语句中都可以使用)
6.  avg,sum  聚合函数
7. having  配合group by  关键字 做删选
8.  select  查询显示的列
9. distinct   去重
10.  order by  排序
11.  limit   分页

SQL语言不同于其他编程语言的最明显特征是处理代码的顺序。在大多数据库语言中，代码按编码顺序被处理。但在SQL语句中，第一个被处理的子句式FROM，而不是第一出现的SELECT。

每一步都会生成一张虚拟表

join 多张表 会多次循环 1 2 3 步 重复生成虚拟表