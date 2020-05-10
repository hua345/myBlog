# synchronized 和锁(ReentrantLock) 区别

> `ReentrantLock`称为重入锁，位于`JUC`包的 locks，和`CountDownLatch`、`FutureTask`一样基于`AQS实现`。能够实现比`synchronized`更细粒度的控制，比如控制公平性。此外需要注意，调用`lock()`之后，必须调用`unlock()`释放锁。它的性能未必比`synchronized`高，并且是可重入的。

- 对于`synchronized`来说，它是 Java 语言关键字，是原生语法层面的互斥，需要 jvm 实现。而`ReentrantLock`他是 jdk1.5 之后提供的 API 层面的互斥锁，需要`lock()`和`unlock()`方法配合`try/finally`语句来完成

- synchronized 是独占锁，加锁和解锁的过程自动进行，易于操作，但不够灵活。ReentrantLock 也是独占锁，加锁和解锁的过程需要手动进行，不易操作，但非常灵活。

## 性能区别

在`Synchronized`优化以前，`synchronized`的性能是比`ReenTrantLock`差很多的，但是自从`Synchronized`引入了`偏向锁`，`轻量级锁（自旋锁）`后，两者的性能就差不多了，在两种方法都可用的情况下，官方甚至建议使用`synchronized`，其实`synchronized`的优化我感觉就借鉴了`ReenTrantLock`中的 CAS 技术。都是试图在用户态就把加锁问题解决，避免进入内核态的线程阻塞。

## Synchronized

`Synchronized`经过编译后，会在同步块前后分别形成`monitorenter`和`monitorexit`两个字节码指令，在执行`monitorenter`指令时，首先要尝试获取对象锁，如果对象没有别锁定，或者当前已经拥有这个对象锁，把锁的计数器加 1，相应的在执行`monitorexit`指令时，会将计数器减 1，当计数器为 0 时，锁就被释放了。如果获取锁失败，那当前线程就要阻塞，直到对象锁被另一个线程释放为止。

```java
public class SyncDemo{

    public static void main(String[] arg){
        Runnable t1=new MyThread();
        new Thread(t1,"t1").start();
        new Thread(t1,"t2").start();
    }
}
class MyThread implements Runnable {

    @Override
    public void run() {
        synchronized (this) {
            for(int i=0;i<10;i++)
                System.out.println(Thread.currentThread().getName()+":"+i);
        }
    }
}
```

## ReentrantLock

由于`ReentrantLock`是`java.util.concurrent`包下面提供的一套互斥锁，相比`Synchronized`类提供了一些高级的功能，主要有一下三项：

- `等待可中断`，持有锁的线程长期不释放的时候，正在等待的线程可以选择放弃等待，这相当于`Synchronized`来说可以避免出现死锁的情况。通过`lock.lockInterruptibly()`来实现这个机制。

- `公平锁`，多个线程等待同一个锁时，必须按照申请锁的时间顺序获得锁，`Synchronized`锁非公平锁，ReentrantLock默认的构造函数是创建的非公平锁，可以通过参数true设为公平锁，但公平锁表现的性能不是很好。

```java
ReentrantLock fairLock = new ReentrantLock(true);

// 参数为true时，倾向于将锁赋予等待时间最久的线程；
// 公平锁：获取锁的顺序按先后调用lock方法的顺序（慎用）；
// 非公平锁：抢占的顺序不一定，看运气；
// synchronized是非公平锁。
```

## ReenTrantLock实现的原理

简单来说，`ReenTrantLock`的实现是一种自旋锁，通过循环调用`CAS`操作来实现加锁。它的性能比较好也是因为避免了使线程进入内核态的阻塞状态。

## 参考

- [synchronized 和 ReentrantLock 的区别](https://www.jianshu.com/p/c6a602be4994)
