# jdk安装

- [http://jdk.java.net/](http://jdk.java.net/)

## linux环境

```bash
sudo apt-get install default-jre
sudo apt-get install default-jdk
#通过这个命令看到java安装路径
sudo update-alternatives --config java
/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java
#配置环境变量
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
export PATH=$JAVA_HOME/bin:$JRE_HOME/bin:$PATH
```

## mac环境

```bash
➜  ~ brew install java
==> Downloading https://mirrors.ustc.edu.cn/homebrew-bottles/bottles/openjdk-15.
######################################################################## 100.0%
==> Pouring openjdk-15.0.1.big_sur.bottle.tar.gz
==> Caveats
For the system Java wrappers to find this JDK, symlink it with
  sudo ln -sfn /usr/local/opt/openjdk/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk

openjdk is keg-only, which means it was not symlinked into /usr/local,
because it shadows the macOS `java` wrapper.

If you need to have openjdk first in your PATH run:
  echo 'export PATH="/usr/local/opt/openjdk/bin:$PATH"' >> ~/.zshrc

For compilers to find openjdk you may need to set:
  export CPPFLAGS="-I/usr/local/opt/openjdk/include"

==> Summary
🍺  /usr/local/Cellar/openjdk/15.0.1: 614 files, 324.9MB

# 设置软连接
➜  ~ sudo ln -sfn /usr/local/opt/openjdk/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk
Password:
# 查看版本号
➜  ~ java --version
openjdk 15.0.1 2020-10-20
OpenJDK Runtime Environment (build 15.0.1+9)
OpenJDK 64-Bit Server VM (build 15.0.1+9, mixed mode, sharing)

# 安装java8
# 下载包所有版本
brew tap AdoptOpenJDK/openjdk
# 搜索包信息
➜  ~ brew search openjdk     
==> Formulae
openjdk ✔                  openjdk@11                 openjdk@8

➜  ~ brew search adoptopenjdk 
==> Casks
adoptopenjdk                             adoptopenjdk13-openj9-jre-large
adoptopenjdk-jre                         adoptopenjdk13-openj9-large
adoptopenjdk-openj9                      adoptopenjdk14
adoptopenjdk-openj9-jre                  adoptopenjdk14-jre
adoptopenjdk-openj9-jre-large            adoptopenjdk14-openj9
adoptopenjdk-openj9-large                adoptopenjdk14-openj9-jre
adoptopenjdk10                           adoptopenjdk14-openj9-jre-large
adoptopenjdk11                           adoptopenjdk14-openj9-large
adoptopenjdk11-jre                       adoptopenjdk15
adoptopenjdk11-openj9                    adoptopenjdk15-jre
adoptopenjdk11-openj9-jre                adoptopenjdk15-openj9
adoptopenjdk11-openj9-jre-large          adoptopenjdk15-openj9-jre
adoptopenjdk11-openj9-large              adoptopenjdk15-openj9-jre-large
adoptopenjdk12                           adoptopenjdk15-openj9-large
adoptopenjdk12-jre                       adoptopenjdk8
adoptopenjdk12-openj9                    adoptopenjdk8
adoptopenjdk12-openj9-jre                adoptopenjdk8-jre
adoptopenjdk12-openj9-jre-large          adoptopenjdk8-openj9
adoptopenjdk12-openj9-large              adoptopenjdk8-openj9-jre
adoptopenjdk13                           adoptopenjdk8-openj9-jre-large
adoptopenjdk13-jre                       adoptopenjdk8-openj9-large
adoptopenjdk13-openj9                    adoptopenjdk9
adoptopenjdk13-openj9-jre
# 下载Java8
brew cask install adoptopenjdk8

sudo ln -sfn /usr/local/opt/openjdk@8/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-8.jdk
```

