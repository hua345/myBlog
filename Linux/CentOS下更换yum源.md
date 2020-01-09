# 首先进入yum源配置目录

```bash
cd /etc/yum.repos.d
```

备份系统自带的yum源

```bash
mv CentOS-Base.repo CentOS-Base.repo.bk
```

根据 [wiki.ubuntu.org.cn/源列表](http://wiki.ubuntu.org.cn/%E6%BA%90%E5%88%97%E8%A1%A8) 的镜像地址列表,找一个喜欢的镜像源。
[http://mirrors.aliyun.com/](http://mirrors.aliyun.com/)

[http://mirrors.aliyun.com/help/centos](http://mirrors.aliyun.com/help/centos)
下载新的CentOS-Base.repo

```bash
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
```

```bash
yum clean all
yum makecache   #生成缓存
yum update #升级软件
```

## 安装epel包

yum更换源后,发现redis都下不了
这是因为缺少了扩展包 EPEL(Extra Packages for Enterprise Linux),可以用 yum repolist 命令检查下。

```bash
mv /etc/yum.repos.d/epel.repo /etc/yum.repos.d/epel.repo.backup
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
```

repolist检查下：

```bash
[root@dev4svn /]# yum repolist
Loaded plugins: fastestmirror, refresh-packagekit, security
Loading mirror speeds from cached hostfile
 * base: mirrors.aliyun.com
 * epel: mirror01.idc.hinet.net
 * extras: mirrors.aliyun.com
 * updates: mirrors.aliyun.com
repo id           reponame 
base              CentOS-6 - Base - mirrors.aliyun.com
epel              Extra Packages for Enterprise Linux 6 - i386
extras            CentOS-6 - Extras - mirrors.aliyun.com
updates           CentOS-6 - Updates - mirrors.aliyun.com
repolist: 15,572
```

有Extra Packages for Enterprise Linux 6 - i386 表示EPEL安装好了

```bash
[root@dev4svn /]# find / -name "redis*"
/etc/yum.repos.d/redis-2.8.19-2.el7.x86_64.rpm
/etc/redis.conf
/etc/logrotate.d/redis
/etc/rc.d/init.d/redis
/usr/share/doc/redis-2.4.10
/usr/bin/redis-benchmark
/usr/bin/redis-check-dump
/usr/bin/redis-cli
/usr/bin/redis-check-aof
/usr/sbin/redis-server
/var/run/redis
/var/log/redis
/var/lib/redis
```

测试一下redis

```bash
reids-server /etc/redis.conf
redis-benchmark -h localhost -p 6379 -c 100 -n 100000
#100个并发连接，100000个请求，检测host为localhost 端口为6379的redis服务器性能
```

### RedHat使用CentOS源

删除redhat原有的yum

```bash
rpm -aq|grep yum|xargs rpm -e --nodeps
```

下载CentOS的yum安装文件

```bash
wget http://mirrors.aliyun.com/centos/6/os/x86_64/Packages/python-iniparse-0.3.1-2.1.el6.noarch.rpm
wget http://mirrors.aliyun.com/centos/6/os/x86_64/Packages/yum-metadata-parser-1.1.2-16.el6.x86_64.rpm 
wget http://mirrors.aliyun.com/centos/6/os/x86_64/Packages/yum-plugin-fastestmirror-1.1.30-30.el6.noarch.rpm
wget http://mirrors.aliyun.com/centos/6/os/x86_64/Packages/yum-3.2.29-69.el6.centos.noarch.rpm
```

安装CentOS的yum

```bash
rpm -ivh python-iniparse-0.3.1-2.1.el6.noarch.rpm
rpm -ivh yum-metadata-parser-1.1.2-16.el6.x86_64.rpm
rpm -ivh yum-plugin-fastestmirror-1.1.30-30.el6.noarch.rpm  yum-3.2.29-69.el6.centos.noarch.rpm
#最后两个包必需同时安装，否则会相互依赖
```

### 更新yum源文件

```bash
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-6.repo
cd /etc/yum.repos.d
cp rhel-source.repo rhel-source.repo.back
vi rhel-source.repo
```

把文件里面的$releasever全部替换为版本号，即6 最后保存。

```bash
# CentOS-Base.repo
#
# The mirror system uses the connecting IP address of the client and the
# update status of each mirror to pick mirrors that are updated to and
# geographically close to the client.  You should use this for CentOS updates
# unless you are manually picking other mirrors.
#
# If the mirrorlist= does not work for you, as a fall back you can try the 
# remarked out baseurl= line instead.
#
#

[base]
name=CentOS-6 - Base - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/6/os/$basearch/
        http://mirrors.aliyuncs.com/centos/6/os/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=6&arch=$basearch&repo=os
gpgcheck=1
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-6
 
#released updates 
[updates]
name=CentOS-$releasever - Updates - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/6/updates/$basearch/
        http://mirrors.aliyuncs.com/centos/6/updates/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=6&arch=$basearch&repo=updates
gpgcheck=1
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-6
 
#additional packages that may be useful
[extras]
name=CentOS-$releasever - Extras - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/6/extras/$basearch/
        http://mirrors.aliyuncs.com/centos/6/extras/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=6&arch=$basearch&repo=extras
gpgcheck=1
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-6
 
#additional packages that extend functionality of existing packages
[centosplus]
name=CentOS-6 - Plus - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/6/centosplus/$basearch/
        http://mirrors.aliyuncs.com/centos/6/centosplus/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=6&arch=$basearch&repo=centosplus
gpgcheck=1
enabled=0
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-6
 
#contrib - packages by Centos Users
[contrib]
name=CentOS-6 - Contrib - mirrors.aliyun.com
failovermethod=priority
baseurl=http://mirrors.aliyun.com/centos/6/contrib/$basearch/
        http://mirrors.aliyuncs.com/centos/6/contrib/$basearch/
#mirrorlist=http://mirrorlist.centos.org/?release=6&arch=$basearch&repo=contrib
gpgcheck=1
enabled=0
gpgkey=http://mirrors.aliyun.com/centos/RPM-GPG-KEY-CentOS-6
```

###更新yum源
```
yum update
rpm -ivh http://mirrors.aliyun.com/epel/6Server/i386/epel-release-6-8.noarch.rpm
```
