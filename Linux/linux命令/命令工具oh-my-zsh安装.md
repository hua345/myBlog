# [oh-my-zsh github地址](https://github.com/robbyrussell/oh-my-zsh)

## 安装准备

- Unix-like operating system (macOS or Linux)
- Zsh should be installed (v4.3.9 or more recent). 
- curl or wget should be installed
- git should be installed

```bash
yum -y install zsh wget git

[root@dockerMaster]~# zsh --version
zsh 5.0.2 (x86_64-redhat-linux-gnu)
```

## 安装`oh-my-zsh`

```bash
#via curl
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

#via wget
sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"

Cloning Oh My Zsh...
正克隆到 '/root/.oh-my-zsh'...
remote: Enumerating objects: 1038, done.
remote: Counting objects: 100% (1038/1038), done.
remote: Compressing objects: 100% (954/954), done.
remote: Total 1038 (delta 23), reused 844 (delta 20), pack-reused 0
接收对象中: 100% (1038/1038), 684.73 KiB | 293.00 KiB/s, done.
处理 delta 中: 100% (23/23), done.
Looking for an existing zsh config...
Using the Oh My Zsh template file and adding it to ~/.zshrc
Time to change your default shell to zsh!
Changing shell for root.
Shell changed.
         __                                     __
  ____  / /_     ____ ___  __  __   ____  _____/ /_
 / __ \/ __ \   / __ `__ \/ / / /  /_  / / ___/ __ \
/ /_/ / / / /  / / / / / / /_/ /    / /_(__  ) / / /
\____/_/ /_/  /_/ /_/ /_/\__, /    /___/____/_/ /_/
                        /____/                       ....is now installed!


Please look over the ~/.zshrc file to select plugins, themes, and options.

p.s. Follow us at https://twitter.com/ohmyzsh

p.p.s. Get stickers, shirts, and coffee mugs at https://shop.planetargon.com/collections/oh-my-zsh

➜  ~
➜  ~
```

### 配置主题和插件

- [Themes](https://github.com/robbyrussell/oh-my-zsh/wiki/Themes)
- [Plugins](https://github.com/robbyrussell/oh-my-zsh/wiki/Plugins)

```bash
# 查看支持的插件
# Standard plugins can be found in ~/.oh-my-zsh/plugins/*
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
➜  ~ ls ~/.oh-my-zsh/plugins/

# 查看支持的主题
# a theme from this variable instead of looking in ~/.oh-my-zsh/themes/
➜  ~ ls ~/.oh-my-zsh/themes/

➜  ~ vi .zshrc
ZSH_THEME="robbyrussell"
plugins=(git docker kubectl)
```
