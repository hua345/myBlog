#### 参考
- [快速签发 Let's Encrypt 证书指南](https://www.cnblogs.com/esofar/p/9291685.html)

> [Let's Encrypt](https://letsencrypt.org/) 是一个由非营利性组织 互联网安全研究小组（ISRG）提供的免费、自动化和开放的证书颁发机构（CA）。
> 简单的说，借助 Let's Encrypt 颁发的证书可以为我们的网站免费启用 HTTPS(SSL/TLS)。
> Let's Encrypt免费证书的签发/续签都是脚本自动化的，官方提供了几种证书的申请方式方法，[点击此处](https://letsencrypt.org/docs/client-options/) 快速浏览。
> 官方推荐使用 Certbot 客户端来签发证书
#### 环境
- 已经备案并且绑定公网IP的域名: www.fangfang520.cn
- 云服务器: CentOS
- 负载均衡: nginx
#### 安装certbot
```
wget https://dl.eff.org/certbot-auto
sudo mv certbot-auto /usr/local/bin/certbot-auto
sudo chown root /usr/local/bin/certbot-auto
sudo chmod 0755 /usr/local/bin/certbot-auto
```
#### 下载依赖包
```
wget http://nginx.org/packages/centos/7/x86_64/RPMS/nginx-1.16.0-1.el7.ngx.x86_64.rpm
#建立nginx的yum仓库
rpm -ivh nginx-1.16.0-1.el7.ngx.x86_64.rpm
#启动nginx服务
systemctl start nginx
```
#### 访问nginx
```
[root@LetsEncrypt ~]# curl 127.0.0.1:80
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>

```
#### 设置主机hosts
```
C:\Windows\System32\drivers\etc\hosts

192.168.137.134 helloencrypt.com
```
#### 在虚拟机上ping
```
[root@LetsEncrypt ~]# ping helloencrypt.com
PING helloencrypt.com.localdomain (192.168.137.134) 56(84) bytes of data.
64 bytes from LetsEncrypt (192.168.137.134): icmp_seq=1 ttl=64 time=0.063 ms
64 bytes from LetsEncrypt (192.168.137.134): icmp_seq=2 ttl=64 time=0.055 ms
```
```
[root@LetsEncrypt ~]# sudo /usr/local/bin/certbot-auto --nginx
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator nginx, Installer nginx
Enter email address (used for urgent renewal and security notices) (Enter 'c' to
cancel): 2290910211@qq.com

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Please read the Terms of Service at
https://letsencrypt.org/documents/LE-SA-v1.2-November-15-2017.pdf. You must
agree in order to register with the ACME server at
https://acme-v02.api.letsencrypt.org/directory
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(A)gree/(C)ancel: a

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Would you be willing to share your email address with the Electronic Frontier
Foundation, a founding partner of the Let's Encrypt project and the non-profit
organization that develops Certbot? We'd like to send you email about our work
encrypting the web, EFF news, campaigns, and ways to support digital freedom.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: y
No names were found in your configuration files. Please enter in your domain
name(s) (comma and/or space separated)  (Enter 'c' to cancel): helloEncrypt.com
Obtaining a new certificate
Performing the following challenges:
http-01 challenge for helloencrypt.com
Using default address 80 for authentication.
Waiting for verification...
Challenge failed for domain helloencrypt.com
http-01 challenge for helloencrypt.com
Cleaning up challenges
Some challenges have failed.

IMPORTANT NOTES:
 - The following errors were reported by the server:

   Domain: helloencrypt.com
   Type:   connection
   Detail: dns :: DNS problem: NXDOMAIN looking up A for
   helloencrypt.com

   To fix these errors, please make sure that your domain name was
   entered correctly and the DNS A/AAAA record(s) for that domain
   contain(s) the right IP address. Additionally, please check that
   your computer has a publicly routable IP address and that no
   firewalls are preventing the server from communicating with the
   client. If you're using the webroot plugin, you should also verify
   that you are serving files from the webroot path you provided.
 - Your account credentials have been saved in your Certbot
   configuration directory at /etc/letsencrypt. You should make a
   secure backup of this folder now. This configuration directory will
   also contain certificates and private keys obtained by Certbot so
   making regular backups of this folder is ideal.
```


```
sudo /usr/local/bin/certbot-auto --nginx certonly
```

####  Detail: dns :: DNS problem: NXDOMAIN looking up A for
```

```