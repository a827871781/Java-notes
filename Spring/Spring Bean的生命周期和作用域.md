# Spring Bean的生命周期和作用域

## Spring Bean生命周期分为创建和销毁两个过程。

### 创建

-   实例化Bean对象。 设置Bean属性。
-   如果我们通过各种Aware接口声明了依赖关系，则会注入Bean对容器基础设施层面的依赖。具体包括BeanNameAware、BeanFactoryAware和ApplicationContextAware，分别会注入Bean ID、Bean Factory或者ApplicationContext。
-   调用BeanPostProcessor的前置初始化方法postProcessBeforeInitialization。 
-   如果实现了InitializingBean接口，则会调用afterPropertiesSet方法。 
-   调用Bean自身定义的init方法。
-   调用BeanPostProcessor的后置初始化方法postProcessAfterInitialization。
-    创建过程完毕。

![51703b48-d91e-11e9-a209-acde48001122](https://i.loli.net/2019/09/17/jw2HPqYaskyfZdx.png )

### 销毁

Spring Bean的销毁过程会依次调用**DisposableBean的destroy**方法和**Bean自身定制的destroy**方法。

## Spring Bean有五个作用域

### 最基础的有下面两种:

-   **Singleton**，这是Spring的默认作用域，也就是为每个IOC容器创建唯一的一个Bean实例。
-   **Prototype**，针对每个getBean请求，容器都会单独创建一个Bean实例。

从Bean的特点来看，Prototype适合有状态的Bean，而Singleton则更适合无状态的情况。另外，使用Prototype作用域需要经过仔细思考，毕竟频繁创建和销毁Bean是有明显开销的。

### 如果是Web容器，则支持另外三种作用域:

-   Request，为每个HTTP请求创建单独的Bean实例。
-   Session，很显然Bean实例的作用域是Session范围。
-   GlobalSession，用于Portlet容器，因为每个Portlet有单独的Session，GlobalSession提供一个全局性的HTTP Session。