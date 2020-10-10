# centOS8安装docker-ce

redhat做了自己的容器解决方案，因此在centos8中移除了对docker的支持

先装好高版本的`containerd.io`再装`docker-ce`

```bash
dnf config-manager --add-repo=http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
wget http://mirrors.aliyun.com/docker-ce/linux/centos/8/x86_64/stable/Packages/containerd.io-1.3.7-3.1.el8.x86_64.rpm
dnf install containerd.io-1.3.7-3.1.el8.x86_64.rpm
dnf install docker-ce

systemctl enable docker.service
systemctl start docker.service
docker version
```

由于`centos8` 将`iptables`替换为`nftables`，docker存在兼容性问题，会出现DNS无法解析的bug。你可以busybox容器校验

```bash
docker run busybox ping baidu.com

Unable to find image 'busybox:latest' locally
latest: Pulling from library/busybox
df8698476c65: Pull complete
Digest: sha256:d366a4665ab44f0648d7a00ae3fae139d55e32f9712c67accd604bb55df9d05a
Status: Downloaded newer image for busybox:latest
nslookup: write to '172.16.8.8': No route to host
nslookup: write to '192.168.1.1': No route to host
nslookup: write to '8.8.8.8': No route to host
;; connection timed out; no servers could be reached
```

## 让firewalld使用iptables

```bash
#修改/etc/firewalld/firewalld.conf
# FirewallBackend
# Selects the firewall backend implementation.
# Choices are:
#       - nftables (default)
#       - iptables (iptables, ip6tables, ebtables and ipset)
FirewallBackend=iptables

systemctl restart firewalld.service
```

[https://github.com/docker/for-linux/issues/957#issuecomment-627166787](https://github.com/docker/for-linux/issues/957#issuecomment-627166787)