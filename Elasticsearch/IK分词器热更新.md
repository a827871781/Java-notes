# 热更新方案

第一种：修改 ik 分词器源码，然后手动支持从 mysql 中每隔一定时间，自动加载新的词库
第二种：基于 ik 分词器原生支持的热更新方案，部署一个 web 服务器，提供一个 http 接口，通过 modified 和 tag 两个 http 响应头，来提供词语的热更新

第一种方案是比较常用的，第二种呢 ik git 官方社区都不建议采用,

本次也是选择了第一种方案.我es 的版本为6.3.2,

## 下载源码

```shell
git clone https://github.com/medcl/elasticsearch-analysis-ik.git
```

### 切换版本

```shell
cd elasticsearch-analysis-ik
#这里是es 的版本
git checkout 6.3.2


```



## 修改源码

### 在 pom 中加入 mysql 的依赖

```xml
<!-- mysql -->
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>6.0.6</version>
</dependency>
```

### 配置 mysql 的连接

在 config 目录下创建一个**jdbc-reload.properties** 文件

```properties
jdbc.url=jdbc:mysql://localhost:3306/my_ik_word?allowMultiQueries=true&autoReconnect=true&useUnicode=true&characterEncoding=utf-8&serverTimezone=GMT
jdbc.user=root
jdbc.password=123456
# 更新词库的语句
jdbc.reload.sql=select word from hot_words
# 更新停用词的语句
jdbc.reload.stopword.sql=select stop_word as word from hot_stop_words
# 隔多少时间去更新一次  单位是秒
jdbc.reload.interval=10
```

### 新建一个线程

run 方法中调用 Dictionary 类的 reLoadMainDict () 方法，就是让他去重新加载词典

```java
package org.wltea.analyzer.dic;

public class HotDicReloadThread implements Runnable {
    private int sheepTime;

    public HotDicReloadThread(int sheepTime) {
        this.sheepTime = sheepTime;
    }


    private static final Logger logger = ESLoggerFactory.getLogger(HotDicReloadThread.class.getName());

    @Override
    public void run() {
        while (true){
            
            logger.info("-------reload hot dic from mysql--------");
            Dictionary.getSingleton().reLoadSQLDict();
            
            try {
                TimeUnit.SECONDS.sleep(sheepTime);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
```

### Dictionary 类中，加入 mysql 驱动类

```java
// prop用来获取上面的properties配置文件
private static Properties prop = new Properties();

static {
	try {
		Class.forName("com.mysql.jdbc.Driver");
	} catch (ClassNotFoundException e) {
		logger.error("error", e);
	}
}
```

### 在Dictionary类initial () 方法中，启动刚刚创建的线程

```java
/**
 * 词典初始化 由于IK Analyzer的词典采用Dictionary类的静态方法进行词典初始化
 * 只有当Dictionary类被实际调用时，才会开始载入词典， 这将延长首次分词操作的时间 该方法提供了一个在应用加载阶段就初始化字典的手段
 * 
 * @return Dictionary
 */
public static synchronized Dictionary initial(Configuration cfg) {
	if (singleton == null) {
		synchronized (Dictionary.class) {
			if (singleton == null) {

				singleton = new Dictionary(cfg);
				singleton.loadMainDict();
				singleton.loadSurnameDict();
				singleton.loadQuantifierDict();
				singleton.loadSuffixDict();
				singleton.loadPrepDict();
				singleton.loadStopWordDict();
//---------------------------这里-----------------------------
                		int reload = Integer.valueOf(prop.getProperty("jdbc.reload.interval")) ;
				// 执行更新词库的线程
					new Thread(new HotDicReloadThread(reload)).start();
                
//--------------------------------------------------------

				if(cfg.isEnableRemoteDict()){
					// 建立监控线程
					for (String location : singleton.getRemoteExtDictionarys()) {
						// 10 秒是初始延迟可以修改的 60是间隔时间 单位秒
						pool.scheduleAtFixedRate(new Monitor(location), 10, 60, TimeUnit.SECONDS);
					}
					for (String location : singleton.getRemoteExtStopWordDictionarys()) {
						pool.scheduleAtFixedRate(new Monitor(location), 10, 60, TimeUnit.SECONDS);
					}
				}

				return singleton;
			}
		}
	}
	return singleton;
}
```

