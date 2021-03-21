# eureka配置

## 服务端

```conf
server.port=8000
spring.application.name=spring-cloud-eureka

# 允许这个服务端作为客户端
eureka.client.register-with-eureka=false
eureka.client.fetch-registry=false

eureka.client.serviceUrl.defaultZone=http://localhost:8000/eureka/
```

## 客户端

```conf
server.port=8002
spring.application.name=cloud-client

eureka-server.host=localhost
eureka-server.port=8000
eureka.instance.hostname=${spring.cloud.client.ip-address}
eureka.client.service-url.defaultZone=http://{eureka-server.host}:${eureka-server.port}/eureka/
eureka.instance.instance-id=${spring.cloud.client.ip-address}:${spring.application.name}:${server.port}

#心跳信号间隔时间，默认30秒
eureka.instance.lease-renewal-interval-in-seconds=10
#每隔一定时间检测不到心跳信号，将server将服务标记为失效服务，默认90秒
eureka.instance.lease-expiration-duration-in-seconds=30
#每隔一定时间在server获取一次服务列表，默认30秒
eureka.client.registry-fetch-interval-seconds=10
```