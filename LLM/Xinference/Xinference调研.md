# Xinference 调研

## 项目结构

- demo结构

```bash
.
├── mycmd.py
├── poetry.lock
├── pyproject.toml
├── README.md
└── xinference_demo
    ├── api
    │   └── restful_api.py
    ├── constants.py
    ├── core
    │   ├── resource.py
    │   ├── supervisor.py
    │   ├── utils.py
    │   └── worker.py
    ├── deploy
    │   ├── cmdline.py
    │   ├── local.py
    │   ├── utils.py
    │   └── worker.py
    ├── model
    │   └── llm
    │       └── llm_family.py
    └── utils.py
```
