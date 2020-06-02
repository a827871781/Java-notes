# 高效回退到特定层级目录

Linux 下如果我们进入到了一个比较长的路径，比如：

```
/home/alvin/projects/blogdemos/linux-system-programming/thread
/home/alvin/projects/blogdemos/diff
```

如果我们想要回退到一个特定的父目录，那么我们通常的做法是这样敲：

```
$ cd ../../../
```

如果层级比较少，那这样勉强还可以接受，但如果层级很深，那可能就会 cd 到你怀疑人生了。

本文将介绍一个工具，它能帮你快速进入到某一个特定的父目录，而无需一路 cd 。你可以直接指定回退的层级数，或者要回退的目标目录，非常方便。

更重要的是，它甚至还支持 tab 键，而且在不重复的情况下，你也可以指定目标目录的前几个字母即可，大大增加了工作效率。

这个工具其实就是个 shell 脚本，名字是 `up.sh` ，除了支持 bash 外，对 zsh 和 fish shell 的支持也很好。

#### up 脚本的安装

这个脚本是第三方人员开发的，所以需要我们人为安装到我们的系统。

首先，我们需要先将 up.sh 下载到我们本地，然后再使能这个脚本：

```shell
curl --create-dirs -o ~/.config/up/up.sh https://raw.githubusercontent.com/shannonmoeller/up/master/up.sh

echo 'source ~/.config/up/up.sh' >> ~/.bashrc

source ~/.bashrc
```

如果你使用的是 zsh shell ，那么需要使用下列步骤去操作：

```shell
curl --create-dirs -o ~/.config/up/up.sh https://raw.githubusercontent.com/shannonmoeller/up/master/up.sh

echo 'source ~/.config/up/up.sh' >> ~/.zshrc

source ~/.zshrc
```

如果你使用的是 fish shell ，那你需要这么操作：

```shell
curl --create-dirs -o ~/.config/up/up.fish https://raw.githubusercontent.com/shannonmoeller/up/master/up.fish

 source ~/.config/up/up.fish
```

#### up 脚本的使用

按照以上步骤操作，我们就能将 up 脚本安装到系统并完成配置。接下来我们就可以用它来尽情地玩耍了。

首先，我们先明确自己所处的路径：

```shell
pwd
#/home/alvin/projects/atb4g/ecall/src/interface
```

如果我们只想回到上级目录，只需执行 `up` 即可。

```shell
up
pwd
#/home/alvin/projects/atb4g/ecall/src
```

那如果我想回退到更高层级的目录呢？我现在是在 src 目录，如果我想回退到 projects 目录，要怎么操作？

我们只需要 up 命令后跟上你要跳转的层级数，不加的话就默认是 1 。在这个例子里，我们要回退 3 层目录，即：

```shell
 up 3
 pwd
#/home/alvin/projects
```

前面已经提到，我们可以直接回退到某一个指定的目录名下。比如我现在还是在 src 目录，想要回退到 projects 目录，我们可以这样操作：

```shell
 pwd
#/home/alvin/projects/atb4g/ecall/src
 up projects
 pwd
#/home/alvin/projects
```

如果要回退的单词长度太长写得太累怎么办？你只需指明这个目录的前几个字母， up 脚本就会识别并跳转。

```shell
pwd				
#/home/alvin/projects/atb4g/ecall/src
up pr        # 这里只指定了前两个字母
pwd
#/home/alvin/projects
```

同时，它也支持 tab 键：

```shell
 pwd
# /home/alvin/projects/atb4g/ecall/src
 	up    # 敲 tab 键
#ecall/    atb4g/    projects/    alvin/    home/
```


