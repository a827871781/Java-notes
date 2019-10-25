# 安装 lrzsz

首先先假定你安装了 [Homebrew](https://brew.sh/)，然后我们通过它，先给 Mac 安装 lrzsz。
在终端下输入 `brew install lrzsz`，静等一会即可安装完毕。

# 配置 iTerm2 脚本

给 iTerm2 加上相应配置前需要下载两个别人已经写好的脚本文件。

[下载地址](https://github.com/aikuyun/iterm2-zmodem)

```shell
cd /usr/local/bin
git clone https://github.com/aikuyun/iterm2-zmodem.git
cd iterm2-zmodem
cp iterm2-recv-zmodem.sh ../
cp iterm2-send-zmodem.sh ../
#文件赋予可执行权限
chmod +x /usr/local/bin/iterm2-send-zmodem.sh /usr/local/bin/iterm2-recv-zmodem.sh
```

# 配置 iTerm2

找到 iTerm2 的配置项：iTerm2 的 Preferences-> Profiles -> Default -> Advanced -> Triggers 的 Edit 按钮。

然后配置项如下：

| Regular Expression              | Action               | Parameters                           | Instant |
| ------------------------------- | -------------------- | ------------------------------------ | ------- |
| rz waiting to receive.\*\*B0100 | Run Silent Coprocess | /usr/local/bin/iterm2-send-zmodem.sh | checked |
| \*\*B00000000000000             | Run Silent Coprocess | /usr/local/bin/iterm2-recv-zmodem.sh | checked |

**尤其注意最后一项需要你将 Instant 选项勾上，否则将不生效**

注意看图：

[![iterm2-lrzsz](https://img.piegg.cn/iterm2-lrzsz.png)](https://img.piegg.cn/iterm2-lrzsz.png)

重新启动 iTerm 之后，rz/sz 就应该可以正常使用了。

# centos 7 安装lrzsz

```shell
 yum -y install lrzsz
```

只要服务端也已经装好了 `lrzsz` 工具包便可以方便地通过 rz\sz 来进行文件上传下载了。
