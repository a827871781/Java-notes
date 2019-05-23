```java
//表明它是一个切面类
@Aspect
@Component
public class HttpAspect {
    //这里就定义了一个总的匹配规则，以后拦截的时候直接拦截log()方法即可，无须去重复写execution表达式
    @Pointcut("execution(* com.example.demo.service.*.*(..))")
    public void log() {}

    @Before("log()")
    public void doBefore() {
        System.out.println("******拦截前的逻辑******");
    }

    @After("log()")
    public void doAfter() {
        System.out.println("******拦截后的逻辑******");
    }
}
//自定义注解
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Component
public @interface TestAnnotation {
    String value() default "";
}


@Autowired
private TestService testService;
@RequestMapping("test")
public void   test(){
      System.out.println("-------------反射方案---");
        Class<?> clz = testService.getClass();
        Method[] methods = clz.getMethods();
        for (Method method : methods) {
            if (method.isAnnotationPresent(TestAnnotation.class)) {
                String uri = method.getAnnotation(TestAnnotation.class).value();
                System.out.println(uri);
            }
        }
        System.out.println("-------------AOP代理后获取注解内容-------------");
        for (Method method : methods) {
            TestAnnotation encrypt = AnnotationUtils.findAnnotation(method, TestAnnotation.class);
            if (encrypt!= null ){
                System.out.println(encrypt.value());
           }
        }
    }

@Service
public class TestService {

    @TestAnnotation("测试注解")
    public  void test(){    }
}

```

测试过程

开启切面类`Component`注解 

结果：

`-------------传统方案-------------
-------------AOP代理后获取注解内容-------------
测试注解`

关闭切面类`Component`注解 

结果：

`-------------传统方案-------------
测试注解
-------------代理后获取注解内容-------------
测试注解`

![](<https://github.com/a827871781/Java-notes/images/11.png \>)

解决方案：

1. 可以自己截取将多余部分截取掉
2. Spring里面提供的`AnnotationUtils`来读取注解。
