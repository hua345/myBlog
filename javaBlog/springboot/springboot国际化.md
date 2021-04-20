# sprintboot国际化

```java
@Configuration
public class Internationalization implements  WebMvcConfigurer {
    @Bean
    public LocaleResolver localeResolver() {
        SessionLocaleResolver sessionLocaleResolver = new SessionLocaleResolver();
        sessionLocaleResolver.setDefaultLocale(Locale.SIMPLIFIED_CHINESE);
        return sessionLocaleResolver;
    }

    @Bean
    public LocaleChangeInterceptor localeChangeInterceptor() {
        LocaleChangeInterceptor localeChangeInterceptor = new LocaleChangeInterceptor();
        localeChangeInterceptor.setParamName("lang");
        return localeChangeInterceptor;
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(localeChangeInterceptor());
    }
}
```

在这段配置中，我们首先提供了一个 `SessionLocaleResolver` 实例，这个实例会替换掉默认的 `AcceptHeaderLocaleResolver`，不同于 `AcceptHeaderLocaleResolver` 通过请求头来判断当前的环境信息，`SessionLocaleResolver` 将客户端的 `Locale` 保存到 `HttpSession`对象中，并且可以进行修改

添加配置,springboot会自动获取到国际化信息

```conf
spring.messages.basename=i18n/messages
spring.messages.encoding=utf-8
```

```java
public class I18nMessageUtil {

    @Autowired
    private MessageSource messageSource;

    private I18nMessageUtil() { /* no instance */ }

    /**
     * 根据key和参数获取对应的内容信息
     *
     * @param key  在国际化资源文件中对应的key
     * @param args 参数
     * @return 对应的内容信息
     */
    public static String getMessage(@Nonnull String key, @Nullable Object[] args) {
        MessageSource messageSource = SpringContextHolder.getBean(MessageSource.class);
        Locale locale = RequestContextUtils.getLocale(ServletContextHolder.request());
        String message = key;
        try {
            message = messageSource.getMessage(key, args, locale);
        } catch (NoSuchMessageException e) {
            log.error("NoSuchMessageException : {}", key);
        }
        return message;
    }
}
```
