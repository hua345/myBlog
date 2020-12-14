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
~ % sudo chown -R $(chenjianhua) /usr/local/Homebrew
```