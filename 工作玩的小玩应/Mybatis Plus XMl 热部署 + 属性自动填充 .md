### Mybatis Plus XMl 热部署 

**MP版本 2.3.3**

**application.yml**：

```yaml
mybatis-plus:
    mapper-locations: classpath:/mapper/*Mapper.xml
    global-config:
        refresh-mapper: true
```

**JavaBean：**

```java
@Configuration
@MapperScan("com.syz.springtransaction.Dao")
public class MybatisPlusConfig {
    
   @Value("${mybatis-plus.mapper-locations}")
   private String mapperLocations;
   @Value("${mybatis-plus.global-config.refresh-mapper}")
   private Boolean refreshMapper;
    
   private static final ResourcePatternResolver resourceResolver = new PathMatchingResourcePatternResolver();

   /**
    * 分页插件
    * @return
    */
   @Bean
   public PaginationInterceptor paginationInterceptor() {
      return new PaginationInterceptor();
   }

   /**
    * MP XML 热部署
    * @param sqlSessionFactory
    * @return
    */
   @Bean
   public MybatisMapperRefresh mybatisMapperRefresh(SqlSessionFactory sqlSessionFactory){
      Resource[] resources = new Resource[0];
      try {
         resources = resourceResolver.getResources(mapperLocations);
      } catch (IOException e) {
         e.printStackTrace();
      }
      return new MybatisMapperRefresh(resources,sqlSessionFactory,10,20,refreshMapper);
   }
}
```

### MP实体类属性自动填充
```java
@Component
public class MyMetaObjectHandler extends MetaObjectHandler {

    /**
     * 测试 user 表 name 字段为空自动填充
     */
    @Override
    public void insertFill(MetaObject metaObject) {
        System.out.println("insert fill");
        // 测试下划线
        Object testType = getFieldValByName("testType", metaObject);
        System.out.println("testType=" + testType);
        if (testType == null) {
            setFieldValByName("updateTime", new Timestamp(System.currentTimeMillis()), metaObject);
            setFieldValByName("createTime", new Timestamp(System.currentTimeMillis()), metaObject);
        }
    }

    @Override
    public void updateFill(MetaObject metaObject) {
        //更新填充
        System.out.println("update fill");
   
        setFieldValByName("updateTime", new Timestamp(System.currentTimeMillis()), metaObject);
    }
}
```

### mybatis plus 

用page  可以分页查询 但是并不能查询出totel  条数

原因：项目中引入的pagehelper 插件  和mybatis plus  冲突  