# MVCC多版本并发控制

`MVCC` 全称是**m**ulti**v**ersion **c**oncurrency **c**ontrol，即多版本并发控制，是 innodb 实现事务并发与回滚的重要功能。
具体的实现是，在数据库的每一行中，添加额外的三个字段：

DB_TRX_ID – 记录插入或更新该行的最后一个事务的事务 ID
DB_ROLL_PTR – 指向改行对应的 undolog 的指针
DB_ROW_ID – 单调递增的行 ID，他就是 AUTO_INCREMENT 的主键 ID


## MVCC的实现

### 3.1 多版本的数据从哪里来——Undo Log

> An undo log is a collection of undo log records associated with a single read-write transaction. An undo log record contains information about how to undo the latest change by a transaction to a clustered index record. If another transaction needs to see the original data as part of a consistent read operation, the unmodified data is retrieved from undo log records.
> undo log是与单个读写事务相关联的撤消日志记录的集合。undo log记录可以明确如何撤消事务对聚集索引记录的最新更改。如果另一个事务需要通过一致性读取操作查看原始数据，可以从undo log记录中查询未修改前的数据。

也就是说，undo log是为了记录如何回滚事务而生成的。数据每进行一次增删改，就会对应一条或多条undo log。 innoDB中使用不同的undo log类型对insert、delete和update进行区分。

#### 3.1.1 插入操作对应的undo log

> TRX_UNDO_INSERT_REC:是插入操作对应的undo log类型，因为插入操作对应的撤销逻辑是删除，所以只需要把这条记录的主键id记录下来。

#### 3.1.2 删除操作对应的undo log

> 由于MVCC的存在，被删除的记录并不会被真正的删除， 而是进行delete mark操作——只是将行记录上的删除标记位delete_flag改为1,后面在通过purge操作把记录加入垃圾链表中，待后续进行空间复用。生成删除语句对应的undo log类型为TRX_UNDO_DELETE_MARK_REC，相比于TRX_UNDO_INSERT_REC，TRX_UNDO_DELETE_MARK_REC不仅保存了主键id，也保存了相关的索引列信息，用来对删除过程中一些中间状态的清理。

#### 3.1.3 更新操作对应的undo log

> 更新操作对应的undo log除了会记录主键和索引列信息之外，还会把被更新前各个字段的信息记录下来，还有指向旧记录的DB_ROLL_PTR和DB_TRX_ID。
>
> - 不更新主键，且被更新的列存储空间不发生变化：直接在原有行记录上面更新。
> - 不更新主键，且被更新的列存储空间发生了变化：先删除旧记录（不是delete mark，而是直接删除），再插入新记录。
> - 更新主键：旧记录进行delete mark，再插入新记录。
> - 过程中更新了二级索引：对旧的二级索引进行delete mark，插入新的二级索引记录。

通过以上3种不同操作对应的undo log，可以得到事务开始前的的历史记录。那么这些记录是如何关联起来的呢？

### 3.2 旧版本如何关联——行记录隐藏字段和版本链

对于InnoDB引擎的表，聚簇索引记录中包含了两个必要的隐藏字段：

> - DB_TRX_ID:一个事务每次对某条聚簇索引记录进行改动（插入、更新或删除）时，会把该事务id赋值给该字段
> - DB_ROLL_PTR：每次对某条聚簇索引记录进行改动时，会把旧版本写入undo日志中，DB_ROLL_PTR就是指向这条记录上一个版本的指针。

# mvcc机制

```
-- auto-generated definition
create table book
(
    id          bigint auto_increment
        primary key,
    book_name   varchar(64) not null comment '书名'
);
```

