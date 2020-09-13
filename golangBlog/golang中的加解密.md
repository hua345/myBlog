#### 参考
- [golang中关于RSA加密、解密、签名、验签的总结](https://blog.csdn.net/xz_studying/article/details/80314111)
- [Golang计算MD5](http://blog.51cto.com/gotaly/1403942)
- [AES加密算法的详细介绍与实现](https://blog.csdn.net/qq_28205153/article/details/55798628)


### 1.1 源码地址[https://github.com/hua345/golangEncrypt](https://github.com/hua345/golangEncrypt)
### 1.2 openssl生成私钥 
```
openssl genrsa -out rsa_private_key.pem 1024
```
### 1.3 openssl生成公钥 
```
openssl rsa -in rsa_private_key.pem -pubout -out rsa_public_key.pem
```
### 2. 编码方式
#### 2.1 hex
hex也称为base16，意思是使用16个可见字符来表示一个二进制数组，编码后数据大小将翻倍,因为1个字符需要用2个可见字符来表示。
```
hex.DecodeString(s string)//解密
hex.EncodeToString(src []byte) string//加密
```
#### 2.2 base64
使用64个可见字符来表示一个二进制数组，编码后数据大小变成原来的4/3,也即3个字符用4个可见字符来表示。
```
base64.StdEncoding.DecodeString(s string) ([]byte, error)//解密
base64.StdEncoding.EncodeToString(src []byte) string//加密
```
### 3. 私钥的格式
解析私钥的方式如下：
```
#PKCS1
x509.ParsePKCS1PrivateKey(der []byte) (key interface{}, err error)
#PKCS8
x509.ParsePKCS8PrivateKey(der []byte) (key interface{}, err error)
```
### 4. 单向加密算法
简而言之就是不可解密的加密方法
>第一是任意两段明文数据，加密以后的密文不能是相同的；
> 第二是任意一段明文数据，经过加密以后，其结果必须永远是不变的。

#### 4.1 MD5
```
package main
import (
    "crypto/md5"
    "encoding/hex"
    "fmt"
)
func main(){
    hash := md5.New()
    hash.Write([]byte("test md5 encrypto"))
    encryptedData := hash.Sum(nil)
    fmt.Println("md5:", hex.EncodeToString(encryptedData))
}
```
中通过md5.New()初始化一个MD5对象，其实它是一个hash.Hash对象。 函数原型为:
```
func New() hash.Hash
```
该对象实现了hash.Hash的Sum接口：计算出校验和。其函数原型 为:
```
func Sum(data []byte) [Size]byte
```
#### 4.2 SHA1
```
hash := sha1.New()
hash.Write([]byte(originalData))
encryptedData, err := rsa.SignPKCS1v15(rand.Reader, prvKey, crypto.SHA1, hash.Sum(nil))
```
#### 4.3 SHA256
```
hash := sha256.New()
hash.Write([]byte(originalData))
encryptedData, err := rsa.SignPKCS1v15(rand.Reader, prvKey, crypto.SHA256, hash.Sum(nil))
```
#### 4.4 HMAC_SHA1
HMAC运算利用哈希算法，以一个密钥和一个消息为输入，生成一个消息摘要作为输出。
  HMAC是需要一个密钥的。所以，HMAC_SHA1也是需要一个密钥的，而SHA1不需要。
  
```
import (
	"crypto/hmac"
	"crypto/sha1"
)
func main(){
    key := []byte("123456")
    mac := hmac.New(sha1.New, key)
    mac.Write(originalData)
    fmt.Println("hmac:", hex.EncodeToString(mac.Sum(nil)))
}
```
### 5. RSA非对称加密
主要有加密/解密、签名/验签4中方式，且加密/解密与签名/验签均是一个相反的过程。两对是根据对公钥及私钥的使用划分的。

>加密/解密是采用公钥加密，私钥解密。
签名/验签是采用私钥签名，公钥验签。
```
#加密
rsa.EncryptPKCS1v15(rand io.Reader, pub *PublicKey, msg []byte) ([]byte, error)
#解密
rsa.DecryptPKCS1v15(rand io.Reader, priv *PrivateKey, ciphertext []byte) ([]byte, error)
#签名
rsa.SignPKCS1v15(rand io.Reader, priv *PrivateKey, hash crypto.Hash, hashed []byte) ([]byte, error)
#验签
rsa.VerifyPKCS1v15(pub *PublicKey, hash crypto.Hash, hashed []byte, sig []byte) error
```
### 6. AES对称加密
