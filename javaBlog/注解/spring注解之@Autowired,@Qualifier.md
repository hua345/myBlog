# @Autowired

## [@Autowired](#Autowired)

> Spring Team recommends: "Always use constructor based dependency injection in your beans. Always use assertions for mandatory dependencies
>
> Spring团队建议: 使用构造函数注入

这个注解可以用于`属性`，`setter` 方法，还有`构造器`上，这个注解用于注入依赖的对象。

有的时候写在变量上会报`空指针异常`NPE，然后通过写在`构造器`上就解决了此问题

```java
@Autowired
private User user;
private String school;

public UserAccountServiceImpl(){
    this.school = user.getSchool();
}
```

因为Java类会`先执行构造方法`，然后再给注解了`@Autowired` 的`user`注入值，所以在`执行构造方法的时候`，就会报错。

```java
private User user;
private String school;

@Autowired
public UserAccountServiceImpl(User user){
    this.user = user;
    this.school = user.getSchool();
}
```

使用`构造器注入`的方法，可以`明确成员变量的加载顺序`。

Java变量的初始化顺序为:`静态变量或静态语句块–>实例变量或初始化语句块–>构造方法–>@Autowired`

## [@Qualifier](#Qualifier)

`@Autowired` 是根据类型进行自动装配的。如果有两个实现类，还要使用`@Autowired`注解，可以加`@Qualifier`指定需要注入的实现类。

`qualifier`的意思是合格者，通过这个标识，表明了哪个实现类才是我们所需要的.

## [@Resource](#Resource)

`@Resource` 的作用相当于`@Autowired`，只不过`@Autowired` 按 byType 自动注入，而`@Resource` 默认按 byName 自动注入罢了。

`@Resource` 装配顺序

- 如果既没有指定 name，又没有指定 type，则自动按照 byName 方式进行装配；如果没有匹配，则回退为一个原始类型进行匹配，如果匹配则自动装配
- 如果同时指定了 name 和 type，则从 Spring 上下文中找到唯一匹配的 bean 进行装配，找不到则抛出异常
- 如果指定了 name，则从上下文中查找名称（id）匹配的 bean 进行装配，找不到则抛出异常
- 如果指定了 type，则从上下文中找到类型匹配的唯一 bean 进行装配，找不到或者找到多个，都会抛出异常

### 测试用例

```java
@Data
public class Fruit {
    private String name;

    public Fruit(String name) {
        this.name = name;
    }
}
```

```java
public class Apple extends Fruit{
    public Apple(String name) {
        super(name);
    }
}
```

```java
public class Banana extends Fruit {
    public Banana(String name) {
        super(name);
    }
}
```

```java
public interface IFruitService {
    /**
     * 获取水果
     * @return
     */
    public Fruit getFruit();
}
```

```java
@Service("fruitAppleServiceImpl")
public class FruitAppleServiceImpl implements IFruitService {
    /**
     * 获取水果
     *
     * @return
     */
    @Override
    public Apple getFruit() {
        return new Apple("苹果");
    }
}
```

```java
@Service("fruitBananaServiceImpl")
public class FruitBananaServiceImpl implements IFruitService {
    /**
     * 获取水果
     *
     * @return
     */
    @Override
    public Banana getFruit() {
        return new Banana("香蕉");
    }
}
```

测试用例

```java
    @Autowired
    @Qualifier(value = "fruitBananaServiceImpl")
    private IFruitService fruitService;

    @Resource(name = "fruitAppleServiceImpl")
    private IFruitService fruitService2;

    @Test
    public void fruitTest(){
        log.info(fruitService.getFruit().getName());
        log.info(fruitService2.getFruit().getName());
    }
```

测试结果

```java
香蕉
苹果
```

### @Autowired

`org.springframework.beans.factory.annotation.Autowired`

```java
@Target({ElementType.CONSTRUCTOR, ElementType.METHOD, ElementType.PARAMETER, ElementType.FIELD, ElementType.ANNOTATION_TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface Autowired {

    /**
     * Declares whether the annotated dependency is required.
     * <p>Defaults to {@code true}.
     */
    boolean required() default true;

}
```

### @Resource

```java
@Target({TYPE, FIELD, METHOD})
@Retention(RUNTIME)
public @interface Resource {
    /**
     * The JNDI name of the resource.  For field annotations,
     * the default is the field name.  For method annotations,
     * the default is the JavaBeans property name corresponding
     * to the method.  For class annotations, there is no default
     * and this must be specified.
     */
    String name() default "";

    /**
     * The name of the resource that the reference points to. It can
     * link to any compatible resource using the global JNDI names.
     *
     * @since Common Annotations 1.1
     */

    String lookup() default "";

    /**
     * The Java type of the resource.  For field annotations,
     * the default is the type of the field.  For method annotations,
     * the default is the type of the JavaBeans property.
     * For class annotations, there is no default and this must be
     * specified.
     */
    Class<?> type() default java.lang.Object.class;

    /**
     * The two possible authentication types for a resource.
     */
    enum AuthenticationType {
            CONTAINER,
            APPLICATION
    }

    /**
     * The authentication type to use for this resource.
     * This may be specified for resources representing a
     * connection factory of any supported type, and must
     * not be specified for resources of other types.
     */
    AuthenticationType authenticationType() default AuthenticationType.CONTAINER;

    /**
     * Indicates whether this resource can be shared between
     * this component and other components.
     * This may be specified for resources representing a
     * connection factory of any supported type, and must
     * not be specified for resources of other types.
     */
    boolean shareable() default true;

    /**
     * A product specific name that this resource should be mapped to.
     * The name of this resource, as defined by the <code>name</code>
     * element or defaulted, is a name that is local to the application
     * component using the resource.  (It's a name in the JNDI
     * <code>java:comp/env</code> namespace.)  Many application servers
     * provide a way to map these local names to names of resources
     * known to the application server.  This mapped name is often a
     * <i>global</i> JNDI name, but may be a name of any form. <p>
     *
     * Application servers are not required to support any particular
     * form or type of mapped name, nor the ability to use mapped names.
     * The mapped name is product-dependent and often installation-dependent.
     * No use of a mapped name is portable.
     */
    String mappedName() default "";

    /**
     * Description of this resource.  The description is expected
     * to be in the default language of the system on which the
     * application is deployed.  The description can be presented
     * to the Deployer to help in choosing the correct resource.
     */
    String description() default "";
}
```

### @Qualifier

`org.springframework.beans.factory.annotation.Qualifier`

```java
/**
 * This annotation may be used on a field or parameter as a qualifier for
 * candidate beans when autowiring. It may also be used to annotate other
 * custom annotations that can then in turn be used as qualifiers.
 *
 * @author Mark Fisher
 * @author Juergen Hoeller
 * @since 2.5
 * @see Autowired
 */
@Target({ElementType.FIELD, ElementType.METHOD, ElementType.PARAMETER, ElementType.TYPE, ElementType.ANNOTATION_TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Inherited
@Documented
public @interface Qualifier {

    String value() default "";

}
```
