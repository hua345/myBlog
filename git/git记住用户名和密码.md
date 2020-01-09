# 记住用户名和密码

```bash
git config --global credential.helper store
# remote: HTTP Basic: Access denied
# 重新设置密码
git config --system --unset credential.helper
```
