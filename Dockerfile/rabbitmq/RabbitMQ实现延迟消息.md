# RabbitMQ实现延迟消息

## 参考

- [RabbitMQ实现延迟消息居然如此简单，整个插件就完事了！](https://segmentfault.com/a/1190000023228816)

## 1.插件安装

去RabbitMQ的官网下载插件，插件地址:[community-plugins](https://www.rabbitmq.com/community-plugins.html)
[rabbitmq-delayed-message-exchange](https://github.com/rabbitmq/rabbitmq-delayed-message-exchange)

```bash
cp rabbitmq_delayed_message_exchange-3.8.0.ez /usr/lib/rabbitmq/lib/rabbitmq_server-3.6.15/plugins/rabbitmq_delayed_message_exchange-3.8.0.ez

rabbitmq-plugins enable rabbitmq_delayed_message_exchange-3.8.0.ez
```
