# stream 流

stream流，像流水一样，可以将多个操作连接起来。同时支持函数式编程，代码非常简洁。

## 2.1排序 `sorted`

`sorted` 提供了 2 个接口：

- `sorted()` 默认使用自然序排序， 其中的元素必须实现`Comparable`接口 。
- `sorted(Comparator<? super T> comparator)` ：我们可以使用`lambada`来创建一个`Comparator`实例。可以按照升序或着降序来排序元素。

```java
@Data
public class Book {
    private Long id;
    private String name;
    private BigDecimal price;

    public Book(Long id, String name, BigDecimal price) {
        this.id = id;
        this.name = name;
        this.price = price;
    }
    private Book(){}
}

public static void main(String[] args) {
    List<Book> bookList = new LinkedList<>();
    bookList.add(new Book(1L, "数学之美", new BigDecimal(21)));
    bookList.add(new Book(3L, "非暴力沟通", new BigDecimal(23)));
    bookList.add(new Book(2L, "秘密花园", new BigDecimal(22)));
    bookList.stream().sorted(Comparator.comparing(Book::getId)).forEach(System.out::println);
    bookList.stream().sorted(Comparator.comparing(Book::getId).reversed()).forEach(System.out::println);
}
```

```log
Book(id=1, name=数学之美, price=21)
Book(id=2, name=秘密花园, price=22)
Book(id=3, name=非暴力沟通, price=23)
Book(id=3, name=非暴力沟通, price=23)
Book(id=2, name=秘密花园, price=22)
Book(id=1, name=数学之美, price=21)
```

## 筛选操作`filter`和`distinct`

- `distinct()`:通过`hashCode`和`equals`去除重复元素。

```java
public static void main(String[] args) {
    List<Book> bookList = new LinkedList<>();
    bookList.add(new Book(1L, "数学之美", new BigDecimal(21)));
    bookList.add(new Book(3L, "哈佛幸福课", new BigDecimal(21)));
    bookList.add(new Book(3L, "非暴力沟通", new BigDecimal(23)));
    bookList.add(new Book(2L, "刻意练习:如何从新手到大师", new BigDecimal(22)));
    bookList.stream().filter(item -> item.getId() >= 2L).forEach(System.out::println);
    bookList.stream().map(Book::getId).distinct().forEach(System.out::println);
}
```

```log
Book(id=3, name=哈佛幸福课, price=21)
Book(id=3, name=非暴力沟通, price=23)
Book(id=2, name=刻意练习:如何从新手到大师, price=22)
1
3
2
```

## 映射操作map(T -> R)

映射操作，就像一个管道，可以将流中的元素`T`通过一个函数进行映射，返回一个新的元素`R`。

```java
public static void main(String[] args) {
    List<Book> bookList = new LinkedList<>();
    bookList.add(new Book(1L, "数学之美", new BigDecimal(21)));
    bookList.add(new Book(3L, "哈佛幸福课", new BigDecimal(21)));
    bookList.add(new Book(3L, "非暴力沟通", new BigDecimal(23)));
    bookList.add(new Book(2L, "刻意练习:如何从新手到大师", new BigDecimal(22)));
    bookList.stream().map(Book::getName).distinct().forEach(System.out::println);
}
```

```log
数学之美
哈佛幸福课
非暴力沟通
刻意练习:如何从新手到大师
```

### flatMap(T -> Stream)

将流中的每一个元素 T 映射为一个流，再把每一个流连接成为一个流

```java
Map<Long, List<Book>> bookMap = bookList.stream().collect(Collectors.groupingBy(Book::getId));
List<Book> originList = bookMap.values().stream().flatMap(List::stream).collect(Collectors.toList());
```

```log
{1=[Book(id=1, name=数学之美, price=21)], 2=[Book(id=2, name=刻意练习:如何从新手到大师, price=22)], 3=[Book(id=3, name=哈佛幸福课, price=21), Book(id=3, name=非暴力沟通, price=23)]}
[Book(id=1, name=数学之美, price=21), Book(id=2, name=刻意练习:如何从新手到大师, price=22), Book(id=3, name=哈佛幸福课, price=21), Book(id=3, name=非暴力沟通, price=23)]
```

## Reduce

`reduce`就是减少的意思，它会将集合中的所有值根据规则计算，最后只返回一个结果。

```java
// 只有一个参数时为累加器
Optional<T> reduce(BinaryOperator<T> var1)
// 第一个参数是我们给出的初值，第二个参数是累加器
T reduce(T var1, BinaryOperator<T> var2)
```

