# Spring AOP

## 参考

- [Spring AOP实现原理](https://www.cnblogs.com/puyangsky/p/6218925.html)

## 什么是AOP

`Aspect Oriented Programming` ，即面向切面编程。

- AOP是对面向对象编程的一个补充。
- 它的目的是将复杂的需求分解为不同的切面，将散布在系统中的公共功能集中解决。
- 它的实际含义是在运行时将代码切入到类的指定方法、指定位置上，将不同方法的同一个位置抽象为一个切面对象，并对该对象进行编程。

### 静态代理

```java
public interface IFruitService {
    /**
     * 获取水果
     * @return
     */
    public Fruit getFruit();
}
```

实现类

```java
public class FruitAppleServiceImpl implements IFruitService {
    /**
     * 获取水果
     *
     * @return
     */
    @Override
    public Fruit getFruit() {
        return new Apple("苹果");
    }
}
```
