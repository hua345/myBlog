# 注解说明

```java
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
```

## jpa配置

```conf
spring.jpa.show-sql=true
spring.jpa.hibernate.ddl-auto=update
spring.jpa.database-platform=org.hibernate.dialect.MySQL5InnoDBDialect
```

## @Entity

标注用于实体类声明语句之前，指出该 Java 类为实体类，将映射到指定的数据库表。

如声明一个实体类`Customer`，将它映射到数据的`coustomer`表上。

```java
@Documented
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
public @interface Entity {
    String name() default "";
}

@Entity
public class Customer {

    @Id
    @GeneratedValue(strategy=GenerationType.AUTO)
    private Long id;
    private String firstName;
    private String lastName;
}
```

## @Table

当实体类与其映射的数据库表名不同名时，需要使用`@Table`标注说明，该注解与`@Entity`标注并列使用，置于实体类声明语句之前，可写于单独语句行，也可与声明数据同行。

> Table 用来定义 entity 主表的 name，catalog，schema 等属性。

```java
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
public @interface Table {
    String name() default "";

    String catalog() default "";

    String schema() default "";

    UniqueConstraint[] uniqueConstraints() default {};

    Index[] indexes() default {};
}


@Entity
@Table(name = "jpa_person",
        uniqueConstraints = {@UniqueConstraint(columnNames = {"first_name", "last_name"})},
        indexes = {@Index(name = "person_index_name", columnList = "last_name")})
@SequenceGenerator(name = "my_id", initialValue = 1, allocationSize = 2)
public class Person {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO, generator = "my_id")
    private Long id;
}
```

## @DynamicUpdate

```java
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
public @interface DynamicUpdate {
    boolean value() default true;
}
```

表示update对象的时候,生成动态的update语句,如果这个字段的值是null就不会被加入到update语句中,默认false。

## @DynamicInsert

```java
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
public @interface DynamicInsert {
    boolean value() default true;
}
```

表示insert对象的时候,生成动态的insert语句,如果这个字段的值是null就不会加入到insert语句当中.默认false。

## @Id

`@Id`标注用于声明一个实体类的属性映射为数据库的主键列

```java
@Target({ElementType.METHOD, ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
public @interface Id {
}
```

## @GeneratedValue

`@GeneratedValue`用于标注主键的生成策略，通过 strategy 属性指定。

```java
@Target({ElementType.METHOD, ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
public @interface GeneratedValue {
    GenerationType strategy() default GenerationType.AUTO;

    String generator() default "";
}
```

```java
public enum GenerationType {
    TABLE,
    SEQUENCE,
    IDENTITY,
    AUTO;

    private GenerationType() {
    }
}
```

- 默认情况下，JPA 自动选择一个最合适底层数据库的主键生成策略：`MySql`对应`auto increment`，`postgres`对应`sequence`。
- IDENTITY：主键由数据库生成，一般为自增型主键，支持的有`MySql`和`Sql Server`
- AUTO：JPA 自动选择合适的策略，是默认选项
- SEQUENCE：使用序列的方式，且其底层数据库要支持序列，通过`@SequenceGenerator`注解指定序列名，一般有`postgres`、`Oracle`等
- TABLE：通过表产生键，框架借助由表模拟序列产生主键，使用该策略可以使应用更易于数据库移植

## @Column

`@Column`元数据定义了映射到数据库的列的所有属性：列名，是否唯一，是否允许为空，是否允许更新等

```java
@Target({ElementType.METHOD, ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
public @interface Column {
    String name() default "";

    boolean unique() default false;

    boolean nullable() default true;

    boolean insertable() default true;

    boolean updatable() default true;

    String columnDefinition() default "";

    String table() default "";

    int length() default 255;

    int precision() default 0;

    int scale() default 0;
}
```

## @Transient

`@Transient`表示该属性并不是一个到数据库表的字段的映射，指定的这些属性不会被持久化，`ORM`框架将忽略该属性。
如果一个属性并非数据库表的字段映射。就务必将其标示为`@Transient`。否则，`ORM`框架默认其注解为`@Basic`

```java
@Target({ElementType.METHOD, ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
public @interface Transient {
}
```

```java
    @Transient
    private String version;
```

## @SequenceGenerator

`SequenceGenerator`定义一个主键值生成器，在 Id 这个元数据的 generator 属性中可以使用生成器的名字

元数据属性说明

- `name`:生成器的唯一名字，可以被 Id 元数据使用。
- `sequenceName`:数据库中，sequence 对象的名称。如果不指定，会使用提供商指定的默认名称。
- `initialValue`:id 值的初始值。
- `allocationSize`:id 值的增量。

```java
@Repeatable(SequenceGenerators.class)
@Target({ElementType.TYPE, ElementType.METHOD, ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
public @interface SequenceGenerator {
    String name();

    String sequenceName() default "";

    String catalog() default "";

    String schema() default "";

    int initialValue() default 1;

    int allocationSize() default 50;
}
```

```java
@Entity
@Table(name = "jpa_person")
@SequenceGenerator(name = "my_id", initialValue = 1, allocationSize = 2)
public class Person {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO, generator = "my_id")
    private Long id;
}
```

## @Version

`Version`指定实体类在乐观事务中的`version`属性。在实体类重新由`EntityManager`管理并且加入到乐观事务中时，保证完整性。

```java
    @Version
    private int versionNum;
```

```java
@Target({ElementType.METHOD, ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
public @interface Version {
}
```
