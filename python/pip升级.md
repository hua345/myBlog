# pip升级

```bash
# 安装失败
pip install --upgrade pip
Consider using the `--user` option or check the permissions.
# 导致pip找不到
ModuleNotFoundError: No module named 'pip'
```

```bash
# 修复pip
python -m ensurepip
# pip升级
python -m pip install --upgrade pip
```