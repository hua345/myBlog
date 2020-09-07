# LocalDateTime

`LocalDateTime`本身不包含时区信息，它存储的是年、月、日、时分秒，纳秒这样的数字

在不同的时区下，这样的数字代表不同的时间。

```java
LocalDateTime.now()
// 或者手动指定时区
LocalDateTime.now(ZoneId.of("+08:00"))
// LocalDateTime既然不带时区 为什么这里又有时区了呢
// 如果只是为了获取当前系统所在默认时区的一个本地时间，那么用LocalDateTime.now()无参数构造方法即可
// 在构造后，LocalDateTime同样不携带时区信息，仍然只是表示一个显示时间而已。
```

设置`springboot`默认时区

```java
public class Application {
    @PostConstruct
    void started() {
        TimeZone.setDefault(TimeZone.getTimeZone("Asia/Shanghai"));
    }
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

## mysql配置

```sql
-- 查看mysql时间。和当前时间做对比
select now();

-- 查看当前时区
show variables like '%time_zone%';
```

[`mysql连接字符串`](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-reference-configuration-properties.html)

```conf
useSSL=false&serverTimezone=Asia/Shanghai
```

## jackson配置

```java
        /**
         * https://github.com/FasterXML/jackson-databind#commonly-used-features
         */
        mapper = new ObjectMapper().setVisibility(PropertyAccessor.FIELD, JsonAutoDetect.Visibility.ANY);
        // 对Date格式化
        mapper.setDateFormat(new SimpleDateFormat("yyyy-MM-dd HH:mm:ss"));
        // 对LocalDateTime格式化
        JavaTimeModule javaTimeModule = new JavaTimeModule();
        //处理LocalDateTime
        DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern(DATE_TIME_PATTERN);
        javaTimeModule.addSerializer(LocalDateTime.class, new LocalDateTimeSerializer(dateTimeFormatter));
        javaTimeModule.addDeserializer(LocalDateTime.class, new LocalDateTimeDeserializer(dateTimeFormatter));
        // https://github.com/FasterXML/jackson-modules-java8
        // javaTimeModule注册时间模块, 支持支持jsr310, 即新的时间类(java.time包下的时间类)
        // Jdk8Module模块可以使用java8 Optional
        // ParameterNamesModule可以使用bean构造函数替代注解JsonProperty
        mapper.registerModule(javaTimeModule);
```

## [mybatis](https://github.com/mybatis/mybatis-3/releases)

[mybatis-3.4.5](https://github.com/mybatis/mybatis-3/releases/tag/mybatis-3.4.5)已经支持`JSR-310 (Java Date and Time API)`规范了

## jpa

```java
    /**
     * 创建时间
     */
    @CreationTimestamp
    @Temporal(TemporalType.TIMESTAMP)
    @Column(updatable = false, nullable = false)
    @JsonFormat(timezone = "GMT+8", pattern = "yyyy-MM-dd HH:mm:ss")
    protected LocalDateTime createTime;
```

报错`Invocation of init method failed; nested exception is org.hibernate.AnnotationException: @Temporal should only be set on a java.util.Date or java.util.Calendar property`

`@Temporal`注解只能用在`java.util.Date or java.util.Calendar`

添加`jpa`配置

```java
@Converter(autoApply = true)
public class LocalDateTimeConverter implements AttributeConverter<LocalDateTime, Timestamp> {

    @Override
    public Timestamp convertToDatabaseColumn(LocalDateTime attribute) {
        return attribute == null ? null : Timestamp.valueOf(attribute);
    }

    @Override
    public LocalDateTime convertToEntityAttribute(Timestamp dbData) {
        return dbData == null ? null : dbData.toLocalDateTime();
    }
}
```

```java
    /**
     * 创建时间
     */
    @CreationTimestamp
    @Column(updatable = false, nullable = false)
    @JsonFormat(timezone = "GMT+8", pattern = "yyyy-MM-dd HH:mm:ss")
    protected LocalDateTime createTime;
```
