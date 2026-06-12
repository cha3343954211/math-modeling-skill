# Windows环境下的数学建模注意事项

## 路径处理

### Python文件路径
在Windows的Git Bash/MSYS环境下，Python无法识别 `/e/` 格式的路径。

**错误写法**：
```python
plt.savefig('/e/数学建模文件夹/results/chart.png')
```

**正确写法**：
```python
plt.savefig('<MATH_MODELING_ARCHIVE>文件夹/results/chart.png')
```

### 终端路径
在终端（bash）中可以使用 `/e/` 格式：
```bash
cd /e/数学建模文件夹
ls -la
```

但在Python代码中必须使用 `E:/` 格式。

---

## 中文字体设置

### Matplotlib中文显示
```python
import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 或 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
```

### 可用中文字体
- SimHei（黑体）
- Microsoft YaHei（微软雅黑）
- SimSun（宋体）
- KaiTi（楷体）

---

## Excel文件读取

### 使用openpyxl引擎
```python
import pandas as pd

# .xlsx文件
df = pd.read_excel('data.xlsx', engine='openpyxl')

# .xls文件
df = pd.read_excel('data.xls', engine='xlrd')
```

### 常见问题
1. **编码问题**：确保Excel文件是UTF-8编码
2. **日期格式**：使用 `pd.to_datetime()` 转换
3. **缺失值**：检查 `df.isnull().sum()`

---

## 图表保存

### 直接保存不显示窗口
```python
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
# ... 绘图代码 ...
plt.savefig('output.png', dpi=300, bbox_inches='tight')
plt.close()  # 关闭图形，不显示窗口
```

### 输出目录创建
```python
import os
os.makedirs('results', exist_ok=True)
plt.savefig('results/chart.png', dpi=300, bbox_inches='tight')
```

---

## 常见错误及解决

### 1. FileNotFoundError
**原因**：路径格式错误
**解决**：使用 `E:/` 而非 `/e/`

### 2. Matplotlib中文乱码
**原因**：未设置中文字体
**解决**：设置 `plt.rcParams['font.sans-serif'] = ['SimHei']`

### 3. Excel读取编码错误
**原因**：文件编码不是UTF-8
**解决**：使用 `encoding='utf-8'` 或 `encoding='gbk'`

### 4. 图表显示不完整
**原因**：图形尺寸太小
**解决**：使用 `plt.figure(figsize=(12, 8))` 调整尺寸
