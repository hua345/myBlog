# 3.6.3版本maven打包报下面错误

```log
$ mvn --version
Apache Maven 3.6.3 (cecedd343002696d0abb50b32b541b8a6ba2883f)
Maven home: C:\MyProgramFile\apache-maven-3.6.3

$ mvn clean install
[INFO] Scanning for projects...
Downloading from alimaven: https://maven.aliyun.com/nexus/content/groups/public/org/springframework/boot/spring-boot-starter-parent/2.4.4/spring-boot-starter-parent-2.4.4.pom
[ERROR] [ERROR] Some problems were encountered while processing the POMs:
[FATAL] Non-resolvable parent POM for com.github.chenjianhua.common:json-spring-boot-starter:0.0.1-SNAPSHOT: Could not transfer artifact org.springframework.boot:spring-boot-starter-parent:pom:2.4.4 from/to alimaven (https://maven.aliyun.com/nexus/content/groups/public/): Transfer failed for https://maven.aliyun.com/nexus/content/groups/public/org/springframework/boot/spring-boot-starter-parent/2.4.4/spring-boot-starter-parent-2.4.4.pom and 'parent.relativePath' points at no local POM @ line 5, column 13
```

忽略ssl验证

```bash
mvn clean install -Dmaven.wagon.http.ssl.insecure=true -Dmaven.wagon.http.ssl.allowall=true
```
