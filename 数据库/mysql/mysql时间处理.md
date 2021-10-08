# 时间戳转字符串

```sql
select date_format(now(), '%Y-%m-%d %H:%i:%s');
```

## 把字串转换成时间

```sql
SELECT str_to_date('2019-11-06 14:30','%Y-%m-%d %H:%i:%s');
```

## 获取当前时间

```sql
select now();
SELECT CURRENT_TIMESTAMP;
```

```sql
-- 给日期添加时间间隔
date_add
-- 给日期添加时间间隔
date_sub
-- 添加1 day间隔
select date_add(now(), interval 1 day);
select date_add(now(), interval 1 hour);
select date_add(now(), interval 1 minute);
select date_add(now(), interval 1 month);
select date_add(now(), interval 1 year);
select date_add(now(), interval -1 day);
```

## 时间精度

在MySQL5.6版本之前是不支持毫秒和微妙的，自MySQL5.6版本开始支持。
先看下微妙和毫秒的单位：
毫秒：millisecond -- 千分之一秒
微秒：microsecond -- 一百万分之一秒

```sql
mysql> select version();
+-----------+
| version() |
+-----------+
| 8.0.22    |
+-----------+
1 row in set (0.00 sec)
mysql> select now(),now(6);
+---------------------+----------------------------+
| now()               | now(6)                     |
+---------------------+----------------------------+
| 2021-01-04 15:44:16 | 2021-01-04 15:44:16.872281 |
+---------------------+----------------------------+
1 row in set (0.00 sec)

mysql> create table db_example.time_test(my_date date,my_datetime datetime,my_datetime3 datetime(3),my_timestamp timestamp,my_timestamp3 timestamp(3));
Query OK, 0 rows affected (0.02 sec)

mysql> insert into db_example.time_test(my_date, my_datetime, my_datetime3, my_timestamp, my_timestamp3)
    -> values (now(6), now(6), now(6), now(6), now(6));
Query OK, 1 row affected, 1 warning (0.02 sec)

mysql> select * from db_example.time_test;
+------------+---------------------+-------------------------+---------------------+-------------------------+
| my_date    | my_datetime         | my_datetime3            | my_timestamp        | my_timestamp3           |
+------------+---------------------+-------------------------+---------------------+-------------------------+
| 2021-01-04 | 2021-01-04 15:51:20 | 2021-01-04 15:51:19.975 | 2021-01-04 15:51:20 | 2021-01-04 15:51:19.975 |
+------------+---------------------+-------------------------+---------------------+-------------------------+
1 rows in set (0.00 sec)
```
