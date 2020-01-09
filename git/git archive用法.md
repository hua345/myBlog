查看帮助
```
 git archive [options] <tree-ish> [<path>...]
 -o, --output <file>   write the archive to this file
 -0                    store only
 -1                    compress faster
 -9                    compress better
 -l, --list            list supported archive formats
```
运行`git archive --list`查看支持的归档格式有`tar、tgz、tar.gz、zip`

```
#导出最新的版本库
git archive -o ../latest.zip HEAD
#导出指定提交记录
git archive -o ../git-1.4.0.tar 8996b47 
#导出一个目录
git archive -o ../git-1.4.0-docs.zip  HEAD:Documentation/  
#导出为tar.gz格式
git archive   8996b47 | gzip > ../git-1.4.0.tar.gz
```
导出最后一次提交修改过的文件
　　我一直在使用这个命令定期进行发送给其他人进行审查/整合。这条命令将把近期提交的修改过的文件导出到一个zip文件。
```
git archive -o ../updated.zip HEAD $(git diff --name-only HEAD^)
```
###参考:
[git archive](http://git-scm.com/docs/git-archive)
[你不一定知道的几个很有用的 Git 命令](http://www.cnblogs.com/lhb25/p/10-useful-advanced-git-commands.html)
