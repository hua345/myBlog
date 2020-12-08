# feign配置[springcloud默认配置](#springcloudspring-configuration-metadata.json)

- [https://github.com/OpenFeign/feign](https://github.com/OpenFeign/feign)

```conf
# 设置连接超时时间
ribbon.ConnectTimeout=5000
# 设置读取超时时间
ribbon.ReadTimeout=60000

# 配置请求GZIP压缩
feign.compression.request.enabled=true
# 配置响应GZIP压缩
feign.compression.response.enabled=true
# 配置压缩数据大小的下限
feign.compression.request.min-request-size=2048

feign.client.config.defautl.connectTimeout=5000
feign.client.config.defautl.readTimeout=30000
# 使用httpclient作为feign调用连接池
feign.httpclient.enabled=false
feign.okhttp.enabled=true
#对所有操作请求都进行重试,默认false
ribbon.OkToRetryOnAllOperations=false
#对当前实例的重试次数，默认0
ribbon.MaxAutoRetries=0
# 对切换实例的重试次数，默认1(默认会看到超时时间是ribbon.ReadTimeout * ribbon.MaxAutoRetriesNextServer的结果时间)
ribbon.MaxAutoRetriesNextServer=1

# 在feign中开启hystrix功能，默认情况下feign不开启hystrix功能
feign.hystrix.enabled=true
# 命令执行(execution)配置
# 隔离策略,默认THREAD
hystrix.command.default.execution.isolation.strategy=THREAD
# 是否允许超时，默认true。如果enabled设置为false，则请求超时交给ribbon控，`timeoutInMilliseconds`则无法控制，
# 如果为true，并同时配置了 Ribbon 和 Hystrix 的超时时间，则`ReadTimeout`和`timeoutInMilliseconds`谁小谁控制
# 超时时间上限，默认1000
hystrix.command.default.execution.isolation.thread.timeoutInMilliseconds=60000
#feign熔断超时总时间计算公式（黄海平 2020-06-08）
# 总时间(feignTimeTotal) = ReadTimeout * (MaxAutoRetries + 1) * (MaxAutoRetriesNextServer * 2)
# 注：hystrix.command.default.execution.timeout.enabled=true timeoutInMilliseconds的时间值必须要比feignTimeTotal大，否则优先于hystrix熔断

# 线程池配置
# Hystrix使用的是JUC线程池ThreadPoolExecutor，线程池相关配置直接影响ThreadPoolExecutor实例。
# 核心线程数，默认10
hystrix.threadpool.default.coreSize=50
# 最大任务队列容量，默认值-1使用的是`SynchronousQueue`无缓冲队列无法存储元素,配置为大于0时使用`LinkedBlockingQueue`有缓冲队列可存储元素
hystrix.threadpool.default.maxQueueSize=1000
# 任务拒绝的任务队列阈值,默认5。当`maxQueueSize`配置为-1的时候，此配置项不生效。
# 即使maxQueueSize没有达到，达到`queueSizeRejectionThreshold`该值后，请求也会被拒绝
hystrix.threadpool.default.queueSizeRejectionThreshold=100

# 命令降级(fallback)配置
# 是否开启降级,默认true
hystrix.command.default.fallback.enabled=true
# 所有命令降级配置对策略ExecutionIsolationStrategy.THREAD或者ExecutionIsolationStrategy.SEMAPHORE都生效
# 最大并发降级请求处理上限，降级逻辑不会执行并且会抛出一个异常。默认10
hystrix.command.default.fallback.isolation.semaphore.maxConcurrentRequests=100

# 断路器(circuit breaker)配置
# 是否启用断路器，默认true
hystrix.command.default.circuitBreaker.enabled=true
# 断路器请求量阈值,使断路器打开的滑动窗口中的最小请求数量，默认20。(需要在启动类添加@EnableCircuitBreaker)
# 如果值是20，那么如果在滑动窗口中只接收到19个请求(比如一个10秒的窗口)，即使所有19个请求都失败了，断路器也不会打开。
hystrix.command.default.circuitBreaker.requestVolumeThreshold=20
# 断路器等待窗口时间,默认5000
# 此属性设置断路器打开后拒绝请求的时间量，每隔一段时间(sleepWindowInMilliseconds，单位是毫秒)允许再次尝试(也就是放行一个请求)确定是否应该关闭断路器。
hystrix.command.default.circuitBreaker.sleepWindowInMilliseconds=3000
# 断路器错误百分比阈值，默认50
# 此属性设置一个错误百分比，当请求错误率超过设定值，断路器就会打开。
hystrix.command.default.circuitBreaker.errorThresholdPercentage=50
```

## maven配置

```xml
<dependency>
    <groupId>org.apache.httpcomponents</groupId>
    <artifactId>httpclient</artifactId>
    <version>4.5.12</version>
</dependency>
```

## 1. feign线程池

### 1.1 FeignRibbon配置

```java
org.springframework.cloud.openfeign.FeignClient
// 通过FeignClient注解找到FeignAutoConfiguration类的位置
org.springframework.cloud.openfeign.FeignAutoConfiguration
org.springframework.cloud.openfeign.ribbon.FeignRibbonClientAutoConfiguration
```

依次导入`HttpClientFeignLoadBalancedConfiguration`, `OkHttpFeignLoadBalancedConfiguration`, `DefaultFeignLoadBalancedConfiguration`到springIOC容器

```java
@ConditionalOnClass({ILoadBalancer.class, Feign.class})
@Configuration
@AutoConfigureBefore({FeignAutoConfiguration.class})
@EnableConfigurationProperties({FeignHttpClientProperties.class})
@Import({HttpClientFeignLoadBalancedConfiguration.class, OkHttpFeignLoadBalancedConfiguration.class, DefaultFeignLoadBalancedConfiguration.class})
public class FeignRibbonClientAutoConfiguration {
    public FeignRibbonClientAutoConfiguration() {
    }
}
```

### 1.2 ApacheHttpClient

```java
@Configuration
@ConditionalOnClass({ApacheHttpClient.class})
@ConditionalOnProperty(
    value = {"feign.httpclient.enabled"},
    matchIfMissing = true
)
class HttpClientFeignLoadBalancedConfiguration {
    HttpClientFeignLoadBalancedConfiguration() {
    }

    @Bean
    @ConditionalOnMissingBean({Client.class})
    public Client feignClient(CachingSpringLoadBalancerFactory cachingFactory, SpringClientFactory clientFactory, HttpClient httpClient) {
        ApacheHttpClient delegate = new ApacheHttpClient(httpClient);
        return new LoadBalancerFeignClient(delegate, cachingFactory, clientFactory);
    }
}
```

### 1.3 okhttp

```java
@Configuration
@ConditionalOnClass({OkHttpClient.class})
@ConditionalOnProperty({"feign.okhttp.enabled"})
class OkHttpFeignLoadBalancedConfiguration {
    OkHttpFeignLoadBalancedConfiguration() {
    }

    @Bean
    @ConditionalOnMissingBean({Client.class})
    public Client feignClient(CachingSpringLoadBalancerFactory cachingFactory, SpringClientFactory clientFactory, okhttp3.OkHttpClient okHttpClient) {
        OkHttpClient delegate = new OkHttpClient(okHttpClient);
        return new LoadBalancerFeignClient(delegate, cachingFactory, clientFactory);
    }

    @Configuration
    @ConditionalOnMissingBean({okhttp3.OkHttpClient.class})
    protected static class OkHttpFeignConfiguration {
        private okhttp3.OkHttpClient okHttpClient;

        protected OkHttpFeignConfiguration() {
        }
    }
}
```

### 1.4 默认配置

```java
@Configuration
class DefaultFeignLoadBalancedConfiguration {
    DefaultFeignLoadBalancedConfiguration() {
    }

    @Bean
    @ConditionalOnMissingBean
    public Client feignClient(CachingSpringLoadBalancerFactory cachingFactory, SpringClientFactory clientFactory) {
        return new LoadBalancerFeignClient(new Default((SSLSocketFactory)null, (HostnameVerifier)null), cachingFactory, clientFactory);
    }
}

public interface Client {
    Response execute(Request var1, Options var2) throws IOException;

    public static class Default implements Client {
        private final SSLSocketFactory sslContextFactory;
        private final HostnameVerifier hostnameVerifier;

        public Default(SSLSocketFactory sslContextFactory, HostnameVerifier hostnameVerifier) {
            this.sslContextFactory = sslContextFactory;
            this.hostnameVerifier = hostnameVerifier;
        }

        public Response execute(Request request, Options options) throws IOException {
            HttpURLConnection connection = this.convertAndSend(request, options);
            return this.convertResponse(connection, request);
        }

        HttpURLConnection convertAndSend(Request request, Options options) throws IOException {
            HttpURLConnection connection = (HttpURLConnection)(new URL(request.url())).openConnection();
        }
    }
}
```

## 2. feign连接池配置

`Default`使用`HttpURLConnection` 建立连接且每次请求都建立一个新的连接

默认情况下，服务之间调用使用的`HttpURLConnection`，效率非常低。为了提高效率，可以通过连接池提高效率

## spring cloud spring-configuration-metadata.json

```json
{
  "groups": [
    {
      "name": "feign.client",
      "type": "org.springframework.cloud.openfeign.FeignClientProperties",
      "sourceType": "org.springframework.cloud.openfeign.FeignClientProperties"
    },
    {
      "name": "feign.compression.request",
      "type": "org.springframework.cloud.openfeign.encoding.FeignClientEncodingProperties",
      "sourceType": "org.springframework.cloud.openfeign.encoding.FeignClientEncodingProperties"
    },
    {
      "name": "feign.httpclient",
      "type": "org.springframework.cloud.openfeign.support.FeignHttpClientProperties",
      "sourceType": "org.springframework.cloud.openfeign.support.FeignHttpClientProperties"
    }
  ],
  "properties": [
    {
      "name": "feign.client.config",
      "type": "java.util.Map<java.lang.String,org.springframework.cloud.openfeign.FeignClientProperties.FeignClientConfiguration>",
      "sourceType": "org.springframework.cloud.openfeign.FeignClientProperties"
    },
    {
      "name": "feign.client.default-config",
      "type": "java.lang.String",
      "sourceType": "org.springframework.cloud.openfeign.FeignClientProperties",
      "defaultValue": "default"
    },
    {
      "name": "feign.client.default-to-properties",
      "type": "java.lang.Boolean",
      "sourceType": "org.springframework.cloud.openfeign.FeignClientProperties",
      "defaultValue": true
    },
    {
      "name": "feign.compression.request.enabled",
      "type": "java.lang.Boolean",
      "description": "Enables the request sent by Feign to be compressed.",
      "defaultValue": "false"
    },
    {
      "name": "feign.compression.request.mime-types",
      "type": "java.lang.String[]",
      "description": "The list of supported mime types.",
      "sourceType": "org.springframework.cloud.openfeign.encoding.FeignClientEncodingProperties",
      "defaultValue": [
        "text\/xml",
        "application\/xml",
        "application\/json"
      ]
    },
    {
      "name": "feign.compression.request.min-request-size",
      "type": "java.lang.Integer",
      "description": "The minimum threshold content size.",
      "sourceType": "org.springframework.cloud.openfeign.encoding.FeignClientEncodingProperties",
      "defaultValue": 2048
    },
    {
      "name": "feign.compression.response.enabled",
      "type": "java.lang.Boolean",
      "description": "Enables the response from Feign to be compressed.",
      "defaultValue": "false"
    },
    {
      "name": "feign.httpclient.connection-timeout",
      "type": "java.lang.Integer",
      "sourceType": "org.springframework.cloud.openfeign.support.FeignHttpClientProperties",
      "defaultValue": 2000
    },
    {
      "name": "feign.httpclient.connection-timer-repeat",
      "type": "java.lang.Integer",
      "sourceType": "org.springframework.cloud.openfeign.support.FeignHttpClientProperties",
      "defaultValue": 3000
    },
    {
      "name": "feign.httpclient.disable-ssl-validation",
      "type": "java.lang.Boolean",
      "sourceType": "org.springframework.cloud.openfeign.support.FeignHttpClientProperties",
      "defaultValue": false
    },
    {
      "name": "feign.httpclient.enabled",
      "type": "java.lang.Boolean",
      "description": "Enables the use of the Apache HTTP Client by Feign.",
      "defaultValue": "true"
    },
    {
      "name": "feign.httpclient.follow-redirects",
      "type": "java.lang.Boolean",
      "sourceType": "org.springframework.cloud.openfeign.support.FeignHttpClientProperties",
      "defaultValue": true
    },
    {
      "name": "feign.httpclient.max-connections",
      "type": "java.lang.Integer",
      "sourceType": "org.springframework.cloud.openfeign.support.FeignHttpClientProperties",
      "defaultValue": 200
    },
    {
      "name": "feign.httpclient.max-connections-per-route",
      "type": "java.lang.Integer",
      "sourceType": "org.springframework.cloud.openfeign.support.FeignHttpClientProperties",
      "defaultValue": 50
    },
    {
      "name": "feign.httpclient.time-to-live",
      "type": "java.lang.Long",
      "sourceType": "org.springframework.cloud.openfeign.support.FeignHttpClientProperties",
      "defaultValue": 900
    },
    {
      "name": "feign.httpclient.time-to-live-unit",
      "type": "java.util.concurrent.TimeUnit",
      "sourceType": "org.springframework.cloud.openfeign.support.FeignHttpClientProperties"
    },
    {
      "name": "feign.hystrix.enabled",
      "type": "java.lang.Boolean",
      "description": "If true, an OpenFeign client will be wrapped with a Hystrix circuit breaker.",
      "defaultValue": "false"
    },
    {
      "name": "feign.okhttp.enabled",
      "type": "java.lang.Boolean",
      "description": "Enables the use of the OK HTTP Client by Feign.",
      "defaultValue": "false"
    }
  ],
  "hints": []
}
```
