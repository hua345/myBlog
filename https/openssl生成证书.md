> 安装Git命令行工具后带有openssl。

[openssl安装文档](安装openssl.md)
### 1.生成公钥私钥

#### 1.1 创建私钥
```
openssl genrsa -out private.pem 2048
```
#### 1.2根据私钥创建公钥
```
openssl rsa -in private.pem -pubout -out public.pem
```
#### 1.3生成证书

> 证书主要的文件类型和协议有: PEM、DER、PFX、JKS、KDB、CER、KEY、CSR、CRT、CRL 、OCSP、SCEP等。

PEM – Openssl使用 PEM(Privacy Enhanced Mail)格式来存放各种信息,它是 openssl 默认采用的信息存放方式。Openssl 中的 PEM 文件一般包含如下信息:

内容类型:表明本文件存放的是什么信息内容,它的形式为“——-BEGIN XXXX ——”,与结尾的“——END XXXX——”对应。
头信息:表明数据是如果被处理后存放,openssl 中用的最多的是加密信息,比如加密算法以及初始化向量 iv。
信息体:为 BASE64 编码的数据。可以包括所有私钥（RSA 和 DSA）、公钥（RSA 和 DSA）和 (x509) 证书。它存储用 Base64 编码的 DER 格式数据，用 ascii 报头包围，因此适合系统之间的文本模式传输。
使用PEM格式存储的证书：
```
—–BEGIN CERTIFICATE—–
MIICJjCCAdCgAwIBAgIBITANBgkqhkiG9w0BAQQFADCBqTELMAkGA1UEBhMCVVMx
………
1p8h5vkHVbMu1frD1UgGnPlOO/K7Ig/KrsU=
—–END CERTIFICATE—–
使用PEM格式存储的私钥：
—–BEGIN RSA PRIVATE KEY—–
MIICJjCCAdCgAwIBAgIBITANBgkqhkiG9w0BAQQFADCBqTELMAkGA1UEBhMCVVMx
………
1p8h5vkHVbMu1frD1UgGnPlOO/K7Ig/KrsU=
—–END RSA PRIVATE KEY—–
使用PEM格式存储的证书请求文件：
—–BEGIN CERTIFICATE REQUEST—–
MIICJjCCAdCgAwIBAgIBITANBgkqhkiG9w0BAQQFADCBqTELMAkGA1UEBhMCVVMx
………
1p8h5vkHVbMu1frD1UgGnPlOO/K7Ig/KrsU=
—–END CERTIFICATE REQUEST—–
```
CSR － 证书请求文件(Certificate Signing Request)。生成 X509 数字证书前,一般先由用户提交证书申请文件,然后由 CA 来签发证书。大致过程如下(X509 证书申请的格式标准为 pkcs#10 和 rfc2314):

用户生成自己的公私钥对;
构造自己的证书申请文件,符合 PKCS#10 标准。该文件主要包括了用户信息、公钥以及一些可选的属性信息,并用自己的私钥给该内容签名;
用户将证书申请文件提交给 CA;
CA 验证签名,提取用户信息,并加上其他信息(比如颁发者等信息),用 CA 的私钥签发数字证书;
说 明:数字证书(如x.509)是将用户(或其他实体)身份与公钥绑定的信息载体。一个合法的数字证书不仅要符合 X509 格式规范,还必须有 CA 的签名。用户不仅有自己的数字证书,还必须有对应的私钥。X509v3 数字证书主要包含的内容有:证书版本、证书序列号、签名算法、颁发者信息、有效时间、持有者信息、公钥信息、颁发者 ID、持有者 ID 和扩展项。


CRT － 证书文件。可以是PEM格式。
KEY   － 一般指PEM格式的私钥文件。



#### 2.1 openssl配置文件
```
/usr/local/openssl/ssl/openssl.cnf
```
#### 2.2 For the CA policy
```
[ policy_match ]
countryName = match
stateOrProvinceName = match
organizationName = match
organizationalUnitName = optional
commonName = supplied
emailAddress = optional
```
“match”表示说明你填写的这一栏一定要和CA本身的证书里面的这一栏相同。supplied表示本栏必须，optional就表示本栏可以不填写。
```
[ CA_default ]
dir     = ./demoCA      # Where everything is kept.
new_certs_dir   = $dir/newcerts     # default place for new certs.
database    = $dir/index.txt    # database index file.
serial      = $dir/serial       # The current serial number
default_days    = 3650          # how long to certify for.
```
#### 2.3 创建demoCA文件夹
一个空的index.txt文件,一个初始值为01的`serial`文件，用来给下一个证书做系列号。
```
mkdir demoCA
mkdir demoCA/newcerts
touch demoCA/index.txt
echo "00" > demoCA/serial
```
### 3. 生成证书
#### 3.1 首先要生成服务器端的私钥(key文件):
```
[root@dockerMaster ~]# openssl genrsa -des3 -out server.key 2048
Generating RSA private key, 2048 bit long modulus
.............................+++
.......+++
e is 65537 (0x10001)
Enter pass phrase for server.key:
Verifying - Enter pass phrase for server.key:

```
`genras`表示生成RSA私有密钥文件，`-des3`表示用DES3加密该文件，2048是我们的key的长度。

#### 3.2 生成Certificate Signing Request（CSR）
```
[root@dockerMaster ~]# openssl req -new -key server.key -out server.csr
Enter pass phrase for server.key:
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

#### 3.3 生成根证书(Root Certificate)

> 我们需要一个证书来为自己颁发的证书签名，这个证书可从其他CA获取，或者是自签名的根证书。这里我们生成一个自签名的根证书。

```
[root@dockerMaster ~]# openssl genrsa -des3 -out ca.key 2048
Generating RSA private key, 2048 bit long modulus
.............................+++
.......+++
e is 65537 (0x10001)
Enter pass phrase for ca.key:
Verifying - Enter pass phrase for ca.key:

[root@dockerMaster ~]# openssl req -new -x509 -key ca.key -out ca.crt -days 3650
Enter pass phrase for ca.key:
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
- x509：本option将产生自签名的证书。

#### 3.4 用生成的ca指令为刚才生成的server.csr文件签名:
```
[root@dockerMaster ~]# openssl ca -in server.csr -out server.crt -cert ca.crt -keyfile ca.key
Using configuration from /usr/local/openssl/ssl/openssl.cnf
Enter pass phrase for ca.key:
Check that the request matches the signature
Signature ok
Certificate Details:
        Serial Number: 0 (0x0)
        Validity
            Not Before: May 10 07:33:56 2019 GMT
            Not After : May  9 07:33:56 2020 GMT
        Subject:
            countryName               = CN
            stateOrProvinceName       = GuangDong
            organizationName          = FangFang
            commonName                = fangfang520.cn
            emailAddress              = 2290910211@qq.com
        X509v3 extensions:
            X509v3 Basic Constraints:
                CA:FALSE
            Netscape Comment:
                OpenSSL Generated Certificate
            X509v3 Subject Key Identifier:
                48:6F:0B:18:7A:C4:2F:A1:4C:2F:B7:39:6B:79:9C:37:E2:BA:55:35
            X509v3 Authority Key Identifier:
                keyid:8C:F5:ED:0D:3B:23:E7:93:36:84:33:09:73:A2:AD:A0:50:9D:A6:AD

Certificate is to be certified until May  9 07:33:56 2020 GMT (365 days)
Sign the certificate? [y/n]:y


1 out of 1 certificate requests certified, commit? [y/n]y
Write out database with 1 new entries
Data Base Updated
```

#### 3.6随机数生成
```
openssl dhparam -out dh512.pem 512
openssl dhparam -out dh1024.pem 1024
```
