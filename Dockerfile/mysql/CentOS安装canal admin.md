# canal admin

## 初始化元数据库

```sql
cd /usr/local/canal_admin
mysql -u root -p
-- 导入初始化SQL
mysql> source conf/canal_manager.sql

mysql> SELECT * FROM mysql.user WHERE user='canal'\G
*************************** 1. row ***************************
                    Host: %
                    User: canal
             Select_priv: Y
             Insert_priv: N
             Update_priv: N
             Delete_priv: N
             Create_priv: N
               Drop_priv: N
             Reload_priv: N
           Shutdown_priv: N
            Process_priv: N
               File_priv: N
              Grant_priv: N
         References_priv: N
              Index_priv: N
              Alter_priv: N
            Show_db_priv: N
              Super_priv: N
   Create_tmp_table_priv: N
        Lock_tables_priv: N
            Execute_priv: N
         Repl_slave_priv: Y
        Repl_client_priv: Y

CREATE USER canal_manager IDENTIFIED BY 'Aa123456.';
-- MySQL 8.0 使用了新的登录验证方式 caching_sha2_password 代替旧的 mysql_native_password
-- Caused by: java.io.IOException: caching_sha2_password Auth failed
ALTER USER 'canal_manager' IDENTIFIED WITH mysql_native_password BY 'Aa123456.';
GRANT SELECT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'canal'@'%';
FLUSH PRIVILEGES;

GRANT ALL PRIVILEGES ON canal_manager.* TO canal_manager WITH GRANT OPTION;
```

## 配置修改

```bash
cd /usr/local/canal_admin
vi conf/application.yml
```

```yml
server:
  port: 8089
spring:
  jackson:
    date-format: yyyy-MM-dd HH:mm:ss
    time-zone: GMT+8

spring.datasource:
  address: 192.168.137.129:3306
  database: canal_manager
  username: canal
  password: Aa123456.
  driver-class-name: com.mysql.jdbc.Driver
  url: jdbc:mysql://${spring.datasource.address}/${spring.datasource.database}?useUnicode=true&characterEncoding=UTF-8&useSSL=false
  hikari:
    maximum-pool-size: 30
    minimum-idle: 1

canal:
  adminUser: admin
  adminPasswd: admin
```

### 添加`mysql 8.0.21`驱动

```java
Caused by: java.lang.NullPointerException: null
        at com.mysql.jdbc.ConnectionImpl.getServerCharset
```

使用`mysql connector 8`版本，问题即解决。所以应该来说是 mysql 驱动版本的问题

```bash
wget https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.21/mysql-connector-java-8.0.21.jar
```

## 启动

```bash
bin/startup.sh
```

### 开放端口

```bash
firewall-cmd --zone=public --add-port=11110/tcp --permanent
➜  ~ firewall-cmd --zone=public --add-port=8089/tcp --permanent
success
# 重新载入防火墙配置，当前连接不中断
➜  ~ firewall-cmd --reload
success
```

[http://192.168.137.129:8089/](http://192.168.137.129:8089/)

`admin/123456`
