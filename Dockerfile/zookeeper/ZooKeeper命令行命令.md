# ZooKeeper 命令行命令

```bash
# 连接服务器 zkCli -server IP:PORT
zkCli.sh -server 192.168.137.128:2181

# 帮助命令
[zk: 192.168.137.128:2181(CONNECTED) 1] help
ZooKeeper -server host:port cmd args
        addauth scheme auth
        close
        config [-c] [-w] [-s]
        connect host:port
        create [-s] [-e] [-c] [-t ttl] path [data] [acl]
        delete [-v version] path
        deleteall path
        delquota [-n|-b] path
        get [-s] [-w] path
        getAcl [-s] path
        history
        listquota path
        ls [-s] [-w] [-R] path
        ls2 path [watch]
        printwatches on|off
        quit
        reconfig [-s] [-v version] [[-file path] | [-members serverID=host:port1:port2;port3[,...]*]] | [-add serverId=host:port1:port2;port3[,...]]* [-remove serverId[,...]*]
        redo cmdno
        removewatches path [-c|-d|-a] [-l]
        rmr path
        set [-s] [-v version] path data
        setAcl [-s] [-v version] [-R] path acl
        setquota -n|-b val path
        stat [-w] path
        sync path


# 获取根节点列表，默认会有一个zookeeper节点，节点列表就像linux目录一样，根节点为/
ls /

# 创建节点(create 命令)
[zk: 192.168.137.128:2181(CONNECTED) 3] create /node1 "node1"
Created /node1

# 获取节点的数据(get 命令)
[zk: 192.168.137.128:2181(CONNECTED) 4] get /node1
node1

# 更新节点数据内容(set 命令)
[zk: 192.168.137.128:2181(CONNECTED) 5] set /node1 "fangfang"

# 查看节点状态(stat 命令)
[zk: 192.168.137.128:2181(CONNECTED) 6] stat /node1
cZxid = 0x100000007
ctime = Wed Jul 17 01:23:43 CST 2019
mZxid = 0x100000008
mtime = Wed Jul 17 01:24:37 CST 2019
pZxid = 0x100000007
cversion = 0
dataVersion = 1
aclVersion = 0
ephemeralOwner = 0x0
dataLength = 8
numChildren = 0

# 删除节点(delete 命令)
delete /node1
```
