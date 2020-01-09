在大规模异地git使用场景中，为了减小主服务器压力和使用效率，可能会添加本地只读镜像服务器，在git客户端可以分别指定push URL和fetch  URL或者对git代理进行读写分离．

### 修改push URL
```
git push --help
#替换旧的URL,真正生效的是actual url
[url "<actual url base>"]
                           insteadOf = <other url base>
#只修改真正push的URL
[url "<actual url base>"]
                           pushInsteadOf = <other url base>

＃例如：
[remote "origin"]
        url = http://fetch.example.com/git-repo.git
        fetch = +refs/heads/*:refs/remotes/origin/*
[url "http://push.example.com"]
    pushInsteadOf = http://fetch.example.com
```
也可以使用git命令设置
```
git config --help
url.<base>.insteadOf
url.<base>.pushInsteadOf
git config url.http://push.example.com.pushInsteadOf http://fetch.example.com
```
也可以在remote中指定push URL和refs,当push时会使用指定的pushurl和refspec
```
[remote "<name>"]
        url = <url>
        pushurl = <pushurl>
        push = <refspec>
        fetch = <refspec>
```
### 输出格式
```
#输出日志格式
<flag> <summary> <from> -> <to> (<reason>)
#--porcelain，日志格式
 <flag> \t <from>:<to> \t <summary> (<reason>)
#--progress，将处理信息输出到标准错误输出，方便脚本处理日志
```
### 设置自动登录
```bash
＃设置登录用户名
git config credential.https://example.com.username foo
[credential "https://github.com"]
        username = foo
＃记录登录的用户名和密码,存储文件默认在'~/.git-credentials'
git config credential.helper 'cache --timeout=300'
git config credential.helper store
＃输入一次密码后，之后就可以不用输入用户名和密码了

＃'~/.git-credentials'存储方式为plaintext，可以将文件复制到到其他服务器
https://user:pass@example.com

```
