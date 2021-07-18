# base image
FROM my/centos

# MAINTAINER
MAINTAINER chenjianhua 2290910211@qq.com

ENV REDIS_VERSION 5.0.5
#ADD redis-$REDIS_VERSION.tar.gz /usr/local/src

RUN wget http://download.redis.io/releases/redis-$REDIS_VERSION.tar.gz && \
tar xfz redis-$REDIS_VERSION.tar.gz
WORKDIR /usr/local/src/redis-$REDIS_VERSION

RUN cd redis-$REDIS_VERSION && \
make -j4 && \
make install && \
cp -f src/redis-sentinel /usr/local/bin && \
mkdir -p /etc/redis && \
cp -f *.conf /etc/redis && \
sed 's/^\(bind .*\)$/# \1/' -i /etc/redis/redis.conf && \
sed 's/^\(daemonize .*\)$/# \1/' -i /etc/redis/redis.conf && \
sed 's/^\(dir .*\)$/# \1\ndir \/data/' -i /etc/redis/redis.conf && \
sed 's/^\(logfile .*\)$/# \1/' -i /etc/redis/redis.conf && \
sed 's/^protected-mode yes/protected-mode no/' -i /etc/redis/redis.conf && \
sed 's/^# unixsocket /unixsocket /' -i /etc/redis/redis.conf && \
sed 's/^# unixsocketperm 700/unixsocketperm 777/' -i /etc/redis/redis.conf

# Define mountable directories.
VOLUME ["/data"]
WORKDIR /data

EXPOSE 6379

CMD ["redis-server","/etc/redis/redis.conf"]