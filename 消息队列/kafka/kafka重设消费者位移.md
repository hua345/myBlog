# kafka重设消费者位移

## 查看消费组信息

```bash
# 查看消费组列表
➜  ~ kafka-consumer-groups.sh  --bootstrap-server 192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094  --list
fangGroup02
fangGroup01
fangGroup
# 查看消费组详情
➜  ~ kafka-consumer-groups.sh  --bootstrap-server 192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094  --describe --group fangGroup01

GROUP           TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             CONSUMER-ID                                                 HOST             CLIENT-ID
fangGroup01     fangfang        0          9               9               0               consumer-fangGroup01-1-695bafa0-8ddc-4d0a-9569-e932bd2b9fb9 /192.168.137.128 consumer-fangGroup01-1
fangGroup01     fangfang        1          9               9               0               consumer-fangGroup01-1-695bafa0-8ddc-4d0a-9569-e932bd2b9fb9 /192.168.137.128 consumer-fangGroup01-1
```

## 重设位移必须要停止消费者

```bash
➜  ~ kafka-consumer-groups.sh -help
This tool helps to list all consumer groups, describe a consumer group, delete consumer group info, or reset consumer group offsets.
Option                                  Description

--reset-offsets                         Reset offsets of consumer group.
                                          Supports one consumer group at the
                                          time, and instances should be
                                          inactive
                                        Has 2 execution options: --dry-run
                                          (the default) to plan which offsets
                                          to reset, and --execute to update
                                          the offsets. Additionally, the --
                                          export option is used to export the
                                          results to a CSV format.
                                        You must choose one of the following
                                          reset specifications: --to-datetime,
                                          --by-period, --to-earliest, --to-
                                          latest, --shift-by, --from-file, --
                                          to-current.
--shift-by <Long: number-of-offsets>    Reset offsets shifting current offset
                                          by 'n', where 'n' can be positive or
                                          negative.
--to-current                            Reset offsets to current offset.
--to-datetime <String: datetime>        Reset offsets to offset from datetime.
                                          Format: 'YYYY-MM-DDTHH:mm:SS.sss'
--to-earliest                           Reset offsets to earliest offset.
--to-latest                             Reset offsets to latest offset.
--to-offset <Long: offset>              Reset offsets to a specific offset.
--topic <String: topic>                 The topic whose consumer group
```

```bash
# 从最早位移处开始消费，这个最早位移不一定就是 0 ，因为很久远的消息会被 Kafka 自动删除，主要取决于你的删除配置。
➜  ~ kafka-consumer-groups.sh --bootstrap-server 192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094 --group fangGroup01 --reset-offsets --all-topics --to-earliest --execute

GROUP                          TOPIC                          PARTITION  NEW-OFFSET
fangGroup01                    fangfang                       1          0
fangGroup01                    fangfang                       0          0

# 移动到前三个消息位置
➜ ~ kafka-consumer-groups.sh --bootstrap-server 192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094 --group fangGroup01 --reset-offsets --topic fangfang --shift-by -3 --execute

GROUP                          TOPIC                          PARTITION  NEW-OFFSET
fangGroup01                    fangfang                       0          6
fangGroup01                    fangfang                       1          6


# 直接指定位移
➜ ~ kafka-consumer-groups.sh --bootstrap-server 192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094 --group fangGroup01 --reset-offsets --topic fangfang --to-offset 6 --execute

GROUP                          TOPIC                          PARTITION  NEW-OFFSET
fangGroup01                    fangfang                       0          6
fangGroup01                    fangfang                       1          6

# 指定消息提交的时间
➜ ~ kafka-consumer-groups.sh --bootstrap-server 192.168.137.128:9092,192.168.137.128:9093,192.168.137.128:9094 --group fangGroup01 --reset-offsets --topic fangfang --to-datetime 2020-07-28T00:00:00.000  --execute

GROUP                          TOPIC                          PARTITION  NEW-OFFSET
fangGroup01                    fangfang                       0          8
fangGroup01                    fangfang                       1          7
```
