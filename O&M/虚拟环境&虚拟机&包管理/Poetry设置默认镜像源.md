# Poetry 设置清华镜像源

- 安装 poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

- 配置国内源

```bash
poetry source add --priority=default mirrors https://pypi.tuna.tsinghua.edu.cn/simple/
```

```bash
poetry source add --priority=primary mirrors https://pypi.tuna.tsinghua.edu.cn/simple/
```

### Python type hints

- 参考资料

https://zhuanlan.zhihu.com/p/464979921
