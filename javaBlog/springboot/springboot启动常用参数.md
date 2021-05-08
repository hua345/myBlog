```bash
# 打包不进行单元测试
mvn install -Dmaven.test.skip=true
```

```bash
nohup java -Xms500m -Xmx500m -Xmn250m -Xss256k -server -XX:+HeapDumpOnOutOfMemoryError -jar $JAR_PATH/test-0.0.1-SNAPSHOT.jar --spring.profiles.active=DEV --server.port=8081 &
```
命令行参数

`java -jar xxx.jar --server.port=8081`

系统参数，该参数会被设置到系统变量中，使用示例如下

`java -jar -Dserver.port=8081 xxx.jar`


```bash
# mac解压jar包
unzip -x -q xxx.jar -d xxx
```