写在最初 : 

Git 可以对任何命令使用 `--help` 选项，例如，`git stash --help`

1. `git config --list`  检查已有配置信息

2. `git status`  查看修改

3. `git checkout -b <branchname>` 基于当前分支,新建分支并切换

4. `git branch -m <current-branch-name> <new-branch-name>` 分支改名

5. `git add .   `     添加所有文件到暂存区

6. `git add -p .` 添加暂存区之前,先将所有改动打印出来,再询问是否添加.

7. `git commit -m [message]`     提交暂存区到仓库区

8.  `git push origin <branchName>`       将本地的分支推送到 origin 主机的 分支,没有就新建

9.  `git push origin --delete <branchName>`   删除远端分支

10.  `git reset --soft HEAD~n` 回退到前N个版本，只回退了 commit 的信息，不会恢复到 index file 一级。如果还要提交，直接 commit 即可；

11.  `git reset -–hard HEAD~n` 彻底回退到N个版本，本地的源码也会变为上一个版本的内容，撤销的 commit 中所包含的更改被冲掉；

12.  `git commit --amend -m  `  修改最后一次 commit 提交信息

13.  `git commit --amend --no-edit`  修改最后一次提交的文件 

14.  `git log`  查看git提交记录,commit 为 提交的idI

15.  `git show <commitId>` 查看  commitId 的提交内容

16.  `git push origin [tagname]` 远端推送标签 

17.  `git push origin --tags` 推送所有标签

   ​    



## 新建Git 仓库是,最后新建一个README.md文件,不然可能会导致许多命令都报错



## git 命令行 git status 时 中文乱码解决

```shell
git config --global core.quotepath false
```



## 运行 Git 命令时，输出的结果会在新窗口打开，需输入 `q` 关闭窗口解决

```shell
git config --global core.pager ''
```

## git commit 提交时,部分乱码解决

```shell
#提交文件
git config --global i18n.commitencoding utf-8
#界面、
git config --global gui.encoding utf-8 
#提交日志 
git config --global i18n.logoutputencoding utf-8
```

