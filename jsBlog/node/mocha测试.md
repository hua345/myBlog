### 参照:
[ 初识 mocha in NodeJS  ](https://cnodejs.org/topic/516526766d38277306c7d277)
[测试驱动开发(TDD)及测试框架Mocha.js入门学习](http://www.mamicode.com/info-detail-852916.html)
[http://mochajs.org/](http://mochajs.org/)

### Mocha.js是被广泛使用的Javascript测试框架, 支持TDD，BDD等多种接口
### The test/ Directory
By default, mocha looks for the glob ./test/*.js, so you may want to put your tests in test/ folder.
```
$ npm install -g mocha
$ mkdir test
$ vi test/test.js
```
以下为最简单的一个mocha示例：
```
var assert = require("assert");
describe('Array', function() {
  describe('#indexOf()', function () {
    it('should return -1 when the value is not present', function () {
      assert.equal(-1, [1,2,3].indexOf(5));
      assert.equal(-1, [1,2,3].indexOf(0));
    });
  });
});

```
- **describe (moduleName, testDetails)**
由上述代码可看出，describe是可以嵌套的，比如上述代码嵌套的两个describe就可以理解成测试人员希望测试Array模块下的#indexOf() 子模块。module_name 是可以随便取的，关键是要让人读明白就好。
- **it (info, function)**
一个it对应一个实际的test case
### Asynchronous
```
var fs = require("fs");
describe('File', function(){
    describe('#readFile()', function(){
        it('should read file1 without error', function(done){
            fs.readFile('file1', function(err){
                if (err) throw err;
                done();
            });
        })
    })
})
```
- **done ()**
按照瀑布流编程习惯，取名done是表示你回调的最深处，也就是结束写嵌套回调函数。但对于回调链来说done实际上意味着告诉mocha从此处开始测试，一层层回调回去。
### Hooks
Mocha提供before(),after(),beforeEach()和afterEach()挂钩,测试时用来准备条件和清理数据.
```
describe('hooks', function() {
  before(function() {
     console.log('runs before all tests in this block');
  });
  beforeEach(function() {
     console.log('runs before each test in this block');
  });
  describe('#indexOf()', function() {
    it('should return -1 when not present', function() {
      assert.equal(-1, [1,2,3].indexOf(4));
    });
    it('should return -1 when not present', function() {
      assert.equal(-1, [1,2,3].indexOf(-1));
    });
  });
});
```
### Dynamically Generating Tests
```
function add() {
  return Array.prototype.slice.call(arguments).reduce(function(prev, curr) {
    return prev + curr;
  }, 0);
}

describe('add()', function() {
  var tests = [
    {args: [1, 2],       expected: 3},
    {args: [1, 2, 3],    expected: 6},
    {args: [1, 2, 3, 4], expected: 10}
  ];

  tests.forEach(function(test) {
    it('correctly adds ' + test.args.length + ' args', function() {
      var res = add.apply(null, test.args);
      assert.equal(res, test.expected);
    });
  });
});
```
### Timeouts
可以为测试套件和组件设置Timeouts.
```
describe('a suite of tests', function() {
  this.timeout(500);

  it('should take less than 500ms', function(done){
    setTimeout(done, 300);
  });

  it('should take less than 500ms as well', function(done){
    setTimeout(done, 200);
  });
})
```
### Test Driven Develop (TDD)
mocha默认的模式是Behavior Driven Develop (BDD)，**在TDD的设想中，测试用例为先，是第一要务。**
在TDD中有suite(), test(), suiteSetup(), suiteTeardown(), setup(), and teardown().

- suite就是一组测试用例的集合，可用于对测试用例进行分类.
- suiteSetup：此方法会在这个suite所有测试用例执行前执行一次，只一次，这是跟setup的区别。
- setup：此方法会在每个测试用例执行前都执行一遍。
- test：具体执行的测试用例实现代码。
```
suite('Array', function() {
  setup(function() {
    console.log("setup init data");
  });
  suiteSetup(function(){
  
  })
  suite('#indexOf()', function() {
    test('should return -1 when not present', function() { 
      assert.equal(-1, [1,2,3].indexOf(4));
    });
  });
});

```
要想执行TDD的test的时候需要加上参数，如
```
mocha -u tdd 
```
### 常用参数
```
-R, --reporter <name>                   specify the reporter to use
-r, --require <name>                    require the given module
-u, --ui <name>                         specify user-interface (bdd|tdd|exports)
--check-leaks                           check for global variable leaks
--compilers <ext>:<module>,...          use the given module(s) to compile files
```
###修改package.json
```
 "scripts": {
   "start": "node ./bin/www",
   "test": "mocha -u tdd  --reporter spec --check-leaks test/ "
 }
```
### Reporters
```
mocha  test.js  -R spec
```
spec - hierarchical spec list   默认显示风格
![这里写图片描述](http://img.blog.csdn.net/20151010152505944)
dot - dot matrix
![这里写图片描述](http://img.blog.csdn.net/20151010152559509)
 list - spec-style listing
![这里写图片描述](http://img.blog.csdn.net/20151010153057082)

