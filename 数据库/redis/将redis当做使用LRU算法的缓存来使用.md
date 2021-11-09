# 参考

- [将redis当做使用LRU算法的缓存来使用](http://www.redis.cn/topics/lru-cache.html)

> 当Redis被当做缓存来使用，当你新增数据时，让它自动地回收旧数据是件很方便的事情。
>
> `LRU`是Redis唯一支持的回收方法。本页面包括一些常规话题，Redis的`maxmemory`指令用于将可用内存限制成一个固定大小，
还包括了`Redis`使用的`LRU`算法，这个实际上只是近似的LRU。

## Maxmemory配置指令

`maxmemory`配置指令用于配置Redis存储数据时指定限制的内存大小。通过`redis.conf`可以设置该指令，或者之后使用CONFIG SET命令来进行运行时配置。

例如为了配置内存限制为100mb，以下的指令可以放在`redis.conf`文件中。

```conf
maxmemory 100mb
```

设置`maxmemory`为0代表没有内存限制。对于64位的系统这是个默认值，对于32位的系统默认内存限制为3GB。

## 回收策略

当`maxmemory`限制达到的时候Redis会使用的行为由 Redis的`maxmemory-policy`配置指令来进行配置。

以下的策略是可用的:

- `noeviction`:返回错误当内存限制达到并且客户端尝试执行会让更多内存被使用的命令（大部分的写入指令，但DEL和几个例外）
- `allkeys-lru`: 尝试回收最少使用的键（LRU），使得新添加的数据有空间存放。
- `volatile-lru`: 尝试回收最少使用的键（LRU），但仅限于在过期集合的键,使得新添加的数据有空间存放。
- `allkeys-random`: 回收随机的键使得新添加的数据有空间存放。
- `volatile-random`: 回收随机的键使得新添加的数据有空间存放，但仅限于在过期集合的键。
- `volatile-ttl`: 回收在过期集合的键，并且优先回收存活时间（TTL）较短的键,使得新添加的数据有空间存放。

## 近似LRU算法

Redis的LRU算法并非完整的实现。这意味着Redis并没办法选择最佳候选来进行回收，也就是最久未被访问的键。

相反它会尝试运行一个近似LRU的算法，通过对少量keys进行取样，然后回收其中一个最好的key（被访问时间较早的）。

过从Redis 3.0算法已经改进为回收键的候选池子。这改善了算法的性能，使得更加近似真是的LRU算法的行为。

Redis LRU有个很重要的点，你通过调整每次回收时检查的采样数量，以实现调整算法的精度。这个参数可以通过以下的配置指令调整:

```conf
maxmemory-samples 5
```

Redis为什么不使用真实的LRU实现是因为这需要太多的内存。不过近似的LRU算法对于应用而言应该是等价的。

使用真实的LRU算法与近似的算法可以通过下面的图像对比。

![lru_comparison.png](./img/lru_comparison.png)
