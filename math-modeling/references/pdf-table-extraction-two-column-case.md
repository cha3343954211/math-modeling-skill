# PDF题目双栏表格数据提取案例：飞机侦察路径题

## 触发场景

数学建模题目的主要数据只在 PDF 题目中，表格采用左右双栏布局，例如同一行同时给出 A 类和 B 类目标：

```text
A: 编号 / 经度 / 纬度 / 海拔    B: 编号 / 经度 / 纬度 / 海拔
```

PyMuPDF 提取文本后，可能出现：
- A 类编号单独占一行；
- A 类经纬度在下一行、海拔再下一行；
- B 类编号+经纬度在同一行、B 类海拔在下一行；
- 换页处混入页码或页标题，导致全局数字流错位。

## 推荐做法

1. 先用 PyMuPDF 提取全文并保存：`extracted_text.txt`。
2. 不要直接把全文所有数字按固定 8 个一组切分；换页页码、题干数字、标题数字会破坏分组。
3. 按“行结构”解析：识别形如 `1.`、`2.` 的 A 类编号行，再读取后续非空行：
   - 第1个非空行：A 类经度、纬度；
   - 第2个非空行：A 类海拔；
   - 第3个非空行：B 类编号、经度、纬度；
   - 第4个非空行：B 类海拔。
4. 对解析结果做强校验：
   - 目标总数是否为 100；
   - A/B 是否各 50；
   - 编号 1--50 是否完整；
   - 缺失值是否为 0；
   - 首尾若干行是否与 PDF 原文一致。
5. 将解析脚本也放入支撑材料 `code/parse_pdf_data.py`，把 `extracted_text.txt` 放入 `data/`，保证数据来源可审计。

## 最小解析模式

```python
import re, csv
from pathlib import Path

lines = Path('extracted_text.txt').read_text(encoding='utf-8').splitlines()
records = []
i = 0
while i < len(lines):
    s = lines[i].strip()
    m = re.fullmatch(r'(\d+)\.', s)
    if not m:
        i += 1
        continue
    idx = int(m.group(1))
    non = []
    j = i + 1
    while j < len(lines) and len(non) < 4:
        st = lines[j].strip()
        if st and not st.startswith('====='):
            non.append((j, st))
        j += 1
    coords = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', non[0][1])]
    alt = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', non[1][1])]
    bline = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', non[2][1])]
    balt = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', non[3][1])]
    if len(coords) == 2 and len(alt) == 1 and len(bline) >= 3 and int(bline[0]) == idx and balt:
        records.append({'class':'A','id':idx,'name':f'A{idx:02d}','lon':coords[0],'lat':coords[1],'alt_m':alt[0]})
        records.append({'class':'B','id':idx,'name':f'B{idx:02d}','lon':bline[1],'lat':bline[2],'alt_m':balt[0]})
        i = non[3][0] + 1
    else:
        i += 1

missing = [k for k in range(1, 51)
           if not any(r['class']=='A' and r['id']==k for r in records)
           or not any(r['class']=='B' and r['id']==k for r in records)]
assert len(records) == 100 and not missing
```

## 论文与支撑材料写法

在论文“数据来源与预处理”中写清：数据由 PDF 表1识别得到，已转为 CSV；样本量、字段、缺失值、单位换算均已审计。支撑材料应包含：

```text
data/targets_from_pdf.csv
data/extracted_text.txt
code/parse_pdf_data.py
```

这样评阅者可以从 PDF 原文追溯到最终建模数据。