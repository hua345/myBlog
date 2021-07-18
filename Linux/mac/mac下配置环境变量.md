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

设置javaHome

```bash
echo $JAVA_HOME
#我们查看时发现mac并没有帮我们设置JAVA_HOME
ls -l /usr/libexec/java_home
lrwxr-xr-x  1 root  wheel  79 12 18 14:18 /usr/libexec/java_home -> /System/Library/Frameworks/JavaVM.framework/Versions/Current/Commands/java_home

# 编辑配置文件
vi ~/.zshrc
export JAVA_HOME=$(/usr/libexec/java_home)
export PATH=$JAVA_HOME/bin:$PATH
export CLASS_PATH=$JAVA_HOME/lib
source .bash_profile
echo $JAVA_HOME
/Library/Java/JavaVirtualMachines/openjdk.jdk/Contents/Home
```

```bash
# 查看环境变量
➜  ~ echo $PATH         
/usr/local/kafka/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Library/Apple/usr/bin
# 查看当前使用的SHELL
➜  ~ echo $SHELL 
/bin/zsh
```