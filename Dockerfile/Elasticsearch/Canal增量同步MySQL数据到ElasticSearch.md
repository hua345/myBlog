# Canal增量同步MySQL数据到ElasticSearch

## 参考

- [Canal——增量同步MySQL数据到ElasticSearch](https://www.cnblogs.com/caoweixiong/p/11825303.html)

## mysql配置

需要先开启MySQL的 `binlog` 写入功能，配置 `binlog-format` 为 `ROW` 模式

命令检查一下`binlog`是否正确启动

```sql
mysql> show variables like 'log_bin%';
+---------------------------------+-----------------------------+
| Variable_name                   | Value                       |
+---------------------------------+-----------------------------+
| log_bin                         | ON                          |
| log_bin_basename                | /var/lib/mysql/binlog       |
| log_bin_index                   | /var/lib/mysql/binlog.index |
| log_bin_trust_function_creators | OFF                         |
| log_bin_use_v1_row_events       | OFF                         |
+---------------------------------+-----------------------------+
5 rows in set (0.00 sec)
mysql> show variables like 'binlog_format%';
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| binlog_format | ROW   |
+---------------+-------+
1 row in set (0.00 sec)
```

授权 `canal` MySQL 账号具有作为`MySQL slave` 的权限, 如果已有账户可直接 grant

```sql
CREATE USER canal IDENTIFIED BY 'Aa123456.';
GRANT SELECT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'canal'@'%';
FLUSH PRIVILEGES;
```
