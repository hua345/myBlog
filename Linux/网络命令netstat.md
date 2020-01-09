#### 1.参考

- [Linux netstat命令详解](https://www.cnblogs.com/ftl1012/p/netstat.html)

> netstat命令用于显示与IP、TCP、UDP和ICMP协议相关的统计数据，一般用于检验本机各端口的网络连接情况。

#### 2.安装netstat

```bash
➜  ~ yum provides netstat
➜  ~ yum install net-tools
```

#### 3.查看帮助

```bash
➜  ~ netstat -h
usage: netstat [-vWeenNcCF] [<Af>] -r         netstat {-V|--version|-h|--help}
       netstat [-vWnNcaeol] [<Socket> ...]
       netstat { [-vWeenNac] -I[<Iface>] | [-veenNac] -i | [-cnNe] -M | -s [-6tuw] } [delay]

        -r, --route              display routing table
        -I, --interfaces=<Iface> display interface table for <Iface>
        -i, --interfaces         display interface table
        -g, --groups             display multicast group memberships
        -s, --statistics         display networking statistics (like SNMP)
        -M, --masquerade         display masqueraded connections

        -v, --verbose            be verbose
        -W, --wide               don't truncate IP addresses
        -n, --numeric            don't resolve names
        --numeric-hosts          don't resolve host names
        --numeric-ports          don't resolve port names
        --numeric-users          don't resolve user names
        -N, --symbolic           resolve hardware names
        -e, --extend             display other/more information
        -p, --programs           display PID/Program name for sockets
        -o, --timers             display timers
        -c, --continuous         continuous listing

        -l, --listening          display listening server sockets
        -a, --all                display all sockets (default: connected)
        -F, --fib                display Forwarding Information Base (default)
        -C, --cache              display routing cache instead of FIB
        -Z, --context            display SELinux security context for sockets

  <Socket>={-t|--tcp} {-u|--udp} {-U|--udplite} {-S|--sctp} {-w|--raw}
           {-x|--unix} --ax25 --ipx --netrom
```

#### 4.1 netstat输出结果分析

```bash
➜  ~ netstat
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 dockerMaster:ssh        192.168.137.1:63100     ESTABLISHED
tcp        0      0 dockerMaster:ssh        192.168.137.1:63125     ESTABLISHED
tcp6       0      0 192.168.137.129:8384    192.168.137.1:51278     ESTABLISHED
tcp6       0      0 192.168.137.129:8384    192.168.137.1:51859     ESTABLISHED
udp        0      0 0.0.0.0:bootpc          0.0.0.0:*
Active UNIX domain sockets (w/o servers)
Proto RefCnt Flags       Type       State         I-Node   Path
unix  2      [ ]         DGRAM                    25883    /run/systemd/shutdownd
unix  3      [ ]         DGRAM                    33       /run/systemd/notify
```

从整体上看，netstat的输出结果可以分为两个部分：

- Active Internet connections

> 称为有源TCP连接，其中"Recv-Q"和"Send-Q"指的是接收队列和发送队列。
这些数字一般都应该是0。如果不是则表示软件包正在队列中堆积。这种情况只能在非常少的情况见到。

- Active UNIX domain sockets

> 称为有源Unix域套接口(和网络套接字一样，但是只能用于本机通信，性能可以提高一倍)。
Proto显示连接使用的协议,RefCnt表示连接到本套接口上的进程号,Types显示套接口的类型,State显示套接口当前的状态,Path表示连接到套接口的其它进程使用的路径名。

#### 4.2 状态说明

|状态|说明|
|-----------|--------------|
|LISTEN|侦听来自远方的TCP端口的连接请求|
|SYN-SENT|再发送连接请求后等待匹配的连接请求（如果有大量这样的状态包，检查是否中招了）|
|SYN-RECEIVED|再收到和发送一个连接请求后等待对方对连接请求的确认（如有大量此状态，估计被flood攻击了）|
|ESTABLISHED|代表一个打开的连接|
|FIN-WAIT-1|等待远程TCP连接中断请求，或先前的连接中断请求的确认|
|FIN-WAIT-2|从远程TCP等待连接中断请求|
|CLOSE-WAIT|等待从本地用户发来的连接中断请求|
|CLOSING|等待远程TCP对连接中断的确认|
|LAST-ACK|等待原来的发向远程TCP的连接中断请求的确认（不是什么好东西，此项出现，检查是否被攻击）|
|TIME-WAIT|等待足够的时间以确保远程TCP接收到连接中断请求的确认|
|CLOSED|没有任何连接状态|

#### 5. 常用组合

#### 5.1 显示TCP连接信息

```bash
netstat -at
```

- `-t|--tcp`显示tcp连接
- `-u|--udp`显示udp连接

#### 5.2 显示监听中的TCP、UDP连接、进程号和进程名

```bash
➜  ~ netstat -lntup
```

- `-n, --numeric`禁用反向域名解析，加快查询速度
- `-p, --programs`显示连接`PID/Program name`

#### 5.3 显示路由信息

```bash
➜  ~ netstat -r
➜  ~ route -n
```
