const http = require("http");
const fs = require("fs");
const url = require("url");
const querystring = require("querystring");
const ROOT = "./";

const get = function (req, res) {
    //readFile
    var pathname = url.parse(req.url).pathname;
    var filename = pathname.replace("/", ROOT);
    if (ROOT == filename) {
        filename = ROOT + "dist/index.html"
    }
    console.log("http get: ", filename);
    fs.stat(filename, function (err, stat) {
        if (err) {
            res.writeHead(404);
            res.end("cann't find file!");
            return;
        }
        var lastModified = stat.mtime.toUTCString();
        //cache-control
        if (lastModified === req.headers["if-modified-since"]) {
            res.setHeader("Content-Type", "text/html");
            res.setHeader("Server", "Nodejs");
            res.writeHead(304, "from cache");
            res.end();
        } else {
            fs.readFile(filename, function (err, file) {
                res.setHeader("Last-Modified", lastModified);
                res.setHeader("Content-Type", "text/html");
                res.setHeader("Server", "Nodejs");
                res.writeHead(200, "OK");
                res.end(file);
            });
        }
    });
}

http.createServer(function (req, res) {
    switch (req.method) {
        case 'GET':
            get(req, res);
            break;
        case 'POST':
            update(req, res);
            break;
        case 'DELETE':
            remove(req, res);
            break;
        case 'PUT':
            create(req, res);
            break;
        default:
            get(req, res);
    }
}).listen(8002);
console.log("server run at 0.0.0.0:8002");