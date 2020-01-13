
### @Component和@Configuration之间的区别

从[@Component](#Component),[@Configuration](#Configuration),[@Service](#Service),[Controller](#Controller),[Repository](#Repository)注解实现类可以看出都等同于[@Component](#Component)注解，只是约定好用于定义不同业务场景bean。

|注解|业务场景说明|
|------------|-------------|
|@Configuration|声明当前类为配置类|
|@Component|泛指组件，当组件不好归类的时候，我们可以使用这个注解进行标注|
|@Controller|声明当前类为控制层类|
|@Service|声明当前类为业务层类|
|@Repository|声明当前类为数据访问层类|

### @Configuration

`org.springframework.context.annotation.Configuration`

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Component
public @interface Configuration {

    /**
     * Explicitly specify the name of the Spring bean definition associated with the
     * {@code @Configuration} class. If left unspecified (the common case), a bean
     * name will be automatically generated.
     * <p>The custom name applies only if the {@code @Configuration} class is picked
     * up via component scanning or supplied directly to an
     * {@link AnnotationConfigApplicationContext}. If the {@code @Configuration} class
     * is registered as a traditional XML bean definition, the name/id of the bean
     * element will take precedence.
     * @return the explicit component name, if any (or empty String otherwise)
     * @see AnnotationBeanNameGenerator
     */
    @AliasFor(annotation = Component.class)
    String value() default "";

}
```

### @Component

`org.springframework.stereotype.Component`

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Indexed
public @interface Component {

    /**
     * The value may indicate a suggestion for a logical component name,
     * to be turned into a Spring bean in case of an autodetected component.
     * @return the suggested component name, if any (or empty String otherwise)
     */
    String value() default "";

}
```

### @Controller

`org.springframework.stereotype.Controller`

```java
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Component
public @interface Controller {

    /**
     * The value may indicate a suggestion for a logical component name,
     * to be turned into a Spring bean in case of an autodetected component.
     * @return the suggested component name, if any (or empty String otherwise)
     */
    @AliasFor(annotation = Component.class)
    String value() default "";

}
```

### @Service

`org.springframework.stereotype.Service`

```java
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Component
public @interface Service {

    /**
     * The value may indicate a suggestion for a logical component name,
     * to be turned into a Spring bean in case of an autodetected component.
     * @return the suggested component name, if any (or empty String otherwise)
     */
    @AliasFor(annotation = Component.class)
    String value() default "";

}
```

### @Repository

`org.springframework.stereotype.Repository`

```java
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Component
public @interface Repository {

    /**
     * The value may indicate a suggestion for a logical component name,
     * to be turned into a Spring bean in case of an autodetected component.
     * @return the suggested component name, if any (or empty String otherwise)
     */
    @AliasFor(annotation = Component.class)
    String value() default "";

}
```
