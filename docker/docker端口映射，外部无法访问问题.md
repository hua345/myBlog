# 查看环境信息

## 查看端口占用情况

```bash
➜  ~ netstat -nltup
tcp6       0      0 :::6379                 :::*                    LISTEN      15442/docker-proxy

➜  ~ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
c56872966046        my/redis:v5.0.5     "redis-server /etc/r…"   4 seconds ago       Up 2 seconds        0.0.0.0:6379->6379/tcp   redis
```

## 查看 iptales 端口映射

```bash
➜  ~ iptables -n -L

Chain INPUT (policy ACCEPT)
Chain FORWARD (policy DROP)
Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
OUTPUT_direct  all  --  0.0.0.0/0            0.0.0.0/0

Chain DOCKER (1 references)
target     prot opt source               destination
ACCEPT     tcp  --  0.0.0.0/0            172.17.0.2           tcp dpt:6379
```

## 查看防火墙状态

```bash
➜  ~ systemctl status iptables
● iptables.service - IPv4 firewall with iptables
   Loaded: loaded (/usr/lib/systemd/system/iptables.service; disabled; vendor preset: disabled)
   Active: inactive (dead)

➜  ~ systemctl status iptables
● iptables.service - IPv4 firewall with iptables
   Loaded: loaded (/usr/lib/systemd/system/iptables.service; disabled; vendor preset: disabled)
   Active: active (exited) since 六 2019-07-27 15:39:53 CST; 20s ago
  Process: 6104 ExecStart=/usr/libexec/iptables/iptables.init start (code=exited, status=0/SUCCESS)
 Main PID: 6104 (code=exited, status=0/SUCCESS)

7月 27 15:39:53 consul01 systemd[1]: Starting IPv4 firewall with iptables...
7月 27 15:39:53 consul01 iptables.init[6104]: iptables: Applying firewall rules: [  确定  ]
7月 27 15:39:53 consul01 systemd[1]: Started IPv4 firewall with iptables.
```

## 检查 ip 转发

```bash
➜  ~ sysctl net.ipv4.ip_forward
net.ipv4.ip_forward = 1
```
