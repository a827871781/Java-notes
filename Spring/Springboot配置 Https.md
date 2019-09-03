## 购买或本地生成 ssl 证书

要使用 https，首先需要 ssl 证书，获取 SSL 证书有两种方式：

-   自己通过 keytool 生成
-   通过证书授权机构购买

### keytool 生成：

```shell
#Mac OS  生成在~/ 文件夹内  tomcat.keystore 文件名
keytool -genkey -alias tomcat -keyalg RSA -keystore ~/tomcat.keystore
```

## Springboot 配置 SSl

tomcat.keystore 文件放到代码resources 文件夹下

### application.properties 配置

```properties
server.port=443
# tomcat.keystore 要放到resources 目录下
server.ssl.key-store=classpath:tomcat.keystore
server.ssl.key-password=123456
server.ssl.key-store-type=JKS
server.ssl.key-alias=tomcat
```



### 设置 http 自动重定向到 https

```java
@Configuration
public class HttpsConfig {

    @Bean
    public Connector connector(){
        Connector connector=new Connector("org.apache.coyote.http11.Http11NioProtocol");
        connector.setScheme("http");
        connector.setPort(9080);
        connector.setSecure(false);
        connector.setRedirectPort(443);
        return connector;
    }

    @Bean
    public TomcatServletWebServerFactory tomcatServletWebServerFactory(Connector connector){
        TomcatServletWebServerFactory tomcat=new TomcatServletWebServerFactory(){
            @Override
            protected void postProcessContext(Context context) {
                SecurityConstraint securityConstraint=new SecurityConstraint();
                securityConstraint.setUserConstraint("CONFIDENTIAL");
                SecurityCollection collection=new SecurityCollection();
                collection.addPattern("/*");
                securityConstraint.addCollection(collection);
                context.addConstraint(securityConstraint);
            }
        };
        tomcat.addAdditionalTomcatConnectors(connector);
        return tomcat;
    }
}
```

#### 现在的状态是：

 http  访问9080 端口 都会被 自动重定向到 https

 https 访问 443 还是https



