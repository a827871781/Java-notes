### spring mvc 参数绑定

@RequestParam 参数必须存在，可以为空串 null。

@RequestBody json参数转换

```java
/**
 *包装类型：id可以不传，后台接受到null。
 *原始类型：id必须要传，否则报错
 */
@RequestMapping("/test")
@ResponseBody 
public ResponseData test(Integer id) {}
public ResponseData test(int id) {} 
```

#### list(简单类型)

```java
@RequestMapping("/test")
@ResponseBody 
public ResponseData test(@RequestParam List<Integer>ids) {}  
@RequestMapping("/test")
@ResponseBody
public ResponseData test(Integer[]ids) { }
//form表单 
<form action="${ctx}/test/test" method="post">   
    <input type="text" name="ids">    
    <input type="text" name="ids">    
    <input type="text" name="ids">    
    <input type="submit"> 
</form>  
// Ajax
var data = [];
data.push(1); 
$.ajax({  
    url: ctx + "/test/test",   
    traditional:true,//必要   
    data: {ids: data},    
    success: function (result) { 
    } 
}) 
```

#### list(pojo包含list)

```java
public class User{
    private String name;
    private String sex;
    private List<Post> posts;
    //get and set ...
}
@RequestMapping("/test")
@ResponseBody
public ResponseData test(User user) {}

<form action="${ctx}/test/test" method="post">
    <input type="text" name="userName" value="zhangsan">
    <input type="text" name="sex" value="123">
    <input type="text" name="posts[0].code" value="232"/>
    <input type="text" name="posts[0].name" value="ad"/>
    <input type="text" name="posts[1].code" value="ad"/>
    <input type="text" name="posts[1].name" value="232"/>
    <input type="submit">
</form>

var user={userName:"zhangsan",password:"123"};
user['posts[0].name']="ada";
user['posts[0].code']="ada";
user['posts[1].name']="ad";
user['posts[1].code']="ad2323a";
$.ajax({
    url: ctx + "/test/test",
    type:"post",
    contentType: "application/x-www-form-urlencoded",
    data:user,
    success: function (result) {
        alert(result);
    }
});
```



#### formdata类型(list (pojo包含list))

```java
this.formDate = new FormData()  
    let arr = [] 	
    for(let i = 0;i<10 ;i++){ 
        arr.push({'id':i+"id",'name':i+"name"}) 	
        this.formDate.append("generalBean["+i+"].id",i+"id") 	
        this.formDate.append("generalBean["+i+"].name",i+"name") 	
    }    
test(  this.formDate ).then(({data}) => {          }) 	
    @RequestMapping(value="test")
    public ResponseResult<BrandVo >test(BrandVo brandVo )  { 
    return ResponseResult.success(brandVo); 
} 	
@Data
public class BrandVo  {  
    private  GeneralBean[]   generalBean ;     
} 
export const test = (data) => {  
    return request({  
        url: request.adornUrl(channelService+`/brand/test`),  
        method: 'post',  
        headers:{'Content-Type':'multipart/form-data'}, 
        data:data,   
        paramsSerializer(data) {
            return qs.stringify(data)  
        } //应该是可以没有  qs  js 序列化的一个工具   }) }  
```



#### date类型

使用注解方式

绑定单个方法

对于传递参数为Date类型，可以在参数前添加@DateTimeFormat注解。如下：



```java
@RequestMapping("/test")
public void test(@DateTimeFormat(pattern="yyyy-MM-dd HH:mm:ss") Date date){} 

如果传递过来的是对象，可以在对象属性上添加注解。

@RequestMapping("/test") 
public void test(Person person){} 
Public class Person{  
    @DateTimeFormat(pattern="yyyy-MM-dd HH:mm:ss")   
    Private Date date;  
    Private String name; 
} 
```



参考：



<https://www.2cto.com/kf/201501/374062.html>



<https://docs.spring.io/spring/docs/current/spring-framework-reference/web.html#mvc-ann-initbinder>



枚举类型

mvc配置文件添加：

```java


 <!--枚举类型转化器-->

    <bean id="formattingConversionService"
          class="org.springframework.format.support.FormattingConversionServiceFactoryBean">
        <property name="converters">
            <set>
                <bean class="org.springframework.core.convert.support.StringToEnumConverterFactory"/>
            </set>
        </property>
    </bean>
```



参考：



Spring Boot绑定枚举类型参数



Spring MVC 自动为对象注入枚举类型



#### json格式对象

后台

```java
@RequestMapping(value = "introductionData", method = {RequestMethod.POST}) 
@ResponseBody 
public RestResult introductionData(@RequestBody SignData signData) { 
} 
public class SignData {   
    private ApplicationInformation applicationInformation;  
    private ApplyUserInformation applyUserInformation;  
    private StudentInformation studentInformation;   
    private List<VolunteerItem> volunteerItems;  
    private ResidencePermit residencePermit;   
    private List<Family> families;     //get and set ...
} 
//前台 
var data = {}
var applyUserInformation = { "applyName": APPLYNAME,"applyCardType": "0", "applyCardID": APPLYIDCARD,  "applyMobile": APPLYMOBILE }; 
var applicationInformation = {"live_address": nowaddress, "addressJZArea": addressJZArea,"schoolLevel": schoolLevel,  "schoolType": schoolType, "applyName": APPLYNAME,"contacts": contacts,"contactNumber": contactNumber }; 
var studentInformation = {     "cardType": cardType,     "cardID": cardID,     "studentName": studentName,     "studentType": studentType,     "studentType1": studentSpecialCase,     "isDisability": "0",     "studentCategory": "0",     "birthday":birthday,     "graduationschool":SchoolName,     "graduationclass":classNameinfo,     "applyName": APPLYNAME };
data["applyUserInformation"] = applyUserInformation; 
data["applicationInformation"] = applicationInformation;
data["studentInformation"] = studentInformation; 
$.ajax({    
    url: ctx + '/overseasData',   
    type: "post",   
    data: JSON.stringify(data),    
    contentType: "application/json;charset=utf-8",   
    success: function (result) {
        
    }
}) 
```

