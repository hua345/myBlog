# 参考

- [Status HTTP API](https://www.consul.io/api/status.html)

## Get Raft Leader

> This endpoint returns the Raft leader for the datacenter in which the agent is running.

|Method|Path|Produces|
|------|---------------|-----------|
|GET|/status/leader|application/json|

Sample Request

```bash
curl http://127.0.0.1:8500/v1/status/leader
```

Sample Response

```bash
"192.168.137.129:8300"
```

## List Raft Peers

> This endpoint retrieves the Raft peers for the datacenter in which the the agent is running. This list of peers is strongly consistent and can be useful in determining when a given server has successfully joined the cluster.

|Method|Path|Produces|
|------|----------|---------|
|GET|/status/peers|application/json|

Sample Request

```bash
curl http://127.0.0.1:8500/v1/status/peers
["192.168.137.129:8300","192.168.137.130:8300","192.168.137.128:8300"]
```
