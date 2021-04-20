# mysql orderby和limit索引问题

```sql
create table book
(
    id           int auto_increment
        primary key,
    book_name    varchar(32)                              not null,
    book_price   decimal(10, 2) default 0.00              null,
    book_type    int            default 0                 null,
    created_time datetime       default CURRENT_TIMESTAMP null comment '创建时间'
);

create index idx_bookTypeCreatedTime
    on book (book_type, created_time);

create index idx_createdTime
    on book (created_time);
```

测试数据在一千万数据左右

```sql
mysql> explain select * from book where book_type = 2 and created_time >= '2021-03-01' order by created_time desc \G;
*************************** 1. row ***************************
           id: 1
  select_type: SIMPLE
        table: book
   partitions: NULL
         type: range
possible_keys: idx_createdTime,idx_bookTypeCreatedTime
          key: idx_bookTypeCreatedTime
      key_len: 11
          ref: NULL
         rows: 130000
     filtered: 100.00
        Extra: Using index condition; Using filesort
1 row in set, 1 warning (0.00 sec)
```

当前返回 [3000] 行，耗时 [651ms.] 

## 加了 limit 后

```sql
mysql> explain
    -> select * from book
    -> where book_type = 2 and created_time >= '2021-03-01'
    -> order by created_time desc limit 0,10 \G;
*************************** 1. row ***************************
           id: 1
  select_type: SIMPLE
        table: book
   partitions: NULL
         type: range
possible_keys: idx_createdTime,idx_bookTypeCreatedTime
          key: idx_createdTime
      key_len: 11
          ref: NULL
         rows: 4900000
     filtered: 100.00
        Extra: Using index condition; Using where; Backward index scan
1 row in set, 1 warning (0.00 sec)
```

这个时候走的索引是`idx_createdTime`而不是`idx_bookTypeCreatedTime`

执行成功，当前返回 [10] 行，耗时 [116ms.] 

## limit后改为conut(*)计算总数

```sql
mysql> explain
    -> select count(*) from book
    -> where book_type = 2 and created_time >= '2021-03-01'
    -> order by created_time desc limit 0,10 \G;
*************************** 1. row ***************************
           id: 1
  select_type: SIMPLE
        table: book
   partitions: NULL
         type: range
possible_keys: idx_createdTime,idx_bookTypeCreatedTime
          key: idx_bookTypeCreatedTime
      key_len: 11
          ref: NULL
         rows: 14564
     filtered: 100.00
        Extra: Using where; Using index for skip scan
1 row in set, 1 warning (0.01 sec)
```

当前返回 [1] 行，耗时 [87ms.] 
