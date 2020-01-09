#### 参考
- [Linux三大剑客之sed](https://blog.csdn.net/solaraceboy/article/details/79272344)
- [linux命令总结sed命令详解](https://www.cnblogs.com/ginvip/p/6376049.html)
#### 1.简介
> grep 查找, sed 编辑, awk 根据内容分析并处理.

> sed英文全称是stream editor。由贝尔实验室开发，如今主流Unix/Linux操作系统上都集成了这个工具。
> sed由自由软件基金组织（FSF）开发和维护，并且随着GNU/Linux进行分发，通常它也称作 GNU sed。

#### 2.sed使用
> sed遵循简单的工作流：读取（从输入中读取某一行），执行（在某一行上执行sed命令）和显示（把结果显示在输出中）。
通常sed命令这样被调用：
```
➜  ~ sed --help
sed OPTIONS... [SCRIPT] [INPUTFILE...]
```
- `-n, --quiet, --silent`只输出明确处理过的内容。
- `-e 脚本, --expression=脚本`
- `-f 脚本文件, --file=脚本文件`
- `-l N, --line-length=N`

例如，把文件input.txt中出现的“hello”全部替换为“world”并输出到文件output.txt中：
```
➜  ~ echo "hello world">input.txt
➜  ~ sed "s/hello/world/" input.txt
world world
```
>如果没有指定输入文件，sed获取到是是标准出入流的内容
```
➜  ~ echo "hello world">input.txt
➜  ~ cat input.txt | sed 's/hello/world/'
world world
```
#### 3.sed 的正则表达式
|元字符|功 能|示 例|	示例的匹配对象|
|---|-----|--------|----|
|^| 行首定位符 | /^love/ | 匹配所有以 love 开头的行|
|$| 行尾定位符 | /love$/ | 匹配所有以 love 结尾的行|
|.|匹配除换行外的单个字符|/l..e/|匹配包含字符 l、后跟两个任意字符、再跟字母 e 的行|
|*|匹配零个或多个前导字符|/*love/|匹配在零个或多个空格紧跟着模式 love 的行|
|[]|匹配指定字符组内任一字符|/[Ll]ove/|匹配包含 love 和 Love 的行|
|\<|词首定位符|/\<love/|匹配包含以 love 开头的单词的行|
|\>|词尾定位符|/love\>/|	匹配包含以 love 结尾的单词的|行
#### 4.sed 操作命令
> sed 操作命令告诉 sed 如何处理由地址指定的各输入行。
如果没有指定地址， sed 就会处理输入的所有的行

| 命令|说明| 
|---|---|
|a |在当前行后添加一行或多行|
|c |用新文本修改（替换）当前行中的文本|
|d|删除一行|
|i|在某行之前插入|
|q|结束或退出 sed|
|s|用一个字符串替换另一个|

#### 5.以redis.conf作为测试
#### 5.1 `s`替换命令
替换和取代文件中的文本可以通过`sed`中的`s`来实现， s 后包含在斜杠中的文本是正则表达式，
后面跟着的是需要替换的文本。可以通过`g`标志对行进行全局替换
```
# 以bind开头的行数据用bind 127.0.0.1替代
cat redis.conf | grep bind | sed 's/^\(bind .*\)$/bind 127.0.0.1/g'
# 以daemonize开头行数据将no改为yes
cat redis.conf | grep daemonize | sed '/^daemonize/s/no/yes/g'
# 以daemonize开头行数据用#注释
cat redis.conf | grep daemonize | sed 's/^\(daemonize .*\)$/# \1/'
# 以dir开头的数据用#注释,在下面一行添加dir /data
cat redis.conf | grep 'dir ' | sed 's/^\(dir .*\)$/# \1\ndir \/data/'
```
#### 5.2 `a`追加命令
> a 命令是追加命令，追加将新文本到文件中当前行(即读入模式的缓存区行)的后面。
不管是在命令行中，还是在 sed 脚本中， a 命令总是在反斜杠的后面。
```
cat redis.conf | grep bind | sed '/^\(bind .*\)$/a hello'
```
#### 5.3 `i`在某行之前插入
> 类似于 a 命令，但不是在当前行后增加文本，而是在当前行前面插入新的文本，即刚读入缓存区模式的行。
```
cat redis.conf | grep bind | sed '/^\(bind .*\)$/i hello'
```
#### 5.4 `c`修改命令
> sed 使用该命令将已有的文本修改成新的文本。旧文本被覆盖。
```
cat redis.conf | grep bind | sed '/^\(bind .*\)$/c bind 0.0.0.0'
cat redis.conf | grep unixsocketperm |sed 's/^# unixsocketperm 700/unixsocketperm 777/'
```
