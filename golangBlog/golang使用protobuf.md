#### 参考:
- [Golang gRPC实践 连载三 Protobuf语法](https://segmentfault.com/a/1190000007917576)
#### 1.1 下载二进制`protobuf`的编译器`protoc`
```
https://github.com/protocolbuffers/protobuf/releases
```
下载: [protoc-xxx-win64.zip](https://github.com/protocolbuffers/protobuf/releases)
解压，把bin目录下的`protoc.exe`复制到`GOPATH/bin`下，`GOPATH/bin`加入环境变量。
#### 1.2 [linux环境编译protobuf](https://github.com/protocolbuffers/protobuf/blob/master/src/README.md)
源代码编译`protobuf`需要下面的工具：
- autoconf
- automake
- libtool
- make
- g++
- unzip
```
yum install autoconf automake libtool curl make g++ unzip
```
下载源代码
```
$ git clone https://github.com/protocolbuffers/protobuf.git
$ cd protobuf
$ git submodule update --init --recursive
$ ./autogen.sh
```
编译`Protocol Buffer`编译器(protoc)
```
$ ./configure
$ make
$ make check
$ sudo make install
$ sudo ldconfig # refresh shared library cache.
```
#### 2. 安装golang编译插件`protoc-gen-go`
```
go get -u github.com/golang/protobuf/protoc-gen-go
```
如果成功，会在`GOPATH/bin`下生成`protoc-gen-go.exe`文件

#### 3. 编辑hello.proto
```
syntax = "proto3";
package hello.protobuf;

enum BookCategory {
    ComputerScience = 0; //计算机科学
    English = 1; //英语
    Economics = 2; //经济学
}
message Book {
    string name = 1; // 书名
    int32 price = 2; // 价格
    repeated BookCategory category = 3; // 类别
}
```
#### 4. 生成golang文件
```
protoc --go_out=. hello.proto
```

### 5. Protobuf语法
#### 5.1 标识符Tags
> 可以看到，消息的定义中，每个字段都有一个唯一的数值型标识符。这些标识符用于标识字段在消息中的二进制格式，使用中的类型不应该随意改动。
需要注意的是，[1-15]内的标识在编码时只占用一个字节，包含标识符和字段类型。[16-2047]之间的标识符占用2个字节。
建议为频繁出现的消息元素使用[1-15]间的标识符

#### 5.2 导入定义(import)
可以使用import语句导入使用其它描述文件中声明的类型
```
import "others.proto";
```
`protocol buffer`编译器会在`-I / --proto_path`参数指定的目录中查找导入的文件，如果没有指定该参数，默认在当前目录中查找。
#### 5.3 字段规则
- `repeated`：标识字段可以重复任意次，类似数组
- `proto3`不支持`proto2`中的`required`和`optional`
#### 5.4 包(Packages)
在.proto文件中使用package声明包名，避免命名冲突。
```
syntax = "proto3";
package hello.protobuf;
...
```
在其他的消息格式定义中可以使用包名+消息名的方式来使用类型，如：
```
syntax = "proto3";
import "hello.proto";

package world.protobuf;

//书店
message BookStore {
    repeated hello.protobuf.Book bookList = 1;
}
```
#### 5.5 Map类型
proto3支持map类型声明:
```
map<key_type, value_type> map_field = N;

message Project {...}
map<string, Project> projects = 1;
```
- 键、值类型可以是内置的标量类型，也可以是自定义`message`类型
- 字段不支持`repeated`属性

### 5.6 基本规范
描述文件以`.proto`做为文件后缀，除结构定义外的语句以分号结尾
#### 5.7 结构定义包括：`message、service、enum`
rpc方法定义结尾的分号可有可无

`message`命名采用驼峰命名方式，字段命名采用小写字母加下划线分隔方式
```
message SongServerRequest {
    required string song_name = 1;
}
```
`enum`命名也采用驼峰命名方式，字段命名采用大写字母加下划线分隔方式
```
enum Foo {
    FIRST_VALUE = 1;
    SECOND_VALUE = 2;
}
```
