## FastDFS介绍

### what is fastDFS ？

是一个开源的高性能分布式文件系统(DFS),用C写的。

主要功能:文件存储，文件同步和文件访问，以及高容量和负载均衡等。 

使用场景:

它主要解决了海量数据存储问题，特别适合以中小文件

建议范围：4KB < file_size <500MB）为载体的在线服务。支持线性扩容、负载均衡等。

## FastDFS从0到1

当前环境centos 7 

安装FastDFS环境(为了简化，这里安装单机版的) 


注意：fastDFS目前只能在linux系统下使用，所以需要装备linux系统或安装虚拟机。一定      要先给linux做网络配置，如果是虚拟机就桥接网络，设置静态内网地址和网关。


### 一. 简单配置

进入linux系统，先做一件事，修改hosts，将文件服务器的ip与域名映射(单机TrackerServer环境)，因为后面很多配置里面都需要去配置服务器地址，ip变了，就只需要修改hosts即可（此步可省）。

```shell
vi /etc/hosts
#增加如下一行，这是我的IP
192.168.1.160 file.xxx.com
#如果要本机访问虚拟机，在C:\Windows\System32\drivers\etc\hosts中同样增加一行
 
```

### 二. 下载安装 libfastcommon



libfastcommon是从 FastDFS 和 FastDHT 中提取出来的公共 C 函数库，基础环境。
1) 下载
`wget https://github.com/happyfish100/libfastcommon/archive/V1.0.7.tar.gz`

2) 解压

```shell
tar -zxvf V1.0.7.tar.gz

cd libfastcommon-1.0.7
```

3) 编译、安装
编译需要有gcc等插件
如果没有就下载

```shell
yum install gcc
yum install -y gcc-c++
yum install -y perl 
yum install -y pcre pcre-devel 
yum install -y zlib zlib-devel
yum install -y openssl openssl-devel
```

可以一次全下载(**推荐**)：

```shell
yum -y install zlib zlib-devel pcre pcre-devel gcc gcc-c++ openssl openssl-devel libevent libevent-devel perl unzip net-tools wget
```

```shell
./make.sh

./make.sh install
```



4)  libfastcommon.so安装到了/usr/lib64/libfastcommon.so，但是FastDFS主程序设置的lib目录是/usr/local/lib，所以就需要创建软链接。


```shell
ln -s /usr/lib64/libfastcommon.so /usr/local/lib/libfastcommon.so
ln -s /usr/lib64/libfastcommon.so /usr/lib/libfastcommon.so
ln -s /usr/lib64/libfdfsclient.so /usr/local/lib/libfdfsclient.so
ln -s /usr/lib64/libfdfsclient.so /usr/lib/libfdfsclient.so
```

### 三. 安装fastDFS 

```shell
#1) 下载fastDFS(或到https://github.com/happyfish100上下载最新版本)
wget https://github.com/happyfish100/fastdfs/archive/V5.05.tar.gz

#2) 解压
tar zxvf  V5.05.tar.gz
cd fastdfs-5.05
#3) 编译、安装
./make.sh
./make.sh install
#fastDFS安装好后，它的命令存在于：/usr/bin/ 目录下

```

4)  FastDFS 服务脚本设置的 bin 目录是 /usr/local/bin， 但实际命令安装在 /usr/bin/ 下
两种方式：

1.  是修改FastDFS 服务脚本中相应的命令路径，也就是把 /etc/init.d/fdfs_storaged 和 /etc/init.d/fdfs_tracker 两个脚本中的 /usr/local/bin 修改成 /usr/bin
2.  是建立 /usr/bin 到 /usr/local/bin 的软链接，本例用这种方式。　

```shell
ln -s /usr/bin/fdfs_trackerd   /usr/local/bin 
ln -s /usr/bin/fdfs_storaged   /usr/local/bin
ln -s /usr/bin/stop.sh         /usr/local/bin
ln -s /usr/bin/restart.sh      /usr/local/bin
 
```

### 四. 配置fastDFS的Tracker

#### 1.配置tracker.conf

进入 /etc/fdfs，复制 FastDFS 跟踪器样例配置文件 tracker.conf.sample，并重命名为 tracker.conf。

