# 命名查询

| 关键字             | 方法命名                       | sql where 字句             |
| ------------------ | ------------------------------ | -------------------------- |
| And                | findByNameAndPwd               | where name= ? and pwd =?   |
| or                 | findByNameOrSex                | where name= ? or sex=?     |
| Is,Equals          | findById,findByIdEquals        | where id= ?                |
| Between            | findByIdBetween                | where id between ? and ?   |
| LessThan           | findByIdLessThan               | where id < ?               |
| LessThanEquals     | findByIdLessThanEquals         | where id <= ?              |
| GreaterThan        | findByIdGreaterThan            | where id > ?               |
| GreaterThanEquals  | findByIdGreaterThanEquals      | where id > = ?             |
| After              | findByIdAfter                  | where id > ?               |
| Before             | findByIdBefore                 | where id < ?               |
| IsNull             | findByNameIsNull               | where name is null         |
| IsNotNull, NotNull | findByNameNotNull              | where name is not null     |
| Like               | findByNameLike                 | where name like ?          |
| NotLike            | findByNameNotLike              | where name not like ?      |
| StartingWith       | findByNameStartingWith         | where name like ‘?%’       |
| EndingWith         | findByNameEndingWith           | where name like ‘%?’       |
| Containing         | findByNameContaining           | where name like ‘%?%’      |
| OrderBy            | findByIdOrderByXDesc           | where id=? order by x desc |
| Not                | findByNameNot                  | where name <> ?            |
| In                 | findByIdIn(Collection<?> c)    | where id not in (?)        |
| NotIn              | findByIdNotIn(Collection<?> c) | where id in (?)            |
| True               | findByAaaTrue                  | where aaa = true           |
| False              | findByAaaFalse                 | where aaa = false          |
| IgnoreCase         | findByNameIgnoreCase           | where UPPER(name)=UPPER(?) |

## 查询示例

```java
//查询第一条记录First
Account findFirstByOrderByCreateAtDesc();

//排序ASC DESC，以下分别按lastname升序，按age降序
User findFirstByOrderByChannelCodeAsc();
User findTopByOrderByChannelCodeDesc();

//带分页，Pageable为分页参数，实现类PageRequest，通过PageRequest.of(...)生成分页对象
Page queryFirst10ByVmCode(String vmCode, Pageable pageable);
Slice findTop3ByVmCode(String vmCode, Pageable pageable);

//带Sort排序，查询前10条
List findFirst10ByVmCode(String vmCode, Sort sort);
```

`Sort` 和 `Pageable` 放方法参数列表的最后

## 动态 SQL

### 单表动态条件查询

前端传来 N 个字段，随机组合其中几个字段组成 SQL 进行查询

```java
Page<Node> page;
Specification<Node> cation = (root, query, builder) -> {
        List<Predicate> predicates = new ArrayList<>();

        if (!StringUtils.isEmpty((nodeParam.getCompanyCode()))) {
            predicates.add(builder.equal(root.get("companyCode"), nodeParam.getCompanyCode()));
        }

        if (!StringUtils.isEmpty(nodeParam.getNodeName())) {
            predicates.add(builder.like(root.get("nodeName"), "%" + nodeParam.getNodeName() + "%"));
        }

        if (predicates.size() > 1) {
             return builder.and(predicates.toArray(new Predicate[predicates.size()]));
        } else if (predicates.size() == 1) {
            return predicates.get(0);
        } else {
            return null;
        }
};
page = nodeRepository.findAll(cation, nodeParam.getPageable());
```

### 多表动态条件查询

4 张表动态 SQL，前端传来 N 个字段，随机组合其中几个字段组成 SQL 进行查询

```java
Specification<ErrorRender> cation = (root, criteriaQuery, builder) -> {
        List<Predicate> predicates = new ArrayList<>();

        predicates.add(builder.greaterThan(root.get("vmCode"), vmCode));
        predicates.add(builder.equal(root.get("status"), 0).not());

        //ErrorRender故障表和Vm表进行连接查询，在ErrorRender必须有一个private Vm vm属性
        //相当于 select * from error_render e left join vm v on e.vm=v.vm
        Join<ErrorRender, Vm> vmJoin = root.join("vm", JoinType.LEFT);

        //机型条件 相当于 v.vmTypeId >= 0
        if (vmTypeId >= 0) {
            predicates.add(builder.equal(vmJoin.get("vmTypeId"), vtId));
        }

        // 相当于(left on node n on v.node_id=n.node_id) as tmp left join org o on o.org_id= tmp.org_id
        Join<Vms, Orgas> orgJoin = vmJoin.join("node", JoinType.LEFT).join("org", JoinType.LEFT);

        //带有orgId查询
        Orgas org = orgasRepository.findOne(orgId);
        //相当于 o.hierarchy like org.getHierarchy() + "%"
        predicates.add(builder.like(orgJoin.get("hierarchy"), org.getHierarchy() + "%"));

        if (error != null && error != 0) {
            predicates.add(root.get("error").in(allErrorList));
        }

        if (predicates.size() > 1) {
            return builder.and(predicates.toArray(new Predicate[predicates.size()]));
        } else if (predicates.size() == 1) {
            return predicates.get(0);
        } else {
            return null;
        }
};
```

## JPA 对 SQL 支持

### 删除数据(delete)(HQL)

