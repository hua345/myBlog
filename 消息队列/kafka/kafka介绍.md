[TOC]

# KAFKA介绍

> kafka的broker采用主从模式（leader - follower），kafka客户端（生产者和消费者）都是和主节点交互（读写），消息发送到主节点之后，副本节点会从主节点同步消息。follower节点会同步主节点数据（有可能失败），如果同步失败，则这个节点在主节点挂掉后最好不要被选举为leader，因为可能会导致消息丢失

特点：高性能、高吞吐、分布式、大并发、可横向扩展、支持消息数据副本备份、消息持久化

缺点：消息类型比较单一，不支持死信队列，延迟消息

与zookeeper关系：1. kafka基于zookeeper保存broker节点信息 2. 基于ZK实现高可用和leader节点选举 3. 主题、分区、消费者信息都会注册到zookeeper上

**kafka架构图：**
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210406211331816.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NuX2hoYWlw,size_16,color_FFFFFF,t_70)
# KAFKA角色关系
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210406211401464.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NuX2hoYWlw,size_16,color_FFFFFF,t_70)
kafka角色：主题、分区、主题分区位移、生产者、消费者、消费者分组

**消费者组和消费者：**一个消费者组可以包含多个消费者，每个消费者只会属于一个消费者组

**主题：**消息分类，区分消息不同类型的最小单位

**分区：**1. 用于存储topic消息，分区用数字索引区分（0、1、2...），分区可以在同一个broker上，也可以是不同的broker，起到分布式负载作用；

2. ```一个topic主题可以有多个分区```（分区不一定在同一个broker节点上），```每个分区的消息是不同```，```分区与分区之间隔离```，topic的分区之间的消息不会相互同步。**每个topic的每个分区，可以被多个消费者组消费，但只能被消费者组的某一个消费者所消费**，所以**每个topic的每个分区相对于每个消费者组都有一个主题分区位移**；


## 主题分区及分区副本
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210406211527217.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NuX2hoYWlw,size_16,color_FFFFFF,t_70)

- 每个主题（TOPIC）会有多个分区，而每个分区又会有多个本分分区，这些分区当中有一个是leader分区，其他都为follower分区

  1. leader分区接收生产者和消费者请求

  2. follower分区的```唯一作用是同步leader分区的数据```（它的存在只是为了保证消息存储的安全性），同时在leader分区出现故障时替换leader成为新的leader分区。

  3. ```ISR同步副本分区列表```：leader分区默认在里面，follower分区必须是和leader分区同步的才可以放到ISR集合中。

     ​			 	    同步标准：```replica.lag.time.max.ms```（同步时间参数）同步leader分区速度慢于leader写入速度，慢于时间超过replica.lag.time.max.ms后，它就变成“非同步”副本，会被踢出ISR副本集合中。后面如follower副本同步速度提上来，又可能会重新加入ISR副本集合

  4. ```kafka的leader分区选举```：leader分区出故障会优先从ISR同步副本分区选择一个副本作为新的leader，若ISR集合为空（可能其他副本没有真正做到同步没加入到集合）kafka设置了```unclean.leader.election.enable=true```则可以在非同步副本分区选择新leader，但这样会丢失消息，所以应设置为false```unclean.leader.election.enable=false```

- 设置副本分区数 **replication.factor**

> 每个topic的每个分区必须有副本分区，如设置： replication.factor >= 3，保证每个 分区(partition) 至少有 3 个副本，虽然数据冗余，但是带来了数据的安全性。

- 设置最小同步副本数 **min.insync.replicas**

> 如： min.insync.replicas > 1 ，配置代表消息至少要被写入到 2 个副本（含一个leader）才算被成功发送。**min.insync.replicas** 的默认值为 1 ，实际生产中应尽量避免默认值 1
>
> 注意：为保证 Kafka 服务高可用性，需确```replication.factor > min.insync.replicas```，如果两个相等，若有一个副本挂掉，整个分区就无法正常工作（副本挂掉则无法满足条件进而kafka无法工作），这明显违反高可用性，推荐设置 ```replication.factor = min.insync.replicas + 1```

- 设置不从ISR集合列表外选取leader **unclean.leader.election.enable** 

