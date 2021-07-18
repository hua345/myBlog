# kafka 查询历史消息

## 查看 log 文件中的信息

```log
➜  ~ kafka-run-class.sh kafka.tools.DumpLogSegments --files /var/kafka/data01/fang-0/00000000000000000000.log --print-data-log
 Dumping /var/kafka/data01/fang-0/00000000000000000000.log
Starting offset: 0
baseOffset: 0 lastOffset: 0 count: 1 baseSequence: -1 lastSequence: -1 producerId: -1 producerEpoch: -1 partitionLeaderEpoch: 0 isTransactional: false isControl: false position: 0 CreateTime: 1595837169568 size: 85 magic: 2 compresscodec: NONE crc: 3509577165 isvalid: true
| offset: 0 CreateTime: 1595837169568 keysize: -1 valuesize: 17 sequence: -1 headerKeys: [] payload: fangfang love you
baseOffset: 1 lastOffset: 1 count: 1 baseSequence: -1 lastSequence: -1 producerId: -1 producerEpoch: -1 partitionLeaderEpoch: 0 isTransactional: false isControl: false position: 85 CreateTime: 1595837191066 size: 72 magic: 2 compresscodec: NONE crc: 1281169013 isvalid: true
| offset: 1 CreateTime: 1595837191066 keysize: -1 valuesize: 4 sequence: -1 headerKeys: [] payload: fang
```

## 获取指定主题当前总的消息数量

```bash
# --time -1 表示最大位移；--time -2 表示最早位移，这个通常是0
kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list 192.168.137.128:9092 --topic fang --time -1
fang:0:23

kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list 192.168.137.128:9092 --topic fang --time -2
fang:0:0
```

## 根据位移查询消息

```bash
➜  ~ kafka-console-consumer.sh --bootstrap-server  192.168.137.128:9092 --offset 1 --partition 0 --topic fang --max-messages 1
fang
```

## 根据时间戳查询

```bash
kafka-dump-log.sh --files  00000000000000000000.timeindex
Dumping 00000000000000000000.timeindex
timestamp: 1595852466014 offset: 299026
timestamp: 1595852466017 offset: 299332
timestamp: 1595852466018 offset: 299740
```
