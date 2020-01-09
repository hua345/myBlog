# 时间戳转字符串

```sql
select to_char(now(),'YYYY-MM-DD hh24:mi:ss')；
select to_char(now(),'YYYY-MM-DD');
select to_char(now(),'YYYY-MM-DD hh:mi:ss');
```

## 把字串转换成时间

```sql
select to_date('2019-8-15 9:02', 'YYYY-MM-DD hh24:mi:ss')
select to_timestamp('2019-8-15 9:02', 'YYYY-MM-DD hh24:mi:ss')
```

## 获取当前时间

```sql
SELECT CURRENT_TIMESTAMP;
```
