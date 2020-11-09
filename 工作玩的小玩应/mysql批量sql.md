MySQL 的 JDBC 连接的 url 中要加 rewriteBatchedStatements 参数，并保证 5.1.13 以上版本的驱动，才能实现高性能的批量插入。
MySQL JDBC 驱动在默认情况下会无视 executeBatch () 语句，把我们期望批量执行的一组 sql 语句拆散，一条一条地发给 MySQL 数据库，批量插入实际上是单条插入，直接造成较低的性能。
只有把 rewriteBatchedStatements 参数置为 true, 驱动才会帮你批量执行 SQL
另外这个选项对 INSERT/UPDATE/DELETE 都有效

