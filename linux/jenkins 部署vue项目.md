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
npm install chromedriver --chromedriver_cdnurl=http://cdn.npm.taobao.org/dist/chromedriver
npm install
echo "info:开始编译"
gulp
echo "info:编译结束"
```



