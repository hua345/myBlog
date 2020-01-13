# 参考

- [http://logback.qos.ch](http://logback.qos.ch)
- [http://www.slf4j.org](http://www.slf4j.org)
- [Log4j,Log4j2,logback,slf4j日志学习](https://www.cnblogs.com/williamjie/p/9197714.html)
- [logback](https://blog.csdn.net/dengsilinming/article/details/8265020)

## Spring Boot默认日志系统

`Spring Boot`默认使用`LogBack`日志系统，如果不需要更改为其他日志系统如`Log4j2`等，则无需多余的配置，`LogBack`默认将日志打印到控制台上。

如果要使用`LogBack`，原则上是需要添加dependency依赖的

```bash
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-logging</artifactId>
    </dependency>
```

`spring-boot-starter-logging`已经包含在`spring-boot-starter-web`中，一般项目引入`spring-boot-starter-web`就够了

```bash
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
```

## Log4j

`Log4j`是Apache的一个开放源代码项目，通过使用`Log4j`，我们可以控制日志信息输送的目的地是控制台、文件、数据库等；

我们也可以控制每一条日志的输出格式；通过定义每一条日志信息的级别，我们能够更加细致地控制日志的生成过程。

## Log4j2

`Spring Boot1.4`以及之后的版本已经不支持`log4j`，`log4j`也很久没有更新了

现在已经有很多其他的日志框架对`Log4j`进行了改良，比如说SLF4J、Logback等。

- Java 5的并发性。`Log4j2`利用`Java5`中的并发特性支持，尽可能地执行最低层次的加锁。解决了在log4j 1.x中存留的死锁的问题
- 异步logger。`Log4j2`是基于LMAX Disruptor库的。在多线程的场景下，和已有的日志框架相比，异步的logger拥有10倍左右的效率提升

## SLF4J

`SLF4J`，即简单日志门面（`Simple Logging Facade for Java`），不是具体的日志解决方案，
而是通过`Facade Pattern`提供一些`Java logging API`，它只服务于各种各样的日志系统。
按照官方的说法，`SLF4J`是一个用于日志系统的简单`Facade`，允许最终用户在部署其应用时使用其所希望的日志系统。

如果你开发的是类库或者嵌入式组件，那么就应该考虑采用`SLF4J`，因为不可能影响最终用户选择哪种日志系统。
在另一方面，如果是一个简单或者独立的应用，确定只有一种日志系统，那么就没有使用`SLF4J`的必要。

## Logback

`Logback`是由`log4j`创始人设计的另一个开源日志组件,官方网站： http://logback.qos.ch。它当前分为下面下个模块

- `logback-core`：其它两个模块的基础模块
- `logback-classic`：它是log4j的一个改良版本，同时它完整实现了`slf4j API`使你可以很方便地更换成其它日志系统如`log4j2`
- `logback-access`：访问模块与Servlet容器集成提供通过Http来访问日志的功能

### logback取代log4j的理由

- `logback`比`log4j`要快大约10倍，而且消耗更少的内存
- `logback-classic`模块直接实现了`SLF4J`的接口，所以我们迁移到`logback`几乎是零开销的
- `logback`能够根据配置文件中设置的上限值，自动删除旧的日志文件
- `logback`能够自动压缩日志文件

### logback的配置介绍

#### Logger、appender及layout

- `Logger`作为日志的记录器，把它关联到应用的对应的`context`上后，主要用于存放日志对象，也可以定义日志类型、级别。
- `Appender`主要用于指定日志输出的目的地，目的地可以是控制台、文件、远程套接字服务器、 MySQL、PostreSQL、 Oracle和其他数据库、 JMS和远程UNIX Syslog守护进程等
- `AsyncAppender`，异步记录日志。

#### RollingFileAppender

`RollingFileAppender`继承`FileAppender`，能够滚动记录文件。
例如，`RollingFileAppender`能先记录到文件“log.txt”，然后当符合某个条件时，变成记录到其他文件。
`RollingFileAppender`有两个与之互动的重要子组件。

- `RollingPolicy`，负责滚动。
- `TriggeringPolicy`，决定是否以及何时进行滚动。

#### Encoder

> This appender no longer admits a layout as a sub-component, set an encoder instead.

`Encoder`负责两件事，一是把事件转换为字节数组，二是把字节数组写入输出流。

`encoder`不但可以完全控制待写出的字节的格式，而且可以控制字节何时及是否被写出
在logback 0.9.19版之前没有`encoder`。

在之前的版本里，用户需要在FileAppender里嵌入一个PatternLayout。

```xml
    <!-- 控制台输出 -->
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <layout class="ch.qos.logback.classic.PatternLayout">
            <!--格式化输出：%d表示日期，%thread表示线程名，%-5level：级别从左显示5个字符宽度%msg：日志消息，%n是换行符-->
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{50} - %msg%n</pattern>
        </layout>
    </appender>
```

而从0.9.19版开始，FileAppender和其子类使用encoder，不接受layout。 如

```xml
    <!-- 控制台输出 -->
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <!--格式化输出：%d表示日期，%thread表示线程名，%-5level：级别从左显示5个字符宽度%msg：日志消息，%n是换行符-->
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{50} - %msg%n</pattern>
        </encoder>
    </appender>
```

#### logger context

各个`logger`都被关联到一个`LoggerContext`，`LoggerContext`负责制造`logger`，也负责以树结构排列各logger。其他所有logger也通过`org.slf4j.LoggerFactory`类的静态方法`getLogger`取得。

### Logback默认配置的步骤

- 尝试在`classpath`下查找文件`logback-test.xml`
- 如果文件不存在，则查找文件`logback.xml`
- 如果两个文件都不存在，`logback`用`BasicConfigurator`自动对自己进行配置，这会导致记录输出到控制台。

在`src/main/resource`目录创建`logback.xml`文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration debug="false">
    <!--定义日志文件的存储地址 勿在 LogBack 的配置中使用相对路径-->
    <property name="LOG_HOME" value="e:/Test/log"/>
    <!-- 控制台输出 -->
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <!--格式化输出：%d表示日期，%thread表示线程名，%-5level：级别从左显示5个字符宽度%msg：日志消息，%n是换行符-->
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{50} - %msg%n</pattern>
        </encoder>
    </appender>
    <!-- 按照每天生成日志文件 -->
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <!--日志文件输出的文件名-->
            <FileNamePattern>${LOG_HOME}/server.%d{yyyy-MM-dd}.log</FileNamePattern>
            <MaxHistory>30</MaxHistory>
        </rollingPolicy>
        <encoder>
            <!--格式化输出：%d表示日期，%thread表示线程名，%-5level：级别从左显示5个字符宽度%msg：日志消息，%n是换行符-->
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{50} - %msg%n</pattern>
        </encoder>
        <!--日志文件最大的大小-->
        <triggeringPolicy class="ch.qos.logback.core.rolling.SizeBasedTriggeringPolicy">
            <MaxFileSize>30MB</MaxFileSize>
        </triggeringPolicy>
    </appender>
    <!-- 异步输出 -->
    <appender name="ASYNC" class="ch.qos.logback.classic.AsyncAppender">
        <!-- 不丢失日志.默认的,如果队列的80%已满,则会丢弃TRACT、DEBUG、INFO级别的日志 -->
        <discardingThreshold>0</discardingThreshold>
        <!-- 更改默认的队列的深度,该值会影响性能.默认值为256 -->
        <queueSize>256</queueSize>
        <!-- 添加附加的appender,最多只能添加一个 -->
        <appender-ref ref="FILE"/>
    </appender>
    <!-- show parameters for ibatis sql 专为 ibatis 定制 -->
    <logger name="com.ibatis" level="DEBUG"/>
    <logger name="com.ibatis.common.jdbc.SimpleDataSource" level="DEBUG"/>
    <logger name="com.ibatis.common.jdbc.ScriptRunner" level="DEBUG"/>
    <logger name="com.ibatis.sqlmap.engine.impl.SqlMapClientDelegate" level="DEBUG"/>
    <logger name="java.sql.Connection" level="DEBUG"/>
    <logger name="java.sql.Statement" level="DEBUG"/>
    <logger name="java.sql.PreparedStatement" level="DEBUG"/>
    <!-- 日志输出级别 -->
    <root level="INFO">
        <appender-ref ref="STDOUT"/>
        <appender-ref ref="ASYNC"/>
    </root>
</configuration>
```

当`Logging Event`进入`AsyncAppender`后，`AsyncAppender`会调用`appender`方法，

`append`方法中在将event填入Buffer(这里选用的数据结构为BlockingQueue)中前，会先判断当前buffer的容量以及丢弃日志特性是否开启，

当消费能力不如生产能力时，`AsyncAppender`会超出Buffer容量的Logging Event的级别，进行丢弃，

作为消费速度一旦跟不上生产速度，中转buffer的溢出处理的一种方案。

`AsyncAppender`并不处理日志，只是将日志缓冲到一个`BlockingQueue`里面去，并在内部创建一个工作线程从队列头部获取日志，

之后将获取的日志循环记录到附加的其他`appender`上去，从而达到不阻塞主线程的效果。

因此`AsynAppender`仅仅充当事件转发器，必须引用另一个`appender`来做事。

## druid配置

```bash
# 配置监控统计拦截的filters，去掉后监控界面sql无法统计，'wall'用于防火墙（防止SQL注入）
spring.datasource.druid.filters=stat,wall,slf4j
```
