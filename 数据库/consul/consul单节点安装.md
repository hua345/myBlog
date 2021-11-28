### 下载consul 二进制文件包

官网下载地址: [https://www.consul.io/downloads.html](https://www.consul.io/downloads.html)
选择对应系统的下载包

```bash
➜  consul unzip consul_1.5.2_linux_amd64.zip
Archive:  consul_1.5.2_linux_amd64.zip
  inflating: consul
➜  consul ls
consul  consul_1.5.2_linux_amd64.zip
➜  consul mv consul /usr/local/bin
➜  consul consul
Usage: consul [--version] [--help] <command> [<args>]

Available commands are:
    acl            Interact with Consul's ACLs
    agent          Runs a Consul agent
    catalog        Interact with the catalog
    config         Interact with Consul's Centralized Configurations
    connect        Interact with Consul Connect
    debug          Records a debugging archive for operators
    event          Fire a new event
    exec           Executes a command on Consul nodes
    force-leave    Forces a member of the cluster to enter the "left" state
    info           Provides debugging information for operators.
    intention      Interact with Connect service intentions
    join           Tell Consul agent to join cluster
    keygen         Generates a new encryption key
    keyring        Manages gossip layer encryption keys
    kv             Interact with the key-value store
    leave          Gracefully leaves the Consul cluster and shuts down
    lock           Execute a command holding a lock
    login          Login to Consul using an auth method
    logout         Destroy a Consul token created with login
    maint          Controls node or service maintenance mode
    members        Lists the members of a Consul cluster
    monitor        Stream logs from a Consul agent
    operator       Provides cluster-level tools for Consul operators
    reload         Triggers the agent to reload configuration files
    rtt            Estimates network round trip time between nodes
    services       Interact with services
    snapshot       Saves, restores and inspects snapshots of Consul server state
    tls            Builtin helpers for creating CAs and certificates
    validate       Validate config files/directories
    version        Prints the Consul version
    watch          Watch for changes in Consul
```

### 启动consul agent代理

#### 查看帮助

```bash
➜  consul consul agent -h
Usage: consul agent [options]

  Starts the Consul agent and runs until an interrupt is received. The
  agent represents a single node in a cluster.
HTTP API Options

  -datacenter=<value>
     Datacenter of the agent.

Command Options

  -advertise=<value>
     Sets the advertise address to use.

  -bind=<value>
     Sets the bind address for cluster communication.

  -bootstrap
     Sets server to bootstrap mode.

  -bootstrap-expect=<value>
     Sets server to expect bootstrap mode.

  -client=<value>
     Sets the address to bind for client access. This includes RPC, DNS,
     HTTP, HTTPS and gRPC (if configured).

  -config-dir=<value>
     Path to a directory to read configuration files from. This
     will read every file ending in '.json' as configuration in this
     directory in alphabetical order. Can be specified multiple times.

  -config-file=<value>
     Path to a file in JSON or HCL format with a matching file
     extension. Can be specified multiple times.

  -data-dir=<value>
     Path to a data directory to store agent state.

  -dev
     Starts the agent in development mode.

  -http-port=<value>
     Sets the HTTP API port to listen on.

  -join=<value>
     Address of an agent to join at start time. Can be specified
     multiple times.

  -log-file=<value>
     Path to the file the logs get written to

  -node=<value>
     Name of this node. Must be unique in the cluster.

  -node-id=<value>
     A unique ID for this node across space and time. Defaults to a
     randomly-generated ID that persists in the data-dir.

  -pid-file=<value>
     Path to file to store agent PID.

  -server
     Switches agent to server mode.

  -server-port=<value>
     Sets the server port to listen on.

  -ui
     Enables the built-in static web UI server.

  -ui-content-path=<value>
     Sets the external UI path to a string. Defaults to: /ui/

  -ui-dir=<value>
     Path to directory containing the web UI resources.
```

### 启动consul服务

```bash
consul agent -server -dev -data-dir=~/consul/data -bind=192.168.137.128 -client=0.0.0.0 -node=consul01 -datacenter=shenzhen -ui
==> Starting Consul agent...
           Version: 'v1.5.2'
           Node ID: '5e8d3d15-b048-d0f9-034d-7a420e80da83'
         Node name: 'consul01'
        Datacenter: 'shenzhen' (Segment: '<all>')
            Server: true (Bootstrap: false)
       Client Addr: [0.0.0.0] (HTTP: 8500, HTTPS: -1, gRPC: 8502, DNS: 8600)
      Cluster Addr: 192.168.137.128 (LAN: 8301, WAN: 8302)
           Encrypt: Gossip: false, TLS-Outgoing: false, TLS-Incoming: false, Auto-Encrypt-TLS: false

==> Log data will now stream in as it occurs:

    2019/07/19 18:14:59 [DEBUG] tlsutil: Update with version 1
    2019/07/19 18:14:59 [DEBUG] tlsutil: OutgoingRPCWrapper with version 1
    2019/07/19 18:14:59 [INFO]  raft: Initial configuration (index=1): [{Suffrage:Voter ID:5e8d3d15-b048-d0f9-034d-7a420e80da83 Address:192.168.137.128:8300}]
    2019/07/19 18:14:59 [INFO]  raft: Node at 192.168.137.128:8300 [Follower] entering Follower state (Leader: "")
    2019/07/19 18:14:59 [INFO] serf: EventMemberJoin: consul01.shenzhen 192.168.137.128
    2019/07/19 18:14:59 [INFO] serf: EventMemberJoin: consul01 192.168.137.128
    2019/07/19 18:14:59 [DEBUG] agent/proxy: managed Connect proxy manager started
    2019/07/19 18:14:59 [WARN] agent/proxy: running as root, will not start managed proxies
    2019/07/19 18:14:59 [INFO] consul: Adding LAN server consul01 (Addr: tcp/192.168.137.128:8300) (DC: shenzhen)
    2019/07/19 18:14:59 [INFO] consul: Handled member-join event for server "consul01.shenzhen" in area "wan"
    2019/07/19 18:14:59 [INFO] agent: Started DNS server 0.0.0.0:8600 (udp)
    2019/07/19 18:14:59 [INFO] agent: Started DNS server 0.0.0.0:8600 (tcp)
    2019/07/19 18:14:59 [INFO] agent: Started HTTP server on [::]:8500 (tcp)
    2019/07/19 18:14:59 [INFO] agent: Started gRPC server on [::]:8502 (tcp)
    2019/07/19 18:14:59 [INFO] agent: started state syncer
==> Consul agent running!
```

#### 访问consul

```bash
http://192.168.137.128:8500/ui
```
