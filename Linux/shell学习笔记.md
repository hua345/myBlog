从程序员的角度来看， Shell本身是一种用C语言编写的程序，从用户的角度来看，Shell是用户与Linux操作系统沟通的桥梁。
首行中的符号#!告诉系统其后路径所指定的程序即是解释此脚本文件的Shell程序。
```
#!/bin/bash
```
env可以在系统的PATH目录中查找指定的脚本解释器来运行
```
#!/usr/bin/env  python
```
###输入输出从定向
输入重定向用于改变命令的输入，输出重定向用于改变命令的输出。输出重定向更为常用，它经常用于将命令的结果输入到文件中，而不是屏幕上。输入重定向的命令是<，输出重定向的命令是>
#### 1. 管道符
前面已经提过过管道符`|`，就是把前面的命令运行的结果丢给后面的命令。
#### 2.作业控制
当运行一个进程时，你可以使它暂停（Ctrl + z），然后使用`fg`命令恢复它，利用bg命令使他到后台运行，你也可以使它终止（Ctrl + c）。
#### 3.变量赋值和引用
```
#!/bin/bash

#对变量赋值：
#给变量赋值的时候，不能在"="两边留空格
hello="hello world"  

#要取用一个变量的值，只需在变量名前面加一个$
echo $hello

#使用 unset 命令可以删除变量
unset variable_name
```
#### 4.单引号 VS 双引号
基本上来说，变量名会在双引号中展开，单引号中则不会。如果你不需要引用变量值，那么使用单引号可以很直观的输出你期望的结果。 An example 示例
```
#!/bin/bash
echo -n '$USER=' 
# -n选项表示阻止echo换行
echo "$USER"
echo "\$USER=$USER"  
# 该命令等价于上面的两行命令
```
###使用大括号保护变量
这里有一个潜在的问题。假设你想打印变量X的值，并在值后面紧跟着打印”abc”。那么问题来了：你该怎么做呢？ 先试一试
```
#!/bin/bash
X=ABC
echo "$Xabc"
```
这个脚本没有任何输出。究竟哪里出了问题？这是由于shell以为我们想要打印变量Xabc的值，实际上却没有这个变量。为了解决这种问题可以用大括号将变量名包围起来，从而避免其他字符的影响。面这个脚本可以正常工作：
```
#!/bin/bash
X=ABC
echo "${X}abc"
```

#### 5. if 语 句
"if"表达式如果条件为真，则执行then后的部分:
```
if ....; then
  ....
elif ....; then
  ....
else
  ....
fi
```
大多数情况下，可以使用测试命令来对条件进行测试，比如可以比较字符串、判断文件是否存在及是否可读等等，通常用` [ ] `来表示条件测试，注意这里的空格很重要，要确保方括号前后的空格。

`[  -f "somefile" ] `：判断是否是一个文件
`[ -x "/bin/ls" ]` ：判断/bin/ls是否存在并有可执行权限
`[ -n "$var" ] `：判断$var变量是否有值
`[ "$a" = "$b" ] `：判断$a和$b是否相等
执行`man test`可以查看所有测试表达式可以比较和判断的类型
```
#!/bin/bash

if [ ${SHELL} = "/bin/bash" ]; then
   echo "your login shell is the bash (bourne again shell)"
else
   echo "your login shell is not bash but ${SHELL}"
fi
```
变量$SHELL包含有登录shell的名称，我们拿它和/bin/bash进行比较以判断当前使用的shell是否为bash。
#### 6. && 和 || 操作符
```
[ -f "/etc/shadow" ] && echo "This computer uses shadow passwords"
```
这里的 && 就是一个快捷操作符，如果左边的表达式为真则执行右边的语句，你也可以把它看作逻辑运算里的与操作。
```
#!/bin/bash

mailfolder=/var/spool/mail/james
[ -r "$mailfolder" ] || { echo "Can not read $mailfolder" ; exit 1; }
echo "$mailfolder has mail from:"
grep "^From " $mailfolder
```
该脚本首先判断mailfolder是否可读，如果可读则打印该文件中以"From"开头的行。如果不可读则或操作生效，打印错误信息后脚本退出。
#### 7. case 语句
case表达式可以用来匹配一个给定的字符串，而不是数字
```
case ... in
   ...) do something here 
   ;;
esac
```
一旦模式匹配，则执行完匹配模式相应命令后不再继续其他模式。如果无一匹配模式，使用星号` * `捕获该值，再执行后面的命令。
```bash
echo "input: a,b,c"
read str

case "$str" in
"a")
echo "select a ok";;
"b")
echo "select b ok";;
"c")
echo "select c ok";;
*) echo "select $str error";;
esac
```
#### 8. select
select表达式是bash的一种扩展应用，擅长于交互式场合。用户可以从一组不同的值中进行选择：
```
select var in ... ; do
　break;
done
.... now $var can be used ....
``` 
```bash
#!/bin/bash

echo "What is your favourite OS?"
select var in "Linux" "Gnu Hurd" "Free BSD" "Other"; do
  break;
done
echo "You have selected $var"
```
#### 9. while/for 循环
```
while ...; do
   ....
done
```
只要测试表达式条件为真，则while循环将一直运行。关键字"break"用来跳出循环，而关键字”continue”则可以跳过一个循环的余下部分，直接跳到下一次循环中。 
```
for var in ....; do
   ....
done
```
for循环会查看一个字符串列表（字符串用空格分隔），并将其赋给一个变量：
```bash
for var in hello error world
do
     if [ $var = error ]; then
     continue
     fi
    echo "string $var"
done
```
#### 10. 函数
```
function function_name () {
    list of commands
    [ return value ]
}
```
`function`可选，`return`可选；如果不加return，会将最后一条命令运行结果作为返回值。
#### 11. 特殊变量
```
# $表示当前Shell进程的ID，即pid
echo $$
# 当前脚本的文件名
echo $0
# 传递给脚本或函数的参数。n 是一个数字，表示第几个参数。例如，第一个参数是$1，第二个参数是$2。
echo $1	
# 传递给脚本或函数的参数个数。
echo $#
# 上个命令的退出状态，或函数的返回值。
echo $?
# 传递给脚本或函数的所有参数。
echo $*
```

[Shell编程基础](http://wiki.ubuntu.org.cn/Shell%E7%BC%96%E7%A8%8B%E5%9F%BA%E7%A1%80)
[Bash脚本15分钟进阶教程](http://www.vaikan.com/bash-scripting)
[Bash快速入门指南](http://blog.jobbole.com/85183/)
[写出健壮的Bash脚本](http://blog.jobbole.com/15668/)

