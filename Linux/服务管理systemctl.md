#### 参考:
- [初识systemd-使用篇](https://blog.51cto.com/andyxu/2122109?source=dra)

> Linux操作系统的开机过程是这样的，即从BIOS开始，然后进入Boot Loader，
再加载系统内核，然后内核进行初始化，最后启动初始化进程。
初始化进程作为Linux系统的第一个进程，它需要完成Linux系统中相关的初始化工作，
为用户提供合适的工作环境。

systemd初始化进程服务采用了并发启动机制，开机速度得到了不小的提升。

### 1.systemctl命令
`systemd`对应的进程管理命令是`systemctl`

```
#启动redis服务
➜  ~ systemctl start redis
#停止redis服务
➜  ~ systemctl stop redis
#重启redis服务
➜  ~ systemctl restart redis
# 开机自动启动
➜  ~ systemctl enable redis
Created symlink from /etc/systemd/system/multi-user.target.wants/redis.service to /usr/lib/systemd/system/redis.service.
# 开机自动启动
➜  ~ systemctl disable redis
Removed symlink /etc/systemd/system/multi-user.target.wants/redis.service.
显示系统状态
systemctl status
#查看redis状态
➜  ~ systemctl status redis
● redis.service - Redis persistent key-value database
   Loaded: loaded (/usr/lib/systemd/system/redis.service; enabled; vendor preset: disabled)
  Drop-In: /etc/systemd/system/redis.service.d
           └─limit.conf
   Active: active (running) since 四 2019-06-27 19:25:10 CST; 9min ago
 Main PID: 19799 (redis-server)
   CGroup: /system.slice/redis.service
           └─19799 /usr/bin/redis-server 0.0.0.0:6379

6月 27 19:25:10 docker01 systemd[1]: Starting Redis persistent key-value database...
6月 27 19:25:10 docker01 systemd[1]: Started Redis persistent key-value database.
```
#### 查看redis的systemd配置
```
➜  ~ systemctl cat redis
# /usr/lib/systemd/system/redis.service
[Unit]
Description=Redis persistent key-value database
After=network.target
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/bin/redis-server /etc/redis.conf --supervised systemd
ExecStop=/usr/libexec/redis-shutdown
Type=notify
User=redis
Group=redis
RuntimeDirectory=redis
RuntimeDirectoryMode=0755

[Install]
WantedBy=multi-user.target


# /etc/systemd/system/redis.service.d/limit.conf
# If you need to change max open file limit
# for example, when you change maxclient in configuration
# you can change the LimitNOFILE value below
# see "man systemd.exec" for information

[Service]
LimitNOFILE=10240
```

#### 2.systemd的资源Unit
Systemd可以管理所有系统资源。不同的资源统称为Unit（单位），Unit一共分成12种。
```
Service unit：系统服务
Target unit：多个Unit构成的一个组
Device Unit：硬件设备
Mount Unit：文件系统的挂载点
Automount Unit：自动挂载点
Path Unit：文件或路径
Scope Unit：不是由Systemd启动的外部进程
Slice Unit：进程组
Snapshot Unit：Systemd快照，可以切回某个快照
Socket Unit：进程间通信的socket
Swap Unit：swap文件
Timer Unit：定时器
```

systemd的Unit放在目录
- `/usr/lib/systemd/system`(Centos)
- `/etc/systemd/system`(Ubuntu)
```
➜  ~ ls /usr/lib/systemd/system/redis.service
/usr/lib/systemd/system/redis.service
```
#### 3.1 Unit配置文件
```
[Unit]
Description=Redis persistent key-value database
After=network.target
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/bin/redis-server /etc/redis.conf --supervised systemd
ExecStop=/usr/libexec/redis-shutdown
Type=notify
User=redis
Group=redis
RuntimeDirectory=redis
RuntimeDirectoryMode=0755

[Install]
WantedBy=multi-user.target
```
#### 3.2 [Unit]区块配置
```
Description：简单描述
Documentation：服务的启动文件和配置文件
Requires：当前Unit依赖的其他Unit，如果它们没有运行，当前Unit会启动失败
Wants：与当前Unit配合的其他Unit，如果它们没有运行，不影响当前Unit的启动
BindsTo：与Requires类似，它指定的Unit如果退出，会导致当前Unit停止运行
Before：如果该字段指定的Unit也要启动，那么必须在当前Unit之后启动
After：如果该字段指定的Unit也要启动，那么必须在当前Unit之前启动
Conflicts：这里指定的Unit不能与当前Unit同时运行
Condition...：当前Unit运行必须满足的条件，否则不会运行
Assert...：当前Unit运行必须满足的条件，否则会报启动失败
```
#### 3.3 [Service]区块配置
```
Type：定义启动时的进程行为，它有以下几种值。
Type=simple：默认值，执行ExecStart指定的命令，启动主进程
Type=forking：以fork方式从父进程创建子进程，之后父进程会退出，子进程成为主进程
Type=oneshot：一次性进程，Systemd会等当前服务退出，再继续往下执行
Type=dbus：当前服务通过D-Bus启动
Type=notify：当前服务启动完毕，会通知Systemd，再继续往下执行
Type=idle：若有其他任务，则其他任务执行完毕，当前服务才会运行
ExecStart：启动当前服务的命令
ExecStartPre：启动当前服务之前执行的命令
ExecStartPost：启动当前服务之后执行的命令
ExecReload：重启当前服务时执行的命令
ExecStop：停止当前服务时执行的命令
ExecStopPost：停止当其服务之后执行的命令
RestartSec：自动重启当前服务间隔的秒数
Restart：定义何种情况Systemd会自动重启当前服务，可能的值包括always（总是重启）、on-success、on-failure、on-abnormal、on-abort、on-watchdog
TimeoutSec：定义Systemd停止当前服务之前等待的秒数
Environment：指定环境变量
```
#### 3.4 [Install]区块配置
```
WantedBy：它的值是一个或多个Target，当前Unit激活时（enable）时，符号链接会放入/etc/systemd/system目录下面以Target名+.wants后缀构成的子目录中
RequiredBy：它的值是一个或多个Target，当前Unit激活时，符号链接会放入/etc/systemd/system目录下面以Target名+.required后缀构成的子目录中
Alias：当前Unit可用于启动的别名
Also：当前Unit激活（enable）时，会被同时激活的其他Unit
```
