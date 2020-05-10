## 什么是自动装箱拆箱

装箱就是自动将基本数据类型转换为包装器类型。
拆箱就是自动将包装器类型转换为基本数据类型。

```java
public class IntTest {
    public static void main(String[] args) {
        //自动装箱
        Integer num = 99;
        //自动拆箱
        int numInt = num;

        Integer num2 = 200;
        Integer num3 = 200;
        System.out.println(num2 == num3);
    }
}
```

这个过程是自动执行的，那么我们需要看看它的执行过程：

```java
// 编译成字节码
javac IntTest.java
// javap可以查看java编译器生成的字节码
javap -c IntTest.class
```

```java
  public static void main(java.lang.String[]);
    Code:
       0: bipush        99
       2: invokestatic  #2                  // Method java/lang/Integer.valueOf:(I)Ljava/lang/Integer;
       5: astore_1
       6: aload_1
       7: invokevirtual #3                  // Method java/lang/Integer.intValue:()I
      10: istore_2
      11: sipush        200
      14: invokestatic  #2                  // Method java/lang/Integer.valueOf:(I)Ljava/lang/Integer;
      17: astore_3
      18: sipush        200
      21: invokestatic  #2                  // Method java/lang/Integer.valueOf:(I)Ljava/lang/Integer;
      24: astore        4
      26: getstatic     #4                  // Field java/lang/System.out:Ljava/io/PrintStream;
      29: aload_3
      30: aload         4
      32: if_acmpne     39
      35: iconst_1
      36: goto          40
      39: iconst_0
      40: invokevirtual #5                  // Method java/io/PrintStream.println:(Z)V
      43: return
```

```java
//自动装箱
Integer num = 99;
// 执行上面那句代码的时候，系统为我们执行了:
Integer num = Integer.valueOf(99);
//自动拆箱
int numInt = num;
// 执行上面那句代码的时候，系统为我们执行了:
int numInt = num.intValue();
```

我们看下 Integer 的源码

```java
private static class IntegerCache {
    static final int low = -128;
    static final int high;
    static final Integer[] cache;

    private IntegerCache() {
    }
    static {
        int h = 127;
        high = h;
        cache = new Integer[high - -128 + 1];
        i = -128;
        for(int k = 0; k < cache.length; ++k) {
            cache[k] = new Integer(i++);
        }
    }
}

public static Integer valueOf(int i) {
    return i >= -128 && i <= Integer.IntegerCache.high ? Integer.IntegerCache.cache[i + 128] : new Integer(i);
}
```

如果数字`-128~127`，返回静态类`Integer.IntegerCache`中的`Integer`;
但如果不在这个范围内，会new一个`Integer`对象.

```java
public boolean equals(Object obj) {
    if (obj instanceof Integer) {
        return this.value == (Integer)obj;
    } else {
        return false;
    }
}

// 构造函数
public Integer(int value) {
    this.value = value;
}

public int intValue() {
    return this.value;
}
```

所以Integer比较的时候应该使用`equals`或者`intValue`
