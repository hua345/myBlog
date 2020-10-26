# [https://github.com/httpie/httpie](https://github.com/httpie/httpie)

> HTTPie 是一个 HTTP 的命令行客户端，目标是让 CLI 和 web 服务之间的交互尽可能的人性化。
> 允许通过自然的语法发送任意 HTTP 请求数据，展示色彩化的输出。

## 1. 主要特性

- 直观的语法
- 格式化和色彩化的终端输出
- 内置 JSON 支持
- 支持上传表单和文件
- HTTPS、代理和认证
- 任意请求数据
- 自定义头部
- 持久性会话
- 类 Wget 下载

### 2.1 安装 httpie

```bash
# linux
yum install httpie

# windows
$ pip install --upgrade pip setuptools
$ pip install --upgrade httpie
```

### 2.2 查看 httpie 版本

```bash
➜  ~ http --debug
HTTPie 0.9.4
Requests 2.22.0
Pygments 1.4
Python 2.7.5 (default, Apr  9 2019, 14:30:50)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-36)]
/usr/bin/python2
Linux 3.10.0-957.12.2.el7.x86_64
```

### 2.3 查看帮助

```bash
➜  ~ http --help
usage: http [--json] [--form] [--pretty {all,colors,format,none}]
            [--style STYLE] [--print WHAT] [--headers] [--body] [--verbose]
            [--all] [--history-print WHAT] [--stream] [--output FILE]
            [--download] [--continue]
            [--session SESSION_NAME_OR_PATH | --session-read-only SESSION_NAME_OR_PATH]
            [--auth USER[:PASS]] [--auth-type {basic,digest}]
            [--proxy PROTOCOL:PROXY_URL] [--follow]
            [--max-redirects MAX_REDIRECTS] [--timeout SECONDS]
            [--check-status] [--verify VERIFY]
            [--ssl {ssl2.3,ssl3,tls1,tls1.1,tls1.2}] [--cert CERT]
            [--cert-key CERT_KEY] [--ignore-stdin] [--help] [--version]
            [--traceback] [--debug]
            [METHOD] URL [REQUEST_ITEM [REQUEST_ITEM ...]]

HTTPie - a CLI, cURL-like tool for humans. <http://httpie.org>
```

### 2.4 参数说明

```bash
METHOD
  The HTTP method to be used for the request (GET, POST, PUT, DELETE, ...).

  This argument can be omitted in which case HTTPie will use POST if there
  is some data to be sent, otherwise GET:

      $ http example.org               # => GET
      $ http example.org hello=world   # => POST
REQUEST_ITEM
  Optional key-value pairs to be included in the request. The separator used
  determines the type:

  ':' HTTP headers:

      Referer:http://httpie.org  Cookie:foo=bar  User-Agent:bacon/1.0

  '==' URL parameters to be appended to the request URI:

      search==httpie

  '=' Data fields to be serialized into a JSON object (with --json, -j)
      or form data (with --form, -f):

      name=HTTPie  language=Python  description='CLI HTTP client'

    '@' Form file fields (only with --form, -f):

      cs@~/Documents/CV.pdf

Output Options:
  --headers, -h
      Print only the response headers. Shortcut for --print=h.

  --body, -b
      Print only the response body. Shortcut for --print=b.

  --download, -d
      Do not print the response body to stdout. Rather, download it and store it
      in a file. The filename is guessed unless specified with --output
      [filename]. This action is similar to the default behaviour of wget.
```

| Item Type                                      | Description                                                                                                                                                                 |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| HTTP Headers Name:Value                        | Arbitrary HTTP header, e.g. X-API-Token:123.                                                                                                                                |
| URL parameters name==value                     | Appends the given name/value pair as a query string parameter to the URL. The == separator is used.                                                                         |
| Data Fields field=value, field=@file.txt       | Request data fields to be serialized as a JSON object (default), or to be form-encoded (--form, -f).                                                                        |
| Raw JSON fields field:=json, field:=@file.json | Useful when sending JSON and one or more fields need to be a Boolean, Number, nested Object, or an Array, e.g., meals:='["ham","spam"]' or pies:=[1,2,3] (note the quotes). |
| Form File Fields field@/dir/file               | Only available with --form, -f. For example screenshot@~/Pictures/img.png. The presence of a file field results in a multipart/form-data request.                           |

### 3.1 httpie 使用

```bash
➜  ~ http httpie.org
HTTP/1.1 301 Moved Permanently
CF-RAY: 4db61fef4f8799a1-LAX
Cache-Control: max-age=3600
Connection: keep-alive
Date: Thu, 23 May 2019 09:50:17 GMT
Expires: Thu, 23 May 2019 10:50:17 GMT
Location: https://httpie.org/
Server: cloudflare
Transfer-Encoding: chunked
Vary: Accept-Encoding
```

### 3.2 只显示 Header

```bash
➜  ~ http -h https://github.com
HTTP/1.1 200 OK
Cache-Control: max-age=0, private, must-revalidate
Content-Encoding: gzip
Content-Type: text/html; charset=utf-8
Date: Thu, 23 May 2019 09:52:48 GMT
ETag: W/"eaa6a1cd16dccc58d2cd8502d04e2ffe"
Expect-CT: max-age=2592000, report-uri="https://api.github.com/_private/browser/errors"
Referrer-Policy: origin-when-cross-origin, strict-origin-when-cross-origin
Server: GitHub.com
```

### 3.3 post json

```bash
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

### 3.3 postjson

```bash
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
