#### 参考
- [docker部署golang应用](../../dockerDeploy/docker部署golang应用.md)
#### 构建脚本
```bash
docker build -t hellodocker:v1 .
```
#### 启动命令
```
docker run -p 8080:8080 hellodocker:v1
```