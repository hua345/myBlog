### 参考

- [https://spring.io/guides/gs/caching/](https://spring.io/guides/gs/caching/)
- [Spring Cache 使用 ---@EnableCaching @Cacheable 注解](https://blog.csdn.net/zl_momomo/article/details/80403564)

#### 1.添加依赖

```gradle
//gradle
dependencies {
    compile("org.springframework.boot:spring-boot-starter-cache")
}
//maven
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-cache</artifactId>
</dependency>
```

#### 2.redis配置

```java
@Configuration
@EnableAutoConfiguration
@EnableCaching
public class RedisConfig extends CachingConfigurerSupport {
    /**
     * LettuceConnectionFactory redisConnectionFactory
     *
     * @param lettuceConnectionFactory 生菜连接池
     * @return redis模板
     */
    @Bean
    public RedisTemplate<String, Serializable> redisCacheTemplate(LettuceConnectionFactory lettuceConnectionFactory) {
        RedisTemplate<String, Serializable> template = new RedisTemplate<>();
        template.setKeySerializer(new StringRedisSerializer());
        template.setValueSerializer(new GenericJackson2JsonRedisSerializer());
        template.setConnectionFactory(lettuceConnectionFactory);
        return template;
    }

    /**
     * 缓存管理器
     * @param lettuceConnectionFactory 生菜连接池
     * @return 缓存管理器
     */
    @Bean
    public CacheManager cacheManager(LettuceConnectionFactory lettuceConnectionFactory) {
        RedisCacheManager.RedisCacheManagerBuilder builder = RedisCacheManager
                .RedisCacheManagerBuilder
                .fromConnectionFactory(lettuceConnectionFactory);
        return builder.build();
    }
}
```

#### 3.1 `@EnableCaching`注解使springboot缓存生效

@EnableCaching注释触发一个前置处理器`PostConstruct`，它检查每个Spring bean是否存在公共方法上的缓存注释。
如果找到[@Cacheable](#@Cacheable), [@CachePut](#@Cacheable)and [@CacheEvict](#@Cacheable)注释，则自动创建代理以拦截方法调用并相应地处理缓存行为。

Spring Boot会自动配置合适的`CacheManager`作为缓存。

```java
package hello;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cache.annotation.EnableCaching;

@SpringBootApplication
@EnableCaching
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

#### 3.2 [@Cacheable](#@Cacheable)注解说明

在方法调用前先判断缓存中是否有值，如果有值返回结果，如果没有调用方法缓存结果

##### 3.2.1 自定义key

默认key生成：
默认key的生成按照以下规则:

- 如果没有参数,则使用0作为key
- 如果只有一个参数，使用该参数作为key
- 如果又多个参数，使用包含所有参数的hashCode作为key

自定义key的生成：

```java
@Cacheable(value="books", key="book.isbn", sync = true)
public Book getByIsbn(Book book) {
    simulateSlowService();
    return new Book(book.getIsbn(), "Some book");
}
```

##### 3.2.2 缓存的同步sync

在多线程环境下，某些操作可能使用相同参数同步调用。
默认情况下，缓存不锁定任何资源，可能导致多次计算，而违反了缓存的目的。
对于这些特定的情况，属性 sync 可以指示底层将缓存锁住，
使只有一个线程可以进入计算，而其他线程堵塞，直到返回结果更新到缓存中。

```java
@Cacheable(value="books", key="isbn", sync = true)
public Book getByIsbn(String isbn) {
    simulateSlowService();
    return new Book(isbn, "Some book");
}
```

#### 3.2.3 condition属性指定发生的条件

```java
@Cacheable(value="books", key="#book.isbn", sync = true, condition = "#book.isbn.length() >= 2")
public Book getByIsbn(Book book) {
    simulateSlowService();
    return new Book(book.getIsbn(), "Some book");
}
```

#### 3.3 @CachePut

每次都会执行该方法，并将执行结果以键值对的形式存入指定的缓存中。

```java
@CachePut(value = "books", key="book.isbn")
public void updateBook(Book book)
```

#### 3.4 @CacheEvict

清除对应的内存

```java
@CacheEvict(value = "books", key="isbn")
public void deleteBook(String isbn)
```

#### 4. 缓存使用

```java
import org.springframework.cache.annotation.Cacheable;

@Component
public class BookService {
    @Cacheable("books")
    public Book getByIsbn(String isbn) {
        simulateSlowService();
        return new Book(isbn, "Some book");
    }
    // Don't do this at home
    private void simulateSlowService() {
        try {
            long time = 3000L;
            Thread.sleep(time);
        } catch (InterruptedException e) {
            throw new IllegalStateException(e);
        }
    }
}
```

#### 5. 单元测试

```java
@RunWith(SpringRunner.class)
@SpringBootTest(classes = Application.class)
public class SpringBootLettuceRedisApplicationTests {

    private static final Logger log = LoggerFactory.getLogger(SpringBootLettuceRedisApplicationTests.class);

    @Autowired
    private BookService bookService;

    @Test
    public void cacheTest() {
        Book book1 = new Book("1","断舍离");
        Book book2 = new Book("22","非暴力沟通");
        log.info("{}",bookService.getByIsbn(book1));
        log.info("{}",bookService.getByIsbn(book2));
        log.info("{}",bookService.getByIsbn(book1));
        log.info("{}",bookService.getByIsbn(book2));
    }
}
```

#### @Cacheable

```java
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Inherited
@Documented
public @interface Cacheable {

    /**
     * Alias for {@link #cacheNames}.
     */
    @AliasFor("cacheNames")
    String[] value() default {};

    /**
     * Names of the caches in which method invocation results are stored.
     * <p>Names may be used to determine the target cache (or caches), matching
     * the qualifier value or bean name of a specific bean definition.
     * @since 4.2
     * @see #value
     * @see CacheConfig#cacheNames
     */
    @AliasFor("value")
    String[] cacheNames() default {};

    /**
     * Spring Expression Language (SpEL) expression for computing the key dynamically.
     * <p>Default is {@code ""}, meaning all method parameters are considered as a key,
     * unless a custom {@link #keyGenerator} has been configured.
     * <p>The SpEL expression evaluates against a dedicated context that provides the
     * following meta-data:
     * <ul>
     * <li>{@code #root.method}, {@code #root.target}, and {@code #root.caches} for
     * references to the {@link java.lang.reflect.Method method}, target object, and
     * affected cache(s) respectively.</li>
     * <li>Shortcuts for the method name ({@code #root.methodName}) and target class
     * ({@code #root.targetClass}) are also available.
     * <li>Method arguments can be accessed by index. For instance the second argument
     * can be accessed via {@code #root.args[1]}, {@code #p1} or {@code #a1}. Arguments
     * can also be accessed by name if that information is available.</li>
     * </ul>
     */
    String key() default "";

    /**
     * The bean name of the custom {@link org.springframework.cache.interceptor.KeyGenerator}
     * to use.
     * <p>Mutually exclusive with the {@link #key} attribute.
     * @see CacheConfig#keyGenerator
     */
    String keyGenerator() default "";

    /**
     * The bean name of the custom {@link org.springframework.cache.CacheManager} to use to
     * create a default {@link org.springframework.cache.interceptor.CacheResolver} if none
     * is set already.
     * <p>Mutually exclusive with the {@link #cacheResolver}  attribute.
     * @see org.springframework.cache.interceptor.SimpleCacheResolver
     * @see CacheConfig#cacheManager
     */
    String cacheManager() default "";

    /**
     * The bean name of the custom {@link org.springframework.cache.interceptor.CacheResolver}
     * to use.
     * @see CacheConfig#cacheResolver
     */
    String cacheResolver() default "";

    /**
     * Spring Expression Language (SpEL) expression used for making the method
     * caching conditional.
     * <p>Default is {@code ""}, meaning the method result is always cached.
     * <p>The SpEL expression evaluates against a dedicated context that provides the
     * following meta-data:
     * <ul>
     * <li>{@code #root.method}, {@code #root.target}, and {@code #root.caches} for
     * references to the {@link java.lang.reflect.Method method}, target object, and
     * affected cache(s) respectively.</li>
     * <li>Shortcuts for the method name ({@code #root.methodName}) and target class
     * ({@code #root.targetClass}) are also available.
     * <li>Method arguments can be accessed by index. For instance the second argument
     * can be accessed via {@code #root.args[1]}, {@code #p1} or {@code #a1}. Arguments
     * can also be accessed by name if that information is available.</li>
     * </ul>
     */
    String condition() default "";

    /**
     * Spring Expression Language (SpEL) expression used to veto method caching.
     * <p>Unlike {@link #condition}, this expression is evaluated after the method
     * has been called and can therefore refer to the {@code result}.
     * <p>Default is {@code ""}, meaning that caching is never vetoed.
     * <p>The SpEL expression evaluates against a dedicated context that provides the
     * following meta-data:
     * <ul>
     * <li>{@code #result} for a reference to the result of the method invocation. For
     * supported wrappers such as {@code Optional}, {@code #result} refers to the actual
     * object, not the wrapper</li>
     * <li>{@code #root.method}, {@code #root.target}, and {@code #root.caches} for
     * references to the {@link java.lang.reflect.Method method}, target object, and
     * affected cache(s) respectively.</li>
     * <li>Shortcuts for the method name ({@code #root.methodName}) and target class
     * ({@code #root.targetClass}) are also available.
     * <li>Method arguments can be accessed by index. For instance the second argument
     * can be accessed via {@code #root.args[1]}, {@code #p1} or {@code #a1}. Arguments
     * can also be accessed by name if that information is available.</li>
     * </ul>
     * @since 3.2
     */
    String unless() default "";

    /**
     * Synchronize the invocation of the underlying method if several threads are
     * attempting to load a value for the same key. The synchronization leads to
     * a couple of limitations:
     * <ol>
     * <li>{@link #unless()} is not supported</li>
     * <li>Only one cache may be specified</li>
     * <li>No other cache-related operation can be combined</li>
     * </ol>
     * This is effectively a hint and the actual cache provider that you are
     * using may not support it in a synchronized fashion. Check your provider
     * documentation for more details on the actual semantics.
     * @since 4.3
     * @see org.springframework.cache.Cache#get(Object, Callable)
     */
    boolean sync() default false;
}
```
