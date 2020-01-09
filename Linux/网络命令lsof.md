#### 1.简介

> lsof(list open files)是一个列出当前系统打开文件的工具。
在linux环境下，任何事物都以文件的形式存在，通过文件不仅仅可以访问常规数据，还可以访问网络连接和硬件。
所以如传输控制协议 (TCP) 和用户数据报协议 (UDP) 套接字等，系统在后台都为该应用程序分配了一个文件描述符，
无论这个文件的本质如何，该文件描述符为应用程序与基础操作系统之间的交互提供了通用接口。

#### 2.参数说明

|参数|说明|
|-----|-----------|
|-i | select by IPv[46] address: [46][proto][@host|addr][:svc_list|port_list] |
|-u|列出某个用户打开的文件信息|
|-t |仅获取进程ID|
|-U |列出Unix套接字|
|-c |列出某个程序所打开的文件信息|

#### 3.1查看谁正在使用某个文件

```bash
lsof  /filepath/file
```

#### 3.2列出某个程序所打开的文件信息

```bash
lsof -c syncthing
```

#### 3.3通过某个进程号显示该进行打开的文件

```bash
lsof -p PID
```

#### 3.4列出所有网络连接

```bash
lsof -i
```

#### 3.5列出所有tcp网络连接信息

```bash
lsof  -i tcp
```

#### 3.6列出谁在使用某个端口

```bash
lsof -i :80
```

#### 3.7找出监听端口

```bash
lsof  -i -s TCP:LISTEN
lsof  -i |grep LISTEN
```

#### 3.8找出已建立的连接

你也可以显示任何已经连接的连接。

```bash
lsof  -i -s TCP:ESTABLISHED
lsof  -i | grep ESTABLISHED
```

#### 3.9使用@host来显示指定到指定主机的连接

```bash
➜  ~ lsof  -i @192.168.137.1
COMMAND     PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
sshd      11570 root    3u  IPv4  71774      0t0  TCP dockerMaster:ssh->192.168.137.1:63100 (ESTABLISHED)
sshd      11609 root    3u  IPv4  70751      0t0  TCP dockerMaster:ssh->192.168.137.1:63125 (ESTABLISHED)
syncthing 17059 root   11u  IPv6 137384      0t0  TCP dockerMaster:8384->192.168.137.1:53557 (ESTABLISHED)
syncthing 17059 root   13u  IPv6 139289      0t0  TCP dockerMaster:8384->192.168.137.1:53653 (ESTABLISHED)
```

#### 3.10 列出某个用户打开的文件信息

```bash
lsof -u root
```
