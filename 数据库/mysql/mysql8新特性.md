# mysql8新特性

```sql
mysql> select version();
+-----------+
| version() |
+-----------+
| 8.0.22    |
+-----------+
1 row in set (0.01 sec)
```

## 默认字符集由`latin1`变为`utf8mb4`

## 默认引擎为`InnoDB`

```sql
mysql> select distinct(ENGINE) from information_schema.tables;
+--------------------+
| ENGINE             |
+--------------------+
| InnoDB             |
| NULL               |
| CSV                |
| PERFORMANCE_SCHEMA |
+--------------------+
4 rows in set (0.01 sec)
```

## `group by` 不再隐式排序

```sql
mysql> select * from book;
+----+--------------+------------+-----------+
| id | book_name    | book_price | book_type |
+----+--------------+------------+-----------+
|  1 | 算法之美     |      43.00 |         2 |
|  2 | 刻意练习     |      23.00 |         0 |
|  3 | 爱的艺术     |      26.00 |         1 |
|  4 | 断舍离       |      33.00 |         1 |
+----+--------------+------------+-----------+
4 rows in set (0.00 sec)
mysql> select book_type,sum(book_price) from book group by book_type;
+-----------+-----------------+
| book_type | sum(book_price) |
+-----------+-----------------+
|         2 |           43.00 |
|         0 |           23.00 |
|         1 |           59.00 |
+-----------+-----------------+
3 rows in set (0.00 sec)
mysql> explain select book_type,sum(book_price) from book group by book_type;
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-----------------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra           |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-----------------+
|  1 | SIMPLE      | book  | NULL       | ALL  | NULL          | NULL | NULL    | NULL |    4 |   100.00 | Using temporary |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+-----------------+
1 row in set, 1 warning (0.00 sec)
```

## innodb select for update跳过锁等待

`select ... for update`，`select ... for share`(8.0新增语法) 添加 `NOWAIT`、`SKIP LOCKED`语法，跳过锁等待，或者跳过锁定。

在5.7及之前的版本，`select...for update`，如果获取不到锁，会一直等待，直到`innodb_lock_wait_timeout`超时。

在8.0版本，通过添加`nowait`，`skip locked`语法，能够立即返回。如果查询的行已经加锁，那么`nowait`会立即报错返回，而`skip locked`也会立即返回，只是返回的结果中不包含被锁定的行。

```sql
-- 事务1
mysql> begin;
Query OK, 0 rows affected (0.00 sec)

mysql> select * from book where id = 1 for update;
+----+--------------+------------+
| id | book_name    | book_price |
+----+--------------+------------+
|  1 | 算法之美     |      41.00 |
+----+--------------+------------+
1 row in set (0.00 sec)

-- 事务2
mysql> select * from book where id = 1 for update nowait;
ERROR 3572 (HY000): Statement aborted because lock(s) could not be acquired immediately and NOWAIT is set.
mysql> select * from book where id = 1 for update skip locked;
Empty set (0.00 sec)
```

## `for update`和`for share`区别

- `for update`语句，相当于一个 update 语句。对行数据进行排他锁（`X锁`），一旦一个事务获取了这个锁，其他的事务是没法在这些数据上执行`for update`
- `for share`语句是一个给查找的数据上一个共享锁（`S锁`）的功能，它允许其他的事务也对该数据上 `S锁`，但是不能够允许对该数据进行修改。如果不及时的commit 或者rollback 也可能会造成大量的事务等待。

```sql
-- 事务1-1
mysql> begin;
Query OK, 0 rows affected (0.01 sec)
-- 事务1-2
mysql> select * from book where id = 1 for share;
+----+--------------+------------+
| id | book_name    | book_price |
+----+--------------+------------+
|  1 | 算法之美     |      42.00 |
+----+--------------+------------+
1 row in set (0.01 sec)
-- 事务2-1,可以查询出数据
mysql> select * from book where id = 1 for share;
+----+--------------+------------+
| id | book_name    | book_price |
+----+--------------+------------+
|  1 | 算法之美     |      42.00 |
+----+--------------+------------+
1 row in set (0.00 sec)
-- 事务1-3,对数据进行修改
mysql> update book set book_price = 43 where id = 1;
Query OK, 1 row affected (0.01 sec)
Rows matched: 1  Changed: 1  Warnings: 0
-- 事务2-2,由于共享锁的数据发生修改未提交，这个时候查询会阻塞
mysql> select * from book where id = 1 for share;
+----+--------------+------------+
| id | book_name    | book_price |
+----+--------------+------------+
|  1 | 算法之美     |      43.00 |
+----+--------------+------------+
1 row in set (30.08 sec)
-- 事务1-4,提交事务
mysql> commit;
Query OK, 0 rows affected (0.00 sec)
-- 事务2-3,之前阻塞的查询，现在返回数据
mysql> select * from book where id = 1 for share;
+----+--------------+------------+
| id | book_name    | book_price |
+----+--------------+------------+
|  1 | 算法之美     |      43.00 |
+----+--------------+------------+
1 row in set (30.08 sec)
```
