## 安装插件

![image-20200701150547943](https://i.loli.net/2020/07/01/czjIr4lGPwSoOE6.png)

## 配置node

进入 Jenkins -> Global Tool Configuration 页面

![](https://i.loli.net/2020/07/01/kpveVzStxjGEQWM.png)







## 创建项目

![image-20200701152414896](https://i.loli.net/2020/07/01/4gDGqdzYxBHN8u3.png)

## 配置项目

### 构建环境配置

![image-20200701152632763](https://i.loli.net/2020/07/01/yAZtsuaYclCdnNW.png)

### 构建配置

![image-20200701152803615](https://i.loli.net/2020/07/01/JOxFXTbBSGtl7DV.png)



![image-20200701152827111](https://i.loli.net/2020/07/01/HGiBsuOJrwlSRx9.png)

```shell
#当前环境
echo $PATH
node -v
npm -v
echo "info:开始删除dist目录"
rm -rf dist

npm install
echo "info:开始编译"
gulp
echo "info:编译结束"
```



### docker配置

```dockerfile
FROM nginx:1.8.1


RUN mkdir /www

ADD www /www

ADD conf/nginx.conf /opt

CMD envsubst '$API_SERVER $API_PORT $RESOLVER'  < /opt/nginx.conf > /etc/nginx/nginx.conf && nginx -g 'daemon off;'

EXPOSE 80

```

```conf

user  nginx;
worker_processes  2;

error_log  /var/log/nginx/error.log info;
pid        /var/run/nginx.pid;


events {
    worker_connections  5000;
}


http {

    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;
    keepalive_timeout  65;
    gzip  on;
    client_max_body_size 500m;
    resolver $RESOLVER;




    #include /etc/nginx/conf.d/*.conf;

	server {

	    listen       80;
	    server_name  localhost;
        # gzip config
        gzip on;
        gzip_min_length 1k;
        gzip_comp_level 9;
        gzip_types text/plain application/javascript application/x-javascript text/css application/xml text/javascript application/x-httpd-php image/jpeg image/gif image/png;
        gzip_vary on;
        gzip_disable "MSIE [1-6]\.";
       

	    #charset koi8-r;
	    #access_log  /var/log/nginx/log/host.access.log  main;

	    location / {
	        root   /www;
	        index  index.html index.htm login.html;
            # 解决vue 项目刷新404问题
            try_files $uri $uri/ /index.html;
        }

	    location ~ /api/(.*) {

	    	proxy_redirect  off;
	    	proxy_pass http://$API_SERVER:$API_PORT/$1$is_args$args;
	    }
	    
	}
}

```



```shell
#!/usr/bin/env bash
#进入到dockerfile 文件目录
cd /opt/

image_name="test";
image_version=`date +%Y%m%d%H%M`;

echo "info:开始构建docker镜像"

#www 为html 代码路径
rm -rf www

#缺省将npm build 后的dist目录移动至当前目录下 www目录内
*************


docker stop $image_name 
docker rm $image_name 

docker build  -t $image_name:$image_version . 

echo "info:构建docker镜像结束"

echo "info:启动docker镜像"
docker run -d --name $image_name -p 8091:80  -e TZ="Asia/Shanghai"  -e API_SERVER=192.168.50.50  -e API_PORT=5062 -e =127.0.0.1  $image_name:$image_version
```

