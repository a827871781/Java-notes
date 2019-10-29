### 创建测试工程

### 新建一个 Jenkins 的 Maven 项目任务：

![d9bb80ea-f55f-11e9-ac07-acde48001122](https://i.loli.net/2019/10/23/Cr84XUtwobW7kuG.png )

### 源码管理配置

![f1d82452-f560-11e9-a1ab-acde48001122](https://i.loli.net/2019/10/23/YjlSi6OIQTqXcx8.png )

出现以上报错:

就单击蓝色框旁边的 **添加**

![17908932-f561-11e9-8637-acde48001122](https://i.loli.net/2019/10/23/Nn8ChpRTxXSwqv1.png )

id和描述 自己看着来,   用户名 和 密码 就是gitlab 已有的账号  或者 给 jenkins 分配一个账号

### 构建触发器

选择`Build when a change is pushed to GitLab. GitLab webhook URL:`项

并复制url 后面的路径

![17cda462-f565-11e9-b87e-acde48001122](https://i.loli.net/2019/10/23/JE4mtIgYOHxqCur.png )

单击高级按钮,再单击generate 按钮 生成密钥,复制到gitlab 配置

![0628f440-f566-11e9-8e54-acde48001122](https://i.loli.net/2019/10/23/K1qFAsbmHdZcIJB.png )

#### 在 gitlab 的项目里 设置 > 集成

![bf996db0-f566-11e9-8953-acde48001122](https://i.loli.net/2019/10/23/EnzsD3MPQlNYqWp.png )

### Build配置项

配置 Maven 打包指令， `clean package -Dmaven.test.skip=true -Dmaven.repo.local=/opt/mvnRepository` （根据项目使用的 Maven Build 插件来定,）：

注意这里没有 mvn，因为他是默认使用 maven 编译的！完整的命令是：

```shell
mvn clean package -Dmaven.test.skip=true 
```

其中：-Dmaven.test.skip=true 是跳过测试。

            -Dmaven.repo.local=/opt/mvnRepository  指定仓库

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

### 构建后脚本

这里构建后,就要往远端部署服务了.所以先配置 [配置 ssh 免密登陆](https://blog.csdn.net/zhuying_linux/article/details/7049078)

配置好免密登陆,

进入系统设置 ![](/Users/syz/Library/Application Support/marktext/images/2019-10-24-15-58-14-image.png)

**配置 ssh 插件**

![](https://i.loli.net/2019/10/24/HnExgZ1qwGKFdty.png)

在配置最后找到 “构建后操作”，选择 "**Send build artifacts over SSH**"


![](https://i.loli.net/2019/10/24/6VcJeTIzkXpq5hj.png)

![](https://i.loli.net/2019/10/25/4n9YFfq1Gd8DLVQ.png)

### 运行任务

![](https://i.loli.net/2019/10/24/xn4zuUo8AjypaDe.png)

再构建历史处 单击最新的构建任务.

![](https://i.loli.net/2019/10/24/bVTXRBH6o4clUQy.png)

![](https://i.loli.net/2019/10/24/tMBrgiqGxknF1jK.png)

![](https://i.loli.net/2019/10/24/pQBYbxZeAsCHWPN.png)

Springboot 自动部署脚本

此脚本默认使用,为自动部署,增加参数 rollback 为回滚到上一个版本

```shell
#!/bin/bash
# description:springboot 自动部署 1.0版本
# version 1.0
show_usage="args: [-t]\[--deploy-type=]"
#版本部署路径
mainpath=/home/java

# 应用名称
appName=helloworld

#主函数
function deploy()
{
  cd ${mainpath}
  echo "[info]start deploy...[$(date +'%F %H:%M:%S')]"
  stop
  backup
  start
}

#启动app
function stop(){


    echo `ps -ef | grep ${appName} | grep -v 'grep' | grep -v 'deploy'|awk  '{print $2}' `;

    PIDCOUNT=`ps -ef | grep ${appName} | grep -v 'grep' | grep -v 'deploy' | awk  '{print $2}' | wc -l`;


    echo "stopping pid count:$PIDCOUNT"
    if [ ${PIDCOUNT} -gt 0 ];then
     {
        # 获取进程ID
        appID=$(ps -ef | grep ${appName} | grep -v 'grep' | grep -v 'deploy' | awk  '{print $2}')
        echo "[info]当前进程ID为:$appID"
        kill -9 $appID
    } || {
        echo "[info]进程ID为:$appID停止异常"
    }
      fi
      echo "stoped pid:$appID"

}

#启动app
function start(){

    echo "starting $appName.jar"

    nohup java -jar  -Xms128m -Xmx512m $mainpath/$appName.jar --server.port=9090 > output.log 2>&1 &

    echo "success started $appName.jar"
}


#版本回滚
deploy_Rollback()
{
    #进入备份文件夹
    cd ${mainpath}/backup/
    #获取最新备份文件



    filecount=0
    for i in `ls | sort -r`;
    do
        filecount=$[$filecount+1]
    done;
    if [[ ${filecount} -lt 2  ]]; then
         echo "当前无备份.";
         exit 1
    fi
    num=0
    file_name_new=''
    for i in `ls | sort -r`;
    do
        num=$[$num+1]
        if [[ ${num} -eq 2 ]]; then
             echo $i;
              file_name_new=$i;
        fi
    done;


    #将备份文件复制到webapps
    cp  ${mainpath}/backup/${file_name_new} ${mainpath}/${appName}.jar
    if [ $? -eq 0 ]
    then
        echo 复制${file_name_new}成功
    else
        echo 复制失败，退出！
    exit 1
    fi
    #进入webapps/目录
    cd  ${mainpath}
    #重启App
    stop
    start
}

#备份原来的项目
function backup()
{
    echo "开始备份to${mainpath}...."
    fileDate=$(date "+%Y%m%d%H%M%S")
    fileName=${appName}${fileDate}
    cp $mainpath/${appName}.jar $mainpath/backup/${fileName}.jar

    cd ${mainpath}/backup/
    num=0
    for i in `ls | sort -r`;
    do
        num=$[$num+1]
        if [[ ${num} -gt 10 ]]; then
             echo 已将历史备份删除: $i;
              rm -f $i;
        fi

    done;
}

echo --------欢迎使用shell自动部署脚本--------

#获取用户操作

case $1 in
rollback)
    deploy_Rollback
    ;;
*)
    deploy
    ;;
esac
```
