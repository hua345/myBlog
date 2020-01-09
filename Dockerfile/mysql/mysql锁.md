# 参考

- [MySQL InnoDB锁机制](https://www.cnblogs.com/null-qige/p/8664009.html)
- [JavaGuide MySQL](https://github.com/Snailclimb/JavaGuide/blob/master/docs/database/MySQL.md)

## 锁机制与InnoDB锁算法

MyISAM和InnoDB存储引擎使用的锁：

- `MyISAM`采用表级锁(table-level locking)。
- `InnoDB`支持行级锁(row-level locking)和表级锁,默认为行级锁

表级锁和行级锁对比：

表级锁： MySQL中锁定 粒度最大 的一种锁，对当前操作的整张表加锁，实现简单，资源消耗也比较少，加锁快，不会出现死锁。其锁定粒度最大，触发锁冲突的概率最高，并发度最低，MyISAM和 InnoDB引擎都支持表级锁。
行级锁： MySQL中锁定 粒度最小 的一种锁，只针对当前操作的行进行加锁。 行级锁能大大减少数据库操作的冲突。其加锁粒度最小，并发度高，但加锁的开销也最大，加锁慢，会出现死锁。

### InnoDB存储引擎的锁的算法有三种

- Record lock：单个行记录上的锁
- Gap lock：间隙锁，锁定一个范围，不包括记录本身
- Next-key lock：record+gap 锁定一个范围，包含记录本身

相关知识点：

- innodb对于行的查询使用`next-key lock`
- Next-locking keying为了解决Phantom Problem幻读问题
- 当查询的索引含有唯一属性时，将next-key lock降级为record key
- Gap锁设计的目的是为了阻止多个事务将记录插入到同一范围内，而这会导致幻读问题的产生
- 有两种方式显式关闭gap锁：（除了外键约束和唯一性检查外，其余情况仅使用record lock） A. 将事务隔离级别设置为RC B. 将参数innodb_locks_unsafe_for_binlog设置为1

## InnoDB锁

InnoDB存储引擎在也实现了自己的数据库锁。一般谈到InnoDB锁的时候，首先想到的都是行锁，行锁相比表锁有一些优点，行锁比表锁有更小锁粒度，可以更大的支持并发。但是加锁动作也是需要额外开销的，比如获得锁、检查锁、释放锁等操作都是需要耗费系统资源。如果系统在锁操作上浪费了太多时间，系统的性能就会受到比较大的影响。

InnoDB实现的行锁有**共享锁(S)**和**排它锁(X)**两种

- 共享锁：允许事务去读一行，阻止其他事务对该数据进行修改
- 排它锁：允许事务去读取更新数据，阻止其他事务对数据进行查询或者修改

行锁虽然很赞，但是还有一个问题，如果一个事务对一张表的某条数据进行加锁，这个时候如果有另外一个线程想要用LOCK TABLES进行锁表，这时候数据库要怎么知道哪张表的哪条数据被加了锁，一张张表一条条数据去遍历是不可行的。InnoDB考虑到这种情况，设计出另外一组锁，**意向共享锁(IS)**和**意向排他锁(IX)**。

- **意向共享锁**:当一个事务要给一条数据加S锁的时候，会先对数据所在的表先加上IS锁，成功后才能加上S锁
- **意向排它锁**:当一个事务要给一条数据加X锁的时候，会先对数据所在的表先加上IX锁，成功后才能加上X锁

**意向锁之间兼容，不会阻塞**。但是会跟S锁和X锁冲突，冲突的方式跟读写锁相同。例如当一张表上已经有一个**排它锁(X锁)**，此时如果另外一个线程要对该表加意向锁，不管意向共享锁还是意向排他锁都不会成功。

- `select for update`能为数据添加排他锁，
- `lock in share mode`为数据添加共享锁。

这两种锁，在事务中生效，而当事务提交或者回滚的时候，会自动释放锁。

```sql
-- step 1
MariaDB [db_example]> begin;
Query OK, 0 rows affected (0.00 sec)
-- step 2
MariaDB [db_example]> select * from book for update;
+----+-------------------+-------+-----------+
| id | book_name         | price | book_desc |
+----+-------------------+-------+-----------+
|  1 | 断舍离            | 80.00 |           |
|  2 | mysql技术内幕     | 20.00 | NULL      |
+----+-------------------+-------+-----------+
2 rows in set (0.00 sec)
-- step 4
MariaDB [db_example]> commit;
Query OK, 0 rows affected (0.01 sec)
```

```sql
-- step 3
MariaDB [db_example]> select * from book for update;
ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
-- 阻塞在这里,如果第一个事务已经commit可以查询出数据
MariaDB [db_example]> select * from book for update;
+----+-------------------+-------+-----------+
| id | book_name         | price | book_desc |
+----+-------------------+-------+-----------+
|  1 | 断舍离            | 80.00 |           |
|  2 | mysql技术内幕     | 20.00 | NULL      |
+----+-------------------+-------+-----------+
2 rows in set (13.91 sec)
```

### 隐式加锁

`select for update`和`lock in share mode`这种通过编写在mysql里面的方式对需要保护的数据进行加锁的方式称为是显式加锁。还有一种加锁方式是隐式加锁，除了把事务设置成串行时，会对SELECT到的所有数据加锁外，SELECT不会对数据加锁（依赖于MVCC）。当执行update、delete、insert的时候会对数据进行加排它锁。

### 外键锁

当插入和更新子表的时候，首先需要检查父表中的记录，并对附表加一条`lock in share mode`，而这可能会对两张表的数据检索造成阻塞。所以一般生产数据库上不建议使用外键。

### 索引和锁

InnoDB在给行添加锁的时候，其实是通过索引来添加锁，如果查询并没有用到索引，就会使用表锁。

```sql
-- step 1
MariaDB [db_example]> begin;
Query OK, 0 rows affected (0.00 sec)
-- step 2
MariaDB [db_example]> select * from book where id=1 for update;
+----+-----------+-------+-----------+
| id | book_name | price | book_desc |
+----+-----------+-------+-----------+
|  1 | 断舍离    | 80.00 |           |
+----+-----------+-------+-----------+
1 row in set (0.00 sec)
-- step 4
MariaDB [db_example]> commit;
Query OK, 0 rows affected (0.01 sec)
```

```sql
-- step 3
MariaDB [db_example]> begin;
Query OK, 0 rows affected (0.00 sec)
-- step 4, 由于id是主键索引,不同的行不会阻塞
MariaDB [db_example]> select * from book where id=2 for update;
+----+-------------------+-------+-----------+
| id | book_name         | price | book_desc |
+----+-------------------+-------+-----------+
|  2 | mysql技术内幕     | 20.00 | NULL      |
+----+-------------------+-------+-----------+
1 row in set (0.00 sec)

```

## 乐观锁和悲观锁

- 悲观锁：指悲观的认为，需要访问的数据随时可能被其他人访问或者修改。因此在访问数据之前，对要访问的数据加锁，不允许其他其他人对数据进行访问或者修改。上述讲到的服务器锁和InnoDB锁都属于悲观锁。

- 乐观锁：指乐观的认为要访问的数据不会被人修改。因此不对数据进行加锁，如果操作的时候发现已经失败了，则重新获取数据进行更新（如CAS），或者直接返回操作失败。

电商卖东西的时候，必须解决的是超卖的问题，超卖是指商品的数量比如只有5件，结果卖出去6件的情况

```java
@Service
public class ProductService implements IProductService {

    @Resource
    private ProductMapper productMapper;

    private static final String product_code = "S001";

    private static final String product_code1 = "S002";

    //乐观锁下单成功数
    private final AtomicInteger optimisticSuccess = new AtomicInteger(0);

    //乐观锁下单失败数
    private final AtomicInteger optimisticFalse = new AtomicInteger(0);

    //悲观锁下单成功数
    private final AtomicInteger pessimisticSuccess = new AtomicInteger(0);

    //悲观锁下单失败数
    private final AtomicInteger pessimisticFalse = new AtomicInteger(0);

    //乐观锁下单
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void orderProductOptimistic() throws TestException {
        int num = productMapper.queryProductNumByCode(product_code);
        if (num <= 0) {
            optimisticFalse.incrementAndGet();
            return;
        }
        int result = productMapper.updateOrderQuantityOptimistic(product_code);
        if (result == 0) {
            optimisticFalse.incrementAndGet();
            throw new TestException("商品已经卖完");
        }
        optimisticSuccess.incrementAndGet();
    }

    //获取售卖记录
    @Override
    public String getStatistics() {
        return "optimisticSuccess:" + optimisticSuccess + ", optimisticFalse:" + optimisticFalse + ",pessimisticSuccess:" + pessimisticSuccess + ", pessimisticFalse:" + pessimisticFalse;
    }

    //悲观锁下单
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void orderProductPessimistic() {
        int num = productMapper.queryProductNumByCodeForUpdate(product_code1);
        if (num <= 0) {
            pessimisticFalse.incrementAndGet();
            return;
        }
        productMapper.updateOrderQuantityPessimistic(product_code1);
        pessimisticSuccess.incrementAndGet();
    }

    //获取产品详情
    @Override
    @Transactional
    public ProductResutl getProductDetail() {
        Random random = new Random();
        String code = random.nextInt() % 2 == 0 ? product_code : product_code1;
        ProductResutl productResutl = productMapper.selectProductDetail(code);
        return productResutl;
    }

    //清楚记录
    @Override
    public void clearStatistics() {
        optimisticSuccess.set(0);
        optimisticFalse.set(0);
        pessimisticSuccess.set(0);
        pessimisticFalse.set(0);
    }
}
```

对应sql如下

```xml
<update id="updateOrderQuantityPessimistic">
        update test_product set quantity=quantity-1 where code=#{productCode}
    </update>

    <update id="updateOrderQuantityOptimistic">
        update test_product set quantity=quantity-1 where code=#{productCode} and  quantity>0;
    </update>

    <select id="queryProductNumByCode" resultType="java.lang.Integer">
        SELECT quantity From test_product WHERE code=#{productCode}
    </select>


    <select id="queryProductNumByCodeForUpdate" resultType="java.lang.Integer">
        SELECT quantity From test_product WHERE code=#{productCode} for update
    </select>

    <select id="selectProductDetail" resultType="com.chinaredstar.jc.crawler.biz.result.product.ProductResutl">
        SELECT
              id as id,
              code as code,
              name as name,
              price as price,
              quantity as quantity
        FROM test_product WHERE code=#{productCode}
    </select>
```
