# 参考

- [http://www.gnu.org/software/make/](http://www.gnu.org/software/make/)
- [make镜像](http://mirrors.ustc.edu.cn/gnu/make/)

## 下载make

```bash
wget http://mirrors.ustc.edu.cn/gnu/make/make-4.2.tar.gz

tar -zvxf make-4.2.tar.gz
cd make-4.2
./configure
make
make install
```

## 查看版本

重新ssh登录

```bash
➜  ~ make -v
GNU Make 4.2
为 x86_64-pc-linux-gnu 编译
Copyright (C) 1988-2016 Free Software Foundation, Inc.
许可证：GPLv3+：GNU 通用公共许可证第 3 版或更新版本<http://gnu.org/licenses/gpl.html>。
本软件是自由软件：您可以自由修改和重新发布它。
在法律允许的范围内没有其他保证。
```
