### 参考

- [一分钟学会spring注解之@Scope注解](https://mp.weixin.qq.com/s/3XXLJ74rR6pKLZ11V2gHzg)

### 1. `@Scope`注解是什么

```java
@Target({ElementType.TYPE, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface Scope {

    /**
     * Alias for {@link #scopeName}.
     * @see #scopeName
     */
    @AliasFor("scopeName")
    String value() default "";

    /**
     * Specifies the name of the scope to use for the annotated component/bean.
     * <p>Defaults to an empty string ({@code ""}) which implies
     * {@link ConfigurableBeanFactory#SCOPE_SINGLETON SCOPE_SINGLETON}.
     * @since 4.2
     * @see ConfigurableBeanFactory#SCOPE_PROTOTYPE
     * @see ConfigurableBeanFactory#SCOPE_SINGLETON
     * @see org.springframework.web.context.WebApplicationContext#SCOPE_REQUEST
     * @see org.springframework.web.context.WebApplicationContext#SCOPE_SESSION
     * @see #value
     */
    @AliasFor("value")
    String scopeName() default "";

    /**
     * Specifies whether a component should be configured as a scoped proxy
     * and if so, whether the proxy should be interface-based or subclass-based.
     * <p>Defaults to {@link ScopedProxyMode#DEFAULT}, which typically indicates
     * that no scoped proxy should be created unless a different default
     * has been configured at the component-scan instruction level.
     * <p>Analogous to {@code <aop:scoped-proxy/>} support in Spring XML.
     * @see ScopedProxyMode
     */
    ScopedProxyMode proxyMode() default ScopedProxyMode.DEFAULT;

}
```

@Scope注解是springIoc容器中的一个作用域，在 Spring IoC 容器中具有以下几种作用域：

- singleton单例模式, 全局有且仅有一个实例
- prototype原型模式, 每次获取Bean的时候会有一个新的实例
- request, request表示该针对每一次HTTP请求都会产生一个新的bean，同时该bean仅在当前HTTP request内有效
- session, session作用域表示该针对每一次HTTP请求都会产生一个新的bean，同时该bean仅在当前HTTP session内有效
- globalsession, global session作用域类似于标准的HTTP Session作用域，不过它仅仅在基于portlet的web应用中才有意义

### 2. `@Scope`注解怎么使用

`@Scope`注解默认的`singleton`实例，`singleton`实例的意思不管你使用多少次在springIOC容器中只会存在一个实例

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

    @Scope(value = ConfigurableBeanFactory.SCOPE_PROTOTYPE)
    @Bean(name = "apple")
    public Apple getApple() {
        System.out.println("给容器中添加Apple....");
        return new Apple("苹果");
    }

    @Scope(value = ConfigurableBeanFactory.SCOPE_SINGLETON)
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
    grape = (Grape)applicationContext.getBean("grape");
    System.out.println("Grape : " + grape.getName());

    Apple apple = (Apple)applicationContext.getBean("apple");
    System.out.println("Apple : " + apple.getName());
    apple = (Apple)applicationContext.getBean("apple");
    System.out.println("Apple : " + apple.getName());
}
```

测试结果

```java
给容器中添加Grape....
bean名称为===beanConfig
bean名称为===apple
bean名称为===grape
Grape : 葡萄
Grape : 葡萄
给容器中添加Apple....
Apple : 苹果
给容器中添加Apple....
Apple : 苹果
```
