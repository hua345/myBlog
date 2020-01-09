```
#下载haproxy
#http://www.haproxy.org/download/1.5/src/
tar -zvxf haproxy-1.5.15.tar.gz
cd haproxy-1.5.15

#编译haproxy
less README  # 安装方法从此处查看
#- linux2628   for Linux 2.6.28, 3.x, and above (enables splice and tproxy)
make TARGET=linux2628 PREFIX=/usr/local/haproxy
make install PREFIX=/usr/local/haproxy

#加入环境变量
vi /etc/profile
export PATH=$PATH:/usr/local/haproxy/sbin
source /etc/profile

#在源码目录中，查看配置示例
less examples/examples.cfg
less doc/configuration.txt
```
使用nodejs作为测试服务器
```nodejs
const http = require('http');

const hostname = '127.0.0.1';
const port = 9001;

http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello World from 1\n');
}).listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
```
```
global                #全局设置
  log 127.0.0.1   local0 #日志输出配置，所有日志都记录在本机，通过local0输出
  ulimit-n 82000       #设置每个进程的可用的最大文件描述符
  maxconn 4096        #最大连接数
  chroot /usr/local/haproxy    #改变当前工作目录
  uid 0                       #所属运行的用户uid
  gid 0                       #所属运行的用户组
  daemon                   #以后台形式运行ha-proxy
  pidfile /usr/local/haproxy/run/haproxy.pid     #pid文件位置
  quiet     #安静模式，启动时无输出
  #debug        #调试模式，输出启动信息到标准输出

defaults                       #默认设置
  mode http
  timeout connect 30s          
  timeout client 300s
  timeout server 300s
  timeout http-keep-alive 30s
  stats uri /stats　　　　　　　　#监控页面的访问地址
  stats realm Global\ statistics
  stats auth admin:admin       #监控页面认证信息
  stats hide-version           #隐藏统计页面的HAproxy版本信息


backend test_read
  mode http
  balance roundrobin
  server node2 127.0.0.1:9002 weight 5 check inter 2000 rise 2 fall 3
  server node2 127.0.0.1:9003 weight 5 check inter 2000 rise 2 fall 3
  # weight 权重
  # check inter 2000 检测心跳频率
  # #rise 2是2次正确认为服务器可用，fall 3是3次失败认为服务器不可用

backend test_write
  mode http
  balance roundrobin
  server node1 127.0.0.1:9001 weight 5 check inter 2000 rise 2 fall 3

frontend http-in
  log global
  bind *:80
  capture request header Host len 20
  acl is_read url_sub  read
  acl is_write url_sub write
  default_backend test_read
  use_backend test_write if is_write
  use_backend test_read if is_read
```
```
vi /etc/haproxy/haproxy.cfg
haproxy -f /etc/haproxy/haproxy.cfg -c
haproxy -f /etc/haproxy/haproxy.cfg

# curl http://127.0.0.1/write
Hello World from 1
# curl http://127.0.0.1/read
Hello World from 2
# curl http://127.0.0.1/read
Hello World from 3
```

