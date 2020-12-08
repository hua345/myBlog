# SpringBoot项目取消数据库配置

## 错误

```java
springboot项目启动时，如果没有配置数据库配置，启动时会抛出如下异常。

Description:

Cannot determine embedded database driver class for database type NONE

Action:

If you want an embedded database please put a supported one on the classpath.
If you have database settings to be loaded from a particular profile you may
need to active it (no profiles are currently active).
```

## 原因

springboot会自动注入数据源，而你却没有配，所以他就抛出该异常。

## 解决方法

如果你只是简单的想建个项目，并不需要数据库支持，那么你可以让他不去注入数据源。

```java
// 一般你启动springboot项目，都会写一个有@SpringBootApplication注解的类
// 你在这个注解中添加exclude={DataSourceAutoConfiguration.class,HibernateJpaAutoConfiguration.class}
// 即可无数据库运行
// 如下

@SpringBootApplication(exclude={DataSourceAutoConfiguration.class,HibernateJpaAutoConfiguration.class})
```
