#### 拉取镜像
```
docker pull jenkins
```
#### 运行镜像
```
docker run -d -p 8002:8080 -v ~/jenkins:/var/jenkins_home --name jenkins --restart=always jenkins
```
#### 查看容器日志
```
docker logs -f jenkins
```
#### 查看容器运行
```
docker ps
```