> unclean.leader.election.enable=false 禁止从同步达不到要求的副本中选取leader，这样可防止丢消息（Kafka 0.11.0.0版本开始 unclean.leader.election.enable 参数的默认值由原来的true 改为false）


## 生产者

### 消息发送架构图

![<img src="/Users/hhaip/Documents/16949dd5a85b5fdf.jpg" alt="16949dd5a85b5fdf" style="zoom: 30%;" />](https://img-blog.csdnimg.cn/20210406211550505.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NuX2hoYWlw,size_16,color_FFFFFF,t_70)
1. 消息发送有主线程和发送线程（sender），通过可能的拦截器、序列化器和分区器的作用之后缓存到消息累加器（RecordAccumulator，也称为消息收集器，默认大小32M，生产者参数buffer.memory 配置）中。Sender 线程负责从 RecordAccumulator 中获取消息并将其发送到 Kafka 中。
2. RecordAccumulator 的内部为每个分区都维护了一个双端队列，队列中的内容就是 ProducerBatch。消息写入缓存时，追加到双端队列的尾部；Sender 从双端队列的头部读取。ProducerBatch 中可以包含一至多个 ProducerRecord（由batch.size配置），ProducerRecord 是生产者中创建的消息，而 ProducerBatch 是指一个消息批次。
3. ProducerBatch会被Sender 进一步封装成 <Node, Request> 的形式，这样可以将 Request 请求发往各个 Node（kafka节点），这里的 Request 是指 Kafka 的各种协议请求，对于消息发送指的是 ProduceRequest。
4.  InFlightRequests 保存对象的具体形式为 Map<NodeId, Deque>，主要作用是缓存已经发出去但还没有收到响应的Request请求
5. 同步发送和异步发送，同步发送可返回 RecordMetadata 对象，包含了消息的一些元数据信息，比如当前消息的主题、分区号、分区中的偏移量（offset）、时间戳等

### 自定义分区器

> 分区器的作用就是为消息分配分区

- 生产者在发送消息时可自定义partition分区索引，也可通过key指定，如果 key 不为 null，那么默认的分区器会对 key 进行哈希（采用 MurmurHash2 算法，具备高运算性能及低碰撞率），所以可以通过定义业务key来指定业务消费发送到指定分区（比如一般大型电商都有多个仓库，可以将仓库的名称或 ID 作为 key 来灵活地记录商品信息）。如果没有既没有指定partition也没有指定key，则会默认轮询分区。

如下发送代码示例：

```java
		/**
     * 异步消息
     * <1> 若指定Partition ID,则PR被发送至指定Partition
     * <2> 若未指定Partition ID,但指定了Key, PR会按照hash(key)发送至对应Partition
     * <3> 若既未指定Partition ID也没指定Key，PR会按照round-robin模式发送到每个Partition
     * <4> 若同时指定了Partition ID和Key, PR只会发送到指定的Partition (Key不起作用，代码逻辑决定)
     */
    public void asyncSend(String topic, Integer partition, String key, String message) {
        asyncSend(topic, partition, key, message, null);
    }
```

- 默认分区器

  默认分区器是 org.apache.kafka.clients.producer.internals.DefaultPartitioner

- 自定义分区器

//代码清单4-4 自定义分区器实现
  public class DemoPartitioner implements Partitioner {
      private final AtomicInteger counter = new AtomicInteger(0);
  
      @Override
      public int partition(String topic, Object key, byte[] keyBytes,
                           Object value, byte[] valueBytes, Cluster cluster) {
          List<PartitionInfo> partitions = cluster.partitionsForTopic(topic);
          int numPartitions = partitions.size();
          if (null == keyBytes) {
              return counter.getAndIncrement() % numPartitions;
          }else
              return Utils.toPositive(Utils.murmur2(keyBytes)) % numPartitions;
      }
  
      @Override public void close() {}
  
      @Override public void configure(Map<String, ?> configs) {}
  }
  
  
  //配置参数 partitioner.class 来显式指定这个分区器。示例如下：
  
  props.put(ProducerConfig.PARTITIONER_CLASS_CONFIG, DemoPartitioner.class.getName());



### 自定义生产者拦截器

生产者拦截器需实现 org.apache.kafka.clients.producer. ProducerInterceptor 接口， 接口包含3个方法：

```java
//将消息序列化和计算分区之前会调用
public ProducerRecord<K, V> onSend(ProducerRecord<K, V> record);

//在消息被应答（Acknowledgement）之前或消息发送失败时调用
public void onAcknowledgement(RecordMetadata metadata, Exception exception);

//关闭拦截器时执行一些资源的清理工作
public void close();

```

如下统计发送成功率示例：

```java
public class ProducerInterceptorPrefix implements ProducerInterceptor<String,String>{
    private volatile long sendSuccess = 0, sendFailure = 0;

    @Override
    public ProducerRecord<String, String> onSend(ProducerRecord<String, String> record) {
        String modifiedValue = "prefix1-" + record.value();
        return new ProducerRecord<>(record.topic(), record.partition(), record.timestamp(),record.key(), modifiedValue, record.headers());
    }

    @Override
    public void onAcknowledgement(RecordMetadata recordMetadata, Exception e) {
        if (e == null) {
            sendSuccess++;
        } else {
            sendFailure ++;
        }
    }

    @Override
    public void close() {
        double successRatio = (double)sendSuccess / (sendFailure + sendSuccess);
        System.out.println("[INFO] 发送成功率="+ String.format("%f", successRatio * 100) + "%");
    }

    @Override
    public void configure(Map<String, ?> map) {}
}


//注意：同时需要在 KafkaProducer 的配置参数 interceptor.classes 中指定这个拦截器。示例如下：
properties.put(ProducerConfig.INTERCEPTOR_CLASSES_CONFIG,ProducerInterceptorPrefix.class.getName());

```

### 设置各种生产参数

| 参 数 名 称                           | 默 认 值                        | 参 数 释 义                                                  |
| ------------------------------------- | ------------------------------- | ------------------------------------------------------------ |
| acks                                  | 1                               | 指定分区中必须要有多少个副本收到这条消息                     |
| request.timeout.ms                    | 30000（ms）                     | 配置 Producer 等待请求响应的最长时间                         |
| compression.type                      | none                            | 可以配置为“gzip”“snappy”和“lz4”，消息压缩是一种使用时间换空间的优化方式，如果对时延有一定的要求，则不推荐对消息进行压缩 |
| retries和retry.backoff.ms             | retries=0，retry.backoff.ms=100 | 重试的次数和重试间隔时间                                     |
| key.serializer                        | ""                              | 消息中 key 对应的序列化类，需要实现 org.apache.kafka.common.serialization.Serializer 接口 |
| value.serializer                      | ""                              | 消息中 value 对应的序列化类，需要实现 org.apache.kafka.common.serialization.Serializer 接口 |
| buffer.memory                         | 33554432（32MB）                | 生产者客户端中用于缓存消息的缓冲区大小                       |
| batch.size                            | 16384（16KB）                   | 用于指定 ProducerBatch 可以复用内存区域的大小                |
| client.id                             | ""                              | 用来设定 KafkaProducer 对应的客户端id                        |
| max.block.ms                          | 60000                           | 用来控制 KafkaProducer 中 send() 方法和 partitionsFor() 方法的阻塞时间。当生产者的发送缓冲区已满，或者没有可用的元数据时，这些方法就会阻塞 |
| partitioner.class                     | DefaultPartitioner              | 用来指定分区器，需要实现 org.apache.kafka. clients.producer.Partitioner 接口 |
| enable.idempotence                    | false                           | 是否开启幂等性功能                                           |
| interceptor.classes                   | ""                              | 用来设定生产者拦截器，需要实现 org.apache. kafka.clients.producer. ProducerInterceptor 接口。 |
| max.in.flight.requests.per.connection | 5                               | 限制每个连接（也就是客户端与 Node 之间的连接）最多缓存的请求数 |
| metadata.max.age.ms                   | 300000（5分钟）                 | 如果在这个时间内元数据没有更新的话会被强制更新               |
| transactional.id                      | null                            | 设置事务id，必须唯一                                         |

### ACKS机制

acks这个配置可以指定三个值，分别是0、1和-1（all）

- acks为0：producer发送数据后，不等待broker确认，直接发送下一条数据，性能最快
- acks为1：producer发送数据后，需要等待**leader副本确认**接收后，才会发送下一条数据，性能中等
- acks为-1：发送的消息写入所有的ISR集合中的副本（注意不是全部副本而是ISR同步分区列表中的副本）后，才会发送下一条数据，性能最慢会产生大量冗余数据，但可靠性最强

生产者配置：

```java
Properties props = new Properties();
props.put(CommonClientConfigs.BOOTSTRAP_SERVERS_CONFIG, "172.18.72.**:9092,172.18.113.**:9092");
//提交策略，默认all最保守策略
props.put(ProducerConfig.ACKS_CONFIG, "all");
```



## 消费者

### 订阅主题消费消息

```java
List<String> topicList = Arrays.asList(topic1, topic2); 
consumer.subscribe(topicList);
consumer.subscribe(List<String> topics, ConsumerRebalanceListener callback);//ConsumerRebalanceListener为再均衡拦截器
```

#### 拉取消息

ConsumerRecords<K, V> poll(final Duration timeout)，间参数 timeout，用来控制 poll() 方法的阻塞时间

consumer.poll(Duration.ofMillis(1000));

#### 提交offset位移

> 消费位移存储在 Kafka 内部的主题__consumer_offsets 中。把将消费位移存储起来（持久化）的动作称为“提交”

- 同步提交

  > 注意：同步提交需要设置生产者参数 props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);

  ```java
  public void commitSync();
  public void commitSync(final Map<TopicPartition, OffsetAndMetadata> offsets);  //更细粒度提交
  
  //示例：
  while (isRunning.get()) {
      ConsumerRecords<String, String> records = consumer.poll(1000);
      for (ConsumerRecord<String, String> record : records) {
          //do some logical processing.
      }
      consumer.commitSync();
  }
  ```

