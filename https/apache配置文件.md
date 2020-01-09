### apache配置文件结构
```
#	/etc/apache2/
#	|-- apache2.conf
#	|	`--  ports.conf
#	|-- mods-enabled
#	|	|-- *.load
#	|	`-- *.conf
#	|-- conf-enabled
#	|	`-- *.conf
# 	`-- sites-enabled
#	 	`-- *.conf

# * apache2.conf是主要配置文件，服务器启动时会Include所有配置文件。
# * ports.conf主要配置文件中端口设置。
＃　mods-enabled, conf-enabled, sites-enabled目录分别包含管理模块配置，全局参数配置和虚拟主机配置
```
### apache文件系统控制
```
<Directory />
	Options FollowSymLinks
	AllowOverride None
	Require all denied
</Directory>
<Directory /var/www/>
	Options Indexes FollowSymLinks
	AllowOverride None
	Require all granted
</Directory>
```
####Options
```
ExecCGI           #在该目录下允许执行CGI脚本。
FollowSymLinks    #在该目录下允许文件系统使用符号连接。
Indexes           #当用户访问该目录时，如果用户找不到DirectoryIndex指定的主页文件(例如index.html),则返回该目录下的文件列表给用户。
SymLinksIfOwnerMatch   #当使用符号连接时，只有当符号连接的文件拥有者与实际文件的拥有者相同时才可以访问。
```
####AllowOverride
是否寻找目录下额外的配置文件｀.htaccess｀
```
None　　　　＃当AllowOverride被设置为None时。不搜索该目录下的.htaccess文件（可以减小服务器开销）。
All　　　　＃在.htaccess文件中可以使用所有的指令。
```
#### Require
在Apache2.4版本中，使用mod_authz_host这个新的模块，来实现访问控制.
```
Require all granted　　　#允许所有连接
Require all denied 　　　#拒绝所有连接
Require env env-var [env-var] ... #允许，匹配环境变量中任意一个
Require method http-method [http-method] ... #允许，特定的HTTP方法
Require expr expression #允许，表达式为true
Require user userid [ userid ] ... #允许，特定用户
Require group group-name [group-name] ... #允许，特定用户组
Require ip 10 172.20 192.168.2  #允许特定IP地址
Require host example.org        #只允许example.org所有请求都被允许，其他拒绝
```
### apache　多处理模式MPM(Multi-Processing Modules)
```
＃查看编译设置
/usr/sbin/apachectl -V
Architecture:   64-bit
Server MPM:     event
  threaded:     yes (fixed thread count)
    forked:     yes (variable process count)

