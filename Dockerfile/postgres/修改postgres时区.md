# 修改postgres时区

## 更新系统时间

```bash
yum install ntpdate
ntpdate cn.pool.ntp.org
```

## 查看当前使用的时区

```bash
show timezone;

UTC
#格林威治时间
```

## 查看所有可供选择的时区

```sql
select * from pg_timezone_names;
```

## 修改配置文件

```conf
vi /var/lib/pgsql/11/data/postgresql.conf

timezone = 'Asia/Shanghai'
log_timezone = 'Asia/Shanghai'
```
