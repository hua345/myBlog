# 参考

- [http://gcc.gnu.org/](http://gcc.gnu.org/)
- [gcc镜像](http://mirrors.ustc.edu.cn/gnu/gcc)

## 下载gcc

```bash
wget http://mirrors.ustc.edu.cn/gnu/gcc/gcc-9.2.0/gcc-9.2.0.tar.xz

tar -vxf gcc-9.2.0.tar.xz
cd gcc-9.2.0

# 下载供编译需求的依赖项
./contrib/download_prerequisites
gmp-6.1.0.tar.bz2: 确定
mpfr-3.1.4.tar.bz2: 确定
mpc-1.0.3.tar.gz: 确定
isl-0.18.tar.bz2: 确定
All prerequisites downloaded successfully.

# 生成Makefile文件
./configure -enable-checking=release -enable-languages=c,c++ -disable-multilib

# 编译
make -j4
# 安装
make install
# 查看版本号
gcc -v
使用内建 specs。
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/local/libexec/gcc/x86_64-pc-linux-gnu/9.2.0/lto-wrapper
目标：x86_64-pc-linux-gnu
配置为：./configure -enable-checking=release -enable-languages=c,c++ -disable-multilib
线程模型：posix
gcc 版本 9.2.0 (GCC)
```

## 升级gcc动态库

```bash
# 查看之前版本动态库文件
ll /usr/lib64/libstdc*
# 查看现在gcc动态库文件
ll /usr/local/lib64/libstdc++*
# 复制libstdc++.s文件
cp /usr/local/lib64/libstdc++.so.6.0.27 /usr/lib64/
# 删除之前的软连接
rm /usr/lib64/libstdc++.so.6

# 将默认库的软连接指向最新动态库
ln -s /usr/lib64/libstdc++.so.6.0.27 /usr/lib64/libstdc++.so.6
```
