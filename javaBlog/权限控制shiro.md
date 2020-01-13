`Apache Shiro`是一个强大且易用的Java安全框架,执行身份验证、授权、密码和会话管理。
使用Shiro的易于理解的API,您可以快速、轻松地获得任何应用程序,从最小的移动应用程序到最大的网络和企业应用程序。

#### 三个核心组件：Subject, SecurityManager和 Realms.
- Subject：代表了当前用户的安全操作，SecurityManager则管理所有用户的安全操作。
- SecurityManager：它是Shiro框架的核心，典型的Facade模式，
Shiro通过SecurityManager来管理内部组件实例，并通过它来提供安全管理的各种服务。
- Realms： Realm充当了Shiro与应用安全数据间的“桥梁”或者“连接器”。
也就是说，当对用户执行认证（登录）和授权（访问控制）验证时，Shiro会从应用配置的Realm中查找用户及其权限信息。

