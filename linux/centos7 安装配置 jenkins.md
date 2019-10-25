## 安装jenkins

### 写在最初:

为什么不用docker安装jenkins,是因为,坑很多.权限可能会有问题,以及与其他工具交互时可能会因为容器引发问题.

不要问我为什么知道,问就是,错过.

### 前置要求:

#### JDK

由于使用 java 写成，所以运行 jenkins 需要有 java 环境，所以我们需要在机器上安装 java, 通过

```shell
#查看java版本
java -version 
```

如果没有,可以参考[centos7安装java8](https://github.com/a827871781/Java-notes/blob/master/linux/centos7安装Java8.md)

#### mavn

```shell
cd /usr/local/maven3
wget http://mirror.bit.edu.cn/apache/maven/maven-3/3.6.1/binaries/apache-maven-3.6.1-bin.tar.gz
tar vxf apache-maven-3.6.1-bin.tar.gz
```

##### 修改环境变量

在 /etc/profile （也有可能是在～/.bash_profile）中添加以下几行

```shell
# Maven配置
export MAVEN_HOME=/usr/local/maven3/apache-maven-3.6.1
export MAVEN_HOME
export PATH=$PATH:$MAVEN_HOME/bin
```

##### 执行 source /etc/profile 使环境变量生效。

##### 运行 mvn -v 验证 maven 是否安装成功

### 安装 Jenkins

http://mirrors.jenkins.io/war/?C=M;O=D

在这个网站找自己想下载的版本,单击下载即可

![1183d4dc-f600-11e9-b53d-acde48001122](https://i.loli.net/2019/10/24/SOKsZA2JmcTI3iF.png )

### 创建jenkins_home 文件夹并将文件上传至jenkins_home文件夹

```shell
cd /home 
mkdir jenkins_home
```

### 启动jenkins

```shell
#默认启动在 8080
java -jar jenkins.war 

#启动在指定端口
java -jar jenkins.war --httpPort=8080

#后台启动jenkins
nohup java -jar jenkins.war --httpPort=8080&

#关闭jenkins
pkill -f jenkins.war
```

**第一次启动jenkins 最好不要使用后台启动,因为jenkins 在第一次启动时会在控制台打印一个随机的密钥,这个是用来登陆的.如果是后台 你还需要去找日志文件**

![b7c0070c-f601-11e9-b85f-acde48001122](https://i.loli.net/2019/10/24/GegCpkxUfq4hSJZ.png )

将打印出来的密钥复制

### 访问Jenkis

ip + 端口

如果没指定端口 那就是8080端口

粘贴在这个输入框内

![2fb43dfa-f602-11e9-bb8e-acde48001122](https://i.loli.net/2019/10/24/SM28CwaY7teKTHy.png )

### 配置jenkins

直接安装推荐的插件即可

![7c2e0ef4-f602-11e9-b3ba-acde48001122](https://i.loli.net/2019/10/24/4CHFR7W3IKdB2uX.png )

#### 创建第一个管理员用户

## 配置 Git、JDK、Maven

进入【**系统管理 -> 全局工具配置**】：

### JDK

我这里是yum安装的jdk,所以这样配置,如果自己配置的jdk 就将javahome路径写上即可

 ![36043818-f61b-11e9-abb7-acde48001122](https://i.loli.net/2019/10/24/JKZSHdlPe6o3Vc8.png )

### Git

如果以安装git,就用`whereis git` 命令找到git安装目录

如果未安装,那么就yum安装 ,`/usr/local/git/bin/git` 就是git的默认安装路径

![faaea112-f620-11e9-98b5-acde48001122](https://i.loli.net/2019/10/24/9nKZUf1FcBPOoVu.png )

![db6d0334-f620-11e9-ad56-acde48001122](https://i.loli.net/2019/10/24/rKbdS1IxaCJU4Mw.png )

### maven

![image-20191024130312984](/Users/syz/Library/Application Support/typora-user-images/image-20191024130312984.png)

#### 登陆 jenkins 的后台管理: Manage Jenkins -> Global Tool Configuration 选择自己的配置文件

![](https://i.loli.net/2019/10/25/jhFXAyt5ZScJNY2.png)



#### 修改 Maven 下载依赖路径

 Manage Jenkins -> Configure System -> Maven 项目配置 ->  全局 MAVEN_OPTS 输入 -Dmaven.repo.local=/opt/mvnRepository 

eg: /opt/mvnRepository  是我的仓库路径



![](https://i.loli.net/2019/10/25/tcHfJl9kEMrVXeS.png)

## 配置jenkins插件

【**系统管理 -> 插件管理 -> 可选插件**】，搜索并安装以下插件：

1. `SSH` 插件 —— 用于 SSH 登录远程主机拉取代码或者部署服务；
2. `Publish Over SSH` 插件 —— 用于将项目部署到远程机器上（SSH 登录然后执行部署脚本）；
3. `Maven Integration` 插件 —— 用于创建一个 Maven 的构建项目；
4. `GitLab` 插件  —— 用于当 gitlab 有 push 时触发 jenkins 拉取代码和将构建状态发送回 GitLab
5. `Gitlab Hook` 插件—— 用于 gitlab 有 push 时触发 jenkins

## 全局安全配置

系统管理”->” 全局安全配置”
**关闭**防止跨站点请求伪造，原因如下:

`webhooks 与 jenkins 配合使用时提示：HTTPStatus403-Novalidcrumbwasincludedintherequest, 这是因为 jenkins 在 http 请求头部中放置了一个名为.crumb 的 token。在使用了反向代理，并且在 jenkins 设置中勾选了 “防止跨站点请求伪造（Prevent Cross Site Request Forgery exploits）” 之后此 token 会被转发服务器 apache/nginx 认为是不合法头部而去掉。导致跳转失败。`

## jenkins 配置插件下载速度慢,配置镜像

https://blog.csdn.net/you227/article/details/81076032
