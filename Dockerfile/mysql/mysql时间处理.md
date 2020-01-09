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
