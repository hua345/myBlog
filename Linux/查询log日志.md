[TOC]

# 查询log日志

## less查询

`less -N -m test.log`浏览单个文件
`ps -ef | less   ps`查看进程信息并通过less分页显示
`history | less`查看命令历史使用记录并通过less分页显示
`less -N -m test01.log test02.log` 浏览多个文件

```yaml
less --help: 显示帮助
-N: 显示每行的行号
-i: 忽略搜索时的大小写
-m: 显示类似more命令的百分比
/关键字: 向下搜索关键字Search forward for (N-th) matching line
?关键字: 向上搜索关键字Search backward for (N-th) matching line
n: 可以查看下一个关键字
N: 可以查看上一个关键字
g: 跳到第一行Go to first line in file
G: 跳到文件尾部Go to last line in file
b: 向后翻一页Backward one window
f: 向后翻一页Forward  one window
q  :q  Q: 退出less 命令
```



## grep查询

```yaml
grep --help
Usage: grep [OPTION]... PATTERN [FILE]...
Search for PATTERN in each FILE.
Example: grep -i 'hello world' menu.h main.c

-G, --basic-regexp        PATTERN is a basic regular expression (default) 默认使用基础正则
-i, --ignore-case         ignore case distinctions忽略大小写
-w, --word-regexp         force PATTERN to match only whole words匹配整个单词
-x, --line-regexp         force PATTERN to match only whole lines匹配整个行
-n, --line-number         print line number with output lines显示行号

grep -i 'hello world' menu.h main.c
```



