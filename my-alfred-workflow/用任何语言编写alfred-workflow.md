标题说的可能有点夸张,但是通过我方法你可以用任意可以在命令行执行的语言编写alfred脚本

## 教程开始

### 第一步,找到你所用语言的绝对路径

以下用python为例

我的python 是用brew安装的  所以可以通过 brew list + 语言  来查找安装路径,

![9ec7b75a-0c2b-11ea-9b4a-acde48001122](https://i.loli.net/2019/11/21/rDPQ5oVSvYJ9bAE.png )

红色框便是我的python3 安装目录

### 第二步,编写脚本

```python
#!/usr/bin/python3
# encoding: utf-8
import json
def main():
    result = {"items": [{"title": "test - Python" }]}
    print(json.dumps(result))


if __name__ == '__main__':
    main()
```

### 第三步,alfred设置workflow

#### 新建一个空白工作流

![a8c5d056-0c2c-11ea-abf2-acde48001122](https://i.loli.net/2019/11/21/FhdR6awcyrj8Iez.png )

单击 + 号 后 在下拉列表内 选择 Blank Workflow   这一步就不截图了,截不到,懒得折腾.

选择 Blank Workflow 后 会提示如下框

![1ac66e18-0c2d-11ea-abc7-acde48001122](https://i.loli.net/2019/11/21/JshLME5CHZeUctR.png )



#### 设置worklow

创建好空白工作流后,可以右键单击选中 input => Script Filter

![edc1cad8-0c2d-11ea-8949-acde48001122](https://i.loli.net/2019/11/21/8cRaGjb9U6i7mL5.png )



这个玩意我知道的也不全.大概知道以上这些就差不多了.其他的可以自行搜索.

以上比较重要的部分就是script 部分:

```shell
/usr/local/Cellar/python/3.7.4_1/bin/python3  ~/testPython.py 
```

重点,命令和 文件 都得是绝对路径.

现在唤出 alfred  键入 t3  就可以 看到打印结果了.

![348e026a-0c2e-11ea-abd8-acde48001122](https://i.loli.net/2019/11/21/kwpDcBHaYFsPyTC.png )

上面是的没有命令行参数的做法.

#### 如果想要带参数,可以参考下面js demo  的方案.

#### 输出的内容格式要求:

1 2  都是可替换的.

```json
{
    "items": [
        {
            "title": " 1"
        },
        {
            "title": " 2"
        }
    ]
}
```





## 以下是我用各种语言写的demo

### java

![image-20191121151347559](/Users/syz/Library/Application Support/typora-user-images/image-20191121151347559.png)

java这个需要稍微注意一下,java命令  绝对路径会报错,我就先进入到根目录 ,在执行的命令,

![99d1aaa0-0c2e-11ea-88fc-acde48001122](https://i.loli.net/2019/11/21/cpk8rG4CjRhesgS.png )

### js

![ee26b848-0c2e-11ea-a5ea-acde48001122](https://i.loli.net/2019/11/21/bSuDgqcajUleAd5.png )

将参数转大写.

![0130030e-0c2f-11ea-b7fb-acde48001122](https://i.loli.net/2019/11/21/3ltvDGu1X7CZj8A.png )

```js
let str = process.argv[2].toUpperCase()
let msg = `{"items": [{"title": "${str}" }]}`
console.log(msg)
```

## 个人的应用

### 上传图片到sm图床,并转为markdown格式.

https://github.com/a827871781/other/blob/master/my-script/fileUpload.py

自动将剪切板内的图片上传至sm图床.不可以直接使用,图中绝对路径修改为.自己的路径就可以

![9a08610a-0f56-11ea-b718-acde48001122](https://i.loli.net/2019/11/25/yIWLN9VMDETwcFY.png )

#### alfre配置

![0e836534-0f57-11ea-81bd-acde48001122](https://i.loli.net/2019/11/25/wOQHmNIgBrEoxai.png )

```shell
#注意脚本位置.绝对路径
/usr/local/Cellar/python/3.7.4_1/bin/python3  ~/Documents/other/my-script/fileUpload.py 

```



#### 最终效果

![336da206-0f57-11ea-bd18-acde48001122](https://i.loli.net/2019/11/25/rlSBiVu2EkHwMtj.png )

### 将[]转为{}

这个是因为我在LeetCode  刷题时,用例数组 总是 用[]表示,而java的数组是{}.所以写此脚本.

https://github.com/a827871781/other/blob/master/my-script/replaceStr.py

#### alfred

```shell
/usr/local/Cellar/python/3.7.4_1/bin/python3  ~/Documents/other/my-script/replaceStr.py 
```

#### 最终效果

略

