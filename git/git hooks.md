Git 默认会放置一些脚本样本在.git/hooks，除了可以作为钩子(hooks)使用，这些样本本身是可以独立使用的。所有的样本都是shell脚本，其中一些还包含了Perl的脚本，不过，任何正确命名的可执行脚本都可以正常使用--可以用Ruby、Python和nodejs等脚本。将样本的.sample结尾去除，就可以激活脚本了。

按照Git Hooks脚本所在的位置可以分为两类：

- 本地Hooks，触发事件如commit、rebase、merge等。
- 服务端Hooks，触发事件如receive等。。
### Commit Hooks
与git commit相关的hooks一共有四个，均由git commit命令触发调用，按照一次发生的顺序分别是：

- pre-commit
- prepare-commit-msg
- commit-msg
- post-commit

pre-commit`挂钩在键入提交信息前运行，被用来检查即将提交的快照，例如，检查是否有东西被遗漏，确认测试是否运行，以及检查代码。当从该挂钩返回非零值时，Git 放弃此次提交，但可以用git commit --no-verify来忽略。该挂钩可以被用来检查代码错误（运行类似lint的程序），检查尾部空白（默认挂钩是这么做的），检查新方法（译注：程序的函数）的说明。

`prepare-commit-msg`挂钩对通常的提交来说不是很有用，只在自动产生的默认提交信息的情况下有作用，如提交信息模板、合并、压缩和修订提交等。可以和提交模板配合使用，以编程的方式插入信息。
它可能接受1到3个参数.
第一个参数是包含commit msg的文件路径.
第二个参数是commit msg的提交类型, 可能的值有:
  `message` (当使用`-m` 或`-F` 选项);
  `template` (当使用`-t` 选项,或`commit.template`配置项已经被设置);
  `merge` (当commit是一个merge或者`.git/MERGE_MSG`存在);
  `squash`(当`.git/SQUASH_MSG`文件存在);
  `commit`, 且附带该commit的SHA1校验和 (当使用`-c`, `-C` 或 `--amend`).
如果以非0状态退出, 'git commit' 将会被取消.
示例`prepare-commit-msg` hook是准备一个merge的冲突列表.

`commit-msg`挂钩接收一个参数，此参数是包含最近提交信息的临时文件的路径。如果该挂钩脚本以非零退出，Git 放弃提交，因此，可以用来在提交通过前验证项目状态或提交信息。.

缺省的'commit-msg' hook, 当启用时,将检查重复的"Signed-off-by"行, 如果找到,则取消commit.

`post-commit`挂钩在整个提交过程完成后运行，他不会接收任何参数
这个钩子主要用于通知,总之，该挂钩是作为通知之类使用的。
###E-mail工作流挂钩
有3个客户端挂钩用于E-mail工作流挂钩,当运行git am命令时,会调用他们。运行次序：

- applypatch-msg
- pre-applypatch
- post-applypatch

首先运行的是applypatch-msg挂钩，他接收一个参数：包含被建议提交信息的临时文件名。如果该脚本非零退出，Git 放弃此补丁。可以使用这个脚本确认提交信息是否被正确格式化，或让脚本编辑信息以达到标准化。

下一个在git am运行期间调用是`pre-applypatch`挂钩。该挂钩不接收参数，在补丁被运用之后运行，因此，可以被用来在提交前检查快照。你能用此脚本运行测试，检查工作树。如果有些什么遗漏，或测试没通过，脚本会以非零退出，放弃此次git am的运行，补丁不会被提交。

最后在git am运行期间调用的是post-applypatch挂钩。你可以用他来通知一个小组或获取的补丁的作者，但无法阻止打补丁的过程。
###其他客户端挂钩
####pre-rebase
`pre-rebase`挂钩在衍合前运行，脚本以非零退出可以中止衍合的过程。你可以使用这个挂钩来禁止衍合已经推送的提交对象, `pre-rebase`挂钩样本就是这么做的。
####post-checkout
在`git checkout`成功运行后，`post-checkout`挂钩会被调用。他可以用来为你的项目环境设置合适的工作目录。例如：放入大的二进制文件、自动产生的文档或其他一切你不想纳入版本控制的文件。
这个hook接受3个参数: 之前HEAD的ref,新HEAD的ref,一个标记(1-改变分支,0-恢复文件)
####post-merge
最后，在`merge`命令成功执行后，`post-merge`挂钩会被调用, 如果合并失败(冲突)不会执行。可以用来在 Git 无法跟踪的工作树中恢复数据，诸如权限数据。该挂钩同样能够验证在 Git 控制之外的文件是否存在，因此，当工作树改变时，你想这些文件可以被复制。这个钩子接受一个参数, 一个状态标记。源码中的[contrib/hooks/setgitperms.perl](https://github.com/git/git/tree/master/contrib/hooks/setgitperms.perl),演示了如何使用这个功能.
####pre-auto-gc
`pre-auto-gc`这个挂钩由`git gc --auto`触发. 它不接受参数, 非0状态退出,将导致`git gc --auto`被取消。源码中[contrib/hooks/pre-auto-gc-battery](https://github.com/git/git/blob/master/contrib/hooks/pre-auto-gc-battery),演示了在电池状态(笔记本电脑没插电源)时,拒绝执行git gc的功能)
#### post-rewrite
`post-rewrite`挂钩由修改commit的命令所触发。
```
git commit --amend #修改最后一次提交内容
git rebase -i master   #将某个分支衍合到master分支
```
它的第一个参数,表示当前是什么命令所触发:`amend` 或 `rebase`。
通过标准输入的文本格式  
```
<old-sha1> SP <new-sha1> [ SP <extra-info> ] LF
#SP 空格 LF换行
```

#### pre-push
`pre-push`挂钩可用于检查是否能被推送。有两个参数，第一个是远程推送地址名称，第二个是远程推送地址URL。由`git push`命令触发，在检查远程状态之后，任何文件被推送之前。可以读取标准输入格式
```
 <local_ref> SP <local_sha1> SP <remote_ref> SP <remote_sha1> LF
