## Executors 创建线程池

在`《阿里巴巴 Java 开发手册》`“并发处理”这一章节，明确指出线程资源必须通过线程池提供，不允许在应用中自行显示创建线程。

> 使用线程池的好处是减少在创建和销毁线程上所消耗的时间以及系统资源开销，解决资源不足的问题。如果不使用线程池，有可能会造成系统创建大量同类线程而导致消耗完内存或者“过度切换”的问题。

`《阿里巴巴 Java 开发手册》`中强制线程池不允许使用 `Executors` 去创建，而是通过 `ThreadPoolExecutor` 构造函数的方式，这样的处理方式让写的同学更加明确线程池的运行规则，规避资源耗尽的风险

`Executors` 返回线程池对象的弊端如下：

- `FixedThreadPool` 和 `SingleThreadExecutor` ： 允许请求的队列长度为 `Integer.MAX_VALUE`,可能堆积大量的请求，从而导致 OOM。
- `CachedThreadPool` 和 `ScheduledThreadPool` ： 允许创建的线程数量为 `Integer.MAX_VALUE` ，可能会创建大量线程，从而导致 OOM。

```java
// 创建固定大小的线程池
Executors.newFixedThreadPool(10);
// 创建只有一个线程的线程池
Executors.newSingleThreadExecutor();
// 创建一个不限线程数上限的线程池，任何提交的任务都将立即执行
Executors.newCachedThreadPool();
// 定时任务线程池
Executors.newScheduledThreadPool(4);

public class Executors {
    public static ExecutorService newFixedThreadPool(int nThreads) {
        return new ThreadPoolExecutor(nThreads, nThreads, 0L, TimeUnit.MILLISECONDS, new LinkedBlockingQueue());
    }
    public static ExecutorService newSingleThreadExecutor() {
        return new Executors.FinalizableDelegatedExecutorService(new ThreadPoolExecutor(1, 1, 0L, TimeUnit.MILLISECONDS, new LinkedBlockingQueue()));
    }
    public static ExecutorService newCachedThreadPool() {
        return new ThreadPoolExecutor(0, 2147483647, 60L, TimeUnit.SECONDS, new SynchronousQueue());
    }
    public static ScheduledExecutorService newScheduledThreadPool(int corePoolSize) {
        return new ScheduledThreadPoolExecutor(corePoolSize);
    }
}
```

小程序使用这些快捷方法没什么问题，对于服务端需要长期运行的程序，创建线程池应该直接使用`ThreadPoolExecutor`的构造方法。

```java
public ThreadPoolExecutor(int corePoolSize, // 线程池长期维持的线程数，即使线程处于Idle状态，也不会回收。
        int maximumPoolSize, // 线程数的上限
        long keepAliveTime, // 当线程数大于核心线程数时，多余的空闲线程存活的最长时间
        TimeUnit unit, // 超时时间单位
        BlockingQueue<Runnable> workQueue, // 任务的排队队列
        ThreadFactory threadFactory, // 新线程的产生方式
        RejectedExecutionHandler handler); // 拒绝策略
```

## 如何正确使用线程池

### 避免使用无界队列



```java
ExecutorService executorService = new ThreadPoolExecutor(2, 2,
        0, TimeUnit.SECONDS,
        new ArrayBlockingQueue<>(512), // 使用有界队列，避免OOM
        new ThreadPoolExecutor.DiscardPolicy());
```

### 明确拒绝任务时的行为

任务队列总有占满的时候，这是再`submit()`提交新的任务会怎么样呢？`RejectedExecutionHandler`接口为我们提供了控制方式，接口定义如下：

```java
public interface RejectedExecutionHandler {
    void rejectedExecution(Runnable var1, ThreadPoolExecutor var2);
}

public class ThreadPoolExecutor extends AbstractExecutorService {
    // 默认拒绝方式
    private static final RejectedExecutionHandler defaultHandler = new ThreadPoolExecutor.AbortPolicy();
    // 默认线程生成器
    public static ThreadFactory defaultThreadFactory() {
        return new Executors.DefaultThreadFactory();
    }

    public ThreadPoolExecutor(int corePoolSize, int maximumPoolSize, long keepAliveTime, TimeUnit unit, BlockingQueue<Runnable> workQueue) {
        this(corePoolSize, maximumPoolSize, keepAliveTime, unit, workQueue, Executors.defaultThreadFactory(), defaultHandler);
    }

    public ThreadPoolExecutor(int corePoolSize, int maximumPoolSize, long keepAliveTime, TimeUnit unit, BlockingQueue<Runnable> workQueue, ThreadFactory threadFactory) {
        this(corePoolSize, maximumPoolSize, keepAliveTime, unit, workQueue, threadFactory, defaultHandler);
    }

    public ThreadPoolExecutor(int corePoolSize, int maximumPoolSize, long keepAliveTime, TimeUnit unit, BlockingQueue<Runnable> workQueue, RejectedExecutionHandler handler) {
        this(corePoolSize, maximumPoolSize, keepAliveTime, unit, workQueue, Executors.defaultThreadFactory(), handler);
    }

    public static class DiscardOldestPolicy implements RejectedExecutionHandler {
        public DiscardOldestPolicy() {
        }

        public void rejectedExecution(Runnable r, ThreadPoolExecutor e) {
            if (!e.isShutdown()) {
                e.getQueue().poll();
                e.execute(r);
            }

        }
    }
    public static class DiscardPolicy implements RejectedExecutionHandler {
        public DiscardPolicy() {
        }

        public void rejectedExecution(Runnable r, ThreadPoolExecutor e) {
        }
    }

    public static class AbortPolicy implements RejectedExecutionHandler {
        public AbortPolicy() {
        }

        public void rejectedExecution(Runnable r, ThreadPoolExecutor e) {
            throw new RejectedExecutionException("Task " + r.toString() + " rejected from " + e.toString());
        }
    }
    public static class CallerRunsPolicy implements RejectedExecutionHandler {
        public CallerRunsPolicy() {
        }

        public void rejectedExecution(Runnable r, ThreadPoolExecutor e) {
            if (!e.isShutdown()) {
                r.run();
            }

        }
    }
}
```

| 拒绝策略            | 拒绝行为                                               |
| ------------------- | ------------------------------------------------------ |
| AbortPolicy         | 抛出 RejectedExecutionException                        |
| DiscardPolicy       | 什么也不做，直接忽略                                   |
| DiscardOldestPolicy | 丢弃执行队列中最老的任务，尝试为当前提交的任务腾出位置 |
| CallerRunsPolicy    | 直接由提交任务者执行这个任务                           |

线程池默认的拒绝行为是 AbortPolicy，也就是抛出 RejectedExecutionHandler 异常，该异常是非受检异常，很容易忘记捕获。如果不关心任务被拒绝的事件，可以将拒绝策略设置成 DiscardPolicy，这样多余的任务会悄悄的被忽略。

## 参考

- [java线程池学习总结](https://github.com/Snailclimb/JavaGuide/blob/master/docs/java/Multithread/java%E7%BA%BF%E7%A8%8B%E6%B1%A0%E5%AD%A6%E4%B9%A0%E6%80%BB%E7%BB%93.md)
- [java 线程池 01-ThreadPoolExecutor 构造方法参数的使用规则](https://www.cnblogs.com/cdf-opensource-007/p/8769777.html)
