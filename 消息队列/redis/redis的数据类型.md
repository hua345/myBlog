# redis数据类型

- [Redis 的 8 大数据类型](https://segmentfault.com/a/1190000038462272)
- [http://www.redis.cn/commands.html](http://www.redis.cn/commands.html)

## Redis-key

```bash
127.0.0.1:6379> keys *
(empty list or set)
127.0.0.1:6379> set name fang
OK
127.0.0.1:6379> set age 20
OK
127.0.0.1:6379> keys *
1) "age"
2) "name"
# 判断key 是否存在
127.0.0.1:6379> exists name
(integer) 1
127.0.0.1:6379> exists name1
(integer) 0
# 设置key的过期时间，单位是秒
127.0.0.1:6379> expire name 100
(integer) 1
# 查看当前key的剩余过期时间
127.0.0.1:6379> ttl name
(integer) 96
127.0.0.1:6379> ttl name
(integer) -2
```

## 1.String

```bash
127.0.0.1:6379> set name fang
OK
127.0.0.1:6379> get name
"fang"
127.0.0.1:6379> strlen name
(integer) 4
# 同时设置多个值
127.0.0.1:6379> mset name fang age 20
OK
# 同时获取多个值
127.0.0.1:6379> mget name age
1) "fang"
2) "20"
```

自增、自减

```bash
# 自增 1
127.0.0.1:6379> incr myNum
(integer) 1
127.0.0.1:6379> incr myNum
(integer) 2
127.0.0.1:6379> get myNum
"2"
# 自减 1
127.0.0.1:6379> decr myNum
(integer) 1
# 设置步长、自增 10
127.0.0.1:6379> incrby myNum 10
(integer) 11
# 设置步长、自减 5
127.0.0.1:6379> decrby myNum 5
(integer) 6
```

## 2.List

```bash
127.0.0.1:6379> lpush list 1
(integer) 1
127.0.0.1:6379> lpush list 2
(integer) 2
127.0.0.1:6379> lpush list 3
(integer) 3
# 查看全部元素
127.0.0.1:6379> lrange list 0 -1
1) "3"
2) "2"
3) "1"
# 通过区间获取值
127.0.0.1:6379> lrange list 0 1
1) "3"
2) "2"
127.0.0.1:6379> rpush list right
(integer) 4
127.0.0.1:6379> lrange list 0 -1
1) "3"
2) "2"
3) "1"
4) "right"
# 弹出 pop
127.0.0.1:6379> lpop list
"3"
127.0.0.1:6379> lrange list 0 -1
1) "2"
2) "1"
3) "right"
```

## 3.Set

```bash
# set 集合中添加元素
127.0.0.1:6379> sadd myset "hello"
(integer) 1
127.0.0.1:6379> sadd myset "world"
(integer) 1
# 查看指定Set的所有值
127.0.0.1:6379> smembers myset
1) "hello"
2) "world"
# 判断某一个值是不是在set中
127.0.0.1:6379> sismember myset hello
(integer) 1
# 获取集合中的个数
127.0.0.1:6379> scard myset
(integer) 2
127.0.0.1:6379> sadd myset fang
(integer) 1
127.0.0.1:6379> smembers myset
1) "fang"
2) "hello"
3) "world"
# 移除元素
127.0.0.1:6379> srem myset world
(integer) 1
127.0.0.1:6379> smembers myset
1) "fang"
2) "hello"
```

## 4.Hash

```bash
127.0.0.1:6379> hset user:1 name fang
(integer) 1
127.0.0.1:6379> hmset user:1 name fang age 20
OK
127.0.0.1:6379> hget user:1 name
"fang"
127.0.0.1:6379> hmget user:1 name age
1) "fang"
2) "20"
# 获取全部的数据
127.0.0.1:6379> hgetall user:1
1) "name"
2) "fang"
3) "age"
4) "20"
# 获取字段个数
127.0.0.1:6379> hlen user:1
(integer) 2
# 判断指定key是否存在
127.0.0.1:6379> hexists user:1 name
(integer) 1
# 获取所有的key
127.0.0.1:6379> hkeys user:1
1) "name"
2) "age"
# 获取所有的value
127.0.0.1:6379> hvals user:1
1) "fang"
2) "20"
# 如果不存在则可以设置
127.0.0.1:6379> hsetnx user:1 name fang
(integer) 0
127.0.0.1:6379> hsetnx user:1 nick fangfang
(integer) 1
```

## 5.zset (有序集合)

```bash
127.0.0.1:6379> zadd myzset 1 one
(integer) 1
127.0.0.1:6379> zadd myzset 2 two 3 three
(integer) 2
127.0.0.1:6379> zrange myzset 0 -1
1) "one"
2) "two"
3) "three"
# 按照分数从小到大排序
127.0.0.1:6379> zrangebyscore myzset -inf +inf
1) "one"
2) "two"
3) "three"
# 按照分数从大到小排序
127.0.0.1:6379> zrevrange myzset 0 -1
1) "three"
2) "two"
3) "one"
127.0.0.1:6379> zrangebyscore myzset -inf +inf withscores
1) "one"
2) "1"
3) "two"
4) "2"
5) "three"
6) "3"
127.0.0.1:6379> zrangebyscore myzset 0 2 withscores
1) "one"
2) "1"
3) "two"
4) "2"

```

## hyperloglog

`Redis 2.8.9` 版本更新了 `hyperloglog` 数据结构，是基于基数统计的算法。

`UV（Unique visitor）`：是指通过互联网访问、浏览这个网页的自然人。访问的一个电脑客户端为一个访客，一天内同一个访客仅被计算一次。

`hyperloglog` 的优点是占用内存小，并且是固定的。存储 2^64 个不同元素的基数，只需要 12 KB 的空间。但是也可能有 0.81% 的错误率。

这个数据结构常用于统计网站的 UV。传统的方式是使用 set 保存用户的ID，然后统计 set 中元素的数量作为判断标准。但是这种方式保存了大量的用户 ID，ID 一般比较长，占空间，还很麻烦。

```bash
# 创建第一组元素
127.0.0.1:6379> pfadd visitNum a b c d
(integer) 1
# 统计基数
127.0.0.1:6379> pfcount visitNum
(integer) 4
127.0.0.1:6379> pfadd visitNum2 a 1 2 3 4
(integer) 1
127.0.0.1:6379> pfcount visitNum2
(integer) 5
# 合并两组
127.0.0.1:6379> pfmerge visitNum3 visitNum visitNum2
OK
127.0.0.1:6379> pfcount visitNum3
(integer) 8
```

## bitmap

bitmap 常用于统计用户信息比如活跃粉丝和不活跃粉丝、登录和未登录、是否打卡等。

```bash
# 设置用户是否登录
127.0.0.1:6379> setbit login 0 1
(integer) 0
127.0.0.1:6379> setbit login 1 1
(integer) 0
127.0.0.1:6379> setbit login 2 0
(integer) 0
127.0.0.1:6379> setbit login 3 0
(integer) 0
127.0.0.1:6379> setbit login 4 1
(integer) 0
# 查看是否登录
127.0.0.1:6379> getbit login 1
(integer) 1
# 统计登录
127.0.0.1:6379> bitcount login
(integer) 3
```
