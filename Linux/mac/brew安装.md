# brew安装

- [https://github.com/Homebrew/brew](https://github.com/Homebrew/brew)
- [https://brew.sh](https://brew.sh)
- [https://mirrors.tuna.tsinghua.edu.cn/help/homebrew/](https://mirrors.tuna.tsinghua.edu.cn/help/homebrew/)

```bash
# 官方的安装方法，但是会有网络问题
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## 推荐的安装方法

```bash
# 同步brew.git库
sudo git clone git://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git /usr/local/Homebrew
# 软连接
sudo ln -s /usr/local/Homebrew/bin/brew /usr/local/bin/brew
# 同步core库
sudo git clone git://mirrors.ustc.edu.cn/homebrew-core.git/ /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core

sudo git clone git://mirrors.ustc.edu.cn/homebrew-cask.git/ /usr/local/Homebrew/Library/Taps/homebrew/homebrew-cask

sudo git clone git://mirrors.ustc.edu.cn/homebrew-cask-versions.git/ /usr/local/Homebrew/Library/Taps/homebrew/homebrew-cask-versions
# 查看版本号
~ % brew -v
Homebrew 2.6.1-86-gced0da1
Homebrew/homebrew-core (git revision 5820; last commit 2020-12-14)

# 替换homebrew镜像地址
~ % cd "$(brew --repo)"
Homebrew % sudo git remote set-url origin git://mirrors.ustc.edu.cn/brew.git
# bash用户
～ % echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.bash_profile
～ % source ~/.bash_profile
# zsh用户
～ % echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.zshrc
～ % source ~/.zshrc

# brew更新
~ % brew update
Error: /usr/local/Homebrew is not writable. You should change the
ownership and permissions of /usr/local/Homebrew back to your
user account:
  sudo chown -R $(whoami) /usr/local/Homebrew
# 设置当前用户权限
~ % sudo chown -R $(whoami) /usr/local/Homebrew
```

## brew使用

```bash
# search搜索包
➜  ~ brew search java         
==> Formulae
app-engine-java            java11                     jslint4java
google-java-format         javacc                     libreadline-java
java ✔                     javarepl                   pdftk-java

# info查看包信息
➜  ~ brew info java  
openjdk: stable 15.0.1 (bottled) [keg-only]
Development kit for the Java programming language
https://openjdk.java.net/
/usr/local/Cellar/openjdk/15.0.1 (614 files, 324.9MB)
  Poured from bottle on 2020-12-14 at 16:15:08
From: git://mirrors.ustc.edu.cn/homebrew-core.git//Formula/openjdk.rb
License: Cannot Represent

```
