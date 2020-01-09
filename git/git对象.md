>Git 是一个内容寻址文件系统。Git 是一个内容寻址文件系统。 看起来很酷， 但这是什么意思呢？ 这意味着，Git 的核心部分是一个简单的键值对数据库（key-value data store）。 你可以向该数据库插入任意类型的内容，它会返回一个键值，通过该键值可以在任意时刻再次检索（retrieve）该内容。 可以通过底层命令 hash-object 来演示上述效果——该命令可将任意数据保存于 .git 目录，并返回相应的键值。
git仓库中有`Commits`,`Trees`,`Blobs`和` Tags`对象．一个树对象可以包含了一条或多条树对象记录（tree entry），每条记录含有一个指向数据对象或者子树对象的 SHA-1 指针，以及相应的模式、类型、文件名信息。

### blob对象
```bash
#git-hash-object - Compute object ID and optionally creates a blob from a file

echo 'test content' | git hash-object -w --stdin
d670460b4b4aece5915caf5c68d12f560a9fe3e4
#-w Actually write the object into the object database.
#--stdin Read the object from standard input instead of from a file.

#可以通过 cat-file 命令从 Git 那里取回数据。
git cat-file -p d670460b4b4aece5915caf5c68d12f560a9fe3e4
#计算文件的SHA
echo 'version 1' > test.txt
git hash-object -w test.txt
83baae61804e65cc73a7201a7252750c76066a30
#查看对象的类型
git cat-file -t 83baae61804e65cc73a7201a7252750c76066a30
blob
```
### tree对象
```
#write-tree - Create a tree object from the current index
git write-tree
3478b7104ac7ba61ffb65c06a6cd7d1b8555c4d0

git cat-file -p 3478b7104ac7ba61ffb65c06a6cd7d1b8555c4d0
100644 blob 3478b7104ac7ba61ffb65c06a6cd7d1b8555c4d0	README
#检查对象类型
git cat-file -t 3478b7104ac7ba61ffb65c06a6cd7d1b8555c4d0
tree

#read-tree - Reads tree information into the index
#--prefix选项，将树对象中的文件读入到--prefix指定的目录
git read-tree --prefix=tree_content 3478b7104ac7ba61ffb65c06a6cd7d1b8555c4d0
```
### commit对象
```
#commit-tree 命令创建一个提交对象，为此需要指定一个树对象的SHA-1值
#对使用write-tree生成的tree进行提交
git commit-tree <tree> [(-p <parent>)…​]　[(-m <message>)…​]
git commit-tree -m "commit-tree" 3478b7
9864bb794428954e5466fc52580d286014e5912f

#通过 cat-file 命令查看这个新提交对象
git cat-file -p 9864bb794428954e5466fc52580d286014e5912f
tree 3478b7104ac7ba61ffb65c06a6cd7d1b8555c4d0
author chenjianhua <c2290910211@163.com> 1456929760 +0800
committer chenjianhua <c2290910211@163.com> 1456929760 +0800

commit-tree

#引用上一个提交,需要指定上一个提交对象
git write-tree　
5259f2aa64fceba122693f8d108f24d555ea60d3
git commit-tree  5259f2a -p 9864bb -m commit-tree2
78dc1fcb4396dbe6c79fab82ce1ea2fe72ca4562

#更新HEAD分支SHA
git update-ref HEAD 78dc1fcb4396dbe6c79fab82ce1ea2fe72ca4562
#查看commit完整内容
git log --format=full
commit 78dc1fcb4396dbe6c79fab82ce1ea2fe72ca4562
Author: chenjianhua <c2290910211@163.com>
Commit: chenjianhua <c2290910211@163.com>

    commit-tree2
#查看HEAD指针移动记录
git reflog
```
### 其他有用的底层命令
```bash
#查看本地分支
git show-ref
78dc1fcb4396dbe6c79fab82ce1ea2fe72ca4562 refs/heads/master
db68642728c06120abd520a89a7de35db0071004 refs/remotes/origin/HEAD
db68642728c06120abd520a89a7de35db0071004 refs/remotes/origin/master
#查看仓库对象
git count-objects -v
count: 9
size: 36
in-pack: 58
packs: 1
size-pack: 8
prune-packable: 0
garbage: 0
size-garbage: 0
#查看仓库打包文件
git verify-pack -v .git/objects/pack/pack-***.idx
#生成bitmap文件
git repack -a --window=10 --depth=50 --write-bitmap-index
```
### 参照:

- [Git 内部原理 - Git 对象](http://git-scm.com/book/zh/v2/Git-%E5%86%85%E9%83%A8%E5%8E%9F%E7%90%86-Git-%E5%AF%B9%E8%B1%A1)

