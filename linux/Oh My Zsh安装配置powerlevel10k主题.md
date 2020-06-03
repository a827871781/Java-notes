## 安装

```shell
#github 镜像地址
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/powerlevel10k

#国内gitee镜像地址
git clone --depth=1 https://gitee.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/powerlevel10k

# 然后设置 .zshrc 中的变量 ZSH_THEME
ZSH_THEME="powerlevel10k/powerlevel10k" 

sourc ~/.zshrc

```

##字体安装
### 自动字体安装

如果您使用的是iTerm2或Termux，`p10k configure`则可以为您安装推荐的字体。在询问是否安装*Meslo Nerd字体*时，只需回答`Yes`。

如果使用其他终端，请手动进行字体安装。 

### 手动字体安装

下载以下四个ttf文件：

-   [MesloLGS NF Regular.ttf](https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS NF Regular.ttf)
-   [MesloLGS NF Bold.ttf](https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS NF Bold.ttf)
-   [MesloLGS NF Italic.ttf](https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS NF Italic.ttf)
-   [MesloLGS NF Bold Italic.ttf](https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS NF Bold Italic.ttf)

根据系统的不同,做相关的字体安装处理

## 配置

输入一下命令,进行个性化配置

```shell
p10k configure
```

