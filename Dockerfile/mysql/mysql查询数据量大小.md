# mysql查询数据量大小

## 最常用的

```sql
SELECT COUNT(*) FROM 表名;
```

查的准确，但是数据量大的话（超过100万），比较慢。


## 查询当前库所有表数据量
```sql
SELECT TABLE_NAME,TABLE_ROWS FROM information_schema.`TABLES`
WHERE TABLE_SCHEMA = (SELECT database())
ORDER BY TABLE_ROWS DESC;

SELECT
	TABLE_NAME,
	TABLE_ROWS,
	concat(round((DATA_LENGTH ) / 1024 / 1024,2),'MB') AS DATA_LENGTH,
	concat(round((INDEX_LENGTH ) / 1024 / 1024,2),'MB') AS INDEX_LENGTH
FROM
	information_schema. TABLES
WHERE
	TABLE_SCHEMA = 'dw' -- 数据库名
ORDER BY
	DATA_LENGTH + 0 DESC;
```

TABLE_ROWS 即表数据量，但是会发现和 select count(*) 执行得到的值是不相同的！

原因：
默认情况下 mysql 对表进行增删操作时，是不会自动更新 information_schema 库中 tables 表的 table_rows 字段的，在网上搜索一下发现说：只有10%的行数发生变化才会自动收集
