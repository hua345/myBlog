# CentOS安装mysql

## 去官网查看最新安装包

[https://dev.mysql.com/downloads/](https://dev.mysql.com/downloads/)

[https://dev.mysql.com/downloads/repo/yum/](https://dev.mysql.com/downloads/repo/yum/)

## 下载MySQL源安装包

```bash
# wget http://mirrors.ustc.edu.cn/mysql-repo/mysql80-community-release-el7-3.noarch.rpm
wget https://repo.mysql.com//mysql80-community-release-el8-1.noarch.rpm
# 安装rpm包
rpm -ivh mysql80-community-release-el8-1.noarch.rpm

# 清除所有的缓存文件
yum clean all
# 制作元数据缓存
yum makecache

# centos8
dnf clean all
dnf makecache
```

## 安装MySQL服务器

```bash
#centos8
dnf install @mysql
#centos7
yum install mysql-community-server

# 启动时自动启动：
systemctl enable --now mysqld

# 查看mysql状态
➜  ~ systemctl status mysqld
● mysqld.service - MySQL 8.0 database server
   Loaded: loaded (/usr/lib/systemd/system/mysqld.service; enabled; vendor pres>
   Active: active (running) since Mon 2019-11-04 18:43:43 HKT; 28min ago
  Process: 2732 ExecStartPost=/usr/libexec/mysql-check-upgrade (code=exited, st>
  Process: 962 ExecStartPre=/usr/libexec/mysql-prepare-db-dir mysqld.service (c>
  Process: 911 ExecStartPre=/usr/libexec/mysql-check-socket (code=exited, statu>
 Main PID: 1022 (mysqld)
   Status: "Server is operational"
    Tasks: 38 (limit: 11373)
   Memory: 448.1M
   CGroup: /system.slice/mysqld.service
           └─1022 /usr/libexec/mysqld --basedir=/usr

11月 04 18:43:38 db.learn systemd[1]: Starting MySQL 8.0 database server...
11月 04 18:43:43 db.learn systemd[1]: Started MySQL 8.0 database server.
```

## 设置用户密码

```bash
mysql_secure_installation

# 连接数据库
➜  ~ mysql -u root -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 10
Server version: 8.0.17 Source distribution

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

## centos7设置用户密码

```bash
# 查看mysql密码
grep 'temporary password' /var/log/mysqld.log

# 连接mysql
mysql -u root -p
# 修改密码
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass4!';
Query OK, 0 rows affected (0.01 sec)
# 查看验证密码规则
mysql> show variables like 'validate_password%';
#允许root远程登录
mysql> CREATE USER 'root'@'%' IDENTIFIED BY 'password';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'WITH GRANT OPTION;
mysql> FLUSH PRIVILEGES;
# 设置防火墙
[root@loveFang ~]# firewall-cmd --zone=public --add-port=3306/tcp --permanent
success
[root@loveFang ~]# firewall-cmd --reload
success
# 添加远程登录用户
mysql> GRANT ALL PRIVILEGES ON *.* TO 'testUsre'@'%' IDENTIFIED BY 'testPassword' WITH GRANT OPTION;

# 查看Mysql用户
mysql> select user,host from mysql.user;
+------------------+-----------+
| user             | host      |
+------------------+-----------+
| root             | %         |
| springuser       | %         |
| root             | gateway   |
| mysql.infoschema | localhost |
| mysql.session    | localhost |
| mysql.sys        | localhost |
| root             | localhost |
+------------------+-----------+
7 rows in set (0.00 sec)
```
