# package 的简单定义如下：

package 是一个为了方便管理组织 java 文件的目录结构，并防止不同 java 文件之间发生命名冲突而存在的一个 java 特性。不同 package 中的类的名字可以相同，只是在使用时要带上 package 的名称加以区分。

有如下代码:

```java
package com.micheal.test
 
public class Test {}
```

java 解释器会将 package 中的 **"."(点)** 解释为目录分隔符 **"/"**，也就是说该文件的目录结构为`..com/micheal/test/Test.java`

# import

import 就是在 java 文件开头的地方，先说明会用到那些类别。
接着我们就能在代码中只用类名指定某个类，也就是只称呼名字，不称呼他的姓。

##  java.lang无论写不写 都会被编译器自动填充

java.lang 包里面的类实在是太常太常太常用到了，几乎没有类不用它的，所以不管你有没有写 import java.lang，编译器都会自动帮你补上，也就是说编译器只要看到没有姓的类别，它就会自动去 lang 包里面查找。所以我们就不用特别去 import java.lang 了。

## import 的导入声明

-   单类型导入 
    （例:**import java.util.ArrayList;** ）

-   按需类型导入
    （例:**import java.util.*;**）

-    静态导入

    （例:**import static com.assignment.test.StaticFieldsClass.staticFunction;**）

## 按需类型导入是否会影响到Java 代码的执行效率 

**不会！**

import 的按需导入

```java
import java.util.*;

public class NeedImportTest {
    public static void main(String[] args) {
        ArrayList tList = new ArrayList();
    }
}
//编译之后的 class 文件 :

//import java.util.*被替换成import java.util.ArrayList
//即按需导入编译过程会替换成单类型导入。
import java.util.ArrayList;

public class NeedImportTest {
    public static void main(String[] args) {
        new ArrayList();
    }
}
```



具体使用按需导入  还是 单类型导入.在日常工作没啥区别.

但是如果往开源项目提交代码,记得要单类型导入.



