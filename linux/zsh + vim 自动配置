## ZSH

```shell
wget https://github.com/FanhuaCloud/ZSH_Install/archive/master.zip
unzip master.zip
cd ZSH_Install-master
./zsh.sh
```

执行完脚本后:

### 配置插件:

#### autojump

使用 `autojump` 的缩写 `j`

`cd` 命令进入 `~/user/github/Youthink` 文件夹，下一次再想进入 `Yourhink` 文件夹的时候，直接 `j youthink` 即可
或者只输入 `youthink` 的一部分 `youth` 都行



```shell
#安装 autojump  mac
brew install autojump
# Linux
git clone git://github.com/joelthelion/autojump.git
#进入目录，执行
cd autojump
./install.py
```

最后把以下代码加入 `.zshrc`：

```
[[ -s ~/.autojump/etc/profile.d/autojump.sh ]] && . ~/.autojump/etc/profile.d/autojump.sh
```

#### zsh-syntax-highlighting

**作用** 平常用的 `ls`、`cd` 等命令输入正确会绿色高亮显示，输入错误会显示其他的颜色。

```shell
#安装
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
#在 ~/.zshrc 中配置
plugins=(其他的插件 zsh-syntax-highlighting)
```



#### zsh-autosuggestions

**作用**

效率神器 👍

如图输入命令时，会给出建议的命令（灰色部分）按键盘 → 补全

```shell
#安装
git clone git://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions
#在 ~/.zshrc 中配置
plugins=(其他的插件 zsh-autosuggestions)
```

这个可能会有颜色不清晰的问题

解决方案:

```shell
 #在 ~/.zshrc 中增加如下行
 ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=yellow'
```



#### 使配置生效

```shell
source ~/.zshrc
```





## vim

```shell
#命令行执行该命令
wget -qO- https://raw.github.com/ma6174/vim/master/setup.sh | sh -x
```

