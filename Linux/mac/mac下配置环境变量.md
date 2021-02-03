# mac下配置环境变量

## 环境变量文件的优先级

```bash
# 全局配置
/etc/profile
# 全局建议修改这个文件
/etc/paths
# 一般在这个文件中添加用户级环境变量,当用户登录时,该文件仅仅执行一次!
~/.bash_profile 
~/.bashrc
# 使用zsh命令行时配置
~/.zshrc
```

## 设置环境变量

```bash
vi ~/.zshrc
export KAFKA_HOME=/usr/local/kafka
export PATH=$KAFKA_HOME/bin:$PATH
source ~/.zshrc
```

```bash
# 查看环境变量
➜  ~ echo $PATH         
/usr/local/kafka/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Library/Apple/usr/bin
# 查看当前使用的SHELL
➜  ~ echo $SHELL 
/bin/zsh
```