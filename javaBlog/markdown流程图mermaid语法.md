# Mermaid 简介

`Mermaid` 是一个用于画流程图、状态图、时序图、甘特图的库，使用 JS 进行本地渲染，广泛集成于许多 Markdown 编辑器中。

- [https://github.com/mermaid-js/mermaid](https://github.com/mermaid-js/mermaid)
- [https://mermaid-js.github.io/mermaid/#/](https://mermaid-js.github.io/mermaid/#/)

## Vscode 安装插件`Markdown Preview Mermaid Support`

## 饼图

```mermaid
pie title 编程语言
         "golang" : 30
         "java" : 50
         "js":20
```

## 时序图

```mermaid
sequenceDiagram
    participant John
    participant Alice
    Alice->>+John: Hello John, how are you?
    John-->>-Alice: Great!
```

### Messages

Messages can be of two displayed either solid or with a dotted line.

`[Actor][arrow][Actor]:Message text`

There are six types of arrows currently supported:

| Type | Description                                 |
| ---- | ------------------------------------------- |
| ->   | Solid line without arrow                    |
| -->  | Dotted line without arrow                   |
| ->>  | Solid line with arrowhead                   |
| -->> | Dotted line with arrowhead                  |
| -x   | Solid line with a cross at the end (async)  |
| --x  | Dotted line with a cross at the end (async) |

## 类图

```mermaid
classDiagram
    class BankAccount
    BankAccount : +String owner
    BankAccount : +Bigdecimal balance
    BankAccount : +deposit(amount)
    BankAccount : +withdrawl(amount)
```

## 状态图

```mermaid
stateDiagram
[*] --> Still
Still --> [*]
Still --> Moving
Moving --> Still
Moving --> Crash
Crash --> [*]
```

## 流程图

```mermaid
graph LR
A[长方形] -- 链接 --> B((圆))
A --> C(圆角长方形)
B --> D{菱形}
C --> D
```

### 流程图方向

流程图方向有下面几个值

- `TB` 从上到下(TopBottom)
- `BT` 从下到上(BottomTop)
- `RL` 从右到左(RightLeft)
- `LR` 从左到右(LeftRight)
- `TD` 同 `TB`(TopDown)

```mermaid
graph TB
从上到下-->B
```

```mermaid
graph LR
从左到右-->B
```

```mermaid
graph BT
从下到上-->B
```

```mermaid
graph RL
从右到左-->B
```

### 基本图形

- `id + [文字描述]`矩形
- `id + (文字描述`)圆角矩形
- `id + >文字描述]`不对称的矩形
- `id + {文字描述}`菱形
- `id + ((文字描述))`圆形

```mermaid
graph TD
    id[带文本的矩形]
    id4(带文本的圆角矩形)
    id3>带文本的不对称的矩形]
    id1{带文本的菱形}
    id2((带文本的圆形))
```

### 节点之间的连接

- `A --> B` A 带箭头指向 B
- `A — B` A 不带箭头指向 B
- `A -.- B` A 用虚线指向 B
- `A -.->` B A 用带箭头的虚线指向 B
- `A ==>` B A 用加粗的箭头指向 B
- `A – 描述 — B` A 不带箭头指向 B 并在中间加上文字描述
- `A – 描述 --> B` A 带箭头指向 B 并在中间加上文字描述
- `A -. 描述 .-> B` A 用带箭头的虚线指向 B 并在中间加上文字描述
- `A == 描述 ==> B` A 用加粗的箭头指向 B 并在中间加上文字描述

```mermaid
graph LR
    A[A] --> B[B]
    A1[A] --- B1[B]
    A4[A] -.- B4[B]
    A5[A] -.-> B5[B]
    A7[A] ==> B7[B]
    A2[A] -- 描述 --- B2[B]
    A3[A] -- 描述 --> B3[B]
    A6[A] -. 描述 .-> B6[B]
    A8[A] == 描述 ==> B8[B]
```

### 绘制一个流程图,找出 A、 B、 C 三个数中最大的一个数

```bash
mermaid
graph LR
    start[开始] --> input[输入A,B,C]
    input --> conditionA{A是否大于B}
    conditionA -- YES --> conditionC{A是否大于C}
    conditionA -- NO --> conditionB{B是否大于C}
    conditionC -- YES --> printA[输出A]
    conditionC -- NO --> printC[输出C]
    conditionB -- YES --> printB[输出B]
    conditionB -- NO --> printC[输出C]
    printA --> stop[结束]
    printC --> stop
    printB --> stop
```

```mermaid
graph TB
    start[开始] --> input[输入A,B,C]
    input --> conditionA{A是否大于B}
    conditionA -- YES --> conditionC{A是否大于C}
    conditionA -- NO --> conditionB{B是否大于C}
    conditionC -- YES --> printA[输出A]
    conditionC -- NO --> printC[输出C]
    conditionB -- YES --> printB[输出B]
    conditionB -- NO --> printC[输出C]
    printA --> stop[结束]
    printC --> stop
    printB --> stop
```
