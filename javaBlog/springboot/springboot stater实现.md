# springboot stater实现


`SpringBoot` 在启动时会去依赖的starter包中寻找`resources/META-INF/spring.factories` 文件，然后根据文件中配置的Jar包去扫描项目所依赖的Jar包，这类似于 Java 的`SPI`机制

根据 `@Conditional`注解的条件，进行自动配置并将`Bean`注入`Spring Context` 上下文当中。

我们也可以使用`@ImportAutoConfiguration({MyServiceAutoConfiguration.class})` 指定自动配置哪些类

可以在[maven springboot](https://mvnrepository.com/artifact/org.springframework.boot?p=1)和[maven springcloud](https://mvnrepository.com/artifact/org.springframework.cloud)上查看有哪些stater

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-configuration-processor</artifactId>
        <optional>true</optional>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-autoconfigure</artifactId>
    </dependency>
</dependencies>
```

`spring-boot-configuration-processor` 的作用是编译时生成 `spring-configuration-metadata.json`，此文件主要给IDE使用.

我们日常使用的Spring`官方的Starter`一般采取`spring-boot-starter-{name}` 的命名方式，如 `spring-boot-starter-web`。

而`非官方的Starter`，官方建议 `artifactId` 命名应遵循`{name}-spring-boot-starter`的格式。 例如：`hello-spring-boot-starter`

我们在[https://start.spring.io/](https://start.spring.io/)生成项目



