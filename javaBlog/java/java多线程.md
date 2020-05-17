# `Runnable` vs `Callable`

`Runnable` 接口不会返回结果或抛出检查异常，但是`Callable`接口可以。
所以，如果任务不需要返回结果或抛出异常推荐使用`Runnable`接口，这样代码看起来会更加简洁。

`Runnable.java`

```java
@FunctionalInterface
public interface Runnable {
   /**
    * 被线程执行，没有返回值也无法抛出异常
    */
    void run();
}
```

`Callable.java`

```java
@FunctionalInterface
public interface Callable<V> {
    /**
     * 计算结果，或在无法这样做时抛出异常。
     * @return 计算得出的结果
     * @throws 如果无法计算结果，则抛出异常
     */
    V call() throws Exception;
}
```

```java
public class DateUtil {
    public static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    public static String getCurrentDate() {
        Date currentTime = new Date();
        LocalDateTime time = LocalDateTime.ofInstant(currentTime.toInstant(), ZoneId.systemDefault());
        String dateString = formatter.format(time);
        return dateString;
    }
}
public class MyRunnable implements Runnable {
    public void run() {
        System.out.println(Thread.currentThread().getName() + " Start. Time = " + DateUtil.getCurrentDate());
        processCommand();
        System.out.println(Thread.currentThread().getName() + " End. Time = " + DateUtil.getCurrentDate());
    }

    private void processCommand() {
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
public class MyCallable implements Callable<String> {

    public String call() throws Exception {
        System.out.println(Thread.currentThread().getName() + " Start. Time = " + DateUtil.getCurrentDate());
        Thread.sleep(1000);
        return "Hello";
    }
}

public class IntTest {
    public static void main(String[] args) {
        ExecutorService executorService = new ThreadPoolExecutor(2, 4,
                0, TimeUnit.SECONDS,
                new ArrayBlockingQueue<>(512), // 使用有界队列，避免OOM
                new ThreadPoolExecutor.DiscardPolicy());
        MyCallable myCallable = new MyCallable();
        Future<String> future = executorService.submit(myCallable);
        try{
            System.out.println("result: " + future.get());
            System.out.println(Thread.currentThread().getName() + " End. Time = " + DateUtil.getCurrentDate());
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
```

## 参考

- [java线程池学习总结](https://github.com/Snailclimb/JavaGuide/blob/master/docs/java/Multithread/java%E7%BA%BF%E7%A8%8B%E6%B1%A0%E5%AD%A6%E4%B9%A0%E6%80%BB%E7%BB%93.md)