```java
public static void main(String[] args) {
    List<Book> bookList = new LinkedList<>();
    bookList.add(new Book(1L, "数学之美", new BigDecimal(21)));
    bookList.add(new Book(3L, "哈佛幸福课", new BigDecimal(21)));
    bookList.add(new Book(3L, "非暴力沟通", new BigDecimal(23)));
    bookList.add(new Book(2L, "刻意练习:如何从新手到大师", new BigDecimal(22)));
    // 求和
    bookList.stream().map(Book::getPrice).reduce((x, y) -> x.add(y)).ifPresent(System.out::println);
    BigDecimal result = bookList.stream().map(Book::getPrice).reduce(BigDecimal.ZERO, BigDecimal::add);
    // 求最小值
    bookList.stream().map(Book::getId).reduce((x, y) -> x >= y ? y : x).ifPresent(System.out::println);
    // 求最小值
    bookList.stream().map(Book::getName).reduce(new BinaryOperator<String>() {
        @Override
        public String apply(String s, String s2) {
            return s.concat(":").concat(s2);
        }
    }).ifPresent(System.out::println);
}
```

```java
87
1
数学之美:哈佛幸福课:非暴力沟通:刻意练习:如何从新手到大师
```

## Collect

collect是一个非常常用的末端操作，它本身的参数很复杂，有3个：

`<R> R collect(Supplier<R> var1, BiConsumer<R, ? super T> var2, BiConsumer<R, R> var3);`

还好，考虑到我们日常使用，java8提供了一个收集器`Collectors`，它是专门为`collect`方法量身打造的接口：

我们常常使用collect将流转换成`List`,`Map`或`Set`:

```java
// 转换成list
List<Book> list = bookList.stream().collect(Collectors.toList());
// 转换成Set
Set<Long> set = bookList.stream().map(Book::getId).collect(Collectors.toSet());
// 转换成Map
Map<String, Book> map = bookList.stream().collect(Collectors.toMap(Book::getName, Function.identity()));
Map<String, Long> nameMap = bookList.stream().collect(Collectors.toMap(Book::getName,Book::getId));

// toMap 如果集合对象有重复的key，会报错Duplicate key ....
// 可以用 (k1,k2)->k1 来设置，如果有重复的key,则保留key1,舍弃key2
Map<String, Book> nameMap = bookList.stream().collect(Collectors.toMap(Book::getId,a -> a,(k1,k2)->k1)));
```

```log
{数学之美=Book(id=1, name=数学之美, price=21), 刻意练习:如何从新手到大师=Book(id=2, name=刻意练习:如何从新手到大师, price=22), 哈佛幸福课=Book(id=3, name=哈佛幸福课, price=21), 非暴力沟通=Book(id=3, name=非暴力沟通, price=23)}
{数学之美=1, 刻意练习:如何从新手到大师=2, 哈佛幸福课=3, 非暴力沟通=3}
```

### joining 连接字符串

也是一个比较常用的方法，对流里面的字符串元素进行连接，其底层实现用的是专门用于字符串连接的 StringBuilder

```java
String nameStr = bookList.stream().map(Book::getName).collect(Collectors.joining(","));
```

`数学之美,哈佛幸福课,非暴力沟通,刻意练习:如何从新手到大师`

### `groupingBy` 分组

```java
Map<Long, List<Book>> bookMap = bookList.stream().collect(Collectors.groupingBy(Book::getId));
// 等同于
Map<Long, List<Book>> bookMap = bookList.stream().collect(Collectors.groupingBy(Book::getId, Collectors.toList()));
```

```log
{1=[Book(id=1, name=数学之美, price=21)], 2=[Book(id=2, name=刻意练习:如何从新手到大师, price=22)], 3=[Book(id=3, name=哈佛幸福课, price=21), Book(id=3, name=非暴力沟通, price=23)]}
```

```java
Map<Long,Long> aa = bookList.stream().collect(Collectors.groupingBy(Book::getId, Collectors.counting()))
// {1=1, 2=1, 3=2}
```

### `partitioningBy` 分区

分区与分组的区别在于，分区是按照`true`和`false`来分的，因此`partitioningBy` 接受的参数的 lambda 也是 T -> boolean

```java
Map<Boolean, List<Book>> partitioningMap = bookList.stream().collect(Collectors.partitioningBy(item -> item.getId() > 2));
// 等同于
Map<Boolean, List<Book>> partitioningMap = bookList.stream().collect(Collectors.groupingBy(item -> item.getId() > 2));
```

```log
{false=[Book(id=1, name=数学之美, price=21), Book(id=2, name=刻意练习:如何从新手到大师, price=22)], true=[Book(id=3, name=哈佛幸福课, price=21), Book(id=3, name=非暴力沟通, price=23)]}
```
