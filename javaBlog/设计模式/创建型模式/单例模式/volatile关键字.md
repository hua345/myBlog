
### volatile特性

`volatile`英文翻译是不稳定的、易变的

当一个共享变量被`volatile`修饰时，它会保证修改的值立即被更新到主存

内存可见性：通俗来说就是，线程A对一个`volatile`变量的修改，对于其它线程来说是可见的，即线程每次获取`volatile`变量的值都是最新的。

### 单例模式

代码读取到instance不为null时，instance引用的对象有可能还没有完成初始化。

主要的原因是重排序。重排序是指编译器和处理器为了优化程序性能而对指令序列进行重新排序的一种手段。

```java
memory = allocate();　　// 1：分配对象的内存空间
ctorInstance(memory);　// 2：初始化对象
instance = memory;　　// 3：设置instance指向刚分配的内存地址
```

根源在于代码中的2和3之间，可能会被重排序。例如：

```java
memory = allocate();　　// 1：分配对象的内存空间
instance = memory;　　// 3：设置instance指向刚分配的内存地址
// 注意，此时对象还没有被初始化！
ctorInstance(memory);　// 2：初始化对象
```