- 异步提交

  ```java
  public void commitAsync();
  public void commitAsync(OffsetCommitCallback callback);
  public void commitAsync(final Map<TopicPartition, OffsetAndMetadata> offsets, OffsetCommitCallback callback);
    
  //示例：
  try {
      while (isRunning.get()) {
          //poll records and do some logical processing.
          consumer.commitAsync();
      }
  } finally {
      try {
          consumer.commitSync();
      }finally {
          consumer.close();
      }
  }
  ```

### 控制或关闭消费

```java
//暂停拉取
public void pause(Collection<TopicPartition> partitions);
//恢复拉取
public void resume(Collection<TopicPartition> partitions);
```

### 指定位移消费

```java
public void seek(TopicPartition partition, long offset);
consumer.subscribe(Arrays.asList(topic)); 
consumer.seek(new TopicPartition(topic,0),10);
```

### 获取消费者分配的分区信息

```java
public Set<TopicPartition> assignment()
```



### 重要参数

| 参 数 名 称             | 默 认 值              | 参 数 释 义                                                  |
| ----------------------- | --------------------- | ------------------------------------------------------------ |
| fetch.min.bytes         | 1B                    | 取的最小数据量                                               |
| fetch.max.bytes         | 50MB                  | 取的最大数据量                                               |
| fetch.max.wait.ms       | 500（ms）             | Kafka 中没有足够多的消息而满足不了 fetch.min.bytes 参数的要求，那么最终会等待500ms |
| max.poll.records        | 500                   | 拉取的最大消息数                                             |
| connections.max.idle.ms | 540000（ms），即9分钟 | 指定在多久之后关闭闲置的连接                                 |
| request.timeout.ms      | 30000（ms）           | 等待请求响应时间                                             |




