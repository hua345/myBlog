### 参考

- [一分钟学会spring注解之@Conditional注解](https://mp.weixin.qq.com/s/b0OpbybsLjkZYLuwXF1AmA)

### 1. @Conditional注解是什么

`@Conditional`注解是可以根据一些自定义的条件动态的选择是否加载该bean到springIOC容器中去，如果看过springBoot源码的同学会发现，springBoot中大量使用了该注解

查看`@Conditional`源码你会发现它既可以作用在方法上，同时也可以作用在类上，源码如下:

```java
@Target({ElementType.TYPE, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface Conditional {

    /**
     * All {@link Condition Conditions} that must {@linkplain Condition#matches match}
     * in order for the component to be registered.
     */
    Class<? extends Condition>[] value();

}
```

从代码中可以看到，需要传入一个Class数组，并且需要继承`Condition`接口：

```java
@FunctionalInterface
public interface Condition {

    /**
     * Determine if the condition matches.
     * @param context the condition context
     * @param metadata metadata of the {@link org.springframework.core.type.AnnotationMetadata class}
     * or {@link org.springframework.core.type.MethodMetadata method} being checked
     * @return {@code true} if the condition matches and the component can be registered,
     * or {@code false} to veto the annotated component's registration
     */
    boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata);

}
```

### 2. `@Conditional`注解怎么使用

```java
@Data
public class Apple {
    private String name;

    public Apple(String name) {
        this.name = name;
    }
}
```

```java
@Data
public class Grape {
    private String name;

    public Grape(String name) {
        this.name = name;
    }
}
```

定义`Condition`接口实现

```java
public class WindowsCondition implements Condition {
    @Override
    public boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {
        //获取ioc使用的beanFactory
        ConfigurableListableBeanFactory beanFactory = context.getBeanFactory();
        //获取类加载器
        ClassLoader classLoader = context.getClassLoader();
        //获取当前环境信息
        Environment environment = context.getEnvironment();

        //获得当前系统名
        String osName = environment.getProperty("os.name");
        System.out.println("osName: " + osName);
        //包含Windows则说明是windows系统，返回true
        if (!StringUtils.isBlank(osName) && osName.contains("Windows")) {
            return true;
        }
        return false;
    }
}

```

```java
public class LinuxCondition implements Condition {
    @Override
    public boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {
        //获取ioc使用的beanFactory
        ConfigurableListableBeanFactory beanFactory = context.getBeanFactory();
        //获取类加载器
        ClassLoader classLoader = context.getClassLoader();
        //获取当前环境信息
        Environment environment = context.getEnvironment();

        //获得当前系统名
        String osName = environment.getProperty("os.name");
        System.out.println("osName: " + osName);
        //包含Windows则说明是windows系统，返回true
        if (!StringUtils.isBlank(osName) && osName.contains("Linux")) {
            return true;
        }
        return false;
    }
}
```

spring bean配置

```java
@Configuration
public class BeanConfig {

    @Conditional({WindowsCondition.class})
    @Bean(name = "apple")
    public Apple getApple() {
        System.out.println("给容器中添加Apple....");
        return new Apple("苹果");
    }

    @Conditional({LinuxCondition.class})
    @Bean(name = "grape")
    public Grape getGrape() {
        System.out.println("给容器中添加Grape....");
        return new Grape("葡萄");
    }
}
```

测试bean加载

```java
public static void main(String[] args) {
    AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(BeanConfig.class);
    String[] beanNames = applicationContext.getBeanDefinitionNames();
    for (String item : beanNames) {
        System.out.println("bean名称为===" + item);
    }
}
```

测试结果

```java
osName: Windows 10
给容器中添加Apple....
bean名称为===beanConfig
bean名称为===apple
```
