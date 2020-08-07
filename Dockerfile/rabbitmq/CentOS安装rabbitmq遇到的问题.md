# 安装rabbitmq错误

## `ERROR: epmd error for host`

```log
journalctl -xe

loveFang rabbitmq-server[31103]: ERROR: epmd error for host loveFang: address (cannot connect to host/port)
```

```conf
# vi /etc/hosts

127.0.0.1   localhost loveFang localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost loveFang localhost.localdomain localhost6 localhost6.localdomain6
```

重启电脑
