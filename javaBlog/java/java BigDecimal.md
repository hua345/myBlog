# 简介

> float和double类型的主要设计目的是为了科学计算和工程计算。它们执行二进制浮点运算，这是为了在广域数值范围上提供较为精确的快速近似计算而精心设计的。然而，它们没有提供完全精确的结果，所以不应该被用于要求精确结果的场合，而BigDecimal则适用于商业高精度计算 。
> 使用 float或者double精确地表示0.1(或者10的任何负数次方值)是不可能的，因为在二进制中是无法精确表示这些数字，就像十进制中无法精确表示1/3一样。

## BigDecimal 常用构造函数

- BigDecimal(int)
  创建一个具有参数所指定整数值的对象

- BigDecimal(double)
  创建一个具有参数所指定双精度值的对象
- BigDecimal(long),创建一个具有参数所指定长整数值的对象
- BigDecimal(String),创建一个具有参数所指定以字符串表示的数值的对象

```java
BigDecimal doubleNum = new BigDecimal(0.1);
BigDecimal strNum = new BigDecimal("0.1");
System.out.println("doubleNum:" + doubleNum);
System.out.println("strNum:" + strNum);
```

打印结果

```log
doubleNum:0.1000000000000000055511151231257827021181583404541015625
strNum:0.1
```

- String 构造方法是完全可预知的：`BigDecimal("0.1")` 将创建一个 `BigDecimal`，它正好等于预期的`0.1`。因此，比较而言， 通常建议优先使用 String 构造方法。
- 当`double`必须用作`BigDecimal`的源时，请注意，此构造方法提供了一个准确转换；
- 它不提供与以下操作相同的结果：先使用`Double.toString(double)`方法，然后使用`BigDecimal(String)`构造方法，将 double 转换为 String。要获取该结果，请使用 static valueOf(double)方法。

### BigDecimal 大小比较

java 中对 BigDecimal 比较大小一般用的是 bigdemical 的 compareTo 方法

### BigDecimal 去掉科学计数法

```java
Double num = 12345678910.11;
System.out.println(num);
NumberFormat NF = NumberFormat.getInstance();
//去掉科学计数法显示
NF.setGroupingUsed(false);
System.out.println(NF.format(num));
// 1.234567891011E10
// 12345678910.11
```

### BigDecimal 格式化

由于 NumberFormat 类的 format()方法可以使用 BigDecimal 对象作为其参数，可以利用 BigDecimal 对超出 16 位有效数字的货币值，百分值，以及一般数值进行格式化控制。

```java
//建立货币格式化引用
NumberFormat currency = NumberFormat.getCurrencyInstance();
//建立百分比格式化引用
NumberFormat percent = NumberFormat.getPercentInstance();
//百分比小数点最多3位
percent.setMaximumFractionDigits(3);
//贷款金额
BigDecimal loanAmount = new BigDecimal("21000");
//年利率
BigDecimal interestRate = new BigDecimal("0.053");
//相乘
BigDecimal interest = loanAmount.multiply(interestRate);

System.out.println("贷款金额: " + currency.format(loanAmount));
System.out.println("利率: " + percent.format(interestRate));
System.out.println("利息: " + currency.format(interest));
```

```log
贷款金额: ￥21,000.00
利率: 5.3%
利息: ￥1,113.00
```

### BigDecimal 的运算——加减乘除

```java
BigDecimal num1 = new BigDecimal("3");
BigDecimal num2 = new BigDecimal("4");
BigDecimal addResult = num2.add(num1);
System.out.println("4+3: " + addResult);
BigDecimal subtractResult = num2.subtract(num1);
System.out.println("4-3: " + subtractResult);
BigDecimal multiplyResult = num2.multiply(num1);
System.out.println("4*3: " + multiplyResult);
// 使用除法函数在divide的时候要设置各种参数，要精确的小数位数和舍入模式
// public BigDecimal divide(BigDecimal divisor, int scale, int roundingMode)
BigDecimal divideResult = num2.divide(num1,4,BigDecimal.ROUND_HALF_DOWN);
System.out.println("4/3: " + divideResult);
```

### 相除时BigDecimal舍入模式

#### ROUND_UP

向远离零的方向舍入。舍弃非零部分，并将非零舍弃部分相邻的一位数字加一。

#### ROUND_DOWN

向接近零的方向舍入。舍弃非零部分，同时不会非零舍弃部分相邻的一位数字加一，采取截取行为。

#### ROUND_CEILING

向正无穷的方向舍入。如果为正数，舍入结果同ROUND_UP一致；如果为负数，舍入结果同ROUND_DOWN一致。注意：此模式不会减少数值大小。

#### ROUND_FLOOR

向负无穷的方向舍入。如果为正数，舍入结果同ROUND_DOWN一致；如果为负数，舍入结果同ROUND_UP一致。注意：此模式不会增加数值大小。

#### ROUND_HALF_UP

向“最接近”的数字舍入，如果与两个相邻数字的距离相等，则为向上舍入的舍入模式。如果舍弃部分>= 0.5，则舍入行为与ROUND_UP相同；否则舍入行为与ROUND_DOWN相同。这种模式也就是我们常说的我们的“四舍五入”。

#### ROUND_HALF_DOWN

向“最接近”的数字舍入，如果与两个相邻数字的距离相等，则为向下舍入的舍入模式。如果舍弃部分> 0.5，则舍入行为与ROUND_UP相同；否则舍入行为与ROUND_DOWN相同。这种模式也就是我们常说的我们的“五舍六入”。

#### ROUND_HALF_EVEN

向“最接近”的数字舍入，如果与两个相邻数字的距离相等，则相邻的偶数舍入。如果舍弃部分左边的数字奇数，则舍入行为与 ROUND_HALF_UP 相同；如果为偶数，则舍入行为与 ROUND_HALF_DOWN 相同。注意：在重复进行一系列计算时，此舍入模式可以将累加错误减到最小。此舍入模式也称为“银行家舍入法”，主要在美国使用。四舍六入，五分两种情况，如果前一位为奇数，则入位，否则舍去。

#### ROUND_UNNECESSARY

断言请求的操作具有精确的结果，因此不需要舍入。如果对获得精确结果的操作指定此舍入模式，则抛出ArithmeticException。
