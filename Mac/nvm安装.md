# 安装

本次安装采用安装文件方式安装,没用brew安装的原因是因为官方不推荐

```shell
#进入 ~文件夹
cd ~
#查找.bash_profile文件  如果没有新建一个文件,有的话 就确认有就没问题了
vim .bash_profile

#访问https://github.com/nvm-sh/nvm/blob/master/README.md 找到最新安装文件

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash


```

![Xnip2020-04-29_20-03-55.jpg](https://i.loli.net/2020/04/29/egytzXlB9SbHn71.jpg)

这里我选择的是第一种,curl的安装方式

执行完安装命令后

重启终端

执行nvm 有如下提示 就是安装成功

![Xnip2020-04-29_20-39-41.jpg](https://i.loli.net/2020/04/29/kuSLYAMDGRU6W4j.jpg)

