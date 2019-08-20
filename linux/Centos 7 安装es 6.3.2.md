# Centos 7 部署 es6.3.2

# 前提

Java 环境

## 下载

```shell
cd /home/elasticsearch
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.3.2.zip
```

## 解压

```shell
unzip elasticsearch-6.3.2.zip
```

## 配置

Es 不允许 Root。用户登陆。so。我们要创建es用户

### 创建 es 用户

```shell
# 创建es组
groupadd elasticsearch
# 在es组下创建es用户，并设置密码为elasticsearch
useradd elasticsearch -g elasticsearch -p elasticsearch
```

### 更改文件夹属主和属组
```shell
chown -R elasticsearch:elasticsearch elasticsearch-6.3.2/
```

### 切换es用户，启服务

```shell
su - elasticsearch
cd elasticsearch-6.3.2/bin
./elasticsearch
```

