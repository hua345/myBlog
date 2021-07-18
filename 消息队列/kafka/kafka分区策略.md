# kafka

## kafka为什么要分区

- 负载均衡，实现系统的高伸缩性。为什么这么说呢？因为不同的分区可以放置在不通的机器节点上，当我们服务的吞吐量特别大的时候，可以通过增加节点来进行提高吞吐量。
- 实现业务级别的消息顺序的问题。

## 分区策略

`分区策略指的是决定生产者将消息发送到那个分区的算法`

kafka是有默认的分区策略

```java
public class DefaultPartitioner implements Partitioner {
    private final StickyPartitionCache stickyPartitionCache = new StickyPartitionCache();

    public DefaultPartitioner() {
    }

    public void configure(Map<String, ?> configs) {
    }

    public int partition(String topic, Object key, byte[] keyBytes, Object value, byte[] valueBytes, Cluster cluster) {
        if (keyBytes == null) {
            return this.stickyPartitionCache.partition(topic, cluster);
        } else {
            List<PartitionInfo> partitions = cluster.partitionsForTopic(topic);
            int numPartitions = partitions.size();
            return Utils.toPositive(Utils.murmur2(keyBytes)) % numPartitions;
        }
    }
}

public class StickyPartitionCache {
    private final ConcurrentMap<String, Integer> indexCache = new ConcurrentHashMap();

    public StickyPartitionCache() {
    }

    public int partition(String topic, Cluster cluster) {
        Integer part = (Integer)this.indexCache.get(topic);
        return part == null ? this.nextPartition(topic, cluster, -1) : part;
    }

    public int nextPartition(String topic, Cluster cluster, int prevPartition) {
        List<PartitionInfo> partitions = cluster.partitionsForTopic(topic);
        Integer oldPart = (Integer)this.indexCache.get(topic);
        Integer newPart = oldPart;
        if (oldPart != null && oldPart != prevPartition) {
            return (Integer)this.indexCache.get(topic);
        } else {
            List<PartitionInfo> availablePartitions = cluster.availablePartitionsForTopic(topic);
            Integer random;
            if (availablePartitions.size() < 1) {
                random = Utils.toPositive(ThreadLocalRandom.current().nextInt());
                newPart = random % partitions.size();
            } else if (availablePartitions.size() == 1) {
                newPart = ((PartitionInfo)availablePartitions.get(0)).partition();
            } else {
                while(newPart == null || newPart.equals(oldPart)) {
                    random = Utils.toPositive(ThreadLocalRandom.current().nextInt());
                    newPart = ((PartitionInfo)availablePartitions.get(random % availablePartitions.size())).partition();
                }
            }

            if (oldPart == null) {
                this.indexCache.putIfAbsent(topic, newPart);
            } else {
                this.indexCache.replace(topic, prevPartition, newPart);
            }

            return (Integer)this.indexCache.get(topic);
        }
    }
}
```

- 如果没有指定`key`,默认是轮询
- 如果执行`key`,是按照`key`进行分发的
