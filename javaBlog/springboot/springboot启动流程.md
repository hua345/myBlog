# springboot启动流程

## springboot启动类

```java
@SpringBootApplication
public class SpringbootJunitTestApplication {

	public static void main(String[] args) {
		SpringApplication.run(SpringbootJunitTestApplication.class, args);
	}
}
```

## SpringApplication

```java
// 实例化SpringApplication并调用run方法
public static ConfigurableApplicationContext run(Class<?>[] primarySources, String[] args) {
    return (new SpringApplication(primarySources)).run(args);
}
public SpringApplication(ResourceLoader resourceLoader, Class<?>... primarySources) {
    // 读取META-INF/spring.factories目录下spi配置信息
    // 配置应用程序启动前的初始化对象
    this.setInitializers(this.getSpringFactoriesInstances(ApplicationContextInitializer.class));
    // 配置应用程序启动前的监听器
    this.setListeners(this.getSpringFactoriesInstances(ApplicationListener.class));
    this.mainApplicationClass = this.deduceMainApplicationClass();
}

public ConfigurableApplicationContext run(String... args) {
    // 通知监听者启动开始
    listeners.starting();
    try {
        // 读取配置文件
        ApplicationArguments applicationArguments = new DefaultApplicationArguments(args);
		ConfigurableEnvironment environment = prepareEnvironment(listeners, applicationArguments);
        // 创建应用程序上下文...此处创建了beanfactory
        context = createApplicationContext();
        prepareContext(context, environment, listeners, applicationArguments, printedBanner);
        // 刷新上下文（spring启动核心）
        refreshContext(context);
        afterRefresh(context, applicationArguments);
        // 启动完成通知
        listeners.started(context);
        // 运行实现ApplicationRunner、CommandLineRunner的bean
        callRunners(context, applicationArguments);
    }
    catch (Throwable ex) {
        handleRunFailure(context, ex, exceptionReporters, listeners);
        throw new IllegalStateException(ex);
    }

    try {
        listeners.running(context);
    }
    catch (Throwable ex) {
        handleRunFailure(context, ex, exceptionReporters, null);
        throw new IllegalStateException(ex);
    }
    return context;
}
```

### createApplicationContext

```java
protected ConfigurableApplicationContext createApplicationContext() {
    Class<?> contextClass = this.applicationContextClass;
    if (contextClass == null) {
        try {
            switch (this.webApplicationType) {
            case SERVLET:
                contextClass = Class.forName(DEFAULT_SERVLET_WEB_CONTEXT_CLASS);
                break;
            case REACTIVE:
                contextClass = Class.forName(DEFAULT_REACTIVE_WEB_CONTEXT_CLASS);
                break;
            default:
                contextClass = Class.forName(DEFAULT_CONTEXT_CLASS);
            }
        }
        catch (ClassNotFoundException ex) {
            throw new IllegalStateException(
                    "Unable create a default ApplicationContext, please specify an ApplicationContextClass", ex);
        }
    }
    return (ConfigurableApplicationContext) BeanUtils.instantiateClass(contextClass);
}

public class AnnotationConfigServletWebServerApplicationContext extends ServletWebServerApplicationContext
		implements AnnotationConfigRegistry {

	private final AnnotatedBeanDefinitionReader reader;

	private final ClassPathBeanDefinitionScanner scanner;

	private final Set<Class<?>> annotatedClasses = new LinkedHashSet<>();

	/**
	 * Create a new {@link AnnotationConfigServletWebServerApplicationContext} that needs
	 * to be populated through {@link #register} calls and then manually
	 * {@linkplain #refresh refreshed}.
	 */
	public AnnotationConfigServletWebServerApplicationContext() {
		this.reader = new AnnotatedBeanDefinitionReader(this);
		this.scanner = new ClassPathBeanDefinitionScanner(this);
	}
}
```
