1. `git status`  查看修改

2. `git add .   `     添加当前目录的所有文件到暂存区

3. `git commit -m [message]`     提交暂存区到仓库区

4. `git push origin master`       将本地的 master 分支推送到 origin 主机的 master 分支

5.  `git push origin --delete <branchName>`   删除远端分支

6.  `git reset –-soft ` 回退到某个版本，只回退了 commit 的信息，不会恢复到 index file 一级。如果还要提交，直接 commit 即可；

7.  `git reset -–hard` 彻底回退到某个版本，本地的源码也会变为上一个版本的内容，撤销的 commit 中所包含的更改被冲掉；

8.  `git commit --amend -m  `  修改最后一次 commit 提交信息

9.  `git commit --amend --no-edit`  修改最后一次提交的文件 

10.  `git log`  查看git提交记录,commit 为 提交的id

11.  `git show <commitId>` 查看  commitId 的提交内容

      





## git 命令行 git status 时 中文乱码解决

```shell
git config --global core.quotepath false
```

