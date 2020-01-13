### 参考

- [三分钟了解spring-bean生命周期之初始化和销毁的三种方式](https://mp.weixin.qq.com/s/ENaqhsYcNabSNLkZPU1xSg)
- [深入理解spring生命周期与BeanPostProcessor的实现原理](https://mp.weixin.qq.com/s/6c2-hbSkD84jClXevNTIlQ)

### 1. spring-bean生命周期之初始化和销毁有三种方式

- 注解bean之指定init-method/destroy-method
- 实现InitializingBean/DisposableBean接口
- @PostConstruct和@PreDestroy注解

#### 1.1 注解bean之指定init-method/destroy-method

```java
@Data
public class Book {
    private String name;

    public Book(String name) {
        this.name = name;
    }
    public void initBook(){
        System.out.println("初始化Book bean之前执行");
    }
    public void destroyBook(){
        System.out.println("Book bean销毁之前执行");
    }
}
```

添加Bean配置

```java
@Configuration
public class BookConfig {
    @Bean(value="book",initMethod="initBook",destroyMethod="destroyBook")
    public Book getBook() {
        System.out.println("创建book实例");
        return new Book("数学之美");
    }
}
```

#### 1.2 实现InitializingBean/DisposableBean接口

实现`InitializingBean`和`DisposableBean`接口

```java
@Data
public class Book1 implements InitializingBean, DisposableBean {
    private String name;

    public Book1(String name) {
        this.name = name;
    }
    @Override
    public void afterPropertiesSet(){
        System.out.println("初始化Book bean之前执行");
    }
    @Override
    public void destroy(){
        System.out.println("Book bean销毁之前执行");
    }
}
```

#### 1.3 @PostConstruct和@PreDestroy注解

```java
@Data
public class Book2 {
    private String name;

    public Book2(String name) {
        this.name = name;
    }

    @PostConstruct
    public void initBook() {
        System.out.println("初始化Book2 bean之前执行");
    }

    @PreDestroy
    public void destroyBook() {
        System.out.println("Book2 bean销毁之前执行");
    }
}
```

#### 1.4 添加Bean配置

```java
@Configuration
public class BookConfig {
    @Bean(value = "book", initMethod = "initBook", destroyMethod = "destroyBook")
    public Book getBook() {
        System.out.println("创建book实例");
        return new Book("数学之美");
    }

    @Bean
    public Book1 getBook1() {
        return new Book1("断舍离");
    }

    @Bean
    public Book2 getBook2() {
        return new Book2("非暴力沟通");
    }
}
```

#### 1.5测试Bean

```java
Book book = (Book)SpringContextHolder.getBean("book");
System.out.println(book.getName());
Book1 book1 = (Book1)SpringContextHolder.getBean("getBook1");
System.out.println(book1.getName());
Book2 book2 = (Book2)SpringContextHolder.getBean("getBook2");
System.out.println(book2.getName());
```

#### 1.6测试结果

```java
创建book实例
初始化Book bean之前执行
初始化Book1 bean之前执行
初始化Book2 bean之前执行
数学之美
断舍离
非暴力沟通
Book2 bean销毁之前执行
Book1 bean销毁之前执行
Book bean销毁之前执行
```

#### 1.7 SpringContextHolder

测试用到的工具类

```java
@Component
public class SpringContextHolder implements ApplicationContextAware {

    private static ApplicationContext ctx;

    @Override
    public void setApplicationContext(@Nonnull ApplicationContext applicationContext) {
        ctx = applicationContext;
    }
    /**
     * 根据注册的 beanName 找到在 Spring 中注册的 Bean
     * @param beanName beanName
     * @return spring 中的单例
     */
    public static Object getBean(String beanName) {
        return ctx.getBean(beanName);
    }
}

```

### spring-bean的统一前后置处理器BeanPostProcessor

#### 2.1 定义一个前置后置处理器MyBeanPostProcessor

```java
public class MyBeanPostProcessor implements BeanPostProcessor {
    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName)
            throws BeansException {
        // 这边只做简单打印   原样返回bean
        System.out.println("postProcessBeforeInitialization===="+beanName);
        return bean;
    }
    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName)
            throws BeansException {
        // 这边只做简单打印   原样返回bean
        System.out.println("postProcessAfterInitialization===="+beanName);
        return bean;
    }
}
```

#### 2.2 配置类中增加配置如下

```java
@Bean
public MyBeanPostProcessor getMyBeanPostProcessor(){
    return new MyBeanPostProcessor();
}
```

#### 2.3 运行测试结果如下

```java
postProcessBeforeInitialization====getBook2
初始化Book2 bean之前执行
postProcessAfterInitialization====getBook2
postProcessBeforeInitialization====redisCacheTemplate
postProcessAfterInitialization====redisCacheTemplate
```

Spring所有的bean都会被统一处理
