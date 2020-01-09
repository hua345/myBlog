# docker常用images

```bash
# 基础系统版本
# alpine
# Debian 8 jessie
# Debian 9 Stretch
# Debian 10 Buster
# Ubuntu 18.04, bionic-20191029, bionic, latest
# Ubuntu19.04, disco-20191030, disco
# Ubuntu19.10, eoan-20191101, eoan, rolling
# Ubuntu20.04, focal-20191030, focal, devel
# Ubuntu14.04, trusty-20190515, trusty
# Ubuntu16.04, xenial-20191108, xenial

#golang:1.13.4-stretch
#golang:1.13.4-buster
stretch和buster是debian的发行版本，表示镜像基于什么版本构建的
```

```bash
# 3.10.3, 3.10, 3, latest
docker pull alpine:3.10.3
# latest, centos8, 8
docker pull centos:centos7
docker pull centos:centos8
# 18.04, bionic-20191029, bionic, latest
docker pull ubuntu:18.04
# 1.13.4, 1.13, 1, latest
docker pull golang:1.13.4
docker pull openjdk:8u232-jdk
docker pull openjdk:11.0.5-jdk
# 3.5.6, 3.5, latest
docker pull zookeeper:3.5.6
# 5.0.7, 5.0, 5, latest
docker pull redis:5.0.7
# 8.0.18, 8.0, 8, latest
docker pull mysql:8.0.18
# 12.1, 12, latest
docker pull postgres:12.1
# 1.17.6, mainline, 1, 1.17, latest
docker pull nginx:1.17.6
# 2.7.1, 2.7, 2, latest
docker pull registry:2.7.1
# 13.2.0-stretch, 13.2.0, latest
docker pull node:13.2.0
# https://github.com/gitlabhq/gitlabhq/releases
# https://about.gitlab.com/install/
# https://docs.gitlab.com/omnibus/docker/
docker pull gitlab/gitlab-ce:12.4.5-ce.0
# 3.8.1, 3.8, 3, latest
docker pull rabbitmq:3.8.1
docker pull elasticsearch:7.4.2
docker pull logstash:7.4.2
docker pull kibana:7.4.2
# 1.6.2, 1.6, latest
docker pull consul:1.6.2
```
