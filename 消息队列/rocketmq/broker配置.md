## broker配置

```conf
brokerClusterName = DefaultCluster
brokerName = broker-a
# 0为master, 1是slave
brokerId = 0
# 记录消息轨迹
traceTopicEnable=true
#默认的Topic队列数
defaultTopicQueueNums=8
#自动创建Topic，建议线上关闭，线下开启
autoCreateTopicEnable=false
#磁盘文件空间充足情况下，默认每天什么时候执行删除过期文件，默认04表示凌晨4点
deleteWhen = 04
#文件保留时间单位小时
fileReservedTime = 48
#ASYNC_MASTER 异步复制Master
#SYNC_MASTER 同步双写Master
brokerRole = ASYNC_MASTER
#刷盘策略
flushDiskType = ASYNC_FLUSH
```
