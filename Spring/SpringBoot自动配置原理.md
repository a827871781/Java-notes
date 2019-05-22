### SpringBoot自动配置

记住一句话 ：约定优于配置。简单的说 就是默认是都有的，但是我们可以选择用自己的或者不要某些默认的

其原理依赖于@Conditional注解来实现的。

@EnableAutoConfiguration 用来开启自动配置

通过调用SpringFactoriesLoader.loadFactoryNames扫描加载含有META-INF/spring.factories文件的jar包，该文件记录了具有哪些自动配置类。

![1557885968756](https://github.com/a827871781/Java-notes/blob/master/images/4.png)

再结合@Conditional注解进行条件注入

![1557886037513](https://github.com/a827871781/Java-notes/blob/master/images/5.png)

