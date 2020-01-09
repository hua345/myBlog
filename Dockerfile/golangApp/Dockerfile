FROM golang:latest

MAINTAINER chenjianhua 2290910211@qq.com

WORKDIR $GOPATH/src/hellodocker
ADD . $GOPATH/src/hellodocker
RUN go build .

EXPOSE 8080

ENTRYPOINT ["./hellodocker"]