
# [https://www.postgresql.org/](https://www.postgresql.org/)

```bash
# Install the repository RPM
yum install https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm

# Install the client packages

yum install postgresql11

# install the server packages

yum install postgresql11-server

# initialize the database and enable automatic start

/usr/pgsql-11/bin/postgresql-11-setup initdb
systemctl enable postgresql-11
systemctl start postgresql-11
```

## 登录postgresql并设置密码

postgresql在安装时默认添加用户postgres

```bash
#切换到postgres用户
su postgres
#登录postgres数据库
psql postgres
#修改postgres用户登录密码
ALTER USER postgres with PASSWORD 'password';
#输入密码
postgres=#
#输入第二遍密码
postgres=# \q
```

## 创建用户

```bash
#创建数据库用户dbuser,并设置密码
CREATE USER dbuser WITH PASSWORD 'password';
#创建用户数据库，这里为exampledb，并指定所有者为dbuser
CREATE DATABASE exampledb OWNER dbuser;
#将exampledb数据库的所有权限都赋予dbuser，否则dbuser只能登录控制台，没有任何数据库操作权限。
GRANT ALL PRIVILEGES ON DATABASE exampledb to dbuser;

# test
CREATE USER fang WITH PASSWORD '123456';
CREATE DATABASE fangdb OWNER fang;
GRANT ALL PRIVILEGES ON DATABASE fangdb to fang;
```

## 登录postgresql

```bash
psql -U postgres -d postgres -h 127.0.0.1 -p 5432
#上面命令的参数含义如下：-U指定用户，-d指定数据库，-h指定服务器，-p指定端口。
psql
#psql命令存在简写形式。如果当前Linux系统用户，同时也是PostgreSQL用户，则可以省略用户名
```

## 控制台命令

```bash
\h  #查看SQL命令的解释，比如\h select。
\?  #查看psql命令列表。
\l  #列出所有数据库。
\c  #[database_name]：连接其他数据库。
\d  #列出当前数据库的所有表格。
\d  #[table_name]：列出某一张表格的结构。
\du #列出所有用户。
\password #设置用户密码
\e  #打开文本编辑器。
\conninfo #列出当前数据库和连接的信息。
\q  #退出
```

## 配置文件

默认情况下postgresql是不用密码不支持远程登录的。我们需要修改配置文件

```bash
ls /var/lib/pgsql/11/data/
pg_hba.conf postgresql.conf

```

```bash
vi /var/lib/pgsql/11/data/postgresql.conf
```

```conf
# - Connection Settings -

listen_addresses = '*'         # what IP address(es) to listen on;
                                        # comma-separated list of addresses;
                                        # defaults to 'localhost'; use '*' for all
                                        # (change requires restart)
#port = 5432                            # (change requires restart)

```

### pg_hba.conf是客户端认证配置文件

```bash
vi /var/lib/pgsql/11/data/pg_hba.conf
```

```bash
# Database administrative login by Unix domain socket
local   all             postgres                                peer

# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     peer
# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
# IPv6 local connections:
host    all             all             ::1/128                 md5

#允许10.1.1.0~10.1.1.255网段登录数据库：
host    all             all             10.1.1.0/24             md5
host    all             all             192.168.137.0/24        md5
#信任192.168.1.10登录数据库：
host    all    all    192.168.1.10/32    trust
```

METHOD指定如何处理客户端的认证。常用的有ident，md5，password，trust，reject等
ident是Linux下PostgreSQL默认的local认证方式，凡是能正确登录服务器的操作系统用户（注：不是数据库用户）就能使用本用户映射的数据库用户不需密码登录数据库。用户映射文件为pg_ident.conf，这个文件记录着与操作系统用户匹配的数据库用户，如果某操作系统用户在本文件中没有映射用户，则默认的映射数据库用户与操作系统用户同名。比如，服务器上有名为user1的操作系统用户，同时数据库上也有同名的数据库用户，user1登录操作系统后可以直接输入psql，以user1数据库用户身份登录数据库且不需密码。很多初学者都会遇到psql -U username登录数据库却出现“username ident 认证失败”的错误，明明数据库用户已经createuser。原因就在于此，使用了ident认证方式，却没有同名的操作系统用户或没有相应的映射用户。解决方案：1、在pg_ident.conf中添加映射用户；2、改变认证方式。

md5是常用的密码认证方式，如果你不使用ident，最好使用md5。密码是以md5形式传送给数据库，较安全，且不需建立同名的操作系统用户。

password是以明文密码传送给数据库，建议不要在生产环境中使用。

trust是只要知道数据库用户名就不需要密码或ident就能登录，建议不要在生产环境中使用。

reject是拒绝认证。

### 参照

- [PostgreSQL新手入门](http://www.ruanyifeng.com/blog/2013/12/getting_started_with_postgresql.html)
- [PostgreSQL pg_hba.conf 文件简析](http://www.cnblogs.com/hiloves/archive/2011/08/20/2147043.html)
