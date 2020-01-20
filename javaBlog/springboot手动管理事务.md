# 编程式的事务管理

spring支持编程式事务管理和声明式事务管理两种方式。

- 编程式事务管理使用`TransactionTemplate`或者直接使用底层的`PlatformTransactionManager`。对于编程式事务管理，`spring推荐使用TransactionTemplate`。
- 声明式事务管理建立在AOP之上的。其本质是对方法前后进行拦截，然后在目标方法开始之前创建或者加入一个事务，在执行完目标方法之后根据执行情况提交或者回滚事务。

```java
public interface PlatformTransactionManager {
    TransactionStatus getTransaction(@Nullable TransactionDefinition var1) throws TransactionException;

    void commit(TransactionStatus var1) throws TransactionException;

    void rollback(TransactionStatus var1) throws TransactionException;
}
```

```java
@Component
public class PlatformTransactionManagerProxy {

    @Resource
    PlatformTransactionManager platformTransactionManager;

    @Resource
    TransactionDefinition transactionDefinition;

    private volatile ThreadLocal<TransactionStatus> transactionStatusThreadLocal = new ThreadLocal<>();


    /**
     * 开启事务
     */
    public void beginTransaction(){
        TransactionStatus transactionStatus = platformTransactionManager.getTransaction(transactionDefinition);
        transactionStatusThreadLocal.set(transactionStatus);
    }

    /**
     * 提交事务
     */
    public void commit() {
        TransactionStatus transactionStatus = transactionStatusThreadLocal.get();
        if(Objects.nonNull(transactionStatus)) {
            platformTransactionManager.commit(transactionStatus);
        } else {
            log.error("事务提交异常");
        }
    }

    /**
     * 回滚事务
     */
    public void rollback() {
        TransactionStatus transactionStatus = transactionStatusThreadLocal.get();
        if(Objects.nonNull(transactionStatus)) {
            platformTransactionManager.rollback(transactionStatus);
        } else {
            log.error("事务回滚异常");
        }
    }
}
```
