## 单元测试

- [https://learning.postman.com/docs/writing-scripts/test-scripts/](https://learning.postman.com/docs/writing-scripts/test-scripts/)

### 检查返回http status 200

```js
pm.test("Status test", function () {
    pm.response.to.have.status(200);
});
pm.test("response must be valid and have a body", function () {
     pm.response.to.be.ok;
     pm.response.to.be.withBody;
     pm.response.to.be.json;
});
```

### 检查返回Header信息

```js
pm.test("Content-Type header is application/json", () => {
  pm.expect(pm.response.headers.get('Content-Type')).to.eql('application/json');
});
```

### 检查返回内容

```js
pm.test("检查自定义状态码", () => {
  const responseJson = pm.response.json();
  pm.expect(responseJson.code).to.eql("200");
});
pm.test("检查自定义状态码", () => {
  const responseJson = pm.response.json();
  pm.expect(responseJson.code).to.be.oneOf([200,401]);
});
```

### 检查返回时间

```js
pm.test("Response time is less than 200ms", () => {
  pm.expect(pm.response.responseTime).to.be.below(200);
});
```
