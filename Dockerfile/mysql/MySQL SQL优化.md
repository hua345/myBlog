# SQL 优化

- 由于 InnoDB,使用 B+树索引,尽量使用自增 Long 类型作为主键
- 防止因字段类型不同造成的隐式转换，导致索引失效
- 创建合适的索引优化查询，但索引数量最好不要超过 5 个
- 查询语句中不要使用 \*

## 1.业务上具有唯一特性的字段，即使是组合字段，也必须建成唯一索引

说明： 不要以为唯一索引影响了 insert 速度，这个速度损耗可以忽略，但提高查找速度是明显的； 另外，
即使在应用层做了非常完善的校验控制，只要没有唯一索引，根据墨菲定律，必然有脏数据产生。

## 2.超过三个表禁止 join

需要 join 的字段，数据类型保持绝对一致； 多表关联查询时，保证被关联的字段需要有索引。

## 3.利用覆盖索引来进行查询操作， 避免回表

说明： 如果一本书需要知道第 11 章是什么标题，会翻开第 11 章对应的那一页吗？目录浏览一下就好，这
个目录就是起到覆盖索引的作用。
正例： 能够建立索引的种类分为主键索引、唯一索引、普通索引三种，而覆盖索引只是一种查询的一种效
果，用 explain 的结果， extra 列会出现： using index。

## 4.建组合索引的时候，区分度最高的在最左边

> 正例： 如果 where a=? and b=?， a 列的几乎接近于唯一值，那么只需要单建 idx_a 索引即可。

说明： 存在非等号和等号混合判断条件时，在建索引时，请把等号条件的列前置。如： where c>? and d=?
那么即使 c 的区分度更高，也必须把 d 放在索引的最前列， 即建立组合索引 idx_d_c。

## 5.合理使用 like 模糊查询

> 【强制】 页面搜索严禁左模糊或者全模糊，如果需要请走搜索引擎来解决。
> 说明： 索引文件具有 B-Tree 的最左前缀匹配特性，如果左边的值未确定，那么无法使用此索引。

可以在页面上对小表进行模糊查询，得到主键 Id 后再精确查询大表

```sql
select id,name from student where name like '%芳%'
select id,name from big_table where student_id = 'xxx'
```

```sql
select id,name from student where name like '%芳%' --会造成全表扫描
select id,name from student where name like '芳%' --不会造成全表扫描
```

## 6.limit 分页优化

> 利用延迟关联或者子查询优化超多分页场景。
> 说明： MySQL 并不是跳过 offset 行，而是取 offset+N 行，然后返回放弃前 offset 行，返回 N 行，那当
> offset 特别大的时候，效率就非常的低下，要么控制返回的总页数，要么对超过特定阈值的页数进行 SQL
> 改写。

正例： 先快速定位需要获取的 id 段，然后再关联：
SELECT a.\* FROM 表 1 a, (select id from 表 1 where 条件 LIMIT 100000,20 ) b where a.id=b.id

```sql
-- 执行成功，当前返回 [10] 行，耗时 [85ms.]
SELECT id,name,create_at FROM big_table ORDER BY create_at LIMIT 1000,10
-- 执行成功，当前返回 [10] 行，耗时 [71788ms.]
SELECT id,name,create_at FROM big_table ORDER BY create_at LIMIT 500000,10
-- 执行成功，当前返回 [10] 行，耗时 [620ms.]
SELECT a.id,a.name,a.create_at FROM big_table a, (select id from big_table ORDER BY create_at LIMIT 500000,10) b where a.id = b.id;

-- create_at已经创建索引的情况下
```

## 7.避免 SQL 中对 where 字段进行函数转换或表达式计算

```sql
explain select * from student WHERE id = 10
select_type:SIMPLE type:ALL rows:43

explain select * from student WHERE id = 10
select_type:SIMPLE type:const rows:1
```

## 参考

- [阿里《Java 开发手册》](https://github.com/alibaba/p3c)
- [Sql 优化总结](https://www.cnblogs.com/joeyJss/p/11096597.html)
