# 1.卸载全部 MariaDB 相关

从 CentOS 7 系统开始，MariaDB 成为 yum 源中默认的数据库安装包。在 CentOS 7 及以上的系统中使用 yum 安装 MySQL 包将无法使用 MySQL。您可以选择使用完全兼容的 MariaDB，或依照本文介绍配置来继续使用 MySQL。

```shell
yum -y remove mariadb*
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
yum install mysql-community-server

#一直输 y 就可以了。
```

# 7.启动 MySQL 服务

```shell
systemctl start mysqld
```

# 8.测试连接 MySQL 服务

```shell
mysql -u root 或者 mysql
--------------------------------------------------------------------------------

提示:

刚安装的 MySQL 是没有密码的，这时如果出现：

ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: NO)，解决如下：

① 停止 MySQL 服务：systemctl stop mysqld 

② 以不检查权限的方式启动 MySQL: mysqld --user=root --skip-grant-tables &

③ 再次输入 mysql -u root 或者 mysql，这次就可以进来了。

④ 更新密码：

MySQL 5.7 版本：UPDATE mysql.user SET authentication_string=PASSWORD('123456') where USER='root';

⑤ 刷新：flush privileges;

⑥ 退出：exit;

设置完之后，输入 mysql -u root -p，这时输入刚设置的密码，就可以登进数据库了。

--------------------------------------------------------------------------------
```

# 9.防火墙设置

将 MySQL 服务加入防火墙，然后重启防火墙：

```shell
#打开防火墙
systemctl start firewalld

# MySQL 服务加入防火墙
firewall-cmd --zone=public --permanent --add-service=mysql
systemctl restart firewalld

```

# 10.设置允许远程访问

```shell
#登陆mysql
mysql -u root -p
#修改 Mysql-Server 用户配置
USE mysql;

GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '你的密码' WITH GRANT OPTION;
flush privileges;

--------------------------------------------------------------------
在执行第一条命令的时候，可能会报：

'ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.' 需要让我们重置密码。

alter user 'root'@'localhost' identified by '你的密码';  
flush privileges;
```

# 11.启动/停止/重启

## 启动方式

-   使用 service 启动：service mysqld start
-   使用 mysqld 脚本启动：/etc/inint.d/mysqld start
-   使用 safe_mysqld 启动：safe_mysqld&

## 停止

-   使用 service 启动：service mysqld stop
-   使用 mysqld 脚本启动：/etc/inint.d/mysqld stop
-    mysqladmin shutdown 

## 重启

-   使用 service 启动：service mysqld restart
-   使用 mysqld 脚本启动：/etc/inint.d/mysqld restart
    提问 编辑摘要