# 1. explain

查看该 SQL 语句有没有使用上了索引，有没有做全表扫描，这都可以通过`explain`命令来查看

```sql
explain update vm_channel set obtained_status=1 where id in ('28dde0bb-a7de-4058-b574-1d479fd18911')
```

| id  | select_type | table      | partitions | type  | possible_keys | key     | key_len | ref   | rows | filtered | Extra       |
| --- | ----------- | ---------- | ---------- | ----- | ------------- | ------- | ------- | ----- | ---- | -------- | ----------- |
| 1   | UPDATE      | vm_channel | null       | range | PRIMARY       | PRIMARY | 146     | const | 1    | 100      | Using where |

| Key           | 说明                       |
| ------------- | -------------------------- |
| id            | 选择标识符                 |
| select_type   | 表示查询的类型。           |
| table         | 输出结果集的表             |
| partitions    | 匹配的分区                 |
| type          | 表示表的连接类型           |
| possible_keys | 表示查询时，可能使用的索引 |
| key           | 表示实际使用的索引         |
| key_len       | 索引字段的长度             |
| ref           | 列与索引的比较             |
| rows          | 扫描出的行数(估算的行数)   |
| filtered      | 按表条件过滤的行百分比     |
| Extra         | 执行情况的描述和说明       |

## 1.1 `select_type` 常见类型及其含义

- `SIMPLE`：不包含子查询或者 UNION 操作的查询
- `PRIMARY`：查询中如果包含任何子查询，那么最外层的查询则被标记为 PRIMARY
- `SUBQUERY`：子查询中第一个 SELECT
- `DEPENDENT SUBQUERY`：子查询中的第一个 SELECT，取决于外部查询
- `UNION`：UNION 操作的第二个或者之后的查询
- `DEPENDENT UNION`：UNION 操作的第二个或者之后的查询,取决于外部查询
- `UNION RESULT`：UNION 产生的结果集
- `DERIVED`：出现在 FROM 字句中的子查询

## 1.2 `type`

对表访问方式，表示 MySQL 在表中找到所需行的方式，又称“访问类型”。

常用的类型有： `ALL、index、range、 ref、eq_ref、const、system、NULL`（从左到右，性能从差到好）

- `ALL`: Full Table Scan， MySQL 将遍历全表以找到匹配的行
- `index`: Full Index Scan，index 与 ALL 区别为 index 类型只遍历索引树
- `range`:使用索引进行范围扫描，常见于 between、> 、< 这样的查询条件
- `ref`: 表示上述表的连接匹配条件，即哪些列或常量被用于查找索引列上的值
- `eq_ref`: 类似 ref，区别就在使用的索引是唯一索引，对于每个索引键值，表中只有一条记录匹配，简单来说，就是多表连接中使用 primary key 或者 unique key 作为关联条件
- `const、system`: 当 MySQL 对查询某部分进行优化，并转换为一个常量时，使用这些类型访问。如将主键置于 where 列表中，MySQL 就能将该查询转换为一个常量，system 是 const 类型的特例，当查询的表只有一行的情况下，使用 system
- `NULL`: MySQL 在优化过程中分解语句，执行时甚至不用访问表或索引，例如从一个索引列里选取最小值可以通过单独索引查找完成。

`阿里编码规范要求：至少要达到 range 级别，要求是 ref 级别，如果可以是 consts 最好`

## 1.3 Extra列

Extra 列主要用于显示额外的信息，常见信息及其含义如下：

- `Using where` ：MySQL 服务器会在存储引擎检索行后再进行过滤
- `Using index`：使用了覆盖索引进行查询，此时不需要访问表，从索引中就可以获取到所需的全部数据
- `Using index condition`：查找使用了索引，但是需要回表查询数据
- `Using index for skip scan`：在MySQL 8.0也实现了索引跳跃扫描，在优化器选项也可以看到`skip_scan=on`

### `Using filesort`

通常出现在 `GROUP BY` 或 `ORDER BY` 语句中，且排序或分组没有基于索引，此时需要使用文件在内存中进行排序，因为使用索引排序的性能好于使用文件排序，所以出现这种情况可以考虑通过添加索引进行优化

`filesort`可以使用的内存空间大小为参数`sort_buffer_size`的值，默认为2M,当排序记录太多`sort_buffer_size`不够用时，mysql会使用临时文件来存放各个分块，然后各个分块排序后再多次合并分块最终全局完成排序。

```sql
mysql> show global variables like 'sort_buffer_size';
+------------------+--------+
| Variable_name    | Value  |
+------------------+--------+
| sort_buffer_size | 262144 |
+------------------+--------+
1 row in set (0.01 sec)
mysql> show global status like '%sort%';
+-------------------+-------+
| Variable_name     | Value |
+-------------------+-------+
| Sort_merge_passes | 0     |
| Sort_range        | 0     |
| Sort_rows         | 155   |
| Sort_scan         | 33    |
+-------------------+-------+
4 rows in set (0.00 sec)
```

`Sort_merge_passes`表示`filesort`执行过的文件分块合并次数的总和，如果该值比较大，建议增大`sort_buffer_size`的值

### `Using temporary`

表示由于排序没有走索引，因此创建了一个内部临时表。常出现在 `GROUP BY` 或 `ORDER BY` 语句中

```sql
mysql> show global status like '%tmp%';
+-------------------------+-------+
| Variable_name           | Value |
+-------------------------+-------+
| Created_tmp_disk_tables | 0     |
| Created_tmp_files       | 4     |
| Created_tmp_tables      | 59    |
+-------------------------+-------+
3 rows in set (0.00 sec)
```

当mysql需要创建临时表时，选择内存临时表还是硬盘临时表取决于参数`tmp_table_size`和`max_heap_table_size`

用户可以在mysql的配置文件里修改该两个参数的值，两者的默认值均为16M。

```conf
tmp_table_size = 16M
max_heap_table_size = 16M
```

```sql
mysql> show global variables like '%_table_size';
+---------------------+----------+
| Variable_name       | Value    |
+---------------------+----------+
| max_heap_table_size | 16777216 |
| tmp_table_size      | 16777216 |
+---------------------+----------+
2 rows in set (0.00 sec)
```

## 查询优化器

```sql
mysql> select @@optimizer_switch \G;
*************************** 1. row ***************************
@@optimizer_switch: index_merge=on,index_merge_union=on,index_merge_sort_union=on,index_merge_intersection=on,engine_condition_pushdown=on,index_condition_pushdown=on,mrr=on,mrr_cost_based=on,block_nested_loop=on,batched_key_access=off,materialization=on,semijoin=on,loosescan=on,firstmatch=on,duplicateweedout=on,subquery_materialization_cost_based=on,use_index_extensions=on,condition_fanout_filter=on,derived_merge=on,use_invisible_indexes=off,skip_scan=on,hash_join=on,subquery_to_derived=off,prefer_ordering_index=on,hypergraph_optimizer=off,derived_condition_pushdown=on
1 row in set (0.00 sec
```
