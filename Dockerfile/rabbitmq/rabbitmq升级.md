# rabbitmq升级

官网下载的安装包比较旧,需要到github下载最新的安装包

## 卸载rabbitmq和erlang

```bash
yum remove rabbitmq-server
yum remove erlang
```

## 安装新版本[Erlang](https://github.com/rabbitmq/erlang-rpm/releases)

RabbitMQ(3.8.4)需要Erlang/OTP(21.3~23.x)
