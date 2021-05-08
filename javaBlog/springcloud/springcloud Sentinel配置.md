# spring cloud Sentinel 配置

- [https://sentinelguard.io/zh-cn/](https://sentinelguard.io/zh-cn/)
- [https://github.com/alibaba/Sentinel](https://github.com/alibaba/Sentinel)

## `Sentinel`: 分布式系统的流量防卫兵

随着微服务的流行，服务和服务之间的稳定性变得越来越重要。`Sentinel`以流量为切入点，从流量控制、熔断降级、系统负载保护等多个维度保护服务的稳定性。

## `Sentinel` 具有以下特征:

- 丰富的应用场景：`Sentinel` 承接了阿里巴巴近 10 年的双十一大促流量的核心场景，例如秒杀（即突发流量控制在系统容量可以承受的范围）、消息削峰填谷、集群流量控制、实时熔断下游不可用应用等。
- 完备的实时监控：`Sentinel` 同时提供实时的监控功能。您可以在控制台中看到接入应用的单台机器秒级数据，甚至 500 台以下规模的集群的汇总运行情况。
- 广泛的开源生态：`Sentinel` 提供开箱即用的与其它开源框架/库的整合模块，例如与 Spring Cloud、Dubbo、gRPC 的整合。您只需要引入相应的依赖并进行简单的配置即可快速地接入 Sentinel。
- 完善的`SPI`扩展点：`Sentinel` 提供简单易用、完善的`SPI`扩展接口。您可以通过实现扩展接口来快速地定制逻辑。例如定制规则管理、适配动态数据源等。

![sentinel](./img/sentinel.png)

## `Sentinel` 的使用可以分为两个部分:

- `核心库`（Java 客户端）：不依赖任何框架/库，能够运行于 Java 7 及以上的版本的运行时环境，同时对 Dubbo / Spring Cloud 等框架也有较好的支持（见 主流框架适配）。
- `控制台`（Dashboard）：Dashboard 主要负责管理推送规则、监控、管理机器信息等。

## maven 依赖

```xml
<dependency>
    <groupId>com.alibaba.csp</groupId>
    <artifactId>sentinel-core</artifactId>
    <version>1.8.0</version>
</dependency>
```

## Sentinel 支持以下几种规则：流量控制规则、熔断降级规则、系统保护规则、来源访问控制规则 和 热点参数规则。

### [流量控制规则 (FlowRule)](https://sentinelguard.io/zh-cn/docs/flow-control.html)

流量规则的定义
重要属性：

| Field           | 说明                                                               | 默认值                      |
| --------------- | ------------------------------------------------------------------ | --------------------------- |
| resource        | 资源名，资源名是限流规则的作用对象                                 |
| count           | 限流阈值                                                           |
| grade           | 限流阈值类型，QPS 或线程数模式                                     | QPS 模式                    |
| limitApp        | 流控针对的调用来源                                                 | default，代表不区分调用来源 |
| strategy        | 调用关系限流策略：直接、链路、关联                                 | 根据资源本身（直接）        |
| controlBehavior | 流控效果（直接拒绝 / 排队等待 / 慢启动模式），不支持按调用关系限流 | 直接拒绝                    |

### 通过代码定义流量控制规则

理解上面规则的定义之后，我们可以通过调用 `FlowRuleManager.loadRules()` 方法来用硬编码的方式定义流量控制规则，比如：

```java
private static void initFlowQpsRule() {
    List<FlowRule> rules = new ArrayList<>();
    FlowRule rule1 = new FlowRule();
    rule1.setResource(resource);
    // Set max qps to 20
    rule1.setCount(20);
    rule1.setGrade(RuleConstant.FLOW_GRADE_QPS);
    rule1.setLimitApp("default");
    rules.add(rule1);
    FlowRuleManager.loadRules(rules);
}
```

## Sentinel 控制台

`Sentinel` 控制台包含如下功能:

- 查看机器列表以及健康情况：收集 Sentinel 客户端发送的心跳包，用于判断机器是否在线。
- 监控 (单机和集群聚合)：通过 Sentinel 客户端暴露的监控 API，定期拉取并且聚合应用监控信息，最终可以实现秒级的实时监控。
- 规则管理和推送：统一管理推送规则。
- 鉴权：生产环境中鉴权非常重要。这里每个开发者需要根据自己的实际情况进行定制。

从 [release 页面](https://github.com/alibaba/Sentinel/releases)下载最新版本的控制台 jar 包

### 启动 Sentinel 控制台

```bash
java -Dserver.port=8080 -Dcsp.sentinel.dashboard.server=localhost:8080 -Dproject.name=sentinel-dashboard -jar sentinel-dashboard.jar
```

默认用户名和密码都是`sentinel`

### 客户端接入控制台

控制台启动后，客户端需要按照以下步骤接入到控制台。

客户端需要引入`Transport`模块来与`Sentinel`控制台进行通信。您可以通过`pom.xml` 引入 JAR 包:

```xml
<dependency>
    <groupId>com.alibaba.csp</groupId>
    <artifactId>sentinel-transport-simple-http</artifactId>
    <version>x.y.z</version>
</dependency>
```

### [修改配置文件](https://sentinelguard.io/zh-cn/docs/startup-configuration.html)

其中，`project.name` 参数只能通过 JVM -D 参数方式配置，其它参数支持所有的配置方式。

其中 project.name 项用于指定应用名（appName）。若未指定，则默认解析 main 函数的类名作为应用名。实际项目使用中建议手动指定应用名。

`sentinel-transport-common` 的配置项

| 名称                               | 含义                                                                              | 类型   | 默认值 | 是否必需                                                        |
| ---------------------------------- | --------------------------------------------------------------------------------- | ------ | ------ | --------------------------------------------------------------- |
| `csp.sentinel.dashboard.server`     | 控制台的地址，指定控制台后客户端会自动向该地址发送心跳包。地址格式为：hostIp:port | String | null   | 是                                                              |
|`csp.sentinel.heartbeat.interval.ms`| 心跳包发送周期，单位毫秒                                                          | long   | null   | 非必需，若不进行配置，则会从相应的 HeartbeatSender 中提取默认值 |
| csp.sentinel.api.port              | 本地启动 HTTP API Server 的端口号                                                 | int    | 8719   | 否                                                              |
| csp.sentinel.heartbeat.client.ip   | 指定心跳包中本机的 IP                                                             | String | -      | 若不指定则通过 HostNameUtil 解析；该配置项多用于多网卡环境      |

`csp.sentinel.api.port` 可不提供，默认为 `8719`，若端口冲突会自动向下探测可用的端口。

