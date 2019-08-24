## 设计模式总结

1. 设计先于实现

2. 不要只使用具体类来变成，要优先使用抽象类和接口来编程

3. 所谓设计模式其实就是通过组合或继承，向用户隐藏实现细节，直白的说，就是给用户一个方法，让他调用，不同设计模式有不同的内部实现细节。

4. 类一旦使用其他类的类名，就意味着该类与其他类紧密地耦合在一起。

5. 只有不知道子类才能替换。保证可替换性

6. 设计模式不是必须的，使用要斟酌，小心过度设计

   

### 目录：

1. [设计原则](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E8%AE%BE%E8%AE%A1%E5%8E%9F%E5%88%99.md)
2. [UML图](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/uml%E5%9B%BE.md)
3. 创建型模式
   1. [单例模式*](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E5%8D%95%E4%BE%8B%E6%A8%A1%E5%BC%8F.md)
   2. [工厂模式*](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E6%96%B9%E6%B3%95%E5%B7%A5%E5%8E%82%E6%A8%A1%E5%BC%8F.md)
   3. [建造模式*](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E5%BB%BA%E9%80%A0%E6%A8%A1%E5%BC%8F.md)
   4. [原型模式](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E5%8E%9F%E5%9E%8B%E6%A8%A1%E5%BC%8F.md)
4. 结构型模式
   1. [代理模式*](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E4%BB%A3%E7%90%86%E6%A8%A1%E5%BC%8F.md)
   2. [装饰模式*](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E8%A3%85%E9%A5%B0%E5%99%A8%E6%A8%A1%E5%BC%8F.md)
   3. [门面模式*](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E5%A4%96%E8%A7%82%EF%BC%88%E9%97%A8%E9%9D%A2%EF%BC%89%E6%A8%A1%E5%BC%8F.md)
   4. [组合模式](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E7%BB%84%E5%90%88%E6%A8%A1%E5%BC%8F.md)
   5. [享元模式](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E4%BA%AB%E5%85%83%E6%A8%A1%E5%BC%8F.md)
   6. [适配器模式](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E9%80%82%E9%85%8D%E5%99%A8%E6%A8%A1%E5%BC%8F.md)
   7. [桥接模式](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E6%A1%A5%E6%8E%A5%E6%A8%A1%E5%BC%8F.md)
5. 行为型模式
   1. [策略模式*](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E7%AD%96%E7%95%A5%E6%A8%A1%E5%BC%8F.md)
   2. [责任链模式*](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E8%B4%A3%E4%BB%BB%E9%93%BE%E6%A8%A1%E5%BC%8F.md)
   3. [状态模式*](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E7%8A%B6%E6%80%81%E6%A8%A1%E5%BC%8F.md)
   4. [模板方法模式*](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E6%96%B9%E6%B3%95%E6%A8%A1%E6%9D%BF%E6%A8%A1%E5%BC%8F.md)
   5. [迭代器模式](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E8%BF%AD%E4%BB%A3%E5%99%A8%E6%A8%A1%E5%BC%8F.md)
   6. [观察者模式](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E8%A7%82%E5%AF%9F%E8%80%85%E6%A8%A1%E5%BC%8F.md)
   7. [命令模式](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E5%91%BD%E4%BB%A4%E6%A8%A1%E5%BC%8F.md)
   8. [中介模式](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E4%B8%AD%E4%BB%8B%E8%80%85%E6%A8%A1%E5%BC%8F.md)
   9. [备忘录模式](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E5%A4%87%E5%BF%98%E5%BD%95%E6%A8%A1%E5%BC%8F.md)
   10. [解释器模式](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E8%A7%A3%E9%87%8A%E5%99%A8%E6%A8%A1%E5%BC%8F.md)
   11. [访问者模式](https://github.com/a827871781/Java-notes/blob/master/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F/%E8%AE%BF%E9%97%AE%E8%80%85%E6%A8%A1%E5%BC%8F.md)

