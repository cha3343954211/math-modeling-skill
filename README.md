# Math Modeling Skill (数学建模人机协同全真攻坚系统)

一个专为 **数学建模竞赛（CUMCM 国赛 / MCM/ICM 美赛 / MathorCup / APMCM / 研赛 / 校赛）与学术建模** 打造的顶级 Agent Skill 包。

深度融合姜启源《数学模型》经典机理体系与历年国一/O奖获奖团队攻坚方法论，支持 **72h/96h 全生命周期攻坚** 与 **极简单步独立按需调用**。

---

## 🌟 核心升级与特性亮点

- 🏆 **72h/96h 真实竞赛全真生命周期**：严格还原赛场节奏（选题 $\to$ 检索 $\to$ 审计 $\to$ 求解 $\to$ 验证 $\to$ 论文 $\to$ 封箱）。
- ⚡ **模块化极简单步独立调用**：全流程解耦为 6 个独立规范文件（`stages/`），支持通过 `/topic`, `/search`, `/audit`, `/solve`, `/validate`, `/paper`, `/pack` 随时单步触发。
- 🤝 **人机协同分阶段审批门控 (CP0~CP5)**：拒绝 AI 黑盒盲跑，关键节点自动弹出【人机协同审批卡】，支持队长/人类选手确认、修改假设（`/revise`）、选定路线（`/select`）与微调参数（`/tune`）。
- 📖 **融入姜启源《数学模型》全书机理库**：内置 13 大专题数学模型公式推导手册与离散运筹技巧，配套 `math_modeling_utils.py` (v3.0) 工具库（AHP多算法、Shapley值、Leslie矩阵、相平面判据、吸收马氏链、EOQ与报童模型、DW检验与敏感度弹性）。
- 🔍 **全自动问题初步分析与专属参考文献库**：
  - 自动拆解子问题要素并绘制 **Mermaid 设问递进图**（`docs/problem_spec.md`）；
  - 自动检索权威高被引文献，批量下载 Open Access PDF 全文至 `docs/references/papers/`；
  - 自动生成 LaTeX `references.bib` 与包含方法对比矩阵、真实参数定界的《文献综述与数模启发报告》（`docs/literature_review.md`）。
- 📝 **专家评审偏好与获奖级排版铁律**：严格执行正文 18~25 页、第1页三段式灵魂摘要（占分 40%+）、第2页目录、正文从 1 标页码、标准三线表（booktabs）及每图每表 2~4 句学术机理解读。
- 🔒 **干净环境一键复跑与匿名合规封箱**：封箱前执行独立干净环境一键全量复跑验证，严防代码运行报错或数字与论文不一致，全工程扫描清除个人与学校信息。

---

## 📂 模块化目录结构

```text
math-modeling-skill/
├── README.md                              # 本说明文档
├── math-modeling/
│   ├── SKILL.md                          # 顶层调度与全局规则入口
│   ├── stages/                           # 6 大独立可编辑/可升级阶段规范
│   │   ├── 00_topic.md                   # Step 0: 破题、量化选题与立项决策 (0~6h)
│   │   ├── 00_search.md                  # 🔍: 学术文献检索、下载与综述生成
│   │   ├── 01_audit.md                   # Step 1: 自动化问题分析、数据审计与符号系统 (6~18h)
│   │   ├── 02_solve.md                   # Step 2: 多问递进建模与代码高效求解 (18~48h)
│   │   ├── 03_validate.md                # Step 3: 对照验证、参数敏感度弹性与数字冻结 (48~60h)
│   │   ├── 04_paper.md                   # Step 4: 灵魂摘要精雕、图表美化与 LaTeX 排版 (60~70h)
│   │   └── 05_pack.md                    # Step 5: 独立复现质检、匿名合规与材料打包 (70~72h)
│   ├── references/                       # 核心数学机理、竞赛策略与排版指南
│   │   ├── real_competition_workflow_72h.md # 72h/96h 竞赛全真攻坚指南与三角色协同协议
│   │   ├── human_in_the_loop_protocol.md    # 人机协同审批点规范 (CP0~CP5) 与指令集
│   │   ├── classic_math_models_handbook.md  # 《数学模型》全书 13 大专题机理推导手册
│   │   ├── programming_and_discrete_tricks.md # 运筹规划与离散建模技巧 (大M法/对偶价格/AHP)
│   │   ├── model_selection_guide.md         # 题型决策树与经典机理映射矩阵
│   │   ├── cumcm_c_problem_expert_handbook.md # 国赛C题专家评审精要与真题解法 (2020~2025)
│   │   ├── supporting_materials_layout_v5_0.md # 支撑材料目录规范
│   ├── scripts/                          # 高性能工具箱
│   │   ├── quickstart.py                 # 交互式快速启动向导 (CLI)
│   │   ├── auto_problem_audit.py         # 自动化问题初步分析与文献归档
│   │   ├── openalex_scholar.py           # OpenAlex 学术文献检索、PDF下载与综述合成
│   │   ├── hybrid_scholar.py             # 双源并发检索与交叉验证
│   │   └── math_modeling_utils.py        # 数学建模核心算法工具库 (v3.0)
│   └── templates/                        # 竞赛 LaTeX 论文模板 (中文/英文) 与配置
```

