# 工厂方法模式

Spring 中提供了 FactoryBean 接口，用于创建各种不同的 Bean。

开发人员也可以自己实现该接口，常用于框架集成。比如 SqlSessionFactoryBean 就是如此。

# 模板方法模式

Spring 针对 JDBC,JMS,JPA 等规范，都提供了相应的模板方法类，如 JdbcTemplate,JmsTemplate, JpaTemplate。 例如 JdbcTemplate, 它提供了很多常用的增加，删除，查询，修改方法模板。而 JMSTemplate 则提供了对于消息的发送，接收方法等。下面是 JMSTemplate 的部分方法图

# 代理模式

Spring 中 AOP，事务等都大量运用了代理模式。

# 观察者模式

Spring 中提供了一种事件监听机制，即 ApplicationListener，可以实现 Spring 容器内的事件监听。

主要是以下两个接口： 发布消息/监听消息

# 单例模式

Spring 默认的创建 Bean 的作用域就是单例，即每个 Spring 容器中只存在一个该类的实例。可以通过 @Scope (“prototype”) 来修改成 prototype 模式，prototype 在设计模式中叫做原型模式，实际上，Spring 中对于 @Scope (“prototype”) 标记的 Bean 的处理的确是原型模式。

# 原型模式

原型模式是创建型模式的一种，其特点在于通过 “复制” 一个已经存在的实例来返回新的实例，而不是新建实例。被复制的实例就是我们所称的 “原型”，这个原型是可定制的。
 原型模式多用于创建复杂的或者耗时的实例，因为这种情况下，复制一个已经存在的实例使程序运行更高效；或者创建值相等，只是命名不一样的同类数据。

Spring 中，如果一个类被标记为”prototype”, 每一次请求（将其注入到另一个 bean 中，或者以程序的方式调用容器的 getBean () 方法）都会产生一个新的 bean 实例。
 但是，Spring 不能对一个 prototype Bean 的整个生命周期负责，容器在初始化、配置、装饰或者是装配完一个 prototype 实例后，将它交给客户端，随后就对该 prototype 实例不闻不问了。不管何种作用域，容器都会调用所有对象的初始化生命周期回调方法，而对 prototype 而言，任何配置好的析构生命周期回调方法都将不会被调用。清除 prototype 作用域的对象并释放任何 prototype bean 所持有的昂贵资源，都是客户端代码的职责。

# 责任链模式

在 SpringMVC 中，我们会经常使用一些拦截器 (HandlerInterceptor),如Spring中的 Filter就使用到了责任链模式 当存在多个拦截器的时候，所有的拦截器就构成了一条拦截器链。SpringMVC 中使用 HandlerExecutionChain 类来将所有的拦截器组装在一起。
 需要注意的是 preHandle 方法的返回值是 boolean 类型，用于决定是否需要下一个拦截器继续处理。

# 适配器模式

在Spring的Aop中，使用的Advice（通知）来增强被代理类的功能。Spring实现这一AOP功能的原理就使用代理模式（1、JDK动态代理。2、CGLib字节码生成技术代理。）对类进行方法级别的切面增强，即，生成被代理类的代理类， 并在代理类的方法前，设置拦截器，通过执行拦截器重的内容增强了代理方法的功能，实现的面向切面编程。

Adapter类接口：Target

```java
public interface AdvisorAdapter { 
    boolean supportsAdvice(Advice advice);  
    MethodInterceptor getInterceptor(Advisor advisor); 
} 
//MethodBeforeAdviceAdapter类，
Adapter class MethodBeforeAdviceAdapter implements AdvisorAdapter, Serializable {  
    public boolean supportsAdvice(Advice advice) {    
        return (advice instanceof MethodBeforeAdvice); 
    }  
	public MethodInterceptor getInterceptor(Advisor advisor) {   
   		 MethodBeforeAdvice advice = (MethodBeforeAdvice) advisor.getAdvice(); 
   		 return new MethodBeforeAdviceInterceptor(advice);  
	} 
}
```



# 代理模式

为其他对象提供一种代理以控制对这个对象的访问。 从结构上来看和Decorator模式类似，但Proxy是控制，更像是一种对功能的限制，而Decorator是增加职责。 

spring的Proxy模式在aop中有体现，比如JdkDynamicAopProxy和Cglib2AopProxy。 

# 策略模式

定义一系列的算法，把它们一个个封装起来，并且使它们可相互替换。本模式使得算法可独立于使用它的客户而变化。  spring中在实例化对象的时候用到Strategy模式

在SimpleInstantiationStrategy中有代码说明了策略模式的使用情况： 





