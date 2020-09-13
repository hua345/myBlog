查看[https://github.com/socketio/engine.io-client/blob/master/lib/socket.js#L91](https://github.com/socketio/engine.io-client/blob/master/lib/socket.js#L91)
```
 this.transports = opts.transports || ['polling', 'websocket'];
```
在浏览器可能有些不支持websocket所以通过polling进行握手，再升级到websocket协议。
### 传输方式
```js
engine.io-client:socket creating transport "polling" +0ms
  engine.io-client:polling polling +1ms
  engine.io-client:polling-xhr xhr poll +1ms
  engine.io-client:polling-xhr xhr open GET: http://localhost/socket.io/?EIO=3&transport=polling&t=1445497479724-0&b64=1 +2ms
  engine.io-client:polling-xhr xhr data null +1ms
  engine.io-client:socket setting transport polling +10ms
  socket.io-client:manager connect attempt will timeout after 20000 +16ms
  socket.io-client:manager readyState opening +3ms
  engine.io-client:polling polling got data 97:0{"sid":"y6Nk3xhxL_IXSkK_AAAG","upgrades":["websocket"],"pingInterval":25000,"pingTimeout":60000} +26ms
  engine.io-client:socket socket receive: type "open", data "{"sid":"y6Nk3xhxL_IXSkK_AAAG","upgrades":["websocket"],"pingInterval":25000,"pingTimeout":60000}" +1ms
  engine.io-client:socket socket open +1ms
  socket.io-client:manager open +25ms
  socket.io-client:socket transport is open - connecting +0ms
  socket.io-client:manager writing packet {"type":0,"nsp":"/chat"} +1ms
  socket.io-parser encoding packet {"type":0,"nsp":"/chat"} +0ms
  socket.io-parser encoded {"type":0,"nsp":"/chat"} as 0/chat +0ms
  engine.io-client:socket flushing 1 packets in socket +1ms
  engine.io-client:polling-xhr xhr open POST: http://localhost/socket.io/?EIO=3&transport=polling&t=1445497479766-1&b64=1&sid=y6Nk3xhxL_IXSkK_AAAG +2ms
  engine.io-client:polling-xhr xhr data 7:40/chat +0ms
  engine.io-client:socket starting upgrade probes +5ms
  engine.io-client:socket probing transport "websocket" +0ms
  engine.io-client:socket creating transport "websocket" +0ms
  engine.io-client:polling polling +5ms
  engine.io-client:polling-xhr xhr poll +0ms
  engine.io-client:polling-xhr xhr open GET: http://localhost/socket.io/?EIO=3&transport=polling&t=1445497479777-2&b64=1&sid=y6Nk3xhxL_IXSkK_AAAG +0ms
  engine.io-client:polling-xhr xhr data null +0ms
  engine.io-client:polling polling got data 2:407:40/chat +10ms
  engine.io-client:socket socket receive: type "message", data "0" +0ms
  socket.io-parser decoded 0 as {"type":0,"nsp":"/"} +24ms
  engine.io-client:socket socket receive: type "message", data "0/chat" +3ms
  socket.io-parser decoded 0/chat as {"type":0,"nsp":"/chat"} +2ms
connect to server
  socket.io-client:manager writing packet {"type":2,"data":["close-info","client close after 10s"],"nsp":"/chat"} +27ms
  socket.io-parser encoding packet {"type":2,"data":["close-info","client close after 10s"],"nsp":"/chat"} +1ms
  socket.io-parser encoded {"type":2,"data":["close-info","client close after 10s"],"nsp":"/chat"} as 2/chat,["close-info","client close after 10s"] +0ms
  engine.io-client:socket flushing 1 packets in socket +2ms
  engine.io-client:polling-xhr xhr open POST: http://localhost/socket.io/?EIO=3&transport=polling&t=1445497479792-3&b64=1&sid=y6Nk3xhxL_IXSkK_AAAG +0ms
  engine.io-client:polling-xhr xhr data 47:42/chat,["close-info","client close after 10s"] +0ms
  engine.io-client:polling polling +1ms
  engine.io-client:polling-xhr xhr poll +0ms
  engine.io-client:polling-xhr xhr open GET: http://localhost/socket.io/?EIO=3&transport=polling&t=1445497479793-4&b64=1&sid=y6Nk3xhxL_IXSkK_AAAG +0ms
  engine.io-client:polling-xhr xhr data null +0ms
  engine.io-client:socket probe transport "websocket" opened +5ms
  engine.io-client:socket probe transport "websocket" pong +13ms
  engine.io-client:socket pausing current transport "polling" +1ms
  engine.io-client:polling we are currently polling - waiting to pause +0ms
  engine.io-client:polling polling got data 1:6 +97ms
  engine.io-client:socket socket receive: type "noop", data "undefined" +0ms
  engine.io-client:polling pre-pause polling complete +0ms
  engine.io-client:polling paused +0ms
  engine.io-client:socket changing transport and sending upgrade packet +0ms
  engine.io-client:socket setting transport websocket +0ms
  engine.io-client:socket clearing existing transport polling +1ms
  engine.io-client:polling ignoring poll - transport state "paused" +0ms

```
socket.io先是以polling方式GET和POST一些数据，包括握手和开始的一些事件，升级到websocket后就采用websocket传输了。

设置直接使用websocket
```
#服务器
var io = require('socket.io')(httpServer,{
   "serveClient": false ,
   "transports":['websocket', 'polling']
 });
#客户端
var socket = require('socket.io-client')('http://localhost/chat',   {
  "transports":['websocket', 'polling']
});
```

```
engine.io-client:socket creating transport "websocket" +0ms
  engine.io-client:socket setting transport websocket +21ms
  socket.io-client:manager connect attempt will timeout after 20000 +23ms
  socket.io-client:manager readyState opening +1ms
  engine.io-client:socket socket receive: type "open", data "{"sid":"Qg_OFtQ_G3c5OfNnAAAB","upgrades":[],"pingInterval":25000,"pingTimeout":60000}" +51ms
  engine.io-client:socket socket open +1ms
  socket.io-client:manager open +50ms
  socket.io-client:socket transport is open - connecting +0ms
  socket.io-client:manager writing packet {"type":0,"nsp":"/chat"} +1ms
  socket.io-parser encoding packet {"type":0,"nsp":"/chat"} +0ms
  socket.io-parser encoded {"type":0,"nsp":"/chat"} as 0/chat +0ms
  engine.io-client:socket flushing 1 packets in socket +2ms
  engine.io-client:socket socket receive: type "message", data "0" +6ms
  socket.io-parser decoded 0 as {"type":0,"nsp":"/"} +8ms
  engine.io-client:socket socket receive: type "message", data "0/chat" +4ms
  socket.io-parser decoded 0/chat as {"type":0,"nsp":"/chat"} +4ms
connect to server
```
