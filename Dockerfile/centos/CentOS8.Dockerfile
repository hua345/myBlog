# base image
FROM centos

# MAINTAINER
MAINTAINER chenjianhua 2290910211@qq.com
# update dnf
RUN cd /etc/yum.repos.d && \
sed -i 's/mirrorlist=/#mirrorlist=/g' CentOS-Base.repo CentOS-AppStream.repo CentOS-Extras.repo && \
sed -i 's/#baseurl=/baseurl=/g' CentOS-Base.repo CentOS-AppStream.repo CentOS-Extras.repo && \
sed -i 's/http:\/\/mirror.centos.org/https:\/\/mirrors.aliyun.com/g' CentOS-Base.repo CentOS-AppStream.repo CentOS-Extras.repo

RUN dnf clean all && dnf makecache && dnf -y update
# update epel
RUN dnf repolist
RUN dnf install -y wget gcc gcc-c++ glibc make autoconf git ntpdate
# 更新系统时间
RUN ntpdate cn.pool.ntp.org
# Commands when creating a new container
CMD ["cat","/etc/redhat-release"]