```
```python
#!/usr/bin/env python
import sys

print "hook name" , sys.argv[0] 
print "remote" , sys.argv[1] 
print "URL" , sys.argv[2] 
line = sys.stdin.readline()
if line.strip() != '':
	print "line" , line
	arr = line.split(' ')
	print "local_ref", arr[0]
	print "local_sha1", arr[1]
	print "remote_ref", arr[2]
	print "remote_sha1", arr[3]
else:
	print "False"
```


### 服务器端挂钩

#### pre-receive 和 post-receive
处理来自客户端的推送（push）操作时最先执行的脚本就是` pre-receive `。它从标准输入（stdin）获取被推送引用的列表；如果它退出时的返回值不是0，所有推送内容都不会被接受。利用此挂钩脚本可以实现类似保证最新的索引中不包含非fast-forward类型的这类效果；抑或检查执行推送操作的用户拥有创建，删除或者推送的权限或者他是否对将要修改的每一个文件都有访问权限。
每个接收操作,仅执行一次. 它不接受参数,但可以从标准输入读取以下格式的文本:
```
<old-value> SP <new-value> SP <ref-name> LF
#<old-value>是ref中原本的Object名，即sha1校验和
#<new-value>是ref中老的Object名 and
#<ref-name> 是ref的全名.
```
`post-receive`挂钩在整个过程完结以后运行，可以用来更新其他系统服务或者通知用户。它接受与 `pre-receive` 相同的标准输入数据。
源码中[post-receive-email](https://github.com/git/git/tree/master/contrib/hooks/post-receive-email)样本，实现了Email通知功能。

### update && post-update
`update `挂钩和 `pre-receive `挂钩十分类似。不同之处在于它会为推送者更新的每一个分支运行一次。假如推送者同时向多个分支推送内容，pre-receive 只运行一次，相比之下 update 则会为每一个更新的分支运行一次。它不会从标准输入读取内容，而是接受三个参数：索引的名字（分支），推送前索引指向的内容的 SHA-1 值，以及用户试图推送内容的 SHA-1 值。如果 update 脚本以退出时返回非零值，只有相应的那一个索引会被拒绝；其余的依然会得到更新。
这个hook可以用于防止特定的分支被'force'推送可以确保"fast-forward only"这一安全准则.


### hook列表:
|钩子名字          |触发命令    |参数|非0导致取消  |备注|
|----------------|------------|---|---------- |----|
|pre-commit        |git commit  |0   |Yes||
|prepare-commit-msg|git commit  |1~3 |Yes||
|commit-msg        |git commit  |1   |Yes||
|post-commit       |git commit  |0   |No ||
|applypatch-msg    |git am      |1   |Yes||
|pre-applypatch    |git am      |0   |Yes||
|post-applypatch   |git am      |0   |No ||
|pre-rebase        |git rebase  |2   |Yes||
|post-checkout     |git checkout|3   |No ||
|post-merge        |git merge   |1   |No ||
|post-rewrite      |--amend or rebase|1   |No |通过标准输入获取信息|
|pre-push          |git push|2   |Yes|通过标准输入获取信息|
|pre-receive       |git-receive-pack |0   |Yes|通过标准输入获取信息|
|update            |git-receive-pack |3   |Yes||
|post-receive      |git-receive-pack |0   |No |通过标准输入获取信息|
|post-update       |git-receive-pack |可变|No ||

### 参照:

- [Documentation/githooks.txt](https://github.com/git/git/blob/master/Documentation/githooks.txt)
- [hooks示例](https://github.com/git/git/tree/master/templates)
- [自定义 Git - Git挂钩](http://git-scm.com/book/zh/v1/%E8%87%AA%E5%AE%9A%E4%B9%89-Git-Git%E6%8C%82%E9%92%A9)
- [git hooks 机制](http://www.360doc.com/content/12/0606/23/10140166_216510889.shtml)


