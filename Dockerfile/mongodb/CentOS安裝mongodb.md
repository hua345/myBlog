### 下载[mongodb](https://www.mongodb.org/)

```bash
wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu1404-3.0.6.tgz
tar -zvxf mongodb-linux-x86_64-ubuntu1404-3.0.6.tgz
```

我们把在mongodb目录下新建一个data目录存放数据、新建一个log目录存放日志，然后在该目录下新建一个日志文件，例如我们命名为mongodb.log

```bash
mkdir data
mkdir log
cd log && touch mongodb.log
```

### 启动mongodb

```bash
＃查看帮助
./bin/mongod --help

./bin/mongod -port 27017  --dbpath data/ --logpath log/mongodb.log  --fork
#--fork后台运行
```

### 客户端端连接mongodb

```bash
./bin/mongo localhost:27017
db.foo.save({hello:'world'})
#WriteResult({ "nInserted" : 1 })
db.foo.find()
#{ "_id" : ObjectId("5605007847084d1e6c9a5b10"), "hello" : "world" }

```

### 通过配置文件来配置mongodb

```bash
vi mongod.conf
port=27017
dbpath=data/
logpath=log/mongodb.log
logappend=true          #--logappend
auth=true               #--auth
httpinterface=true      #--httpinterface
rest=true               #--rest
fork=true               #--fork
```

```bash
./bin/mongod  -f mongod.conf
```

### 关闭mongodb

```bash
./bin/mongodb --dbpath data  --shutdown
```

### 参照

[./bin/mongod --help](https://docs.mongodb.org/manual/reference/program/mongod/)
[./bin/mongo   --help](https://docs.mongodb.org/manual/reference/program/mongo/)
[Mongodb在Linux下的安装和启动和配置](http://chenzhou123520.iteye.com/blog/1582179)