# 动态重平衡（Rebalance）

## GroupCoordinator

> 每个kafka的broker启动时，都会一起启动一个Group Coordinator实例

### GroupCoordinator作用：

1. 消费者组管理

   - 从消费者组中选举leader

   - 消费者和分区分配关系、消费者组的状态信息保存在Coordinator中

   - 保存消费者组和消费者元数据信息

   - 监听消费者变化（消费者上下线），与消费者之间保持心跳（hartbeat），负责触发Rebalance

   - 消费者和分区之间的消费规则分配的协调中间者（实际分区和消费者之间的消关系由消费者组里的leader消费者负责），将leader消费者处理的和分区的关系结果发送给Coordinator，由Coordinator同步给其他follower消费者

2. offset管理

   - 负责提交offset，同时将消费者topic消费的分区offset写入到__consumer_offsets主题（该主题默认有50个分区）

### GroupCoordinator和消费者间的消息类型

1. heartbeat：Group中的Consumer周期性地给Coordinator发送该心跳信号，表示自己存活；

2. join-group：Consumer请求加入Group的信号；

3. leave-group：Consumer主动退出Group的信号；

4. sync-group：Coordinator将已生成的Consumer-Partition消费对应关系分发给Consumer的信号

### GroupCoordinator消费者心跳

