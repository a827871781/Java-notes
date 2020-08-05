# 自动生成 serialversionuid

File --> Settings --> Editor --> Inspections --> 搜索 serialization --> 勾选如下两项:  -->  并将其设置为Error

Serializable class without serialversionuid

Serialversionuid field not declared private static final long

![30d9fb9a-1676-11ea-a25b-00e04c0008f5](https://i.loli.net/2019/12/04/GoFd8zfDNhb9lmI.png )

# 自动导包并去除*号

File --> Settings -->  Editor--> General --> Auto Import --> Imports  -->  勾选

-    Add unambiguous imports on the fly   ( 自动导包)
-   Optimize imports on the fly  (for current project)    (自动去除无用包)

![b70f6d4e-1676-11ea-88a6-00e04c0008f5](https://i.loli.net/2019/12/04/3lAwGqthVs8W6np.png )

File --> Settings -->  Editor--> Code Style--> Java--> Imports

-   将 Class count to use import with "*" 改为 99（导入同一个包的类超过这个数值自动变为 * ）
-    将 Names count to use static import with "*" 改为 99（同上，但这是静态导入的）

![1a3f0bf4-1677-11ea-8335-00e04c0008f5](https://i.loli.net/2019/12/04/z6TiolPuGZrQkJe.png )

ps:

去除*号是因为github 提交代码时,部分仓库开源者,可能抵触import * ,认为可能会导致问题.故有此配置.



# 启动 IDEA 时，弹出项目选择框

File --> Settings -->  Appearance & Behavior --> System Sttings 

-   取消勾选 Reopen last project on startup

![422415c8-1678-11ea-a013-00e04c0008f5](https://i.loli.net/2019/12/04/iEDZtk4Ry597uOm.png )

# idea 不显示打开文件名

File --> Settings -->  Editor --> General  -->  Editor Tabs

-   Tab placement :设置为 None

![1d020dbc-1679-11ea-9ee5-00e04c0008f5](https://i.loli.net/2019/12/04/uPbiUvJtEcBIznl.png )

使用command + e   打开最近访问的文件 

使用command + option   + 回车  跳转到最后编辑文件位置

还有更多跳转组合键具体详情可以看一看[快捷键](https://github.com/a827871781/Java-notes/blob/master/idea/调教Mac Idea Win键盘 快捷键.md)

熟练使用你会发现这要做的效率远远高于眼睛寻找在单击

如果想要知道当前编辑文件名字,下图两个位置都可以知道:

![a3b64e7c-1679-11ea-8275-00e04c0008f5](https://i.loli.net/2019/12/04/LyrAms7wubRDKz1.png )



# 忽略大小写提示

File --> Settings -->  Editor --> General  -->  Code Completion 

-   选中Match case  (取消选中为忽略大小写)
-   选中First letter only     ( 这里我设置为首字母区分大小写   )
-   选中Smart type completion 
-   图中有错误:All letters  为全部都不忽略大小写

![image-20191204174308068](/Users/syz/Library/Application Support/typora-user-images/image-20191204174308068.png)

# 显示最近svn/git提交人

在要显示的文件左侧右键单击  并 选中Annotate 即可显示

![5ae190f6-167b-11ea-aa03-00e04c0008f5](https://i.loli.net/2019/12/04/PcFLM9zQuEBaxfj.png )

# 编码,properties文件显示中文

File --> Settings -->  Editor --> Fo;e Encodings 

-   Global Encodeing : utf - 8
-   Project Encodeing : utf - 8 
-   Default encoding for properties files : utf - 8 
-   勾选Transparent native-to-ascii conversion

![image-20191204175626564](/Users/syz/Library/Application Support/typora-user-images/image-20191204175626564.png)

# idea 正则匹配

![image-20200709133148208](https://i.loli.net/2020/07/09/ZaADLnRxNjFVhS2.png)

# idea复制所选的行数完整内容

![image-20200804105159880](https://i.loli.net/2020/08/04/HEVohI3PiyRls6L.png)

Command +d 快捷键本来将复制所选内容并黏贴的，但是黏贴的位置是补充在原来的位置后。

改成这个就会变成复制所选行，并粘贴