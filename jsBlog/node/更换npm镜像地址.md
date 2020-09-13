由于学校网络限制，很多时候下载不了nodejs库,我们选择访问方便的镜像库。
1.临时指定镜像源:
```
npm install <registry-name> --registry https://registry.npm.taobao.org
```
2.永久设置:
```
npm config set registry https://registry.npmjs.org  
```
```
npm config list #查看更新后的config设置
```
npm镜像源站点:
[https://registry.npmjs.org](https://registry.npmjs.org)
[https://r.cnpmjs.org](https://r.cnpmjs.org)
[https://registry.npm.taobao.org](https://registry.npm.taobao.org)

也可以安装定制的cnpm命令行工具：
```
$ npm install -g cnpm --registry=https://registry.npm.taobao.org
```

