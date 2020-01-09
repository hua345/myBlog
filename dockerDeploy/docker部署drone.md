#### 1. 参考
- [drone gogs安装](https://docs.drone.io/installation/gogs/single-machine/)
- [https://github.com/drone/drone](https://github.com/drone/drone)

#### 2. 拉取drone镜像
```
docker pull drone/drone:1
```
#### 3. 运行drone服务
```
docker run \
  --volume=/var/run/docker.sock:/var/run/docker.sock \
  --volume=/var/lib/drone:/data \
  --env=DRONE_GIT_ALWAYS_AUTH=false \
  --env=DRONE_GOGS_SERVER=${DRONE_GOGS_SERVER} \
  --env=DRONE_RUNNER_CAPACITY=2 \
  --env=DRONE_SERVER_HOST=${DRONE_SERVER_HOST} \
  --env=DRONE_SERVER_PROTO=${DRONE_SERVER_PROTO} \
  --env=DRONE_TLS_AUTOCERT=false \
  --publish=80:80 \
  --publish=443:443 \
  --restart=always \
  --detach=true \
  --name=drone \
  drone/drone:1
```
#### 4. drone配置
#### 4.1 DRONE_GOGS_SERVER
Gogs服务器地址
```
DRONE_GOGS_SERVER=https://gogs.domain.com
```
#### 4.2 DRONE_SERVER_PROTO
drone服务http协议类型，`http`或者`https`
```
DRONE_SERVER_PROTO=http
```
#### 4.3 DRONE_RUNNER_CAPACITY
drone并发pipeline执行数量
```
DRONE_RUNNER_CAPACITY=2
```
#### 4.4 DRONE_TLS_AUTOCERT
自动化https证书生成和配置
```
DRONE_TLS_AUTOCERT=false
```
