# brew服务管理

## 查看帮助

```yaml
➜  ~ brew help
Example usage:
  brew search [TEXT|/REGEX/]
  brew info [FORMULA...]
  brew install FORMULA...
  brew update
  brew upgrade [FORMULA...]
  brew uninstall FORMULA...
  brew list [FORMULA...]

➜  ~ brew services -h  
Usage: brew services [subcommand]

Manage background services with macOS' launchctl(1) daemon manager'.

If sudo is passed, operate on /Library/LaunchDaemons (started at boot).
Otherwise, operate on ~/Library/LaunchAgents (started at login).

[sudo] brew services [list]:
    List all managed services for the current user (or root).

[sudo] brew services run (formula|--all):
    Run the service formula without registering to launch at login (or boot).

[sudo] brew services start (formula|--all):
    Start the service formula immediately and register it to launch at login
(or boot).

[sudo] brew services stop (formula|--all):
    Stop the service formula immediately and unregister it from launching at
login (or boot).

[sudo] brew services restart (formula|--all):
    Stop (if necessary) and start the service formula immediately and register
it to launch at login (or boot).

[sudo] brew services cleanup:
    Remove all unused services
```

```bash
# 安装服务
brew install redis
# 列出所有服务
➜  ~ brew services list
Name  Status  User        Plist
mysql started chenjianhua /Users/chenjianhua/Library/LaunchAgents/homebrew.mxcl.mysql.plist
redis started chenjianhua /Users/chenjianhua/Library/LaunchAgents/homebrew.mxcl.redis.plist

#运行服务,开机不自动启动
brew services run redis
# 启动服务,开机自动启动
brew services start redis
# 停止，并取消开机自动启动
brew services stop redis
# 重启，并且注册开机自动启动
brew services restart redis
```
