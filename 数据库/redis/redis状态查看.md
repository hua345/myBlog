## redis状态查看

```bash
info
"# Server
redis_version:4.0.12
redis_git_sha1:00000000
redis_git_dirty:0
redis_build_id:a126988df423134e
redis_mode:standalone
os:Linux 3.10.0-693.2.2.el7.x86_64 x86_64
arch_bits:64
multiplexing_api:epoll
#查看连接数
info clients
"# Clients
connected_clients:2631
client_longest_output_list:0
client_biggest_input_buf:0
blocked_clients:0
"
# 允许最大连接数
config get maxclients
1) "maxclients"
2) "10000"

# 客户端连接列表
client list
```

