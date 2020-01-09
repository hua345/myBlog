# 1. `nohup`

> nohup 命令运行由 Command 参数和任何相关的 Arg 参数指定的命令，忽略所有挂断（SIGHUP）信号。
> 在注销后使用`nohup`命令运行后台中的程序。要运行后台中的`nohup`命令，添加 & （ 表示“and”的符号）到命令的尾部。
>
> nohup 是`no hang up`的缩写，就是不挂断的意思。
>
> 在缺省情况下该作业的所有输出都被重定向到一个名为`nohup.out`的文件中。

## 2. nohup 和&的区别

- `&`是指在后台运行，但当用户推出(挂起)的时候，命令自动也跟着退出
- `nohup`是指忽略所有挂断（SIGHUP）信号，注意并没有后台运行的功能

## 3. 案例

```java
nohup syncthing > syncthing.log 2>&1 &
```

- 0 – stdin (standard input)
- 1 – stdout (standard output)
- 2 – stderr (standard error)
- 2>&1 是将标准错误（2）重定向到标准输出（&1），
- 标准输出（&1）再被重定向输入到`syncthing.log`文件中。

## 查看运行的后台进程

```bash
jobs -l
```

## 4. docker

> 如果服务器安装了`docker`,`Dockerfile`制作镜像，用容器启动更为方便

```java
➜  ~ docker run -d -p 5000:5000 --name=registry --restart=always --privileged=true -v ~/data/registry:/var/lib/registry registry
f6ab8faaac24c332358abccc9230cc140e83dc63ae6c9739c6020e79c7ec0b3a

➜  ~ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                      NAMES
9a94515348fa        registry            "/entrypoint.sh /etc…"   3 days ago          Up 2 hours          0.0.0.0:5000->5000/tcp     registry
```
