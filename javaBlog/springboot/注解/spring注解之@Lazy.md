### 参考

- [一分钟学会spring注解之@Lazy注解](https://mp.weixin.qq.com/s/Wxm_fWa7LhSdBfbhgZJlAQ)

#### 1. @Lazy注解是什么

```java
/**
 * Indicates whether a bean is to be lazily initialized.
 *  #@Lazy注解用于标识bean是否需要延迟加载
 * <p>May be used on any class directly or indirectly annotated with {@link
 * org.springframework.stereotype.Component @Component} or on methods annotated with
 * {@link Bean @Bean}.
 *  #可以直接作用在`@Component`类和`@Bean`注解标识的方法上
 * <p>If this annotation is not present on a {@code @Component} or {@code @Bean} definition,
 * eager initialization will occur. If present and set to {@code true}, the {@code @Bean} or
 * {@code @Component} will not be initialized until referenced by another bean or explicitly
 * retrieved from the enclosing {@link org.springframework.beans.factory.BeanFactory
 * BeanFactory}. If present and set to {@code false}, the bean will be instantiated on
 * startup by bean factories that perform eager initialization of singletons.
 * 
 * <p>If Lazy is present on a {@link Configuration @Configuration} class, this
 * indicates that all {@code @Bean} methods within that {@code @Configuration}
 * should be lazily initialized. If {@code @Lazy} is present and false on a {@code @Bean}
 * method within a {@code @Lazy}-annotated {@code @Configuration} class, this indicates
 * overriding the 'default lazy' behavior and that the bean should be eagerly initialized.
 * #如果作用在`@Configuration`注解标识的类上，则@Configuration中的所有bean都会被懒加载。
 *
 * <p>In addition to its role for component initialization, this annotation may also be placed
 * on injection points marked with {@link org.springframework.beans.factory.annotation.Autowired}
 * or {@link javax.inject.Inject}: In that context, it leads to the creation of a
 * lazy-resolution proxy for all affected dependencies, as an alternative to using
 * {@link org.springframework.beans.factory.ObjectFactory} or {@link javax.inject.Provider}.
 *
 * @author Chris Beams
 * @author Juergen Hoeller
 * @since 3.0
 * @see Primary
 * @see Bean
 * @see Configuration
 * @see org.springframework.stereotype.Component
 */
@Target({ElementType.TYPE, ElementType.METHOD, ElementType.CONSTRUCTOR, ElementType.PARAMETER, ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface Lazy {

    /**
     * Whether lazy initialization should occur.
     */
    boolean value() default true;
}
```

`@Lazy`注解注解的作用主要是减少springIOC容器启动的加载时间

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

spring bean配置

```java
@Configuration
public class BeanConfig {

    @Bean(name = "apple")
    public Apple getApple() {
        System.out.println("给容器中添加Apple....");
        return new Apple("苹果");
    }

    @Lazy
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
    Grape grape = (Grape)applicationContext.getBean("grape");
    System.out.println("Grape : " + grape.getName());
    Apple apple = (Apple)applicationContext.getBean("apple");
    System.out.println("Apple : " + apple.getName());
}
```

测试结果

```java
给容器中添加Apple....
bean名称为===beanConfig
bean名称为===apple
bean名称为===grape
14:25:38.672 [main] DEBUG org.springframework.beans.factory.support.DefaultListableBeanFactory - Creating shared instance of singleton bean 'grape'
给容器中添加Grape....
Grape : 葡萄
Apple : 苹果
```
