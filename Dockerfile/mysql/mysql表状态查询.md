# 1.查看SQL执行计划

```sql
MariaDB [db_example]> explain select * from admin_user where user_id=3741713707034;
+------+-------------+------------+-------+-------------------------+-------------------------+---------+-------+------+-------+
| id   | select_type | table      | type  | possible_keys           | key                     | key_len | ref   | rows | Extra |
+------+-------------+------------+-------+-------------------------+-------------------------+---------+-------+------+-------+
|    1 | SIMPLE      | admin_user | const | sys_user_user_id_uindex | sys_user_user_id_uindex | 9       | const |    1 |       |
+------+-------------+------------+-------+-------------------------+-------------------------+---------+-------+------+-------+
1 row in set (0.00 sec)
```

## 2.查看自增位移

```sql
MariaDB [db_example]> show variables like '%auto_increment%';
+--------------------------+-------+
| Variable_name            | Value |
+--------------------------+-------+
| auto_increment_increment | 1     |
| auto_increment_offset    | 1     |
+--------------------------+-------+
2 rows in set (0.00 sec)
```

修改配置文件，重启`mysqld`

```conf
vi my.cnf
auto-increment-increment = 2
auto-increment-offset = 2
```

### 3.查看表状态

```sql
MariaDB [db_example]> SHOW TABLE STATUS LIKE 'admin_user'\G;
*************************** 1. row ***************************
           Name: admin_user
         Engine: InnoDB
        Version: 10
     Row_format: Compact
           Rows: 4
 Avg_row_length: 4096
    Data_length: 16384
Max_data_length: 0
   Index_length: 16384
      Data_free: 7340032
 Auto_increment: 10008
    Create_time: 2019-06-19 21:02:20
    Update_time: NULL
     Check_time: NULL
      Collation: utf8_general_ci
       Checksum: NULL
 Create_options:
        Comment: 运营后台用户表
1 row in set (0.00 sec)
```

`Auto_increment: 10008`是自增字段的起始值

### 3. 查看支持的数据库索引

```sql
MariaDB [db_example]> SHOW ENGINES;
+--------------------+---------+----------------------------------------------------------------------------+--------------+------+------------+
| Engine             | Support | Comment                                                                    | Transactions | XA   | Savepoints |
+--------------------+---------+----------------------------------------------------------------------------+--------------+------+------------+
| MEMORY             | YES     | Hash based, stored in memory, useful for temporary tables                  | NO           | NO   | NO         |
| MRG_MYISAM         | YES     | Collection of identical MyISAM tables                                      | NO           | NO   | NO         |
| CSV                | YES     | CSV storage engine                                                         | NO           | NO   | NO         |
| BLACKHOLE          | YES     | /dev/null storage engine (anything you write to it disappears)             | NO           | NO   | NO         |
| MyISAM             | YES     | MyISAM storage engine                                                      | NO           | NO   | NO         |
| InnoDB             | DEFAULT | Percona-XtraDB, Supports transactions, row-level locking, and foreign keys | YES          | YES  | YES        |
| ARCHIVE            | YES     | Archive storage engine                                                     | NO           | NO   | NO         |
| FEDERATED          | YES     | FederatedX pluggable storage engine                                        | YES          | NO   | YES        |
| PERFORMANCE_SCHEMA | YES     | Performance Schema                                                         | NO           | NO   | NO         |
| Aria               | YES     | Crash-safe tables with MyISAM heritage                                     | NO           | NO   | NO         |
+--------------------+---------+----------------------------------------------------------------------------+--------------+------+------------+
```
