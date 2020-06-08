### 参考

- [一分钟学会spring注解之@Conditional注解](https://mp.weixin.qq.com/s/b0OpbybsLjkZYLuwXF1AmA)
- [SpringBoot @ConditionalOnBean、@ConditionalOnMissingBean注解源码分析与示例](https://blog.csdn.net/xcy1193068639/article/details/81517456)

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

### @OnBeanCondition,@ConditionalOnMissingBean,@ConditionalOnBean

```java
@Target({ElementType.TYPE, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Conditional({OnBeanCondition.class})
public @interface ConditionalOnMissingBean {
    Class<?>[] value() default {};

    String[] type() default {};
}
```

`@ConditionalOnMissingBean`使用了`@Conditional`注解，`OnBeanCondition`作为条件类

```java
public interface ConfigurationCondition extends Condition {
    ConfigurationCondition.ConfigurationPhase getConfigurationPhase();

    public static enum ConfigurationPhase {
        PARSE_CONFIGURATION,
        REGISTER_BEAN;

        private ConfigurationPhase() {
        }
    }
}
@Order(2147483647)
class OnBeanCondition extends FilteringSpringBootCondition implements ConfigurationCondition {
    public static final String FACTORY_BEAN_OBJECT_TYPE = "factoryBeanObjectType";

    OnBeanCondition() {
    }

    public ConfigurationPhase getConfigurationPhase() {
        return ConfigurationPhase.REGISTER_BEAN;
    }
}
```

它继承了`SpringBootCondition`类，`OnBeanCondition`类中没有`matches`方法，而`SpringBootCondition`类中有实现`matches`方法。

```java
public abstract class SpringBootCondition implements Condition {
    private final Log logger = LogFactory.getLog(this.getClass());

    public SpringBootCondition() {
    }

    public final boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {
        String classOrMethodName = getClassOrMethodName(metadata);

        try {
            ConditionOutcome outcome = this.getMatchOutcome(context, metadata);
            this.logOutcome(classOrMethodName, outcome);
            this.recordEvaluation(context, classOrMethodName, outcome);
            return outcome.isMatch();
        } catch (NoClassDefFoundError var5) {
            throw new IllegalStateException("Could not evaluate condition on " + classOrMethodName + " due to " + var5.getMessage() + " not found. Make sure your own configuration does not rely on that class. This can also happen if you are @ComponentScanning a springframework package (e.g. if you put a @ComponentScan in the default package by mistake)", var5);
        } catch (RuntimeException var6) {
            throw new IllegalStateException("Error processing condition on " + this.getName(metadata), var6);
        }
    }
}
```

```java
class OnBeanCondition extends FilteringSpringBootCondition implements ConfigurationCondition {
    public static final String FACTORY_BEAN_OBJECT_TYPE = "factoryBeanObjectType";

    OnBeanCondition() {
    }
    public ConditionOutcome getMatchOutcome(ConditionContext context, AnnotatedTypeMetadata metadata) {
        ConditionMessage matchMessage = ConditionMessage.empty();
        OnBeanCondition.BeanSearchSpec spec;
        OnBeanCondition.MatchResult matchResult;
        String reason;
        if (metadata.isAnnotated(ConditionalOnBean.class.getName())) {
            spec = new OnBeanCondition.BeanSearchSpec(context, metadata, ConditionalOnBean.class);
            matchResult = this.getMatchingBeans(context, spec);
            if (!matchResult.isAllMatched()) {
                reason = this.createOnBeanNoMatchReason(matchResult);
                return ConditionOutcome.noMatch(ConditionMessage.forCondition(ConditionalOnBean.class, new Object[]{spec}).because(reason));
            }

            matchMessage = matchMessage.andCondition(ConditionalOnBean.class, new Object[]{spec}).found("bean", "beans").items(Style.QUOTE, matchResult.getNamesOfAllMatches());
        }

        if (metadata.isAnnotated(ConditionalOnSingleCandidate.class.getName())) {
            OnBeanCondition.BeanSearchSpec spec = new OnBeanCondition.SingleCandidateBeanSearchSpec(context, metadata, ConditionalOnSingleCandidate.class);
            matchResult = this.getMatchingBeans(context, spec);
            if (!matchResult.isAllMatched()) {
                return ConditionOutcome.noMatch(ConditionMessage.forCondition(ConditionalOnSingleCandidate.class, new Object[]{spec}).didNotFind("any beans").atAll());
            }

            if (!this.hasSingleAutowireCandidate(context.getBeanFactory(), matchResult.getNamesOfAllMatches(), spec.getStrategy() == SearchStrategy.ALL)) {
                return ConditionOutcome.noMatch(ConditionMessage.forCondition(ConditionalOnSingleCandidate.class, new Object[]{spec}).didNotFind("a primary bean from beans").items(Style.QUOTE, matchResult.getNamesOfAllMatches()));
            }

            matchMessage = matchMessage.andCondition(ConditionalOnSingleCandidate.class, new Object[]{spec}).found("a primary bean from beans").items(Style.QUOTE, matchResult.getNamesOfAllMatches());
        }

        if (metadata.isAnnotated(ConditionalOnMissingBean.class.getName())) {
            spec = new OnBeanCondition.BeanSearchSpec(context, metadata, ConditionalOnMissingBean.class);
            matchResult = this.getMatchingBeans(context, spec);
            if (matchResult.isAnyMatched()) {
                reason = this.createOnMissingBeanNoMatchReason(matchResult);
                return ConditionOutcome.noMatch(ConditionMessage.forCondition(ConditionalOnMissingBean.class, new Object[]{spec}).because(reason));
            }

            matchMessage = matchMessage.andCondition(ConditionalOnMissingBean.class, new Object[]{spec}).didNotFind("any beans").atAll();
        }

        return ConditionOutcome.match(matchMessage);
    }
}
```

```java
// ConditionalOnBean
public boolean isAllMatched() {
    return this.unmatchedAnnotations.isEmpty() && this.unmatchedNames.isEmpty() && this.unmatchedTypes.isEmpty();
}

// ConditionalOnMissingBean
public boolean isAnyMatched() {
    return !this.matchedAnnotations.isEmpty() || !this.matchedNames.isEmpty() || !this.matchedTypes.isEmpty();
}
```

`@ConditionalOnBean`如果匹配到Bean,则注入IOC容器
`@ConditionalOnMissingBean`如果没有匹配到Bean,则注入IOC容器

```java
@Data
public class Computer {
    private String name;

    public Computer(String name){
        this.name =name;
    }
}
```

spring bean配置

```java
@Configuration
public class BeanConfig {

    @Bean(name = "笔记本电脑")
    public Computer computer1() {
        return new Computer("笔记本电脑");
    }

    @ConditionalOnBean(name = {"笔记本电脑"})
    @Bean("ipad")
    public Computer computer2() {
        return new Computer("ipad");
    }

    @ConditionalOnMissingBean(Computer.class)
    @Bean("备用电脑")
    public Computer computer3() {
        return new Computer("备用电脑");
    }

    public static void main(String[] args) {
        AnnotationConfigApplicationContext applicationContext = new AnnotationConfigApplicationContext(BeanConfig.class);
        String[] beanNames = applicationContext.getBeanDefinitionNames();
        for (String item : beanNames) {
            System.out.println("bean名称为===" + item);
        }
    }
}
```

测试结果

```java
bean名称为===beanConfig
bean名称为===笔记本电脑
bean名称为===ipad
```
