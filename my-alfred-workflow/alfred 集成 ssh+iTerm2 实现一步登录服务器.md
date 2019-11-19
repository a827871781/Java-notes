# alfred - ssh

## 下载alfred - ssh

**github 地址**：https://github.com/deanishe/alfred-ssh/

**下载地址**：https://github.com/deanishe/alfred-ssh/releases/tag/v0.8.0

![fb721fd4-cd4e-11e9-8177-acde48001122](https://i.loli.net/2019/09/02/CXB7OfHWQr6p8mu.png )

## 安装 alfred 集成 Iterm2 配置

## Iterm2 配置：

![47196122-cd4f-11e9-b25b-acde48001122](https://i.loli.net/2019/09/02/liPr7Xd4uCx12DH.png )

## Alfred配置

首先在 Alfred 的 Features 页面，具体为 Alfred `Preferences → Features → Terminal/Shell` 将 Application 的值改为 Custom

![82dfeb4a-cd4f-11e9-abe6-acde48001122](https://i.loli.net/2019/09/02/CKQUH35FOXnj2rJ.png )

图内3 位置的文本不同版本 iterm 的代码有所不同。

通过访问：

https://github.com/stuartcryan/custom-iterm-applescripts-for-alfred/

![d9905b0a-cd4f-11e9-9ce1-acde48001122](https://i.loli.net/2019/09/02/qZXLMpITEONSkw5.png )

根据自己 iterm 的版本获取，如果不知道，就用 3.1.1

复制命令在终端中输入。结果会自动复制到剪切板内，

将代码粘贴到 3 的位置。

## iterm 配置密码登录登陆

实现密码登录的方法是通过 `openssh` 的 `ssh config` 的功能。具体操作为～/.ssh/config，如果不存在，可以新建一个

```shell
vim ~/.ssh/config

# host 别名  HostName ip ，User 用户名
Host aliyun  
  HostName 192.168.1.1
  User root
  Port 22
```

保存退出。这时在 *iTerm2* 中就可以输入 `ssh aliyun`, 回车 然后输入密码。注意，这时候已经不用输入 ssh root@192.168.1.1，只要输入密码就登录上了。

## iterm设置免密登录

方法是使用 `ssh-copy-id` 功能，原理是将本机的密钥复制到远程要连接的机器上，从而授权连接。iterm 终端输入：

```shell
ssh-keygen
#输入完 就一路回车就行。
```

### 复制密钥到远程目的服务器

```shell
#   demouser@192.168.1.1      root:用户名   ，192.168.1.1 ： ip
ssh-copy-id -i root@192.168.1.101
```

## 快速添加服务器地址

用以下shell 脚本 即可

```shell
#!/bin/bash
# 四个参数,分别对应
#hostname   // ip地址  必填
#Host   别名   默认值为 hostname
#user   用户,默认值 root
#port  端口号 默认值 22 
#
#
#
#
ip=$1
if [ ! ${ip} ]; then
       echo "ip is miss"
     exit 1
fi

name=$2
if [ ! $2 ]; then
    name=$ip
fi

user=$3
port=$4

if [ ! $3 ]; then
    user='root'
fi

if [ ! $4 ]; then
    port='22'
fi

echo "Host ${name}" >> /Users/syz/.ssh/config
echo "  HostName ${ip}" >> /Users/syz/.ssh/config
echo "  User ${user}" >> /Users/syz/.ssh/config
echo "  Port ${port}" >> /Users/syz/.ssh/config

cd /Users/syz/.ssh
a='ssh-copy-id -i root@'
eval $a$ip
```

## 在终端中切换服务器

用以下py脚本,并为该脚本配置别名.可以更加方便切换服务器.

我将其定义为sshp

通过输入sshp命令,可以打印出配置文件内所有服务器配置.格式为序号 + hostName

通过输入序号,即可在终端内切换不同服务器..

此脚本为alfred的补充,

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
dict ={}
dictA ={}
def readFile(fileName):

    flag=0
    lastHost=""
    file = open(fileName)
    while 1:
        line = file.readline()
        if not line:
            break
        if flag:
            dict[lastHost.split( )[1]]=line.split( )[1]
            flag=0
        if "Host " in line:
            flag=1
            lastHost = line


def printDict():
    index=1
    for key in dict.keys():
        dictA[index]=key
        print('{} : {}'.format(index,key))
        index=index+1


if __name__ == '__main__':
    readFile("/Users/syz/.ssh/config")
    print("以下为当下所有可连接服务器:")
    printDict()
    print("请输入想要连接服务器的序号:")
    a = int(sys.stdin.readline().strip())
    str="ssh root@{}".format(dict[dictA[a]])
    print(str)
    os.system(str)
```



### 使用效果:

![11aae7d4-0a9b-11ea-a8af-acde48001122](https://i.loli.net/2019/11/19/2HcaFEidPCb8mv1.png )