### 在Dictionary添加一个 loadMySqlExtDict () 方法

```java
/**
 * 从mysql中加载热更新词典
 */
private void loadMySqlExtDict(){
		Connection connection = null;
		Statement statement = null;
		ResultSet resultSet = null;

		try {
			Path file = PathUtils.get(getDictRoot(),"jdbc-reload.properties");
			prop.load(new FileInputStream(file.toFile()));

			logger.info("-------jdbc-reload.properties-------");

			String sql = prop.getProperty("jdbc.reload.sql");
			logger.info("------- query hot dict from mysql, sql:{}-------", sql);
			String url = prop.getProperty("jdbc.url");
			String user = prop.getProperty("jdbc.user");
			String password = prop.getProperty("jdbc.password");
			logger.info("------- jdbc.url:{}-------", url);
			logger.info("------- jdbc.user:{}-------", user);
			logger.info("------- jdbc.password:{}-------", password);

			// 建立mysql连接
			connection = DriverManager.getConnection(url,user,password);

			// 执行查询
			statement = connection.createStatement();
			resultSet = statement.executeQuery(sql);

			// 循环输出查询啊结果,添加到Main.dict中去
			while (resultSet.next()) {
				String theWord = resultSet.getString("word");
				logger.info("------hot word from mysql:{}------", theWord);
				// 加到mainDict里面
				_MainDict.fillSegment(theWord.trim().toCharArray());
			}
		} catch (Exception e) {
			logger.error("error", e);
		} finally {
			try {
				if (resultSet != null) {
					resultSet.close();
				}
				if (statement != null) {
					statement.close();
				}
				if (connection != null) {
					connection.close();
				}
			} catch (SQLException e){
				logger.error("error", e);
			}
		}
	}
```

### 在Dictionary中loadMainDict () 方法最后，调用loadMySqlExtDict这个方法

```java
/**
 * 加载主词典及扩展词典
 */
private void loadMainDict() {
   // 建立一个主词典实例
   _MainDict = new DictSegment((char) 0);

   // 读取主词典文件
   Path file = PathUtils.get(getDictRoot(), Dictionary.PATH_DIC_MAIN);
   loadDictFile(_MainDict, file, false, "Main Dict");
   // 加载扩展词典
   this.loadExtDict();
   // 加载远程自定义词库
   this.loadRemoteExtDict();
   //----------------------这里--------------------------------------
   // 加载mysql词典
   this.loadMySqlExtDict();
   //------------------------------------------------------------
}
```

### 在Dictionary添加 loadMySqlStopwordDict () 方法，用来从 mysql 中获取停用词

```java
/**
 * 从mysql中加载停用词
 */
private void loadMySqlStopwordDict(){
	Connection conn = null;
	Statement stmt = null;
	ResultSet rs = null;

	try {
		Path file = PathUtils.get(getDictRoot(), "jdbc-reload.properties");
		prop.load(new FileInputStream(file.toFile()));

		logger.info("-------jdbc-reload.properties-------");
		for(Object key : prop.keySet()) {
			logger.info("-------key:{}", prop.getProperty(String.valueOf(key)));
		}

		logger.info("-------query hot stopword dict from mysql, sql:{}",props.getProperty("jdbc.reload.stopword.sql"));

		conn = DriverManager.getConnection(
				prop.getProperty("jdbc.url"),
				prop.getProperty("jdbc.user"),
				prop.getProperty("jdbc.password"));
		stmt = conn.createStatement();
		rs = stmt.executeQuery(prop.getProperty("jdbc.reload.stopword.sql"));

		while(rs.next()) {
			String theWord = rs.getString("word");
			logger.info("------- hot stopword from mysql: {}", theWord);
			_StopWords.fillSegment(theWord.trim().toCharArray());
		}

		Thread.sleep(Integer.valueOf(String.valueOf(prop.get("jdbc.reload.interval"))));
	} catch (Exception e) {
		logger.error("error", e);
	} finally {
		try {
			if(rs != null) {
				rs.close();
			}
			if(stmt != null) {
				stmt.close();
			}
			if(conn != null) {
				conn.close();
			}
		} catch (SQLException e){
			logger.error("error:{}", e);
		}

	}
}
```



