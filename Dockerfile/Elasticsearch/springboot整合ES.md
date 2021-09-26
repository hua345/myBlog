# springboot整合ES

## 参考

- [Spring Data Elasticsearch](https://spring.io/projects/spring-data-elasticsearch)
- [Spring Data Elasticsearch对应ES版本](https://docs.spring.io/spring-data/elasticsearch/docs/4.2.5/reference/html/#preface.versions)
- [Spring Data Elasticsearch注解](https://docs.spring.io/spring-data/elasticsearch/docs/4.2.5/reference/html/#elasticsearch.mapping.meta-model.annotations)
- [Spring Data Elasticsearch主要类](https://docs.spring.io/spring-data/elasticsearch/docs/4.2.5/reference/html/#elasticsearch.operations)

## 引入依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-elasticsearch</artifactId>
</dependency>
```

```java
// type数据类型
@Field(type = FieldType.Text, store = true, fielddata = true)

```





- 使用`ElasticsearchTemplate`
- `IndexOperations` defines actions on index level like creating or deleting an index.
- `DocumentOperations` defines actions to store, update and retrieve entities based on their id.
- `SearchOperations` define the actions to search for multiple entities using queries
- `ElasticsearchOperations` combines the `DocumentOperations` and `SearchOperations` interfaces.

```java
    @Autowired
    private RestHighLevelClient restHighLevelClient;

    @Autowired
    private ElasticsearchRestTemplate restTemplate;

    @Order(1)
    @DisplayName("创建ES索引")
    @Test
    public void createDocument() {
        IndexOperations indexOperations = restTemplate.indexOps(JdProduct.class);
        boolean exist = indexOperations.exists();
        indexOperations.createSettings();
        if (!exist) {
            // 创建索引Settings
            Assertions.assertTrue(indexOperations.create());
            // 创建索引Mapping
            Assertions.assertTrue(indexOperations.putMapping(indexOperations.createMapping()));
        }
    }

```



