# hystrix配置

- [https://github.com/Netflix/Hystrix](https://github.com/Netflix/Hystrix)
- [https://github.com/Netflix/Hystrix/wiki/Configuration](https://github.com/Netflix/Hystrix/wiki/Configuration)

```conf
# 开启断路器
spring.cloud.circuit.breaker.enabled=true
# 在feign中开启hystrix功能，默认情况下feign不开启hystrix功能
feign.hystrix.enabled=true
# 命令执行(execution)配置
# 隔离策略,默认THREAD
hystrix.command.default.execution.isolation.strategy=THREAD
# 是否允许超时，默认true。如果enabled设置为false，则请求超时交给ribbon控，`timeoutInMilliseconds`则无法控制，
# 如果为true，并同时配置了 Ribbon 和 Hystrix 的超时时间，则`ReadTimeout`和`timeoutInMilliseconds`谁小谁控制
# 超时时间上限，默认1000
hystrix.command.default.execution.isolation.thread.timeoutInMilliseconds=60000
#feign熔断超时总时间计算公式（黄海平 2020-06-08）
# 总时间(feignTimeTotal) = ReadTimeout * (MaxAutoRetries + 1) * (MaxAutoRetriesNextServer * 2)
# 注：hystrix.command.default.execution.timeout.enabled=true timeoutInMilliseconds的时间值必须要比feignTimeTotal大，否则优先于hystrix熔断

# 线程池配置
# Hystrix使用的是JUC线程池ThreadPoolExecutor，线程池相关配置直接影响ThreadPoolExecutor实例。
# 核心线程数，默认10
hystrix.threadpool.default.coreSize=50
# 最大任务队列容量，默认值-1使用的是`SynchronousQueue`无缓冲队列无法存储元素,配置为大于0时使用`LinkedBlockingQueue`有缓冲队列可存储元素
hystrix.threadpool.default.maxQueueSize=1000
# 任务拒绝的任务队列阈值,默认5。当`maxQueueSize`配置为-1的时候，此配置项不生效。
# 即使maxQueueSize没有达到，达到`queueSizeRejectionThreshold`该值后，请求也会被拒绝
hystrix.threadpool.default.queueSizeRejectionThreshold=100

# 命令降级(fallback)配置
# 是否开启降级,默认true
hystrix.command.default.fallback.enabled=true
# 所有命令降级配置对策略ExecutionIsolationStrategy.THREAD或者ExecutionIsolationStrategy.SEMAPHORE都生效
# 最大并发降级请求处理上限，降级逻辑不会执行并且会抛出一个异常。默认10
hystrix.command.default.fallback.isolation.semaphore.maxConcurrentRequests=100

# 断路器(circuit breaker)配置
# 是否启用断路器，默认true
hystrix.command.default.circuitBreaker.enabled=true
# 断路器请求量阈值,使断路器打开的滑动窗口中的最小请求数量，默认20。(需要在启动类添加@EnableCircuitBreaker)
# 如果值是20，那么如果在滑动窗口中只接收到19个请求(比如一个10秒的窗口)，即使所有19个请求都失败了，断路器也不会打开。
hystrix.command.default.circuitBreaker.requestVolumeThreshold=20
# 断路器等待窗口时间,默认5000
# 此属性设置断路器打开后拒绝请求的时间量，每隔一段时间(sleepWindowInMilliseconds，单位是毫秒)允许再次尝试(也就是放行一个请求)确定是否应该关闭断路器。
hystrix.command.default.circuitBreaker.sleepWindowInMilliseconds=3000
# 断路器错误百分比阈值，默认50
# 此属性设置一个错误百分比，当请求错误率超过设定值，断路器就会打开。
hystrix.command.default.circuitBreaker.errorThresholdPercentage=50
```

## maven依赖

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-hystrix</artifactId>
</dependency>
```
