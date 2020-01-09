```sql
create table `order`
(
    id           bigint                              not null
        primary key,
    product_id   bigint                              not null comment '产品Id',
    custom_id    bigint                              not null comment '消费者Id',
    amount       decimal                             not null comment '消费金额',
    created_date timestamp default CURRENT_TIMESTAMP null comment '订单创建时间'
);
```

```sql
INSERT INTO `order` (id, product_id, custom_id, amount) VALUES (1, 10, 1, 30);
INSERT INTO `order` (id, product_id, custom_id, amount) VALUES (2, 10, 1, 30);
INSERT INTO `order` (id, product_id, custom_id, amount) VALUES (3, 10, 2, 30);
INSERT INTO `order` (id, product_id, custom_id, amount) VALUES (4, 20, 2, 30);
INSERT INTO `order` (id, product_id, custom_id, amount) VALUES (5, 30, 1, 30);
INSERT INTO `order` (id, product_id, custom_id, amount) VALUES (6, 30, 2, 30);
```

## 聚合函数

```sql
COUNT，SUM， AVG
```

### 查询某个用户所有消费金额

```sql
select custom_id, sum(amount) as total from `order` group by custom_id;
```

| custom_id | total |
| --------- | ----- |
| 1         | 90    |
| 2         | 90    |

### 每个产品下面每个用户消费金额

```sql
select product_id, custom_id, sum(amount) as total from `order` group by product_id,custom_id;
```

| product_id | custom_id | total |
| ---------- | --------- | ----- |
| 10         | 1         | 60    |
| 10         | 2         | 30    |
| 20         | 2         | 30    |
| 30         | 1         | 30    |
| 30         | 2         | 30    |

### 查询某个用户十天内订单数

```sql
SELECT NOW(),CURDATE(),CURTIME();
```

| NOW()               | CURDATE()  | CURTIME() |
| ------------------- | ---------- | --------- |
| 2019-09-26 23:01:50 | 2019-09-26 | 23:01:50  |

```sql
SELECT NOW(),CURDATE(),CURDATE()-10;
```

| NOW()               | CURDATE()  | CURDATE()-10 |
| ------------------- | ---------- | ------------ |
| 2019-09-26 23:01:50 | 2019-09-26 | 20190916     |

```sql
select * from `order` where created_date >= CURDATE()-10;
```
