#### 参考

- [@Validated和@Valid区别：Spring validation验证框架对入参实体进行嵌套验证必须在相应属性（字段）加上@Valid而不是@Validated](https://blog.csdn.net/qq_27680317/article/details/79970590)

#### 1.1 @Validated和@Valid区别

> `Spring Validation`验证框架对参数的验证机制提供了`@Validated`
`javax`提供了`@Valid`
在检验Controller的入参是否符合规范时，
使用@Validated或者@Valid在基本验证功能上没有太多区别
主要是支持嵌套验证上的区别：

- @Validated:不能用在成员属性（字段）上，也无法提示框架进行嵌套验证。能配合嵌套验证注解@Valid进行嵌套验证。
- @Valid：能够用在成员属性（字段）上，提示验证框架进行嵌套验证。能配合嵌套验证注解@Valid进行嵌套验证。

#### 1.2 嵌套验证

比如我们现在有个实体叫做Item:

```java
public class Item {

    @NotNull(message = "id不能为空")
    @Min(value = 1, message = "id必须为正整数")
    private Long id;

    @NotNull(message = "props不能为空")
    @Size(min = 1, message = "至少要有一个属性")
    private List<Prop> props;
}
```

Item带有很多属性，属性里面有属性id，属性值id，属性名和属性值，如下所示：

```java
public class Prop {

    @NotNull(message = "pid不能为空")
    @Min(value = 1, message = "pid必须为正整数")
    private Long pid;

    @NotNull(message = "vid不能为空")
    @Min(value = 1, message = "vid必须为正整数")
    private Long vid;

    @NotBlank(message = "pidName不能为空")
    private String pidName;

    @NotBlank(message = "vidName不能为空")
    private String vidName;
}
```

现在我们有个ItemController接受一个Item的入参，想要对Item进行验证，如下所示：

```java
@RestController
public class ItemController {

    @RequestMapping("/item/add")
    public void addItem(@Validated Item item, BindingResult bindingResult) {
        doSomething();
    }
}
```

> 如果Item实体的props属性不额外加注释，只有@NotNull和@Size
@Validated和@Valid加在方法参数前，都不会自动对参数进行嵌套验证。
我们修改Item类如下所示：

```java
public class Item {

    @NotNull(message = "id不能为空")
    @Min(value = 1, message = "id必须为正整数")
    private Long id;

    @Valid // 嵌套验证必须用@Valid
    @NotNull(message = "props不能为空")
    @Size(min = 1, message = "props至少要有一个自定义属性")
    private List<Prop> props;
}
```

#### 2. javax.validation.constraints

|约束|详细信息|
|----------|----------|
|@Null|验证对象是否为null|
|@NotNull|验证对象是否不为null, 无法查检长度为0的字符串|
|@NotBlank|只能作用在String上，不能为null，而且调用trim()后，长度必须大于0|
|@NotEmpty|校验对象（Array,Collection,Map,String）是否为null，并且不为Empty|
|@AssertTrue|校验对象必须为 true|
|@AssertFalse|校验对象必须为 false|
|@Min(value)|校验对象必须是一个数字，其值必须大于等于指定的最小值|
|@Max(value)|校验对象必须是一个数字，其值必须小于等于指定的最大值|
|@Size(min=, max=)| 校验对象（Array,Collection,Map,String）大小是否在给定的范围之内|
|@Pattern(regex=) |  校验时间String 对象是否符合正则表达式的规则|
|@Email|校验邮箱|
|@Valid |递归的对关联对象进行校验, 如果关联对象是个集合或者数组,那么对其中的元素进行递归校验,如果是一个map,则对其中的值部分进行校验|

#### 3. org.hibernate.validator.constraints

|约束|详细信息|
|----------|----------|
|@Length(min=, max=)|校验字符串长度|
|@Range(min=, max=)|校验对象Integer, Decimal值大小|

```java
@Validated @RequestBody
```

#### 4.1 参数校验异常

```java
    @PostMapping(path = "/")
    public ResponseVO<GetUserOutputDTO> addUser(@Valid @RequestBody GetUserInputDTO param)
```

校验错误时，抛出`MethodArgumentNotValidException`异常

```java
    @GetMapping(path = "/")
    public ResponseVO<GetUserOutputDTO> getUser(@Valid GetUserInputDTO param)
```

校验错误时，抛出`BindException`异常

```java
    @GetMapping(path = "/")
    public ResponseVO<GetUserOutputDTO> getUser(@RequestParam String name)
```

没有传递参数name时，抛出`MissingServletRequestParameterException`异常

```java
@RestController
@RequestMapping(path = "/api/v1/user")
@Validated
public class UserController {
    @GetMapping(path = "/")
    public ResponseVO<GetUserOutputDTO> getUser(@NotBlank(message = "名字不能为空") @RequestParam String name)
}
```

校验错误时，抛出`ConstraintViolationException`异常

#### 4.2 参数异常处理

```java
    /**
     * 处理Get请求中 使用@Valid 验证路径中请求实体校验失败后抛出的异常
     * 参数校验不通过异常处理
     * //@GetMapping(path = "/")
     * public ResponseVO<GetUserOutputDTO> getUser(@Valid/@Validated GetUserInputDTO param)
     *
     * @param e validation 校验异常
     * @return 返回给前台的响应实体，会被Jackson序列化成json
     */
    @ExceptionHandler(BindException.class)
    @ResponseBody
    public ResponseVO bindExceptionHandler(BindException e) {
        log.info("BindException Handler--- ERROR: {}", JSON.toJSONString(e.getBindingResult().getAllErrors()));
        String message = e.getBindingResult().getAllErrors()
                .stream().map(DefaultMessageSourceResolvable::getDefaultMessage)
                .collect(Collectors.joining());
        ResponseVO<String> response = ResponseUtil.fail(ResponseStatusEnum.PARAMETER_CHECK_ERROR);
        response.setData(message);
        return response;
    }

    /**
     * 使用@RequestParam上validate失败后抛出的异常是javax.validation.ConstraintViolationException
     * 处理请求参数格式错误
     * //@Validated
     * public class UserController {
     * //   @GetMapping(path = "/")
     * public ResponseVO<GetUserOutputDTO> getUser(@NotBlank(message = "名字不能为空") @RequestParam String name)
     * }
     *
     * @param e ConstraintViolationException
     * @return ResponseVO
     */
    @ExceptionHandler(ConstraintViolationException.class)
    @ResponseBody
    public ResponseVO constraintViolationExceptionHandler(ConstraintViolationException e) {
        log.info("ConstraintViolationException Handler--- ERROR: {}", e.getConstraintViolations());
        String message = e.getConstraintViolations().stream()
                .map(ConstraintViolation::getMessage).collect(Collectors.joining());
        ResponseVO<String> response = ResponseUtil.fail(ResponseStatusEnum.PARAMETER_CHECK_ERROR);
        response.setData(message);
        return response;
    }

    /**
     * 使用@Validated @RequestBody上校验参数失败后抛出的异常是MethodArgumentNotValidException异常。
     * org.springframework.validation.annotation.Validated
     * //@PostMapping(path = "/")
     * public ResponseVO<GetUserOutputDTO> addUser(@Valid/@Validated @RequestBody GetUserInputDTO param)
     *
     * @param e MethodArgumentNotValidException 校验异常
     * @return 返回给前台的响应实体，会被Jackson序列化成json
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseBody
    public ResponseVO methodArgumentNotValidException(MethodArgumentNotValidException e) {
        List<ObjectError> errors = e.getBindingResult().getAllErrors();
        StringBuffer errorMsg = new StringBuffer();
        errors.forEach(x -> errorMsg.append(x.getDefaultMessage()).append(";"));
        log.error("MethodArgumentNotValidException Handler--- ERROR: {}", errorMsg.toString());
        ResponseVO<String> response = ResponseUtil.fail(ResponseStatusEnum.PARAMETER_CHECK_ERROR);
        response.setData(errorMsg.toString());
        return response;
    }
```
