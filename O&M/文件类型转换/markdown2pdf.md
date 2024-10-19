# markdown2pdf

## 一、字体配置

### 1. 安装 xetex 和常见中文字体

- **`texlive-xetex` 是 XeTeX 引擎**：这是一个基于 TeX 的现代排版引擎，主要特点是原生支持 Unicode 和 OpenType 字体，使得在 LaTeX 中处理多种语言和复杂的字体变得更加容易。与传统的 TeX 引擎（如 pdfTeX）不同，XeTeX 可以直接调用系统字体，无需手动下载或安装额外的字体包。

- **`latex-cjk-all` CJK 字符集支持**：`latex-cjk-all` 是一个包含了对 CJK（Chinese, Japanese, Korean）字符处理的完整 LaTeX 包，它提供了对这三种东亚文字的排版支持。CJK 字符集通常对排版有特殊要求，这个包能处理好这些细节问题。

```bash
apt install texlive-xetex 
apt install latex-cjk-all
# apt install fonts-noto-cjk fonts-noto-cjk-extra
```

### 2. 从 Windows 向 Linux 迁移 ttf 字体文件

>  Windows的字体文件位于 `C:\Windows\Fonts`

> Linux的字体文件位于 `/usr/share/fonts`

- 执行以下指令创建新路径

```bash
mkdir /usr/share/fontsChinese/song/
```

- 执行以下指令更新并查询

```bash
# 更新
fc-cache
# 查看
fc-list  | grep 宋
```

### 3. 脚本

- `-V` 指定变量名

`CJKmainfont` 指定中文字体， `CJKsansfont` 指定中文粗体？

```python
from pathlib import Path
import os

work_dir = Path.cwd()

export_pdf_dir = work_dir / 'pdf'
if not export_pdf_dir.exists():
    export_pdf_dir.mkdir()

for md_file in list(work_dir.glob('*.md')):
    md_file_name = md_file.name
    pdf_file_name = md_file_name.replace('.md', '.pdf')
    pdf_file = export_pdf_dir / pdf_file_name
    cmd = "pandoc '{}' -o '{}' --pdf-engine=xelatex -V 'CJKmainfont=STZhongsong' -V 'CJKsansfont=STZhongsong' --template=template.tex".format(md_file, pdf_file)
    os.system(cmd)
```

### 4. 模板

设置模板

```bash
\documentclass[12pt,UTF8,nofonts]{ctexart}
......
\setCJKmainfont{Noto Sans CJK SC}
\setCJKsansfont{Noto Sans CJK SC}
\setmainfont{Noto Sans CJK SC}
\setsansfont{Noto Sans CJK SC}
```

## 参考资料

[如何把 Markdown 文件批量转换为 PDF - 少数派](https://sspai.com/post/47110)
