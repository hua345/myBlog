[TOC]

# springboot MapStruct集成

## 参考

- [MapStruct官网](https://mapstruct.org/)
- [MapStruct文档](https://mapstruct.org/documentation/stable/reference/html/#configuration-options)



## mapStruct简介

> MapStruct is a code generator that greatly simplifies the implementation of mappings between Java bean types based on a convention over configuration approach.
>
> The generated mapping code uses plain method invocations and thus is fast, type-safe and easy to understand.
>
> `MapStruct `是一种代码生成器，它根据基于配置方法的约定大大简化了`Java bean`之间的映射实现。
>
> 生成的映射代码使用简单的方法调用，因此速度快、类型安全且易于理解。

## mapStruct pom配置

```xml
    <properties>
        <java.version>1.8</java.version>
        <mapstruct.version>1.4.2.Final</mapstruct.version>
        <maven-compiler-plugin.version>3.8.1</maven-compiler-plugin.version>
        <lombok.version>1.18.22</lombok.version>
    </properties>
    <dependency>
        <groupId>org.mapstruct</groupId>
        <artifactId>mapstruct</artifactId>
        <version>${mapstruct.version}</version>
    </dependency>
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>${maven-compiler-plugin.version}</version>
                <configuration>
                    <source>${java.version}</source>
                    <target>${java.version}</target>
                    <annotationProcessorPaths>
                        <path>
                            <groupId>org.projectlombok</groupId>
                            <artifactId>lombok</artifactId>
                            <version>${lombok.version}</version>
                        </path>
                        <path>
                            <groupId>org.mapstruct</groupId>
                            <artifactId>mapstruct-processor</artifactId>
                            <version>${mapstruct.version}</version>
                        </path>
                    </annotationProcessorPaths>
                </configuration>
            </plugin>
        </plugins>
    </build>
```

## mapStruct示例

### 新增`Book`和`BookVo`类

```
@Data
public class Book {
    private Long id;
    private String name;
    private BigDecimal price;

    public Book() {
    }

    public Book(Long id, String name, BigDecimal price) {
        this.id = id;
        this.name = name;
        this.price = price;
    }
}
@Data
public class BookVo {
    private Long id;
    private String bookName;
    private BigDecimal price;
}
```

### 新增mapStruct转换类

```
@Mapper(unmappedTargetPolicy = ReportingPolicy.ERROR)
public interface BookBoMapper {

    BookBoMapper MAPPER = Mappers.getMapper(BookBoMapper.class);

    /**
     * 转换对象
     */
    @Mapping(source = "name", target = "bookName")
    BookVo toVo(Book s);
}
```

### 新增单元测试

```
    public static Book book;

    @BeforeAll
    public static void initData() {
        book = new Book(10L, "刻意练习", BigDecimal.valueOf(20));
    }

    @Test
    @DisplayName("mapStruct转换")
    public void testMapStruct() {
        for (int i = 0; i < TEST_TIMES; i++) {
            BookVo bookVo = BookBoMapper.MAPPER.toVo(book);
            assertEquals(book.getId(), bookVo.getId());
            assertEquals(book.getName(), bookVo.getBookName());
            assertEquals(book.getPrice(), bookVo.getPrice());
        }
    }
```

### 查看生成的代码

`target/generated-sources/annotations/BookBoMapperImpl`

```
public class BookBoMapperImpl implements BookBoMapper {

    @Override
    public BookVo toVo(Book s) {
        if ( s == null ) {
            return null;
        }

        BookVo bookVo = new BookVo();

        bookVo.setBookName( s.getName() );
        bookVo.setId( s.getId() );
        bookVo.setPrice( s.getPrice() );

        return bookVo;
    }
}
```

## [*@Mapper*注解](https://mapstruct.org/documentation/stable/reference/html/#retrieving-mapper)

在接口上添加这个注解，MapStruct才会去实现该接口

获取转换器的方式根据 `@Mapper` 注解的 `componentModel` 属性不同而不同，支持以下四种不同的取值：

1. **default** 默认方式，使用工厂方式（`Mappers.getMapper(Class) `）来获取，无状态、线程安全
2. **spring** 自动添加注解`@Component`，通过`@Autowired`方式注入，在 `Spring` 框架中推荐使用此方式
3. **cdi** 此时生成的映射器是一个应用程序范围的 `CDI bean`，使用 `@Inject` 注解来获取
4. **jsr330** 生成的映射器用 `@javax.inject.Named` 和 `@Singleton` 注解，通过 `@Inject` 来获取




## [mappings定义](https://mapstruct.org/documentation/stable/reference/html/#basic-mappings)

> The `@Mapper` annotation causes the MapStruct code generator to create an implementation of the `BookBoMapper` interface during build-time.
>
> `@Mapper`注解会在`BookBoMapper`接口编译期间生成实现类

### 多个不同参数

```
@Mapper(unmappedTargetPolicy = ReportingPolicy.ERROR)
public interface BookBoMapper {

    BookBoMapper INSTANCE = Mappers.getMapper(BookBoMapper.class);
    /**
     * 转换对象
     */
    @Mapping(source = "book.id", target = "id")
    @Mapping(source = "book2.name", target = "bookName")
    @Mapping(source = "book2.price", target = "price")
    BookVo multiToVo(Book book, Book book2);
}
```

### 更新已有的bean

在某些情况下，您需要映射，这些映射不会创建目标类型的新实例，而是更新该类型的现有实例。这种映射可以通过为目标对象添加参数并标记此参数来实现。

```
@Mapper(unmappedTargetPolicy = ReportingPolicy.ERROR)
public interface BookBoMapper {

    BookBoMapper INSTANCE = Mappers.getMapper(BookBoMapper.class);

    /**
     * 更新对象
     */
    @Mapping(source = "name", target = "bookName")
    void updateBookVo(Book book, @MappingTarget BookVo bookVo);
}
```

