# 检查数据库表的编码

```sql
show create table book;

CREATE TABLE `book` (
  `id` bigint(20) NOT NULL,
  `book_name` varchar(32) NOT NULL,
  `price` decimal(10,2) NOT NULL DEFAULT '0.00',
  `book_desc` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `book_id_uindex` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

```sql
alter table book convert to character set utf8;
```
