# base image
FROM my/centos

# MAINTAINER
MAINTAINER chenjianhua 2290910211@qq.com

# 如果 <源路径> 为一个 tar 压缩文件的话，压缩格式为 gzip, bzip2 以及 xz 的情况下
# 自动解压缩这个压缩文件到nginx-1.16.0
ADD nginx-1.16.0.tar.gz /usr/local/src

# running required command
RUN yum install -y gcc gcc-c++ glibc make autoconf
RUN yum install -y openssl openssl-devel pcre pcre-devel zlib zlib-devel

WORKDIR /usr/local/src/nginx-1.16.0

# execute command to compile nginx
RUN ./configure --prefix=/usr/local/nginx \
    --with-http_ssl_module \
    --with-http_stub_status_module \
    --with-threads \
    --with-http_v2_module \
    --with-stream --with-stream_ssl_module

RUN make -j4 && make install
ENV PATH /usr/local/nginx/sbin:$PATH

RUN nginx -V
# http
EXPOSE 80
# https
EXPOSE 443

# 关闭守护进程
CMD ["nginx", "-g", "daemon off;"]