```shell
cd /etc/fdfs
cp tracker.conf.sample tracker.conf
vim tracker.conf
```

#### 2.编辑tracker.conf 

```shell
#写的是比较重要部分,没写 基本就不用改
# 配置文件是否不生效，false 为生效
disabled=false
# 提供服务的端口
port=22122
# Tracker 数据和日志目录地址(根目录必须存在,子目录会自动创建)
base_path=/opt/fastdfs/tracker
# HTTP 服务端口
http.server_port=80

```

#### 3.创建tracker基础数据目录，即base_path对应的目录

```shell
mkdir -p /opt/fastdfs/tracker
```



#### 4.防火墙中打开跟踪端口（默认的22122）


```shell
vim /etc/sysconfig/iptables
#添加如下端口行：
-A INPUT -m state --state NEW -m tcp -p tcp --dport 22122 -j ACCEPT
 
#关闭防火墙：
systemctl stop firewalld
#安装|更新服务：
yum install iptables-services
#启动iptables:
systemctl enable iptables
```

如果是云只需要在安全组里的入方向配置云的规则。

#### 5.启动Tracker

```shell
service fdfs_trackerd start
```

#### 6.设置Tracker开机启动

```shell
chkconfig fdfs_trackerd on
#或者：
vim /etc/rc.d/rc.local
#加入配置：
 
/etc/init.d/fdfs_trackerd start 
```

#### 7.tracker server 目录及文件结构 

```shell
#${base_path}
#  |__data
#  |   |__storage_groups.dat：存储分组信息
#  |   |__storage_servers.dat：存储服务器列表
#  |__logs
#  |   |__trackerd.log： tracker server 日志文件 
```



### 五. 配置fastDFS的Storage

#### 1.配置storage.conf

进入 /etc/fdfs 目录，复制 FastDFS 存储器样例配置文件 storage.conf.sample，并重命名为 storage.conf

```shell
cd /etc/fdfs
cp storage.conf.sample storage.conf
vim storage.conf
```

#### 2.编辑storage.conf

```shell
# 配置文件是否不生效，false 为生效
disabled=false 


 
# Storage 数据和日志目录地址(根目录必须存在，子目录会自动生成)
base_path=/opt/fastdfs/storage
 

# 如果不配置 store_path0，那它就和 base_path 对应的路径一样。
store_path0=/opt/fastdfs/file
 

 
# tracker_server 的列表 ，会主动连接 tracker_server
# 有多个 tracker server 时，每个 tracker server 写一行
tracker_server=file.xxx.com:22122


# 访问端口

http.server_port=80
```

 

#### 3.创建Storage基础数据目录

```shell
 mkdir -p /opt/fastdfs/storage
  
# 这是配置的store_path0路径
 mkdir -p /opt/fastdfs/file
```



#### 4. 防火墙中打开存储器端口(默认的 23000) ，

如果是云服务器只需要安全组里的入方向配置云服务器规则即可

```shell
 vim /etc/sysconfig/iptables
 
#添加如下端口行：
-A INPUT -m state --state NEW -m tcp -p tcp --dport 23000 -j ACCEPT
 
#重启防火墙：
 service iptables restart
 

```

#### 5. 启动 Storage

```shell
service fdfs_storaged start


#查看Storage和Tracker是否在通信：

/usr/bin/fdfs_monitor /etc/fdfs/storage.conf

```

