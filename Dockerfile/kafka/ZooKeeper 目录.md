# 参考

- [http://kafka.apachecn.org/documentation.html#impl_zookeeper](http://kafka.apachecn.org/documentation.html#impl_zookeeper)

下面给出了Zookeeper的结构和算法，用于协调`consumer`和`broker`。

## Broker节点注册

```bash
/brokers/ids/[0...N] --> {"jmx_port":...,"timestamp":...,"endpoints":[...],"host":...,"version":...,"port":...} (ephemeral node)
```

这是当前所有`broker`的节点列表，其中每个提供了一个唯一的逻辑`broker`的id标识它的`consumer`（必须作为配置的一部分）。在启动时，broker节点通过在`/brokers/ids/`下用逻辑`broker id`创建一个znode来注册它自己。

逻辑`broker id`的目的是当broker移动到不同的物理机器时，而不会影响消费者。尝试注册一个已存在的broker id时将返回错误（因为2个server配置了相同的broker id）。

由于broker在Zookeeper中用的是`临时znode`来注册，因此这个注册是动态的，如果broker关闭或宕机，节点将消失（通知consumer不再可用）。

## Broker Topic 注册

```bash
/brokers/topics/[topic]/partitions/[0...N]/state --> {"controller_epoch":...,"leader":...,"version":...,"leader_epoch":...,"isr":[...]} (ephemeral node)
```

每个`broker`在它自己的topic下注册，维护和存储该topic分区的数据。

## Consumer Id 注册

除了由所有consumer共享的group_id，每个consumer都有一个临时且唯一的consumer_id（主机名的形式:uuid）用于识别。consumer的id在以下目录中注册。

```bash
/consumers/[group_id]/ids/[consumer_id] --> {"version":...,"subscription":{...:...},"pattern":...,"timestamp":...} (ephemeral node)
```

组中的每个consumer用consumer_id注册znode。znode的值包含一个map。这个id只是用来识别在组里目前活跃的consumer，这是个临时节点，如果consumer在处理中挂掉，它就会消失。

## Consumer Offsets

Consumers track the maximum offset they have consumed in each partition. This value is stored in a ZooKeeper directory if offsets.storage=zookeeper.

```bash
/consumers/[group_id]/offsets/[topic]/[partition_id] --> offset_counter_value (persistent node)
```
