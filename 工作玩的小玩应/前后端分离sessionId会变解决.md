前端携带cookie
```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title> test</title>
</head>
<body>
	  <div id="app">
		<button  @click="test()"> test</button >
	  </div>
</body>
<script src="https://cdn.jsdelivr.net/npm/vue"></script>
<script src="https://unpkg.com/axios/dist/axios.min.js"></script>
<script>
    //此处很重要前端请求携带cookie
	axios.defaults.withCredentials=true;
	new Vue({
		el: '#app',
		methods:{
			test:function(){		
				axios.get('http://localhost:8080/test1')
				  .then(function (response) {
					
				  });
			}
		}
		
	})
</script>
</html>
```

后端配置跨域

```java
@Component
public class CorsFilter1 implements Filter {

    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain) throws IOException, ServletException {
        HttpServletResponse response = (HttpServletResponse) res;
        response.setHeader("Access-Control-Allow-Origin", "http://localhost:8080");
        response.setHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS, DELETE");
        response.setHeader("Access-Control-Max-Age", "3600");
        response.setHeader("Access-Control-Allow-Headers", "Content-type");
        response.setHeader("Access-Control-Allow-Credentials","true");
        chain.doFilter(req, res);
    }
}
```

