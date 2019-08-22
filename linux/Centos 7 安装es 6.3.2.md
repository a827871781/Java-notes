# Centos 7 部署 ES6.3.2 +logstash-input-jdbc +IK分词器

**logstash 和 IK 的版本一定要和 ES的版本一致。**

## ES

### 前提

Java 环境

### 下载

```shell
cd /home/elasticsearch
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.3.2.zip
```

### 解压

```shell
unzip elasticsearch-6.3.2.zip
```

### 配置

ES 不允许 Root。用户登陆。so。我们要创建ES用户

#### 创建 ES 用户

```shell
# 创建ES组
groupadd elasticsearch
# 在ES组下创建ES用户，并设置密码为elasticsearch
useradd elasticsearch -g elasticsearch -p elasticsearch
```

#### ES 配置外网访问及Java服务访问

```shell
cd ../config
vim elasticsearch.yml
#增加如下一行代码 注意yml文件 需要在每一项前面加空格。
 http.host: 0.0.0.0
 http.port: 9200
#Java 访问9300端口 
 network.host: 0.0.0.0
```

#### 更改文件夹属主和属组

```shell
chown -R elasticsearch:elasticsearch elasticsearch-6.3.2/
```

#### 切换ES用户，启服务

```shell
su - elasticsearch
cd elasticsearch-6.3.2/bin
./elasticsearch
## 后台启动服务，如果不是后台启动服务，那么关闭终端 es 服务会停止。
./elasticsearch -d
```



## logstash-input-jdbc 

logstash-input-jdbc 是logstash 的一个插件，所以要先安装logstash

#### logstash 安装

```shell
cd /home/elasticsearch
wget https://artifacts.elastic.co/downloads/logstash/logstash-6.3.2.tar.gz
tar -zxvf logstash-6.3.2.tar.gz
```

#### logstash-input-jdbc 安装

```shell
cd logstash-6.3.2
bin/logstash-plugin install logstash-input-jdbc
```

#### 查看对应的插件版本

```shell
#这个要自己查，不同版本的安装的插件版本可能不同
cd /home/elasticsearch/logstash-6.3.2/vendor/bundle/jruby/2.3.0/gems/logstash-input-jdbc-4.3.9/
```

对应的 jdbc 插件版本是 4.3.9

#### 下载mysql数据库连接包

mysql驱动版本无要求，应该都可以

```shell
cd /home/elasticsearch
wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.45.tar.gz
tar -zxvf mysql-connector-java-5.1.45.tar.gz
```



#### 编写同步的配置文件

```shell
input {
stdin {
}
jdbc {
    #mysql 相关 jdbc 配置  ！！！这里需要修改
    jdbc_connection_string => "jdbc:mysql://x.x.x.x:3306/x?serverTimezone=UTC&zeroDateTimeBehavior=convertToNull"
    #！！！这里需要修改
    jdbc_user => "x"
    #！！！这里需要修改
    jdbc_password => "x"
    #jdbc 连接 mysql 驱动的文件目录，第 3 步下载的文件目录
    jdbc_driver_library => "/home/elasticsearch/mysql-connector-java-5.1.45/mysql-connector-java-5.1.45-bin.jar"
    jdbc_driver_class => "com.mysql.jdbc.Driver"
    jdbc_paging_enabled => "true"
    jdbc_page_size => "50000"
    #mysql 文件，也可以直接写 SQL 语句在此处
    #statement => "SELECT * from * "
    # 去对应的文件位置编写sql代码。就用vim 就可以，千万别用自己电脑写完文件在上传到服务器 这种方式可能会引发编码问题
    statement_filepath => "/home/elasticsearch/jdbc.sql"
    #定时操作，和 crontab 一样
    schedule => "*/2 * * * *"
    type => "item"
    #是否记录上次执行结果，如果为真，将会把上次执行到的 tracking_column 字段的值记录下来，保存到
    last_run_metadata_path => "/home/elasticsearch/logstash-6.3.2/config/last_id"
    record_last_run => "true"
    #是否需要记录某个 column 的值，如果 record_last_run 为真，可以自定义我们需要 track 的 column 名称，此时该参数就要为 true. 否则默认 track 的是 timestamp 的值.
    use_column_value => "true"
    #如果 use_column_value 为真，需配置此参数. track 的数据库 column 名，该 column 必须是递增的。
    
    # 这个就用更新时间 来做增量更新 es 通过判断这个字段变化 来增量更新
    tracking_column => "updateTime"
    #是否清除 last_run_metadata_path 的记录，如果为真那么每次都相当于从头开始查询所有的数据库记录
    clean_run => "false"
    #是否将 字段 (column) 名称转小写
    lowercase_column_names => "false"
   }
}
#此处暂不做过滤处理，如果需要可添加
filter {}
output {
#输出到 elasticsearch 的配置，配置很简单，一看就懂，就不作说明了
elasticsearch {
    hosts => ["127.0.0.1:9200"]
    #！！！这里需要修改
    index => "x"
     # 需要关联的数据库中有有一个id字段，对应索引的id号,这个就是你sql查出来 要有id字段，也可以改，就是你先要那个字段为document_id 那么这里就写那个字段。多个表聚合查询时，可以用N个id 在数据库用concat函数 拼接起来的字段 as id 保证唯一，方便以后做增量更新。
    document_id => "%{id}"
    #！！！这里需要修改
    document_type => "x"
    template_overwrite => true
   }

}
```



