# OCRmyPDF 部署使用指南

### 安装

- 安装

```bash
apt install ocrmypdf
```

- 查找可用语言包

```bash
apt-cache search tesseract-ocr
```

- 安装中文和英文语言包

```bash
apt-get install tesseract-ocr-eng tesseract-ocr-chi-sim
```

### 使用

- 添加可执行脚本

```bash
# vim /usr/local/bin/ocrmypdf-txt
#! /bin/bash
cd $(pwd)
ocrmypdf -l chi_sim --force-ocr --output-type=none --sidecar=- "$1" /dev/null
# chmod +x /usr/local/bin/ocrmypdf-txt
```

- 使用可执行脚本

```bash
ocrmypdf-txt input_file.pdf
```
