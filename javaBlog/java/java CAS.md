# CAS乐观锁

无锁 `CAS`(`Compare and swap`，比较和交换)是一种乐观的并发控制策略，`它假设对资源的访问是没有冲突的，遇到冲突进行重试操作直到没有冲突为止`。

这种设计思路和数据库的乐观锁很相像。在硬件层面，大部分的处理器都支持原子化的 CAS 指令。

也就是说比较和交换这个操作是有处理器来保证是原子操作的（在最坏的情况下，如果处理器不支持，JVM 将使用自旋锁）。

## JDK 中的原子操作类

在 `JDK8` 中`java.util.concurrent.atomic`包中包含了原子操作类，这些类比锁的粒度更细，量级更轻。

```java
AtomicBoolean
AtomicMarkableReference
Striped64
AtomicIntegerArray
AtomicReferenceArray
LongAccumulator
AtomicReferenceFieldUpdater
AtomicLongFieldUpdater
LongAdder
AtomicLongArray
AtomicIntegerFieldUpdater
AtomicLong
DoubleAccumulator
DoubleAdder
AtomicInteger
AtomicStampedReference
AtomicReference
```

```java
public class AtomicTest {
    private static int threadCount = 20;
    private static int incrementNum = 10000;

    @Test
    public void AtomicTest() throws Exception {
        AtomicInteger count = new AtomicInteger();
        CountDownLatch countDownLatch = new CountDownLatch(threadCount);
        for (int i = 0; i < threadCount; i++) {
            ThreadPoolUtil.getInstance().submit(new Runnable() {
                @Override
                public void run() {
                    for (int j = 0; j < incrementNum; j++) {
                        count.incrementAndGet();
                    }
                    countDownLatch.countDown();
                }
            });
        }
        countDownLatch.await();
        assertEquals(threadCount * incrementNum, count.get());
    }
}
```

## `ABA` 问题

假设`expected = A , update = C`，那么当我们执行 CAS 时，如果有另外一几个线程将 A 改为了 B，紧接着又改回了 A，那么对于此次 CAS 操作而言也是成功的。

对于某些场景而言，这种异常出现是无关紧要的，因为我们只关心最终结果。

如果`不仅需要关注结果而且还想关注过程`，JDK 为我们提供了 2 个类来解决 `ABA` 问题。它们分别是`AtomicStampedReference`和`AtomicMarkableReference`。个人推荐使用`AtomicStampedReference`，类似于`数据库乐观锁`。

```java
    public boolean compareAndSet(V   expectedReference,
                                 V   newReference,
                                 int expectedStamp,
                                 int newStamp) {
        Pair<V> current = pair;
        return
            expectedReference == current.reference &&
            expectedStamp == current.stamp &&
            ((newReference == current.reference &&
              newStamp == current.stamp) ||
             casPair(current, Pair.of(newReference, newStamp)));
    }
```

```java
    public void printCurrentCas(AtomicStampedReference<String> asr) {
        System.out.println(Thread.currentThread().getName() + "当前变量值=" + asr.getReference() + "当前版本戳=" + asr.getStamp());
    }

    public void printCasResult(AtomicStampedReference<String> asr, boolean result) {
        System.out.println(Thread.currentThread().getName() + "当前变量值=" + asr.getReference() + "当前版本戳=" + asr.getStamp() + "更新成功?" + result);
    }

    @Test
    public void AtomicStampedReferenceTest() {
        AtomicStampedReference<String> asr = new AtomicStampedReference<>("A", 0);
        printCurrentCas(asr);
        ThreadPoolUtil.getInstance().submit(new Runnable() {
            @Override
            public void run() {
                int currentStamp = asr.getStamp();
                String currentReference = asr.getReference();
                printCasResult(asr, asr.compareAndSet(currentReference, "B", currentStamp, currentStamp + 1));
            }
        });
        ThreadPoolUtil.getInstance().submit(new Runnable() {
            @Override
            public void run() {
                int currentStamp = asr.getStamp();
                String currentReference = asr.getReference();
                printCasResult(asr, asr.compareAndSet(currentReference, "A", 0, 0));
                printCasResult(asr, asr.compareAndSet(currentReference, "A", currentStamp, currentStamp + 1));
            }
        });
    }
```

```log
main当前变量值=A当前版本戳=0
my-threadPool-my-thread-1当前变量值=B当前版本戳=1更新成功?true
my-threadPool-my-thread-2当前变量值=B当前版本戳=1更新成功?false
my-threadPool-my-thread-2当前变量值=A当前版本戳=2更新成功?true
```
