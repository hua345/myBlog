# brew doctor查看健康信息

```bash
➜  Desktop brew doctor
Please note that these warnings are just used to help the Homebrew maintainers
with debugging if you file an issue. If everything you use Homebrew for is
working fine: please don't worry or file an issue; just ignore this. Thanks!

Warning: Suspicious https://github.com/Homebrew/brew git origin remote found.
The current git origin is:
  git://mirrors.ustc.edu.cn/brew.git

With a non-standard origin, Homebrew won't update properly.
You can solve this by setting the origin remote:
  git -C "/usr/local/Homebrew" remote set-url origin https://github.com/Homebrew/brew

Warning: Suspicious https://github.com/Homebrew/homebrew-core git origin remote found.
The current git origin is:
  git://mirrors.ustc.edu.cn/homebrew-core.git/

With a non-standard origin, Homebrew won't update properly.
You can solve this by setting the origin remote:
  git -C "/usr/local/Homebrew/Library/Taps/homebrew/homebrew-core" remote set-url origin https://github.com/Homebrew/homebrew-core

Warning: The following directories do not exist:
/usr/local/sbin

You should create these directories and change their ownership to your account.
  sudo mkdir -p /usr/local/sbin
  sudo chown -R $(whoami) /usr/local/sbin

Warning: You have unlinked kegs in your Cellar.
Leaving kegs unlinked can lead to build-trouble and cause brews that depend on
those kegs to fail to run properly once built. Run `brew link` on these:
  gdbm
  rabbitmq
  xz
  tmpwatch
```
