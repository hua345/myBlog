# 参考

- [CS-Notes 缓存](https://github.com/CyC2018/CS-Notes/blob/master/notes/%E7%BC%93%E5%AD%98.md)
- [看完这篇Redis缓存三大问题，保你面试能造火箭，工作能拧螺丝。](https://juejin.im/post/5edceb206fb9a047a644684f)
- [Redis缓存如何保证一致性](https://www.cnblogs.com/AshOfTime/p/10815593.html)
- [Redis 缓存雪崩、击穿、穿透](https://segmentfault.com/a/1190000022029639)

## 1.缓存穿透

缓存穿透是指查询一条数据库和缓存都没有的一条数据，就会一直查询数据库，对数据库的访问压力就会增大。

缓存穿透的解决方案，有以下两种：

- 缓存空对象：代码维护较简单，但是效果不好。
- 布隆过滤器：代码维护复杂，效果很好。

## 2.缓存击穿

缓存击穿是指一个key非常热点，在不停的扛着大并发，大并发集中对这一个点进行访问，当这个key在失效的瞬间，持续的大并发就穿破缓存，直接请求数据库，瞬间对数据库的访问压力增大。

缓存击穿这里强调的是并发，造成缓存击穿的原因有以下两个：

- 该数据没有人查询过 ，第一次就大并发的访问。（冷门数据）
- 添加到了缓存，reids有设置数据失效的时间 ，这条数据刚好失效，大并发访问（热点数据）

## 3.缓存雪崩

指的是由于数据没有被加载到缓存中，或者缓存数据在同一时间大面积失效（过期），又或者缓存服务器宕机，导致大量的请求都到达数据库。

在有缓存的系统中，系统非常依赖于缓存，缓存分担了很大一部分的数据请求。当发生缓存雪崩时，数据库无法处理这么大的请求，导致数据库崩溃。

比如天猫双11，马上就要到双11零点，很快就会迎来一波抢购，这波商品在23点集中的放入了缓存，假设缓存一个小时，那么到了凌晨24点的时候，这批商品的缓存就都过期了。

对于缓存雪崩的解决方案有以下两种：

- 为了防止缓存在同一时间大面积过期导致的缓存雪崩，可以通过观察用户行为，合理设置缓存过期时间来实现；
- 为了防止缓存服务器宕机出现的缓存雪崩，可以使用分布式缓存，分布式缓存中每一个节点只缓存部分的数据，当某个节点宕机时可以保证其它节点的缓存仍然可用。
- 也可以进行缓存预热，避免在系统刚启动不久由于还未将大量数据进行缓存而导致缓存雪崩。

## 4.缓存一致性

数据库和缓存之间一般不需要强一致性,最终一致性就可以了。

对Redis里的数据设置合理的过期时间能够保证最终一致性。

### Cache Aside Pattern--先写数据库，再删缓存

为什么更新数据库后不更新而是删除缓存？

更新缓存的操作不是必须的。可能缓存里的数据并没有被读到，就会被下一次更新MySQL操作带来Redis更新操作覆盖，那么本次更新操作就是无意义的。
