ssh（secure shell）是一种对数据进行加密安全传输的协议。利用ssh工具可以非常方便的登录远程提供有ssh服务的主机，也可以很方便的进行文件传输。利用 ssh tunnel 可以进行端口转发（port forwarding）, 它在ssh连接上建立一个加密的通道。创建了ssh tunnel之后，可以突破一些网络的限制访问不能直接访问的资源。
ssh tunnel分为三种，本地（L），远程（R）和动态（D）。
比如sshserver上服务监听在127.0.0.1:80上，并没有暴露80端口给网络，可以通过隧道转发到本机端口进行访问．
```bash
man ssh 
#-L [bind_address:]port:host:hostport 
#Specifies that the given port on the local (client) host is to be forwarded to the given host and port on the remote side.

#-R  [bind_address:]port:host:hostport
#Specifies that the given port on the remote (server) host is to be forwarded to the given host and port on the local side. 

#-N      Do not execute a remote command.  This is useful for just forwarding ports (protocol version 2 only).
#-T      Disable pseudo-terminal allocation.
#-N, -T这个两个参数可以放在一起用，代表这个SSH连接只用来传数据，不执行远程操作。

＃-f  让ssh后台运行
```
![这里写图片描述](http://img.blog.csdn.net/20151112103941185)
![这里写图片描述](http://img.blog.csdn.net/20151112103954029)

### 可能应用的场景
#### 本地端口映射 -L
比如ssh服务器host1上服务监听在127.0.0.1:80上，并没有暴露80端口给网络，可以通过隧道转发到本机端口进行访问．
```
ssh -NfL 9000:localhost:80  host1　＃默认绑定地址是127.0.0.1
ssh -NfL 0.0.0.0:9000:localhost:80  host1　＃监听0.0.0.0,将端口暴露给网络
这样一来，我们只要连接本地的9000端口，就等于连上了host1本地的80端口。
```
#### 远程端口转发 -R
既然"本地端口转发"是指绑定本地端口的转发，那么"远程端口转发"（remote forwarding）当然是指绑定远程端口的转发。
比如在家里想访问到公司里面的电脑，由于都不是在同一个局域网中不能直接访问，需要一台外网服务器remoteHost
```
#在公司电脑上，将本地的ssh服务端口映射到远程机器的9022端口。
ssh -NfR 9022:localhost:22 remoteHost
#在家里登录外网服务器后，ssh连接公司电脑.
ssh -p 9022 localhost
```

#### 动态端口映射 -D
因为防火墙等因素本地机器不能访问某些资源，但是远程ssh主机可以访问。你可以从本地ssh到远程那台主机。这时你希望用远程主机做代理以方便本地的网络访问，因为最先介绍的本地端口映射只能对指明的个别网站进行访问。
```
ssh -NfD 9000 remoteHost
```
通过SSH建立的SOCKS服务器使用的是SOCKS5协议，在为应用程序设置SOCKS代理的时候要特别注意。
接着在浏览器上设置`Socket代理`：地址是`localhost`，端口是`9000`。从此以后，你的访问都是加密的了，而且走的是远程主机，IP变为了远程主机的IP，一些不能直接访问的资源通过这个代理可以访问。

### 参照：

- [SSH Tunnel (port forwarding) 的一些应用](http://blog.itpub.net/7734298/viewspace-680712/)
- [https://en.wikipedia.org/wiki/Tunneling_protocol](https://en.wikipedia.org/wiki/Tunneling_protocol)
- [SSH隧道技术简介](http://blog.chinaunix.net/uid-20761674-id-74962.html)
- [SSH原理与运用（二）：远程操作与端口转发](http://www.ruanyifeng.com/blog/2011/12/ssh_port_forwarding.html)
