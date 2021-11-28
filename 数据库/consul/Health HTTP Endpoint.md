# 参考

- [Health HTTP Endpoint](https://www.consul.io/api/health.html)

> The /health endpoints query health-related information. 

## List Checks for Service

This endpoint returns the checks specific to the node provided on the path.

| Method | Path               | Produces         |
| ------ | ------------------ | ---------------- |
| GET    | /health/checks/:service | application/json |

```json
➜  ~ http http://127.0.0.1:8500/v1/health/checks/gin-service
HTTP/1.1 200 OK
Content-Encoding: gzip
Content-Length: 297
Content-Type: application/json
Date: Sun, 28 Jul 2019 03:15:22 GMT
Vary: Accept-Encoding
X-Consul-Effective-Consistency: leader
X-Consul-Index: 16491
X-Consul-Knownleader: true
X-Consul-Lastcontact: 0

[
    {
        "CheckID": "gin-service01",
        "CreateIndex": 15454,
        "Definition": {},
        "ModifyIndex": 15910,
        "Name": "gin-check",
        "Node": "consul01",
        "Notes": "",
        "Output": "HTTP GET http://192.168.137.128:8080/ping: 200 OK Output: {\"message\":\"pong\"}\n",
        "ServiceID": "gin-service01",
        "ServiceName": "gin-service",
        "ServiceTags": [
            "gin"
        ],
        "Status": "passing"
    }
]
```