### 在 loadStopWordDict () 方法最后，调用上面的更新停用词的方法

```java
//这个我没加 暂时没用到
// 从mysql中加载停用词
this.loadMySqlStopwordDict();

```

### 创建线程所用的Dictionary类reLoadSQLDict方法

```java
public void reLoadSQLDict() {
   this.loadMySqlExtDict();
    //这个看你用不用停词
   //this.loadMySqlStopwordDict();
}
```

### maven 打包项目

```shell
mvn clean package -DskipTests
```

## 数据库

### 词库表

```sql
CREATE TABLE `hot_words` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `word` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '词语',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
```

### 停用词库表

```sql
CREATE TABLE `hot_stop_words` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `stop_word` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '停用词',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
```



## 服务器配置

### Ik替换



```shell
#将打包完成后，在项目目录的 target\releases 路径下面有个压缩包解压并找到elasticsearch-analysis-ik-6.3.0.jar 文件,将elasticsearch-analysis-ik-6.3.0.jar 和mysql 驱动包丢进去
# 不要在意6.3.0 ,直接用.没关系
cd /home/elasticsearch/elasticsearch-6.3.2/plugins/analysis-ik/

#将config/jdbc-reload.properties 文件上传到 /home/elasticsearch/elasticsearch-6.3.2/config/analysis-ik/


```



### 修改jre安全策略文件

```shell
#${java_home}  说的是系统的java路径.
cd /${java_home}/jre/lib/security
vim java.policy
#增加如下三行代码
permission java.net.SocketPermission "*","connect,resolve";
permission java.lang.RuntimePermission "createClassLoader";
permission java.lang.RuntimePermission "getClassLoader";

```

### 启动es

看到打印如下信息 那就代表成功了.

