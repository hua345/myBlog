# apollo 部署

- [apollo-build-scripts](https://github.com/apolloconfig/apollo-build-scripts)

```bash
git clone https://github.com/apolloconfig/apollo-build-scripts.git
```

## 创建数据库

Apollo 服务端共需要两个数据库：ApolloPortalDB 和 ApolloConfigDB，我们把数据库、表的创建和样例数据都分别准备了 sql 文件，只需要导入数据库即可。

### 创建 ApolloPortalDB

通过各种 MySQL 客户端导入`sql/apolloportaldb.sql`即可。

下面以 MySQL 原生客户端为例：

`source /your_local_path/sql/apolloportaldb.sql`

导入成功后，可以通过执行以下 sql 语句来验证：

```sql
select `Id`, `AppId`, `Name` from ApolloPortalDB.App;
```

| Id  | AppId     | Name       |
| --- | --------- | ---------- |
| 1   | SampleApp | Sample App |

### 创建 ApolloConfigDB

通过各种 MySQL 客户端导入`sql/apolloconfigdb.sql`即可。

下面以 MySQL 原生客户端为例：

```sql
source /your_local_path/sql/apolloconfigdb.sql
```

导入成功后，可以通过执行以下 sql 语句来验证：

```sql
select `NamespaceId`, `Key`, `Value`, `Comment` from ApolloConfigDB.Item;
```

| NamespaceId | Key     | Value | Comment |
| ----------- | ------- | ----- | ------- | ------------ |
| 1           | timeout | 100   | sample  | timeout 配置 |
