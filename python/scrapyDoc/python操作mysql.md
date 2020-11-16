# python 操作 mysql

- [https://dev.mysql.com/downloads/](https://dev.mysql.com/downloads/)
- [https://github.com/mysql/mysql-connector-python](https://github.com/mysql/mysql-connector-python)
- [https://github.com/PyMySQL/PyMySQL](https://github.com/PyMySQL/PyMySQL)
- [https://github.com/sqlalchemy/sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)

- `mysql-connector-python`是 MySQL 官方的`纯Python驱动`
- `PyMySQL`是一个`纯Python`实现的 MySQL 客户端库，支持兼容 `Python3`，用于代替`MySQLdb`
- `sqlalchemy`python最有名的ORM框架

```bash
# mysql-connector-python
pip3 install mysql-connector-python -i https://mirrors.aliyun.com/pypi/simple/
# PyMySQL
pip3 install PyMySQL -i https://mirrors.aliyun.com/pypi/simple/
# sqlalchemy
pip install sqlalchemy -i https://mirrors.aliyun.com/pypi/simple/
```

## 创建示例表

```sql
CREATE TABLE `book` (
 `id` BIGINT NOT NULL AUTO_INCREMENT,
 `book_name` VARCHAR(32) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
 `price` DECIMAL(10,2) NULL DEFAULT '0.00',
 `create_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
 `update_at` DATETIME NULL,
 PRIMARY KEY (`id`) USING BTREE
)
```

## [mysql基本操作](./mysqlBase.py)

## [mysql Orm](./mysqlOrm.py)
