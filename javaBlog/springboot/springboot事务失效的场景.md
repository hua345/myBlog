## 1.Transactional注解标注方法修饰符为非public时，@Transactional注解将会不起作用

```java
@Component
public class TestServiceImpl {
    @Resource
    TestMapper testMapper;
    
    @Transactional
    void insertTestWrongModifier() {
        int re = testMapper.insert(new Test(10,20,30));
        if (re > 0) {
            throw new NeedToInterceptException("need intercept");
        }
        testMapper.insert(new Test(210,20,30));
    }
}
```

在同一个包内，新建调用对象，进行访问。

```java
@Component
public class InvokcationService {
    @Resource
    private TestServiceImpl testService;
    public void invokeInsertTestWrongModifier(){
        //调用@Transactional标注的默认访问符方法
        testService.insertTestWrongModifier();
    }
}
```

## 2.在类内部调用调用类内部@Transactional标注的方法，这种情况下也会导致事务不开启。

```java

@Component
public class TestServiceImpl implements TestService {
    @Resource
    TestMapper testMapper;
 
    @Transactional
    public void insertTestInnerInvoke() {
        //正常public修饰符的事务方法
        int re = testMapper.insert(new Test(10,20,30));
        if (re > 0) {
            throw new NeedToInterceptException("need intercept");
        }
        testMapper.insert(new Test(210,20,30));
    }
 
 
    public void testInnerInvoke(){
        //类内部调用@Transactional标注的方法。
        insertTestInnerInvoke();
    }
}
```

## 3.事务方法内部捕捉了异常，没有抛出新的异常，导致事务操作不会进行回滚。

```java

@Component
public class TestServiceImpl implements TestService {
    @Resource
    TestMapper testMapper;
 
    @Transactional
    public void insertTestCatchException() {
        try {
            int re = testMapper.insert(new Test(10,20,30));
            if (re > 0) {
                //运行期间抛异常
                throw new NeedToInterceptException("need intercept");
            }
            testMapper.insert(new Test(210,20,30));
        }catch (Exception e){
            System.out.println("i catch exception");
        }
    }
}
```