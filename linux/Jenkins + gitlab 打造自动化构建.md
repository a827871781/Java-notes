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



### 构建前执行脚本



![799b99b6-f622-11e9-88d2-acde48001122](https://i.loli.net/2019/10/24/V6n9rIuzKlwJeGH.png )

```shell
#将工作空间的jar包删除
SERVER_NAME_1=swapping
echo "=========================>>>>>>>工作空间WORKSPACE的地址：$WORKSPACE "
cd $WORKSPACE

echo "=========================>>>>>>>进入工作空间WORKSPACE，清除工作空间中原项目的工作空间$SERVER_NAME_1 "
rm -rf $SERVER_NAME_1

echo "=========================>>>>>>>清除工作空间中原项目的工作空间$SERVER_NAME_1 ......成功success"
```

