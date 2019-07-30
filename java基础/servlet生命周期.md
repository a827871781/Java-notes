### Servlet 的生命周期

1. 加载：容器通过类加载器使用 Servlet 类对应的文件来加载 Servlet

2. 创建：通过**调用 Servlet 的构造函数来创建一个 Servlet 实例**

3. 初始化：通过调用 Servlet 的 init () 方法来完成初始化工作，**这个方法是在 Servlet 已经被创建，但在向客户端提供服务之前调用。**

4. 处理客户请求：Servlet 创建后就可以处理请求，当有新的客户端请求时，Web 容器都会**创建一个新的线程**来处理该请求。接着调用 Servlet 的Service () 方法来响应客户端请求（Service 方法会根据请求的 method 属性来调用 doGet（）和 doPost（））

5. 卸载：**容器在卸载 Servlet 之前**需要调用 destroy () 方法，让 Servlet 释放其占用的资源。

