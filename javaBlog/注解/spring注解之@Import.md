### 参考

- [一分钟学会spring注解之@Import注解](https://mp.weixin.qq.com/s/RKuHBQmatIBpjcaom-GLeQ)

### 1. @Import注解是什么

通过导入的方式实现把实例加入springIOC容器中

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface Import {

    /**
     * {@link Configuration}, {@link ImportSelector}, {@link ImportBeanDefinitionRegistrar}
     * or regular component classes to import.
     */
    Class<?>[] value();

}
```

### 2. @Import的三种使用方式

#### 2.1 Configuration

再Bean目录添加`Apple`和`Orange`类

```java
public class Apple {
}
public class Orange {
}
```

`BeanConfig`注解配置中增加`@Import`注解如下：

```java
@Import({Apple.class, Orange.class})
@Configuration
public class BeanConfig {
}
```

测试Bean加载情况

```java
    public static void main(String[] args) {
        AnnotationConfigApplicationContext applicationContext2 = new AnnotationConfigApplicationContext(BeanConfig.class);
        String[] beanNames = applicationContext2.getBeanDefinitionNames();
        for (String item : beanNames) {
            System.out.println("bean名称为===" + item);
        }
    }
```

测试结果

```java
bean名称为===beanConfig
bean名称为===com.github.code.admin.service.Apple
bean名称为===com.github.code.admin.service.Orange
```

对应的import的bean都已经加入到spring容器中了

#### 2.2 基于自定义ImportSelector

定义一个自己的`ImportSelector`

```java
public class MyImportSelector implements ImportSelector {
    @Override
    public String[] selectImports(AnnotationMetadata importingClassMetadata) {
        return new String[]{"com.github.code.admin.service.Watermelon"};
    }
}
```

`BeanConfig`注解配置修改如下：

```java
@Import({Apple.class, Orange.class, MyImportSelector.class})
@Configuration
public class BeanConfig {
}
```

测试结果

```java
bean名称为===beanConfig
bean名称为===com.github.code.admin.service.Apple
bean名称为===com.github.code.admin.service.Orange
bean名称为===com.github.code.admin.service.Watermelon
```

#### 2.3 基于ImportBeanDefinitionRegistrar

定义一个自己的`ImportBeanDefinitionRegistrar`

```java
public class MyImportBeanDefinitionRegistrar implements ImportBeanDefinitionRegistrar {
    @Override
    public void registerBeanDefinitions(
            AnnotationMetadata importingClassMetadata,
            BeanDefinitionRegistry registry) {
        // new一个RootBeanDefinition
        RootBeanDefinition rootBeanDefinition = new RootBeanDefinition(Banana.class);
        // 注册一个名字叫rectangle的bean
        registry.registerBeanDefinition("Banana", rootBeanDefinition);
    }
}
```

`BeanConfig`注解配置修改如下：

```java
@Import({Apple.class, Orange.class, MyImportSelector.class, MyImportBeanDefinitionRegistrar.class})
@Configuration
public class BeanConfig {
}
```

测试结果

```java
bean名称为===beanConfig
bean名称为===com.github.code.admin.service.Apple
bean名称为===com.github.code.admin.service.Orange
bean名称为===com.github.code.admin.service.Watermelon
bean名称为===Banana
```
