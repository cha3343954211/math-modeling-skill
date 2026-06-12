# Windows 中文路径下 LaTeX 编译与打包稳健模式

## 触发场景

数学建模项目根目录含中文、空格或特殊字符时，XeLaTeX 虽然能读取 `.tex`，但常见问题包括：

- `\graphicspath` 的相对图片路径解析失败，报 `Unable to load picture or PDF file`；
- 终端 `workdir` 因中文路径被工具阻塞；
- Python heredoc 中手写反斜杠替换路径时容易出现字符串转义错误；
- 论文已经生成了部分 PDF，但图片缺失或引用未稳定，不能直接交付。

这些问题不是模型或论文内容错误，而是 Windows + 中文路径 + LaTeX/终端路径解析的组合风险。

## 稳健编译流程

1. **原地保留正式产物结构**：所有正式代码、图表、结果、论文源文件仍放在用户指定题目目录的 `支撑材料/` 下。
2. **创建简单英文临时编译目录**，例如 `E:/hermes_tmp_a_paper/`。
3. **复制论文 `.tex` 与所有图片到临时目录**：
   - `paper.tex`
   - `figs/*.png`
4. **用 Python 改写临时 `.tex` 的 `\graphicspath`**，指向简单英文绝对路径：
   ```python
   from pathlib import Path
   p = Path('E:/hermes_tmp_a_paper/paper.tex')
   s = p.read_text(encoding='utf-8')
   s = s.replace(
       r'\graphicspath{{../quest1/figures/}{../quest2/figures/}{../quest3/figures/}{../quest4/figures/}}',
       r'\graphicspath{{E:/hermes_tmp_a_paper/figs/}}'
   )
   p.write_text(s, encoding='utf-8')
   ```
5. **在简单目录连续编译 3--4 遍**：
   ```bash
   cd /e/hermes_tmp_a_paper
   xelatex -interaction=nonstopmode -halt-on-error paper.tex
   xelatex -interaction=nonstopmode -halt-on-error paper.tex
   xelatex -interaction=nonstopmode -halt-on-error paper.tex
   xelatex -interaction=nonstopmode -halt-on-error paper.tex
   ```
6. **复制最终 PDF 回正式目录**：
   ```bash
   cp /e/hermes_tmp_a_paper/paper.pdf '<PROJECT_PATH>/支撑材料/papper/论文.pdf'
   pdfinfo '<PROJECT_PATH>/支撑材料/papper/论文.pdf' | grep Pages
   ```
7. **只有最终 PDF 复制回正式目录后才打包/发送**。

## 打包核验模式

用 `Path.as_posix()` 生成 zip 内部路径，避免在 heredoc 中手写 `replace('\\','/')` 导致字符串转义错误：

```python
from pathlib import Path
import zipfile
root = Path('<PROJECT_PATH>/支撑材料')
zip_path = Path('<PROJECT_PATH>/论文与支撑材料.zip')
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in root.rglob('*'):
        if p.is_file():
            z.write(p, '支撑材料/' + p.relative_to(root).as_posix())

with zipfile.ZipFile(zip_path) as z:
    names = set(z.namelist())
    required = [
        '支撑材料/papper/论文.pdf',
        '支撑材料/papper/论文.tex',
        '支撑材料/code/main_modeling.py',
        '支撑材料/results/frozen_numbers.json',
        '支撑材料/tables/final_evaluation_results.csv',
        '支撑材料/readme.txt',
    ]
    for r in required:
        print(r, r in names)
```

## 质量门控补充

- LaTeX 编译日志中若出现 `Unable to load picture`，即使生成了部分 PDF，也视为 L3 不通过。
- 编译后必须用 `pdfinfo` 核验页数，数学建模正式论文正文仍按不少于 15 页要求执行。
- MiKTeX 的“未检查更新”提示属于环境提示，不等价于编译失败；以 exit code、缺图错误、未定义引用和 PDF 页数作为交付判断依据。
