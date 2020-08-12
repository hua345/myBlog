# Arthas简介

[Arthas](https://github.com/alibaba/arthas/blob/master/README_CN.md) 是 Alibaba 开源的 Java 诊断工具，深受开发者喜爱。

当你遇到以下类似问题而束手无策时，Arthas 可以帮助你解决：

- 这个类从哪个 jar 包加载的？为什么会报各种类相关的 Exception？
- 我改的代码为什么没有执行到？难道是我没 commit？分支搞错了？
- 遇到问题无法在线上 debug，难道只能通过加日志再重新发布吗？
- 线上遇到某个用户的数据处理有问题，但线上同样无法 debug，线下无法重现！
- 是否有一个全局视角来查看系统的运行状况？
- 有什么办法可以监控到 JVM 的实时运行状态？

## [快速安装](https://alibaba.github.io/arthas/install-detail.html)

下载`arthas-boot.jar`，然后用`java -jar`的方式启动：

```bash
wget https://alibaba.github.io/arthas/arthas-boot.jar
java -jar arthas-boot.jar
```

如果下载速度比较慢，可以使用 aliyun 的镜像：

```bash
java -jar arthas-boot.jar --repo-mirror aliyun --use-http
```

### 全量安装

可以尝试用[阿里云的镜像仓库](https://maven.aliyun.com/mvn/search)，比如要下载 3.x.x 版本（替换 3.x.x 为最新版本），下载的 url 是：
`https://maven.aliyun.com/repository/public/com/taobao/arthas/arthas-packaging/3.x.x/arthas-packaging-3.x.x-bin.zip`
解压缩 arthas 的压缩包

```bash
unzip arthas-packaging-bin.zip
```

解压后，在文件夹里有`arthas-boot.jar`，直接用`java -jar`的方式启动：

```bash
java -jar arthas-boot.jar
```

打印帮助信息：

```bash
java -jar arthas-boot.jar -h
```

### 卸载 Arthas

```bash
rm -rf ~/.arthas/
rm -rf ~/logs/arthas
```

### 查看help

```bash
help
 NAME         DESCRIPTION
 help         Display Arthas Help
 keymap       Display all the available keymap for the specified connection.
 sc           Search all the classes loaded by JVM
 sm           Search the method of classes loaded by JVM
 classloader  Show classloader info
 jad          Decompile class
 getstatic    Show the static field of a class
 monitor      Monitor method execution statistics, e.g. total/success/failure
              count, average rt, fail rate, etc.
 stack        Display the stack trace for the specified class and method
 thread       Display thread info, thread stack
 trace        Trace the execution time of specified method invocation.
 watch        Display the input/output parameter, return object, and thrown ex
              ception of specified method invocation
 tt           Time Tunnel
 jvm          Display the target JVM information
 perfcounter  Display the perf counter infornation.
 ognl         Execute ognl expression.
 mc           Memory compiler, compiles java files into bytecode and class fil
              es in memory.
 redefine     Redefine classes. @see Instrumentation#redefineClasses(ClassDefi
              nition...)
 dashboard    Overview of target jvm's thread, memory, gc, vm, tomcat info.
 dump         Dump class byte array from JVM
 heapdump     Heap dump
 options      View and change various Arthas options
 cls          Clear the screen
 reset        Reset all the enhanced classes
 version      Display Arthas version
 session      Display current session information
 sysprop      Display, and change the system properties.
 sysenv       Display the system env.
 vmoption     Display, and update the vm diagnostic options.
 logger       Print logger info, and update the logger level
 history      Display command history
 cat          Concatenate and print files
 echo         write arguments to the standard output
 pwd          Return working directory name
 mbean        Display the mbean information
 grep         grep command for pipes.
 tee          tee command for pipes.
 profiler     Async Profiler. https://github.com/jvm-profiling-tools/async-pro
              filer
 stop         Stop/Shutdown Arthas server and exit the console.
```

### 查看 `dashboard`

输入 `dashboard`，按回车/enter，会展示当前进程的信息，按`ctrl+c`可以中断执行

```bash
ID     NAME               GROUP         PRIOR STATE  %CPU  TIME   INTER DAEMON
30     Abandoned connecti main          5     TIMED_ 0     0:0    false true
70     AsyncAppender-Work system        5     WAITIN 0     0:0    false true
5      Attach Listener    system        5     RUNNAB 0     0:0    false true
37     ContainerBackgroun main          5     TIMED_ 0     0:0    false true
58     DestroyJavaVM      main          5     RUNNAB 0     0:5    false false
34     Druid-ConnectionPo main          5     WAITIN 0     0:0    false true
35     Druid-ConnectionPo main          5     TIMED_ 0     0:0    false true
3      Finalizer          system        8     WAITIN 0     0:0    false true
6      Monitor Ctrl-Break main          5     RUNNAB 0     0:0    false true
42     NioBlockingSelecto main          5     RUNNAB 0     0:0    false true
Memory           used  total max  usage GC
heap             206M  320M                                 8
ps_eden_space    168M  196M  646M       gc.ps_scavenge.time 159
                 13M   13M   13M        (ms)
ps_old_gen       24M   110M       1.85% gc.ps_marksweep.cou 2
nonheap          60M   70M   -1         nt
Runtime
os.name             Windows 10
os.version          10.0
java.version        1.8.0_161
java.home           D:\Program Files\JD
                    K8\jre

```

#### `Thread`一目了然的了解系统的状态，哪些线程比较占 cpu？他们到底在做什么？

```bash
#展示当前最忙的前N个线程并打印堆栈
thread -n 3
#当没有参数时，显示所有线程的信息。
thread
#thread id， 显示指定线程的运行堆栈
thread 2
```

```bash
$ thread -n 3
thread -n 3
"Reference Handler" Id=2 cpuUsage=0% WAITING on java.lang.ref.Reference$Lock@4396c8dd
    at java.lang.Object.wait(Native Method)
    -  waiting on java.lang.ref.Reference$Lock@4396c8dd
    at java.lang.Object.wait(Object.java:502)
    at java.lang.ref.Reference.tryHandlePending(Reference.java:191)
    at java.lang.ref.Reference$ReferenceHandler.run(Reference.java:153)


"Finalizer" Id=3 cpuUsage=0% WAITING on java.lang.ref.ReferenceQueue$Lock@b118b39
    at java.lang.Object.wait(Native Method)
    -  waiting on java.lang.ref.ReferenceQueue$Lock@b118b39
    at java.lang.ref.ReferenceQueue.remove(ReferenceQueue.java:143)
    at java.lang.ref.ReferenceQueue.remove(ReferenceQueue.java:164)
    at java.lang.ref.Finalizer$FinalizerThread.run(Finalizer.java:209)

"Signal Dispatcher" Id=4 cpuUsage=0% RUNNABLE
```

#### `jad`对类进行反编译

```bash
$ jad javax.servlet.Servlet

ClassLoader:
+-java.net.URLClassLoader@6108b2d7
  +-sun.misc.Launcher$AppClassLoader@18b4aac2
    +-sun.misc.Launcher$ExtClassLoader@1ddf84b8

Location:
/Users/xxx/work/test/lib/servlet-api.jar

/*
 * Decompiled with CFR 0_122.
 */
package javax.servlet;

import java.io.IOException;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;

public interface Servlet {
    public void init(ServletConfig var1) throws ServletException;

    public ServletConfig getServletConfig();

    public void service(ServletRequest var1, ServletResponse var2) throws ServletException, IOException;

    public String getServletInfo();

    public void destroy();
}
```

反编译指定的函数

```bash
jad java.lang.String trim
ClassLoader:
Location:
public String trim() {
    int n;
    int n2 = this.value.length;
    char[] arrc = this.value;
    for (n = 0; n < n2 && arrc[n] <= ' '; ++n) {
    }
    while (n < n2 && arrc[n2 - 1] <= ' ') {
        --n2;
    }
    return n > 0 || n2 < this.value.length ? this.substring(n, n2) : this;
}

```

#### `sc`查找 JVM 中已经加载的类

```bash
$ sc com.github.hello.*
sc com.github.hello.*
com.github.hello.fang.Application
com.github.hello.fang.Application$$EnhancerBySpringCGLIB$$92b49232
com.github.hello.fang.config.DruidConfiguration
com.github.hello.fang.config.DruidConfiguration$$EnhancerBySpringCGLIB$$5c8c4462
com.github.hello.fang.config.DruidConfiguration$$EnhancerBySpringCGLIB$$5c8c4462$$FastClassBySpringCGLIB$$597b88ee
com.github.hello.fang.config.DruidConfiguration$$FastClassBySpringCGLIB$$28a57280
com.github.hello.fang.config.DruidDataSourceProperties
com.github.hello.fang.mapper.UserMapper
com.github.hello.fang.model.User
```

#### Classloader

了解当前系统中有多少类加载器，以及每个加载器加载的类数量，帮助您判断是否有类加载器泄露。

```bash
classloader
 name                                                numberOfInstances  loaded
                                                                        CountT
                                                                        otal
 sun.misc.Launcher$AppClassLoader                    1                  5557
 BootstrapClassLoader                                1                  3226
 com.taobao.arthas.agent.ArthasClassloader           1                  1717
 sun.reflect.DelegatingClassLoader                   134                134
 sun.misc.Launcher$ExtClassLoader                    1                  30
 javax.management.remote.rmi.NoCallStackClassLoader  2                  2
 sun.reflect.misc.MethodUtil                         1                  1
```
