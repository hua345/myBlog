### 1.下载内核源码
```
wget http://mirrors.aliyun.com/linux-kernel/v4.x/linux-4.2.tar.xz 
tar -xvJf linux-4.2.tar.xz
mv linux-4.2 /usr/src/kernels/linux-4.2
cd /usr/src/linux-4.2
```
### 2.确保已经安装gcc和ncurses-devel
```
apt-get install gcc
apt-get install libncurses5-dev
```
配置编译选项:
设置内核编译选项是通过 kconfig 这个工具来完成的.
kconfig 的源码就是内核代码中 script/kconfig 目录下
make mrproper  #清除环境变量，即清除配置文件
生成配置文件:

- make menuconfig :: 源码根目录下生成 .config (没有会自动生成), .config中就是各个内核编译选项的选择状况.
- make defconfig :: 根据当前系统的架构默认 .config 生成内核源码目录下的 .config (每个架构的配置文件: ex. arch/x86/configs/x86_64_defconfig)
- make oldconfig :: 将已有的 .config 放到源码根目录下后执行, 目的是为了复用之前的内核编译选项的配置.
- make xconfig :: 图形化配置, 需要qt3, 个人觉得没有必要, 有 make menuconfig 就足够了.
- make localmodconfig :: 生成以正在使用的内核模块为对象的 .config

### 3. 编译内核
由于内核代码的庞大, 所以和一般应用程序相比, 编译时间会很长. 可以尝试以下方法来加快编译速度:

1.  不用的驱动程序都不要设置, 这样就不会编译
2.  利用make的 -j 选项来并发编译, ex. make -j N (N是并发数). 如果你的机器有4个CPU, 可以用 make -j 4 来提高编译速度
3.  使用 make localmodconfig 来生成仅以正在使用的内核模块为对象的 .config (一般这样生成的.config中包含的内核模块最少, 所以编译速度快)
```
make clean    #确保所有东西均保持最新状态
make -j4 bzImage  #编译内核
make -j4 modules  #编译模块
make -j4 modules_install  #安装内核模块到 /lib/modules 下
make install  #安装内核二进制映像, 生成并安装boot初始化文件系统映像文件
```
### 4. 修改启动菜单
```
vi /boot/grub/grub.cfg #好像不要就可以用了
reboot
uname -r  #查看当前内核版本
```
### 5. 卸载内核
```
删除/lib/modules/目录下不需要的内核库文件
删除/usr/src/kernel/目录下不需要的内核源码
删除/boot目录下启动的核心档案和内核映像
更改grub的配置，删除不需要的内核启动列表
```
### 6. 详细提示make help
### 6.1 几个重要的Linux内核文件介绍
为了进一步提高服务器的性能，可以需要根据特定的硬件及需求重新编译Linux内核。
#### 6.2 vmlinuz
vmlinuz是可引导的、压缩的内核。“vm”代表“Virtual Memory”。Linux 支持虚拟内存，不像老的操作系统比如DOS有640KB内存的限制。Linux能够使用硬盘空间作为虚拟内存，因此得名“vm”。vmlinuz是可执行的Linux内核，它位于/boot/vmlinuz，它一般是一个软链接。
vmlinuz的建立有两种方式。
一是编译内核时通过“make zImage”创建，zImage适用于小内核的情况，它的存在是为了向后的兼容性。
二是内核编译时通过命令make bzImage创建。
bzImage是压缩的内核映像，需要注意，bzImage不是用bzip2压缩的，bzImage中的bz容易引起误解，bz表示“big zImage”。 bzImage中的b是“big”意思。

zImage（vmlinuz）和bzImage（vmlinuz）都是用gzip压缩的。它们不仅是一个压缩文件，而且在这两个文件的开头部分内嵌有gzip解压缩代码。所以你不能用gunzip 或 gzip –dc解包vmlinuz。

内核文件中包含一个微型的gzip用于解压缩内核并引导它。两者的不同之处在于，老的zImage解压缩内核到低端内存（第一个640K），bzImage解压缩内核到高端内存（1M以上）。如果内核比较小，那么可以采用zImage 或bzImage之一，两种方式引导的系统运行时是相同的。大的内核采用bzImage，不能采用zImage。

vmlinux是未压缩的内核，vmlinuz是vmlinux的压缩文件。 
#### 6.3 initrd-x.x.x.img
initrd是“initial ramdisk”的简写。initrd一般被用来临时的引导硬件到实际内核vmlinuz能够接管并继续引导的状态。initrd实现加载一些模块和安装文件系统等。 
#### 6.4 System.map
System.map是一个特定内核的内核符号表。它是你当前运行的内核的System.map的链接。 
[编译Linux内核](http://www.cnblogs.com/wang_yb/p/3899439.html)
[CentOS6.5升级内核到3.10.28 ](http://blog.csdn.net/taiyang1987912/article/details/42744019)
