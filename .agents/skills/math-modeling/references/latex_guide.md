# LaTeX 编译指南（Windows）

## 环境检查

```bash
# 检查 XeLaTeX 是否可用
xelatex --version

# 检查中文字体
fc-list :lang=zh
```

推荐安装 TeX Live（完整版），包含 XeLaTeX、ctex、所有常用宏包。

## 中文支持编译

```latex
\documentclass[UTF8,a4paper,12pt]{ctexart}
\usepackage{geometry}
\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}
\usepackage{setspace}
\setstretch{1.35}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[C]{\small 论文题名缩写}
\fancyfoot[C]{\thepage}
\setlength{\headheight}{14pt}
\usepackage{amsmath,amssymb,booktabs,longtable,array,graphicx,float,caption,hyperref}
\captionsetup[table]{position=top}
\captionsetup[figure]{position=bottom}
```

编译命令：
```bash
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

## PDF 论文输出规范

### 推荐流程：MD草稿 → LaTeX → PDF

1. 先用 Markdown 写草稿（快速迭代）
2. 确认内容后转 LaTeX（精细排版）
3. 编译 PDF（检查页数、格式）

### 图片引用注意事项

- 图片格式优先 PDF/SVG（矢量），其次 PNG（位图，dpi≥300）
- 路径用相对路径：`\includegraphics{figures/chart.png}`
- 中文文件名可能导致编译失败，图片名用英文

## LaTeX 目录（TOC）控制技巧

```latex
% 控制目录显示深度
\setcounter{tocdepth}{2}  % 显示到二级标题

% 目录字号和间距
\renewcommand{\contentsname}{\centerline{目\quad 录}}
\renewcommand{\baselinestretch}{1.5}
```

若目录超过1页：
- 调整 `tocdepth` 为1（只显示一级标题）
- 缩小目录字号：`\small` 或 `\footnotesize`
- 减少段前段后间距

## 常见 LaTeX 问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 中文显示为方框 | 未用 XeLaTeX 或未加载 ctex | 编译用 `xelatex`，文档类用 `ctexart` |
| 公式被裁切 | 公式太长超出页边距 | 用 `aligned`/`split`/`multline` 拆行 |
| 图片不显示 | 路径错误或格式不支持 | 检查路径，用 `\graphicspath{{figures/}}` |
| 参考文献不显示 | 未运行 bibtex | 编译4次：xelatex→bibtex→xelatex→xelatex |
| 页码不连续 | 分节设置问题 | `\pagenumbering{arabic}` |
| 表格溢出页面 | 表格太宽 | 用 `resizebox` 或 `longtable` |
