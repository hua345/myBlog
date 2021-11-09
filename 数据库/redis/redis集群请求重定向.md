# 参考

- [redis实战第十二篇 redis cluster请求重定向](https://blog.csdn.net/u012062455/article/details/87436237)

> 在集群模式下，redis在接收到键任何命令时会先计算该键所在的槽，
>
> 如果改键所在的槽位于当前节点，则直接执行命令，如果改键位于其它节点，则不执行该命令，返回重定向信息。

```bash
#比如name这个键在槽位5798，而槽位5798位于6380节点上，假设在6379上执行get name，则会返回重定向信息

127.0.0.1:6379> get name
(error) MOVED 5798 192.168.137.128:6380
```

## 查找键所在的节点信息

```bash
127.0.0.1:6379> cluster keyslot name
(integer) 5798
```

再通过`cluster nodes`获取槽所在节点的信息，就可以知道键所在的节点信息。

## 使用-c参数来自动重定向

在使用redis-cli时，可以加上-c参数，这样redis会自动帮我们连接到正确的节点执行命令。

```bash
➜  ~ redis-cli -p 6379 -c
127.0.0.1:6379> get name
-> Redirected to slot [5798] located at 192.168.137.128:6380
"fang"
```

## hash_tag

> 如果键中包含{}，则集群在计算槽时会使用{}内的内容，而不是整个键，{}内的内容又称为hash_tag。
>
> 它提供不同的键拥有相同的slot功能，通常用于redis IO优化。

```bash
# 不加{}，name和age会被放到不同的槽中
192.168.137.128:6380> set user:info:name fang
-> Redirected to slot [14914] located at 192.168.137.128:6381
OK
192.168.137.128:6381> set user:info:age 20
-> Redirected to slot [8325] located at 192.168.137.128:6380
OK

# 加上{}，所有的键都位于同一个槽中

192.168.137.128:6380> set user:{info}:name fang
OK
192.168.137.128:6380> set user:{info}:age fang
OK
```
