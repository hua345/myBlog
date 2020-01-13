# 参考

- [https://github.com/alibaba/druid](https://github.com/alibaba/druid)
- [DruidDataSource配置](https://github.com/alibaba/druid/wiki/DruidDataSource%E9%85%8D%E7%BD%AE)
- [DruidDataSource配置属性列表](https://github.com/alibaba/druid/wiki/DruidDataSource%E9%85%8D%E7%BD%AE%E5%B1%9E%E6%80%A7%E5%88%97%E8%A1%A8)
- [Druid常见问题](https://github.com/alibaba/druid/wiki/%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98)
- [https://github.com/alibaba/druid/tree/master/druid-spring-boot-starter](https://github.com/alibaba/druid/tree/master/druid-spring-boot-starter)

## Druid介绍

> Druid连接池是阿里巴巴开源的数据库连接池项目。Druid连接池为监控而生，内置强大的监控功能，监控特性不影响性能。

## 添加maven依赖

```xml
    <dependency>
        <groupId>com.alibaba</groupId>
        <artifactId>druid</artifactId>
        <version>${druid-version}</version>
    </dependency>
```

## druid配置

```conf
# JDBC配置
spring.datasource.druid.type=com.alibaba.druid.pool.DruidDataSource
spring.datasource.druid.url=jdbc:mariadb://192.168.137.128:3306/db_example
spring.datasource.druid.username=springuser
spring.datasource.druid.password=123456
spring.datasource.druid.driverClassName=org.mariadb.jdbc.Driver
# dataSource Pool configuration
spring.datasource.druid.initialSize=5
spring.datasource.druid.minIdle=5
spring.datasource.druid.maxActive=20
spring.datasource.druid.maxActive.maxWait=60000
# 配置间隔多久才进行一次检测，检测需要关闭的空闲连接，单位是毫秒
spring.datasource.druid.timeBetweenEvictionRunsMillis=60000
# 配置一个连接在池中最小生存的时间，单位是毫秒
spring.datasource.druid.minEvictableIdleTimeMillis=300000
spring.datasource.druid.validationQuery=SELECT 1 FROM DUAL
spring.datasource.druid.testWhileIdle=true
spring.datasource.druid.testOnBorrow=false
spring.datasource.druid.exceptionSorter=true
spring.datasource.druid.testOnReturn=false
spring.datasource.druid.poolPreparedStatements=true
spring.datasource.druid.maxPoolPreparedStatementPerConnectionSize=20
# 配置监控统计拦截的filters，去掉后监控界面sql无法统计，
# Druid内置提供一个StatFilter，用于统计监控信息
# wall用于防火墙（防止SQL注入）
# slf4j日志打印
spring.datasource.druid.filters=stat,wall,slf4j
# 通过connectProperties属性来打开mergeSql功能；慢SQL记录
# StatFilter属性slowSqlMillis用来配置SQL慢的标准，执行时间超过slowSqlMillis的就是慢。
# slowSqlMillis的缺省值为3000，也就是3秒。
spring.datasource.druid.connectionProperties=druid.stat.mergeSql=true;druid.stat.slowSqlMillis=500
# 合并多个DruidDataSource的监控数据
spring.datasource.druid.useGlobalDataSourceStat=true

# config/DruidConfiguration中已经配置了登录用户
# 浏览器打开 /druid/index.html,账号默认admin
```

## [内置Filter的别名](https://github.com/alibaba/druid/wiki/%E5%86%85%E7%BD%AEFilter%E7%9A%84%E5%88%AB%E5%90%8D)

|Filter类名|别名|
|-----------|-----------|
|default|com.alibaba.druid.filter.stat.StatFilter|
|stat|com.alibaba.druid.filter.stat.StatFilter|
|mergeStat|com.alibaba.druid.filter.stat.MergeStatFilter|
|encoding|com.alibaba.druid.filter.encoding.EncodingConvertFilter|
|log4j|com.alibaba.druid.filter.logging.Log4jFilter|
|log4j2|com.alibaba.druid.filter.logging.Log4j2Filter|
|slf4j|com.alibaba.druid.filter.logging.Slf4jLogFilter|
|commonlogging|com.alibaba.druid.filter.logging.CommonsLogFilter|
|wall|com.alibaba.druid.wall.WallFilter|
