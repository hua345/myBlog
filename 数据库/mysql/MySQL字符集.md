# mysql 字符集

## `utf8mb4` 和 `utf8` 比较

- `utf8mb4`: A UTF-8 encoding of the Unicode character set using one to four bytes per character.
- `utf8mb3`: A UTF-8 encoding of the Unicode character set using one to three bytes per character.
- `utf8`: An alias for `utfmb3`

`mb4`即 `most bytes 4`

MySQL 的 utf8 是 utfmb3，不能保存`Emoji`表情和一些不常用的汉字,MySQL8 已经默认`utf8mb4`了

## 1.查看 mysql 字符集方法

### 1.1 查看 mysql 服务器支持的字符集

```sql
show character set;
```

| Charset | Description   | `Default collation` | Maxlen |
| ------- | ------------- | ------------------- | ------ |
| utf8mb4 | UTF-8 Unicode | utf8mb4_0900_ai_ci  | 4      |

### 1.2 查看字符集的校对规则

```sql
show collation;
```

| Collation          | Charset | Id  | `Default` | Compiled | Sortlen | Pad_attribute |
| ------------------ | ------- | --- | --------- | -------- | ------- | ------------- |
| utf8mb4_0900_ai_ci | utf8mb4 | 255 | Yes       | Yes      | 0       | NO PAD        |
| utf8mb4_0900_as_ci | utf8mb4 | 305 |           | Yes      | 0       | NO PAD        |
| utf8mb4_0900_as_cs | utf8mb4 | 278 |           | Yes      | 0       | NO PAD        |
| utf8mb4_bin        | utf8mb4 | 46  |           | Yes      | 1       | PAD SPACE     |
| utf8mb4_unicode_ci | utf8mb4 | 224 |           | Yes      | 8       | PAD SPACE     |

- `MySQL 8.0`默认的是 `utf8mb4_0900_ai_ci`，属于 `utf8mb4_unicode_ci` 中的一种
- `uft8mb4` 表示用 UTF-8 编码方案，每个字符最多占 4 个字节。
- `0900` 指的是 Unicode 校对算法版本。（Unicode 归类算法是用于比较符合 Unicode 标准要求的两个 Unicode 字符串的方法）。
- `ai` 指的是口音不敏感。也就是说，排序时 `e，è，é，ê 和 ë` 之间没有区别。
- `ci` 表示不区分大小写的排序方式
- `cs` 表示区分大小写的排序方式
- `_bin`：将字符串每个字符用二进制数据编译存储，区分大小写，而且可以存二进制的内容。

### 1.3 查看当前数据库的字符集

```sql
show variables like 'character%';
```

| Variable_name            | Value                          | 说明                                                        |
| ------------------------ | ------------------------------ | ----------------------------------------------------------- |
| character_set_client     | utf8mb4                        | 客户端请求数据的字符集                                      |
| character_set_connection | utf8mb4                        | 服务器连接的字符集                                          |
| character_set_database   | utf8mb4                        | 默认数据库的字符集                                          |
| character_set_filesystem | binary                         | 把 os 上文件名转化成此字符集， 默认 binary 是不做任何转换的 |
| character_set_results    | utf8mb4                        | 结果集，返回给客户端的字符集                                |
| character_set_server     | utf8mb4                        | 数据库服务器的默认字符集                                    |
| character_set_system     | utf8                           | 系统字符集，这个值总是 utf8，不需要设置                     |
| character_sets_dir       | /usr/share/mysql-8.0/charsets/ |

### 1.4 查看当前数据库的校对规则

```sql
show variables like 'collation%';
```

| Variable_name        | Value              |
| -------------------- | ------------------ |
| collation_connection | utf8mb4_0900_ai_ci |
| collation_database   | utf8mb4_bin        |
| collation_server     | utf8mb4_0900_ai_ci |

## 表字符集需要保存一致

```sql
-- 查询表字符集
show table status from `库名` like  `表名`;
-- 查询列字符集
show full columns from `表名`;
-- 查询字符集有哪些表
select TABLE_SCHEMA,TABLE_NAME,TABLE_COLLATION from information_schema.tables where table_collation = 'utf8mb4_0900_ai_ci';
-- 修改表字符集
ALTER TABLE `表名` DEFAULT CHARACTER SET utf8mb4 COLLATE 'utf8mb4_0900_ai_ci';
-- 修改字段字符集
ALTER TABLE  `表名` CHANGE  product_id  product_id varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL;
-- 将一个表所有字段修改为指定字符集
alter table `表名` convert to character set utf8mb4 COLLATE utf8mb4_bin;
-- 查询列字符集
show full columns from `表名`;
```

排序字符集 `collation`, 字符除了需要存储，还需要排序或比较大小。