#编译的时候，可以通过configure的参数来指定：
--with-mpm=prefork|worker|event
#也可以编译为三种都支持，通过修改配置来更换
--enable-mpms-shared=all
#在mods-enabled目录下添加需要的模块配置，mpm_event.conf文件
# Conflicts: mpm_worker mpm_prefork
LoadModule mpm_event_module /usr/lib/apache2/modules/mod_mpm_event.so
```
- prefork_module, 这个多路处理模块(MPM)实现了一个非线程型的、预派生的web服务器，它的工作方式类似于Apache 1.3。
它适合于没有线程安全库，需要避免线程兼容性问题的系统。它是要求将每个请求相互独立的情况下最好的MPM，这样若一个请求出现问题就不会影响到其他请求。
这个MPM具有很强的自我调节能力，只需要很少的配置指令调整。最重要的是将MaxClients设置为一个足够大的数值以处理潜在的请求高峰，同时又不能太大，以致需要使用的内存超出物理内存的大小。
- worker, 此多路处理模块(MPM)使网络服务器支持混合的多线程多进程。由于使用线程来处理请求，所以可以处理海量请求，而系统资源的开销小于基于进程的MPM。但是，它也使用了多进程，每个进程又有多个线程，以获得基于进程的MPM的稳定性。
每个进程可以拥有的线程数量是固定的。服务器会根据负载情况增加或减少进程数量。一个单独的控制进程(父进程)负责子进程的建立。每个子进程可以建立ThreadsPerChild数量的服务线程和一个监听线程，该监听线程监听接入请求并将其传递给服务线程处理和应答。

- 不管是Worker模式或是Prefork 模式，Apache总是试图保持一些备用的(spare)或者是空闲的子进程（空闲的服务线程池）用于迎接即将到来的请求。这样客户端就不需要在得到服务前等候子进程的产生。

- event, 以上两种稳定的MPM方式在非常繁忙的服务器应用下都有些不足。尽管HTTP的Keepalive方式能减少TCP连接数量和网络负载，但是 Keepalive需要和服务进程或者线程绑定，这就导致一个繁忙的服务器会耗光所有的线程。 Event MPM是解决这个问题的一种新模型，它把服务进程从连接中分离出来。在服务器处理速度很快，同时具有非常高的点击率时，可用的线程数量就是关键的资源限 制，此时Event MPM方式是最有效的。
event MPM需要系统支持Epoll网络模型,Linux内核版本 >= 2.6
event HTTPS的连接（SSL），它的运行模式仍然是类似worker的方式，线程会被一直占用，直到连接关闭。

#### mods-available/mpm_prefork.conf
```
# prefork MPM
# StartServers: number of server processes to start
# MinSpareServers: minimum number of server processes which are kept spare
# MaxSpareServers: maximum number of server processes which are kept spare
# MaxRequestWorkers: maximum number of server processes allowed to start
# MaxConnectionsPerChild: maximum number of requests a server process serves

<IfModule mpm_prefork_module>
	StartServers			 5
	MinSpareServers		  5
	MaxSpareServers		 10
	MaxRequestWorkers	  150
	MaxConnectionsPerChild   0
</IfModule>
```
#### mods-available/mpm_worker.conf
```
# worker MPM
# StartServers: initial number of server processes to start
# MinSpareThreads: minimum number of worker threads which are kept spare
# MaxSpareThreads: maximum number of worker threads which are kept spare
# ThreadLimit: ThreadsPerChild can be changed to this maximum value during a
#			  graceful restart. ThreadLimit can only be changed by stopping
#			  and starting Apache.
# ThreadsPerChild: constant number of worker threads in each server process
# MaxRequestWorkers: maximum number of threads
# MaxConnectionsPerChild: maximum number of requests a server process serves

<IfModule mpm_worker_module>
	StartServers			 2
	MinSpareThreads		 25
	MaxSpareThreads		 75
	ThreadLimit			 64
	ThreadsPerChild		 25
	MaxRequestWorkers	  150
	MaxConnectionsPerChild   0
</IfModule>
```
#### mods-available/mpm_event.conf
```
# event MPM
# StartServers: initial number of server processes to start
# MinSpareThreads: minimum number of worker threads which are kept spare
# MaxSpareThreads: maximum number of worker threads which are kept spare
# ThreadsPerChild: constant number of worker threads in each server process
# MaxRequestWorkers: maximum number of worker threads
# MaxConnectionsPerChild: maximum number of requests a server process serves
<IfModule mpm_event_module>
	StartServers			 2
	MinSpareThreads		 25
	MaxSpareThreads		 75
	ThreadLimit			 64
	ThreadsPerChild		 25
	MaxRequestWorkers	  150
	MaxConnectionsPerChild   0
</IfModule>
```
### 参考：

- [Upgrading to 2.4 from 2.2](http://httpd.apache.org/docs/2.4/upgrading.html)
- [mod_authz_core#require ](http://httpd.apache.org/docs/2.4/mod/mod_authz_core.html#require)
- [Apache MPM event](https://httpd.apache.org/docs/2.4/mod/event.html)
- [Apache2.4 访问控制](http://blog.wangyan.org/apache24-access-control.html)
- [Apache Prefork、Worker和Event三种MPM分析](http://www.cnblogs.com/fnng/archive/2012/11/20/2779977.html)

