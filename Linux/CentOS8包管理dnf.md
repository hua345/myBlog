# 更新yum源

CentOS 8更改了软件包的安装程序，取消了`yum`的配置方法，改而使用了`dnf`作为安装程序。

centos 8 默认是会读取centos.org的mirrorlist的，所以一般来说是不需要配置镜像的。
如果你的网络访问centos.org的mirrorlist有问题，可能才需要另外配置镜像

```bash
cd /etc/yum.repos.d
# 备份
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
# CentOS 8
curl -o /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-8.repo

sed -i 's/mirrorlist=/#mirrorlist=/g' CentOS-Base.repo CentOS-AppStream.repo CentOS-Extras.repo
sed -i 's/#baseurl=/baseurl=/g' CentOS-Base.repo CentOS-AppStream.repo CentOS-Extras.repo
sed -i 's/http:\/\/mirror.centos.org/https:\/\/mirrors.aliyun.com/g' CentOS-Base.repo CentOS-AppStream.repo CentOS-Extras.repo
```

## dnf包管理

```bash
# 清除所有的缓存文件
dnf clean all

# 制作元数据缓存
dnf makecache

# 查找提供指定内容的软件包
dnf provides mysql
```
