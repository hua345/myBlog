# mac安装rabbitmq

- [https://www.rabbitmq.com/admin-guide.html](https://www.rabbitmq.com/admin-guide.html)

## 安装rabbitmq

```bash
brew update
brew install rabbitmq

==> Summary
🍺  /usr/local/Cellar/erlang/23.2: 7,978 files, 460.7MB
==> Installing rabbitmq
==> /usr/bin/unzip -qq -j /usr/local/Cellar/rabbitmq/3.8.9_1/plugins/rabbitmq_ma
Error: The `brew link` step did not complete successfully
The formula built, but is not symlinked into /usr/local
Could not symlink sbin/rabbitmq-defaults
/usr/local/sbin is not writable.

You can try again using:
  brew link rabbitmq
==> erlang
Man pages can be found in:
  /usr/local/opt/erlang/lib/erlang/man

Access them with `erl -man`, or add this directory to MANPATH.
==> rabbitmq
Management Plugin enabled by default at http://localhost:15672

To have launchd start rabbitmq now and restart at login:
  brew services start rabbitmq
Or, if you don't want/need a background service you can just run:
  rabbitmq-server
```

## 配置环境信息

安装完成后需要将`/usr/local/sbin`添加到`$PATH`，可以将下面这两行加到`~/.bash_profile`

```bash
# 使用zsh命令行时配置
~/.zshrc
vi ~/.zshrc
export SBIN_PATH=/usr/local/sbin
export PATH=$PATH:$SBIN_PATH
source ~/.zshrc

export PATH=$PATH:/usr/local/sbin
source ~/.bash_profile
```

## 启动RabbitMQ服务

```bash
➜  Desktop rabbitmq-server
Configuring logger redirection

  ##  ##      RabbitMQ 3.8.9
  ##  ##
  ##########  Copyright (c) 2007-2020 VMware, Inc. or its affiliates.
  ######  ##
  ##########  Licensed under the MPL 2.0. Website: https://rabbitmq.com

  Doc guides: https://rabbitmq.com/documentation.html
  Support:    https://rabbitmq.com/contact.html
  Tutorials:  https://rabbitmq.com/getstarted.html
  Monitoring: https://rabbitmq.com/monitoring.html

  Logs: /usr/local/var/log/rabbitmq/rabbit@localhost.log
        /usr/local/var/log/rabbitmq/rabbit@localhost_upgrade.log

  Config file(s): (none)

  Starting broker... completed with 6 plugins.
```

## 访问管理界面

[http://127.0.0.1:15672/](http://127.0.0.1:15672/)

默认用户名密码都是`guest`

其他操作参考[CentOS安装rabbitmq](./CentOS安装rabbitmq.md)
