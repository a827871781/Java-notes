### SpringCloud 工作中遇到的问题

#### feign 服务调用时默认传输格式为xml  

解决方案消费者 requestMapping 注解 配置属性

  @RequestMapping(value="X",produces = { "application/json;charset=UTF-8" }) 

或者引入feign-jackson依赖

因为引入了jackson-dataformat-xml这个依赖，它是提供了jackson将实体类转化为xml相关的作用。而本身jackson是可以将实体类转化为json的，所以这样Jackson是可以将实体类转化为两种类型的数据，而具体要转化为哪一种数据，是要看http请求里面的accept头信息的，我的浏览器chrome的accept是 Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8 ，然后服务器会根据accept来决定是返回xml还是json，由于浏览器accept只有最后的*/*是匹配 application/json的，而application/xml在*/*前面，优先级比json高，所以用浏览器直接调用是会优先返回xml格式的。



feign调用服务时如果要上传图片 需要引入两个jar包，并建立配置对象

但是这样引发另一个问题feign调用时如果返回是对象内还有对象的组合方式 那么不能讲属性映射到对象内对象 

```java
<!--  feign 模拟表单提交       -->
<dependency>
    <groupId>io.github.openfeign.form</groupId>
    <artifactId>feign-form</artifactId>
    <version>3.0.3</version>
</dependency>
<dependency>
    <groupId>io.github.openfeign.form</groupId>
    <artifactId>feign-form-spring</artifactId>
    <version>3.0.3</version>
</dependency>

/**

- 引用配置类MultipartSupportConfig.并且实例化
  */
  class MultipartSupportConfig {
  @Bean
  public Encoder feignFormEncoder() {
      return new SpringFormEncoder();
  }
  }

```



#### feign参数限制：

1.  当参数比较复杂时，feign即使声明为get请求也会强行使用post请求

2.  不支持@GetMapping类似注解声明请求，需使用@RequestMapping(value = "x",method = RequestMethod.GET)

3.  使用@RequestParam注解时必须要在后面加上参数名

4.  多参数的 URL 也可以使用 Map 去构建(不建议，语义不清晰)

5.  post 传递对象时，可以` @PostMapping(value = "x",,consumes = "application/json")`

   或 `@PostMapping(value="x")
   List<x>getA11(@RequestBody X x);`



#### 心跳配置开发环境中配置

eureka.instance.lease-renewal-interval-in-seconds   =15 eureka.instance.lease-expiration-duration-in-seconds =5 

每15S发送一次心跳，超过5S没有收到心跳，则下线。导致前后端联调时服务经常会404

解决方案：

eureka.instance.lease-renewal-interval-in-seconds   =30 eureka.instance.lease-expiration-duration-in-seconds =60 

30S一次心跳，60S每心跳下线，容错一次。





#### mybatis plus 

用page  可以分页查询 但是并不能查询出totel  条数

原因：项目中引入的pagehelper 插件  和mybatis plus  冲突  



#### Springcloud 2.0 restTemplate  

装配RestTemplate

 配置忽略ssl

 配置添加请求头

在@Bean 注入RestTemplate时  如果要调用的是SpringCloud 实例上的请求 

那么就要@LoadBalanced   注解开启均衡负载能⼒。

  **//@LoadBalanced  开启SpringCloud Rest   Http寻找的是eureka实例**

```java
import lombok.extern.slf4j.Slf4j;
import org.apache.http.conn.ssl.NoopHostnameVerifier;
import org.apache.http.conn.ssl.SSLConnectionSocketFactory;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.ssl.SSLContexts;
import org.apache.http.ssl.TrustStrategy;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpRequest;
import org.springframework.http.client.ClientHttpRequestExecution;
import org.springframework.http.client.ClientHttpRequestInterceptor;
import org.springframework.http.client.ClientHttpResponse;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import javax.net.ssl.SSLContext;
import java.io.IOException;
import java.security.KeyManagementException;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.util.Collections;

/**
 * 装配RestTemplate
 * 配置忽略ssl
 * 配置添加请求头
 * @author syz
 * @version 1.0
 * @create 2019-04-15 17:37
 **/
@Slf4j
@Configuration
public class RestTemplateConfig {

    @Autowired
    ActionTrackInterceptor actionTrackInterceptor ;

    /**
     * 忽略ssl
     * @return
     * @throws NoSuchAlgorithmException
     * @throws KeyManagementException
     * @throws KeyStoreException
     */
    @Bean
    public HttpComponentsClientHttpRequestFactory httpComponentsClientHttpRequestFactory()
            throws NoSuchAlgorithmException, KeyManagementException, KeyStoreException{
        TrustStrategy acceptingTrustStrategy = (x509Certificates, authType) -> true;
        SSLContext sslContext = SSLContexts.custom().loadTrustMaterial(null, acceptingTrustStrategy).build();
        SSLConnectionSocketFactory connectionSocketFactory = new SSLConnectionSocketFactory(sslContext, new NoopHostnameVerifier());
        HttpClientBuilder httpClientBuilder = HttpClients.custom();
        httpClientBuilder.setSSLSocketFactory(connectionSocketFactory);
        CloseableHttpClient httpClient = httpClientBuilder.build();
        HttpComponentsClientHttpRequestFactory factory = new HttpComponentsClientHttpRequestFactory();
        factory.setHttpClient(httpClient);
        return factory;
    }

    /**
     * 注入 RestTemplate 并忽略安全证书ssl
     * 并添加head请求头
     * @return RestTemplate
     */
    //@LoadBalanced  开启SpringCloud Rest   Http寻找的是eureka实例
    @Bean
    public RestTemplate restTemplate(HttpComponentsClientHttpRequestFactory factory){
        RestTemplate restTemplate = new RestTemplate(factory);
        restTemplate.setInterceptors(Collections.singletonList(actionTrackInterceptor));
        return restTemplate ;
    }

    /**
     * 添加请求头
     * @author syz
     * @date 2019/4/15 0015
     */
    @Component
     class ActionTrackInterceptor implements ClientHttpRequestInterceptor {
        @Value("${token.code}")
        private String tokenCode;

        @Override
        public ClientHttpResponse intercept(HttpRequest request, byte[] body, ClientHttpRequestExecution execution)
                throws IOException {
            HttpHeaders headers = request.getHeaders();
            // 加入自定义字段
            headers.add("code", tokenCode);
            // 保证请求继续被执行
            return execution.execute(request, body);
        }
    }
}

```



