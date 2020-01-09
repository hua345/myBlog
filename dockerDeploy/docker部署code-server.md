> [code-server](https://github.com/cdr/code-server) 是`VS Code`运行在服务器端，通过浏览器进行访问。

#### 启动`code-server`
```
docker pull codercom/code-server
mkdir ~/codeServer

# 不需要登录
docker run -d -p 8443:8443  -u root -v ~/codeServer:/home/coder/project codercom/code-server --allow-http --no-auth
# 需要登录
[root@code-server ~]# docker run -d -p 8443:8443 -u root -v ~/codeServer:/home/coder/project codercom/code-server --allow-http
fa22fabfa095a77a545d362229add2808e072aa6e86f500ed69b5469eb25b9b1

[root@code-server ~]# docker logs fa22fabfa095a77a545d362229add2808e072aa6e86f500ed69b5469eb25b9b1
(node:6) [DEP0005] DeprecationWarning: Buffer() is deprecated due to security and usability issues. Please use the Buffer.alloc(), Buffer.allocUnsafe(), or Buffer.from() methods instead.
INFO  code-server development
INFO  Additional documentation: http://github.com/codercom/code-server
INFO  Initializing {"data-dir":"/home/coder/.local/share/code-server","extensions-dir":"/home/coder/.local/share/code-server/extensions","working-dir":"/home/coder/project","log-dir":"/home/coder/.cache/code-server/logs/20190510072214475"}
INFO  Starting shared process [1/5]...
INFO  Starting webserver... {"host":"0.0.0.0","port":8443}
WARN  No certificate specified. This could be insecure.
WARN  Documentation on securing your setup: https://github.com/codercom/code-server/blob/master/doc/security/ssl.md
INFO
INFO  Password: 05df54f62e7761cad92d5e8c
INFO
INFO  Started (click the link below to open):
INFO  http://localhost:8443/
INFO
WARN  stderr {"data":"(node:19) [DEP0005] DeprecationWarning: Buffer() is deprecated due to security and usability issues. Please use the Buffer.alloc(), Buffer.allocUnsafe(), or Buffer.from() methods instead.\n"}
INFO  Connected to shared process
```
#### 访问`code-server`
```
http://192.168.137.133:8443/
```

![vscode01](../img/dockerDeploy/vscode01.png)

![vscode02](../img/dockerDeploy/vscode02.png)

