## 什么是 flyway

*Flyway is an open-source database migration tool. It strongly favors simplicity and convention over configuration.*

Flyway 是一个简单开源数据库版本控制器（约定大于配置），主要提供 migrate、clean、info、validate、baseline、repair 等命令。它支持 SQL（PL/SQL、T-SQL）方式和 Java 方式，支持命令行客户端等，还提供一系列的插件支持（Maven、Gradle、SBT、ANT 等）。

官方网站：[flywaydb.org/](https://flywaydb.org/)

## 为什么要使用 flyway

痛点:

每次提测/上线,都要给测试/运维人员发送数据库脚本文件

## Flyway 的工作原理

flyway 会在 DB 中先创建一个 metdata 表 (缺省表名为 flyway_schema_history), 在该表中保存着每次 执行脚本 的记录，记录包含  脚本的版本号和 SQL 脚本的 checksum 值。当一个新的 SQL 脚本被扫描到后，Flyway 解析该 SQL 脚本的版本号，并和 metadata 表已 执行 的的 记录 对比，如果该 SQL 脚本版本大于当前记录表内最大版本的话，将在指定的 DB 上执行该 SQL 文件，否则跳过该 SQL 文件.

两个 flyway 版本号的比较，采用左对齐原则，缺位用 0 代替。举例如下:

-   1.2.9.4 比 1.2.9 版本高.
-   1.2.10 比 1.2.9.4 版本高.
-   1.2.10 和 1.2.010 版本号一样高，每个版本号部分的前导 0 会被忽略.

## sql 脚本的命名规范

prefix: default:V (大写) 

version: 版本号的数字间以 "." 或 "_" 分隔开  

separator: 分隔符，双下划线 __  

description: 描述（必须要有意义）  

suffix: 后缀 default:  .sql

 格式:V+ 版本号 + 分隔符+ 描述 + 后缀名

例如：

`V1.0.1__initial.sql `

` V1.0.2__updata.sql。`

注意 V1默认用于创建记录表.所以,新建脚本的版本要大于V1

## springboot 集成 flyway

最后有源码

### pom添加依赖

```xml
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-core</artifactId>
</dependency>
```

### properties添加配置

```properties
spring.datasource.driverClassName = com.mysql.jdbc.Driver
spring.datasource.url = jdbc:mysql://x.x.x.x:3306/test
spring.datasource.username = root
spring.datasource.password = x

## 设定 flyway 属性
# flyway 的 clean 命令会删除指定 schema 下的所有 table, 杀伤力太大了, 应该禁掉.
spring.flyway.cleanDisabled = true
# 启用或禁用 flyway
spring.flyway.enabled=true
spring.flyway.encoding=utf-8

#sql文件存放位置
spring.flyway.locations=classpath:db/migration

#版本记录表格
# 设定 flyway 的 metadata 表名, 缺省为 flyway_schema_history
spring.flyway.table=schemas_version
spring.flyway.baseline-on-migrate=true
spring.flyway.validate-on-migrate=false


```

### 创建脚本

根据spring.flyway.locations 配置的路径,在resources目录 下创建文件夹,并将sql脚本文件放在该文件夹内

![26400f00-11ba-11ea-a46b-acde48001122](https://i.loli.net/2019/11/28/xoz2FaV1u35fimA.png )

### 完成以上配置,就可以启动项目查看,脚本是否执行了.

## 注意事项

Flyway 通过在spring.flyway.table配置的表,.在每次执行脚本时都会将信息记录在该表内. 

如果一个脚本已经执行过了,就不会再次执行.

如果一个脚本命名低于当前最高的版本号,同样也是不会执行的.

如果想要再次执行某个脚本,可以通过删除记录表内的记录,便可再次执行.



如果是已经有的项目,可以直接新增相关依赖.并不会影响到原来的项目.

## 源码

https://github.com/a827871781/springboot-flyway