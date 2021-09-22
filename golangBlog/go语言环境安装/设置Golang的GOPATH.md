Go是一门全新的静态类型开发语言，具有`自动垃圾回收`，`丰富的内置类型`,`函数多返回值`，`错误处理`，`匿名函数`,`并发编程`，`反射`等特性．
### 1.1 Linux golang安装
[golang下载](http://www.golangtc.com/download)
```bash
sudo tar -zvxf go1.6.2.linux-amd64.tar.gz
sudo mv go /usr/local/go
#设置环境变量
vi /etc/profile
export GOROOT=/usr/local/go  #设置为go安装的路径
export GOPATH=$HOME/gocode   #默认安装包的路径
export PATH=$PATH:$GOROOT/bin:$GOPATH/bin
source /etc/profile
```
#### 1.2 Windows golang安装
[golang下载](https://mirrors.ustc.edu.cn/golang/)
```bash
#设置环境变量
vi /etc/profile
GOROOT=D:\Program Files\Golang\  #设置为go安装的路径
GOPATH=E:\gocode   #默认安装包的路径
Path路径添加%GOROOT%\bin;%GOPATH%\bin
```
![这里写图片描述](//img-blog.csdn.net/20180318202510157?watermark/2/text/Ly9ibG9nLmNzZG4ubmV0L2NoZW5qaDIxMw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
![这里写图片描述](//img-blog.csdn.net/20180318202409108?watermark/2/text/Ly9ibG9nLmNzZG4ubmV0L2NoZW5qaDIxMw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
### 2.0 GOPATH设置
`go`命令依赖一个重要的环境变量：`$GOPATH`
`GOPATH`允许多个目录，当有多个目录时，请注意分隔符，多个目录的时候Windows是分号`;`，Linux系统是冒号`:`
当有多个`GOPATH时`默认将`go get`获取的包存放在第一个目录下
`$GOPATH`目录约定有三个子目录

- `src`存放源代码(比如：.go .c .h .s等)
- `pkg`编译时生成的中间文件（比如：.a）
- `bin`编译后生成的可执行文件（为了方便，可以把此目录加入到 $PATH 变量中，如果有多个gopath，那么使用`${GOPATH//://bin:}/bin`添加所有的bin目录）

### 3. 代码目录结构规划
GOPATH下的src目录就是接下来开发程序的主要目录，所有的源码都是放在这个目录下面，那么一般我们的做法就是一个目录一个项目，例如: $GOPATH/src/mymath 表示mymath这个应用包或者可执行应用，这个根据package是main还是其他来决定，main的话就是可执行应用，其他的话就是应用包，这个会在后续详细介绍package。

下面我就以mymath为例来讲述如何编写应用包，执行如下代码
新建一个自己`golang`代码的路径`myGolang`
```
export GOPATH=$HOME/gocode:$HOME/myGolang
export PATH=$PATH:$GOROOT/bin:${GOPATH//://bin:}/bin
```
```sh
cd $GOPATH/src
mkdir mymath
```
新建文件`fabnacci.go`
```
package mymath

func Fabnacci(num int) int {
  if num == 0 || num == 1 {
    return num
  }
  return Fabnacci(num -1) + Fabnacci(num -2)
}
```
### 4.0 编译应用
上面我们已经建立了自己的应用包,如何进行编译安装呢?有两种方式可以进行安装

- 进入对于的安装包目录，然后执行`go install`
- 在任意的目录下指定需要编译的包`go build mymath`
编译后可以在`$GOPATH/pkg/${GOOS}_${GOARCH}`下看到`mymath.a`文件
.a文件是应用包，那么我们如何进行调用呢?
接下来我们新建一个应用程序来调用这个应用包
```
cd $GOPATH/src
mkdir mathapp
```
新建Fabnacci.go文件
```go
package main

import (
  "mymath"
  "fmt"
  "os"
  "strconv"
)
func main() {
  if len(os.Args) < 2 {
    fmt.Println("input number")
    return
  }
  num, err := strconv.Atoi(os.Args[1])
  if err != nil {
    fmt.Println("input must be number", err)
    return
  }
  fmt.Println("Fabnacci :", num, mymath.Fabnacci(num))
}
```
如何编译程序呢？进入该应用目录，然后执行`go build`，在该目录下会生成`mathapp`可执行文件
```
time ./mathapp 45
Fabnacci : 45 1134903170

real	0m10.836s
user	0m10.208s
sys	0m0.032s
```
如何安装应用程序?进入该目录执行`go install`，那么会在`$GOPATH/bin/`增加一个可执行文件`mathapp`
`$GOPATH/bin/`目录已经加入了环境变量，可以直接运行`mathapp`

参照:

- [GOPATH与工作空间](https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/01.2.md)
