# 参考

- [https://nsq.io/components/nsqd.html](https://nsq.io/components/nsqd.html)

> nsqd is the daemon that receives, queues, and delivers messages to clients.
>
> It can be run standalone but is normally configured in a cluster with nsqlookupd instance(s) (in which case it will announce topics and channels for discovery).
>
> It listens on two TCP ports, one for clients and another for the HTTP API. It can optionally listen on a third port for HTTPS.

- `-broadcast-address` string
    address that will be registered with lookupd (defaults to the OS hostname) (default "consul01")
- `-config` string
    path to config file
- `-data-path` string
    path to store disk-backed messages
- `-http-address` string
    `<addr>:<port>` to listen on for HTTP clients (default "0.0.0.0:4151")
- `-http-client-connect-timeout` duration
    timeout for HTTP connect (default 2s)
- `-http-client-request-timeout` duration
    timeout for HTTP request (default 5s)
- `-lookupd-tcp-address` value
    lookupd TCP address (may be given multiple times)
- `-tcp-address` string
    `<addr>:<port>` to listen on for TCP clients (default "0.0.0.0:4150")

## HTTP API

- /ping - liveness
- /info - version
- /stats - comprehensive runtime telemetry
- /pub - publish a message to a topic
- /mpub - publish multiple messages to a topic
- /config - configure nsqd
- /debug/pprof - pprof debugging portal
- /debug/pprof/profile - generate pprof CPU profile
- /debug/pprof/goroutine - generate pprof goroutine profile
- /debug/pprof/heap - generate pprof heap profile
- /debug/pprof/block - generate pprof blocking profile
- /debug/pprof/threadcreate - generate pprof OS thread profile

## v1 namespace (nsqd v0.2.29+)

- /topic/create - create a new topic
- /topic/delete - delete a topic
- /topic/empty - empty a topic
- /topic/pause - pause message flow for a topic
- /topic/unpause - unpause message flow for a topic
- /channel/create - create a new channel
- /channel/delete - delete a channel
- /channel/empty - empty a channel
- /channel/pause - pause message flow for a channel
- /channel/unpause - unpause message flow for a channel

### POST /pub

Publish a message

#### Query Params

- topic - the topic to publish to
- defer - the time in ms to delay message delivery (optional)

#### Body

raw message bytes

#### Example

```bash
➜  ~ curl -d "hello world 1" http://192.168.137.128:4151/pub\?topic\=test
OK#

➜  ~ http http://192.168.137.128:4151/pub\?topic\=test  hello=world --verbose
POST /pub?topic=test HTTP/1.1
Accept: application/json
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 18
Content-Type: application/json
Host: 192.168.137.128:4151
User-Agent: HTTPie/0.9.4

{
    "hello": "world"
}

HTTP/1.1 200 OK
Content-Length: 2
Content-Type: text/plain; charset=utf-8
Date: Sun, 11 Aug 2019 00:30:25 GMT
X-Nsq-Content-Type: nsq; version=1.0

OK
```

### POST /topic/create

Create a topic

#### Query Params

topic - the topic to create

Example

```bash
➜  ~ http post http://127.0.0.1:4151/topic/create topic==fang --verbose
POST /topic/create?topic=fang HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: 127.0.0.1:4151
User-Agent: HTTPie/0.9.4



HTTP/1.1 200 OK
Content-Length: 0
Date: Sun, 11 Aug 2019 02:24:11 GMT
X-Nsq-Content-Type: nsq; version=1.0
```

### POST /topic/delete

Delete an existing topic (and all channels)

Query Params:

topic - the existing topic to delete
Example:

```bash
➜  ~ http post http://127.0.0.1:4151/topic/delete topic==fang
HTTP/1.1 200 OK
Content-Length: 0
Date: Sun, 11 Aug 2019 02:19:45 GMT
X-Nsq-Content-Type: nsq; version=1.0
```

### POST /channel/create

Create a channel for an existing topic

Query Params:

topic - the existing topic
channel - the channel to create

Example:

```bash
➜  ~ http post http://127.0.0.1:4151/channel/create topic==fang channel==fangChan --verbose
POST /channel/create?topic=fang&channel=fangChan HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: 127.0.0.1:4151
User-Agent: HTTPie/0.9.4



HTTP/1.1 200 OK
Content-Length: 0
Date: Sun, 11 Aug 2019 02:28:00 GMT
X-Nsq-Content-Type: nsq; version=1.0
```

### POST /channel/delete

Delete an existing channel on an existing topic

Query Params:

topic - the existing topic
channel - the existing channel to delete
Example:

```bash
➜  ~ http post http://127.0.0.1:4151/channel/delete topic==fang channel==fangChan --verbose
POST /channel/delete?topic=fang&channel=fangChan HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0
Host: 127.0.0.1:4151
User-Agent: HTTPie/0.9.4



HTTP/1.1 200 OK
Content-Length: 0
Date: Sun, 11 Aug 2019 02:30:01 GMT
X-Nsq-Content-Type: nsq; version=1.0
```
