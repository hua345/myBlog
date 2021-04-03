# spring 常用设计模式

## 浅谈控制反转（IOC）与依赖注入（DI）

`IOC（Inversion of Control）`是`Spring`中一个非常重要的概念，它不是什么技术，而是一种解耦的设计思想。它主要的额目的是借助于第三方（Spring中的IOC容器）实现具有依赖关系的的对象之间的解耦（IOC容易管理对象，你只管使用即可），从而降低代码之间的耦合度。

## 工厂设计模式（简单工厂和工厂方法）

Spring使用工厂模式可以通过`BeanFactory`或`ApplicationContext`创建bean对象。

## 单例设计模式

Spring中bean的默认作用域就是`singleton`。除了`singleton`作用域，`Spring bean`还有下面几种作用域：

- `prototype` : 每次请求都会创建一个新的 bean 实例。
- `request` : 每一次HTTP请求都会产生一个新的bean，该bean仅在当前HTTP request内有效。
- `session` : 每一次HTTP请求都会产生一个新的 bean，该bean仅在当前 HTTP session 内有效。

## 代理设计模式

`Spring AOP`就是基于动态代理的，如果要代理的对象，实现了某个接口，那么`Spring AOP`会使用`JDK Proxy`，去创建代理对象，而对于没有实现接口的对象，就无法使用JDK Proxy去进行代理了，这时候`Spring AOP`会使用`Cglib`，这时候Spring AOP会使用Cglib生成一个被代理对象的子类来作为代理。

## 模板方法设计模式

模板方法模式是一种行为设计模式，它定义一个操作中的算法的骨架，而将一些步骤延迟到子类中。模板方法使得子类可以在不改变一个算法的结构即可重定义该算法的默写特定步骤的实现方式。

```java
public abstract class Template {  
    //这是我们的模板方法  
    public final void TemplateMethod(){  
        PrimitiveOperation1();    
        PrimitiveOperation2();  
        PrimitiveOperation3();  
    }  
    protected void  PrimitiveOperation1(){  
        //当前类实现  
    }
    //被子类实现的方法  
    protected abstract void PrimitiveOperation2();  
    protected abstract void PrimitiveOperation3();  
}

public class TemplateImpl extends Template {  
    @Override  
    public void PrimitiveOperation2() {  
        //当前类实现  
    }  
    @Override  
    public void PrimitiveOperation3() {  
        //当前类实现  
    }  
}
```

Spring中`jdbcTemplate`、`hibernateTemplate`等以`Template`结尾的对数据库操作的类，它们就使用到模板模式。

一般情况下，我们都是使用继承的方式来实现模板模式，但是`Spring`并没有使用这种方式，而是使用`Callback模式`与`模板方法`配合，既达到了代码复用的效果，同时增加了灵活性。

## 观察者设计模式

观察者设计模式是一种对象行为模式。它表示的是一种对象与对象之间具有依赖关系，当一个对象发生改变时，这个对象锁依赖的对象也会做出反应。Spring事件驱动模型就是观察者模式很经典的应用。

- 事件角色：ApplicationEvent（org.springframework.context包下）充当事件的角色，这是一个抽象类。
- 事件监听者角色：ApplicationListener充当了事件监听者的角色，它是一个接口，里面只定义了一个onApplicationEvent（）方法来处理ApplicationEvent。
- 事件发布者角色：ApplicationEventPublisher充当了事件的发布者，它也是个接口。

```java
// 定义一个事件,继承自ApplicationEvent并且写相应的构造函数  
public class DemoEvent extends ApplicationEvent{  
    private static final long serialVersionUID = 1L;  
    private String message;  
    public DemoEvent(Object source,String message){  
        super(source);  
        this.message = message;  
    }  
    public String getMessage() {  
         return message;  
          }  
// 定义一个事件监听者,实现ApplicationListener接口，重写 onApplicationEvent() 方法；  
@Component  
public class DemoListener implements ApplicationListener<DemoEvent>{  
    //使用onApplicationEvent接收消息  
    @Override  
    public void onApplicationEvent(DemoEvent event) {  
        String msg = event.getMessage();  
        System.out.println("接收到的信息是："+msg);  
    }  
}  
// 发布事件，可以通过ApplicationEventPublisher  的 publishEvent() 方法发布消息。  
@Component  
public class DemoPublisher {  
    @Autowired  
    ApplicationContext applicationContext;  
    public void publish(String message){  
        //发布事件  
        applicationContext.publishEvent(new DemoEvent(this, message));  
    }  
}
```
