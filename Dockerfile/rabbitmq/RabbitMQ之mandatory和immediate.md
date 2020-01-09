# 参考

- [RabbitMQ之mandatory和immediate](https://www.cnblogs.com/wangzhongqiu/archive/2017/11/14/7832796.html)

> `mandatory`和`immediate`是AMQP协议中basic.publish方法中的两个标识位，它们都有当消息传递过程中不可达目的地时将消息返回给生产者的功能。

## mandatory

当`mandatory`标志位设置为true时，`如果exchange根据自身类型和消息routeKey无法找到一个符合条件的queue`，
那么会调用basic.return方法将消息返回给生产者(Basic.Return + Content-Header + Content-Body),
当`mandatory`设置为false时，出现上述情形broker会直接将消息扔掉。

## immediate

当`immediate`标志位设置为true时，如果exchange在将消息路由到queue(s)时发现对于的queue上么有消费者，
那么这条消息不会放入队列中。当与消息routeKey关联的所有queue（一个或者多个）都没有消费者时，
该消息会通过basic.return方法返还给生产者。

## 概括来说

`mandatory`标志告诉服务器至少将该消息route到一个队列中，否则将消息返还给生产者；
`immediate`标志告诉服务器如果该消息关联的queue上有消费者，则马上将消息投递给它，
如果所有queue都没有消费者，直接把消息返还给生产者，不用将消息入队列等待消费者了。
