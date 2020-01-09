使用 submodule 有助于项目模块划分，提高 git 管理的性能。

```
demo
|-- .git/
|-- .gitignore
|-- lib
|-- README
```

### 添加子模块

注意需要在保存子模块的目录 lib 下执行

```
git submodule add git@192.168.0.190:root/module_x.git
```

查看缓冲区 Index 变化

```
git status

        new file:   .gitmodules
        new file:   lib/module_x
```

首先应当注意到新的 .gitmodules 文件。 该置文件保存了项目 URL 与已经拉取的本地目录之间的映射：

```
cat .gitmodules
[submodule "lib/module_x"]
        path = lib/module_x
        url = git@192.168.0.190:root/module_x.git
```

### 更新子模块

```bash
#更新带有submodule的项目
git submodule update --remote
Submodule path 'lib/module_y': checked out '65441273ea8d226bb5390e83e8ca76e78807
3f68'
#在主项目中提交子模块更新
git commit -a -m "update module_y"
#如果你的 submodule 又依赖了 submodule
git submodule foreach git submodule update
```

### 克隆含有子模块的项目

接下来我们将会克隆一个含有子模块的项目。 当你在克隆这样的项目时，默认会包含该子模块目录，但其中还没有任何文件：

```
git clone git@192.168.0.190:root/demo.git
```

你必须运行两个命令：git submodule init 用来初始化本地配置文件，而 git submodule update 则从该项目中抓取所有数据并检出父项目中列出的合适的提交。

```
git submodule init
git submodule update
```

不过还有更简单一点的方式。 如果给 git clone 命令传递 --recursive 选项，它就会自动初始化并更新仓库中的每一个子模块。

```
git clone --recursive git@192.168.0.190:root/demo.git
```

### 参照:

- [Git-子模块](http://git-scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E5%AD%90%E6%A8%A1%E5%9D%97)
- [Git Submodule 的坑](http://blog.devtang.com/blog/2013/05/08/git-submodule-issues/)
