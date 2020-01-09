# 设置名字和邮箱地址

```bash
git config --global user.name "yourname"
git config --global user.email yourname@example.com
```

- 它首先会查找/etc/gitconfig文件，该文件含有 对系统上所有用户及他们所拥有的仓库都生效的配置值（译注：gitconfig是全局配置文件）。如果传递--system选项给git config命令，Git 会读写这个文件。
- 接下来 Git 会查找系统当前用户的~/.gitconfig文件，你能传递--global选项让 Git读写该文件。
- 最后 Git 会查找当前库中 Git 目录下的配置文件（.git/config），该文件中的值只对属主库有效。

## 客户端基本配置

- **color.ui为true来打开所有的默认终端着色**

```bash
git config --global color.ui true
```

- **commit.template**。当你提交的时候，Git会默认使用该文件定义的内容。例如：你创建了一个模板文件$HOME/.gitmessage.txt，它看起来像这样

```template
subject line

what happened

[ticket: X]
```

设置`commit.template`，当运行git commit时，Git 会在你的编辑器中显示以上的内容。

```bash
git config --global commit.template $HOME/.gitmessage.txt
git commit
```

- **user.signingkey**。如果你要创建经签署的含附注的标签，那么把你的GPG签署密钥设置为配置项会更好，设置密钥ID如下

```bash
git config --global user.signingkey <gpg-key-id>
```

现在你能够签署标签，从而不必每次运行git tag命令时定义密钥

```bash
git tag -s <tag-name>
```

- **core.autocrlf**。在跨平台情况下，由于Windows使用CRLF作为行结束符，Linux和Mac系统使用LF作为行结束符，虽然它是个小问题但会扰乱跨平台协作。
在Windows系统上，autocrlf设置为true,在你提交时自动地把行结束符CRLF转换成LF，而在签出代码时把LF转换成CRLF。

```bash
git config --global core.autocrlf true
```

Linux和Mac系统上，当一个以CRLF为行结束符的文件不小心被引入时你肯定想进行修正，把core.autocrlf设置成input来告诉 Git 在提交时把CRLF转换成LF，签出时不转换。

```bash
git config --global core.autocrlf input
```

这样会在Windows系统上的签出文件中保留CRLF，会在Mac和Linux系统上，包括仓库中保留LF。

```bash
#拒绝提交包含混合换行符的文件
git config --global core.safecrlf true  

#允许提交包含混合换行符的文件
git config --global core.safecrlf false  

#提交包含混合换行符的文件时给出警告
git config --global core.safecrlf warn
```

### 参考

- [自定义 Git - 配置 Git](http://git-scm.com/book/zh/v1/%E8%87%AA%E5%AE%9A%E4%B9%89-Git-%E9%85%8D%E7%BD%AE-Git)