---

## ⚡ 极简使用指南

### 1. 终端交互式启动向导 (Quickstart CLI)
无需记忆指令，直接在终端中运行可视化操作菜单：
```powershell
python math-modeling/scripts/quickstart.py
```

---

### 2. 五大场景化一键预设模式 (Scenario Presets)
向 AI 发送对应指令，自动调整求解深度与执行策略：

| 场景预设指令 | 适用场景 | 自动化策略与执行深度 |
| :--- | :--- | :--- |
| **`/mode contest`** | **72h/96h 正式竞赛** | **完整模式**：启动 CP0~CP5 全生命周期门控，严格执行数字冻结、1页摘要、18~25页论文、一键复跑与合规封箱。 |
| **`/mode solve_only`** | **闪电解题与代码求解** | **纯算模式**：快速做问题拆解、推导公式、编写 Python 求解代码并输出图表与数据表，跳过长篇论文撰写。 |
| **`/mode paper_only`** | **已有结果一键生成论文** | **写作模式**：读取已有代码、图表与数字，直接套用国赛/美赛 LaTeX 模板生成符合 18~25 页、1页三段式摘要的 PDF 论文。 |
| **`/mode review_only`** | **论文与代码质量体检** | **质检模式**：深度审查已有论文与代码（模型匹配度、数字一致性、可复现性、匿名合规排查）。 |
| **`/mode research`** | **前沿文献与参数定界** | **调研模式**：针对赛题自动检索 OpenAlex 权威文献，下载 OA PDF 全文，生成机理综述与参数基准表。 |

---

### 3. 模块化单步极简调用指令表（随时按需单步触发）
当您仅需完成某一特定环节时，可直接发送快捷指令（如 `/topic`, `/audit`, `/solve`, `/validate`, `/paper`, `/pack`），AI 将精准进入对应阶段执行：

