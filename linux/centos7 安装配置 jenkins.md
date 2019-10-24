## 安装jenkins

### 前置要求:

由于使用 java 写成，所以运行 jenkins 需要有 java 环境，所以我们需要在机器上安装 java, 通过

```shell
#查看java版本
java -version 
```

如果没有,可以参考[centos7安装java8](https://github.com/a827871781/Java-notes/blob/master/linux/linux安装Java8.md)

#### 在 home 目录创建 jenkins_home 文件夹

```shell
cd /home
mkdir jenkins_home
```

### 把 jenkins_home 文件夹给 jenkins 用户操作权限

```shell
 sudo chown -R 1000 /home/jenkins_home
```

### 启动 jenkins Docker 在 8088 端口 

```shell
sudo docker run -p 8088:8080 -p 50000:50000 -v /home/jenkins_home:/var/jenkins_home jenkins -e JAVA_OPTS=-Duser.timezone=Asia/Shanghai
```

这里因为没有后台启动,所以 在启动后会将初始 密码 打印在终端内.可以直接复制

也可以通过如下命令:

```shell
cat /home/jenkins_home/secrets/initialAdminPassword
#没试过,我用的第一种
```

#### 选择安装推荐的插件

![](https://i.loli.net/2019/10/22/sfLwPcZ3lIVUHTr.png)

#### 创建第一个管理员用户



## 配置 Git、JDK、Maven

进入【**系统管理 -> 全局工具配置**】：

 使用自动安装 依次配置 以上三个工具

JDK  需要Oracle 账号

jenkinsci/blueocean 镜像 自带git  .

## 配置jenkins插件

【**系统管理 -> 插件管理 -> 可选插件**】，搜索并安装以下插件：

1.  `SSH` 插件 —— 用于 SSH 登录远程主机拉取代码或者部署服务；
2.  `Publish Over SSH` 插件 —— 用于将项目部署到远程机器上（SSH 登录然后执行部署脚本）；
3.  `Maven Integration` 插件 —— 用于创建一个 Maven 的构建项目；
4.  `GitLab` 插件  —— 用于当 gitlab 有 push 时触发 jenkins 拉取代码和将构建状态发送回 GitLab
5.  `Gitlab Hook` 插件—— 用于 gitlab 有 push 时触发 jenkins

## 全局安全配置

系统管理”->” 全局安全配置”
**关闭**防止跨站点请求伪造，原因如下:

`webhooks 与 jenkins 配合使用时提示：HTTPStatus403-Novalidcrumbwasincludedintherequest, 这是因为 jenkins 在 http 请求头部中放置了一个名为.crumb 的 token。在使用了反向代理，并且在 jenkins 设置中勾选了 “防止跨站点请求伪造（Prevent Cross Site Request Forgery exploits）” 之后此 token 会被转发服务器 apache/nginx 认为是不合法头部而去掉。导致跳转失败。`

## Jenkins  配置 ssh key 从 gitlab 拉取代码

### 进入容器生成 ssh key

```shell
docker exec -it <jenkins容器id> /bin/bash
#容器内
mkdir ~/.ssh
cd ~/.ssh
#输入完以下命令后  一直回车 即可
ssh-keygen
# 输出公钥
cat id_rsa.pub
#记录下来
```



## 创建测试工程

### 新建一个 Jenkins 的 Maven 项目任务：

![d9bb80ea-f55f-11e9-ac07-acde48001122](https://i.loli.net/2019/10/23/Cr84XUtwobW7kuG.png )





### 源码管理配置

![f1d82452-f560-11e9-a1ab-acde48001122](https://i.loli.net/2019/10/23/YjlSi6OIQTqXcx8.png )

出现以上报错:

就单击蓝色框旁边的 **添加**

![17908932-f561-11e9-8637-acde48001122](https://i.loli.net/2019/10/23/Nn8ChpRTxXSwqv1.png )

id和描述 自己看着来,   用户名 和 密码 就是gitlab 已有的账号  或者 给 jenkins 分配一个账号

###  构建触发器

选择`Build when a change is pushed to GitLab. GitLab webhook URL:`项

并复制url 后面的路径

![17cda462-f565-11e9-b87e-acde48001122](https://i.loli.net/2019/10/23/JE4mtIgYOHxqCur.png )

单击高级按钮,再单击generate 按钮 生成密钥,复制到gitlab 配置

![0628f440-f566-11e9-8e54-acde48001122](https://i.loli.net/2019/10/23/K1qFAsbmHdZcIJB.png )



#### 在 gitlab 的项目里 设置 > 集成

![bf996db0-f566-11e9-8953-acde48001122](https://i.loli.net/2019/10/23/EnzsD3MPQlNYqWp.png )



### Build配置项

配置 Maven 打包指令， `clean package -Dmaven.test.skip=true` （根据项目使用的 Maven Build 插件来定,）：

注意这里没有 mvn，因为他是默认使用 maven 编译的！完整的命令是：

```shell
mvn clean package -Dmaven.test.skip=true
```

其中：-Dmaven.test.skip=true 是跳过测试。



![4ffdb53c-f562-11e9-a15e-acde48001122](https://i.loli.net/2019/10/23/4UbXdu9TaelHcqZ.png )





## jenkins 配置插件下载速度慢,配置镜像

https://blog.csdn.net/you227/article/details/81076032

## jenkins 配置中文

https://blog.csdn.net/u013053075/article/details/101770152