![38acca4a-dab3-11e9-b04e-acde48001122](https://i.loli.net/2019/09/19/kVf1GgM6aOvlU5z.png )





### 百度云下载

链接:https://pan.baidu.com/s/1f6p92bRpP5ioVaSkz3N5fg  密码:414u



### 如果懒得改可以直接替换Dictionary类

```java
/**
 * IK 中文分词  版本 5.0
 * IK Analyzer release 5.0
 *
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * 源代码由林良益(linliangyi2005@gmail.com)提供
 * 版权声明 2012，乌龙茶工作室
 * provided by Linliangyi and copyright 2012 by Oolong studio
 *
 *
 */
package org.wltea.analyzer.dic;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.file.attribute.BasicFileAttributes;
import java.nio.file.Files;
import java.nio.file.FileVisitResult;
import java.nio.file.Path;
import java.nio.file.SimpleFileVisitor;
import java.security.AccessController;
import java.security.PrivilegedAction;
import java.sql.*;
import java.util.*;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.elasticsearch.SpecialPermission;
import org.elasticsearch.common.io.PathUtils;
import org.elasticsearch.common.logging.ESLoggerFactory;
import org.elasticsearch.plugin.analysis.ik.AnalysisIkPlugin;
import org.wltea.analyzer.cfg.Configuration;
import org.apache.logging.log4j.Logger;


/**
 * 词典管理类,单子模式
 */
public class Dictionary {

	/*
	 * 词典单子实例
	 */
	private static Dictionary singleton;

	private DictSegment _MainDict;

	private DictSegment _SurnameDict;

	private DictSegment _QuantifierDict;

	private DictSegment _SuffixDict;

	private DictSegment _PrepDict;

	private DictSegment _StopWords;

	/**
	 * 配置对象
	 */
	private Configuration configuration;

	private static final Logger logger = ESLoggerFactory.getLogger(Monitor.class.getName());

	private static ScheduledExecutorService pool = Executors.newScheduledThreadPool(1);

	public static final String PATH_DIC_MAIN = "main.dic";
	public static final String PATH_DIC_SURNAME = "surname.dic";
	public static final String PATH_DIC_QUANTIFIER = "quantifier.dic";
	public static final String PATH_DIC_SUFFIX = "suffix.dic";
	public static final String PATH_DIC_PREP = "preposition.dic";
	public static final String PATH_DIC_STOP = "stopword.dic";

	private final static  String FILE_NAME = "IKAnalyzer.cfg.xml";
	private final static  String EXT_DICT = "ext_dict";
	private final static  String REMOTE_EXT_DICT = "remote_ext_dict";
	private final static  String EXT_STOP = "ext_stopwords";
	private final static  String REMOTE_EXT_STOP = "remote_ext_stopwords";

	private Path conf_dir;
	private Properties props;

	// prop用来获取上面的properties配置文件
	private static Properties prop = new Properties();

	static {
		try {
			Class.forName("com.mysql.jdbc.Driver");
		} catch (ClassNotFoundException e) {
			logger.error("error", e);
		}
	}


	private Dictionary(Configuration cfg) {
		this.configuration = cfg;
		this.props = new Properties();
		this.conf_dir = cfg.getEnvironment().configFile().resolve(AnalysisIkPlugin.PLUGIN_NAME);
		Path configFile = conf_dir.resolve(FILE_NAME);

		InputStream input = null;
		try {
			logger.info("try load config from {}", configFile);
			input = new FileInputStream(configFile.toFile());
		} catch (FileNotFoundException e) {
			conf_dir = cfg.getConfigInPluginDir();
			configFile = conf_dir.resolve(FILE_NAME);
			try {
				logger.info("try load config from {}", configFile);
				input = new FileInputStream(configFile.toFile());
			} catch (FileNotFoundException ex) {
				// We should report origin exception
				logger.error("ik-analyzer", e);
			}
		}
		if (input != null) {
			try {
				props.loadFromXML(input);
			} catch (InvalidPropertiesFormatException e) {
				logger.error("ik-analyzer", e);
			} catch (IOException e) {
				logger.error("ik-analyzer", e);
			}
		}
	}

	public String getProperty(String key){
		if(props!=null){
			return props.getProperty(key);
		}
		return null;
	}
	/**
	 * 词典初始化 由于IK Analyzer的词典采用Dictionary类的静态方法进行词典初始化
	 * 只有当Dictionary类被实际调用时，才会开始载入词典， 这将延长首次分词操作的时间 该方法提供了一个在应用加载阶段就初始化字典的手段
	 * 
	 * @return Dictionary
	 */
	public static synchronized Dictionary initial(Configuration cfg) {
		if (singleton == null) {
			synchronized (Dictionary.class) {
				if (singleton == null) {

					singleton = new Dictionary(cfg);
					singleton.loadMainDict();
					singleton.loadSurnameDict();
					singleton.loadQuantifierDict();
					singleton.loadSuffixDict();
					singleton.loadPrepDict();
					singleton.loadStopWordDict();


//---------------------------这里-----------------------------
					int reload = Integer.valueOf(prop.getProperty("jdbc.reload.interval")) ;
					// 执行更新词库的线程
					new Thread(new HotDicReloadThread(reload)).start();

//--------------------------------------------------------

					if(cfg.isEnableRemoteDict()){
						// 建立监控线程
						for (String location : singleton.getRemoteExtDictionarys()) {
							// 10 秒是初始延迟可以修改的 60是间隔时间 单位秒
							pool.scheduleAtFixedRate(new Monitor(location), 10, 60, TimeUnit.SECONDS);
						}
						for (String location : singleton.getRemoteExtStopWordDictionarys()) {
							pool.scheduleAtFixedRate(new Monitor(location), 10, 60, TimeUnit.SECONDS);
						}
					}

					return singleton;
				}
			}
		}
		return singleton;
	}


	/**
	 * 从mysql中加载热更新词典
	 */
	private void loadMySqlExtDict(){
		Connection connection = null;
		Statement statement = null;
		ResultSet resultSet = null;

		try {
			Path file = PathUtils.get(getDictRoot(),"jdbc-reload.properties");
			prop.load(new FileInputStream(file.toFile()));

			logger.info("-------jdbc-reload.properties-------");

			String sql = prop.getProperty("jdbc.reload.sql");
			logger.info("------- query hot dict from mysql, sql:{}-------", sql);
			String url = prop.getProperty("jdbc.url");
			String user = prop.getProperty("jdbc.user");
			String password = prop.getProperty("jdbc.password");
			logger.info("------- jdbc.url:{}-------", url);
			logger.info("------- jdbc.user:{}-------", user);
			logger.info("------- jdbc.password:{}-------", password);

			// 建立mysql连接
			connection = DriverManager.getConnection(url,user,password);

			// 执行查询
			statement = connection.createStatement();
			resultSet = statement.executeQuery(sql);

			// 循环输出查询啊结果,添加到Main.dict中去
			while (resultSet.next()) {
				String theWord = resultSet.getString("word");
				logger.info("------hot word from mysql:{}------", theWord);
				// 加到mainDict里面
				_MainDict.fillSegment(theWord.trim().toCharArray());
			}
		} catch (Exception e) {
			logger.error("error", e);
		} finally {
			try {
				if (resultSet != null) {
					resultSet.close();
				}
				if (statement != null) {
					statement.close();
				}
				if (connection != null) {
					connection.close();
				}
			} catch (SQLException e){
				logger.error("error", e);
			}
		}
	}

	private List<String> walkFileTree(List<String> files, Path path) {
		if (Files.isRegularFile(path)) {
			files.add(path.toString());
		} else if (Files.isDirectory(path)) try {
			Files.walkFileTree(path, new SimpleFileVisitor<Path>() {
				@Override
				public FileVisitResult visitFile(Path file, BasicFileAttributes attrs) {
					files.add(file.toString());
					return FileVisitResult.CONTINUE;
				}
				@Override
				public FileVisitResult visitFileFailed(Path file, IOException e) {
					logger.error("[Ext Loading] listing files", e);
					return FileVisitResult.CONTINUE;
				}
			});
		} catch (IOException e) {
			logger.error("[Ext Loading] listing files", e);
		} else {
			logger.warn("[Ext Loading] file not found: " + path);
		}
		return files;
	}

	private void loadDictFile(DictSegment dict, Path file, boolean critical, String name) {
		try (InputStream is = new FileInputStream(file.toFile())) {
			BufferedReader br = new BufferedReader(
					new InputStreamReader(is, "UTF-8"), 512);
			String word = br.readLine();
			if (word != null) {
				if (word.startsWith("\uFEFF"))
					word = word.substring(1);
				for (; word != null; word = br.readLine()) {
					word = word.trim();
					if (word.isEmpty()) continue;
					dict.fillSegment(word.toCharArray());
				}
			}
		} catch (FileNotFoundException e) {
			logger.error("ik-analyzer: " + name + " not found", e);
			if (critical) throw new RuntimeException("ik-analyzer: " + name + " not found!!!", e);
		} catch (IOException e) {
			logger.error("ik-analyzer: " + name + " loading failed", e);
		}
	}

	public List<String> getExtDictionarys() {
		List<String> extDictFiles = new ArrayList<String>(2);
		String extDictCfg = getProperty(EXT_DICT);
		if (extDictCfg != null) {

			String[] filePaths = extDictCfg.split(";");
			for (String filePath : filePaths) {
				if (filePath != null && !"".equals(filePath.trim())) {
					Path file = PathUtils.get(getDictRoot(), filePath.trim());
					walkFileTree(extDictFiles, file);

				}
			}
		}
		return extDictFiles;
	}

	public List<String> getRemoteExtDictionarys() {
		List<String> remoteExtDictFiles = new ArrayList<String>(2);
		String remoteExtDictCfg = getProperty(REMOTE_EXT_DICT);
		if (remoteExtDictCfg != null) {

			String[] filePaths = remoteExtDictCfg.split(";");
			for (String filePath : filePaths) {
				if (filePath != null && !"".equals(filePath.trim())) {
					remoteExtDictFiles.add(filePath);

				}
			}
		}
		return remoteExtDictFiles;
	}

	public List<String> getExtStopWordDictionarys() {
		List<String> extStopWordDictFiles = new ArrayList<String>(2);
		String extStopWordDictCfg = getProperty(EXT_STOP);
		if (extStopWordDictCfg != null) {

			String[] filePaths = extStopWordDictCfg.split(";");
			for (String filePath : filePaths) {
				if (filePath != null && !"".equals(filePath.trim())) {
					Path file = PathUtils.get(getDictRoot(), filePath.trim());
					walkFileTree(extStopWordDictFiles, file);

				}
			}
		}
		return extStopWordDictFiles;
	}

	public List<String> getRemoteExtStopWordDictionarys() {
		List<String> remoteExtStopWordDictFiles = new ArrayList<String>(2);
		String remoteExtStopWordDictCfg = getProperty(REMOTE_EXT_STOP);
		if (remoteExtStopWordDictCfg != null) {

			String[] filePaths = remoteExtStopWordDictCfg.split(";");
			for (String filePath : filePaths) {
				if (filePath != null && !"".equals(filePath.trim())) {
					remoteExtStopWordDictFiles.add(filePath);

				}
			}
		}
		return remoteExtStopWordDictFiles;
	}

	public String getDictRoot() {
		return conf_dir.toAbsolutePath().toString();
	}


	/**
	 * 获取词典单子实例
	 * 
	 * @return Dictionary 单例对象
	 */
	public static Dictionary getSingleton() {
		if (singleton == null) {
			throw new IllegalStateException("词典尚未初始化，请先调用initial方法");
		}
		return singleton;
	}


	/**
	 * 批量加载新词条
	 * 
	 * @param words
	 *            Collection<String>词条列表
	 */
	public void addWords(Collection<String> words) {
		if (words != null) {
			for (String word : words) {
				if (word != null) {
					// 批量加载词条到主内存词典中
					singleton._MainDict.fillSegment(word.trim().toCharArray());
				}
			}
		}
	}

	/**
	 * 批量移除（屏蔽）词条
	 */
	public void disableWords(Collection<String> words) {
		if (words != null) {
			for (String word : words) {
				if (word != null) {
					// 批量屏蔽词条
					singleton._MainDict.disableSegment(word.trim().toCharArray());
				}
			}
		}
	}

	/**
	 * 检索匹配主词典
	 * 
	 * @return Hit 匹配结果描述
	 */
	public Hit matchInMainDict(char[] charArray) {
		return singleton._MainDict.match(charArray);
	}

	/**
	 * 检索匹配主词典
	 * 
	 * @return Hit 匹配结果描述
	 */
	public Hit matchInMainDict(char[] charArray, int begin, int length) {
		return singleton._MainDict.match(charArray, begin, length);
	}

	/**
	 * 检索匹配量词词典
	 * 
	 * @return Hit 匹配结果描述
	 */
	public Hit matchInQuantifierDict(char[] charArray, int begin, int length) {
		return singleton._QuantifierDict.match(charArray, begin, length);
	}

	/**
	 * 从已匹配的Hit中直接取出DictSegment，继续向下匹配
	 * 
	 * @return Hit
	 */
	public Hit matchWithHit(char[] charArray, int currentIndex, Hit matchedHit) {
		DictSegment ds = matchedHit.getMatchedDictSegment();
		return ds.match(charArray, currentIndex, 1, matchedHit);
	}

	/**
	 * 判断是否是停止词
	 * 
	 * @return boolean
	 */
	public boolean isStopWord(char[] charArray, int begin, int length) {
		return singleton._StopWords.match(charArray, begin, length).isMatch();
	}

	/**
	 * 加载主词典及扩展词典
	 */
	private void loadMainDict() {
		// 建立一个主词典实例
		_MainDict = new DictSegment((char) 0);

		// 读取主词典文件
		Path file = PathUtils.get(getDictRoot(), Dictionary.PATH_DIC_MAIN);
		loadDictFile(_MainDict, file, false, "Main Dict");
		// 加载扩展词典
		this.loadExtDict();
		// 加载远程自定义词库
		this.loadRemoteExtDict();
		//----------------------这里--------------------------------------
		// 加载mysql词典
		this.loadMySqlExtDict();
		//------------------------------------------------------------
	}


	/**
	 * 从mysql中加载停用词
	 */
	private void loadMySqlStopwordDict(){
		Connection conn = null;
		Statement stmt = null;
		ResultSet rs = null;

		try {
			Path file = PathUtils.get(getDictRoot(), "jdbc-reload.properties");
			prop.load(new FileInputStream(file.toFile()));

			logger.info("-------jdbc-reload.properties-------");
			for(Object key : prop.keySet()) {
				logger.info("-------key:{}", prop.getProperty(String.valueOf(key)));
			}

			logger.info("-------query hot stopword dict from mysql, sql:{}",props.getProperty("jdbc.reload.stopword.sql"));

			conn = DriverManager.getConnection(
					prop.getProperty("jdbc.url"),
					prop.getProperty("jdbc.user"),
					prop.getProperty("jdbc.password"));
			stmt = conn.createStatement();
			rs = stmt.executeQuery(prop.getProperty("jdbc.reload.stopword.sql"));

			while(rs.next()) {
				String theWord = rs.getString("word");
				logger.info("------- hot stopword from mysql: {}", theWord);
				_StopWords.fillSegment(theWord.trim().toCharArray());
			}

			Thread.sleep(Integer.valueOf(String.valueOf(prop.get("jdbc.reload.interval"))));
		} catch (Exception e) {
			logger.error("error", e);
		} finally {
			try {
				if(rs != null) {
					rs.close();
				}
				if(stmt != null) {
					stmt.close();
				}
				if(conn != null) {
					conn.close();
				}
			} catch (SQLException e){
				logger.error("error:{}", e);
			}

		}
	}

	/**
	 * 加载用户配置的扩展词典到主词库表
	 */
	private void loadExtDict() {
		// 加载扩展词典配置
		List<String> extDictFiles = getExtDictionarys();
		if (extDictFiles != null) {
			for (String extDictName : extDictFiles) {
				// 读取扩展词典文件
				logger.info("[Dict Loading] " + extDictName);
				Path file = PathUtils.get(extDictName);
				loadDictFile(_MainDict, file, false, "Extra Dict");
			}
		}
	}

	/**
	 * 加载远程扩展词典到主词库表
	 */
	private void loadRemoteExtDict() {
		List<String> remoteExtDictFiles = getRemoteExtDictionarys();
		for (String location : remoteExtDictFiles) {
			logger.info("[Dict Loading] " + location);
			List<String> lists = getRemoteWords(location);
			// 如果找不到扩展的字典，则忽略
			if (lists == null) {
				logger.error("[Dict Loading] " + location + "加载失败");
				continue;
			}
			for (String theWord : lists) {
				if (theWord != null && !"".equals(theWord.trim())) {
					// 加载扩展词典数据到主内存词典中
					logger.info(theWord);
					_MainDict.fillSegment(theWord.trim().toLowerCase().toCharArray());
				}
			}
		}

	}

	private static List<String> getRemoteWords(String location) {
		SpecialPermission.check();
		return AccessController.doPrivileged((PrivilegedAction<List<String>>) () -> {
			return getRemoteWordsUnprivileged(location);
		});
	}

	/**
	 * 从远程服务器上下载自定义词条
	 */
	private static List<String> getRemoteWordsUnprivileged(String location) {

		List<String> buffer = new ArrayList<String>();
		RequestConfig rc = RequestConfig.custom().setConnectionRequestTimeout(10 * 1000).setConnectTimeout(10 * 1000)
				.setSocketTimeout(60 * 1000).build();
		CloseableHttpClient httpclient = HttpClients.createDefault();
		CloseableHttpResponse response;
		BufferedReader in;
		HttpGet get = new HttpGet(location);
		get.setConfig(rc);
		try {
			response = httpclient.execute(get);
			if (response.getStatusLine().getStatusCode() == 200) {

				String charset = "UTF-8";
				// 获取编码，默认为utf-8
				if (response.getEntity().getContentType().getValue().contains("charset=")) {
					String contentType = response.getEntity().getContentType().getValue();
					charset = contentType.substring(contentType.lastIndexOf("=") + 1);
				}
				in = new BufferedReader(new InputStreamReader(response.getEntity().getContent(), charset));
				String line;
				while ((line = in.readLine()) != null) {
					buffer.add(line);
				}
				in.close();
				response.close();
				return buffer;
			}
			response.close();
		} catch (ClientProtocolException e) {
			logger.error("getRemoteWords {} error", e, location);
		} catch (IllegalStateException e) {
			logger.error("getRemoteWords {} error", e, location);
		} catch (IOException e) {
			logger.error("getRemoteWords {} error", e, location);
		}
		return buffer;
	}

	/**
	 * 加载用户扩展的停止词词典
	 */
	private void loadStopWordDict() {
		// 建立主词典实例
		_StopWords = new DictSegment((char) 0);

		// 读取主词典文件
		Path file = PathUtils.get(getDictRoot(), Dictionary.PATH_DIC_STOP);
		loadDictFile(_StopWords, file, false, "Main Stopwords");

		// 加载扩展停止词典
		List<String> extStopWordDictFiles = getExtStopWordDictionarys();
		if (extStopWordDictFiles != null) {
			for (String extStopWordDictName : extStopWordDictFiles) {
				logger.info("[Dict Loading] " + extStopWordDictName);

				// 读取扩展词典文件
				file = PathUtils.get(extStopWordDictName);
				loadDictFile(_StopWords, file, false, "Extra Stopwords");
			}
		}

		// 加载远程停用词典
		List<String> remoteExtStopWordDictFiles = getRemoteExtStopWordDictionarys();
		for (String location : remoteExtStopWordDictFiles) {
			logger.info("[Dict Loading] " + location);
			List<String> lists = getRemoteWords(location);
			// 如果找不到扩展的字典，则忽略
			if (lists == null) {
				logger.error("[Dict Loading] " + location + "加载失败");
				continue;
			}
			for (String theWord : lists) {
				if (theWord != null && !"".equals(theWord.trim())) {
					// 加载远程词典数据到主内存中
					logger.info(theWord);
					_StopWords.fillSegment(theWord.trim().toLowerCase().toCharArray());
				}
			}
		}
		//-------------------------------这里------------------------------------------
		// 从mysql中加载停用词
		//this.loadMySqlStopwordDict();

		//-------------------------------------------------------------------------
	}

	/**
	 * 加载量词词典
	 */
	private void loadQuantifierDict() {
		// 建立一个量词典实例
		_QuantifierDict = new DictSegment((char) 0);
		// 读取量词词典文件
		Path file = PathUtils.get(getDictRoot(), Dictionary.PATH_DIC_QUANTIFIER);
		loadDictFile(_QuantifierDict, file, false, "Quantifier");
	}

	private void loadSurnameDict() {
		_SurnameDict = new DictSegment((char) 0);
		Path file = PathUtils.get(getDictRoot(), Dictionary.PATH_DIC_SURNAME);
		loadDictFile(_SurnameDict, file, true, "Surname");
	}

	private void loadSuffixDict() {
		_SuffixDict = new DictSegment((char) 0);
		Path file = PathUtils.get(getDictRoot(), Dictionary.PATH_DIC_SUFFIX);
		loadDictFile(_SuffixDict, file, true, "Suffix");
	}

	private void loadPrepDict() {
		_PrepDict = new DictSegment((char) 0);
		Path file = PathUtils.get(getDictRoot(), Dictionary.PATH_DIC_PREP);
		loadDictFile(_PrepDict, file, true, "Preposition");
	}

	public void reLoadMainDict() {
		logger.info("重新加载词典...");
		// 新开一个实例加载词典，减少加载过程对当前词典使用的影响
		Dictionary tmpDict = new Dictionary(configuration);
		tmpDict.configuration = getSingleton().configuration;
		tmpDict.loadMainDict();
		tmpDict.loadStopWordDict();
		_MainDict = tmpDict._MainDict;
		_StopWords = tmpDict._StopWords;
		logger.info("重新加载词典完毕...");
	}


	public void reLoadSQLDict() {
		this.loadMySqlExtDict();
		//this.loadMySqlStopwordDict();
	}




}

```