| 快捷指令 | 阶段名 | 独立规范 | 核心输入 | 单步核心交付成果 |
| :--- | :--- | :--- | :--- | :--- |
| **`/topic`** | **1. 选题** | [`00_topic.md`](file:///f:/CodeworksF/skills/math-modeling/stages/00_topic.md) | 题目集 (A/B/C/D/E/F) | 4 维度量化评分矩阵、`topic_decision.md`、`competition_brief.md` |
| **`/search`** | **🔍 检索** | [`00_search.md`](file:///f:/CodeworksF/skills/math-modeling/stages/00_search.md) | 关键词 / 赛题方向 | 权威文献列表、真实物理参数范围、BibTeX 引用 |
| **`/audit`** | **2. 审计** | [`01_audit.md`](file:///f:/CodeworksF/skills/math-modeling/stages/01_audit.md) | 赛题文本与附件数据 | 问题规格书 `problem_spec.md`（含递进图）、`docs/references/` 专属文献库、符号表 `symbols.md`、`assumptions.md` |
| **`/solve`** | **3. 求解** | [`02_solve.md`](file:///f:/CodeworksF/skills/math-modeling/stages/02_solve.md) | 算法方案、清洗数据 | 完整公式推导、Python 求解代码、中间解表格与高分辨率图表 |
| **`/validate`** | **4. 验证** | [`03_validate.md`](file:///f:/CodeworksF/skills/math-modeling/stages/03_validate.md) | 求解代码与结果 | 改装效果对照表、参数弹性 $S = \frac{x}{y}\frac{dy}{dx}$、DW自相关检验、`frozen_numbers.json` |
| **`/paper`** | **5. 论文** | [`04_paper.md`](file:///f:/CodeworksF/skills/math-modeling/stages/04_paper.md) | 冻结数字、图表、结论 | 1 页三段式灵魂摘要、1 页目录、18~25 页正文的完整 LaTeX 源码与 PDF |
| **`/pack`** | **6. 封箱** | [`05_pack.md`](file:///f:/CodeworksF/skills/math-modeling/stages/05_pack.md) | 论文 PDF、全量代码 | 干净环境一键复跑报告、匿名合规扫描、规范支撑材料包与 MD5 码 |

### 4. 全局辅助与状态控制指令
- **`/status`**：查看当前竞赛进度时钟、各子问题完成状态与已锁定的数字清单。
- **`/resume`**：从最近一次中断或审批通过的 Checkpoint 节点无缝恢复继续。
- **`/export`**：一键整理并导出符合国赛/美赛提交规范的 `支撑材料/` 压缩包。

---

## 🤝 人机协同 5 大审批门控交互示例 (Checkpoints)

在每个阶段完成时，AI 会主动弹出结构化审批卡，人类选手可直接发送控制指令推进或修正：

```text
AI 输出示例：
--------------------------------------------------------------------------------
### 📋 [Checkpoint 1: 数据审计、符号系统与假设清单] 人机协同审批卡
1. 产出汇报：已生成 docs/problem_spec.md，已在 docs/references/ 归档 5 篇权威文献并生成综述
2. 递进主线：Q1(静态MILP) -> Q2(时变鲁棒优化) -> Q3(多目标TOPSIS)
3. 待决策：是否同意当前数据清洗规则与假设清单？
--------------------------------------------------------------------------------

人类选手回复指令：
- 回复 "/approve"                 --> 确认通过，直接进入 Stage 2 开始核心建模与代码求解
- 回复 "/revise assumption [内容]" --> 修改或放宽特定假设
- 回复 "/tune lambda=0.25"         --> 微调特定物理或算法超参数
- 回复 "/refine abstract [要点]"   --> 指定摘要精修侧重点
```

---

## 🛠️ 工具库与命令行使用指南

### 1. 自动化问题初步分析与文献归档
```powershell
python math-modeling/scripts/auto_problem_audit.py
```
> 全自动解析赛题要素、绘制设问递进图、检索 OpenAlex 学术数据库、下载开放获取 PDF 至 `docs/references/papers/`、自动生成 `docs/references/references.bib` 与 `docs/literature_review.md`。

### 2. 学术文献检索与综述生成
```powershell
# 搜索并生成文献综述与数模启发报告
python math-modeling/scripts/openalex_scholar.py --query "traffic flow shock wave modeling" --sort cited_by_count:desc --limit 5 --review docs/literature_review.md

# 自动下载所有 Open Access 论文 PDF
python math-modeling/scripts/openalex_scholar.py --query "battery thermal management" --field physics --year-start 2020 --download-dir data/papers/
```

### 3. 数学建模核心算法工具箱 (`math_modeling_utils.py`)
```python
from math_modeling_utils import AHPTool, GameTheoryTool, DynamicSystemTool, StatisticsTool

# 1. 层次分析法 (AHP) 特征值法与一致性检验
weights, cr, is_pass = AHPTool.eigenvalue_method(comparison_matrix)

# 2. 合作博弈 Shapley 利益分配值计算
shapley_values = GameTheoryTool.shapley_value(num_players=3, v_func=v_func)

# 3. 参数敏感度弹性分析 S = (x/y) * (dy/dx)
elasticity = StatisticsTool.parameter_elasticity(x_base=10.0, y_base=50.0, x_perturbed=11.0, y_perturbed=53.0)
```

---

## 🏆 获奖级论文排版铁律清单

1. **第 1 页为摘要页（严格限制 1 页）**：必须包含【背景定位 + 分问具体方法与精确冻结数字 + 稳健性结论】三段式结构，拒绝空话。
2. **第 2 页为目录页（严格限制 1 页）**：通过 `tocdepth=2` 显示至二级标题，通过字体行距微调强制压缩为 1 页。
3. **正文页码从 1 起标**：摘要与目录不标页码或标罗马数字，正文第 1 节起标阿拉伯数字 1。
4. **正文篇幅严格 18~25 页**：不足 18 页需扩充推导、验证与图表解读；超过 25 页必须精简。
5. **图表“三一法则”**：全篇使用标准三线表（booktabs），每图每表必须有编号与量纲，且正文中紧跟 **2~4 句深入的数学与现实机理解读**。

---

## 💻 运行环境依赖

- **Python 3.9+**：`numpy`, `pandas`, `scipy`, `scikit-learn`, `matplotlib`, `seaborn`, `statsmodels`, `pulp`, `networkx`
- **LaTeX 环境**：TeX Live / MiKTeX（支持 `xelatex` 编译中文论文）
