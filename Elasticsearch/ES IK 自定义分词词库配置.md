## 配置词库

```shell
cd /home/elasticsearch/elasticsearch-6.3.2/config/analysis-ik/
#将custom 文件放入这个文件夹内
```

##  修改 ik 的配置文件

```shell
#先备份一个配置
cp IKAnalyzer.cfg.xml IKAnalyzer备份.cfg.xml

vim IKAnalyzer.cfg.xml
```

### IKAnalyzer.cfg.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE properties SYSTEM "http://java.sun.com/dtd/properties.dtd">  
<properties>  
	<comment>IK Analyzer 扩展配置</comment>
	<!--用户可以在这里配置自己的扩展字典 -->	
	<entry key="ext_dict">custom/mydict.dic;custom/single_word_low_freq.dic</entry> 	
	 <!--用户可以在这里配置自己的扩展停止词字典-->
	<entry key="ext_stopwords">custom/ext_stopword.dic</entry> 	
</properties>
```

## 重启 es，并查看是否启动


![de9cedf4-cef6-11e9-a8f2-acde48001122](https://i.loli.net/2019/09/04/qg8cdvW3FSPiI41.png )

