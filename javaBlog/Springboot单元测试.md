# 参考

- [Testing the Web Layer](https://spring.io/guides/gs/testing-web/)
- [https://github.com/spring-guides/gs-testing-web](https://github.com/spring-guides/gs-testing-web)

## 1. 创建简单 controller 类

```java
src/main/java/hello/HomeController.java
```

```java
package hello;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class HomeController {

    @RequestMapping("/")
    public @ResponseBody String greeting() {
        return "Hello World";
    }

}
```

## 2. 创建启动类

```java
src/main/java/hello/Application.java
```

```java
package hello;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

## 3. 添加依赖

```java
#maven
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>

#gradle
testCompile("org.springframework.boot:spring-boot-starter-test")
```

## 4.1 创建测试用例

- `@RunWith` and `@SpringBootTest`注解测试类
- `@Test`注解一般测试用例
- `@Test(expected = Exception.class)`测试方法期望得到的异常类，
  如果方法执行没有抛出指定的异常，则测试失败
- `@Before`在每个测试方法前执行，一般用来初始化方法
- `@After`在每个测试方法后执行，在方法执行完成后要做的事情

```java
src/test/java/hello/ContextLoadTest.java
```

```java
package hello;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
@SpringBootTest
public class ContextLoadTest {
    private static final Logger log = LoggerFactory.getLogger(ContextLoadTest.class);
    @Autowired
    private GreetingController controller;

    @Test
    public void contexLoads() throws Exception {
        log.info("测试中");
        assertThat(controller).isNotNull();
    }
    @Before
    public void testBefore(){
        log.info("测试前");
    }
    @After
    public void testAfter(){
        log.info("测试后");
    }
}
```

`@SpringBootTest`注解告诉 springboot 去哪寻找主要配置类(用@SpringBootApplication 注解的类)

## 4.2

我们发现`SpringRunner`底层使用的是`JUnit4`

```java
/**
 * <p><strong>NOTE:</strong> This class requires JUnit 4.12 or higher.
 *
 * @author Sam Brannen
 * @since 4.3
 * @see SpringJUnit4ClassRunner
 * @see org.springframework.test.context.junit4.rules.SpringClassRule
 * @see org.springframework.test.context.junit4.rules.SpringMethodRule
 */
public final class SpringRunner extends SpringJUnit4ClassRunner {
```

## 5. Http 请求测试用例

- `@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)`
  随机生成测试启动的端口
- `@LocalServerPort`注入获取随机生成的端口

```java
import org.junit.Test;
import org.junit.runner.RunWith;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.web.server.LocalServerPort;
import org.springframework.test.context.junit4.SpringRunner;

import static org.assertj.core.api.Assertions.assertThat;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
public class HttpRequestTest {

    public static final String GREETING_URL = "/greeting";
    /**
     * Note the use of webEnvironment=RANDOM_PORT to start the server with a random port
     * (useful to avoid conflicts in test environments),
     * and the injection of the port with @LocalServerPort
     */
    @LocalServerPort
    private int port;

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    public void greetingShouldReturnDefaultMessage() throws Exception {
        String responseStr = this.restTemplate.getForObject("http://localhost:" + port + GREETING_URL,
                String.class);
        assertThat(responseStr.contains("Hello World"));
    }
}
```

## idea 设置

- `settings -> Gradle -> 勾选Create directories for empty content roots automatically`
- `Build and run using`选择`gradle`
- `Run tests using`选择`gradle`

![gradle_test](./img/gradle/gradle_test.png)
