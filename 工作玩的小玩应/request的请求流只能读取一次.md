# request的请求流只能读取一次解决

因为流对应的是数据，数据放在内存中，有的是部分放在内存中。read 一次标记一次当前位置（mark position），第二次 read 就从标记位置继续读（从内存中 copy）数据。 所以这就是为什么读了一次第二次是空了。 怎么让它不为空呢？只要 inputstream 中的 pos 变成 0 就可以重写读取当前内存中的数据。javaAPI 中有一个方法 public void reset() 这个方法就是可以重置 pos 为起始位置，但是不是所有的 IO 读取流都可以调用该方法！ServletInputStream 是不能调用 reset 方法，这就导致了只能调用一次 getInputStream ()。

##### 解决办法：

思路狸猫换太子

在一次请求中Fifle是比Interceptor要快的

利用Fifle就把流拿过来封装成自己的流，这样就想读多少次就读多少次！

1. 重写 HttpServletRequestWrapper 方法

   ```java
   public class RequestWrapper extends HttpServletRequestWrapper {
       private final String body;
   
       public RequestWrapper(HttpServletRequest request) {
           super(request);
           StringBuilder stringBuilder = new StringBuilder();
           BufferedReader bufferedReader = null;
           InputStream
                   inputStream = null;
           try {
               inputStream = request.getInputStream();
               if (inputStream != null) {
                   bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
                   char[] charBuffer = new char[128];
                   int bytesRead = -1;
                   while ((bytesRead = bufferedReader.read(charBuffer)) > 0) {
                       stringBuilder.append(charBuffer, 0, bytesRead);
                   }
               } else {
                   stringBuilder.append("");
               }
           } catch (IOException ex) {
   
           } finally {
               if (inputStream != null) {
                   try {
                       inputStream.close();
                   }
                   catch (IOException e) {
                       e.printStackTrace();
                   }
               }
               if (bufferedReader != null) {
                   try {
                       bufferedReader.close();
                   }
                   catch (IOException e) {
                       e.printStackTrace();
                   }
               }
           }
           body = stringBuilder.toString();
       }
   
       @Override
       public ServletInputStream getInputStream() throws IOException {
           final ByteArrayInputStream byteArrayInputStream = new ByteArrayInputStream(body.getBytes());
           ServletInputStream servletInputStream = new ServletInputStream() {
               @Override
               public boolean isFinished() {
                   return false;
               }
               @Override
               public boolean isReady() {
                   return false;
               }
               @Override
               public void setReadListener(ReadListener readListener) {
               }
               @Override
               public int read() throws IOException {
                   return byteArrayInputStream.read();
               }
           };
           return servletInputStream;
   
       }
   
       @Override
       public BufferedReader getReader() throws IOException {
           return new BufferedReader(new InputStreamReader(this.getInputStream()));
       }
   
       public String getBody() {
           return this.body;
       }
   
   }
   ```

2. 拦截器 LogInterceptor

   ```java
   @Component
   public class LogInterceptor extends HandlerInterceptorAdapter {
   
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        try {
            RequestWrapper requestWrapper = new RequestWrapper(request);
            String body = requestWrapper.getBody();
            System.out.println("LogInterceptor"+body);
            return true;
        }catch (Exception e){
            e.printStackTrace();
        }
        return false;
    }
    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView){
        //System.out.println("postHandle");
    }
   }
   ```

3. 过滤器 RepeatReadFilter类

   ```java
   @Component
   public class RepeatReadFilter implements Filter {
   
   
       public void init(FilterConfig filterConfig) throws ServletException {
   
       }
   
       @Override
       public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
               throws IOException, ServletException {
           ServletRequest requestWrapper = null;
           if(request instanceof HttpServletRequest) {
               requestWrapper = new RequestWrapper((HttpServletRequest) request);
           }
           //System.out.println("doFilter");
           if(requestWrapper == null) {
               chain.doFilter(request, response);
           } else {
               chain.doFilter(requestWrapper, response);
           }
       }
   
       @Override
       public void destroy() {
   
       }
   }
   ```

4. 加入拦截器和过滤器

   ```java
   @Component
   public class LoggerConfig {
       //日志拦截
       @Bean
       public WebMvcConfigurer mvcConfigurer() {
           return new WebMvcConfigurer() {
               @Override
               public void addInterceptors(InterceptorRegistry registry) {
                   registry.addInterceptor(new LogInterceptor());
               }
           };
       }
       @Bean
       public FilterRegistrationBean registFilter() {
           FilterRegistrationBean registration = new FilterRegistrationBean();
           registration.setFilter(new RepeatReadFilter());
           registration.addUrlPatterns("/app/*");
           registration.setName("UrlFilter");
           registration.setOrder(1);
           return registration;
       }
   }
   ```

   

