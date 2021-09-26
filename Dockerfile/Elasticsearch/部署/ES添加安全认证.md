[TOC]

# ES添加安全认证

## 参考

- [Set up minimal security for Elasticsearch ](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-minimal-setup.html)

## [开启ES安全功能](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-minimal-setup.html#_enable_elasticsearch_security_features)

> When you use the basic license, the Elasticsearch security features are disabled by default. Enabling the Elasticsearch security features enables basic authentication so that you can run a local cluster with username and password authentication.
>
> 1. On **every** node in your cluster, stop both Kibana and Elasticsearch if they are running.
> 2. On **every** node in your cluster, add the `xpack.security.enabled` setting to the `$ES_PATH_CONF/elasticsearch.yml` file and set the value to `true`:

```bash
# 编辑es配置
vi elasticsearch.yml
xpack.security.enabled: true
```

## [创建安全密码](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-minimal-setup.html#security-create-builtin-users)

```log
 # 自动生成随机密码
 ./bin/elasticsearch-setup-passwords auto

 # 使用自己设置的密码
 ./bin/elasticsearch-setup-passwords.bat interactive
 
Initiating the setup of passwords for reserved users elastic,apm_system,kibana,kibana_system,logstash_system,beats_system,remote_monitoring_user.
You will be prompted to enter passwords as the process progresses.
Please confirm that you would like to continue [y/N]
Enter password for [elastic]:
Reenter password for [elastic]:
Enter password for [apm_system]:
Reenter password for [apm_system]:
Enter password for [kibana_system]:
Reenter password for [kibana_system]:
Enter password for [logstash_system]:
Reenter password for [logstash_system]:
Enter password for [beats_system]:
Reenter password for [beats_system]:
Enter password for [remote_monitoring_user]:
Reenter password for [remote_monitoring_user]:
Changed password for user [apm_system]
Changed password for user [kibana_system]
Changed password for user [kibana]
Changed password for user [logstash_system]
Changed password for user [beats_system]
Changed password for user [remote_monitoring_user]
Changed password for user [elastic]
```

## 配置kibana密码

> Add the `elasticsearch.username` setting to the `KIB_PATH_CONF/kibana.yml` file and set the value to the `kibana_system` user:

```
# If your Elasticsearch is protected with basic authentication, these settings provide
# the username and password that the Kibana server uses to perform maintenance on the Kibana
# index at startup. Your Kibana users still need to authenticate with Elasticsearch, which
# is proxied through the Kibana server.
elasticsearch.username: "kibana_system"
elasticsearch.password: "pass"
```

