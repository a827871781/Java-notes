## 一台nginx 上部署多个Vue 项目

### Vue处改动

1. 修改`config/index.js`文件

    ```js
    2module.exports = {
    //注意一定要是 build 下 的 assetsPublicPath属性
      build: {
        assetsPublicPath: "/test/";, //你要修改的前缀
        }
    }
    ```

2. 修改`index.html`文件

    ```html
      <!-- 增加一下内容   -->
    <mate base = "/test/"></mate>
    ```

3. 修改`src/router/index.js`文件

    ```js
    const router = new Router({
      base:'/test/',  //你要修改的前缀
    })
    ```

### nginx改动

```conf

    location /test/ {
    	 alias /x/x/x/test/;
		try_files $uri $uri/ /test/index.html;  
		#很重要这个路径要参考具体情况 在这里标识 test目录下index.html 文件 		
		#，如果是吧dict直接扔掉test目录下，要注意加入dict
		#以上写法映射的地址为/x/x/x/test/index.html 要注意！！！！  切记 不要盲目复制
    }


```
## 