![4fcd3036-1193-11ea-bb53-acde48001122](https://i.loli.net/2019/11/28/reNI6qpTKasjZ8E.png )



#### 6.设置 Storage 开机启动

```shell
chkconfig fdfs_storaged on
#或者：
#加入配置：
/etc/init.d/fdfs_storaged start
 
 
```

### 六. 文件上传测试

##### 1.修改 Tracker 服务器中的客户端配置文件 

```shell
 
cd /etc/fdfs
cp client.conf.sample client.conf
vim client.conf
#修改：
# Client 的数据和日志目录
base_path=/opt/fastdfs/client
# Tracker端口
tracker_server=file.xxx.com:22122
 
#再为它创建目录：
mkdir -p /opt/fastdfs/client
 

```



##### 2.上传测试

```shell
#随便整个图片过来，在linux内部执行如下命令上传a2.jpg图片
/usr/bin/fdfs_upload_file /etc/fdfs/client.conf a2.jpg
#上传成功后返回文件ID号
 
#删除上传文件:
/usr/bin/fdfs_delete_file /etc/fdfs/client.conf group1/M00/00/00/wKgBoFw4TE-AGKvMAAA0aLoff8c194.jpg
 
格式：group/存储目录/两级子目录/fileid.文件后缀名（由客户端指定，主要用于区分文件类型）拼接而成
 
```

![9e356d7e-11a2-11ea-88e0-acde48001122](https://i.loli.net/2019/11/28/mJgNLdrElsDAcGT.png )



### 七. 配置nginx

如果不需要http形式的访问，可以跳过它。
nginx只需要安装到StorageServer所在的服务器即可，用于访问文件。
如果是安在tracker上主要是为了：提供http反向代理、负载均衡及缓存服务。



 注：gcc、pcre-devel 、zlib、OpenSSL都要装全了，前面已经装全了。

#### 1.下载nginx

```shell
wget -c https://nginx.org/download/nginx-1.14.2.tar.gz
tar zxvf nginx-1.14.2.tar.gz
cd nginx-1.14.2
#使用默认配置
./configure

```

#### 2.编译、安装

```shell
make
make install
```

#### 3.启动nginx

```shell
cd /usr/local/nginx/sbin/
./nginx

#其它：
# ./nginx -s stop ，# ./nginx -s quit ， # ./nginx -s reload
```

#### 4.设置开机启动

```shell
vim /etc/rc.local
#添加一行：
/usr/local/nginx/sbin/nginx

# 设置执行权限
chmod 755 /etc/rc.d/rc.local

#查看ngin版本和模块：
/usr/local/nginx/sbin/nginx -V

```

#### 5.防火墙中打开nginx端口

```shell
#防火墙中打开nginx端口（默认的 80）
vim /etc/sysconfig/iptables
#在-A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT下
#添加如下端口行：
-A INPUT -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT

#重启防火墙：
service iptables restart
```

#### 6. 配置conf

```shell
#修改nginx.conf
vim /usr/local/nginx/conf/nginx.conf
 
#添加如下行，将 /group1/M00 映射到 /opt/fastdfs/file/data
location /group1/M00 {
    alias /opt/fastdfs/file/data;
}

# 重启nginx
/usr/local/nginx/sbin/nginx -s reload
 
# 在浏览器访问之前上传的图片、成功。
#http://x.x.x.x/group1/M00/00/00/wKgBoFw4NWaAIFQsAACgIuTmy1Q390.jpg
 

#外部访问只能用地址访问。如果内部能访问外部访问不了，一般是防火墙没设置好，vi /etc/sysconfig/iptables
#,比较 -A INPUT -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT是否有，然后再重新加载 #systemctl restart iptables.service
 
```

### 八. 访fastDFS配置nginx模块（非必须）

#### fastdfs-nginx-module 为啥安它？

FastDFS 通过 Tracker 服务器，将文件放在 Storage 服务器存储， 但是同组存储服务器之间需要进行文件复制， 有同步延迟的问题。如果就一个服务器，也不搞什么集群，不怕崩，可以略过此步。
假设 Tracker 服务器将文件上传到了 192.168.51.128，上传成功后文件 ID已经返回给客户端。
此时 FastDFS 存储集群机制会将这个文件同步到同组存储 192.168.51.129，在文件还没有复制完成的情况下，客户端如果用这个文件 ID 在 192.168.51.129 上取文件,就会出现文件无法访问的错误。
而 fastdfs-nginx-module 可以重定向文件链接到源服务器取文件，避免客户端由于复制延迟导致的文件无法访问错误。

#### 安装fastdfs-nginx-module

```sh
 # 下载 fastdfs-nginx-module、解压
# 这里为啥这么长一串呢，因为最新版的master与当前nginx有些版本问题。
wget https://github.com/happyfish100/fastdfs-nginx-module/archive/5e5f3566bbfa57418b5506aaefbe107a42c9fcb1.zip
 
#最新链接：https://codeload.github.com/happyfish100/fastdfs-nginx-module/zip/master
 
# 解压
 unzip 5e5f3566bbfa57418b5506aaefbe107a42c9fcb1.zip
 
# 重命名，如果是最新的就不用重命名了
 mv fastdfs-nginx-module-5e5f3566bbfa57418b5506aaefbe107a42c9fcb1  fastdfs-nginx-module-master
 


```

#### 配置nginx

```shell
#在nginx中添加模块
# 先停掉nginx服务
/usr/local/nginx/sbin/nginx -s stop

#进入解压包目录
cd /softpackages/nginx-1.12.1/

# 添加模块
./configure --add-module=../fastdfs-nginx-module-master/src
 
#重新编译、安装
 make && make install
#1) 如果出现致命错误等字样，改变两行 :vi fastdfs-nginx-module-master/src/config
#ngx_module_incs="/usr/include/fastdfs /usr/include/fastcommon/"

CORE_INCS="$CORE_INCS /usr/include/fastdfs /usr/include/fastcommon/"
#2) 再重新到nginx目录下，执行：
.configure
make & make install
#查看Nginx的模块:/usr/local/nginx/sbin/nginx -V

 

 
```

#### 配置mod_fastdfs.conf

```shell
# 复制 fastdfs-nginx-module 的配置文件到/etc/fdfs 目录， 并修改
cd /opt/software/fastdfs-nginx-module-master/src
cp mod_fastdfs.conf /etc/fdfs/
vi /etc/fdfs/mod_fastdfs.conf

# 连接超时时间
connect_timeout=10
# Tracker Server
tracker_server=file.kbz.com:22122

# StorageServer 默认端口
storage_server_port=23000

# 如果文件ID的uri中包含/group**，则要设置为true
url_have_group_name = true

# Storage 配置的store_path0路径，必须和storage.conf中的一致store_path0=/opt/fastdfs/file


# 复制FastDFS 的部分配置文件到/etc/fdfs 目录,
cd /opt/software/fastdfs-5.05/conf/
cp anti-steal.jpg http.conf mime.types /etc/fdfs/



 
#⑦ 在/ljzsg/fastdfs/file 文件存储目录下创建软连接，将其链接到实际存放数据的目录，单机版，这一步可以省略。
ln -s /opt/fastdfs/file/data/ /opt/fastdfs/file/data/M00 
 

#有打印pid字样就算成功：

 
#或许现在没看到什么效果，但如果多台机器再传个超大文件，就可以测试出来了，在分组机器未同步时，会重定向到有文件的那台机器。
```

#### 配置nginx转发规则

```shell
vim /usr/local/nginx/conf/nginx.conf

#在80端口添加：
location ~/group([0-9])/M00 {
    ngx_fastdfs_module;
}
#说明：listen 80 端口值是要与 /etc/fdfs/storage.conf 中的 http.server_port=80 (前面改成80了)相对应,
```

#### 创建软连接

```shell
# 在/ljzsg/fastdfs/file 文件存储目录下创建软连接，将其链接到实际存放数据的目录，单机版，这一步可以省略。
ln -s /opt/fastdfs/file/data/ /opt/fastdfs/file/data/M00 
```

#### 启动nginx

```shell
/usr/local/nginx/sbin/nginx
```





## JAVA文件操作

前面文件系统平台搭建好了，现在就要写客户端代码在系统中实现上传下载，这里只是简单的测试代码

### 1.新建一个springboot项目。加入fastdfs-client依赖

```xml
<dependency>
    <groupId>com.github.tobato</groupId>
    <artifactId>fastdfs-client</artifactId>
    <version>1.26.5</version>
</dependency>
```

```properties
#properties配置文件
#获取文件超时时间
fdfs.so-timeout = 30000
#连接超时时间
fdfs.connect-timeout = 20000
#图片压缩后宽度
fdfs.thumb-image.width = 150
#图片压缩收高度
fdfs.thumb-image.height = 150
#tracker配置
fdfs.tracker-list=39.105.198.140:22122
#前端获取url
fdfs.webServerUrl=
#上传最大10M
spring.servlet.multipart.max-file-size=10485760
spring.servlet.multipart.max-request-size=10485760
```



### 2.  建工具类

```java
@Data
public class FastDFSFile implements Serializable {

    private static final long serialVersionUID = 1L;

    private byte[] content;
    private String name;

    private String ext;

    private String length;


    public FastDFSFile(byte[] content, String ext) {

        this.content = content;

        this.ext = ext;
    }

    public FastDFSFile(byte[] content, String name, String ext) {
        this.content = content;
        this.name = name;
        this.ext = ext;
    }


    public FastDFSFile(byte[] content, String name, String ext, String length,

                       String author) {
        this.content = content;
        this.name = name;
        this.ext = ext;
        this.length = length;
    }


}}

 
```

 



 

**2)**  **工具类**

 

```java
/**

 \* **@author** Administrator

 \* **@type** 图片服务器的客户端

 */

@Component

public class FastDFSClient {

    private final Logger logger = LoggerFactory.getLogger(FastDFSClient.class);
    @Autowired
    private FastFileStorageClient storageClient;

    @Autowired
    private FdfsWebServer fdfsWebServer;

    /**
     * 上传文件
     * @param file 文件对象
     * @return 文件访问地址
     * @throws IOException
     */
    public String uploadFile(MultipartFile file) throws IOException {
        StorePath storePath = storageClient.uploadFile(file.getInputStream(),file.getSize(), FilenameUtils.getExtension(file.getOriginalFilename()),null);
        return getResAccessUrl(storePath);
    }


    /**
     * 上传文件
     * @param file 文件对象
     * @return 文件访问地址
     * @throws IOException
     */
    public String uploadFile(File file) throws IOException {
        FileInputStream inputStream = new FileInputStream (file);
        StorePath storePath = storageClient.uploadFile(inputStream,file.length(), FilenameUtils.getExtension(file.getName()),null);
        return getResAccessUrl(storePath);
    }

    /**
     * 将一段字符串生成一个文件上传
     * @param content 文件内容
     * @param fileExtension
     * @return
     */
    public String uploadFile(String content, String fileExtension) {
        byte[] buff = content.getBytes(Charset.forName("UTF-8"));
        ByteArrayInputStream stream = new ByteArrayInputStream(buff);
        StorePath storePath = storageClient.uploadFile(stream,buff.length, fileExtension,null);
        return getResAccessUrl(storePath);

    }

    // 封装图片完整URL地址
    private String getResAccessUrl(StorePath storePath) {
        String fileUrl = fdfsWebServer.getWebServerUrl() + storePath.getFullPath();
        return fileUrl;
    }
 
    /**
     * 删除文件
     * @param fileUrl 文件访问地址
     * @return
     */
    public void deleteFile(String fileUrl) {
        if (StringUtils.isEmpty(fileUrl)) {
            return;
        }
        try {
            StorePath storePath = StorePath.parseFromUrl(fileUrl);
            storageClient.deleteFile(storePath.getGroup(), storePath.getPath());
        } catch (FdfsUnsupportStorePathException e) {
            logger.warn(e.getMessage());
        }

```



### 3. Controller上传、删除

```java
@RestController

@RequestMapping("/file")
public class  FileController {

	@Autowired
	private FastDFSClient fastDFSClient;

	 @RequestMapping("/upload")
 	public String upload(MultipartFile file) {
	 Properties pro = new Properties();
	String appPath="F:\\img-test\\path.properties";

	 String path =null;
		try (FileOutputStream out =new FileOutputStream(appPath,true)){
			//上传，返回路径
			path = fastDFSClient.uploadFile(file);
			pro.put(file.getOriginalFilename(), path);
			 pro.store( out, null);
		 } catch (IOException e) {
			 e.printStackTrace();
        }
		return path;
    }


  @RequestMapping("/delete")
	public  String down(String path) {
    	fastDFSClient.deleteFile(path);
 			String appPath="F:\\img-test\\path.properties";

      try  (FileOutputStream out = new  FileOutputStream(appPath, false );
             FileInputStream in=new FileInputStream(appPath);)
        {

                Properties pro = new Properties();
                pro.load(in);
                pro.entrySet().forEach(x->{
          if (x.getValue()==path) 
            pro.remove(x.getKey()); 
          });
          pro.store(out, null);
        } catch (FileNotFoundException | IOException e) {
          e.printStackTrace();
        }   

        return "ok";
    } 

}

```

