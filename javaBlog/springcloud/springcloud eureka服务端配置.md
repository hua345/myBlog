# eureka 服务端配置

## maven 依赖

```xml
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-netflix-eureka-server</artifactId>
</dependency>
```

## 修改配置文件

```conf
server.port=8000
spring.application.name=spring-cloud-eureka

# 允许这个服务端作为客户端
eureka.client.register-with-eureka=false
eureka.client.fetch-registry=false

eureka.client.serviceUrl.defaultZone=http://localhost:8000/eureka/
```
