### 什么是GPG
>要了解什么是GPG，就要先了解PGP。
1991年，程序员Phil Zimmermann为了避开政府监视，开发了加密软件PGP。这个软件非常好用，迅速流传开来，成了许多程序员的必备工具。但是，它是商业软件，不能自由使用。所以，自由软件基金会决定，开发一个PGP的替代品，取名为GnuPG。这就是GPG的由来。

### 生成GPG Key
```
mkdir ~/.gnupg  #GPG保存文件时需要
gpg --gen-key   #根据提示输入信息
```
### 查看生成的GPG key
```
gpg --list-keys         #公钥
gpg --list-secret-keys  #私钥
```
```
c:/Users/***/.gnupg\pubring.gpg
------------------------------------------
pub   2048R/E6FA5EAF 2015-08-25 [expires: 2025-08-22]
uid                  yourname (first pgp encrypt) <***@qq.com>
sub   2048R/41B91511 2015-08-25 [expires: 2025-08-22]
```
### 使用GPG加密tag
```
git tag -u "gpg-key-id" -m "tag comment" v2.0
# -u, --local-user <key-id> #指定gpg keyId
```
### 配置gitconfig
```
git config --global user.signingkey <GPG-key-id>
```
现在你能够签署标签或提交时，不必每次运行时指定密钥：
```
git commit -S -m "GPG-sign" 
# -s --signoff ,只添加一行Signed-off-by注释
# -S[<keyid>]  ,使用GPG签名并提交.

git tag -s -m "GPG-sign tag"
# -s --sign    ,使用默认key签名 
```
默认情况下git log不会列出或者验证签名。要显示提交所对应的签名，我们可以使用```--show-signature ```选项
```
git log --show-signature
```
### 参照：

- [GPG入门教程](http://www.ruanyifeng.com/blog/2013/07/gpg.html)
- [Git 使用中的教训：签名提交确保代码完整可信](http://www.oschina.net/translate/git-horror-story?lang=chs&page=4#)
