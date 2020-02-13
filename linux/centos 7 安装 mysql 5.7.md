# 1.卸载全部 MariaDB 相关

从 CentOS 7 系统开始，MariaDB 成为 yum 源中默认的数据库安装包。在 CentOS 7 及以上的系统中使用 yum 安装 MySQL 包将无法使用 MySQL。您可以选择使用完全兼容的 MariaDB，或依照本文介绍配置来继续使用 MySQL。

```shell
yum -y remove mariadb
```

# 2.下载 MySQL 的 YUM 源

```shell
#进入到要下载到的路径：
cd /usr/local/src
#下载：
wget https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm

```

# 3.安装 MySQL 的 YUM 源

```shell
rpm -ivh mysql57-community-release-el7-11.noarch.rpm
```

# 4.检查 MySQL 的 YUM 源是否安装成功

```shell
yum repolist enabled | grep "mysql.*-community.*"
```

![722c38d8-d3af-11e9-ab82-acde48001122](https://i.loli.net/2019/09/10/S5LA7vKXDyfVh3I.png )

如图所示则安装成功。

# 5.查看 MySQL 版本

```shell
yum repolist all | grep mysql
```

![c7901cd6-d3af-11e9-85b5-acde48001122](https://i.loli.net/2019/09/10/HfDT16hiqXnutwj.png )

# 6.安装 MySQL

```shell
yum -y install mysql-community-server
```



# 7.测试连接 MySQL 服务

```shell
#先启动MySQL服务
systemctl start mysqld

#连接MySQL
mysql -u root 或者 mysql
-------------------------------------------------------
提示:

刚安装的 MySQL 会随机生成密码
在 /var/log/mysqld.log 这个文件的前几行即可找到



#修改密码：
set password=password("xxxxxx");

#刷新：
flush privileges;

#退出：
exit;

设置完之后，输入 mysql -u root -p，这时输入刚设置的密码，就可以登进数据库了。


```

# 8.防火墙设置

将 MySQL 服务加入防火墙，然后重启防火墙：

```shell
#打开防火墙
systemctl start firewalld

# MySQL 服务加入防火墙
firewall-cmd --zone=public --permanent --add-service=mysql
systemctl restart firewalld

```

# 9.设置允许远程访问

```shell
#登陆mysql
mysql -u root -p
#修改 Mysql-Server 用户配置
USE mysql;

#授权
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '你的密码' WITH GRANT OPTION;

flush privileges;

--------------------------------------------------------------------
在执行第一条命令的时候，可能会报：

'ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.' 需要让我们重置密码。
这时候就参看第七步的修改密码即可
```

ps:云服务器 记得将3306端口加入安全组

# 10.常用命令

## 启动

```shell
systemctl start mysqld 
```

## 停止

```shell
systemctl stop mysqld 
```



## 重启

```shell
systemctl restart mysqld 
```

##查看MySQL当前运行状态

```shell
systemctl status mysqld 
```





