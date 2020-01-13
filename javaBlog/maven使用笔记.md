### 下载maven

[http://maven.apache.org/download.cgi](http://maven.apache.org/download.cgi)

### 安装java

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

### 配置maven路径

```bash
vim /etc/profile
export MAVEN_HOME=~/java/apache-maven-3.3.9
export PATH=$PATH:$MAVEN_HOME/bin

source /etc/profile
```

### 验证Maven的安装

```bash
mvn -version
Apache Maven 3.3.9 (bb52d8502b132ec0a5a3f4c09453c07478323dc5; 2015-11-11T00:41:47+08:00)
Maven home: /home/chenjianhua/java/apache-maven-3.3.9
Java version: 1.8.0_91, vendor: Oracle Corporation
Java home: /usr/lib/jvm/java-8-openjdk-amd64/jre
Default locale: zh_CN, platform encoding: UTF-8
OS name: "linux", version: "4.4.0-23-generic", arch: "amd64", family: "unix"
```

### Maven的生命周期主要有编译、测试、打包、部署

### 修改`${MAVEN_HOME}/conf/settings.xml`配置文件

#### 保存仓库的路径

```bash
<!-- localRepository
 | The path to the local repository maven will use to store artifacts.
 |
 | Default: ${user.home}/.m2/repository
<localRepository>/path/to/local/repo</localRepository>
-->
#查看下载后的仓库
ls ~/.m2/repository
```

#### 修改远程镜像仓库地址

```bash
<mirrors>
  <mirror>
    <id>alimaven</id>
    <name>aliyun maven</name>
    <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
    <mirrorOf>central</mirrorOf>
  </mirror>
</mirrors>
```

### 通过maven创建简单程序

```bash
`group Id`：com.fenby (包名)
`artifact Id`fenby （项目名）

mvn archetype:generate -DgroupId=com.fenby -DartifactId=fenby -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
```

在这个新建的项目中，我们可以看到有个`pom.xml`文件,`pom`是对象模型,有`pom.xml`说明是个`maven`项目

```bash
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/maven-v4_0_0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.fenby</groupId>
  <artifactId>fenby</artifactId>
  <packaging>jar</packaging>
  <version>1.0-SNAPSHOT</version>
  <name>fenby</name>
  <url>http://maven.apache.org</url>
  <dependencies>
    <dependency>
      <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>3.8.1</version>
      <scope>test</scope>
    </dependency>
  </dependencies>
</project>
```

#### 添加依赖包

```bash
#在`<dependencies>`标签中加入
<dependency>
  <groupId>Mysql</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>5.1.30</version>
</dependency>
```

#### 项目目录结构

| 目录               | 约定的用途                   |
| ------------------ | ---------------------------- |
| src/main/java      | 项目的java源代码             |
| src/main/resources | 项目的资源，比如property文件 |
| src/test/java/     | 项目测试类，比如Junit代码    |
| src/main/resources | 测试使用的资源               |

#### Maven -U参数

> 该参数能强制让Maven检查所有SNAPSHOT依赖更新，确保集成基于最新的状态，
>
> 如果没有该参数，Maven默认以天为单位检查更新，而持续集成的频率应该比这高很多。

#### 发布包到maven仓库

`pom.xml文件`

```xml
<!--定义snapshots库和releases库的nexus地址-->  
<distributionManagement>  
    <repository>  
        <id>nexus-releases</id>  
        <url>  
            http://172.17.103.59:8081/nexus/content/repositories/releases/  
        </url>  
    </repository>  
    <snapshotRepository>  
        <id>nexus-snapshots</id>  
        <url>  
            http://172.17.103.59:8081/nexus/content/repositories/snapshots/  
        </url>  
    </snapshotRepository>  
</distributionManagement>
```

`maven sertting.xml文件`

```xml
<server>  
  <id>nexus-releases</id>  
  <username>admin</username>  
  <password>admin123</password>  
</server>  
  
<server>  
  <id>nexus-snapshots</id>  
  <username>admin</username>  
  <password>admin123</password>  
</server>
```

> maven会根据(`pom.xml`文件中的`version`)中是否带有`-SNAPSHOT`来判断是快照版本还是正式版本。
> `maven sertting.xml文件`配置的server的`id`必须和`pom文件`中的`distributionManagement`对应仓库的`id`保持一致
> maven在处理发布时会根据id查找用户名称和密码进行登录和文件的上传发布。

### maven常用命令

```bash
#创建Maven的普通java项目
mvn archetype:generate -DgrouId=packageName -DartifactId=projectName
#创建Maven的Web项目：
mvn archetype:generate -DgroupId=packageName -DartifactId=webappName -DarchetypeArtifactId=maven-archetype-webapp
#打印整个依赖树
mvn dependency:tree
#查看有效的pom.xml信息
mvn help:effective-pom
#将项目转化为Eclipse项目
mvn eclipse:eclipse
#编译源代码
mvn compile
#运行测试
mvn test
#打包项目
mvn package
#只打jar包
mvn jar:jar  
#清除产生的中间文件
mvn clean
#在本地repository中安装jar
mvn install
#调用 Jetty 插件的 Run 目标在 Jetty Servlet 容器中启动 web 应用
mvn jetty:run
#下载源代码
mvn dependency:sources -DdownloadSources=true -DdownloadJavadocs=true
#生成eclipse的配置文件
mvn eclipse:eclipse
#查看帮助信息
mvn help:help
```

#### 保留Mybatis Mapper配置文件

```bash
<resources>
    <resource>
        <directory>src/main/java/com/github/chenjianhua
    </directory>
    <targetPath>com/github/chenjianhua</targetPath>
    <includes>
        <include>**/*.xml</include>
    </includes>
    <filtering>false</filtering>
    </resource>
</resources>
```

### 添加eclipse的maven插件

`Windows` --> `Preference` --> `Maven` --> `Installations` -->`Add`
![这里写图片描述](http://img.blog.csdn.net/20161119002140824)

#### 设置maven配置文件路径

`Windows` --> `Preference` --> `Maven` --> `User Settings`
![这里写图片描述](http://img.blog.csdn.net/20161125001546338)

### 新建maven工程

![这里写图片描述](http://img.blog.csdn.net/20161119220831490)

#### 更新工程

项目右键`Maven > Update Project`
![这里写图片描述](https://img-blog.csdn.net/20180402221253356?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NoZW5qaDIxMw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

#### 运行工程

`Spring boot`项目中`Main`方法右键`Run As > Java Application`
![这里写图片描述](https://img-blog.csdn.net/20180402221351833?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NoZW5qaDIxMw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

#### 停止程序

`Console`右边的红色按钮停止`Spring boot`
![这里写图片描述](https://img-blog.csdn.net/20180402221430862?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2NoZW5qaDIxMw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

### 调试maven项目

`右击项目> Debug As > Debug on Server`
![这里写图片描述](http://img.blog.csdn.net/20161120120933712)
