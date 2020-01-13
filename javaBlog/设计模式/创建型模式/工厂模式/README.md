### 工厂模式的分类

- 简单工厂（`Simple Factory`）模式，又称静态工厂方法模式（Static Factory Method Pattern）。
- 工厂方法（`Factory Method`）模式，又称多态性工厂（Polymorphic Factory）模式或虚拟构造子（Virtual Constructor）模式；
- 抽象工厂（`Abstract Factory`）模式，又称工具箱（Kit 或Toolkit）模式。

### 为什么要用工厂模式

- 解耦 ：把对象的创建和使用的过程分开
- 降低代码重复: 如果创建某个对象的过程都很复杂，需要一定的代码量，而且很多地方都要用到，那么就会有很多的重复代码。
- 降低维护成本 ：由于创建过程都由工厂统一管理，所以发生业务逻辑变化，不需要找到所有需要创建对象的地方去逐个修正，只需要在工厂里修改即可，降低维护成本。
