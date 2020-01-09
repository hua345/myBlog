# 参考

- [https://hub.docker.com/_/nginx](https://hub.docker.com/_/nginx)

```bash
docker build -t my/nginx:v1.16 .
docker run --name some-nginx -d -p 8001:80 --restart=always my/nginx:v1.16

#官方镜像
docker run --name some-nginx -d -p 8001:80 --restart=always nginx:1.17.6
```
