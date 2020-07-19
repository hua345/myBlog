# 1. 安装 redis

````conf
# 下载redis
# https://redis.io/download

wget http://download.redis.io/releases/redis-6.0.5.tar.gz
tar -zvxf redis-6.0.5.tar.gz
cd redis-6.0.5
yum install gcc
# linux
make MALLOC=libc -j4
make install

➜  redis-server -v
Redis server v=6.0.5 sha=00000000:0 malloc=libc bits=64 build=bbfca0eb815accea
➜   redis-server
91442:C 15 Aug 2019 11:06:09.112 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
91442:C 15 Aug 2019 11:06:09.112 # Redis version=5.0.5, bits=64, commit=00000000, modified=0, pid=91442, just started
91442:C 15 Aug 2019 11:06:09.112 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
                _._
           _.-``__ ''-._
      _.-``    `.  `_.  ''-._           Redis 5.0.5 (00000000/0) 64 bit
  .-`` .-```.  ```\/    _.,_ ''-._
 (    '      ,       .-`  | `,    )     Running in standalone mode
 |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6379
 |    `-._   `._    /     _.-'    |     PID: 91442
  `-._    `-._  `-./  _.-'    _.-'
 |`-._`-._    `-.__.-'    _.-'_.-'|
 |    `-._`-._        _.-'_.-'    |           http://redis.io
  `-._    `-._`-.__.-'_.-'    _.-'
 |`-._`-._    `-.__.-'    _.-'_.-'|
 |    `-._`-._        _.-'_.-'    |
  `-._    `-._`-.__.-'_.-'    _.-'
      `-._    `-.__.-'    _.-'
          `-._        _.-'
              `-.__.-'

91442:M 15 Aug 2019 11:06:09.115 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
91442:M 15 Aug 2019 11:06:09.115 # Server initialized
````

## 查看帮助

```bash
➜  redis redis-server -h
Usage: ./redis-server [/path/to/redis.conf] [options]
       ./redis-server - (read config from stdin)
       ./redis-server -v or --version
       ./redis-server -h or --help
       ./redis-server --test-memory <megabytes>

Examples:
       ./redis-server (run the server with default conf)
       ./redis-server /etc/redis/6379.conf
       ./redis-server --port 7777
       ./redis-server --port 7777 --replicaof 127.0.0.1 8888
       ./redis-server /etc/myredis.conf --loglevel verbose

Sentinel mode:
       ./redis-server /etc/sentinel.conf --sentinel
```

## 2. 修改 redis 配置文件

```conf
# 绑定地址
bind 0.0.0.0
# By default Redis does not run as a daemon. Use 'yes' if you need it.
# Note that Redis will write a pid file in /var/run/redis.pid when daemonized.
# redis默认不是用守护进程的，如果需要更改，把daemonize no改成daemonize yes
daemonize yes
# Set the number of databases.
databases 16
# 当redis用守护进程运行的时候，它会写一个pid到 `/var/run/redis.pid` 文件里面
pidfile /var/run/redis_6379.pid
################################ SNAPSHOTTING  ################################
#
# Save the DB on disk:
#
#   save <seconds> <changes>
#
#   Will save the DB if both the given number of seconds and the given
#   number of write operations against the DB occurred.
#
#   In the example below the behaviour will be to save:
#   after 900 sec (15 min) if at least 1 key changed
#   after 300 sec (5 min) if at least 10 keys changed
#   after 60 sec if at least 10000 keys changed
#
#   Note: you can disable saving completely by commenting out all "save" lines.
#
#   It is also possible to remove all the previously configured save
#   points by adding a save directive with a single empty string argument
#   like in the following example:
#
#   save ""

save 900 1
save 300 10
save 60 10000
# The working directory.
#
# The DB will be written inside this directory, with the filename specified
# above using the 'dbfilename' configuration directive.
#
# The Append Only File will also be created inside this directory.
#
# Note that you must specify a directory here, not a file name.
dir ./
# If you run Redis from upstart or systemd, Redis can interact with your
# supervision tree. Options:
#   supervised no      - no supervision interaction
#   supervised upstart - signal upstart by putting Redis into SIGSTOP mode
#   supervised systemd - signal systemd by writing READY=1 to $NOTIFY_SOCKET
#   supervised auto    - detect upstart or systemd method based on
#                        UPSTART_JOB or NOTIFY_SOCKET environment variables
# Note: these supervision methods only signal "process is ready."
#       They do not enable continuous liveness pings back to your supervisor.
supervised no
```

### 5. 启动 redis

```bash
cp ~/redis-6.0.5/redis.conf ~/redis/redis.conf
redis-server ~/redis/redis.conf

# --permanent 永久生效，没有此参数重启后失效
firewall-cmd --zone=public --add-port=6379/tcp --permanent
# 重新载入防火墙配置，当前连接不中断
firewall-cmd --reload
# 查看开放的端口
firewall-cmd --zone=public --list-ports
```

### 6.加入 systemctl 服务

```bash
cp ~/redis/redis.conf /etc/redis.conf
vi /lib/systemd/system/redis.service
```

```conf
[Unit]
Description=Redis persistent key-value database
After=network.target
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/local/bin/redis-server /etc/redis.conf  --daemonize no
ExecStop=/usr/local/bin/redis-cli shutdown
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl start redis

```

#### 7. 检查是否启动成功

```bash
➜  netstat -nltup
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:3306            0.0.0.0:*               LISTEN      5466/mysqld
tcp        0      0 0.0.0.0:6379            0.0.0.0:*               LISTEN      92424/redis-server
```

Redis 有两种存储方式，默认是 snapshot 方式，实现方法是定时将内存的快照(snapshot)持久化到硬盘，这种方法缺点是持久化之后如果出现 crash 则会丢失一段数据。因此在完美主义者的推动下作者增加了 aof 方式。aof 即 append only mode，在写入内存数据的同时将操作命令保存到日志文件。

### 参考

- [Redis (一) 安装](http://blog.csdn.net/chenggong2dm/article/details/6100001)
- [https://github.com/antirez/redis](https://github.com/antirez/redis)
