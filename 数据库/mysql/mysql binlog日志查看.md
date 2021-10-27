[TOC]

## 参考

- [MySQL 基础技术（二） —— MySQL 是如何更新的](https://www.jianshu.com/p/4006d6ed60d6)
- [MySQL 基础技术（三）—— MySQL 如何保证数据不丢失](https://juejin.cn/post/7019969643657822216#heading-5)
- [带你了解 MySQL Binlog 不为人知的秘密 ](https://www.cnblogs.com/rickiyang/p/13841811.html)
- [mysql查看binlog日志](https://www.cnblogs.com/softidea/p/12624778.html)

## mysql日志路径

```sql
# 显示mysql日志变量
show variables like 'log_%'
# 查看所有binlog日志列表
show master logs
show binary logs
# 查看binlog
show binlog events
show binlog events in 'binlog.000009';
# 也可以用mysqlbinlog查看日志
# 先将C:\Program Files\MySQL\MySQL Server 8.0\bin加入环境变量
mysqlbinlog.exe binlog.000008
# 配置 `binlog-format` 为 `ROW` 模式
show variables like 'binlog_format%';
+-------------+-----+
|Variable_name|Value|
+-------------+-----+
|binlog_format|ROW  |
+-------------+-----+
```

| Variable\_name                              | Value                                                        |
| :------------------------------------------ | :----------------------------------------------------------- |
| log\_bin                                    | ON                                                           |
| log\_bin\_basename                          | C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Data\\xxx-bin      |
| log\_bin\_index                             | C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Data\\xxx-bin.index |
| log\_statements\_unsafe\_for\_binlog        | ON                                                           |
| log\_throttle\_queries\_not\_using\_indexes | 0                                                            |
| log\_timestamps                             | UTC                                                          |

## 查看事务日志

### 新增一条事务数据

```sql
# 显示当前binlog日志文件
show master status;
+-------------------------+--------+
|File                     |Position|
+-------------------------+--------+
|binlog.000009|1597    |
+-------------------------+--------+
show binlog events in 'binlog.000009';
+---+--------------+---------+-----------+------------------------------------------------+
|Pos|Event_type    |Server_id|End_log_pos|Info                                            |
+---+--------------+---------+-----------+------------------------------------------------+
|4  |Format_desc   |1        |125        |Server ver: 8.0.26, Binlog ver: 4               |
|125|Previous_gtids|1        |156        |                                                |
|156|Anonymous_Gtid|1        |235        |SET @@SESSION.GTID_NEXT= 'ANONYMOUS'            |
|235|Query         |1        |325        |BEGIN                                           |
|325|Table_map     |1        |399        |table_id: 83 (db_example.book)                  |
|399|Update_rows   |1        |560        |table_id: 83 flags: STMT_END_F                  |
|560|Query         |1        |684        |SAVEPOINT `0d12b796_cded_4631_a47a_1d204e97417a`|
|684|Xid           |1        |715        |COMMIT /* xid=255 */                            |
+---+--------------+---------+-----------+------------------------------------------------+
```

### 新增`test_log`表和一条数据

```sql
show binlog events in 'binlog.000009';
```



| Pos  | Event\_type     | Server\_id | End\_log\_pos | Info                                                         |
| :--- | :-------------- | :--------- | :------------ | :----------------------------------------------------------- |
| 684  | Xid             | 1          | 715           | COMMIT /\* xid=255 \*/                                       |
| 715  | Anonymous\_Gtid | 1          | 794           | SET @@SESSION.GTID\_NEXT= 'ANONYMOUS'                        |
| 794  | Query           | 1          | 1068          | use \`db\_example\`; /\* ApplicationName=DataGrip 2021.2 \*/ create table test\_log<br/>\(<br/>id bigint auto\_increment,<br/>name varchar\(32\) null comment '名称',<br/>constraint test\_log\_pk<br/>primary key \(id\)<br/>\) /\* xid=512 \*/ |
| 1068 | Anonymous\_Gtid | 1          | 1147          | SET @@SESSION.GTID\_NEXT= 'ANONYMOUS'                        |
| 1147 | Query           | 1          | 1228          | BEGIN                                                        |
| 1228 | Table\_map      | 1          | 1296          | table\_id: 107 \(db\_example.test\_log\)                     |
| 1296 | Write\_rows     | 1          | 1344          | table\_id: 107 flags: STMT\_END\_F                           |
| 1344 | Xid             | 1          | 1375          | COMMIT /\* xid=679 \*/                                       |

### 删除`test_log`表, 使用`binlog`恢复数据

```sql
mysqlbinlog.exe --help
Dumps a MySQL binary log in a format usable for viewing or for piping to
the mysql command line client.

-d, --database=name List entries for just this database (local log only).
-j, --start-position=#
                      Start reading the binlog at position N. Applies to the
                      first binlog passed on the command line.
-v, --verbose       Reconstruct pseudo-SQL statements out of row events. -v
                      -v adds comments on column data types.
                      -v -v添加字段数据类型注释
--stop-position=#   Stop reading the binlog at position N. Applies to the
                      last binlog passed on the command line.
--start-datetime=name
                      Start reading the binlog at first event having a datetime
                      equal or posterior to the argument; the argument must be
                      a date and time in the local time zone, in any format
                      accepted by the MySQL server for DATETIME and TIMESTAMP
                      types, for example: 2004-12-25 11:25:56
--stop-datetime=name
                      Stop reading the binlog at first event having a datetime
                      equal or posterior to the argument; the argument must be
                      a date and time in the local time zone, in any format
                      accepted by the MySQL server for DATETIME and TIMESTAMP
                      types, for example: 2004-12-25 11:25:56
mysqlbinlog.exe -v -v --base64-output=decode-rows --start-position=715 --stop-position=1375 CHENJH91-VSZBN-bin.000009 > testlog.sql
```

```sql
# The proper term is pseudo_replica_mode, but we use this compatibility alias
# to make the statement usable on server versions 8.0.24 and older.
/*!50530 SET @@SESSION.PSEUDO_SLAVE_MODE=1*/;
/*!50003 SET @OLD_COMPLETION_TYPE=@@COMPLETION_TYPE,COMPLETION_TYPE=0*/;
DELIMITER /*!*/;
# at 156
#211019  9:29:24 server id 1  end_log_pos 125 CRC32 0x853b6916 	Start: binlog v 4, server v 8.0.26 created 211019  9:29:24 at startup
# Warning: this binlog is either in use or was not closed properly.
ROLLBACK/*!*/;
BINLOG '
dB9uYQ8BAAAAeQAAAH0AAAABAAQAOC4wLjI2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAB0H25hEwANAAgAAAAABAAEAAAAYQAEGggAAAAICAgCAAAACgoKKioAEjQA
CigBFmk7hQ==
'/*!*/;
# at 715
#211020 20:15:14 server id 1  end_log_pos 794 CRC32 0xfd0e1f62 	Anonymous_GTID	last_committed=1	sequence_number=2	rbr_only=no	original_committed_timestamp=1634732114049955	immediate_commit_timestamp=1634732114049955	transaction_length=353
# original_commit_timestamp=1634732114049955 (2021-10-20 20:15:14.049955 �й���׼ʱ��)
# immediate_commit_timestamp=1634732114049955 (2021-10-20 20:15:14.049955 �й���׼ʱ��)
/*!80001 SET @@session.original_commit_timestamp=1634732114049955*//*!*/;
/*!80014 SET @@session.original_server_version=80026*//*!*/;
/*!80014 SET @@session.immediate_server_version=80026*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 794
#211020 20:15:14 server id 1  end_log_pos 1068 CRC32 0x2fa33b56 	Query	thread_id=10	exec_time=0	error_code=0	Xid = 512
use `db_example`/*!*/;
SET TIMESTAMP=1634732114/*!*/;
SET @@session.pseudo_thread_id=10/*!*/;
SET @@session.foreign_key_checks=1, @@session.sql_auto_is_null=0, @@session.unique_checks=1, @@session.autocommit=1/*!*/;
SET @@session.sql_mode=1075838976/*!*/;
SET @@session.auto_increment_increment=1, @@session.auto_increment_offset=1/*!*/;
/*!\C utf8mb4 *//*!*/;
SET @@session.character_set_client=255,@@session.collation_connection=255,@@session.collation_server=255/*!*/;
SET @@session.lc_time_names=0/*!*/;
SET @@session.collation_database=DEFAULT/*!*/;
/*!80011 SET @@session.default_collation_for_utf8mb4=255*//*!*/;
/*!80013 SET @@session.sql_require_primary_key=0*//*!*/;
/* ApplicationName=DataGrip 2021.2 */ create table test_log
(
	id bigint auto_increment,
	name varchar(32) null comment '名称',
	constraint test_log_pk
		primary key (id)
)
/*!*/;
# at 1068
#211020 20:15:29 server id 1  end_log_pos 1147 CRC32 0x9677eec7 	Anonymous_GTID	last_committed=2	sequence_number=3	rbr_only=yes	original_committed_timestamp=1634732129431814	immediate_commit_timestamp=1634732129431814	transaction_length=307
/*!50718 SET TRANSACTION ISOLATION LEVEL READ COMMITTED*//*!*/;
# original_commit_timestamp=1634732129431814 (2021-10-20 20:15:29.431814 �й���׼ʱ��)
# immediate_commit_timestamp=1634732129431814 (2021-10-20 20:15:29.431814 �й���׼ʱ��)
/*!80001 SET @@session.original_commit_timestamp=1634732129431814*//*!*/;
/*!80014 SET @@session.original_server_version=80026*//*!*/;
/*!80014 SET @@session.immediate_server_version=80026*//*!*/;
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 1147
#211020 20:15:29 server id 1  end_log_pos 1228 CRC32 0x2f6fdefd 	Query	thread_id=12	exec_time=0	error_code=0
SET TIMESTAMP=1634732129/*!*/;
BEGIN
/*!*/;
# at 1228
#211020 20:15:29 server id 1  end_log_pos 1296 CRC32 0x59607bf7 	Table_map: `db_example`.`test_log` mapped to number 107
# at 1296
#211020 20:15:29 server id 1  end_log_pos 1344 CRC32 0x1b72e129 	Write_rows: table id 107 flags: STMT_END_F

BINLOG '
YQhwYRMBAAAARAAAABAFAAAAAGsAAAAAAAEACmRiX2V4YW1wbGUACHRlc3RfbG9nAAIIDwKAAAIB
AQACA/z/APd7YFk=
YQhwYR4BAAAAMAAAAEAFAAAAAGsAAAAAAAEAAgAC/wABAAAAAAAAAAPoirMp4XIb
'/*!*/;
### INSERT INTO `db_example`.`test_log`
### SET
###   @1=1 /* LONGINT meta=0 nullable=0 is_null=0 */
###   @2='芳' /* VARSTRING(128) meta=128 nullable=1 is_null=0 */
# at 1344
#211020 20:15:29 server id 1  end_log_pos 1375 CRC32 0xa08f236a 	Xid = 679
COMMIT/*!*/;
SET @@SESSION.GTID_NEXT= 'AUTOMATIC' /* added by mysqlbinlog */ /*!*/;
DELIMITER ;
# End of log file
/*!50003 SET COMPLETION_TYPE=@OLD_COMPLETION_TYPE*/;
/*!50530 SET @@SESSION.PSEUDO_SLAVE_MODE=0*/;
```
