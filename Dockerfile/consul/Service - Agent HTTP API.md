# 参考

- [Service - Agent HTTP API](https://www.consul.io/api/agent/service.html)

> The /agent/service endpoints interact with services on the local agent in Consul.

## List Services

> This endpoint returns all the services that are registered with the local agent.

| Method | Path            | Produces         |
| ------ | --------------- | ---------------- |
| GET    | /agent/services | application/json |

```bash
http http://127.0.0.1:8500/v1/agent/services
```

```json
{
    "gin-service01": {
        "Address": "192.168.137.128",
        "EnableTagOverride": false,
        "ID": "gin-service01",
        "Meta": {},
        "Port": 8080,
        "Service": "gin-service",
        "Tags": [
            "gin"
        ],
        "Weights": {
            "Passing": 1,
            "Warning": 1
        }
    }
}
```

```bash
➜  ~ http http://127.0.0.1:8500/v1/agent/service/gin-service01
HTTP/1.1 200 OK
Content-Encoding: gzip
Content-Length: 186
Content-Type: application/json
Date: Sun, 28 Jul 2019 01:36:01 GMT
Vary: Accept-Encoding
X-Consul-Contenthash: 544558c9c787894a

{
    "Address": "192.168.137.128",
    "ContentHash": "544558c9c787894a",
    "EnableTagOverride": false,
    "ID": "gin-service01",
    "Meta": null,
    "Port": 8080,
    "Service": "gin-service",
    "Tags": [
        "gin"
    ],
    "Weights": {
        "Passing": 1,
        "Warning": 1
    }
}
```

### Get local service health

> Retrieve an aggregated state of service(s) on the local agent by name.

| Method | Path                                                    | Produces         |
| ------ | ------------------------------------------------------- | ---------------- |
| GET    | /v1/agent/health/service/name/:service_name             | application/json |
| GET    | /v1/agent/health/service/name/:service_name?format=text | text/plain       |

```bash
http http://127.0.0.1:8500/v1/agent/health/service/name/gin-service
```

### Get local service health by its ID

> Retrive an aggregated state of service(s) on the local agent by ID.

| Method | Path                                                | Produces         |
| ------ | --------------------------------------------------- | ---------------- |
| GET    | /v1/agent/health/service/id/:service_id             | application/json |
| GET    | /v1/agent/health/service/id/:service_id?format=text | text/plain       |

```bash
➜  ~ http http://127.0.0.1:8500/v1/agent/health/service/id/gin-service01
```

### Register Service

> This endpoint adds a new service, with an optional health check, to the local agent.

| Method | Path                    | Produces         |
| ------ | ----------------------- | ---------------- |
| PUT    | /agent/service/register | application/json |

- Name (string: <required>) - Specifies the logical name of the service. Many service instances may share the same logical service name.
- ID (string: "") - Specifies a unique ID for this service. This must be unique per agent. This defaults to the Name parameter if not provided.
- Tags (array<string>: nil) - Specifies a list of tags to assign to the service. These tags can be used for later filtering and are exposed via the APIs.
- Address (string: "") - Specifies the address of the service. If not provided, the agent's address is used as the address for the service during DNS queries.
- Port (int: 0) - Specifies the port of the service.
- Check (Check: nil) - Specifies a check. Please see the check documentation for more information about the accepted fields. If you don't provide a name or id for the check then they will be generated. To provide a custom id and/or name set the CheckID and/or Name field.
- Weights (Weights: nil) - Specifies weights for the service. Please see the service documentation for more information about weights. If this field is not provided weights will default to {"Passing": 1, "Warning": 1}.

```json
{
  "ID": "myGin01",
  "Name": "myGin",
  "Address": "192.168.137.128",
  "Port": 8080,
  "EnableTagOverride": false,
  "Check": {
    "DeregisterCriticalServiceAfter": "90m",
    "HTTP": "http://192.168.137.128:8080/ping",
    "Interval": "5s"
  },
  "Weights": {
    "Passing": 10,
    "Warning": 1
  }
}
```

```bash
➜  ~ http put http://127.0.0.1:8500/v1/agent/service/register @register.json
HTTP/1.1 200 OK
Content-Length: 0
Date: Sun, 28 Jul 2019 02:19:20 GMT
Vary: Accept-Encoding
```

### Deregister Service

This endpoint removes a service from the local agent. If the service does not exist, no action is taken.

| Method | Path                                  | Produces         |
| ------ | ------------------------------------- | ---------------- |
| PUT    | /agent/service/deregister/:service_id | application/json |

```bash
➜  ~ http put http://127.0.0.1:8500/v1/agent/service/deregister/myGin01
HTTP/1.1 200 OK
Content-Length: 0
Date: Sun, 28 Jul 2019 02:22:02 GMT
Vary: Accept-Encoding
```
