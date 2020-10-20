# [minio](https://github.com/minio/minio)

- [https://github.com/minio/minio](https://github.com/minio/minio)
- [https://docs.min.io/cn/](https://docs.min.io/cn/)

`MinIO` 是一个基于Apache License v2.0开源协议的对象存储服务。它兼容亚马逊S3云存储服务接口，非常适合于存储大容量非结构化的数据，例如图片、视频、日志文件、备份数据和容器/虚拟机镜像等，而一个对象文件可以是任意大小，从几kb到最大5T不等。

`MinIO`是一个非常轻量的服务,可以很简单的和其他应用的结合，类似 NodeJS, Redis 或者 MySQL。

## 启动服务

```bash
docker run -p 9000:9000 \
  -e "MINIO_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE" \
  -e "MINIO_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" \
  minio/minio server /data
```

## 开放端口

```bash
firewall-cmd --zone=public --add-port=9000/tcp --permanent
firewall-cmd --reload
# 打开页面
# http://192.168.137.129:9000/minio/
```

![minio](./img/minio.png)
