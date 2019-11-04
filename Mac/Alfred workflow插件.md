# Alfred

## 自带功能

|  快捷键  |             功能             |
| :------: | :--------------------------: |
|    ！    |       执行 shell 命令        |
|   lock   | 默认锁屏，修改为直接进入屏保 |
| restart  |             重启             |
| shutdown |             关机             |
|  logout  |             登出             |
|   quit   |           关闭 app           |
|   hide   |          最小化app           |
|    bm    |           书签搜索           |
|          |                              |
|          |                              |
|          |                              |
|          |                              |
|          |                              |
|          |                              |
|          |                              |
|          |                              |
|          |                              |
|          |                              |
|          |                              |

## workflow 插件

### CodeVar

#### 功能：

中文转英文命名

#### 使用：

- `xt + 单词`：小驼峰命名法
- `dt + 单词`：大驼峰命名法
- `xh + 单词`：下划线命名法
- `cl + 单词`：常量命名法
- `zh + 单词`：中划线命名法

#### 地址：

https://github.com/xudaolong/CodeVar

### terminalfinder

#### 功能：

**在终端中和Finder切换**

#### 使用：

- `ft`：在**终端中**打开当前的**Finder**目录
- `tf`：在 **Finder 中**打开当前**终端**目录
- `fi`：在 **iTerm 中**打开当前的**Finder**目录
- `if`：在 **Finder 中**打开当前的**iTerm**目录
- `pt`：在 **Terminal 中**打开当前的**Path Finder**目录
- `tp`：在**路径查找器中**打开当前**终端**目录
- `pi`：在 **iTerm 中**打开当前的**Path Finder**目录
- `ip`：在 **Path Finder 中**打开当前的**iTerm**目录

#### 地址

http://www.packal.org/workflow/terminalfinder

### Google Translate

#### 功能：

**谷歌翻译，中英互译**

#### 使用：

- `tr + 要翻译的单词`：

**选中单词按后：**

enter ： 阅读

cmd+ C ： 复制项目

cmd+ L ： 查看完整内容

**全局快捷键：**

option  + t ： 划词翻译

#### 地址

https://github.com/xfslove/alfred-google-translate

### Kill Process

#### 功能：

**快速杀掉进程**

#### 使用：

- `kill + app 名`：可以输入不全，会自动推断

#### 地址

https://github.com/ngreenstein/alfred-process-killer

### Fakeum

#### 功能：

**生成假测试数据**

#### 使用：

- `fake name`：名称
- `fake email`：email
- `fake date`：日期
- `fake datetime`：日期时间

#### 地址

https://github.com/deanishe/alfred-fakeum

### Secure Shell

#### 功能：

可在 Alfred 上快速打开 SSH/SFTP/mosh 链接

#### 使用：

默认启动关键字是：`ssh`。默认情况下，在选中的 SSH 链接上直接回车后就会在终端中访问对应的 SSH 服务器。

#### 地址：

https://github.com/deanishe/alfred-ssh/

#### 配置方法：

[**alfred 集成 ssh+iTerm2 实现一步登录服务器**](https://github.com/a827871781/Java-notes/blob/master/my-alfred-workflow/alfred 集成 ssh%2BiTerm2 实现一步登录服务器.md)

### UUIDGen

#### 功能：

可在 Alfred 上快速获取 UUID

#### 使用：

默认启动关键字是：`UUID`。

#### 地址：

http://www.packal.org/workflow/uuid-generator-0

### 切换外观模式

#### 功能：

可在 Alfred 上快速切换在电脑深色与浅色模式，

#### 使用：

默认启动关键字是：`dk`。

#### 地址：

[https://cdn.sspai.com/%E5%88%87%E6%8D%A2%E5%A4%96%E8%A7%82%E6%A8%A1%E5%BC%8F-Alfred.alfredworkflow.zip](https://cdn.sspai.com/切换外观模式-Alfred.alfredworkflow.zip)

### Toggle Wifi

#### 功能：

可在 Alfred 上打开与关闭 wifi

#### 使用：

默认启动关键字是：`wifi`。

#### 地址：

http://www.packal.org/workflow/toggle-wifi

### Hidden Files

#### 功能：

可在 Alfred 上隐藏和显示文件夹

#### 使用：

默认启动关键字是：`hidden`。

#### 地址：

http://www.packal.org/workflow/toggle-hidden-files

### Reminders for Alfred 3

#### 功能：

可在 Alfred 上添加提醒事项

#### 使用：

默认启动关键字是：`r`。

`r <some text>` : ` r lol `添加lol至提醒事项 , `<some text>`为提示的标题

`r today <some text>`  :  今天加入一个标题为`<some text>`的提醒事项

`r tomorrow <some text>`  :  明天加入一个标题为`<some text>`的提醒事项

`r in <n> minutes <some text>`  :  n分钟后 提示 标题为`<some text>` 的提醒事项 ,`<n>`为数字

`r in <n> hours <some text>`  :  n小时后 提示 标题为`<some text>` 的提醒事项

`r on <data> <some text>`  :  指定日期`<data>` 提示 标题为`<some text>` 的提醒事项,`<data>`为日期,格式月/日/年,或者月-日-年

`r on <dataTime> <some text>`  :  指定日期时间`<dataTime>` 提示 标题为`<some text>` 的提醒事项,`<dataTime>`为日期时间,格式月/日/年 时:分,或者月-日-年 时.分

`r at <n>pm <some text>`  : 下午n点提醒

`r at <n>am <some text>`  : 上午n点提醒

`r next thursday at 15.30 <some text>`  : 下周4 ,15:30提醒

`r help` 将显示一些内置示例。

`r this` 将捕获当前应用程序并将其转换为提醒。

支持的应用程序

- Adobe Acrobat (Pro/DX)
- Chromium
- Contacts
- Finder
- FoldingText
- Google Chrome
- Google Chrome Canary
- Mail
- Mailplane 3
- Microsoft PowerPoint
- Microsoft Word
- Safari
- TextEdit
- TextMate
- Vienna
- WebKit

#### 地址：

https://github.com/surrealroad/alfred-reminders

### JetBrains - Open Project - v3

#### 功能:

打开切换 **JetBrains** 项目

#### 地址：

https://github.com/bchatard/alfred-jetbrains

### Pretty JSON

#### 功能:

json格式化

#### 使用:

默认启动关键字是：`json`。

选中需要格式化的json 文本,然后输入 json 格式化  文本

#### 地址:

http://www.packal.org/workflow/pretty-json

### Password Generator

#### 功能:

密码生成

#### 使用:

默认启动关键字是：`pwgen`。

#### 地址:

https://github.com/deanishe/alfred-pwgen#installation

# Recent Documents

#### 功能:

快速打开最近访问的文档、文件夹、应用。
快速打开当前应用的最近访问文件。

#### 使用:

输入`rd`，列出最近打开的各种文件。

输入`rr`，列出当前激活应用的最近文档。

输入`rf`，列出最近访问的文件夹。

输入`rd`，列出最近打开的各种文件。

#### 地址:

https://github.com/mpco/AlfredWorkflow-Recent-Documents/blob/master/README_CN.md



# Uninstall with AppCleaner

#### 功能:

配合AppCleaner App  更为干净的卸载 app

#### 使用:

输入`uninstall` + App名，列出最近打开的各种文件。



#### 地址:

AppCleaner下载地址 :http://freemacsoft.net/appcleaner/

https://github.com/Louiszhai/tool/blob/master/workflow/AppCleaner.alfredworkflow?raw=true