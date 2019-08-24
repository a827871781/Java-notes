# SpringBoot2.X 配置跨域

## 1、配置 过滤器

```java
@Configuration
public class GlobalCorsConfig {
    @Bean
    public CorsFilter corsFilter() {
        CorsConfiguration config = new CorsConfiguration();
          config.addAllowedOrigin("*");
          config.setAllowCredentials(true);
          config.addAllowedMethod("*");
          config.addAllowedHeader("*");
          config.addExposedHeader("*");

        UrlBasedCorsConfigurationSource configSource = new UrlBasedCorsConfigurationSource();
        configSource.registerCorsConfiguration("/**", config);

        return new CorsFilter(configSource);
    }
}

```

## 2、配置拦截器

```java
@Configuration
public class MyConfiguration extends WebMvcConfigurerAdapter  {

    @Override  
    public void addCorsMappings(CorsRegistry registry) {  
        registry.addMapping("/**")  
                .allowCredentials(true)  
                .allowedHeaders("*")  
                .allowedOrigins("*")  
                .allowedMethods("*");  

    }  
}

```

## 3、 单个请求的跨域通过 @CrossOrigin 注解来实现

```java
@RequestMapping("/hello")
@CrossOrigin("http://localhost:8080") 
public String hello( ){
return "Hello World";
}
```

