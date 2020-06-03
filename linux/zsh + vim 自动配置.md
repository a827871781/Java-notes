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

```shell
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
 # 支持以下颜色 black, red, green, yellow, blue, magenta, cyan and white 
 ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=yellow'
 #可能会不生效 那么就执行一下命令并重启item
 echo "export TERM=xterm-256color" >> ~/.zshrc
```



#### 使配置生效

```shell
source ~/.zshrc
```



## vim

环境要求:git /  zsh / yum  / centos

```shell
#命令行执行该命令
wget -qO- https://raw.githubusercontent.com/a827871781/other/master/my-script/installVim.sh | sh -x
```

一些vim的配置 及 NERDTree 插件一起安装 配置

双击esc 退出vim  == :q

F2 打开NERDtree 文件树视图

NERDtree一些常用快捷键

```bash
ctrl + w + h    光标 focus 左侧树形目录
ctrl + w + l    光标 focus 右侧文件显示窗口
ctrl + w + w    光标自动在左右侧窗口切换 #！！！
ctrl + w + r    移动当前窗口的布局位置
o       在已有窗口中打开文件、目录或书签，并跳到该窗口
go      在已有窗口 中打开文件、目录或书签，但不跳到该窗口
t       在新 Tab 中打开选中文件/书签，并跳到新 Tab
T       在新 Tab 中打开选中文件/书签，但不跳到新 Tab
i       split 一个新窗口打开选中文件，并跳到该窗口
gi      split 一个新窗口打开选中文件，但不跳到该窗口
s       vsplit 一个新窗口打开选中文件，并跳到该窗口
gs      vsplit 一个新 窗口打开选中文件，但不跳到该窗口
!       执行当前文件
O       递归打开选中 结点下的所有目录
x       合拢选中结点的父目录
X       递归 合拢选中结点下的所有目录
e       Edit the current dif

双击    相当于 NERDTree-o
中键    对文件相当于 NERDTree-i，对目录相当于 NERDTree-e

D       删除当前书签

P       跳到根结点
p       跳到父结点
K       跳到当前目录下同级的第一个结点
J       跳到当前目录下同级的最后一个结点
k       跳到当前目录下同级的前一个结点
j       跳到当前目录下同级的后一个结点

C       将选中目录或选中文件的父目录设为根结点
u       将当前根结点的父目录设为根目录，并变成合拢原根结点
U       将当前根结点的父目录设为根目录，但保持展开原根结点
r       递归刷新选中目录
R       递归刷新根结点
m       显示文件系统菜单 #！！！然后根据提示进行文件的操作如新建，重命名等
cd      将 CWD 设为选中目录

I       切换是否显示隐藏文件
f       切换是否使用文件过滤器
F       切换是否显示文件
B       切换是否显示书签

q       关闭 NerdTree 窗口
?       切换是否显示 Quick Help
:tabnew [++opt选项] ［＋cmd］ 文件      建立对指定文件新的tab
:tabc   关闭当前的 tab
:tabo   关闭所有其他的 tab
:tabs   查看所有打开的 tab
:tabp   前一个 tab
:tabn   后一个 tab

标准模式下：
gT      前一个 tab
gt      后一个 tab
```