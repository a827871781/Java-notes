# GitHub骚操作

## 1、通过in关键字限制搜索范围

**xxx in:name**  项目名包含 xxx 的

**xxx in:description** 项目描述包含 xxx 的

**xxx in:readme** 项目的 readme 文件中包含 xxx 的

也可以通过 **xxx in:name,desciption** 来组合使用

![s1.png](https://i.loli.net/2019/08/09/LdQMglsWIo3K6xb.png)
![s.png](https://i.loli.net/2019/08/09/Py7oNKFHJjR9VhA.png)
![s3.png](https://i.loli.net/2019/08/09/YIQ13NETMl6Vm8u.png)
![s2.png](https://i.loli.net/2019/08/09/nh4rM3Gpxwo9H8d.png)
![s4.png](https://i.loli.net/2019/08/09/z8yjULqxbtrfo1S.png)

## 2、通过 Star 或者 Fork 数 去查找项目

通过通配符 > < = 即可，区间范围内可通过 num1..num2

如，要查找 stars 数不小于 5000的 springboot 项目

**springboot  stars:>=5000**
![s1.png](https://i.loli.net/2019/08/09/Sa32wAPmjpxR9eQ.png)


forks 大于等于 2000

**springboot forks:>2000**

![s2.png](https://i.loli.net/2019/08/09/orj2tqfwGIJp1en.png)

查找 fork 在 100 到 200 之间 且 stars 数在 80 到 100 之间的 springboot 项目

**springboot forks:500..5000 stars:8000..10000**
![s3.png](https://i.loli.net/2019/08/09/N4l5BSpkXhafeFW.png)



## 3、awesome + 关键字



搜索和关键字匹配的优秀项目

**awesome XXX**   搜索 XXX 相关的优秀项目，包括框架、教程等

如：**awesome springboot**  搜索 springboot相关的优秀项目，包括框架、教程等

一般是用来收集学习、工具、书籍类相关的项目

  ![s1.png](https://i.loli.net/2019/08/09/hazr4RQGwO91gsx.png)

我点进去了，发现查出来的所有仓库Readme 内开头都是awesome  我不知道 这个结果 是GitHub认为的优秀项目，还是说，写了就能查到。
![s1.png](https://i.loli.net/2019/08/09/SZyOjgUClx1iuR8.png)

我个人不会选择这种查询方式。star+fork数高的，就够我学的，最起码，他们 被很多人认可过。





## 4、分享项目中某一行的代码

只需要在具体的网址后面拼接 #Lxx (xx 为行数)

如 https://github.com/spring-projects/spring-framework/blob/master/spring-aop/src/test/java/test/aop/PerThisAspect.java
![s2.png](https://i.loli.net/2019/08/09/qVUKGiMR7FxHN4t.png)


我需要分享这个类中的 @Aspect注解，值需要在后面拼接上#L23即可

 https://github.com/spring-projects/spring-framework/blob/master/spring-aop/src/test/java/test/aop/PerThisAspect.java#L23

浏览器访问 就可以发现高亮了

也可以段落高亮  **#L6-L10**

 ![s1.png](https://i.loli.net/2019/08/09/92rnV7AeDNt3go6.png)

## 5、搜索某个地区内的大佬

可以通过 location: 地区 进行检索，在具体可以通过 language: 语言  缩小检索范围

如搜索地区在北京的 Java 方向的用户

location:beijing language:java



## 6、GitHub快捷键





## 7、GitHub谷歌插件

**Octotree**：可以将项目的目录结构以树形结构显示，点击之后会自动跳转到相应的目录



## 8、总结

| 查询方式                                     | 仓库数 |
| -------------------------------------------- | ------ |
| SpringBoot                                   | 97405  |
| SpringBoot in:name                           | 77068  |
| SpringlBoot in:readme                        | 53250  |
| SpringBoot in:description                    | 33687  |
| SpringBoot in:readme,name,descripition       | 108727 |
| springboot  stars:>=5000                     | 8      |
| springboot forks:>2000                       | 7      |
| springboot forks:500..5000 stars:8000..10000 | 2      |
|                                              |        |

没有统计 3 4 5 

因为 我感觉我用不到。

**star + fork** 搜热门。一定要会

**in** 的话 可以用来搜一搜冷门的。