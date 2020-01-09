# firewall 简述

- `Centos7`默认的防火墙是`firewall`，替代了以前的`iptables`
- `firewall`使用更加方便、功能也更加强大一些

## Firewalld 与 iptables 对比

- `firewalld` 是 `iptables` 的前端控制器
- `iptables` 静态防火墙 任一策略变更需要 reload 所有策略，丢失现有链接
- `firewalld` 动态防火墙 任一策略变更不需要 reload 所有策略 将变更部分保存到 iptables,不丢失现有链接
- `firewalld` 提供一个 daemon 和 service 底层使用 `iptables`
- 都是基于内核的 Netfilter

如果想使用`iptables`配置防火墙规则，要先安装`iptables`并禁用`firewalld`

## 基本启动命令

```bash
# 查看firewalld的状态
systemctl status firewalld

systemctl start firewalld
systemctl stop firewalld
# firewalld开机启动
systemctl enable firewalld
# 取消firewalld开机启动
systemctl disable firewalld
```

## 常用命令

### 查看

```bash
# 查看激活的域
firewall-cmd --get-active-zones
# 查看开放的端口
firewall-cmd --zone=public --list-ports
# 查看添加的规则
firewall-cmd --zone=public --list-rich-rules
```

### 添加端口

```bash
# 开放单个端口
# --permanent 永久生效，没有此参数重启后失效
firewall-cmd --zone=public --add-port=80/tcp --permanent

# 开放端口范围
# --permanent 永久生效，没有此参数重启后失效
firewall-cmd --zone=public --add-port=8388-8389/tcp --permanent

#  同服务器端口转发 80端口转发到8081端口
firewall-cmd --zone="public" --add-forward-port=port=80:proto=tcp:toport=8081

# 不同服务器端口转发，要先开启 masquerade
firewall-cmd --zone=public --add-masquerade

# 不同服务器端口转发，转发到192.168.137.128的8080端口
firewall-cmd --zone="public" --add-forward-port=port=80:proto=tcp:toport=8080:toaddr=192.168.137.128

# 对 147.152.139.197 开放10000端口
firewall-cmd --permanent --zone=public --add-rich-rule='
        rule family="ipv4"
        source address="147.152.139.197/32"
        port protocol="tcp" port="10000" accept'

# 拒绝端口：
firewall-cmd --permanent --zone=public --add-rich-rule='
              rule family="ipv4"
              source address="47.52.39.197/32"
              port protocol="tcp" port="10000" reject'

# 开放全部端口给IP
firewall-cmd --permanent --zone=public --add-rich-rule='
              rule family="ipv4"
              source address="192.168.0.1/32" accept';

# 开放全部端口给网段
firewall-cmd --permanent --zone=public --add-rich-rule='
              rule family="ipv4"
              source address="192.168.0.0/16" accept';
```

### 添加服务

```bash
# 查看全部支持的服务
firewall-cmd --get-service

# 查看开放的服务
firewall-cmd --list-service

# 添加服务,添加https
# --permanent 永久生效，没有此参数重启后失效
firewall-cmd --add-service=https --permanent
```

### 移除端口

```bash
# 移除添加的端口
# --permanent 永久生效，没有此参数重启后失效
firewall-cmd --zone=public --remove-port=80/tcp --permanent
```

### 重载配置

```bash
# 重新载入防火墙配置，当前连接不中断
firewall-cmd --reload
# 重新载入防火墙配置，当前连接中断
firewall-cmd --complete-reload
```
