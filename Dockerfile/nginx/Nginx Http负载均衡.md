# Nginx Http负载均衡

nginx反向代理实现包括下面这些负载均衡HTTP、HTTPS、Websocket、FastCGI、uwsgi，SCGI和memcached。

要配置HTTPS的负载均衡，只需使用“https”开头的协议。

当要设置FastCGI，uwsgi，SCGI，或者memcached的负载平衡，分别使用fastcgi_pass，uwsgi_pass，scgi_pass和memcached_pass指令。

```bash
Syntax: server address [parameters];
Default:  —
Context: upstream
```

## 可以定义下面的parameters

1. weight=number
 设置服务器的权重，默认是1
2. max_fails=number
默认情况下，max_fails为1。如果被设置为0，该服务器的健康检测将禁用。
3. fail_timeout=time
fail_timeout和max_fails是相关联的。在fail_timeout时间内与服务器连接尝试失败次数达到max_fails次，服务器将视为unavailable。
在fail_timeout后，nginx将检测该服务器是否存活。
默认情况下，超时时间被设置为10S。
4. backup
 标记该服务器为备用服务器。当主服务器不可用时，请求会被发送到它这里。
5. down
 标记服务器永久停机了；与指令ip_hash一起使用。
6. max_conns=number
与服务器最大连接数，默认是0,意味着没有限制。

###负载均衡策略

1. round-robin：默认方式--轮询。以轮询方式将请求分配到不同服务器上。

```nginx
http {
    upstream httpCluster {
        server 127.0.0.1:6180;
        server 127.0.0.1:6181;
        server 127.0.0.1:6182;
    }
    server {
        listen 80;

        location / {
            proxy_pass http://httpCluster;
        }
    }
}
```

1. 使用最少连接负载均衡，将下一个请求分配到连接数最少的那台服务器上。

```conf
upstream httpCluster {
    least_conn;
    server 127.0.0.1:6180;
    server 127.0.0.1:6181;
    server 127.0.0.1:6182;
}
```

1. 负载均衡的ip-hash机制，基于客户端的IP地址。散列函数被用于确定下一个请求分配到哪台服务器上

```conf
upstream httpCluster {
    ip_hash;
    server 127.0.0.1:6180;
    server 127.0.0.1:6181;
    server 127.0.0.1:6182;
}
```

1. 当指定的服务器的权重参数，权重占比为负载均衡决定的一部分。权重大负载就大。

```conf
upstream httpCluster {
    server 127.0.0.1:6180 weight = 3;
    server 127.0.0.1:6181 weight = 5;
    server 127.0.0.1:6182 weight = 7;
}
```

1. fair（第三方）
按后端服务器的响应时间来分配请求，响应时间短的优先分配。

```conf
upstream httpCluster {
    server 127.0.0.1:6180;
    server 127.0.0.1:6181;
    server 127.0.0.1:6182;
    fair;
}
```

1. url_hash（第三方）
按访问url的hash结果来分配请求，使每个url定向到同一个后端服务器，后端服务器为缓存时比较有效。
例：在upstream中加入hash语句，server语句中不能写入weight等其他的参数，hash_method是使用的hash算法

```conf
upstream httpCluster {
  server 127.0.0.1:6180;
  server 127.0.0.1:6181;
  server 127.0.0.1:6182;
  hash $request_uri;
  hash_method crc32;
}
```

- [nginx map使用方法](http://www.ttlsa.com/nginx/using-nginx-map-method/)
- [Module ngx_stream_upstream_module](http://nginx.org/en/docs/stream/ngx_stream_upstream_module.html)
- [upstream模块](http://tengine.taobao.org/book/chapter_05.html#id5)
- [使用nginx作为HTTP负载均衡](http://www.ttlsa.com/nginx/using-nginx-as-http-loadbalancer/)
