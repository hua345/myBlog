# kafka错误处理

## 启动时加载日志失败

```log
[2020-07-28 11:17:02,348] INFO Loading logs. (kafka.log.LogManager)
[2020-07-28 11:17:02,397] ERROR There was an error in one of the threads during logs loading: java.lang.NumberFormatException: For input string: "hs_err_pid32300" (kafka.log.LogManager)
[2020-07-28 11:17:02,398] INFO [Log partition=love-2, dir=/var/kafka/data01] Recovering unflushed segment 0 (kafka.log.Log)
[2020-07-28 11:17:02,400] ERROR [KafkaServer id=0] Fatal error during KafkaServer startup. Prepare to shutdown (kafka.server.KafkaServer)
java.lang.NumberFormatException: For input string: "hs_err_pid32300"
        at java.lang.NumberFormatException.forInputString(NumberFormatException.java:65)
        at java.lang.Long.parseLong(Long.java:589)
        at java.lang.Long.parseLong(Long.java:631)
        at scala.collection.immutable.StringLike.toLong(StringLike.scala:309)
        at scala.collection.immutable.StringLike.toLong$(StringLike.scala:309)
        at scala.collection.immutable.StringOps.toLong(StringOps.scala:33)
        at kafka.log.Log$.offsetFromFileName(Log.scala:2568)
        at kafka.log.Log$.offsetFromFile(Log.scala:2572)
        at kafka.log.Log.$anonfun$loadSegmentFiles$3(Log.scala:597)
        at scala.collection.TraversableLike$WithFilter.$anonfun$foreach$1(TraversableLike.scala:877)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:36)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:33)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:198)
        at scala.collection.TraversableLike$WithFilter.foreach(TraversableLike.scala:876)
        at kafka.log.Log.loadSegmentFiles(Log.scala:586)
        at kafka.log.Log.$anonfun$loadSegments$1(Log.scala:697)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:23)
        at kafka.log.Log.retryOnOffsetOverflow(Log.scala:2329)
        at kafka.log.Log.loadSegments(Log.scala:691)
        at kafka.log.Log.<init>(Log.scala:297)
        at kafka.log.Log$.apply(Log.scala:2463)
        at kafka.log.LogManager.loadLog(LogManager.scala:272)
        at kafka.log.LogManager.$anonfun$loadLogs$12(LogManager.scala:342)
        at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
        at java.util.concurrent.FutureTask.run(FutureTask.java:266)
        at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
        at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
        at java.lang.Thread.run(Thread.java:748)
[2020-07-28 11:17:02,400] INFO [Log partition=love-2, dir=/var/kafka/data01] Loading producer state till offset 0 with message format version 2 (kafka.log.Log)
[2020-07-28 11:17:02,403] INFO [KafkaServer id=0] shutting down (kafka.server.KafkaServer)
```

### 查询文件所在位置

```bash
➜  data01 find /var/kafka -name 'hs_err_pid*'
/var/kafka/data01/fang-0/hs_err_pid32300.log
```

当JVM发生致命错误导致崩溃时，会生成一个`hs_err_pid_xxx.log`这样的文件，该文件包含了导致 `JVM crash` 的重要信息，我们可以通过分析该文件定位到导致 `JVM Crash` 的原因

```bash
#
# There is insufficient memory for the Java Runtime Environment to continue.
# Native memory allocation (mmap) failed to map 67108864 bytes for committing reserved memory.
# Possible reasons:
#   The system is out of physical RAM or swap space
#   The process is running with CompressedOops enabled, and the Java Heap may be blocking the growth of the native heap
# Possible solutions:
#   Reduce memory load on the system
#   Increase physical memory or swap space
#   Check if swap backing store is full
#   Decrease Java heap size (-Xmx/-Xms)
#   Decrease number of Java threads
#   Decrease Java thread stack sizes (-Xss)
#   Set larger code cache with -XX:ReservedCodeCacheSize=
#   JVM is running with Unscaled Compressed Oops mode in which the Java heap is
#     placed in the first 4GB address space. The Java Heap base address is the
#     maximum limit for the native heap growth. Please use -XX:HeapBaseMinAddress
#     to set the Java Heap base and to place the Java Heap above 4GB virtual address.
# This output file may be truncated or incomplete.
#
#  Out of Memory Error (os_linux.cpp:2763), pid=32300, tid=0x00007fea7f42b700
#
# JRE version: OpenJDK Runtime Environment (8.0_252-b09) (build 1.8.0_252-b09)
# Java VM: OpenJDK 64-Bit Server VM (25.252-b09 mixed mode linux-amd64 compressed oops)
# Failed to write core dump. Core dumps have been disabled. To enable core dumping, try "ulimit -c unlimited" before starting Java again
```

虚拟机内存不足，导致内存分配失败

扩大虚拟机内存，并删除`hs_err_pid_xxx.log`文件
