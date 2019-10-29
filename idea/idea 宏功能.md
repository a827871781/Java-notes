# 记录 idea 一个宏的设置:

## 需求:

平时开发,一般都是mvc 三层 代码 结构:

一般就是 control + service + servider 实现类 + dao

其中  从service 创建好方法后,并没有一个快捷键可以快速给子类创建实现方法:,这 是对我键盘流操作的侮辱,我当然不能放过它.

## 接下来记录一下解决问题的思路

首先先确定怎么操作能相对快捷的创建实现方法

1.  光标落在需要重写的方法名上
2.  command + shift + a  激活 actions 窗口
3.  输入 implement method 
4.  回车

OK,有了一上5步 我们就开启宏录制,然后按步骤执行即可.

## 实操

### 开启宏录制

edit  ->   Marcos -> Start Macro Recording 

![e5414f16-fa29-11e9-a5e8-acde48001122](https://i.loli.net/2019/10/29/NdE7mrkapjsKRUZ.png )

开启成功后

右下角会提示

![710f8990-fa2a-11e9-98e2-acde48001122](https://i.loli.net/2019/10/29/HKuDV4FxzsGAZpC.png )

### 接下来录制操作:

按思路步骤  录制.

### 停止录制,并保存

上图,右下角开启成功标识内,红色按钮 就是 停止按钮.单击即可.

![d491188a-fa2a-11e9-a0fd-acde48001122](https://i.loli.net/2019/10/29/65Q93YFklRfVqOm.png )

输入宏的名字

### 宏设置快捷键

settings -> keymap -> Macros 

![0af3ceae-fa2b-11e9-a2f2-acde48001122](https://i.loli.net/2019/10/29/djTK7bS4CO6tma3.png )



## 效果展示

![test.gif](https://i.loli.net/2019/10/29/arvXU59hpluzHkN.gif)