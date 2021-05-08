#### 1.测试redis连接

```bash
➜  ~ redis-cli -h 192.168.137.132
192.168.137.132:6379> ping
PONG
```

> 随着Spring Boot2.x的到来，支持的组件越来越丰富，也越来越成熟，
其中对Redis的支持不仅仅是丰富了它的API，更是替换掉底层Jedis的依赖，取而代之换成了Lettuce(生菜)

#### 2. Lettuce

> `Lettuce`和`Jedis`的都是连接Redis Server的客户端程序。
`Jedis`在实现上是直连`redis server`，多线程环境下非线程安全，除非使用连接池，
为每个Jedis实例增加物理连接。`Lettuce基于Netty的连接实例`（StatefulRedisConnection），
可以在多个线程间并发访问，且线程安全，满足多线程环境下的并发访问，
同时它是可伸缩的设计，一个连接实例不够的情况也可以按需增加连接实例。

#### 3. 添加pom文件依赖

在pom.xml中spring-boot-starter-data-redis的依赖，
Spring Boot2.x后底层不在是Jedis如果做版本升级的朋友需要注意下

```maven
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```

#### 4. 属性配置

在application.properties文件中配置如下内容，由于Spring Boot2.x的改动，
连接池相关配置需要通过`spring.redis.lettuce.pool`或者`spring.redis.jedis.pool`进行配置

```properties
# Redis服务器地址
spring.redis.host=192.168.137.128
# Redis服务器连接端口
spring.redis.port=6379
# Redis服务器连接密码（默认为空）
spring.redis.password=
# 连接超时时间（毫秒）
spring.redis.timeout=10000
# Redis默认情况下有16个分片，这里配置具体使用的分片，默认是0
spring.redis.database=0
# 连接池最大连接数（使用负值表示没有限制） 默认 8
spring.redis.jedis.pool.max-active=8
# 连接池最大阻塞等待时间（使用负值表示没有限制） 默认 -1
spring.redis.jedis.pool.max-wait=-1
# 连接池中的最大空闲连接 默认 8
spring.redis.jedis.pool.max-idle=8
# 连接池中的最小空闲连接 默认 0
spring.redis.jedis.pool.min-idle=0
```

#### 5. 自定义Template

默认情况下的模板只能支持`RedisTemplate<String, String>`，也就是只能存入字符串，
这在开发中是不友好的，所以自定义模板是很有必要的，
当自定义了模板又想使用String存储这时候就可以使用`StringRedisTemplate`的方式，它们并不冲突

```java
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.lettuce.LettuceConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.serializer.GenericJackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.StringRedisSerializer;

import java.io.Serializable;

/**
 * @author CHENJIANHUA
 * @date 2019/6/28 16:33
 */
@Configuration
@EnableAutoConfiguration
public class RedisConfig {
    /**
     * LettuceConnectionFactory redisConnectionFactory
     *
     * @param redisConnectionFactory
     * @return
     */
    @Bean
    public RedisTemplate<String, Serializable> redisCacheTemplate(LettuceConnectionFactory redisConnectionFactory) {
        RedisTemplate<String, Serializable> template = new RedisTemplate<>();
        template.setKeySerializer(new StringRedisSerializer());
        template.setValueSerializer(new GenericJackson2JsonRedisSerializer());
        template.setConnectionFactory(redisConnectionFactory);
        return template;
    }
}
```

#### 6. 单元测试

```java
import org.junit.Test;
import org.junit.runner.RunWith;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.test.context.junit4.SpringRunner;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.IntStream;

@RunWith(SpringRunner.class)
@SpringBootTest
public class SpringBootLettuceRedisApplicationTests {

    private static final Logger log = LoggerFactory.getLogger(SpringBootLettuceRedisApplicationTests.class);

    @Autowired
    private StringRedisTemplate stringRedisTemplate;

    @Autowired
    private RedisTemplate<String, Serializable> redisCacheTemplate;


    @Test
    public void get() {
        // 测试线程安全
        ExecutorService executorService = Executors.newFixedThreadPool(1000);
        //主键生成
        stringRedisTemplate.opsForValue().set("userId", "10000");
        IntStream.range(0, 1000).forEach(i ->
                executorService.execute(() -> stringRedisTemplate.opsForValue().increment("userId", 1))
        );
        // 简单key value获取
        String userId = stringRedisTemplate.opsForValue().get("userId");
        log.info("[主键生成userId] - [{}]", userId);
        stringRedisTemplate.opsForValue().set("name", "fang");
        String name = stringRedisTemplate.opsForValue().get("name");
        log.info("[字符缓存结果] - [{}]", name);
        //  以下只演示整合，具体Redis命令可以参考官方文档，Spring Data Redis 只是改了个名字而已，Redis支持的命令它都支持
        String userIdKey = "user:" + userId;
        redisCacheTemplate.opsForValue().set(userIdKey, "fangfang");
        // 对应 String（字符串）
        String fangName = (String) redisCacheTemplate.opsForValue().get(userIdKey);
        log.info("[对象缓存结果] - [{}]", fangName);
    }
}
```
