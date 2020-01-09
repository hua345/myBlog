# crontab 命令

## crontab 简介

- `crontab`常见于 Unix 和类 Unix 的操作系统之中，用于设置周期性被执行的指令。
- `crond`是`crontab`的守护进程

## 查看帮助

```yaml
Usage: crontab [options] file
  crontab [options]
  crontab -n [hostname]

Options: -u <user>  define user
  -e         edit user's crontab
  -l         list user's crontab
  -r         delete user's crontab
```

## 查看 crontab 状态

```bash
# 查看crond状态
systemctl status crond
```

## crontab 文件说明

用户所建立的 crontab 文件中，每一行都代表一项任务，格式如下

```bash
minute hour day month week command
```

- `minute`表示分钟，可以是从`0~59`之间的任何整数。
- `hour`表示小时，可以是从`0~23`之间的任何整数。
- `day`表示日期，可以是从`1~31`之间的任何整数。
- `month`表示月份，可以是从`1~12`之间的任何整数。
- `week`表示星期几，可以是从`0~7`之间的任何整数，这里的`0或7`代表星期日。
- `command`要执行的命令，可以是系统命令，也可以是自己编写的脚本文件。
- `*`：表示任意时间，实际上就是“每”的意思。可以代表`00~23`小时或者`00~12`每月或者`00~59`分
- `-`：表示区间，是一个范围，`00 17-19 * * * cmd`，就是每天 17,18,19 点的整点执行命令
- `,`：是分割时段，`30 3,19,21 * * * cmd`，就是每天凌晨 3 和晚上 19,21 点的半点时刻执行命令
- `/n`：表示分割，可以看成除法，`*/5 * * * * cmd`，每隔五分钟执行一次

![crontab.png](img/crontab.png)

## 常用示例

```bash
# 编辑定时任务
crontab -e

# 每1分钟执行一次command
* * * * * command

# 每小时更新系统时间
0 */1 * * * /usr/sbin/ntpdate cn.pool.ntp.org >/dev/null 2>&1
```

## 查看crond日志

```bash
tail -f /var/log/cron
```

## 重启 crond,使配置生效

```bash
systemctl restart crond
```

## crontab与环境变量

cron并不知道所需要的特殊环境变量。所以要保证在shelll脚本中提供所有必要的路径和环境变量

- 脚本中涉及文件路径时写全局路径
- 脚本执行要用到程序或其他环境变量时，通过`source`命令引入环境变量

```bash
#!/bin/bash
source /etc/profile
/usr/sbin/ntpdate cn.pool.ntp.org >/dev/null 2>&1
```

新创建的`cron job`，不会马上执行，至少要过2分钟才执行。如果`重启crond`则马上执行。

每条`JOB`执行完毕之后，系统会自动将输出发送邮件给当前系统用户。日积月累，非常的多，甚至会撑爆整个系统。所以每条`JOB`命令后面进行重定向处理是非常必要的: `>/dev/null 2>&1` 。前提是对`Job`中的命令需要正常输出已经作了一定的处理, 比如追加到某个特定日志文件。

- `/dev/null` 代表空设备文件
- `1`表示`stdout`标准输出，系统默认值是1，所以`>/dev/null`等同于`1>/dev/null`
- `2`表示`stderr`标准错误
- `&`表示等同于的意思，`2>&1`，表示标准错误输出重定向等同于标准输出
