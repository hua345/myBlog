# mysql设置自增

```sql
-- 查询表引擎
select table_name,`engine` from information_schema.tables where table_schema = 'db_example';

-- 设置主键自增
alter table book_2020 modify id bigint auto_increment;

-- 设置自增初始值
alter table book_2020 AUTO_INCREMENT=10000;

-- 查看自增步长
mysql> SHOW VARIABLES LIKE 'auto_inc%' ;
+--------------------------+-------+
| Variable_name            | Value |
+--------------------------+-------+
| auto_increment_increment | 1     |
| auto_increment_offset    | 1     |
+--------------------------+-------+
2 rows in set (0.00 sec)

-- 查看表状态
mysql> show table status like 'book_2020' \G;
*************************** 1. row ***************************
           Name: book_2020
         Engine: InnoDB
        Version: 10
     Row_format: Dynamic
           Rows: 11
 Avg_row_length: 1489
    Data_length: 16384
Max_data_length: 0
   Index_length: 0
      Data_free: 0
 Auto_increment: 10000
    Create_time: 2020-11-26 10:11:14
    Update_time: NULL
     Check_time: NULL
      Collation: utf8mb4_0900_ai_ci
       Checksum: NULL
 Create_options:
        Comment:
1 row in set (0.00 sec)

-- 迁移数据到新表
INSERT INTO book_2020 (old_id, `book_name`, `version`, `creator`, `create_time`, `updator`, `update_time`, `deleted`)
select `id` as old_id,
       `book_name`,
       `version`,
       `creator`,
       `create_time`,
       `updator`,
       `update_time`,
       `deleted`
from book;
-- 重命名表
ALTER TABLE book RENAME book_bak;
ALTER TABLE book_2020 RENAME book;
```
