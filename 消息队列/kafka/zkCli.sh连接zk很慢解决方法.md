# 参考

- [macOS 下，连接zookeeper等java软件加载较慢的解决方案](https://www.cnblogs.com/wgh0807/p/10920183.html)

卡顿主要是在获取主机地址时发生的：

```bash
java.net.InetAddress.getLocalHost ().getHostAddress();
```

## 获取本机名称

```bash
➜  ~ echo $HOSTNAME
consul01
```

## 修改/etc/hosts

```bash
vi /etc/hosts
```

## 将域名加入hosts中

```bash
127.0.0.1   localhost consul01
::1         localhost consul01
```
