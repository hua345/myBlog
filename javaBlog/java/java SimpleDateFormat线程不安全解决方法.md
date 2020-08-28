# SimpleDateFormat

## SimpleDateFormat 为什么不是线程安全的

如果我们把`SimpleDateFormat`定义成`static`成员变量，那么多个`thread`之间会共享这个`SimpleDateFormat`对象， 所以`Calendar`对象也会共享。

```java
public abstract class DateFormat extends Format {
    protected Calendar calendar;
}

public class SimpleDateFormat extends DateFormat {
    @Override
    public StringBuffer format(Date date, StringBuffer toAppendTo,
                               FieldPosition pos)
    {
        pos.beginIndex = pos.endIndex = 0;
        return format(date, toAppendTo, pos.getFieldDelegate());
    }

    // Called from Format after creating a FieldDelegate
    private StringBuffer format(Date date, StringBuffer toAppendTo,
                                FieldDelegate delegate) {
        // Convert input date to time field list
        calendar.setTime(date);
    }
}
```

### 线程安全示例

```java
    private static SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.CHINA);
    private static String date[] = { "2016-01-06", "2017-01-07", "2018-01-08" , "2019-01-09" , "2020-01-10"};

    public static void main(String[] args) throws Exception {
        for (int i = 0; i < date.length; i++) {
            final int temp = i;
            new Thread(new Runnable() {
                @Override
                public void run() {
                    try {
                        String str1 = date[temp];
                        String str2 = sdf.format(sdf.parse(str1));
                        System.out.println(Thread.currentThread().getName() + ", " + str1 + "," + str2);
                        if(!str1.equals(str2)){
                            throw new RuntimeException(Thread.currentThread().getName()
                                    + ", Expected " + str1 + " but got " + str2);
                        }
                    } catch (Exception e) {
                        throw new RuntimeException("parse failed", e);
                    }
                }
            }).start();
        }
    }
```

```log
Thread-4, 2019-01-09,2200-01-09
Thread-1, 2016-01-06,2016-01-06
Thread-5, 2020-01-10,2020-01-10
java.lang.RuntimeException: parse failed
    at com.github.demo.learn.utils.DateUtil$1.run(DateUtil.java:243)
    at java.lang.Thread.run(Thread.java:748)
Caused by: java.lang.RuntimeException: Thread-4, Expected 2019-01-09 but got 2200-01-09
```

## SimpleDateFormat 线程不安全的解决方法

### 将`SimpleDateFormat`定义成局部变量
  
### 加一把线程同步锁：`synchronized(lock)`

性能较差，每次都要等待锁释放后其他线程才能进入

```java
    private static SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.CHINA);
    private static String date[] = {"2016-01-06", "2017-01-07", "2018-01-08", "2019-01-09", "2020-01-10"};

    public static void main(String[] args) throws Exception {
        for (int i = 0; i < date.length; i++) {
            final int temp = i;
            new Thread(new Runnable() {
                @Override
                public void run() {
                    try {
                        synchronized (sdf) {
                            String str1 = date[temp];
                            String str2 = sdf.format(sdf.parse(str1));
                            System.out.println(Thread.currentThread().getName() + ", " + str1 + "," + str2);
                            if (!str1.equals(str2)) {
                                throw new RuntimeException(Thread.currentThread().getName()
                                        + ", Expected " + str1 + " but got " + str2);
                            }
                        }
                    } catch (Exception e) {
                        throw new RuntimeException("parse failed", e);
                    }
                }
            }).start();
        }
    }
```

### 使用`ThreadLocal`

每个线程都将拥有自己的`SimpleDateFormat`对象副本

```java
public final class DateUtil {
    private static ThreadLocal<SimpleDateFormat> local = new ThreadLocal<SimpleDateFormat>();

    public static Date parse(String str) throws Exception {
        SimpleDateFormat sdf = local.get();
        if (sdf == null) {
            sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.CHINA);
            local.set(sdf);
        }
        return sdf.parse(str);
    }

    public static String format(Date date) throws Exception {
        SimpleDateFormat sdf = local.get();
        if (sdf == null) {
            sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.CHINA);
            local.set(sdf);
        }
        return sdf.format(date);
    }

    public static void main(String[] args) {
        for (int i = 0; i < date.length; i++) {
            final int temp = i;
            new Thread(new Runnable() {
                @Override
                public void run() {
                    try {
                        String str1 = date[temp];
                        String str2 = DateUtil.format(DateUtil.parse(str1));
                        System.out.println(Thread.currentThread().getName() + ", " + str1 + "," + str2);
                        if (!str1.equals(str2)) {
                            throw new RuntimeException(Thread.currentThread().getName()
                                    + ", Expected " + str1 + " but got " + str2);
                        }
                    } catch (Exception e) {
                        throw new RuntimeException("parse failed", e);
                    }
                }
            }).start();
        }
    }
}
```

### 使用 DateTimeFormatter 代替 SimpleDateFormat