#### 启动配置文件

这里有一个点 就是最好用root用户启动 因为这个命令会对磁盘进行写入，会需要权限。最省事的办法就是用root用户。

```shell
cd /home/elasticsearch/logstash-6.3.2/bin/

./logstash -f /home/elasticsearch/logstash-6.3.2/mysql-config/jdbc.conf
```

### 

### 遇到的问题

#### 1.修改elasticsearch.yml ES 启动报错 权限不够

 root 用户下为普通用户授权就可以了
例如我的普通用户名是 elasticsearch

```shell
chown elasticsearch  /home/elasticsearch/elasticsearch-6.3.2 -R
```

#### 2.启动报错max file descriptors [4096] for elasticsearch process is too low, increase to at least [65536]max number of threads [1024] for user [hadoop] is too low, increase to at least [2048]
max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]

切换到 root 用户

vim /etc/security/limits.conf 

添加下面设置 elasticsearch 是用户

```shell
 elasticsearch hard nofile 65536
 elasticsearch soft nofile 65536
 elasticsearch soft    nproc           4096
 elasticsearch hard    nproc           4096
```

vim /etc/sysctl.conf

添加下面配置：

```shell
vm.max_map_count=655360
```

退出用户重新登录并启动elasticsearch 服务

#### 3.SpringBoot 报错：org.elasticsearch.client.transport.NoNodeAvailableException: None of the configured nodes are available

这个问题就是因为没加这行配置

 ```shell
 network.host: 0.0.0.0
 ```



#### 4.Springboot 配置文件中cluster-name的值如何确定

cluster-name: elasticsearch

浏览器直接访问部署es服务的服务器

http://X.X.X.X:9200/

可以看到cluster_name 的属性值

#### 5.LogStash 错误：Logstash could not be started because there is already another instance usin

这个错误是因为反复执行	`./logstash -f /home/elasticsearch/logstash-6.3.2/mysql-config/jdbc.conf`命令，导致加锁。

解决方案：

```shell
cd /home/elasticsearch/logstash-6.3.2/data/
#查看是否存在 .lock 文件，如果存在把它删除
ls -alh
#删除
rm .lock
```

## IK分词器

### 插件安装

```shell
cd /home/elasticsearch/elasticsearch6.3.2
./bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v6.3.2/elasticsearch-analysis-ik-6.3.2.zip
```

### 重启 es

1.  查找 es 进程

```shell
ps -ef | grep elastic
```

2.  终止进程 

```shell
#这里写查出的进程ID
kill -9 XXX
```

3.  启动 es 后台运行

