## 1.单例模式简介

保证一个类仅有一个实例，并提供一个访问它的全局访问点。

### 1.1 为什么要用单例模式呢

简单来说使用单例模式可以带来下面几个好处:

- 对于频繁使用的对象，可以省略创建对象所花费的时间，这对于那些重量级对象而言，是非常可观的一笔系统开销

- 由于`new`操作的次数减少，因而对系统内存的使用频率也会降低，这将减轻`GC`压力，缩短`GC`停顿时间。

### 1.2为什么不使用全局变量确保一个类只有一个实例呢

我们知道全局变量分为静态变量和实例变量，静态变量也可以保证该类的实例只存在一个。

只要程序加载了类的字节码，不用创建任何实例对象，静态变量就会被分配空间，静态变量就可以被使用了。

但是，如果说这个对象非常消耗资源，而且程序某次的执行中一直没用，这样就造成了资源的浪费。利用单例模式的话，我们就可以实现在需要使用时才创建对象，这样就避免了不必要的资源浪费。

## 2. 单例的模式的实现

通常单例模式在Java语言中，有两种构建方式：

- 饿汉方式。指全局的单例实例在类装载时构建
- 懒汉方式。指全局的单例实例在第一次被使用时构建。
不管是那种创建方式，它们通常都存在下面几点相似处：

单例类必须要有一个`private`访问级别的构造函数，只有这样，才能确保单例不会在系统中的其他代码内被实例化;
`instance` 成员变量和`getInstance`方法必须是 static 的。

### 2.1 饿汉模式

```java
public class Singleton {
    //在静态初始化器中创建单例实例，这段代码保证了线程安全
    private static Singleton instance = new Singleton();
    //Singleton类只有一个构造方法并且是被private修饰的，所以用户无法通过new方法创建该对象实例
    private Singleton(){}
    public static Singleton getInstance(){
        return instance;
    }
}
```

所谓 “饿汉方式” 就是说JVM在加载这个类时就马上创建此唯一的单例实例，不管你用不用，先创建了再说，
如果一直没有被使用，便浪费了空间，典型的空间换时间，每次调用的时候，就不需要再判断，节省了运行时间。

### 2.2 懒汉式(双重检查加锁版本)

```java
public class Singleton {
    //volatile保证，当uniqueInstance变量被初始化成Singleton实例时，多个线程可以正确处理uniqueInstance变量
    private volatile static Singleton instance;

    private Singleton() {
        // to prevent instantiating by Reflection call
        if (instance != null) {
            throw new IllegalStateException("Already initialized.");
        }
    }

    public static Singleton getInstance() {
        //检查实例，如果不存在，就进入同步代码块
        if (null == instance) {
            //只有第一次才彻底执行这里的代码
            synchronized (Singleton.class) {
                //进入同步代码块后，再检查一次，如果仍是null，才创建实例
                if (null == instance) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

## 3. spring获取单例bean

```java
protected Object getSingleton(String beanName, boolean allowEarlyReference) {
    Object singletonObject = this.singletonObjects.get(beanName);
    if (singletonObject == null && isSingletonCurrentlyInCreation(beanName)) {
        synchronized (this.singletonObjects) {
            singletonObject = this.earlySingletonObjects.get(beanName);
            if (singletonObject == null && allowEarlyReference) {
                ObjectFactory<?> singletonFactory = this.singletonFactories.get(beanName);
                if (singletonFactory != null) {
                    singletonObject = singletonFactory.getObject();
                    this.earlySingletonObjects.put(beanName, singletonObject);
                    this.singletonFactories.remove(beanName);
                }
            }
        }
    }
    return singletonObject;
}
```
