# rhel8与7的区别

在rhel7上，同时支持`network.service`和`NetworkManager.service`（简称NM）。默认情况下，这2个服务都有开启，但许多人都会将NM禁用掉。

在rhel8上，已废弃`network.service`，因此只能通过`NM`进行网络配置，包括动态ip和静态ip。换言之，在rhel8上，必须开启NM，否则无法使用网络。

rhel8依然支持`network.service`，只是默认没安装

## NetworkManager介绍

`NetworkManager`是2004年Red Hat启动的项目，旨在能够让Linux用户更轻松地处理现代网络需求，尤其是无线网络，能自动发现网卡并配置ip地址。

类似在手机上同时开启wifi和蜂窝网络，自动探测可用网络并连接，无需手动切换。

## 为什么要用NM

- 工具齐全：命令行、文本界面、图形界面、web
- 广纳天地：纳管各种网络，有线、无线、物理、虚拟
- 参数丰富：多达200多项配置参数（包括ethtool参数）

## 查看帮助

```bash
[root@db ~]# nmcli -h
用法：nmcli [选项] OBJECT

选项：
  -o[verview]                                    概览模式（隐藏默认值）
  -t[erse]                                       简洁输出
  -p[retty]                                      整齐输出
  -m[ode] tabular|multiline                      输出模式
  -c[olors] auto|yes|no                          是否在输出中使用颜色
  -f[ields] |all|common       指定要输出的字段
  -g[et-values] |all|common   -m tabular -t -f 的快捷方式
  -e[scape] yes|no                               在值中转义列分隔符
  -a[sk]                                         询问缺少的参数
  -s[how-secrets]                                允许显示密码
  -w[ait]                                    为完成的操作设置超时等待时间
  -v[ersion]                                     显示程序版本
  -h[elp]                                        输出此帮助

对象：
  g[eneral]       网络管理器（NetworkManager）的常规状态和操作
  n[etworking]    整体联网控制
  r[adio]         网络管理器无线电开关
  c[onnection]    网络管理器的连接
  d[evice]        由网络管理器管理的设备
  a[gent]         网络管理器的密钥（secret）代理或 polkit 代理
  m[onitor]       监视网络管理器更改
```

## nmcli命令

```bash
# 查看网络（类似于ifconfig、ip addr）
[root@db ~]# nmcli
ens33: 已连接 to ens33
        "Intel 82545EM"
        ethernet (e1000), 00:0C:29:CF:94:EB, 硬件, mtu 1500
        ip4 默认
        inet4 192.168.137.128/24
        route4 192.168.138.2/32
        route4 192.168.137.0/24
        route4 0.0.0.0/0
        inet6 fe80::85df:5c3e:e60:b851/64
        route6 fe80::/64
# 启动网卡
[root@db yum.repos.d]# nmcli c up ens33
连接已成功激活（D-Bus 活动路径：/org/freedesktop/NetworkManager/ActiveConnection/2）

# 查看connection列表
[root@db yum.repos.d]# nmcli c show
NAME   UUID                                  TYPE      DEVICE
ens33  5c15e95b-f0ce-40bb-9df8-ac56706633d5  ethernet  ens33

# 立即生效connection
nmcli c up ens33
nmcli d reapply ens33
nmcli d connect ens33

# 查看connection详细信息
nmcli c show ens33

# 查看device列表
[root@db yum.repos.d]# nmcli d
DEVICE  TYPE      STATE   CONNECTION
ens33   ethernet  已连接  ens33
lo      loopback  未托管  --


# 查看所有device详细信息
nmcli d show

# 查看NM纳管状态
[root@db yum.repos.d]# nmcli n
enabled

# 开启NM纳管
nmcli n on

# 监听事件
nmcli m

# 查看NM本身状态
nmcli
```
