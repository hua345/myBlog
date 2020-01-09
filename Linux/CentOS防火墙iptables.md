# 参考:

- [iptables 详解](https://www.cnblogs.com/davidwang456/p/3540837.html)

## iptables 提供了哪些表

| table  | 说明                                                                           |
| ------ | ------------------------------------------------------------------------------ |
| filter | 主要和主机自身有关，主要负责防火墙功能 过滤本机流入流出的数据包是默认使用的表; |
| nat    | 负责进行网络地址转换，内核模块 iptable_nat                                     |
| mangle | 拆解报文，进行修改，重新封装，内核模块 iptable_mangle                          |
| raw    | 关闭 nat 表上启用的连接追踪机制，内核模块 iptable_raw                          |

## iptables 链

| chain   | 说明                                                              |
| ------- | ----------------------------------------------------------------- |
| input   | 负责过滤所有目标地址是本机地址的数据包，就是过滤进入主机的数据包; |
| forward | 负责转发流经主机但不进入本机的数据包，和 NAT 关系很大;            |
| output  | 负责处理源地址的数据包，就是对本机发出的数据包;                   |

## iptables 处理动作

| target     | 说明                                                                 |
| ---------- | -------------------------------------------------------------------- |
| ACCEPT     | 允许数据包通过。                                                     |
| DROP       | 直接丢弃数据包。不回应任何信息，客户端只有当该链接超时后才会有反应。 |
| REJECT     | 拒绝数据包。会给客户端发送一个响应的信息 。                          |
| SNAT       | 源 NAT，解决私网用户用同一个公网 IP 上网的问题。                     |
| MASQUERADE | 是 SNAT 的一种特殊形式，适用于动态的、临时会变的 IP 上。             |
| DNAT       | 目的 NAT，解决私网服务端，接收公网请求的问题。                       |
| REDIRECT   | 在本机做端口映射。                                                   |
| LOG        | 在 /etc/log/messages 中留下记录，但并不对数据包进行任何操作。        |

## 查看帮助

```bash
iptables -h
 Usage: iptables -[ACD] chain rule-specification [options]
       iptables -I chain [rulenum] rule-specification [options]
       iptables -R chain rulenum rule-specification [options]
       iptables -D chain rulenum [options]
       iptables -P chain target [options]

Commands:
Either long or short options are allowed.
  --append  -A chain            Append to chain
  --check   -C chain            Check for the existence of a rule
  --delete  -D chain            Delete matching rule from chain
  --list    -L [chain]          List the rules in a chain or all chains
  --flush   -F [chain]          Delete all rules in  chain or all chains
  --new     -N chain            Create a new user-defined chain
  --policy  -P chain target     Change policy on chain to target
```

## iptables 常用语法

## 查看规则

```bash
iptables -n -L
#默认查看的是filter表
iptables -t filter -nvL
```

### 查看特定的链

```bash
iptables -nvL INPUT
```

#### 清空 fllter 表所有链

```bash
iptables -F
```

#### 保存 iptables 配置

```bash
service iptables save
#重启iptables
systemctl restart iptables
```

#### 设置默认链策略

默认的链策略是`ACCEPT`，可以将它们设置只接受允许规则。

```bash
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT DROP
```

#### 允许所有 SSH 的连接请求

```bash
#允许本地回环接口(即运行本机访问本机)
iptables -A INPUT -s 127.0.0.1 -d 127.0.0.1 -j ACCEPT

 #允许已建立的或相关连的通行
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

#允许访问ssh端口
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT

#允许访问http端口
iptables -A INPUT -p tcp --dport 80 -j ACCEPT

iptables -A OUTPUT -p tcp --sport 80 -j ACCEPT

iptables -A INPUT -p tcp --dport 6379 -j ACCEPT

iptables -A OUTPUT -p tcp --sport 6379 -j ACCEPT

#允许访问https端口
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

iptables -A OUTPUT -p tcp --sport 443 -j ACCEPT
```

#### 允许外部主机 ping 内部主机

```bash
iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT

iptables -A OUTPUT -p icmp --icmp-type echo-reply -j ACCEPT
```

#### 允许内部主机 ping 外部主机

```bash
iptables -A OUTPUT -p icmp --icmp-type echo-request -j ACCEPT
iptables -A INPUT -p icmp --icmp-type echo-reply -j ACCEPT
```

#### 阻止指定 IP 地址

```bash
iptables -A INPUT -s x.x.x.x -j DROP
#阻止来自IP地址x.x.x.x tcp的包
iptables -A INPUT -s x.x.x.x p tcp -j DROP
```
