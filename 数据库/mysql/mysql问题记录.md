# MySQL 问题

## Lock wait timeout exceeded; try restarting transaction

```java
Caused by: org.hibernate.PessimisticLockException: could not execute statement
    at org.hibernate.dialect.MySQLDialect$3.convert(MySQLDialect.java:531) ~[hibernate-core-5.3.9.Final.jar!/:5.3.9.Final]
    at org.hibernate.exception.internal.StandardSQLExceptionConverter.convert(StandardSQLExceptionConverter.java:42) ~[hibernate-core-5.3.9.Final.jar!/:5.3.9.Final]

Caused by: com.mysql.cj.jdbc.exceptions.MySQLTransactionRollbackException: Lock wait timeout exceeded; try restarting transaction
    at com.mysql.cj.jdbc.exceptions.SQLError.createSQLException(SQLError.java:123) ~[mysql-connector-java-8.0.15.jar!/:8.0.15]
    at com.mysql.cj.jdbc.exceptions.SQLError.createSQLException(SQLError.java:97) ~[mysql-connector-java-8.0.15.jar!/:8.0.15]
```

### 查询当前处理中进程

```sql
show full processlist;
```

### 查询当前被锁的SQL

我们可以通过到`information_schema` 中来进行查找被锁的语句
我们可以用下面三张表来查原因：

- `innodb_trx` 当前运行的所有事务
- `innodb_locks` 当前出现的锁
- `innodb_lock_waits` 锁等待的对应关系

如果数据库中有锁的话，我们可以使用这条语句来查看：

```sql
select * from information_schema.innodb_trx
```

```sql
desc information_schema.innodb_trx;
```

| Field                      | Type                | NUll |
| -------------------------- | ------------------- | ---- |
| trx_id                     | varchar(18)         | NO   |
| trx_state                  | varchar(13)         | NO   |
| trx_started                | datetime            | NO   |
| trx_requested_lock_id      | varchar(105)        | YES  |
| trx_wait_started           | datetime            | YES  |
| trx_weight                 | bigint(21) unsigned | NO   |
| trx_mysql_thread_id        | bigint(21) unsigned | NO   |
| trx_query                  | varchar(1024)       | YES  |
| trx_operation_state        | varchar(64)         | YES  |
| trx_tables_in_use          | bigint(21) unsigned | NO   |
| trx_tables_locked          | bigint(21) unsigned | NO   |
| trx_lock_structs           | bigint(21) unsigned | NO   |
| trx_lock_memory_bytes      | bigint(21) unsigned | NO   |
| trx_rows_locked            | bigint(21) unsigned | NO   |
| trx_rows_modified          | bigint(21) unsigned | NO   |
| trx_concurrency_tickets    | bigint(21) unsigned | NO   |
| trx_isolation_level        | varchar(16)         | NO   |
| trx_unique_checks          | int(1)              | NO   |
| trx_foreign_key_checks     | int(1)              | NO   |
| trx_last_foreign_key_error | varchar(256)        | YES  |
| trx_adaptive_hash_latched  | int(1)              | NO   |
| trx_adaptive_hash_timeout  | bigint(21) unsigned | NO   |
| trx_is_read_only           | int(1)              | NO   |
| trx_autocommit_non_locking | int(1)              | NO   |

### innodb_locks

```sql
desc information_schema.innodb_locks;
```
