# 参考

- [https://nsq.io/components/nsqlookupd.html](https://nsq.io/components/nsqlookupd.html)

> nsqlookupd is the daemon that manages topology information. Clients query nsqlookupd to discover nsqd producers for a specific topic and nsqd nodes broadcasts topic and channel information.
>
> There are two interfaces: A TCP interface which is used by nsqd for broadcasts and an HTTP interface for clients to perform discovery and administrative actions.

- `-broadcast-address` string
    address of this lookupd node, (default to the OS hostname) (default "PROSNAKES.local")
- `-config` string
    path to config file
- `-http-address` string
    `<addr>:<port>` to listen on for HTTP clients (default "0.0.0.0:4161")
-inactive-producer-timeout duration
    duration of time a producer will remain in the active list since its last ping (default 5m0s)
- `-tcp-address` string
    `<addr>:<port>` to listen on for TCP clients (default "0.0.0.0:4160")

## HTTP Interface

### GET /lookup

Returns a list of producers for a topic

Params:

topic - the topic to list producers for

```bash
➜  ~ http http://127.0.0.1:4161/lookup topic==fang
HTTP/1.1 200 OK
Content-Length: 187
Content-Type: application/json; charset=utf-8
Date: Sun, 11 Aug 2019 03:12:54 GMT
X-Nsq-Content-Type: nsq; version=1.0

{
    "channels": [
        "fangChan"
    ],
    "producers": [
        {
            "broadcast_address": "192.168.137.128",
            "hostname": "consul01",
            "http_port": 4151,
            "remote_address": "127.0.0.1:37294",
            "tcp_port": 4150,
            "version": "1.1.0"
        }
    ]
}
```

### GET /topics

Returns a list of all known topics

```bash
➜  ~ http http://127.0.0.1:4161/topics
HTTP/1.1 200 OK
Content-Length: 26
Content-Type: application/json; charset=utf-8
Date: Sun, 11 Aug 2019 03:09:16 GMT
X-Nsq-Content-Type: nsq; version=1.0

{
    "topics": [
        "test",
        "fang"
    ]
}
```

### GET /channels

Returns a list of all known channels of a topic

Params:

topic - the topic to list channels for

```bash
➜  ~ http http://127.0.0.1:4161/channels topic==fang
HTTP/1.1 200 OK
Content-Length: 25
Content-Type: application/json; charset=utf-8
Date: Sun, 11 Aug 2019 03:11:43 GMT
X-Nsq-Content-Type: nsq; version=1.0

{
    "channels": [
        "fangChan"
    ]
}
```

### GET /nodes

Returns a list of all known nsqd

```bash
➜  ~ http http://127.0.0.1:4161/nodes
HTTP/1.1 200 OK
Content-Length: 215
Content-Type: application/json; charset=utf-8
Date: Sun, 11 Aug 2019 03:10:25 GMT
X-Nsq-Content-Type: nsq; version=1.0

{
    "producers": [
        {
            "broadcast_address": "192.168.137.128",
            "hostname": "consul01",
            "http_port": 4151,
            "remote_address": "127.0.0.1:37294",
            "tcp_port": 4150,
            "tombstones": [
                false,
                false
            ],
            "topics": [
                "fang",
                "test"
            ],
            "version": "1.1.0"
        }
    ]
}
```
