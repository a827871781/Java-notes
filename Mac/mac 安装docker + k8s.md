#  Docker + k8s

## docker

### 安装

```shell
brew install docker --cask
```

### 配置 Docker 镜像国内加速：

```config
{
  "debug": true,
  "experimental": false,
  "registry-mirrors": [
    "https://hub-mirror.c.163.com",
    "https://docker.mirrors.ustc.edu.cn",
    "https://mirror.baidubce.com"
  ]
}
```

![](https://img-blog.csdnimg.cn/20200525170253512.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Fkc29uMTk4Nw==,size_16,color_FFFFFF,t_70)

## kubernetes

### 下载

由于国内被墙的缘故，可选择阿里云 git 这种方式下载 k8s 镜像，这里适配 docker 的 k8s 版本地址可以查看：

![](https://img-blog.csdnimg.cn/20200525170803395.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Fkc29uMTk4Nw==,size_16,color_FFFFFF,t_70)

安装使用:

https://github.com/AliyunContainerService/k8s-for-docker-desktop