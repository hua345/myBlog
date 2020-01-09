#### 1.证书主要的文件类型

- PEM – Openssl使用 PEM(Privacy Enhanced Mail)格式来存放各种信息,它是 openssl 默认采用的信息存放方式。
- CSR － 证书请求文件(Certificate Signing Request)。生成 X509 数字证书前,一般先由用户提交证书申请文件,然后由 CA 来签发证书。
- CRT － 证书文件。可以是PEM格式。
- KEY 一般指PEM格式的私钥文件。

#### openssl.cnf位置

- /usr/local/openssl/ssl/openssl.cnf

(用的是git自带的openssl在bin目录中，配置文件openssl.cnf在ssl目录中,openssl.cnf参照[openssl生成证书 ](openssl生成证书.md) )

#### 2.生成证书

#### 2.1 生成服务器端的私钥(key文件)

```bash
[root@dockerMaster ~]# openssl genrsa -des3 -out myhost.key 2048
Generating RSA private key, 2048 bit long modulus (2 primes)
........+++++
.........................................................+++++
e is 65537 (0x010001)
Enter pass phrase for myhost.key:
Verifying - Enter pass phrase for myhost.key:
```

#### 2.2 生成Certificate Signing Request（CSR）

```bash
[root@dockerMaster ~]# openssl req -new -key myhost.key -out myhost.csr
Enter pass phrase for myhost.key:
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:CN
State or Province Name (full name) [Some-State]:GuangDong
Locality Name (eg, city) []:ShenZhen
Organization Name (eg, company) [Internet Widgits Pty Ltd]:FangFang
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:fangfang520.cn
Email Address []:2290910211@qq.com

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
```

#### 2.3 生成浏览器浏览网页时不需要输入密码的密钥

```bash
[root@dockerMaster ~]# openssl rsa -in myhost.key -out myhost-nopwd.key
Enter pass phrase for myhost.key:
writing RSA key
```

#### 2.4 生成自签名的证书

```bash
[root@dockerMaster ~]# openssl req -new -x509 -in myhost.csr -key myhost-nopwd.key -out myhost.crt -days 3650
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:CN
State or Province Name (full name) [Some-State]:GuangDong
Locality Name (eg, city) []:ShenZhen
Organization Name (eg, company) [Internet Widgits Pty Ltd]:FangFang
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:fangfang520.cn
Email Address []:2290910211@qq.com
```

#### 3. Nginx配置Https

Web服务器需要把`myhost.crt`发送给浏览器验证，然后用`myhost-nopass.key`解密浏览器发送的数据。
在需要Https的server模块中配置

```bash
server {
    listen  443;
    server_name  127.0.0.1  localhost;
    ssl on;
    ssl_certificate     D:/nginx/ssl/myhost.crt;
    ssl_certificate_key D:/nginx/myhost-nopwd.key;
}
```
