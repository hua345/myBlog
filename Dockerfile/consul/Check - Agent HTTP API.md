# 参考

- [HTTP API Structure](https://www.consul.io/api/agent/check.html)

> The /agent/check endpoints interact with checks on the local agent in Consul.

## List Checks

> This endpoint returns all checks that are registered with the local agent.

| Method | Path          | Produces         |
| ------ | ------------- | ---------------- |
| GET    | /agent/checks | application/json |

```bash
http http://127.0.0.1:8500/v1/agent/checks
```

```json
{
    "service:gin-service01": {
        "Node": "consul01",
        "CheckID": "service:gin-service01",
        "Name": "Service 'gin-service' check",
        "Status": "passing",
        "Notes": "",
        "Output": "HTTP GET http://192.168.137.128:8080/ping: 200 OK Output: {\"message\":\"pong\"}\n",
        "ServiceID": "gin-service01",
        "ServiceName": "gin-service",
        "ServiceTags": ["gin"],
        "Definition": {},
        "CreateIndex": 0,
        "ModifyIndex": 0
    }
}
```

## Register Check

> This endpoint adds a new check to the local agent. Checks may be of script, HTTP, TCP, or TTL type. The agent is responsible for managing the status of the check and keeping the Catalog in sync.

| Method | Path                  | Produces         |
| ------ | --------------------- | ---------------- |
| PUT    | /agent/check/register | application/json |

### Parameters

- Name (string: <required>) - Specifies the name of the check.

- ID (string: "") - Specifies a unique ID for this check on the node. This defaults to the "Name" parameter, but it may be necessary to provide an ID for uniqueness.

- Interval (string: "") - Specifies the frequency at which to run this check. This is required for HTTP and TCP checks.

- Timeout (duration: 10s) - Specifies a timeout for outgoing connections in the case of a Script, HTTP, TCP, or gRPC check. Can be specified in the form of "10s" or "5m" (i.e., 10 seconds or 5 minutes, respectively).

- TTL (string: "") - Specifies this is a TTL check, and the TTL endpoint must be used periodically to update the state of the check.

- HTTP (string: "") - Specifies an HTTP check to perform a GET request against the value of HTTP (expected to be a URL) every Interval.

- Method (string: "") - Specifies a different HTTP method to be used for an HTTP check. When no value is specified, GET is used.

- ServiceID (string: "") - Specifies the ID of a service to associate the registered check with an existing service provided by the agent.

- Status (string: "") - Specifies the initial status of the health check.

```json
{
  "ID": "gin-service01",
  "Name": "gin-check",
  "ServiceID": "gin-service01",
  "Interval": "5s",
  "DeregisterCriticalServiceAfter": "90m",
  "HTTP": "http://192.168.137.128:8080/ping",
  "Method": "GET"
}
```

```bash
➜  ~ http put http://127.0.0.1:8500/v1/agent/check/register @payload.json
HTTP/1.1 200 OK
Content-Length: 0
Date: Sun, 28 Jul 2019 00:13:56 GMT
Vary: Accept-Encoding
```

### Deregister Check

> This endpoint remove a check from the local agent. The agent will take care of deregistering the check from the catalog. If the check with the provided ID does not exist, no action is taken.

| Method | Path                  | Produces         |
| ------ | --------------------- | ---------------- |
|PUT|/agent/check/deregister/:check_id|application/json|

```bash
➜  ~ http put http://127.0.0.1:8500/v1/agent/check/deregister/service:gin-check
HTTP/1.1 200 OK
Content-Length: 0
Date: Sun, 28 Jul 2019 01:29:12 GMT
Vary: Accept-Encoding
```

### TTL Check Pass

> This endpoint is used with a TTL type check to set the status of the check to passing and to reset the TTL clock.

| Method | Path                  | Produces         |
| ------ | --------------------- | ---------------- |
|PUT|/agent/check/pass/:check_id|application/json|

```bash
http put http://127.0.0.1:8500/v1/agent/check/pass/gin-check
```
