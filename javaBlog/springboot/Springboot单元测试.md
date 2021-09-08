[TOC]

# 参考

- [Testing the Web Layer](https://spring.io/guides/gs/testing-web/)
- [Mockito framework site](https://site.mockito.org/)
- [https://github.com/spring-guides/gs-testing-web](https://github.com/spring-guides/gs-testing-web)

`Spring Boot 2.2.0` 版本开始引入 `Junit5` 作为单元测试默认库

## 1. 添加依赖

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>2.4.4</version>
    <relativePath/> <!-- lookup parent from repository -->
</parent>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
```



## 2.创建测试用例

## 2.1 创建简单测试用例

- `@Test`注解一般测试用例
- `@DisplayName`设置测试用例显示名称
- `@BeforeAll`,`@AfterAll`测试类执行前/后运行的方法,需要`public static`,替代`junit4`中`@BeforeClass,@AfterClass`
- `@BeforeEach`,`@AfterEach`在每个测试用例前/后执行,替代`junit4`中`@Before,@After`
- `@RepeatedTest(5)`设置单元测试执行次数

```java
import lombok.extern.slf4j.Slf4j;

import org.junit.jupiter.api.*;

@Slf4j
public class JunitTest {
    @BeforeAll
    public static void testBeforeAll() {
        log.info("BeforeAll");
    }

    @BeforeEach
    public void testBeforeEach() {
        log.info("BeforeEach");
    }

    @AfterAll
    public static void testAfterAll() {
        log.info("AfterAll");
    }

    @AfterEach
    public void testAfterEach() {
        log.info("AfterEach");
    }

    @Test
    @DisplayName("junit单元测试1")
    public void junitTest() {
        log.info("单元测试1");
    }

    @Test
    @DisplayName("junit单元测试2")
    public void junitTest2() {
        log.info("单元测试2");
    }
}
```

```log
14:52:25.744 [main] INFO com.github.springbootjunittest.JunitTest - BeforeAll
14:52:25.766 [main] INFO com.github.springbootjunittest.JunitTest - BeforeEach
14:52:25.769 [main] INFO com.github.springbootjunittest.JunitTest - 单元测试2
14:52:25.775 [main] INFO com.github.springbootjunittest.JunitTest - AfterEach
14:52:25.787 [main] INFO com.github.springbootjunittest.JunitTest - BeforeEach
14:52:25.788 [main] INFO com.github.springbootjunittest.JunitTest - 单元测试1
14:52:25.789 [main] INFO com.github.springbootjunittest.JunitTest - AfterEach
14:52:25.792 [main] INFO com.github.springbootjunittest.JunitTest - AfterAll
```

## 2.2 断言

- `Assertions.assertEquals(expected, actual)`断言相等
- `Assertions.assertTrue()`断言是否为`true`
- `Assertions.assertNotNull()`断言不为空

- `Assertions.assertThrows()`断言出现异常

```
        NumberFormatException exception = Assertions.assertThrows(
                NumberFormatException.class,
                () -> Integer.parseInt("one"));
        Assertions.assertEquals("For input string: \"one\"", exception.getMessage());
```



### 2.3 springboot测试

- `@SpringBootTest`启动`springboot`上下文环境

```java
@BootstrapWith(SpringBootTestContextBootstrapper.class)
@ExtendWith(SpringExtension.class)
public @interface SpringBootTest  {
	WebEnvironment webEnvironment() default WebEnvironment.MOCK;
}
```

- - `WebEnvironment.MOCK`,该类型提供一个mock环境，可以和`@AutoConfigureMockMvc`搭配使用，开启`Mock`相关的功能。注意此时内嵌的服务`servlet容器`并没有真正启动，也`不会监听web服务端口`。
  - `WebEnvironment.RANDOM_PORT`,启动一个真实的web服务,用随机端口运行测试用例, 可以使用` @LocalServerPort`注入端口
  - `WebEnvironment.DEFINED_PORT`,启动一个真实的web服务，监听一个定义好的端口（从`application.properties`读取）
- `@ActiveProfiles("dev")`选择测试环境

### 2.3.1 WebEnvironment.RANDOM_PORT测试

- `@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)`
  随机生成测试启动的端口
- `@LocalServerPort`注入获取随机生成的端口

```java
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.web.server.LocalServerPort;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
public class HttpRequestTest {

	@LocalServerPort
	private int port;

	@Autowired
	private TestRestTemplate restTemplate;

	@Test
	public void greetingShouldReturnDefaultMessage() throws Exception {
		assertThat(this.restTemplate.getForObject("http://localhost:" + port + "/",
				String.class)).contains("Hello, World");
	}
}
```

### 2.3.2 WebEnvironment.MOCK测试

```
@Slf4j
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK)
@ActiveProfiles("dev")
@AutoConfigureMockMvc
class HelloControllerTest {

    @Autowired
    private MockMvc mockMvc;

    private final Charset defaultCharset = StandardCharsets.UTF_8;

    @Test
    void testPostHello() throws Exception {
        HelloParam helloParam = new HelloParam();
        helloParam.setName("fang");
        MvcResult mvcResult = mockMvc.perform(
                        post("/postHello")
                                .contentType(MediaType.APPLICATION_JSON)
                                .content(JsonUtil.toJsonString(helloParam))
                                .accept(MediaType.APPLICATION_JSON))
                .andExpect(MockMvcResultMatchers.status().isOk())
                .andReturn();

        ResponseVO responseVO = JsonUtil.toBean(mvcResult.getResponse().getContentAsString(defaultCharset), ResponseVO.class);
        Assertions.assertNotNull(responseVO);
        Assertions.assertEquals(ResponseStatusEnum.SUCCESS.getErrorCode(), responseVO.getCode());
        log.info("responseVO:{}", JsonUtil.toJsonString(responseVO));
    }
}
```

## 3. MockBean和SpyBean模拟对象

- [Mockito framework site](https://site.mockito.org/)

`SpyBean`和`MockBean`是`spring-boot-test`包所提供的两个注解，用于Spy或Mock Spring容器所管理的实例。

而Spy与Mock的方式正好相反，spy默认所有方法均真实调用，Mock默认所有方法均调用mock的实现。 

```
List list = new LinkedList();
List spy = spy(list);

//Impossible: real method is called so spy.get(0) throws IndexOutOfBoundsException (the list is yet empty)
when(spy.get(0)).thenReturn("foo");

//You have to use doReturn() for stubbing
doReturn("foo").when(spy).get(0);

```

```
// you can mock concrete classes, not only interfaces
LinkedList mockedList = mock(LinkedList.class);

// stubbing appears before the actual execution
when(mockedList.get(0)).thenReturn("first");

// the following prints "first"
System.out.println(mockedList.get(0));

// the following prints "null" because get(999) was not stubbed
System.out.println(mockedList.get(999));
```

