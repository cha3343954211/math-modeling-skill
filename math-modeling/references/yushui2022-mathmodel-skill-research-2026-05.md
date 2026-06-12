# yushui2022/MathModel-Skill 深度研究与融合建议（2026-05）

来源仓库：`https://github.com/yushui2022/MathModel-Skill.git`  
本地研究快照：`95f39b8 Harden MathModel workflow gates`  
研究目的：提炼其 Agent-native 数学建模工作流中可迁移到 Hermes `math-modeling` skill 的流程、目录、证据契约和质量门禁。

## 1. 仓库定位

该仓库不是单一提示词，而是面向 Trae、Claude Code、Codex 的完整数学建模 skill 包。核心思想是：

```text
读题 → 拆题 → 模型路线 → 判断附件性质 → 生成/修改赛题专用代码
→ 运行代码 → 真实图表/表格/结果 → 证据门禁
→ 正式 outline → Agent 全局写作 → Word 排版 → 格式门禁 → 最终 QA
```

其最大价值不是具体算法，而是把“当前赛题产物”和“可复用 skill 能力”严格分离，并使用结构化 JSON 契约让不同阶段稳定交接。

## 2. 可迁移核心机制

### 2.1 启动预检 Preflight

正式流程第一步运行预检，检查：

- `problem_files/` 是否存在且非空；
- 是否有可解析题面（PDF/DOCX/TXT/MD 等）；
- `.doc` 等不可直接解析文件是否需要转换；
- `.xlsx` 是否损坏；
- `result*`、`结果*`、`submit*`、`提交*` 等是否疑似结果模板；
- 是否存在旧 `final_paper.docx` 等陈旧产物。

可迁移到 Hermes 的规则：

```text
开工前先做输入资产健康检查；失败时停止，不要先凑论文草稿。
```

### 2.2 附件性质判断

仓库明确要求把附件分为：

| 类型 | 处理方式 |
|---|---|
| 原始数据 | 读取字段、单位、样本粒度，生成清洗和建模代码 |
| 结果模板 | 只作为输出格式参考，不能当输入数据清洗 |
| 说明文档 | 提取约束、公式、参数和格式要求 |
| 参考材料 | 提取背景、规则、定义和可引用信息 |

重要护栏：官方 `result*.xlsx` 通常是结果模板，不得据此伪造建模结论。

### 2.3 当前赛题代码落点

当前赛题专用代码统一写入：

```text
paper_output/code/
├── data_processing/
├── visualization/
├── modeling/
└── qa/
```

Skill 包内 `scripts/` 只是样板和代码级提示词，不应被当前赛题代码污染。

对 Hermes 现有 `支撑材料/questN` 结构的融合方式：

- 用户已有指定题目目录时，仍优先使用 `支撑材料/` 标准结构；
- 可在 `支撑材料/` 下增加 `paper_output/` 或等价契约目录；
- 若继续使用 `quest1/quest2/quest3`，也要保持“当前赛题代码只在项目支撑材料内，不写回 skill 目录”的原则。

### 2.4 Workflow Contracts（结构化交接单）

仓库定义了一组 JSON 契约，不是平台标准，而是工作流稳定交接单：

| Contract | 作用 |
|---|---|
| `step1/problem_analysis.json` | 结构化题意分析、子问题、任务类型、附件画像 |
| `plan/model_route.json` | 每问模型路线、验证计划、图表证据和章节落点 |
| `plan/rubric_alignment.json` | 评分点与证据形式映射 |
| `plan/data_plan.json` | 数据文件、字段画像、清洗任务与子问题链接 |
| `plan/visualization_plan.json` | 图表计划、图题、用途、候选字段、输出路径 |
| `figure_index.json` | 图表索引和正文引用检查依据 |
| `results/model_results.json` | 每问模型输出、参数、方案、预测值或排序结果 |
| `results/metrics.json` | RMSE、MAE、F1、综合得分、约束满足率等指标 |
| `results/conclusions.json` | 每问回扣题目的结构化结论 |
| `tables/table_index.json` | 表格索引、表题、用途、关联子问题和路径 |
| `plan/paper_outline.json` | 正式论文大纲和证据引用要求 |

