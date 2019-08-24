# git PR 提交

## 提交过程：

git分 本地仓库和远程仓库。

### 本地仓库：

1. 将要修改的项目fork至自己github

2. 将自己github 的代码clone至个人计算机。

   ```shell
   git clone https://github.com/X/X.git #这里是你的github代码地址
   ```

3. 计算机上的代码和上游建立连接。

   ```shell
   git remote add upstream XXX # fork的原地址
   ```

4. 查看上游连接

   ```shell
   git remote -v 
   ```

5. 创建新分支

   ```shell
   git checkout -b XXX #XXX 为分支名 
   #这条命令是创建并切换到新建分支
   ```

6. 自行修改代码

7. 修改的代码提交至新建的分支下

   ```shell
   git status #查看修改
   git add ***.java # 将所有修改的java后缀的文件，暂存待提交
   git commit -m "XXX" # XXX 提交时要说的话 
   git push origin XXX # XXX 刚才新建的分支名 ，将当前分支推送到自己的远程仓库
   
   ```

### 远程仓库

1. github 在自己fork的项目页面内找到 ` New pull request`
2. 选择 刚才提交上来的分支 单击`compare  `按钮
3.  跳页 单击 `Create pull request`按钮
4. 写好名字，写好说明，提交，就 OK 啦。 

参考：<https://blog.csdn.net/vim_wj/article/details/78300239>