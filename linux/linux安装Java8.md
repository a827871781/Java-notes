# 1.下载

https://www.oracle.com/java/technologies/jdk8-downloads.html

下载文件名为:jdk-8u221-linux-x64.tar.gz的文件

# 2.解压

```shell
#先创建 java 文件目录，如果已存在就不用创建
mkdir -p /usr/local/java
cd /usr/local/java
#将文件放到当前文件夹下
#解压
tar -vzxf jdk-8u221-linux-x64.tar.gz  
```

# 3.添加环境变量，编辑配置文件

```shell
vi /etc/profile

#这里jdk的版本号可能有区别,注意修改
export JAVA_HOME=/usr/local/java/jdk1.8.0_221
export CLASSPATH=$:CLASSPATH:$JAVA_HOME/lib/
export PATH=$PATH:$JAVA_HOME/bin


#重新加载配置文件
source /etc/profile
```

# 4.测试结果

```shell
java -version


#结果
java version “1.8.0_161”
Java™ SE Runtime Environment (build 1.8.0_161-b12)
Java HotSpot™ 64-Bit Server VM (build 25.161-b12, mixed mode)
```

