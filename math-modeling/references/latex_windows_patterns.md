# Windows LaTeX 编译模式

## 环境检查

```bash
where pdflatex
where xelatex
# 常见路径：
# <USER_HOME>\AppData\Local\Programs\MiKTeX\miktex\bin\x64\
# D:\texlive\2025\bin\windows\
```

## 中文支持编译

```bash
# 必须使用XeLaTeX（支持中文）
xelatex -interaction=nonstopmode 论文.tex

# 需要运行2-3次以解决交叉引用
xelatex -interaction=nonstopmode 论文.tex
xelatex -interaction=nonstopmode 论文.tex
```

## 图片路径问题

### 问题
LaTeX编译时报错 `Division by 0` 或 `File not found`，即使图片存在。

### 原因
相对路径包含子目录时，LaTeX可能无法正确解析。

### 解决方案
1. 将图片复制到.tex文件同目录
2. 使用本地路径（无子目录）
3. 或使用绝对路径

```bash
# 复制图片到论文目录
cp 支撑材料/图表/*.png 支撑材料/论文/

# LaTeX中使用本地路径
\includegraphics[width=0.85\textwidth]{问题1_区域AQI对比.png}
```

## 常见问题速查

| 问题 | 解决方案 |
|------|----------|
| 中文显示乱码 | 使用XeLaTeX而非PDFLaTeX |
| 图片找不到 | 复制图片到.tex同目录 |
| 交叉引用错误 | 运行2-3次XeLaTeX |
| 字体缺失 | 使用ctex宏包 |
| 页眉高度警告 | 添加 `\setlength{\headheight}{14pt}` |
| Division by 0 | 检查图片路径，使用本地路径 |

## 清理辅助文件

```bash
# Windows
del *.aux *.log *.out *.toc *.bbl *.blg

# Linux/Mac
rm -f *.aux *.log *.out *.toc *.bbl *.blg
```

## 编译脚本模板

```bash
#!/bin/bash
# 编译LaTeX论文（Windows Git Bash）

TEX_FILE="论文.tex"

# 编译3次
for i in {1..3}; do
    echo "第${i}次编译..."
    xelatex -interaction=nonstopmode "$TEX_FILE"
done

# 清理辅助文件
rm -f *.aux *.log *.out *.toc

echo "✅ 编译完成"
```
