# @Transactional

`spring 2.1.7.RELEASE`

```java
public @interface Transactional {
    @AliasFor("transactionManager")
    String value() default "";

    @AliasFor("value")
    String transactionManager() default "";

    Propagation propagation() default Propagation.REQUIRED;

    Isolation isolation() default Isolation.DEFAULT;

    int timeout() default -1;

    boolean readOnly() default false;

    Class<? extends Throwable>[] rollbackFor() default {};

    String[] rollbackForClassName() default {};

    Class<? extends Throwable>[] noRollbackFor() default {};

    String[] noRollbackForClassName() default {};
}
```

## 事物传播行为

```java
// 如果有事务, 那么加入事务, 没有的话新建一个(默认情况下)
@Transactional(value = Transactional.TxType.REQUIRED)
// 容器不为这个方法开启事务
@Transactional(value = Transactional.TxType.NOT_SUPPORTED)
// 不管是否存在事务,都创建一个新的事务,原来的挂起,新的执行完毕,继续执行老的事务
@Transactional(value = Transactional.TxType.REQUIRES_NEW)
// 必须在一个已有的事务中执行,否则抛出异常
@Transactional(value = Transactional.TxType.MANDATORY)
// 必须在一个没有的事务中执行,否则抛出异常(与Propagation.MANDATORY相反)
@Transactional(value = Transactional.TxType.NEVER)
// 如果其他bean调用这个方法,在其他bean中声明事务,那就用事务.如果其他bean没有声明事务,那就不用事务.
@Transactional(value = Transactional.TxType.SUPPORTS)
```
