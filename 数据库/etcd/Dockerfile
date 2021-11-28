# https://github.com/etcd-io/etcd/blob/master/Dockerfile-release
# base image
FROM golang

# MAINTAINER
MAINTAINER chenjianhua 2290910211@qq.com

# Go installed (version 1.11+ is required)
RUN go version
RUN echo $GOPATH

# https://github.com/etcd-io/etcd
ADD etcd-3.3.13.tar.gz $GOPATH/src

WORKDIR $GOPATH/src/etcd-3.3.13

RUN ./build
RUN mv ./bin/etcd /usr/local/bin/etcd
RUN mv ./bin/etcdctl /usr/local/bin/etcdctl

RUN /usr/local/bin/etcd --version
EXPOSE 2379 2380
CMD ["/usr/local/bin/etcd"]