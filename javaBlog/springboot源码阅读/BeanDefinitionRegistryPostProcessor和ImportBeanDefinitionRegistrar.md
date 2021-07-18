# BeanDefinitionRegistryPostProcessor 和 ImportBeanDefinitionRegistrar

`BeanDefinitionRegistryPostProcessor`和`ImportBeanDefinitionRegistrar`都可以用于动态注册`bean`到容器中

`BeanDefinitionRegistryPostProcessor`实现了`BeanFactoryPostProcessor`接口，是`Spring`框架的`BeanDefinitionRegistry`的后处理器，用来注册额外的`BeanDefinition`。postProcessBeanDefinitionRegistry 方法会在所有的 BeanDefinition 已经被加载了，但是所有的 Bean 还没有被创建前调用。BeanDefinitionRegistryPostProcessor 经常被用来注册 BeanFactoryPostProcessor 的 BeanDefinition。

## ImportBeanDefinitionRegistrar

`@Import`注解用来支持在`Configuration`类中引入其他的配置类，包括`Configuration`类，`ImportSelector`和`ImportBeanDefinitionRegistrar`的实现类。
`ImportBeanDefinitionRegistrar`在`ConfigurationClassPostProcessor`处理`Configuration`类期间被调用，用来生成该`Configuration`类所需要的`BeanDefinition`

`myabtis`的`MapperScan`注解

```java
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.TYPE})
@Documented
@Import({MapperScannerRegistrar.class})
@Repeatable(MapperScans.class)
public @interface MapperScan {
}

public class MapperScannerRegistrar implements ImportBeanDefinitionRegistrar, ResourceLoaderAware {
    public MapperScannerRegistrar() {
    }

    public void registerBeanDefinitions(AnnotationMetadata importingClassMetadata, BeanDefinitionRegistry registry) {
        AnnotationAttributes annoAttrs = AnnotationAttributes.fromMap(importingClassMetadata.getAnnotationAttributes(MapperScan.class.getName()));
        BeanDefinitionBuilder builder = BeanDefinitionBuilder.genericBeanDefinition(MapperScannerConfigurer.class);
        builder.addPropertyValue("processPropertyPlaceHolders", true);
        Class<? extends Annotation> annotationClass = annoAttrs.getClass("annotationClass");
        builder.addPropertyValue("basePackage", StringUtils.collectionToCommaDelimitedString(basePackages));
        registry.registerBeanDefinition(beanName, builder.getBeanDefinition());
    }
}
```

```java
// 查询所有实现BeanDefinitionRegistryPostProcessor的类
postProcessorNames = beanFactory.getBeanNamesForType(BeanDefinitionRegistryPostProcessor.class, true, false);
```
