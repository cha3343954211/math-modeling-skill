# 支撑材料说明

## 项目信息
- **题目**：[填写题目名称]
- **日期**：[填写日期]
- **队伍**：[填写队伍名称或编号]

## 目录结构

```
支撑材料/
├── data/           # 数据区（raw/ 原始附件，processed/ 清洗数据）
├── code/           # 代码区（q1/ q2/ q3/ 按问题分目录）
├── output/         # 输出区（q1/ q2/ q3/ 图表结果，frozen_numbers.json 冻结数字）
├── paper/          # 论文区（论文.tex，论文.pdf，assets/ 图片资源）
├── refs/           # 参考资料（文献、模型契约、主张-证据映射）
├── audit/          # 审计报告（预检、代码审查、最终审计）
└── README.md       # 本文件
```

## 运行环境

### Python 版本
- Python 3.9+

### 主要依赖
```bash
pip install numpy pandas scipy scikit-learn matplotlib seaborn statsmodels
pip install pulp networkx xgboost
```

### LaTeX 编译
- 使用 XeLaTeX 编译（支持中文）
- 编译命令：`cd paper && xelatex 论文.tex`（运行3次）

## 运行入口

### 问题一
```bash
cd code/q1
python q1_main.py
```

### 问题二
```bash
cd code/q2
python q2_main.py
```

### 问题三
```bash
cd code/q3
python q3_main.py
```

## 主要结果

### 问题一
- [填写问题一的主要结果]
- [填写关键数值]

### 问题二
- [填写问题二的主要结果]
- [填写关键数值]

### 问题三
- [填写问题三的主要结果]
- [填写关键数值]

> 完整冻结数字见 `output/frozen_numbers.json`

## 复现顺序

1. **数据预处理**：运行 `code/q1/q1_main.py` 中的数据加载部分
2. **各问模型求解**：依次运行 `q1_main.py`、`q2_main.py`、`q3_main.py`
3. **生成图表/表格**：图表自动保存到 `output/qN/`
4. **编译论文**：
   ```bash
   cd paper
   xelatex 论文.tex
   xelatex 论文.tex
   xelatex 论文.tex
   ```
5. **打包与审计**：检查 `audit/final_audit.md`，打包支撑材料

## 注意事项

- 所有图表使用 `plt.savefig()` 保存，不使用 `plt.show()`
- 关键数字只从 `output/frozen_numbers.json` 读取
- 论文中的图表引用使用英文文件名
- 提交前检查匿名性，不包含个人信息
