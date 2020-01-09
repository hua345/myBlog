#### 参考
- [Http/2 升级指南](https://www.cnblogs.com/syyong/p/9088672.html)
- [Nginx线程池性能提升9倍](https://segmentfault.com/a/1190000002924458)
#### 1.安装依赖包
```bash
yum install gcc gcc-c++ pcre pcre-devel
```
#### 1.1 安装openssl和zlib
参考[CentOS安装openssl.md](CentOS安装openssl.md)

#### 2. 编译nginx
#### 2.1 下载[nginx](http://nginx.org/)

[http2支持需要1.9.5+](https://github.com/http2/http2-spec/wiki/Implementations)

#### 2.2 编译安装nginx
[查看编译选项](#3-编译选项)
```bash
tar -zvxf nginx-1.16.0.tar.gz
cd nginx-1.16.0
./configure --prefix=/usr/local/nginx \
--with-openssl=/root/openssl-OpenSSL_1_1_1b \
--with-http_ssl_module \
--with-http_stub_status_module \
--with-threads \
--with-http_v2_module \
--with-stream --with-stream_ssl_module

make -j4 && make install
```
- `--with-openssl=<DIR>`openssl源码路径
- `--with-http_ssl_module`支持https协议
- `--with-http_stub_status_module`支持nginx监控
- `--with-threads`使用线程池
- `--with-http_v2_module`支持http/2协议
- `--with-stream --with-stream_ssl_module`支持https反向代理
#### 2.3查看nginx版本
```bash
vi /etc/profile
export PATH=/usr/local/nginx/sbin:$PATH 
source /etc/profile

[root@dockerMaster nginx-1.16.0]# nginx -V
nginx version: nginx/1.16.0
built by gcc 4.8.5 20150623 (Red Hat 4.8.5-36) (GCC)
built with OpenSSL 1.1.1b  26 Feb 2019
TLS SNI support enabled
configure arguments: --prefix=/usr/local/nginx --with-openssl=/root/openssl-OpenSSL_1_1_1b --with-http_ssl_module --with-http_stub_status_module --with-threads --with-http_v2_module --with-stream --with-stream_ssl_module
```
#### 2.4 查看nginx运行信息
```bash
# ps -ef |grep nginx
root     110609      1  0 20:00 ?        00:00:00 nginx: master process nginx
root     112857 110609  0 20:37 ?        00:00:00 nginx: worker process
root     112886  45767  0 20:38 pts/1    00:00:00 grep --color=auto nginx

# lsof -i:80
COMMAND    PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
nginx   110609 root    6u  IPv4  89016      0t0  TCP *:http (LISTEN)
nginx   112857 root    6u  IPv4  89016      0t0  TCP *:http (LISTEN)
```

#### 3. 编译选项
```
# ./configure --help

  --help                             print this message

  --prefix=PATH                      set installation prefix
  --sbin-path=PATH                   set nginx binary pathname
  --modules-path=PATH                set modules path
  --conf-path=PATH                   set nginx.conf pathname
  --error-log-path=PATH              set error log pathname
  --pid-path=PATH                    set nginx.pid pathname
  --lock-path=PATH                   set nginx.lock pathname

  --user=USER                        set non-privileged user for
                                     worker processes
  --group=GROUP                      set non-privileged group for
                                     worker processes

  --build=NAME                       set build name
  --builddir=DIR                     set build directory

  --with-select_module               enable select module
  --without-select_module            disable select module
  --with-poll_module                 enable poll module
  --without-poll_module              disable poll module

  --with-threads                     enable thread pool support

  --with-file-aio                    enable file AIO support

  --with-http_ssl_module             enable ngx_http_ssl_module
  --with-http_v2_module              enable ngx_http_v2_module
  --with-http_realip_module          enable ngx_http_realip_module
  --with-http_addition_module        enable ngx_http_addition_module
  --with-http_xslt_module            enable ngx_http_xslt_module
  --with-http_xslt_module=dynamic    enable dynamic ngx_http_xslt_module
  --with-http_image_filter_module    enable ngx_http_image_filter_module
  --with-http_image_filter_module=dynamic
                                     enable dynamic ngx_http_image_filter_module
  --with-http_geoip_module           enable ngx_http_geoip_module
  --with-http_geoip_module=dynamic   enable dynamic ngx_http_geoip_module
  --with-http_sub_module             enable ngx_http_sub_module
  --with-http_dav_module             enable ngx_http_dav_module
  --with-http_flv_module             enable ngx_http_flv_module
  --with-http_mp4_module             enable ngx_http_mp4_module
  --with-http_gunzip_module          enable ngx_http_gunzip_module
  --with-http_gzip_static_module     enable ngx_http_gzip_static_module
  --with-http_auth_request_module    enable ngx_http_auth_request_module
  --with-http_random_index_module    enable ngx_http_random_index_module
  --with-http_secure_link_module     enable ngx_http_secure_link_module
  --with-http_degradation_module     enable ngx_http_degradation_module
  --with-http_slice_module           enable ngx_http_slice_module
  --with-http_stub_status_module     enable ngx_http_stub_status_module

  --without-http_charset_module      disable ngx_http_charset_module
  --without-http_gzip_module         disable ngx_http_gzip_module
  --without-http_ssi_module          disable ngx_http_ssi_module
  --without-http_userid_module       disable ngx_http_userid_module
  --without-http_access_module       disable ngx_http_access_module
  --without-http_auth_basic_module   disable ngx_http_auth_basic_module
  --without-http_mirror_module       disable ngx_http_mirror_module
  --without-http_autoindex_module    disable ngx_http_autoindex_module
  --without-http_geo_module          disable ngx_http_geo_module
  --without-http_map_module          disable ngx_http_map_module
  --without-http_split_clients_module disable ngx_http_split_clients_module
  --without-http_referer_module      disable ngx_http_referer_module
  --without-http_rewrite_module      disable ngx_http_rewrite_module
  --without-http_proxy_module        disable ngx_http_proxy_module
  --without-http_fastcgi_module      disable ngx_http_fastcgi_module
  --without-http_uwsgi_module        disable ngx_http_uwsgi_module
  --without-http_scgi_module         disable ngx_http_scgi_module
  --without-http_grpc_module         disable ngx_http_grpc_module
  --without-http_memcached_module    disable ngx_http_memcached_module
  --without-http_limit_conn_module   disable ngx_http_limit_conn_module
  --without-http_limit_req_module    disable ngx_http_limit_req_module
  --without-http_empty_gif_module    disable ngx_http_empty_gif_module
  --without-http_browser_module      disable ngx_http_browser_module
  --without-http_upstream_hash_module
                                     disable ngx_http_upstream_hash_module
  --without-http_upstream_ip_hash_module
                                     disable ngx_http_upstream_ip_hash_module
  --without-http_upstream_least_conn_module
                                     disable ngx_http_upstream_least_conn_module
  --without-http_upstream_random_module
                                     disable ngx_http_upstream_random_module
  --without-http_upstream_keepalive_module
                                     disable ngx_http_upstream_keepalive_module
  --without-http_upstream_zone_module
                                     disable ngx_http_upstream_zone_module

  --with-http_perl_module            enable ngx_http_perl_module
  --with-http_perl_module=dynamic    enable dynamic ngx_http_perl_module
  --with-perl_modules_path=PATH      set Perl modules path
  --with-perl=PATH                   set perl binary pathname

  --http-log-path=PATH               set http access log pathname
  --http-client-body-temp-path=PATH  set path to store
                                     http client request body temporary files
  --http-proxy-temp-path=PATH        set path to store
                                     http proxy temporary files
  --http-fastcgi-temp-path=PATH      set path to store
                                     http fastcgi temporary files
  --http-uwsgi-temp-path=PATH        set path to store
                                     http uwsgi temporary files
  --http-scgi-temp-path=PATH         set path to store
                                     http scgi temporary files

  --without-http                     disable HTTP server
  --without-http-cache               disable HTTP cache

  --with-mail                        enable POP3/IMAP4/SMTP proxy module
  --with-mail=dynamic                enable dynamic POP3/IMAP4/SMTP proxy module
  --with-mail_ssl_module             enable ngx_mail_ssl_module
  --without-mail_pop3_module         disable ngx_mail_pop3_module
  --without-mail_imap_module         disable ngx_mail_imap_module
  --without-mail_smtp_module         disable ngx_mail_smtp_module

  --with-stream                      enable TCP/UDP proxy module
  --with-stream=dynamic              enable dynamic TCP/UDP proxy module
  --with-stream_ssl_module           enable ngx_stream_ssl_module
  --with-stream_realip_module        enable ngx_stream_realip_module
  --with-stream_geoip_module         enable ngx_stream_geoip_module
  --with-stream_geoip_module=dynamic enable dynamic ngx_stream_geoip_module
  --with-stream_ssl_preread_module   enable ngx_stream_ssl_preread_module
  --without-stream_limit_conn_module disable ngx_stream_limit_conn_module
  --without-stream_access_module     disable ngx_stream_access_module
  --without-stream_geo_module        disable ngx_stream_geo_module
  --without-stream_map_module        disable ngx_stream_map_module
  --without-stream_split_clients_module
                                     disable ngx_stream_split_clients_module
  --without-stream_return_module     disable ngx_stream_return_module
  --without-stream_upstream_hash_module
                                     disable ngx_stream_upstream_hash_module
  --without-stream_upstream_least_conn_module
                                     disable ngx_stream_upstream_least_conn_module
  --without-stream_upstream_random_module
                                     disable ngx_stream_upstream_random_module
  --without-stream_upstream_zone_module
                                     disable ngx_stream_upstream_zone_module

  --with-google_perftools_module     enable ngx_google_perftools_module
  --with-cpp_test_module             enable ngx_cpp_test_module

  --add-module=PATH                  enable external module
  --add-dynamic-module=PATH          enable dynamic external module

  --with-compat                      dynamic modules compatibility

  --with-cc=PATH                     set C compiler pathname
  --with-cpp=PATH                    set C preprocessor pathname
  --with-cc-opt=OPTIONS              set additional C compiler options
  --with-ld-opt=OPTIONS              set additional linker options
  --with-cpu-opt=CPU                 build for the specified CPU, valid values:
                                     pentium, pentiumpro, pentium3, pentium4,
                                     athlon, opteron, sparc32, sparc64, ppc64

  --without-pcre                     disable PCRE library usage
  --with-pcre                        force PCRE library usage
  --with-pcre=DIR                    set path to PCRE library sources
  --with-pcre-opt=OPTIONS            set additional build options for PCRE
  --with-pcre-jit                    build PCRE with JIT compilation support

  --with-zlib=DIR                    set path to zlib library sources
  --with-zlib-opt=OPTIONS            set additional build options for zlib
  --with-zlib-asm=CPU                use zlib assembler sources optimized
                                     for the specified CPU, valid values:
                                     pentium, pentiumpro

  --with-libatomic                   force libatomic_ops library usage
  --with-libatomic=DIR               set path to libatomic_ops library sources

  --with-openssl=DIR                 set path to OpenSSL library sources
  --with-openssl-opt=OPTIONS         set additional build options for OpenSSL

  --with-debug                       enable debug logging
  ```
