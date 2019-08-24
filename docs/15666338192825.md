```java
public static void main(String[] args) {
    int arr [] = {1, 2, 3};
    List ints = Arrays.asList(arr);
    System.out.println(ints.size());
    //结果 等于 1 基本类型转 整体转
    //由于Arrays.ArrayList参数为可变长泛型，
    // 而基本类型是无法泛型化的，所以它把int[] arr数组当成了一个泛型对象，所以集合中最终只有一个元素arr。
    String arr1 [] = {"A","B","C"};
    List<String> strings = Arrays.asList(arr1);
    arr1[1]= "E";
    strings.set(2, "F");
   System.out.println(Arrays.toString(arr1));
   //[A, E, F]
   System.out.println(strings.toString());
   //[A, E, F]
   // 由于asList产生的集合元素是直接引用作为参数的数组，所以当外部数组或集合改变时，
    // 数组和集合会同步变化，这在平时我们编码时可能产生莫名的问题。

    strings.add("G");
    strings.remove(0);
    //异常 UnsupportedOperationException
    //由于asList产生的集合并没有重写add,remove等方法，
    // 所以它会调用父类AbstractList的方法，而父类的方法中抛出的却是异常信息。

    //基础类型转换
    int arr2 [] = {1, 2, 3};
    List<Integer> list = Arrays.stream(arr2).boxed().collect(Collectors.toList());
    System.out.println(list.toString());
    //引用数组问题及改变集合问题
    String arr3 [] = {"A","B","C"};
    List<String> list3 = new ArrayList<>(Arrays.asList(arr3));
    arr3[1] = "E";
    list3.set(2, "F");
    System.out.println(Arrays.toString(arr3));
    System.out.println(list3.toString());
    list3.add("G");
    list3.remove(0);
    System.out.println(list3.toString());

}
```

