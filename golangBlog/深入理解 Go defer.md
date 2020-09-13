#### 参考
- [深入理解 Go defer](https://segmentfault.com/a/1190000019303572)
### 特性
我们简单的过一下 defer 关键字的基础使用，让大家先有一个基础的认知

#### 一、延迟调用
```
package main

import "log"
func main() {
    defer log.Println("Fang.")

    log.Println("end.")
}
```
输出结果：
```
$ go run main.go
2019/06/06 09:58:20 end.
2019/06/06 09:58:20 Fang.
```
#### 二、后进先出
```
package main

import (
        "log"
        "strconv"
)
func main() {
    for i := 0; i < 6; i++ {
        defer log.Println("Fang" + strconv.Itoa(i) + ".")
    }


    log.Println("end.")
}
```
输出结果：
```
$ go run main.go
2019/06/06 10:23:23 end.
2019/06/06 10:23:24 Fang5.
2019/06/06 10:23:24 Fang4.
2019/06/06 10:23:24 Fang3.
2019/06/06 10:23:24 Fang2.
2019/06/06 10:23:24 Fang1.
2019/06/06 10:23:24 Fang0.
```
#### 三、运行时间点
```
package main

import "log"

func main() {
        func() {
                defer log.Println("defer.Fang.")
        }()

        log.Println("main.Fang.")
}
```
输出结果：
```
$ go run main.go 
2019/05/22 23:30:27 defer.EDDYCJY.
2019/05/22 23:30:27 main.EDDYCJY.
```
#### 四、异常处理
```
package main

import "log"

func main() {
    defer func() {
        if e := recover(); e != nil {
            log.Println("Fang.")
        }
    }()

    panic("end.")
}
```
输出结果：
```
$ go run main.go
2019/06/06 10:29:30 Fang.
```
### 源码剖析
```
package main

import "log"
func main() {
    defer log.Println("Fang.")
    log.Println("end.")
}
```
```
$ go tool compile -S main.go
"".main STEXT size=234 args=0x0 locals=0x50
        0x0000 00000 (main.go:4)        TEXT    "".main(SB), ABIInternal, $80-0
        ...
        0x0043 00067 (main.go:5)        MOVQ    CX, ""..autotmp_4+48(SP)
        0x0048 00072 (main.go:5)        MOVL    $24, (SP)
        0x004f 00079 (main.go:5)        PCDATA  $2, $2
        0x004f 00079 (main.go:5)        LEAQ    log.Println·f(SB), CX
        0x0077 00119 (main.go:5)        CALL    runtime.deferproc(SB)
        0x00bb 00187 (main.go:6)        CALL    log.Println(SB)
        0x00c0 00192 (main.go:7)        XCHGL   AX, AX
        0x00c1 00193 (main.go:7)        CALL    runtime.deferreturn(SB)
        0x00c6 00198 (main.go:7)        MOVQ    72(SP), BP
        0x00cb 00203 (main.go:7)        ADDQ    $80, SP
        0x00cf 00207 (main.go:7)        RET
        0x00d0 00208 (main.go:5)        XCHGL   AX, AX
        0x00d1 00209 (main.go:5)        CALL    runtime.deferreturn(SB)
        0x00d6 00214 (main.go:5)        MOVQ    72(SP), BP
        0x00db 00219 (main.go:5)        ADDQ    $80, SP
        0x00df 00223 (main.go:5)        RET
        0x00e0 00224 (main.go:5)        NOP
        0x00e0 00224 (main.go:4)        PCDATA  $0, $-1
        0x00e0 00224 (main.go:4)        PCDATA  $2, $-1
        0x00e0 00224 (main.go:4)        CALL    runtime.morestack_noctxt(SB)
        0x00e5 00229 (main.go:4)        JMP     0
```
#### 查看源代码
在golang源代码目录`src/runtime/panic.go`
```
// Create a new deferred function fn with siz bytes of arguments.
// The compiler turns a defer statement into a call to this.
//go:nosplit
func deferproc(siz int32, fn *funcval) { // arguments of fn follow fn
	if getg().m.curg != getg() {
		// go code on the system stack can't defer
		throw("defer on system stack")
	}

	// the arguments of fn are in a perilous state. The stack map
	// for deferproc does not describe them. So we can't let garbage
	// collection or stack copying trigger until we've copied them out
	// to somewhere safe. The memmove below does that.
	// Until the copy completes, we can only call nosplit routines.
	sp := getcallersp()
	argp := uintptr(unsafe.Pointer(&fn)) + unsafe.Sizeof(fn)
	callerpc := getcallerpc()

	d := newdefer(siz)
	if d._panic != nil {
		throw("deferproc: d.panic != nil after newdefer")
	}
	d.fn = fn
	d.pc = callerpc
	d.sp = sp
	switch siz {
	case 0:
		// Do nothing.
	case sys.PtrSize:
		*(*uintptr)(deferArgs(d)) = *(*uintptr)(unsafe.Pointer(argp))
	default:
		memmove(deferArgs(d), unsafe.Pointer(argp), uintptr(siz))
	}
}
```
```
// The single argument isn't actually used - it just has its address
// taken so it can be matched against pending defers.
//go:nosplit
func deferreturn(arg0 uintptr) {
	gp := getg()
	d := gp._defer
	if d == nil {
		return
	}
	sp := getcallersp()
	if d.sp != sp {
		return
	}

	// Moving arguments around.
	//
	// Everything called after this point must be recursively
	// nosplit because the garbage collector won't know the form
	// of the arguments until the jmpdefer can flip the PC over to
	// fn.
	switch d.siz {
	case 0:
		// Do nothing.
	case sys.PtrSize:
		*(*uintptr)(unsafe.Pointer(&arg0)) = *(*uintptr)(deferArgs(d))
	default:
		memmove(unsafe.Pointer(&arg0), deferArgs(d), uintptr(d.siz))
	}
	fn := d.fn
	d.fn = nil
	gp._defer = d.link
	freedefer(d)
	jmpdefer(fn, uintptr(unsafe.Pointer(&arg0)))
}
```
