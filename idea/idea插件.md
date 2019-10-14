# 插件推荐


| 名称                           | 功能                                                     | 快捷键                 |
| ------------------------------ | -------------------------------------------------------- | ---------------------- |
| AceJump                        | 快速定位光标位置                                         | ctrl+;                 |
| alibaba java coding guidelines | 代码检查                                                 | Ctrl+Shift+Alt+J       |
| CamelCase                      | 驼峰式大小写插件                                         | ctrl + shift + u       |
| GenerateAllSetter              | 自动生成 setter 方法调用                                 | Alt + enter            |
| HighlightBracketPair           | 括号自动高亮匹配                                         | nav                    |
| JRebel for Intellij            | 热部署（力荐，需要破解）                                 | Ctrl + F9              |
| Key  Promoter X                | 快捷键提示                                               |                        |
| Lombok                         | 通过注解生成代码                                         |                        |
| Maven Helper                   | 解决maven jar包冲突                                      |                        |
| MyBatis log Plugin             | 优化mybatis 日志输出，直接生成sql                        | ctrl + shift + alt + o |
| MyBatisCodeHelperPro           | 代码生成（力荐，需破解）                                 |                        |
| Plugin aiXcoder                | 智能代码提示（暂时没感觉作用）                           | ctrl + space           |
| Rainbow Brackets               | 配对括号相同颜色                                         |                        |
| RestfulToolkit                 | 接口自测及接口搜索功能                                   | ctrl + \               |
| Translation                    | 谷歌翻译                                                 | ctrl + shift + o       |
| alibaba cloud toolkit          | 远程部署                                                 |                        |
| Save action                    | 自动格式化代码 及删除无用包和google java format 组合使用 | 配置 图 1              |
| FindBugs-IDEA                  | 前找到这些潜在的问题                                     |                        |

## Save action

**图 1：**

![ca2abc3c-de7f-11e9-9ffe-acde48001122](https://i.loli.net/2019/09/24/1GAp8Vu3br5OzkU.png )

上图:     **Reformat file**  也要勾选





## FindBugs-IDEA

1.  Bad pratice 编程的坏习惯
    主要是命名问题，比如类名最好以大写开头，字符串不要使用等号不等号进行比较，可能会有异常最好用 try-catch 包裹的代码，方法有返回值但被忽略等等，这些如果不想改可以直接忽略.

2.  Malicious code vulnerability 恶意代码漏洞
    听起来很吓人呀，主要是一些属性直接使用 public 让别的类来获取，建议改为 private 并为其提供 get/set 方法.
    还有一些 public 的静态字段，可能会被别的包获取之类的.
    这些也需要根据项目具体情况来，个人意见，在有的不重要类，有时直接公开使用属性，可能更为便捷。如果你认为这些不需要修改，完全可以忽略.

3.  Dodgy code 糟糕的代码
    比如一个 double/float 被强制转换成 int/long 可能会导致精度损失，一些接近零的浮点数会被直接截断，事实上我们应该保留.

    -   比如使用 switch 的时候没有提供 default。

    -   多余的空检查，就是不可能为空的值，增加了不为空判断，这是没有必要的。属于代码冗余

    -   不安全的类型转换等等。

        这项太多了，就不一一列举了。

4.  performance 性能
    主要是一些无用的代码，比如声明了没有用到的属性等等
    
5.  correctness 代码的正确性 这一项应该算是最重要的了
    主要是没有对变量进行不为空判定，在特殊情况可能发生空指针异常.
    
6.  