# 参考

- [KV Store Endpoints](https://www.consul.io/api/kv.html)

## KV Store Endpoints

> The /kv endpoints access Consul's simple key/value store, useful for storing service configuration or other metadata.
> Values in the KV store cannot be larger than 512kb.
> For multi-key updates, please consider using [transaction](https://www.consul.io/api/txn.html).

### Read Key

> This endpoint returns the specified key. If no key exists at the given path, a 404 is returned instead of a 200 response.

| Method | Path                                  | Produces         |
| ------ | ------------------------------------- | ---------------- |
| PUT    | /kv/:key | application/json |

#### Parameters

- key (string: "") - Specifies the path of the key to read.

```bash
➜  ~ http http://127.0.0.1:8500/v1/kv/name
HTTP/1.1 200 OK
Content-Encoding: gzip
Content-Length: 114
Content-Type: application/json
Date: Sun, 28 Jul 2019 03:22:55 GMT
Vary: Accept-Encoding
X-Consul-Index: 1530
X-Consul-Knownleader: true
X-Consul-Lastcontact: 0

[
    {
        "CreateIndex": 1509,
        "Flags": 0,
        "Key": "name",
        "LockIndex": 0,
        "ModifyIndex": 1530,
        "Value": "ImZhbmdmYW5nYSI="
    }
]
```

### Create/Update Key

> This endpoint

| Method | Path                                  | Produces         |
| ------ | ------------------------------------- | ---------------- |
| PUT    | /kv/:key | application/json |

#### Create/Update Parameters

- key (string: "") - Specifies the path of the key to read.
- cas (int: 0) - Specifies to use a Check-And-Set operation. This is very useful as a building block for more complex synchronization primitives. If the index is 0, Consul will only put the key if it does not already exist. If the index is non-zero, the key is only set if the index matches the ModifyIndex of that key.
- release (string: "") - Supply a session ID to use in a release operation.

```bash
➜  ~ http put http://127.0.0.1:8500/v1/kv/my-name\?cas\=0 @content
HTTP/1.1 200 OK
Content-Encoding: gzip
Content-Length: 28
Content-Type: application/json
Date: Sun, 28 Jul 2019 03:37:26 GMT
Vary: Accept-Encoding

true

➜  ~ http put http://127.0.0.1:8500/v1/kv/my-name\?cas\=0 @content
HTTP/1.1 200 OK
Content-Encoding: gzip
Content-Length: 29
Content-Type: application/json
Date: Sun, 28 Jul 2019 03:33:30 GMT
Vary: Accept-Encoding

false
```

### Delete Key

> This endpoint deletes a single key or all keys sharing a prefix.

| Method | Path                                  | Produces         |
| ------ | ------------------------------------- | ---------------- |
| PUT    | /kv/:key | application/json |

```bash
➜  ~ http delete http://127.0.0.1:8500/v1/kv/my-name
HTTP/1.1 200 OK
Content-Encoding: gzip
Content-Length: 28
Content-Type: application/json
Date: Sun, 28 Jul 2019 03:36:47 GMT
Vary: Accept-Encoding

true
```
