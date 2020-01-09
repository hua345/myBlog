# 问题

```bash
ImportError: /lib64/libstdc++.so.6: version `CXXABI_1.3.8' not found

ImportError: /lib64/libm.so.6: version `GLIBC_2.23' not found
```

## 检查libstdc

```bash
➜  tensorflow ls /usr/lib64/libstdc*
/usr/lib64/libstdc++.so.6  /usr/lib64/libstdc++.so.6.0.19
```

## 检查libstdc中的内容

```bash
strings /usr/lib64/libstdc++.so.6 | grep CXXABI
CXXABI_1.3
CXXABI_1.3.1
CXXABI_1.3.2
CXXABI_1.3.3
CXXABI_1.3.4
CXXABI_1.3.5
CXXABI_1.3.6
CXXABI_1.3.7
CXXABI_TM_1
```

## [升级gcc](../gcc/Centos升级gcc.md)

```bash
strings /usr/lib64/libstdc++.so.6 | grep CXXABI
CXXABI_1.3
CXXABI_1.3.1
CXXABI_1.3.2
CXXABI_1.3.3
CXXABI_1.3.4
CXXABI_1.3.5
CXXABI_1.3.6
CXXABI_1.3.7
CXXABI_1.3.8
CXXABI_1.3.9
CXXABI_1.3.10
CXXABI_1.3.11
CXXABI_1.3.12
CXXABI_TM_1
CXXABI_FLOAT128
CXXABI_1.3
CXXABI_1.3.11
CXXABI_1.3.2
CXXABI_1.3.6
CXXABI_FLOAT128
CXXABI_1.3.12
CXXABI_1.3.9
CXXABI_1.3.1
CXXABI_1.3.5
CXXABI_1.3.8
CXXABI_1.3.4
CXXABI_TM_1
CXXABI_1.3.7
CXXABI_1.3.10
CXXABI_1.3.3
```
