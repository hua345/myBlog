MongoDB默认是不需要用户密码连接操作,不过为了安全最好添加认证

首先以非认证方式启动mongod

```nash
./bin/mongod --dbpath data --logpath log/mongod.conf  --fork
```

### 创建数据库角色

```bash
use admin
help  　　　　　　#查看帮助
show roles    　＃查看所有创建的角色
＃内建普通角色read，readWrite，dbAdmin，dbOwner，userAdmin，dbAdminAnyDatabase，clusterAdmin等．
#dbOwner有readWrite, dbAdmin and userAdmin权限.
＃超级角色root有readWriteAnyDatabase, dbAdminAnyDatabase, userAdminAnyDatabase and clusterAdmin权限
#查看角色权限
db.getRole( "readWrite", { showPrivileges: true } )
＃创建角色
db.createRole(
   {
     role: "mongostatRole",
     privileges: [
       { resource: { cluster: true }, actions: [ "serverStatus" ] }
     ],
     roles: []
   }
)
```

### 创建数据库管理员用户

```bash
use admin
db.createUser(
  {
    user: "root",
    pwd: "password",
    roles: [ { role: "root", db: "admin" } ]
  }
)

use test
db.createUser(
  {
    user: "testOwner",
    pwd: "password",
    roles: [ { role: "dbOwner", db: "test" } ]
  }
)
show users   #查看所有用户
db.getUser("root")
#更改密码
db.updateUser(
   "root",
   {
      pwd: "123456"
   }
)
```

启动时开启认证--auth

```bash
./bin/mongod --dbpath data --shutdown
./bin/mongod --dbpath data --logpath log/mongod.conf  --fork --auth
```

```bash
use admin
db.auth("root","123456")
1
db.auth("root","error＂)
Error: 18 Authentication failed.
0
```

[command](https://docs.mongodb.org/manual/reference/command/#role-management-commands)
[built-in-roles](https://docs.mongodb.org/manual/reference/built-in-roles/#read)
[Privilege Actions](https://docs.mongodb.org/manual/reference/privilege-actions/#authr.createUser)
[create-user-defined-role](https://docs.mongodb.org/manual/tutorial/manage-users-and-roles/#create-user-defined-role)
[change-own-password-and-custom-data](https://docs.mongodb.org/manual/tutorial/change-own-password-and-custom-data/)
[add-user-administrator](https://docs.mongodb.org/manual/tutorial/add-user-administrator/)
