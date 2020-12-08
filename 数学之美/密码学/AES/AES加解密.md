# 1.AES对称加密

- [https://github.com/matt-wu/AES](https://github.com/matt-wu/AES)
- [http://www.ehcoo.com/cryptology.html](http://www.ehcoo.com/cryptology.html)
- [https://zhuanlan.zhihu.com/p/123221394](https://zhuanlan.zhihu.com/p/123221394)
- [https://xiaoxueying.gitbooks.io/graphic-cryptology/content/cryptogram_world.html](https://xiaoxueying.gitbooks.io/graphic-cryptology/content/cryptogram_world.html)
- [https://github.com/looly/hutool](https://github.com/looly/hutool)
- [https://github.com/brix/crypto-js](https://github.com/brix/crypto-js)

`AES`，全称`Advanced Encryption Standard`，高级加密标准，是NIST（美国国家标准与技术研究院）在2001年推出的标准，内容见《ADVANCED ENCRYPTION STANDARD (AES)》。但其实在1997年的时候NIST就公开征集`更安全的加密算法`以替代`DES`，经过3年的时间的验证，最终决定采用`Rijndael`算法。因此，有时候在网上搜索AES算法，会看见Rijndael这个名词。实际上：`AES=Rijndael算法子集`。

比如: 密钥长度则可以是128，192或256比特；而Rijndael使用的密钥和区块长度可以是32位的整数倍，以128位为下限，256比特为上限。加密过程中使用的密钥是由Rijndael密钥生成方案产生。

## 2.工作模式

分组（block）密码的工作模式（mode of operation）允许使用同一个分组密码密钥对多于一块的数据进行加密，并保证其安全性。

早在1981年，DES算法公布之后，NIST在标准文献FIPS 81中公布了4种工作模式：

- 电子密码本：Electronic Code Book Mode (ECB)
- 密码分组链接：Cipher Block Chaining Mode (CBC)
- 密文反馈：Cipher Feedback Mode (CFB)
- 输出反馈：Output Feedback Mode (OFB)

2001年又针对AES加入了新的工作模式：计数器模式：Counter Mode (CTR)

### 2.1电子密码本（ECB）

最简单的加密模式即为电子密码本（Electronic codebook，ECB）模式。需要加密的消息按照块密码的块大小被分为数个块，并对每个块进行独立加密.加密过程如下：

![ecb](./img/ecb.png)

解密过程如下：

![ecb](./img/ecb02.png)

### 2.2CBC：密码分组链接模式

此模式是1976年由IBM所发明，引入了`IV`（初始化向量：`Initialization Vector`）的概念。`IV`是长度为分组大小的一组随机，通常情况下不用保密，不过在大多数情况下，针对同一密钥不应多次使用同一组`IV`。

CBC模式相比ECB实现了更好的模式隐藏，但因为其将密文引入运算，加解密操作无法并行操作。同时引入的IV向量，还需要加、解密双方共同知晓方可。

加密过程如下：

![cbc](./img/cbc.png)

解密过程如下：

![cbc](./img/cbc02.png)

### 2.3 CFB：密文反馈模式

与CBC模式类似，但不同的地方在于，CFB模式先生成密码流字典，然后用密码字典与明文进行异或操作并最终生成密文。后一分组的密码字典的生成需要前一分组的密文参与运算。

![cfb](./img/cfb.png)

### 2.4 OFB：输出反馈模式

OFB模式与CFB模式不同的地方是：生成字典的时候会采用明文参与运算，CFB采用的是密文。

![ofb](./img/ofb.png)

### 2.5 CTR：计数器模式模式

CTR模式同样会产生流密码字典，但同是会引入一个计数，以保证任意长时间均不会产生重复输出。

![ctr](./img/ctr.png)

## 3. 数据补齐/填充（Padding）

`Padding`并不复杂，但是需要遵循同一套补齐/填充规则

`Bit Padding`（位填充）。这是ISO/IEC 9797-1推荐的做法，很简单，就是在原文后面增加二进制：10...0，首先填补`1`，接着还缺几位就补几位`0`。这种填充方式用在了诸如MD5和SHA等算法中。

`PKCS#5和PKCS#7`。前者是后者的子集，而`PKCS#7`也是我们很常见到的填充算法，且是`openssl`的默认填充算法（摘自《PKCS7 / PKCS5 填充算法》），它的设计也很巧妙：需要填充多少个byte，就在每个要填充的byte上填多少。

```bash
原文 01
原文 02 02
原文 03 03 03
原文 04 04 04 04
原文 05 05 05 05 05
原文 06 06 06 06 06 06
```

细心的你发现了一个问题没有：如果原文正好是`block size`（AES算法来说是128bits）的倍数，是否不需要填充？如果是，那么解密的时候怎么知道数据是否被填充过？

答案是：`无论是否block size的倍数，都需要填充。`

`PKCS#5`填充与`PKCS#7`填充相同，只不过它是为使用64位（8字节）块大小的块密码定义的。 实际上，两者可以互换使用。
