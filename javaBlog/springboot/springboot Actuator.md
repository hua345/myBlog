# Spring Boot & Actuator

> SpringBoot 自带监控功能 Actuator，可以帮助实现对程序内部运行情况监控，比如监控状况、Bean 加载情况、环境变量、日志信息、线程信息等

## 引入依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

浏览器打开[http://localhost:8080/actuator/](http://localhost:8080/actuator/)

```json
{
  "_links": {
    "self": { "href": "http://localhost:8080/actuator", "templated": false },
    "health": {
      "href": "http://localhost:8080/actuator/health",
      "templated": false
    },
    "health-path": {
      "href": "http://localhost:8080/actuator/health/{*path}",
      "templated": true
    },
    "info": {
      "href": "http://localhost:8080/actuator/info",
      "templated": false
    }
  }
}
```

Spring Boot 2.X 中，`Actuator` 默认只开放 `health` 和 `info` 两个端点。

暴露端点

| ID             | JMX | Web |
| -------------- | --- | --- |
| auditevents    | Yes | No  |
| beans          | Yes | No  |
| conditions     | Yes | No  |
| configprops    | Yes | No  |
| env            | Yes | No  |
| flyway         | Yes | No  |
| health         | Yes | Yes |
| heapdump       | N/A | No  |
| httptrace      | Yes | No  |
| info           | Yes | Yes |
| jolokia        | Yes | No  |
| logfile        | Yes | No  |
| loggers        | Yes | No  |
| liquibase      | Yes | No  |
| metrics        | Yes | No  |
| mappings       | Yes | No  |
| prometheus     | N/A | No  |
| scheduledtasks | Yes | No  |
| sessions       | Yes | No  |
| shutdown       | Yes | No  |
| threaddump     | Yes | No  |

要更改公开哪些端点，请使用以下技术特定的 include 和 exclude 属性：

| Property                                  | Default      |
| ----------------------------------------- | ------------ |
| management.endpoints.jmx.exposure.exclude |              |
| management.endpoints.jmx.exposure.include | \*           |
| management.endpoints.web.exposure.exclude |              |
| management.endpoints.web.exposure.include | info, health |
