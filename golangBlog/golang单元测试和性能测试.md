> Go语言中自带有一个轻量级的测试框架`testing`

#### 1. 查看帮助
```
go test -h
```
### 2. 单元测试
```
package util

import (
	"crypto/md5"
	"encoding/hex"
)

func EncodeMD5(value string) string {
	m := md5.New()
	m.Write([]byte(value))

	return hex.EncodeToString(m.Sum(nil))
}
```
在需要测试的文件同一目录创建测试文件
约定文件名必须是`_test.go`结尾的,测试用例函数必须是`Test`开头
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190329114531547.png)
```
package util

import (
"testing"
)

// 单元测试
// go test -v
func TestEncodeMD5(t *testing.T) {
	if EncodeMD5("hello") != "5d41402abc4b2a76b9719d911017c592" {
		t.Error(`EncodeMD5("hello") != "5d41402abc4b2a76b9719d911017c592"`)
	}
	if EncodeMD5("world") != "7d793037a0760186574b0282f2f435e7" {
		t.Error(`EncodeMD5("world") != "7d793037a0760186574b0282f2f435e7"`)
	}
}
```
### 3. 单元测试覆盖率
```
go test -cover
Test Begin
PASS
coverage: 100.0% of statements
ok      ginLearn/pkg/util       0.510s

```
### 4. 基准测试
- 压力测试用例约定以`Benchmark`开头
- 压力测试参数是`b *testing.B`
- 在循环体内使用`testing.B.N`，以使压力测试可以正常的运行
- `1s(秒) = 1000ms(毫秒) 1ms = 1000 us(微秒) 1 us = 1000ns(纳秒)`
```
func BenchmarkXXX(b *testing.B) { ... }
```
```
func BenchmarkEncodeMD5(b *testing.B) {
	b.StopTimer() //停止压力测试的时间计数
	//做一些初始化的工作,例如读取文件数据,数据库连接之类的,
	b.StartTimer() //重新开始时间
	for i := 0; i < b.N; i++ { //use b.N for looping
		EncodeMD5("hello")
	}
}
```
执行命令`go test -test.bench=.`
```
$ go test -test.bench=".*"
goos: windows
goarch: amd64
pkg: ginLearn/pkg/util
BenchmarkEncodeMD5-4     3000000               513 ns/op
PASS
ok      ginLearn/pkg/util       2.519s
```
结果中`基准测试名的数字后缀部分`，这里是`4`，表示运行时对应的`GOMAXPROCS`的值，这对于一些与并发相关的基准测试是重要的信息。
执行多次压力测试`go test -test.bench=.* -count=5`,可以查看多次运行的平均时间
```
$ go test -test.bench=".*" -count=5
goos: windows
goarch: amd64
pkg: ginLearn/pkg/util
BenchmarkEncodeMD5-4     3000000               510 ns/op
BenchmarkEncodeMD5-4     3000000               514 ns/op
BenchmarkEncodeMD5-4     3000000               511 ns/op
BenchmarkEncodeMD5-4     3000000               524 ns/op
BenchmarkEncodeMD5-4     3000000               511 ns/op
PASS
ok      ginLearn/pkg/util       10.931s
```
快的程序往往是伴随着较少的内存分配。`-benchmem`命令行标志参数将在报告中包含内存的分配数据统计。我们可以比较优化前后内存的分配情况。
```
$ go test -bench=. -benchmem
goos: windows
goarch: amd64
pkg: ginLearn/pkg/util
BenchmarkEncodeMD5-4     3000000               504 ns/op             184 B/op         5 allocs/op
PASS
ok      ginLearn/pkg/util       2.411s
```
### 剖析
CPU剖析数据标识了最耗CPU时间的函数。在每个CPU上运行的线程在每隔几毫秒都会遇到操作系统的中断事件，每次中断时都会记录一个剖析数据然后恢复正常的运行。

堆剖析则标识了最耗内存的语句。剖析库会记录调用内部内存分配的操作，平均每512KB的内存申请会触发一个剖析数据。

阻塞剖析则记录阻塞goroutine最久的操作，例如系统调用、管道发送和接收，还有获取锁等。每当goroutine被这些操作阻塞时，剖析库都会记录相应的事件。
只需要开启下面其中一个标志参数就可以生成各种分析文件。当同时使用多个标志参数时需要当心，因为一项分析操作可能会影响其他项的分析结果。
```
go test -cpuprofile=cpu.out
go test -blockprofile=block.out
go test -memprofile=mem.out
```
