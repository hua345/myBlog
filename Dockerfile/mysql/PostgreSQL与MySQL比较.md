# 参考

- [PostgreSQL与MySQL比较](https://www.cnblogs.com/geekmao/p/8541817.html)

## PostgreSQL主要优势

1. PostgreSQL完全免费，而且是BSD协议，如果你把PostgreSQL改一改，然后再拿去卖钱，也没有人管你，这一点很重要，这表明了PostgreSQL数据库不会被其它公司控制。
2. 与PostgreSQl配合的开源软件很多，有很多分布式集群软件，如pgpool、pgcluster等等，很容易做读写分离、负载均衡、数据水平拆分等方案，而这在MySQL下则比较困难。
3. PostgreSQL在很多方面都比MySQL强，如复杂SQL的执行、存储过程、触发器、索引。同时PostgreSQL是多进程的，而MySQL是线程的，虽然并发不高时，MySQL处理速度快，但当并发高的时候，对于现在多核的单台机器上，MySQL的总体处理性能不如PostgreSQL，原因是MySQL的线程无法充分利用CPU的能力。
