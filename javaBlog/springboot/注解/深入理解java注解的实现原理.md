### 参考

- [深入理解java注解的实现原理](https://mp.weixin.qq.com/s?__biz=MzAxMjY1NTIxNA==&mid=2454441897&idx=1&sn=729688d470c94560c1e73e79f0c13adc&chksm=8c11e0a8bb6669be1cc4daee95b221ba437d536d598520d635fac4f18612dded58d6fddb0dce&scene=21#wechat_redirect)

### 1.什么是注解

> 注解也叫元数据，例如我们常见的`@Override`和`@Deprecated`，注解是`JDK1.5`版本开始引入的一个特性，用于对代码进行说明，可以对包、类、接口、字段、方法参数、局部变量等进行注解

一般常用的注解可以分为三类：

- 一类是Java自带的标准注解，包括@Override（标明重写某个方法）、@Deprecated（标明某个类或方法过时）
和@SuppressWarnings（标明要忽略的警告），使用这些注解后编译器就会进行检查。

- 一类为元注解，元注解是用于定义注解的注解，包括@Retention（标明注解被保留的阶段）、
@Target（标明注解使用的范围）、@Inherited（标明注解可继承）、@Documented（标明是否生成javadoc文档）

- 一类为自定义注解，可以根据自己的需求定义注解

### 2.注解的用途

在看注解的用途之前，有必要简单的介绍下XML和注解区别，

注解：是一种分散式的元数据，与源代码紧绑定。

xml：是一种集中式的元数据，与源代码无绑定

当然网上存在各种XML与注解的辩论哪个更好，这里不作评论和介绍，主要介绍一下注解的主要用途:

- 生成文档，通过代码里标识的元数据生成javadoc文档。

- 编译检查，通过代码里标识的元数据让编译器在编译期间进行检查验证。

- 编译时动态处理，编译时通过代码里标识的元数据动态处理，例如动态生成代码。

- 运行时动态处理，运行时通过代码里标识的元数据动态处理，例如使用反射注入实例

### 3. 注解详情

jdk1.5版本内置了三种标准的注解：

- `@Override`表示当前的方法定义将覆盖超类中的方法。
- `@Deprecated`，`使用了注解为它的元素编译器将发出警告，因为注解`@Deprecated`是不赞成使用的代码，被弃用的代码。
- `@SuppressWarnings`,关闭不当编辑器警告信息。

Java还提供了4中注解，专门负责新注解的创建:

- `@Target`
- `@Retention`
- `@Documented`
- `@Inherited`

#### 3.1 以spring的Autowired注解为例

```java
package org.springframework.beans.factory.annotation;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
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

#### 3.2 @Target

`@Target`用于描述注解的使用范围

```java
@Documented
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.ANNOTATION_TYPE)
public @interface Target {
    /**
     * Returns an array of the kinds of elements an annotation type
     * can be applied to.
     * @return an array of the kinds of elements an annotation type
     * can be applied to
     */
    ElementType[] value();
}
```

#### 3.3  ElementType

```java
public enum ElementType {
    /** Class, interface (including annotation type), or enum declaration */
    TYPE,

    /** Field declaration (includes enum constants) */
    FIELD,

    /** Method declaration */
    METHOD,

    /** Formal parameter declaration */
    PARAMETER,

    /** Constructor declaration */
    CONSTRUCTOR,

    /** Local variable declaration */
    LOCAL_VARIABLE,

    /** Annotation type declaration */
    ANNOTATION_TYPE,

    /** Package declaration */
    PACKAGE,

    /**
     * Type parameter declaration
     *
     * @since 1.8
     */
    TYPE_PARAMETER,

    /**
     * Use of a type
     *
     * @since 1.8
     */
    TYPE_USE
}
```

#### 3.4 @Retention

定义了该Annotation被保留的时间长短：某些Annotation仅出现在源代码中，而被编译器丢弃；而另一些却被编译在class文件中；编译在class文件中的Annotation可能会被虚拟机忽略，而另一些在class被装载时将被读取（请注意并不影响class的执行，因为Annotation与class在使用上是被分离的）

```java
@Documented
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.ANNOTATION_TYPE)
public @interface Retention {
    /**
     * Returns the retention policy.
     * @return the retention policy
     */
    RetentionPolicy value();
}

```

#### 3.5 RetentionPolicy

```java
public enum RetentionPolicy {
    /**
     * Annotations are to be discarded by the compiler.
     */
    SOURCE,

    /**
     * Annotations are to be recorded in the class file by the compiler
     * but need not be retained by the VM at run time.  This is the default
     * behavior.
     */
    CLASS,

    /**
     * Annotations are to be recorded in the class file by the compiler and
     * retained by the VM at run time, so they may be read reflectively.
     *
     * @see java.lang.reflect.AnnotatedElement
     */
    RUNTIME
}
```

#### 3.5@Documented

将注解包含在Javadoc中

#### 3.7@Inherited

允许子类继承父类中的注解

### 4. 自定义注解

```java
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = MobileValidator.class)
public @interface IsMobile {

    String message();

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};
}
```
