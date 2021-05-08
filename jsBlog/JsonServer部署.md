#### 1. 安装`JSON Server`
```bash
npm install -g cnpm --registry=https://registry.npm.taobao.org
cnpm install -g json-server
```

#### 2. 创建`json`数据文件`db.json`
```json
{
  "posts": [
    { "id": 1, "title": "json-server", "author": "typicode" }
  ],
  "comments": [
    { "id": 1, "body": "some comment", "postId": 1 }
  ],
  "profile": { "name": "typicode" }
}
```
#### 3. 启动`JSON Server`
```
➜  ~ json-server --watch db.json

  \{^_^}/ hi!

  Loading db.json
  Done

  Resources
  http://localhost:3000/posts
  http://localhost:3000/comments
  http://localhost:3000/profile

  Home
  http://localhost:3000

  Type s + enter at any time to create a snapshot of the database
  Watching...
```
#### 路由
```
# Route
GET    /posts
GET    /posts/1
POST   /posts
PUT    /posts/1
PATCH  /posts/1
DELETE /posts/1

# Database
GET /db
```
```
➜  ~ curl http://localhost:3000/posts/1
{
  "id": 1,
  "title": "json-server",
  "author": "typicode"
}

➜  ~ node
> var aa = {
...   "id": 2,
...   "title": "json api",
...   "author": "fangfang"
... }
> JSON.stringify(aa)
'{"id":2,"title":"json api","author":"fangfang"}'

➜  ~ curl -X POST -H 'Content-type':'application/json' -d '{"id":2,"title":"json api","author":"fangfang"}' http://localhost:3000/posts
{
  "id": 2,
  "title": "json api",
  "author": "fangfang"
}
➜  ~ curl 127.0.0.1:3000/posts
{
  "code": 200,
  "msg": "success",
  "data": [
    {
      "id": 1,
      "title": "json-server",
      "author": "typicode"
    },
    {
      "id": 2,
      "title": "json api",
      "author": "fangfang"
    }
  ]
}
```
#### 编辑`server.js`
```
const jsonServer = require('json-server')
const server = jsonServer.create()
const router = jsonServer.router('db.json')
const middlewares = jsonServer.defaults()

const hostname = '0.0.0.0'
const port = 3000
const apiRoute = '/api/v1'

// Set default middlewares (logger, static, cors and no-cache)
server.use(middlewares)

// Add custom routes before JSON Server router
server.get('/echo', (req, res) => {
    res.jsonp(req.query)
})

// To handle POST, PUT and PATCH you need to use a body-parser
// You can use the one used by JSON Server
server.use(jsonServer.bodyParser)

router.render = (req, res) => {
    res.jsonp({
        code: 200,
        msg: 'success',
        data: res.locals.data
    })
}

// Use default router
server.use(apiRoute, router)
server.listen(port, hostname, () => {
    console.log(`JSON Server running at http://${hostname}:${port}/`);
    console.log(`Api Path http://${hostname}:${port}${apiRoute}`);
})
```
