#### 官方文档[https://github.com/netdata/netdata](https://github.com/netdata/netdata)
```
docker pull netdata/netdata
```
```
docker run -d --name=netdata \
  -p 19999:19999 \
  --restart=always \
  -v /proc:/host/proc:ro \
  -v /sys:/host/sys:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  --cap-add SYS_PTRACE \
  --security-opt apparmor=unconfined \
  netdata/netdata
```
