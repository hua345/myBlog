### [Kibana](https://www.elastic.co/cn/products/kibana)

- [https://www.elastic.co/cn/products/kibana](https://www.elastic.co/cn/products/kibana)
- [https://github.com/elastic/kibana](https://github.com/elastic/kibana)

`Kibana` 是一款基于 `Apache` 开源协议，使用`JavaScript`语言编写，为 `Elasticsearch` 提供分析和可视化的 Web 平台。它可以在 `Elasticsearch` 的索引中查找，交互数据，并生成各种维度的表图。

![kibana](./img/illustrated-screenshot-hero-kibana.png)

```bash
# https://www.elastic.co/cn/downloads/kibana
wget https://artifacts.elastic.co/downloads/kibana/kibana-7.8.1-linux-x86_64.tar.gz

tar -xzf kibana-7.8.1-linux-x86_64.tar.gz

cd kibana-7.8.1-linux-x86_64
```

`vi config/kibana.yml`

```yml
# Kibana is served by a back end server. This setting specifies the port to use.
server.port: 5601

# Specifies the address to which the Kibana server will bind. IP addresses and host names are both valid values.
# The default is 'localhost', which usually means remote machines will not be able to connect.
# To allow connections from remote users, set this parameter to a non-loopback address.
server.host: "192.168.137.128"

# The URLs of the Elasticsearch instances to use for all your queries.
elasticsearch.hosts: ["http://192.168.137.128:9200"]
```

### 加入`systemctl`服务

```bash
vi /lib/systemd/system/kibana.service
```

```conf
[Unit]
Description=kibana Service 01
After=network.target
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=elasticsearch
Group=elasticsearch
LimitNOFILE=65536
LimitNPROC=65536
ExecStart=/home/elasticsearch/kibana-7.8.1-linux-x86_64/bin/kibana
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable kibana
systemctl start kibana
```

```yml
➜  elasticsearch systemctl status kibana
● kibana.service - kibana Service 01
   Loaded: loaded (/usr/lib/systemd/system/kibana.service; enabled; vendor preset: disabled)
   Active: active (running) since 三 2020-08-12 09:53:58 CST; 2min 19s ago
 Main PID: 32100 (node)
    Tasks: 11
   Memory: 523.6M
   CGroup: /system.slice/kibana.service
           └─32100 /home/elasticsearch/kibana-7.8.1-linux-x86_64/bin/../node/bin/node /home/elasticsearch/kibana-7.8.1-linux-x86_64/bin/../src/cli

8月 12 09:54:37 fangfang01 kibana[32100]: {"type":"log","@timestamp":"2020-08-12T01:54:37Z","tags":["status","plugin:ui_metric@7.8.1","info"],"pid":32100,"state":"green","message":"Status changed from uninitialized to green - Ready","prevState":"u...sg":"uninitialized"}
8月 12 09:54:37 fangfang01 kibana[32100]: {"type":"log","@timestamp":"2020-08-12T01:54:37Z","tags":["listening","info"],"pid":32100,"message":"Server running at http://192.168.137.129:5601"}
8月 12 09:54:38 fangfang01 kibana[32100]: {"type":"log","@timestamp":"2020-08-12T01:54:38Z","tags":["info","http","server","Kibana"],"pid":32100,"message":"http server running at http://192.168.137.129:5601"}
```

### 开放端口

```bash
➜  ~ firewall-cmd --zone=public --add-port=5601/tcp --permanent
success
# 重新载入防火墙配置，当前连接不中断
➜  ~ firewall-cmd --reload
success
```

#### 查看kibana显示的数据

打开[http://192.168.137.129:5601](http://192.168.137.129:5601)

![这里写图片描述](https://imgconvert.csdnimg.cn/aHR0cDovL2ltZy5ibG9nLmNzZG4ubmV0LzIwMTYxMTIyMjM0OTU0NTg2)

注意右上角是查询的时间范围，如果没有查找到数据，那么你就可能需要调整这个时间范围了，这里我选择`Today`：

![这里写图片描述](https://imgconvert.csdnimg.cn/aHR0cDovL2ltZy5ibG9nLmNzZG4ubmV0LzIwMTYxMTIyMjM0NjUzMjE4)
