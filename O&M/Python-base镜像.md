# Python-base镜像

## 一、环境

### 1. python依赖

#### 1.1 requirement.txt

- 

```python
FastAPI
kubernetes
PyYAML
requests
pymysql
sqlalchemy
colorlog
minio
pyDes
```

- poetry 创建虚拟环境

```bash
# 安装poetry
curl -sSL https://install.python-poetry.org | python3 -
# 初始化项目
mkdir python-base
poetry init
# 添加依赖
poetry add fastapi kubernetes pyyaml requests pymysql sqlalchemy colorlog minio pyDes
```
