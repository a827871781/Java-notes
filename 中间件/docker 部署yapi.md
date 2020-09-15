# 部署

## 1、准备

```shell
cd /opt
mkdir yapi && cd yapi
mkdir mongo

echo '{
  "port": "3000",
  "adminAccount": "admin@admin.com",
  "timeout":120000,
  "db": {
    "servername": "127.0.0.1",
    "DATABASE": "yapi",
    "port": 27017,
    "user": "test1",
    "pass": "test1",
    "authSource": ""
  },
  "mail": {
    "enable": true,
    "host": "smtp.163.com",
    "port": 465,
    "from": "***@163.com",
    "auth": {
      "user": "***@163.com",
      "pass": "*****"
    }
  }
}' > config.json


```



## 2、启动 MongoDB

```shell
docker run -d --name mongo-yapi  -p 27017:27017  -v /opt/yapi/mongo:/data/db  mongo
```

## 3、获取 Yapi 镜像

```shell
docker pull registry.cn-hangzhou.aliyuncs.com/anoy/yapi/opt/yapi/mongo:/data/db  mongo
```

## 4、初始化 Yapi 数据库索引及管理员账号

```shell
docker run  -it --rm \
  --link mongo-yapi:mongo \
  --entrypoint npm \
  --workdir /api/vendors \
  registry.cn-hangzhou.aliyuncs.com/anoy/yapi \
  run install-server \
  -v /opt/yapi/config.json:/api/config.json
```

## 5、启动 Yapi 服务

```shell
docker run -d \
  --name yapi \
  --link mongo-yapi:mongo \
  --workdir /api/vendors \
  -p 3010:3000 \
  registry.cn-hangzhou.aliyuncs.com/anoy/yapi \
  server/app.js
  
```

## 6、升级 Yapi

```bash
# 1、停止并删除旧版容器
docker rm -f yapi

# 2、获取最新镜像
docker pull registry.cn-hangzhou.aliyuncs.com/anoy/yapi

# 3、启动新容器
docker run -d \
  --name yapi \
  --link mongo-yapi:mongo \
  --workdir /api/vendors \
  -p 3010:3000 \
  registry.cn-hangzhou.aliyuncs.com/anoy/yapi \
  server/app.js
```





# 使用 Yapi

访问 http://ip:3010 

注册用户

连接mongoDB 数据库  找到yapi 库。user表，修改注册的用户role 为 admin ，普通用户为member





