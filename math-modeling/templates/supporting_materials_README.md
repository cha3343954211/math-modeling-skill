# 数学建模支撑材料 README 模板

## 项目信息

- 题目：
- 竞赛/课程：
- 日期：
- 队伍编号：
- 说明：本支撑材料按 `data / references / contracts / questN / results / qa / papper / package` 结构组织。

## 目录结构

```text
支撑材料/
├── README.md
├── run.yaml
├── progress.jsonl
├── data/
│   ├── raw/
│   ├── processed/
│   └── data_audit.md
├── references/
├── contracts/
├── quest1/
│   ├── codes/
│   ├── figures/
│   ├── outputs/
│   ├── tables/
│   └── q1_solution_package_for_writer.md
├── quest2/
├── quest3/
├── results/
├── figures/
├── tables/
├── qa/
├── papper/
│   ├── 论文.md
│   ├── 论文.tex
│   ├── 论文.pdf
│   └── assets/
└── package/
```

## 运行环境

```bash
python --version
pip install numpy pandas scipy scikit-learn matplotlib seaborn statsmodels pulp networkx
```

LaTeX 编译：使用 XeLaTeX。

```bash
cd papper
xelatex -interaction=nonstopmode 论文.tex
xelatex -interaction=nonstopmode 论文.tex
xelatex -interaction=nonstopmode 论文.tex
```

## 运行入口

| 子问题 | 入口脚本 | 输出位置 |
|---|---|---|
| 问题一 | `python quest1/codes/q1_main.py` | `quest1/outputs/`, `quest1/figures/` |
| 问题二 | `python quest2/codes/q2_main.py` | `quest2/outputs/`, `quest2/figures/` |
| 问题三 | `python quest3/codes/q3_main.py` | `quest3/outputs/`, `quest3/figures/` |

## 主要结果

最终关键数字统一见：`results/frozen_numbers.json`。

### 问题一

- 方法：
- 关键结果：
- 证据文件：

### 问题二

- 方法：
- 关键结果：
- 证据文件：

### 问题三

- 方法：
- 关键结果：
- 证据文件：

## 证据链文件

| 文件 | 用途 |
|---|---|
| `contracts/problem_analysis.json` | 题意、子问题、输入输出、依赖关系 |
| `contracts/model_contract.md` | 候选模型、baseline、PoC、验证计划 |
| `contracts/claim_evidence_map.md` | 论文主张到证据文件的映射 |
| `results/frozen_numbers.json` | 摘要/正文关键数字唯一来源 |
| `qa/final_submission_audit.md` | 提交前最终审计 |

## 复现顺序

1. 检查 `data/raw/` 与 `qa/preflight_report.md`。
2. 运行数据预处理脚本，生成 `data/processed/`。
3. 依次运行 `quest1`、`quest2`、`quest3` 代码。
4. 汇总最终数字到 `results/frozen_numbers.json`。
5. 生成论文图表和表格。
6. 编译 `papper/论文.tex` 得到 `papper/论文.pdf`。
7. 完成 `qa/evidence_gate_report.md`、`qa/format_gate_report.md`、`qa/final_submission_audit.md`。
8. 打包 `package/支撑材料.zip` 并核验 manifest。

## 提交前核验

```text
□ PDF 存在且页数达标
□ 代码入口可运行
□ frozen_numbers.json 存在且论文数字一致
□ 图表中文无乱码
□ 参考文献已核验真实性
□ zip 不含 .git、__pycache__、旧 PDF、个人隐私或匿名性风险
```
