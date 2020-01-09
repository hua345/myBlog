# Pull base image.
FROM my/centos
# MAINTAINER
MAINTAINER chenjianhua 2290910211@qq.com

# Set environment variables.
ENV GOROOT /usr/local/go
ENV GOPATH /gocode
ENV GOLANG_VERSION 1.13.4

ADD go$GOLANG_VERSION.linux-amd64.tar.gz /usr/local

ENV PATH $GOROOT/bin:$GOPATH/bin:$PATH

# Define working directory.
WORKDIR $GOPATH

# Define default command.
CMD ["bash"]