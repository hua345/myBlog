> ab 是 apachebench 命令的缩写。
> ab 的原理：ab 命令会创建多个并发访问线程，模拟多个访问者同时对某一 URL 地址进行访问。

#### 1. 安装 ab

```bash
➜  ~ yum provides ab
➜  ~ yum install httpd-tools
➜  ~ ab -h
Usage: ab [options] [http[s]://]hostname[:port]/path
Options are:
    -n requests     Number of requests to perform
    -c concurrency  Number of multiple requests to make at a time
    -t timelimit    Seconds to max. to spend on benchmarking
                    This implies -n 50000
    -s timeout      Seconds to max. wait for each response
                    Default is 30 seconds
    -b windowsize   Size of TCP send/receive buffer, in bytes
    -B address      Address to bind to when making outgoing connections
    -p postfile     File containing data to POST. Remember also to set -T
    -u putfile      File containing data to PUT. Remember also to set -T
    -T content-type Content-type header to use for POST/PUT data, eg.
                    'application/x-www-form-urlencoded'
                    Default is 'text/plain'
    -k              Use HTTP KeepAlive feature
```

#### 2. ab 测试

```bash
ab [options] [http[s]://]hostname[:port]/path
➜  ~ ab -c 1000 -n 100000  http://localhost:8080/

# post 并发测试
ab -n 10 -c 10 -p test.json -T application/json http://localhost:8080/xxx
```

#### 3.1 查看最大允许打开的文件数量

```bash
➜  ~ ulimit -a
-t: cpu time (seconds)              unlimited
-f: file size (blocks)              unlimited
-d: data seg size (kbytes)          unlimited
-s: stack size (kbytes)             8192
-c: core file size (blocks)         0
-m: resident set size (kbytes)      unlimited
-u: processes                       14990
-n: file descriptors                1024
-l: locked-in-memory size (kbytes)  64
-v: address space (kbytes)          unlimited
-x: file locks                      unlimited
-i: pending signals                 14990
-q: bytes in POSIX msg queues       819200
-e: max nice                        0
-r: max rt priority                 0
-N 15:                              unlimited
```

#### 3.2 设置最大允许打开的文件数量

```bash
➜  ~ ulimit -n 20480
```

#### 3.3 KeepAlive

```bash
➜  ~ ab -c 100 -n 10000 http://localhost:8080/
# 保持KeepAlive
Percentage of the requests served within a certain time (ms)
  50%      9
  66%     12
  75%     14
  80%     15
  90%     19
  95%     23
  98%     28
  99%     30
 100%     54 (longest request)

 # 不保持KeepAlive
 Percentage of the requests served within a certain time (ms)
  50%     23
  66%     25
  75%     26
  80%     27
  90%     31
  95%     34
  98%     41
  99%     52
 100%     82 (longest request)
```

#### 4.1 golang gin

```bash
Percentage of the requests served within a certain time (ms)
  50%     23
  66%     25
  75%     26
  80%     27
  90%     30
  95%     33
  98%     37
  99%     39
 100%     53 (longest request)

# 1000并发
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0   91 104.5     82    1116
Processing:    21  121  33.6    119     327
Waiting:        1   93  32.6     95     298
Total:         72  212 104.6    204    1267

Percentage of the requests served within a certain time (ms)
  50%    204
  66%    214
  75%    222
  80%    225
  90%    234
  95%    243
  98%    288
  99%   1167
 100%   1267 (longest request)

 # 5000 并发
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0  264 366.1    104    1138
Processing:     7  137  88.7    122     557
Waiting:        1  110  82.6     91     525
Total:         19  401 411.3    270    1587

Percentage of the requests served within a certain time (ms)
  50%    270
  66%    315
  75%    360
  80%    402
  90%   1212
  95%   1275
  98%   1459
  99%   1572
 100%   1587 (longest request)
```

#### 4.2 node express

```bash
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.4      0       5
Processing:     2   56   9.3     55     111
Waiting:        1   56   9.3     55     111
Total:          6   56   9.2     55     111

Percentage of the requests served within a certain time (ms)
  50%     55
  66%     58
  75%     60
  80%     62
  90%     67
  95%     71
  98%     82
  99%     86
 100%    111 (longest request)

# 1000并发
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0  257 648.1      0    3010
Processing:    25  152  90.1    141     881
Waiting:        1  152  90.1    141     881
Total:         60  410 654.1    150    3342

Percentage of the requests served within a certain time (ms)
  50%    150
  66%    178
  75%    239
  80%    492
  90%   1138
  95%   1188
  98%   3177
  99%   3186
 100%   3342 (longest request)

  # 4000 并发
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0  654 951.2    213    3027
Processing:    84  573 606.7    199    3363
Waiting:        1  572 606.7    199    3363
Total:        127 1226 957.5   1168    6217

Percentage of the requests served within a certain time (ms)
  50%   1168
  66%   1300
  75%   1650
  80%   1883
  90%   3163
  95%   3196
  98%   3219
  99%   3236
 100%   6217 (longest request)
```

#### 4.3 springboot

```bash
# 100并发
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    7   4.3      7      28
Processing:     0   17   9.3     15      90
Waiting:        0   14   9.1     12      88
Total:          1   24  10.0     22     100

Percentage of the requests served within a certain time (ms)
  50%     22
  66%     25
  75%     27
  80%     28
  90%     33
  95%     43
  98%     58
  99%     65
 100%    100 (longest request)

# 1000 并发
Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0  106 195.4     67    1117
Processing:    24  131  67.2    117     484
Waiting:        1  107  55.8     96     442
Total:         54  237 200.4    198    1298

Percentage of the requests served within a certain time (ms)
  50%    198
  66%    224
  75%    244
  80%    256
  90%    315
  95%    396
  98%   1165
  99%   1198
 100%   1298 (longest request)

 # 2000并发
Percentage of the requests served within a certain time (ms)
  50%    410
  66%    477
  75%    502
  80%    513
  90%    594
  95%    683
  98%   1491
  99%   1513
 100%   1562 (longest request)
```
