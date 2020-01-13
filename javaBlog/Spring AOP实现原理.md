### 参考

- [Spring AOP实现原理](https://www.cnblogs.com/puyangsky/p/6218925.html)

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
