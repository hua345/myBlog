# springboot 接口文档

## 参考

- [knife4j](https://doc.xiaominfo.com/)

目前已经发行的Knife4j版本，Knife4j本身已经引入了springfox，开发者在使用时不用再单独引入Springfox的具体版本，否额会导致版本冲突

Spring Boot的版本必须大于等于`2.2.x`

1、如果开发者继续使用OpenAPI2的规范结构，底层框架依赖springfox2.10.5版本，那么可以考虑`Knife4j`的2.x版本

```xml
<dependency>
    <groupId>com.github.xiaoymin</groupId>
    <artifactId>knife4j-spring-boot-starter</artifactId>
    <!--在引用时请在maven中央仓库搜索2.X最新版本号-->
    <version>2.0.9</version>
</dependency>
```

2、如果开发者使用OpenAPI3的结构，底层框架依赖springfox3.0.0,可以考虑`Knife4j`的3.x版本

```xml
<dependency>
    <groupId>com.github.xiaoymin</groupId>
    <artifactId>knife4j-spring-boot-starter</artifactId>
    <!--在引用时请在maven中央仓库搜索3.X最新版本号-->
    <version>3.0.3</version>
</dependency>
```

