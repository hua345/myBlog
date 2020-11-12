# 本地kafka异常

```log
 (NetworkClient.java.processDisconnection:671.kafka-producer-network-thread) Connection to node 163 could not be established. Broker may not be available.
```

```bash
$ netstat -h

显示协议统计信息和当前 TCP/IP 网络连接。

NETSTAT [-a] [-b] [-e] [-f] [-n] [-o] [-p proto] [-r] [-s] [-x] [-t] [interval]

  -a            显示所有连接和侦听端口。
  -b            显示在创建每个连接或侦听端口时涉及的
                可执行程序。在某些情况下，已知可执行程序承载
                多个独立的组件，这些情况下，
                显示创建连接或侦听端口时
                涉及的组件序列。在此情况下，可执行程序的
                名称位于底部 [] 中，它调用的组件位于顶部，
                直至达到 TCP/IP。注意，此选项
                可能很耗时，并且在你没有足够
                权限时可能失败。
  -e            显示以太网统计信息。此选项可以与 -s 选项
                结合使用。
  -f            显示外部地址的完全限定
                域名(FQDN)。
  -n            以数字形式显示地址和端口号。
  -o            显示拥有的与每个连接关联的进程 ID。
  -p proto      显示 proto 指定的协议的连接；proto
                可以是下列任何一个: TCP、UDP、TCPv6 或 UDPv6。如果与 -s
                选项一起用来显示每个协议的统计信息，proto 可以是下列任何一个:
                IP、IPv6、ICMP、ICMPv6、TCP、TCPv6、UDP 或 UDPv6。
  -q            显示所有连接、侦听端口和绑定的
                非侦听 TCP 端口。绑定的非侦听端口
                 不一定与活动连接相关联。
  -r            显示路由表。
  -s            显示每个协议的统计信息。默认情况下，
                显示 IP、IPv6、ICMP、ICMPv6、TCP、TCPv6、UDP 和 UDPv6 的统计信息;
                -p 选项可用于指定默认的子网。
  -t            显示当前连接卸载状态。
  -x            显示 NetworkDirect 连接、侦听器和共享
                终结点。
  -y            显示所有连接的 TCP 连接模板。
                无法与其他选项结合使用。
```

```bash
# 查看显示所有连接，对应的程序、地址、进程id
netstat -abno

 [java.exe]
  TCP    127.0.0.1:51132        127.0.0.1:51131        ESTABLISHED     36856
 [java.exe]
  TCP    127.0.0.1:51140        127.0.0.1:51141        ESTABLISHED     36856
 [java.exe]
  TCP    127.0.0.1:51141        127.0.0.1:51140        ESTABLISHED     36856
 [java.exe]
  TCP    127.0.0.1:51142        127.0.0.1:51143        ESTABLISHED     36856

# 查看网络连接数：
netstat -an |wc -l
# 查看进程连接数
netstat -an |grep 39868 |wc -l
# 查看连接数等待time_wait状态连接数
netstat -an |grep TIME_WAIT|wc -l
# 查看建立稳定连接数量
netstat -an |grep ESTABLISHED |wc -l
# 查看进程详情
tasklist |findstr 36856
java.exe                     36856 Console                    1    968,636 K
```
