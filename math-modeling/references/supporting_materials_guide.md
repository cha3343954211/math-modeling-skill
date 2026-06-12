# 支撑材料组织规范

## 标准目录结构

```
项目目录/
├── 支撑材料/
│   ├── README.md           # 项目说明文档
│   ├── 数据/               # 原始数据和题目文件
│   │   ├── 附件1_XXX.xlsx
│   │   ├── 附件2_XXX.xlsx
│   │   └── 题目.docx
│   ├── 代码/               # Python代码
│   │   └── XXX_完整解答.py
│   ├── 图表/               # 可视化结果
│   │   ├── 问题1_XXX.png
│   │   ├── 问题2_XXX.png
│   │   └── 问题3_XXX.png
│   ├── contracts/          # 结构化交接单（推荐新增）
│   │   ├── problem_analysis.json      # 题意、子问题、附件画像
│   │   ├── model_route.json           # 每问模型路线、baseline、验证计划
│   │   ├── rubric_alignment.json      # 评分点→证据→论文位置
│   │   ├── data_plan.json             # 数据字段、清洗任务、子问题链接
│   │   ├── visualization_plan.json    # 图表计划、用途、输出路径
│   │   ├── figure_index.json          # 论文图表索引
│   │   ├── model_results.json         # 每问模型输出/参数/方案/预测
│   │   ├── metrics.json               # 误差、得分、约束满足率等指标
│   │   ├── conclusions.json           # 回扣题目的结构化结论
│   │   ├── table_index.json           # 论文表格索引
│   │   └── paper_outline.json         # 正式论文大纲与证据引用要求
│   ├── qa/                 # 门禁与审计报告（推荐新增）
│   │   ├── preflight_report.md        # 输入资产预检：题面/附件/模板/旧产物
│   │   ├── evidence_gate_report.md    # 证据门禁：结果/指标/图表/表格/结论
│   │   └── format_gate_report.md      # 格式门禁：页数/标题/引用/附录
│   └── 论文/               # 论文文件
│       ├── 论文.md
│       ├── 论文.tex
│       └── 论文.pdf
├── 附件1_XXX.xlsx          # 原始文件（保留）
├── 附件2_XXX.xlsx
└── 题目.docx
```

> 说明：`contracts/` 和 `qa/` 融合自 yushui2022/MathModel-Skill 的 Agent-native workflow。它们不是平台强制格式，而是为了让题意、模型路线、数据计划、真实结果、论文图表和最终正文之间可追溯。若项目已有 `paper_output/` 结构，也可把上述 JSON 放在 `paper_output/` 对应子目录；原则是“当前赛题产物留在项目目录，不写回 skill 目录”。

## README.md 模板

```markdown
# 支撑材料

## 项目信息
- **题目**：XXX
- **日期**：XXXX年XX月XX日

## 文件结构
[目录树]

## 运行说明
### 环境要求
pip install ...

### 运行代码
python XXX.py

### 编译论文
xelatex 论文.tex

## 主要结果
### 问题一
- 结果1
- 结果2

### 问题二
- 结果1
- 结果2
```

## 文件组织原则

1. **数据文件**：原始数据、题目文件、数据字典
2. **代码文件**：完整可运行的Python代码
3. **图表文件**：所有可视化结果，命名规范
4. **论文文件**：Markdown、LaTeX、PDF三种格式

## 命名规范

- 数据文件：保持原始命名
- 代码文件：`题目名称_完整解答.py`
- 图表文件：`问题N_图表描述.png`
- 论文文件：`论文.md`、`论文.tex`、`论文.pdf`
