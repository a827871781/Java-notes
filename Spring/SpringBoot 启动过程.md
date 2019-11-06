# `SpringBoot `启动过程

1. `new SpringApplication`  
2. 加载webApplicationType 对象 推断是web环境 还是非web环境
3. 通过`SpringFactoriesLoader`，加载`META-INF/spring.factories` 所有`ApplicationContextInitializer、     `ApplicationListener`
4. 通过堆栈里获取的方式，判断 `main `函数，找到原始启动的 `main` 函数
5. 然后由 `SpringApplicationRunListener` 来发出 starting 消息
6. 创建参数，并配置当前 `SpringBoot` 应用将要使用的` Environment`
7. 完成之后，依然由 `SpringApplicationRunListener` 来发出 environmentPrepared 消息
8. 创建 `ApplicationContext` 
9. 初始化 `ApplicationContext`
10. 设置 `context` 环境变量
11. 注册`internalConfigurationBeanNameGenerator`实例  
12. 执行`ApplicationContextInitializer.initialize`方法
13. 通过bean工厂注册`springApplicationArguments`的单例对象
14. 由 `SpringApplicationRunListener` 来发出 `contextPrepared` 消息，告知`SpringBoot` 应用使用的 `ApplicationContext` 已准备OK
15. 将各种 `beans `装载入 `ApplicationContext`，继续由 `SpringApplicationRunListener` 来发出 `contextLoaded `消息，告知 SpringBoot 应用使用的 `ApplicationContext` 已装填OK
16. `refresh ApplicationContext`， **方法有锁**  ，线程安全完成`IOC`容器可用的最后一步(配置类的解析、各种`BeanFactoryPostProcessor`和`BeanPostProcessor`的注册、国际化配置的初始化、`web`内置容器的构造) 
17. 由 `SpringApplicationRunListener` 来发出 `started `消息
18. 完成最终的程序的启动
19. 由 `SpringApplicationRunListener` 来发出 running 消息，告知程序已运行起来了

ApplicationContextInitializer ：应用上下文初始化器

 `ApplicationListener`：监听器

`Environment`：环境

`environmentPrepared` ：环境准备就绪

`ApplicationContext` ：`Spring`容器

`contextPrepared` ：上下文准备就绪

`contextLoaded`  : 上下文加载就绪

`refresh ` :  刷新



``` java
//构造方法
public SpringApplication(ResourceLoader resourceLoader, Class<?>... primarySources) {
        this.sources = new LinkedHashSet();
        this.bannerMode = Mode.CONSOLE;
        this.logStartupInfo = true;
        this.addCommandLineProperties = true;
        this.addConversionService = true;
        this.headless = true;
        this.registerShutdownHook = true;
        this.additionalProfiles = new HashSet();
        this.isCustomEnvironment = false;
        this.resourceLoader = resourceLoader;
        Assert.notNull(primarySources, "PrimarySources must not be null");
        this.primarySources = new LinkedHashSet(Arrays.asList(primarySources));
    	//SERVLET 、REACTIVE 内置web容器  web环境 默认使用SERVLET
    	//加载webApplicationType 对象 推断是web环境 还是非web环境
    	//第一步 
        this.webApplicationType = WebApplicationType.deduceFromClasspath();  
     	// 从spring.factories文件中找出key为ApplicationContextInitializer的类并实例化后设置到SpringApplication的initializers属性中。
    	//这个过程也就是找出所有的应用程序初始化器
    	//2
        this.setInitializers(this.getSpringFactoriesInstances(ApplicationContextInitializer.class));
       	// 从spring.factories文件中找出key为ApplicationListener的类并实例化后设置到SpringApplication的listeners属性中.
    	//这个过程就是找出所有的应用程序事件监听器
   		//监听器
    	//3
    	this.setListeners(this.getSpringFactoriesInstances(ApplicationListener.class));
        //通过堆栈里获取的方式，判断main函数，找到原始启动的main函数
        //4
    	this.mainApplicationClass = this.deduceMainApplicationClass();
    }


 public ConfigurableApplicationContext run(String... args) {
    	 //开启执行时间记录器
        StopWatch stopWatch = new StopWatch();
        stopWatch.start();
        ConfigurableApplicationContext context = null;
        Collection<SpringBootExceptionReporter> exceptionReporters = new ArrayList();
        this.configureHeadlessProperty();
       //根据传递的参数 加载spirng.factories中的SpringApplicationRunListener实例监听对象
        SpringApplicationRunListeners listeners = this.getRunListeners(args);
        listeners.starting();

        Collection exceptionReporters;
        try {
            // 将传入的参数转换为ApplicationArguments格式
            ApplicationArguments applicationArguments = new DefaultApplicationArguments(args);
            ConfigurableEnvironment environment = this.prepareEnvironment(listeners, applicationArguments);
            this.configureIgnoreBeanInfo(environment);
            // 从环境变量中检查和设置banner.mode的模式  OFF时不打印
            // 这部分是sb项目启动时显示几行springboot字符串头像
            //自定义配置可参阅 SpringApplicationBannerPrinter
            Banner printedBanner = this.printBanner(environment);
            //创建应用上下文环境 检查是web环境还是默认环境等生成相对应环境
            context = this.createApplicationContext();
             // 从spring.factories中获取SpringBootExceptionReporter类型的实例 
            exceptionReporters = this.getSpringFactoriesInstances(SpringBootExceptionReporter.class, new Class[]{ConfigurableApplicationContext.class}, context);
            //准备context  
            //  详情看下一段代码
            this.prepareContext(context, environment, listeners, applicationArguments, printedBanner);
             //刷新上下文context  注意根据ServletWeb和ReactiveWeb以及默认的applicationContext的不同来进行具体刷新
            this.refreshContext(context);
             // 刷新后的操作  现在是保留方法
            this.afterRefresh(context, applicationArguments);
              //结束执行时间记录器
            stopWatch.stop();
            // 是否开启启动日志
            if (this.logStartupInfo) {
                (new StartupInfoLogger(this.mainApplicationClass)).logStarted(this.getApplicationLog(), stopWatch);
            }
            // 发布事件  context.publishEvent(ApplicationStartedEvent)
            listeners.started(context);
             // 将ApplicationRunner和CommandLineRunner类型的回调处理
            this.callRunners(context, applicationArguments);
        } catch (Throwable var10) {
            
            this.handleRunFailure(context, var10, exceptionReporters, listeners);
            throw new IllegalStateException(var10);
        }

        try {
            listeners.running(context);
            return context;
        } catch (Throwable var9) {
            this.handleRunFailure(context, var9, exceptionReporters, (SpringApplicationRunListeners)null);
            throw new IllegalStateException(var9);
        }
    }

	//prepareContext
    private void prepareContext(ConfigurableApplicationContext context,
                ConfigurableEnvironment environment, SpringApplicationRunListeners listeners,
                ApplicationArguments applicationArguments, Banner printedBanner) {
           // 设置context环境变量
            context.setEnvironment(environment);
           // 注册internalConfigurationBeanNameGenerator实例  setResourceLoader 或者setClassLoader
            postProcessApplicationContext(context);
            // 执行ApplicationContextInitializer.initialize方法
            applyInitializers(context);
            // 设置监听上下文
            listeners.contextPrepared(context);
            // 如果启动日志开的话 则启动日志实例
            if (this.logStartupInfo) {
                logStartupInfo(context.getParent() == null);
                logStartupProfileInfo(context);
            }
            // Add boot specific singleton beans
            // 通过bean工厂注册springApplicationArguments的单例对象
            context.getBeanFactory().registerSingleton("springApplicationArguments",
                    applicationArguments);
            // 如果 printedBanner 不为空则通过bean工厂注册springBootBanner的单例对象
            if (printedBanner != null) {
                context.getBeanFactory().registerSingleton("springBootBanner", printedBanner);
            }

            // Load the sources  加载sources
            Set<Object> sources = getAllSources();
            Assert.notEmpty(sources, "Sources must not be empty"); 		    
            //通过 createBeanDefinitionLoader方法  获取lBeanDefinitionLoader 并设置beanNameGenerator、environment、resourceLoader
           // 最后根据类型进行装载registerbean 常见的类型有xml ,annotation,package,resouces等等 最后返回bean数量
            load(context, sources.toArray(new Object[0])); 		    
            // 通过SimpleApplicationEventMulticaster的Executor 去invoke是ApplicationListener类型的listener
              // 循环执行listener.onApplicationEvent(event);
            listeners.contextLoaded(context);
        }

```