统一规则：

- JSON 必须包含 `schema_version`、`generated_by`、`generated_at`；
- 子问题 ID 统一 `Q1/Q2/Q3`；
- 结果、指标、结论、表格必须能追溯到 `question_id`；
- 路径尽量用相对路径；
- JSON 只保存结构化交接信息，不保存完整论文正文。

### 2.5 证据门禁 Evidence Gate

正式成稿前必须检查每个子问题是否具备：

- 真实模型结果；
- 评价指标；
- 图表或表格证据；
- 结构化结论；
- 任务追踪；
- official 模式下还要有 `execution_provenance`：`source_code_path`、`run_command`、`run_exit_code=0`、`output_artifacts`。

若结果状态仍是 `missing`、`needs_real_modeling`、`scaffold_result_needs_review`、`draft_contract`、`to_be_filled`、`template`、`draft`，不得称为最终稿。

### 2.6 正式论文门禁 Format Gate

证据门禁通过后再进入正式成稿。正式稿要求：

- 标题编号采用 `1 / 1.1 / 1.1.1`；
- 正文目标 `18000–25000` 中文字；
- 摘要 `800–1200` 字并按子问题展开；
- 第 5 章每个问题至少包含：建模思路、变量定义与公式推导、求解算法、结果分析、模型检验或灵敏度分析；
- 每张图表必须先正文引用、再插入、再解释；
- 公式必须先定义变量，后解释公式含义和用途；
- 算法必须写清输入、状态变量、步骤、停止条件和输出；
- 格式门禁失败时，Word 只能称为草稿。

### 2.7 Quickstart 定位

仓库强调 quickstart 仅用于安装验证或 smoke test，不代表正式比赛论文质量。其草稿不应覆盖正式 `final_paper.docx`。

迁移规则：

```text
如果用户要求正式建模，不要先跑 quickstart；如果用户只是验证安装，必须明确输出是验证草稿。
```

## 3. 与 Hermes 现有 math-modeling skill 的差距与融合方式

现有 Hermes skill 已经具备 G1–G6、三层质量门控、冻结数字、支撑材料目录和论文页数门槛。yushui2022 仓库可补强四点：

1. **输入资产预检**：把开工前的题面/附件健康检查显式化；
2. **附件类型判断**：防止把结果模板当原始数据；
3. **结构化契约层**：增加 `problem_analysis/model_route/data_plan/figure_index/results/metrics/conclusions/table_index/paper_outline` 等交接单概念；
4. **双门禁命名**：证据门禁 + 格式门禁，避免“代码跑了但论文不合格”或“Word 生成了但结果证据不足”。

## 4. Hermes 推荐融合版流程

```text
S0 输入资产预检
  - 检查题面、附件、损坏文件、结果模板、旧产物
S1 题意解析
  - 输出 problem_analysis.json / 题意对齐.md
S2 模型路线与评分闭环
  - 输出 model_route.json / rubric_alignment.json
S3 数据与图表计划
  - 输出 data_plan.json / visualization_plan.json / figure_index.json
S4 当前赛题专用代码
  - 在支撑材料或 paper_output/code/ 下写 data_processing / modeling / visualization / qa
S5 真实运行与结果证据
  - 输出 model_results.json / metrics.json / conclusions.json / table_index.json
  - 每个正式结果记录 execution_provenance
S6 证据门禁
  - 结果、指标、图表/表格、结论、来源均通过
S7 正式论文全局写作
  - 基于完整证据链写，不机械拼接草稿
S8 格式门禁与最终 QA
  - 页数/字数、标题层级、图表引用、参考文献、附录、数字一致性
```

## 5. 执行时的关键提醒

- 预检失败时停止；不要用“先写一版”绕过输入缺陷。
- 结果模板只能指导输出格式，不支撑结论。
- 任何写入论文的数字都必须来自冻结数字或结构化结果契约。
- `scripts/` 是样板，不是赛题答案；真实赛题要二次生成/修改代码并实际运行。
- 证据门禁和格式门禁都通过，才可称为最终稿。
- 若用户要求短报告/课程小作业，可降低字数要求，但必须显式说明“不是正式竞赛论文标准”。
