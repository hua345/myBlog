# mac用户和用户组

```bash
# 查看当前用户
➜  ~ whoami
chenjianhua
# 查看当前用户所属组
➜  ~ groups
# 查看指定用户所属组
➜  ~ groups chenjianhua
staff everyone localaccounts _appserverusr admin _appserveradm _lpadmin _appstore _lpoperator _developer _analyticsusers com.apple.access_ftp com.apple.access_screensharing com.apple.access_ssh com.apple.access_remote_ae com.apple.sharepoint.group.1
```

## staff、 wheel用户组的区别

`wheel` 组的概念继承自 `UNIX`。当服务器需要进行一些日常系统管理员无法执行的高级维护时，往往就要用到 `root` 权限

`wheel` 是一个特殊的用户组，该组的用户可以使用 su 切换到 root

`staff` 组是所有普通用户的集合。
