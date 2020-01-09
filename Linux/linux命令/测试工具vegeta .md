# [https://github.com/tsenart/vegeta](https://github.com/tsenart/vegeta)

```bash
go get -u github.com/tsenart/vegeta
```

```yaml
➜  ~ vegeta -h
Usage: vegeta [global flags] <command> [command flags]

global flags:
  -cpus int
        Number of CPUs to use (default 4)
  -profile string
        Enable profiling of [cpu, heap]
  -version
        Print version and exit

attack command:
  -body string
        Requests body file
  -cert string
        TLS client PEM encoded certificate file
  -connections int
        Max open idle connections per target host (default 10000)
  -duration duration
        Duration of the test [0 = forever]
  -format string
        Targets format [http, json] (default "http")
  -h2c
        Send HTTP/2 requests without TLS encryption
  -header value
        Request header
  -http2
        Send HTTP/2 requests when supported by the server (default true)
  -insecure
        Ignore invalid server TLS certificates
  -keepalive
        Use persistent connections (default true)
  -laddr value
        Local IP address (default 0.0.0.0)
  -lazy
       Read targets lazily
  -max-body value
       Maximum number of bytes to capture from response bodies. [-1 = no limit] (default -1)
  -name string
       Attack name
  -output string
       Output file (default "stdout")
  -rate value
       Number of requests per time unit (default 50/1s)
  -redirects int
       Number of redirects to follow. -1 will not follow but marks as success (default 10)
  -resolvers value
       List of addresses (ip:port) to use for DNS resolution. Disables use of local system DNS. (comma separated list)
  -root-certs value
       TLS root certificate files (comma separated list)
  -targets string
       Targets file (default "stdin")
  -timeout duration
       Requests timeout (default 30s)
examples:
  echo "GET http://localhost/" | vegeta attack -duration=5s | tee results.bin | vegeta report
  vegeta report -type=json results.bin > metrics.json
  cat results.bin | vegeta plot > plot.html
  cat results.bin | vegeta report -type="hist[0,100ms,200ms,300ms]"
```

## vegeta 示例

```bash
echo "GET http://localhost:8080/" | \
vegeta attack -http2 -keepalive -duration=5s -rate 1000 | \
tee results.bin | vegeta report

Requests      [total, rate]            5000, 1000.45
Duration      [total, attack, wait]    4.998617048s, 4.997756372s, 860.676µs
Latencies     [mean, 50, 95, 99, max]  1.994552ms, 810.298µs, 5.247249ms, 33.03017ms, 63.756222ms
Bytes In      [total, mean]            130000, 26.00
Bytes Out     [total, mean]            0, 0.00
Success       [ratio]                  100.00%
Status Codes  [code:count]             200:5000

echo "GET http://localhost:8080/" | \
vegeta attack -http2=false -keepalive=false -duration=5s -rate 1000 | \
tee results.bin | vegeta report

Requests      [total, rate]            5000, 1000.12
Duration      [total, attack, wait]    5.001122657s, 4.999399936s, 1.722721ms
Latencies     [mean, 50, 95, 99, max]  13.06756ms, 4.068804ms, 64.649063ms, 167.893529ms, 241.467486ms
Bytes In      [total, mean]            130000, 26.00
Bytes Out     [total, mean]            0, 0.00
Success       [ratio]                  100.00%
Status Codes  [code:count]             200:5000
Error Set:

echo "GET http://localhost:8080/" | \
vegeta attack -http2=false -keepalive -duration=5s -rate 1000 | \
tee results.bin | vegeta report

Requests      [total, rate]            5000, 1000.10
Duration      [total, attack, wait]    5.001149915s, 4.999519475s, 1.63044ms
Latencies     [mean, 50, 95, 99, max]  1.924871ms, 731.831µs, 5.176089ms, 30.490032ms, 73.876369ms
Bytes In      [total, mean]            130000, 26.00
Bytes Out     [total, mean]            0, 0.00
Success       [ratio]                  100.00%
Status Codes  [code:count]             200:5000
Error Set:
```