1. 消费者和GroupCoordinator之间保持心跳连接
2. 消费者有一个单独的心跳线程负责发送心跳



## Rebalance

### Rebalance发生条件：

1. 分区发生变化（新增或删除topic分区）
2. 消费客户端上线或下线

### Rebalance过程

> 分为joinGroup和syncGroup两步

1. consumer 向 Coordinator 发送 joinGroup 请求（原本在组内的consumer会放弃自己的partition）， (joinGroup send) 
2. Coordinator 收到组内所有消费者的 joinGroup 请求，选举一个leader消费者， 若consumer为 leader 则返回当前所有组内成员信息，若为 follower，则返回空。(joinGroup respond)，group 进入 PreparingRebalance 状态。
3. consumer 收到回复后，若发现自己为 leader，则根据返回的信息，执行 rebalance 的计算（进行消费者和partition消费关系分配），计算完成后将 rebalance 结果通过 syncGroup 请求发送给 Coordinator。若自己为 follower，则直接发送 syncGroup 请求。(joinGroup recv，syncGroup send) 
4. Coordinator 收到 syncGroup 请求，判断请求方是否为 leader，如果不是 leader，则等待 leader 将 rebalance 结果送达，如果请求方是 leader，则给所有的 syncGroup 请求返回 rebalance 的结果。 (syncGroup respond) 
5.  consumer 收到 syncGroup 结果，则调用相应的回调方法，(onPartitionRebalance) 按照最新的 rebalance 结果进行消费

### Rebalance的改进方案

#### Rebalance产生的问题

1. ```stop-the-world```问题——需要收回（revoke）所有Partition再重新分配（reassign），在此时间内所有Consumer都无法进行消费，如果Rebalance时间长，会造成延迟，同时消费者过多有可能出现频繁的Rebalance情况

2. ```back-and-forth```问题——如果多次触发Rebalance，很有可能造成一个Consumer消费的Partition被分配给其他Consumer，然后又分配回来，做了无用功

为了解决该问题，在kafka2.4版本 特别提出了**Incremental（增量）Rebalance**。就是Rebalance时不再让所有Consumer都放弃掉所有已分配的Partition，而是每次先记录，并转化成多次少量的Rebalance过程，且Consumer在此期间不会STW。简图如下所示

