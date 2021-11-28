[TOC]

## 参考

[概述 · GitBook (ksoong.org)](http://ksoong.org/drools-examples/content/)

[Drools规则引擎 系列教程（二）Drools规则语法 & LHS 条件 ](https://www.ytooo.top/38470.html)

# Drools

>`Rete` 算法最初是由卡内基梅隆大学的 `Charles L.Forgy` 博士在 1974 年发表的论文中所阐述的算法 , 该算法提供了专家系统的一个高效实现
>
>`Rete` 匹配算法是一种进行大量模式集合和大量对象集合间比较的高效方法，通过网络筛选的方法找出所有匹配各个模式的对象和规则。
>
>其核心思想是将分离的匹配项根据内容动态构造匹配树，以达到显著降低计算量的效果。`Rete` 算法可以被分为两个部分：规则编译和规则执行。当`Rete`算法进行事实的断言时，包含三个阶段：匹配、选择和执行，称做 match-select-act cycle。
>
>`Drools` 是一个基于`Charles Forgy’s`的`RETE`算法的，易于访问企业策略、易于调整以及易于管理的开源业务规则引擎，符合业内标准，速度快、效率高。 业务分析师人员或审核人员可以利用它轻松查看业务规则，从而检验是否已编码的规则执行了所需的业务规则。

### 匹配模式

#### 没有约束的匹配模式

不需要满足任何条件，若类型相同，则触发该规则，如：

```java
package people.rules
import com.github.chenjianhua.springbootdrools.dto.People

dialect  "java"

rule "people"
    when
        People()
    then
        System.out.println("people规则执行");
end
```

##### 有条件约束的匹配模式

实事类型相同，且满足条件，则触发该规则，如：

```
package people.rules
import com.github.chenjianhua.springbootdrools.dto.People

dialect  "java"

rule "people"
    when
        People("girl" == sex && "people" == drlType)
    then
        System.out.println("有条件约束的匹配模式");
end
```

#### 匹配并绑定属性

实事类型相同，且满足条件，则触发该规则，并绑定数据

```java
package people.rules
import com.github.chenjianhua.springbootdrools.dto.People

dialect  "java"

rule "girl"
    when
        $p : People(sex == 0 && drlType == "people")
    then
        System.out.println($p.getName() + "是女孩");
end
```

### 约束

  标准Java运算符优先级适用于DRL中的约束运算符，而drl运算符除==和!=运算符外均遵循标准Java语义。

  在drl中 Person( firstName != “John” )类似于 !java.util.Objects.equals(person.getFirstName(), “John”)

| 约束                   | 描述                                                         |
| ---------------------- | ------------------------------------------------------------ |
| !.                     | 使用此运算符可以以空安全的方式取消引用属性。!.运算符左侧的值不能为null（解释为!= null） |
| []                     | 按List索引访问值或Map按键访问值                              |
| <，<=，>，>=           | 在具有自然顺序的属性上使用这些运算符                         |
| ==, !=                 | 在约束中使用这些运算符作为equals()和!equals()方法            |
| &&，\|\|               | 组合关系条件                                                 |
| matches，not matches   | 使用这些运算符可以指示字段与指定的Java正则表达式匹配或不匹配 |
| contains，not contains | 使用这些运算符可以验证Array或字段是否包含或不包含指定值      |
| memberOf，not memberOf | 使用这些运算符可以验证字段是否为定义为变量Array的成员        |
| in，notin              | 使用这些运算符可以指定一个以上的可能值来匹配约束（复合值限制） |

```
People(name contains "芳")
```

