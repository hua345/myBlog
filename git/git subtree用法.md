替代git submodule 命令, 合并子仓库到项目中并放在子目录。
### 添加子仓库
```
#添加远程分支
git remote add -f module_y git@192.168.0.190:root/module_y.git 

git subtree add --prefix=libs/module_y module_y master --squash
#-d                    show debug messages
#-P, --prefix ...      the name of the subdir to split out
```
在使用 --squash 参数的情况下， subtree add 或者 pull 操作的结果对应两个 commit， 一个是 Squash 了子项目的历史记录， 一个是 Merge 到主项目中。
### 更新仓库
```
git subtree pull --prefix=libs/module_y module_y master --squash
```
### 合并提交记录
```
git subtree merge --prefix=<prefix> <commit>
```
### 提交子仓库记录
```
git subtree push --prefix=libs/module_y module_y master --squash
```
### 切分出相关的提交
```
git subtree split --prefix=<prefix> <commit...>
#-b, --branch ...      create a new branch from the split subtree

#切换到module_y后更改子仓库就很方便了
git subtree split --prefix=libs/module_y -b module_y
git checkout module_y
git commit -m "add file"

#向module_y远程仓库提交master主分支修改
git push module_y master
```

### 参考：

- [Git submodule VS Git Subtree](http://www.tuicool.com/articles/JR3qUz)
- [Git subtree 要不要使用 –squash 参数](http://jishu.zol.com.cn/17342.html)
- [为什么使用Git Subtree](http://wenku.baidu.com/view/9767a3bc910ef12d2bf9e72d.html?from=search)
