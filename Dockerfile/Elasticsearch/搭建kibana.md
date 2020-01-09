### [Kibana](https://www.elastic.co/cn/products/kibana)

- [https://www.elastic.co/cn/products/kibana](https://www.elastic.co/cn/products/kibana)
- [https://github.com/elastic/kibana](https://github.com/elastic/kibana)

`Kibana` 是一款基于 `Apache` 开源协议，使用`JavaScript`语言编写，为 `Elasticsearch` 提供分析和可视化的 Web 平台。它可以在 `Elasticsearch` 的索引中查找，交互数据，并生成各种维度的表图。

![kibana](./img/illustrated-screenshot-hero-kibana.png)

```bash
wget https://artifacts.elastic.co/downloads/kibana/kibana-7.2.0-linux-x86_64.tar.gz

tar -xzf kibana-7.2.0-linux-x86_64.tar.gz

cd kibana-7.2.0-linux-x86_64
```

```conf
vi config/kibana.yml
# Specifies the address to which the Kibana server will bind. IP addresses and host names are both valid values.
# The default is 'localhost', which usually means remote machines will not be able to connect.
# To allow connections from remote users, set this parameter to a non-loopback address.
server.host: "192.168.137.128"
# The URLs of the Elasticsearch instances to use for all your queries.
elasticsearch.hosts: ["http://192.168.137.128:9200"]


#启动kibana
./bin/kibana
# nohup ./bin/kibana > ~/kibana.log 2>&1 &

log   [08:25:26.951] [info][status][plugin:reporting@7.2.0] Status changed from uninitialized to green - Ready
log   [08:25:27.093] [info][task_manager] Installing .kibana_task_manager index template version: 7020099.
log   [08:25:27.216] [info][task_manager] Installed .kibana_task_manager index template: version 7020099 (API version 1)
log   [08:25:28.266] [info][migrations] Creating index .kibana_1.
log   [08:25:28.597] [info][migrations] Pointing alias .kibana to .kibana_1.
log   [08:25:28.678] [info][migrations] Finished in 422ms.
log   [08:25:28.681] [info][listening] Server running at http://192.168.137.128:5601
log   [08:25:29.477] [info][status][plugin:spaces@7.2.0] Status changed from yellow to green - Ready
```

#### 查看kibana显示的数据

打开[http://192.168.137.128:5601](http://192.168.137.128:5601)

![这里写图片描述](https://imgconvert.csdnimg.cn/aHR0cDovL2ltZy5ibG9nLmNzZG4ubmV0LzIwMTYxMTIyMjM0OTU0NTg2)

注意右上角是查询的时间范围，如果没有查找到数据，那么你就可能需要调整这个时间范围了，这里我选择`Today`：

![这里写图片描述](https://imgconvert.csdnimg.cn/aHR0cDovL2ltZy5ibG9nLmNzZG4ubmV0LzIwMTYxMTIyMjM0NjUzMjE4)