![\[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-6O6bWds9-1617714767125)(/Users/hhaip/Documents/195230-890a7cc54fe5a1ec.png)\]](https://img-blog.csdnimg.cn/20210406211646500.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NuX2hoYWlw,size_16,color_FFFFFF,t_70)

# kafka为什么那么快

> kafka快的原因：1、消息顺序写入磁盘（写消息到磁盘，效率比随机写入高）  2、零拷贝技术（读消息）

## 消息数据存储

### Partition消息存储

消息持久化存储：Kafka初始会单独开辟一块磁盘空间，将数据保存在磁盘内，消息按partition顺序追加写入数据

Partition在服务器上的对应一个一个的文件夹，每个partition文件夹下会有多个segment文件，每组segment文件又包含```.index文件```、```.log文件```、```.timeindex文件```（早期版本中没有）三个文件

> **log文件就实际是存储message的地方，而index和timeindex文件为索引文件，用于检索消息**

![<img src="/Users/hhaip/Downloads/企业微信20210330-165908@2x.png" alt="企业微信20210330-165908@2x" style="zoom:50%;" />](https://img-blog.csdnimg.cn/20210406211801533.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NuX2hoYWlw,size_16,color_FFFFFF,t_70)
![\[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-QTqDDoxQ-1617714767128)(/Users/hhaip/Documents/90DE5297-0689-4EA7-B3C6-5E6FF8184715.png)\]](https://img-blog.csdnimg.cn/20210406211850624.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NuX2hoYWlw,size_16,color_FFFFFF,t_70)


- segment文件命名：文件的命名是以该segment最小offset来命名的，如000.index存储offset为0~368795的消息；```kafka利用分段+索引的方式来解决查找效率的问题```。

- log文件数据存储：

  > log文件存储的是一个个Message实体，producer往kafka写入是一条一条的message，Message数据结构：消息体、消息大小、offset、压缩类型……等等！

  1. Message数据结构说明：

     - offset：offset是一个占8byte的有序id号，它可以唯一确定每条消息在parition内的位置！

     - 消息大小：消息大小占用4byte，用于描述消息的大小。

     - 消息体：消息体存放的是实际的消息数据（被压缩过），占用的空间根据具体的消息而不一样。

  2. Kafka旧数据删除策略：

     - 基于时间，默认配置是168小时（7天）

     - 基于大小，默认配置是1073741824。

> 注意：kafka读取消息时间复杂度是O(1)，所以删除过期的文件并不会提高kafka的性能

### 消息消费和查找

> 如：kafka查找某个offset的消息，**位移offset存储在__consumer_offsets主题中**

- 通过二分查找的方式先找到segment文件
- 再次通过二分查找在index文件中找到offset所对应消息在log中的索引



## 零拷贝技术

**传统拷贝技术**

> 内核空间拷贝到用户空间是通过CPU调度进行的
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210406212009927.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NuX2hoYWlw,size_16,color_FFFFFF,t_70)

**DMA拷贝技术**

> DMA拷贝减少了从内核空间复制到应用空间步骤，减少了上下文切换和数据复制次数。此时对网卡缓冲区的操作可映射到内核缓冲区，相当于两个缓冲区数据共享。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210406212023988.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NuX2hoYWlw,size_16,color_FFFFFF,t_70)
传统内存访问，所有请求都会发送到 CPU ，然后再由 CPU 来完成相关调度工作：
![\[外链图片转存失败,源站可能有防盗链机制,建议将图片保存下来直接上传(img-yVBB0P5P-1617714767133)(/Users/hhaip/Documents/2323.png)\]](https://img-blog.csdnimg.cn/20210406212051275.png)
DMA 技术的出现，数据文件可直接在各个层之间的传输，则可以直接绕过CPU，使得外围设备可以通过DMA控制器直接访问内存。与此同时，CPU可以继续执行程序：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210406212100959.png)

**Java零拷贝的实现**

```java
File file = new File("demo.zip");
RandomAccessFile raf = new RandomAccessFile(file, "rw");
FileChannel fileChannel = raf.getChannel();
SocketChannel socketChannel = SocketChannel.open(new InetSocketAddress("", 1234));
// 直接使用了transferTo()进行通道间的数据传输
fileChannel.transferTo(0, fileChannel.size(), socketChannel);
```

Java的零拷贝由 FileChannel.transferTo() 方法实现。transferTo() 方法将数据从 FileChannel 对象传送到可写的字节通道（如Socket Channel等）。在内部实现中，由 native 方法 transferTo() 来实现，它依赖底层操作系统的支持。在 UNIX 和 Linux系统中，调用这个方法将会引起 sendfile() 系统调用。



**Kafka快的原因**

> 1. partition顺序读写，充分利用磁盘特性
>
> 2. Producer生产的数据持久化到broker，采用mmap文件映射，实现顺序的快速写入（数据直接从NIC buffer复制到read buffer）；
> 3. Customer从broker读取数据，采用sendfile，将磁盘文件读到OS内核缓冲区后，直接转到socket buffer进行网络发送。
>
> mmap 和 sendfile总结
>
> 1. 都是Linux内核提供、实现零拷贝的API；
>
> 2. sendfile 是将读到内核空间的数据，转到socket buffer，进行网络发送；
>
> 3. mmap将磁盘文件映射到内存，支持读和写，对内存的操作会反映在磁盘文件上。
>
>    RocketMQ 在消费消息时，使用了 mmap（推消息），kafka 使用了 sendFile（拉消息）
> 