```java
//删除需要添加@Modifying 注解，@Transactional 可加可不加，加上后，将以 repository 类中的事务为主
@Modifying
@Query("delete from VmModelUnitRelation v where v.vmModelId=?1")
void deleteByVmModelId(Long vmModelId);

//可在仓库类中定义 SQL 语句，在@Query 中引用
String FIND_VM_MODELID = "delete from VmModelUnitRelation v where v.vmModelId=?1";

@Query(FIND_VM_MODELID) //FIND_VM_MODELID 可继续添加查询条件
void deleteByVmModelId(Long vmModelId);
```

### 修改数据（update）(HQL)

```java
//更新需要添加@Modifying 注解 命名参数绑定，对参数顺序要求不严格
@Modifying
@Query(value = "update Vm v set v.deviceCode = :deviceCode where c.id = :vmCode")
public void updateDeviceCode(@Param("vmCode") String vmCode, String deviceCode);

@Modifying
@Query(value = "update Vm v set v.deviceCode = ?2 where c.id = ?1")
public void updateDeviceCode(String vmCode, String deviceCode);
单表查询(HQL)
@Query("select v from Vm v where v.vmCode = ?1 and channelCode = ?2")
User findByVmCodeAndChannelCode(String vmCode, Integer channelCode)

//分页
@Query("select v from Vm v where v.vmCode = ?1 and channelCode = ?2")
User findByVmCodeAndChannelCode(String vmCode, Integer channelCode, Pageable pageable)
```

### 多表连接查询并支持分页(原生 SQL)

只需要设置 nativeQuery 为 true

```java
@Query(value = "SELECT vm.\* FROM vm AS vm LEFT JOIN vm_auailiary AS auailiary ON vm.vm_code != auailiary.vm_code WHERE vm.node_id=:nodeId AND vm.host_type=:hostType",
countQuery = "SELECT count(vm.vm_code) FROM vm AS vm LEFT JOIN vm_auailiary AS auailiary ON vm.vm_code != auailiary.vm_code WHERE vm.node_id=:nodeId AND vm.host_type=:hostType",
nativeQuery = true)
Page<Vm> findByNodeIdAndVmCodeNotIn(@Param("nodeId") String nodeId, @Param("hostType")Integer hostType, Pageable pageable);
```

### 实体自动映射

```java
ManyToOne
@ManyToOne
@Fetch(FetchMode.JOIN)
@JoinColumn(name = "vmTypeId", insertable = false , updatable= false, referencedColumnName = "id", foreignKey=@ForeignKey(ConstraintMode.NO_CONSTRAINT))
private VmType vmType;
```

### JPA N+1 问题

使用@NamedEntityGraph 或@NamedEntityGraphs、@EntityGraph 注解

@NamedEntityGraph 和@NamedEntityGraphs 作用在实体上，@EntityGraph 作用在 repository 的方法上
eg:

#### Vm 实体类配置实体图

```java
@Entity
@Table
@NamedEntityGraph(name="vmGraph",attributeNodes={@NamedAttributeNode("vmTypeId")})
public class Vm extends AbstractModel {

private String vmTypeId;

@OneToOne
@JoinColumn(name="vmTypeId", referencedColumnName="id")
private VmType vmType;
}
```

#### VmRepository 配置实体图

```java
public interface VmRepository extends JpaRepository<Vm, String>{
@EntityGraph(value = "vmGraph" , type=EntityGraphType.FETCH)
Vm findById(String id);
}
```

### 自定义 SQL 和防 SQL 注入

#### 使用原生 SQL

```java
@Service
public class JdbcTemplateService {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Autowired
    private NamedParameterJdbcTemplate nameJdbcTemplate;

    /**
     * 防止SQL注入（适用于参数占位符为 ? 的参数语句，如果参数为命名绑定，则使用Map设置参数）
     * @param sql     sql语句
     * @param params  按 ? 顺序添加参数
     * @param clazz   返回List包含对象class
     */
    public <T> List<T> queryList(String sql, @Nullable Object[] params, Class<T> clazz){
        return jdbcTemplate.queryForList(sql, params, clazz);
    }

    /**
     * 防止SQL注入，适用于参数为命名绑定形式(如 vmCode = :vmCode) （推荐）
     * @param sql       sql语句
     * @param paramMap  参数Map，key为绑定的命名参数（:后面的名称,如上为vmCode）
     * @param clazz     返回List包含对象class
     */
    public <T> List<T> queryList(String sql, Map<String, Object> paramMap, Class<T> clazz){
        if(paramMap == null){
            paramMap = new HashMap<>();
        }
        return nameJdbcTemplate.query(sql, paramMap, new BeanPropertyRowMapper<>(clazz));
    }

    /**
     * 查询单个对象
     * @param sql    sql语句
     * @param clazz  对象class
     */
    public <T> T queryOne(String sql, Class<T> clazz){
        return jdbcTemplate.queryForObject(sql, clazz);
    }

    /**
     * @param sql    sql语句
     * @return       List列表中是一个个返回对象，Map的key为字段名，value为对应字段值
     */
    public List<Map<String, Object>> queryList(String sql){
        return jdbcTemplate.queryForList(sql);
    }

    /**
     * 查询指定返回对象类型列表(不能防止SQL注入)
     * @param sql    sql语句
     * @param clazz  返回List包含对象class
     */
    public <T> List<T> queryList(String sql, Class<T> clazz){
        return jdbcTemplate.queryForList(sql, clazz);
    }

}
```
