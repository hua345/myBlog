用js写点canvas画图，比如读取图片数据时，需要HTTP支持，所以用nodejs写了个静态文件服务器，不过后来也没怎没用用nginx了。

```js
var http        = require("http");
var fs          = require("fs");
var url         = require("url");
var querystring = require("querystring");
var ROOT        = "./";
var get =function(req,res){
    //readFile
    var pathname = url.parse(req.url).pathname;
    var filename = pathname.replace("/","./");
    fs.stat(filename,function(err,stat){
        if(err){
            res.writeHead(404);
            res.end("cann't find file!");
            return;
        }
        var lastModified = stat.mtime.toUTCString();
        //cache-control
        if(lastModified === req.headers["if-modified-since"]){
            res.setHeader("Content-Type","text/html");
            res.setHeader("Server","Nodejs");
            res.writeHead(304,"from cache");
            res.end();
            }
        else{
            fs.readFile(filename,function(err,file){
            res.setHeader("Last-Modified",lastModified);
            res.setHeader("Content-Type","text/html");
            res.setHeader("Server","Nodejs");
            res.writeHead(200,"OK");
            res.end(file);
        });
        }
        });

    }
http.createServer(function(req,res){
switch(req.method){
    case 'GET':
       get(req,res);
       break;
    case 'POST':
       update(req,res);
       break;
    case 'DELETE':
       remove(req,res);
       break;
    case 'PUT':
       create(req,res);
       break;
    default:
       get(req,res);
    }
}).listen(8002,"127.0.0.1");
console.log("server runat 127.0.0.1:8002");
```

`nodejs`的小技巧：
运行时按`Ctrl + C`退出,这样可以方便重启;
