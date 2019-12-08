### 使用客户端调用 es 服务的方式

#### Springboot Data 提供的 Elasticsearch Repositories

使用TransportClient通过9300 端口通信

作为一个外部访问者，请求 ES 的集群，对于集群而言，它是一个外部因素,会导致一个问题 就是Es 如果升级的话,代码迁移 会很麻烦.

并且Es 官网,不建议用该方式,计划在 7 中删除 TransportClient 客户端，并在 8 中完全删除它。

#### REST

#####  Java 低级别 REST 客户端（Java Low Level REST Client）

Elasticsearch 的官方 low-level 客户端。 它允许通过 http 与 Elasticsearch 集群进行通信。 不会对请求进行编码和响应解码。 **它与所有 Elasticsearch 版本兼容**。

#####  Java 高级 REST 客户端（Java High Level REST Client）

Elasticsearch 的官方 high-level 客户端。 基于 low-level 客户端，它公开了 API 特定的方法，并负责处理。内部仍然是基于低级客户端。它提供了更多的 API，接受请求对象作为参数并返回响应对象，由客户端自己处理编码和解码。每个 API 都可以同步或异步调用。 同步方法返回一个响应对象，而异步方法的名称以 async 后缀结尾，需要一个监听器参数，一旦收到响应或错误，就会被通知（由低级客户端管理的线程池）。高级客户端依赖于 Elasticsearch core 项目。 它接受与 TransportClient 相同的请求参数并返回相同的响应对象。**但 不完善**

### 在这里 我选择的是 Java 高级 REST 客户端 ,原因是:

1.  我的项目已经开始了,代码已经开发完了,用的Elasticsearch Repositories 写的代码,改成 Java 高级 REST 客户端 的代码  改动量相对低了很多.
2.  API 虽然 不完善,但是友好,易上手,
3.  高级么...就选咯.

### Springboot 基础 Java High Level REST Client + x-pack

#### POM文件

```xml

	<properties>
		<java.version>1.8</java.version>
        <!--这里注意自己es 的版本 -->
		<elasticsearch.version>6.3.2</elasticsearch.version>
	</properties>
<!--这注意 必须要有. -->
	<repositories>
		<repository>
			<id>elasticsearch-releases</id>
			<url>https://artifacts.elastic.co/maven</url>
			<releases>
				<enabled>true</enabled>
			</releases>
			<snapshots>
				<enabled>false</enabled>
			</snapshots>
		</repository>
	</repositories>


	<!--elasticsearch base-->
		<dependency>
			<groupId>org.elasticsearch</groupId>
			<artifactId>elasticsearch</artifactId>
			<version>${elasticsearch.version}</version>
		</dependency>
		<dependency>
			<groupId>org.elasticsearch.client</groupId>
			<artifactId>elasticsearch-rest-client</artifactId>
			<version>${elasticsearch.version}</version>
		</dependency>
		<dependency>
			<groupId>org.elasticsearch.client</groupId>
			<artifactId>elasticsearch-rest-high-level-client</artifactId>
			<version>${elasticsearch.version}</version>
		</dependency>
```

#### 增加配置类

```java
@Configuration
public class EsConfiguration {
 

   @Bean
   public RestHighLevelClient client() {
      /** 用户认证对象 */
      CredentialsProvider credentialsProvider = new BasicCredentialsProvider();
      /** 设置账号密码 */
      credentialsProvider.setCredentials(AuthScope.ANY,
            new UsernamePasswordCredentials("elastic", "x-pack密码"));
      /** 创建rest client对象 */
      RestClientBuilder builder = RestClient.builder(new HttpHost("es地址", 9200))
            .setHttpClientConfigCallback(httpClientBuilder -> httpClientBuilder.setDefaultCredentialsProvider(credentialsProvider));
      RestHighLevelClient client = new RestHighLevelClient(builder);
      return client;
   }
 
}
```

#### API

https://www.elastic.co/guide/en/elasticsearch/client/java-rest/6.3/java-rest-high-supported-apis.html