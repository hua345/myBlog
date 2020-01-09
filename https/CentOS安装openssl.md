#### [https://github.com/openssl/openssl](https://github.com/openssl/openssl)
#### OpenSSL 1.1.1正式支持TLS1.3
> OpenSSL既上个LTS（长期支持版本）1.0.2之后有一个LTS版本,最重要的功能是支持了TLSv1.3.
- 由于减少了客户端和服务器之间所需的往返次数，缩短了连接时间
- 在某些情况下，客户端能够立即开始将加密数据发送到服务器而无需与服务器进行任何往返（称为0-RTT或“早期数据”）。
- 由于删除了各种过时和不安全的加密算法以及更多连接握手的加密，提高了安全性

> 之前的LTS版本（OpenSSL 1.0.2）将继续获得全面支持， 之后它只会收到安全修复程序。 它将在2019年底停止接收所有支持。
#### 1.1 openssl里的fips是什么意思？
> openssl-fips是符合FIPS标准的Openssl。

> 联邦信息处理标准（Federal Information Processing Standards，FIPS）是一套描述文件处理、加密算法和其他信息技术标准（在非军用政府机构和与这些机构合作的政府承包商和供应商中应用的标准）的标准。
#### 1.2 OPENSSL_FIPS宏有什么作用？
> Intel AES指令（AES-NI）是Intel32纳米微架构上的一组新指令。这些指令对于使用 AES（Advancde Encryption Standard）算法进行数据加解密的操作能够起到加速的作用。AES标准由FIPS定义，如今广泛 应用在贸易安全，数据库的加密等各个方面。

> Intel AES-NI包括七条指令。其中六条是硬件对AES的支持（四条关于AES加解密，另两条指令有关AES key的扩展）。第七条指令有助于进位乘法。

> AES-NI可以灵活地支持AES的各种使用方式，包括各种标准密钥的长度，各种模式的操作，甚至是一些非标准或是未来可能的各种方式。对比现在一些纯软件的实现，它对性能的提升非常显著。

> 如果打开该宏，直接调用Intel AES指令，轻松获得5倍左右的性能提升（这个摘抄网上的说法，没有真正测试过）。
#### 2.1 安装依赖环境
```
yum install perl gcc
[root@dockerMaster openssl-OpenSSL_1_0_2r]# perl -v

This is perl 5, version 16, subversion 3 (v5.16.3) built for x86_64-linux-thread-multi
(with 39 registered patches, see perl -V for more detail)

Copyright 1987-2012, Larry Wall

Perl may be copied only under the terms of either the Artistic License or the
GNU General Public License, which may be found in the Perl 5 source kit.

Complete documentation for Perl, including FAQ lists, should be found on
this system using "man perl" or "perldoc perl".  If you have access to the
Internet, point your browser at http://www.perl.org/, the Perl Home Page.

[root@dockerMaster openssl-OpenSSL_1_0_2r]# gcc -v
使用内建 specs。
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/libexec/gcc/x86_64-redhat-linux/4.8.5/lto-wrapper
目标：x86_64-redhat-linux
配置为：../configure --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info --with-bugurl=http://bugzilla.redhat.com/bugzilla --enable-bootstrap --enable-shared --enable-threads=posix --enable-checking=release --with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions --enable-gnu-unique-object --enable-linker-build-id --with-linker-hash-style=gnu --enable-languages=c,c++,objc,obj-c++,java,fortran,ada,go,lto --enable-plugin --enable-initfini-array --disable-libgcj --with-isl=/builddir/build/BUILD/gcc-4.8.5-20150702/obj-x86_64-redhat-linux/isl-install --with-cloog=/builddir/build/BUILD/gcc-4.8.5-20150702/obj-x86_64-redhat-linux/cloog-install --enable-gnu-indirect-function --with-tune=generic --with-arch_32=x86-64 --build=x86_64-redhat-linux
线程模型：posix
gcc 版本 4.8.5 20150623 (Red Hat 4.8.5-36) (GCC)
```
#### 2.2 安装[zlib](https://github.com/madler/zlib)
```
tar -zvxf zlib-1.2.11.tar.gz
cd zlib-1.2.11
./configure
make && make install
```
#### 3.1 查看当前openssl版本
```
# openssl version
OpenSSL 1.0.2k-fips  26 Jan 2017
```
#### 3.2 安装openssl
```
tar -zvxf openssl-OpenSSL_1_1_1b.tar.gz
cd openssl-OpenSSL_1_1_1b
```
#### 3.3 编译openssl
```
./config shared zlib  --prefix=/usr/local/openssl
make && make install
```
#### 3.4 修改环境变量
```
vi /etc/ld.so.conf
#添加动态库路径
/usr/local/openssl/lib
# 使动态库生效
ldconfig
```
```
vi /etc/profile
export PATH=/usr/local/openssl/bin:$PATH 
source /etc/profile

# openssl version -a
OpenSSL 1.1.1b  26 Feb 2019
built on: Fri May 10 06:24:03 2019 UTC
platform: linux-x86_64
options:  bn(64,64) rc4(16x,int) des(int) idea(int) blowfish(ptr)
compiler: gcc -fPIC -pthread -m64 -Wa,--noexecstack -Wall -O3 -DOPENSSL_USE_NODELETE -DL_ENDIAN -DOPENSSL_PIC -DOPENSSL_CPUID_OBJ -DOPENSSL_IA32_SSE2 -DOPENSSL_BN_ASM_MONT -DOPENSSL_BN_ASM_MONT5 -DOPENSSL_BN_ASM_GF2m -DSHA1_ASM -DSHA256_ASM -DSHA512_ASM -DKECCAK1600_ASM -DRC4_ASM -DMD5_ASM -DAES_ASM -DVPAES_ASM -DBSAES_ASM -DGHASH_ASM -DECP_NISTZ256_ASM -DX25519_ASM -DPADLOCK_ASM -DPOLY1305_ASM -DZLIB -DNDEBUG
OPENSSLDIR: "/usr/local/openssl/ssl"
ENGINESDIR: "/usr/local/openssl/lib/engines-1.1"
Seeding source: os-specific
```
