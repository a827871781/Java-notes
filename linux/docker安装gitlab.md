### 下载 Gitlab 的 Docker 镜像

```shell
docker pull gitlab/gitlab-ce
```

### 运行如下命令来启动 Gitlab

```shell
docker run --detach \
  --publish 10443:443 --publish 1080:80 --publish 1022:22 \
  --name gitlab \
  --restart always \
  --volume /mydata/gitlab/config:/etc/gitlab \
  --volume /mydata/gitlab/logs:/var/log/gitlab \
  --volume /mydata/gitlab/data:/var/opt/gitlab \
  gitlab/gitlab-ce:latest
  
  #  --volume /mydata/gitlab/config:/etc/gitlab \
 # --volume /mydata/gitlab/logs:/var/log/gitlab \
  #--volume /mydata/gitlab/data:/var/opt/gitlab \
  这三行说的是将镜像配置文件挂在到宿主文件内,,前宿主 后镜像
```

### 开启防火墙的指定端口

```shell
# 开启1080端口
firewall-cmd --zone=public --add-port=1080/tcp --permanent 
# 重启防火墙才能生效
systemctl restart firewalld
# 查看已经开放的端口
firewall-cmd --list-ports

#ps : 可以在开启后关闭防火墙.这块具体需要开启端口,不太确定,我是先开启,启动gitlab 后 关闭防火墙,没有影响到后续的启动
```

### 访问 Gitlab

-   访问地址：http://服务器ip:1080/

-   由于 Gitlab 启动比较慢，所以在没有启动完成访问 Gitlab ，会出现如下错误。需要耐心等待 10 分钟左右，

![img](http://macro-oss.oss-cn-shenzhen.aliyuncs.com/mall/blog/gitlab_screen_04.png)

### 配置Gitlab

#### QQ邮箱:

```shell
vim /mydata/gitlab/config/gitlab.rb
```

```properties
#修改如下配置
gitlab_rails['smtp_enable'] = true
gitlab_rails['smtp_address'] = "smtp.exmail.qq.com"
gitlab_rails['smtp_port'] = 465
gitlab_rails['smtp_user_name'] = "你的qq邮箱"
gitlab_rails['smtp_password'] = "你的M密码"
gitlab_rails['smtp_authentication'] = "login"
gitlab_rails['smtp_enable_starttls_auto'] = true
gitlab_rails['smtp_tls'] = true
gitlab_rails['gitlab_email_from'] = '你的qq邮箱'
```

#### 配置 gitlab 服务器的访问地址:

```shell
vim /mydata/gitlab/config/gitlab.rb
```

```properties
# 配置http协议所使用的访问地址
external_url 'http://你的gitlabe服务器ip:1080'

# 修改 nginx['listen_port'] 配置 将  nil  改为 80 
nginx['listen_port'] = 80
```

### 重新加载配置

```shell
docker exec gitlab gitlab-ctl reconfigure
#查看容器id
docker ps 
docker restart Gitlab容器ID
```

### 一点建议

如果搭建Gitlab  只是为了个人玩,那么配置无所谓.如果是公司用,那么一定要用一个可用内存高( 4G+ )的服务器,这会避免很多莫名的问题.

如果一直502报错,可以去看看配置文件是否有多余的配置.或者修改错了的配置.

如果配置没问题,可以参考https://blog.csdn.net/snowglede/article/details/74911101解决问题.

