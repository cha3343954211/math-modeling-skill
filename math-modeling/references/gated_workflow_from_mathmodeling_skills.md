# MathModeling-skills 门控工作流融合指南

来源参考：KyrieZhang329/MathModeling-skills（MIT）。本文件把其“26 个单一职责 skill + G1–G6 门控 + 可追溯产物”的思想，融合为 Hermes `math-modeling` 使用时的执行规范。

## 核心理念

数模竞赛常见失败点不是“完全不会模型”，而是流程漂移：

- 题没读清就建模；
- 没有 baseline 就宣称模型更优；
- 方法没用真实数据验证就进入大代码；
- bug 修复后论文数字跟结果文件不一致；
- 图表和论文结论找不到来源 artifact；
- 审核只靠口头“没问题”，没有落盘记录。

因此，执行数学建模任务时应遵循：**先解析 → 再分类 → 再候选方法 → 小 PoC 验证 → 正式代码 → 结果冻结 → 论文写作 → 独立审计**。

## yushui2022/MathModel-Skill 补强：S0–S8 双门禁工作流

2026-05 进一步研究 `yushui2022/MathModel-Skill`（快照 `95f39b8 Harden MathModel workflow gates`）后，将其 Agent-native 流程融合为 Hermes 数学建模的补强规则。详细研究见 `references/yushui2022-mathmodel-skill-research-2026-05.md`。

### S0 输入资产预检（新增，开工第一步）

正式建模前先检查题面与附件健康状态；失败时停止，不要先凑草稿。

必查项：

- 题目目录/`problem_files/`/用户指定附件目录是否存在且非空；
- 是否有可解析题面（PDF/DOCX/TXT/MD，`.doc` 通常需转换）；
- Excel/CSV 是否能打开，是否损坏或编码异常；
- 文件名含 `result`、`结果`、`submit`、`提交` 的表格是否疑似**结果模板**；
- 是否存在旧 `final_paper`、旧图表、旧 frozen snapshot，避免误用陈旧产物。

附件性质必须分类：

| 类型 | 处理方式 |
|---|---|
| 原始数据 | 读取字段、单位、口径和样本粒度，生成清洗与建模代码 |
| 结果模板 | 只作为输出格式参考，不能当输入数据，更不能支撑结论 |
| 说明文档 | 提取约束、公式、参数和格式要求 |
| 参考材料 | 提取背景、规则、定义和可引用信息 |

### 结构化契约层（推荐新增）

在 `支撑材料/contracts/` 或项目 `paper_output/` 中维护结构化交接单：

| Contract | 作用 |
|---|---|
| `problem_analysis.json` | 题意、子问题、任务类型、附件画像 |
| `model_route.json` | 每问模型路线、baseline、验证计划、图表证据和章节落点 |
| `rubric_alignment.json` | 评分点 → 证据形式 → 论文位置 |
| `data_plan.json` | 数据文件、字段画像、清洗任务与子问题链接 |
| `visualization_plan.json` | 图表计划、图题、用途、候选字段和输出路径 |
| `figure_index.json` | 论文图表索引和正文引用检查依据 |
| `model_results.json` | 每问模型输出、参数、方案、预测值或排序结果 |
| `metrics.json` | RMSE、MAE、F1、综合得分、约束满足率等指标 |
| `conclusions.json` | 每问回扣题目的结构化结论 |
| `table_index.json` | 表格索引、表题、用途、关联子问题和路径 |
| `paper_outline.json` | 正式论文大纲和证据引用要求 |

契约规则：

- JSON 包含 `schema_version`、`generated_by`、`generated_at`；
- 子问题 ID 统一 `Q1/Q2/Q3`；
- 结果、指标、结论、表格必须带 `question_id`；
- 路径尽量用相对路径；
- JSON 只保存结构化交接信息，完整解释写 Markdown，完整正文写论文源文件。

### 证据门禁 + 格式门禁（新增命名）

在 G6 最终审计中显式拆成两道门：

1. **Evidence Gate（证据门禁）**：每问必须具备真实模型结果、评价指标、图表/表格证据、结构化结论和运行来源。正式结果建议记录 `execution_provenance`：`source_code_path`、`run_command`、`run_exit_code=0`、`output_artifacts`。
2. **Format Gate（格式门禁）**：正式论文必须通过页数/字数、标题层级、摘要数字、图表引用、公式解释、参考文献、附录和 PDF/Word 可打开性检查。

若任一结果仍标记为 `missing`、`needs_real_modeling`、`scaffold_result_needs_review`、`draft_contract`、`to_be_filled`、`template` 或 `draft`，不得称为最终稿。

---

## G1–G6 门控规则

| Gate | 名称 | 通过条件 | 失败回退 |
|---|---|---|---|
| G1 | PROBLEM_PARSED | 题目解析、子问题拆解、题型分类、数据清单存在 | 回到审题/分类 |
| G2 | METHOD_VALIDATED | 每个候选方法都有 ≤30 行 PoC，且在真实数据小切片上输出可行性数字 | 回到方法选择，淘汰不合适方法 |
| G3 | CODE_REVIEWED | 代码能跑；有审查记录，至少 5 项明确通过项或修复项 | 回到代码实现/审查 |
| G4 | RESULTS_FROZEN | 关键数字已写入 `frozen_numbers.json`，论文数字只能从这里取 | 解冻→改代码/结果→重冻结 |
| G5 | PAPER_SECTION_READY | 章节引用冻结数字；每个重要数值至少有 3 类讨论（敏感性/物理意义/baseline/跨题/不确定性等） | 回到材料包或论文段落 |
| G6 | AUDIT_LAYER_PASSED | 一致性、完整性、质量审计均通过 | 按最早 blocker 回退修复 |

### 三条硬规则

1. **没有最终方法详解，不写最终论文。** 不要基于早期候选方法池写定稿。
2. **没有最终结果分析，不交给论文手。** 代码跑完 ≠ 子问题完成。
3. **论文手只看材料包和冻结数字，不从零散输出里猜。**

## 推荐项目目录

此结构比旧版 `quest1/quest2` 更强调可追溯。如果用户已有旧结构，可保留旧结构；新项目优先采用下列结构。

```text
project/
├── planning/
│   ├── parse/                         # 题目解析
│   ├── classification/                # 子问题题型分类
│   ├── symbol_table.md                # 全局符号表
│   ├── model_assumptions.md           # 全局假设
│   ├── question_dependency.md         # 小问依赖
│   └── progress_dashboard.md          # 进度看板
├── methods/Qx/
│   ├── qx_method_candidates.md        # 候选方法池
│   ├── poc/                           # 每候选 ≤30 行 PoC
│   ├── qx_method_iteration_log.md     # 方法迭代/淘汰记录
│   ├── qx_final_method_explanation.md # 最终方法详解
│   └── qx_figure_table_plan.md        # 图表计划
├── code/Qx/
│   ├── *.py                           # Python 代码
│   └── reviews/qx_python_review.md    # 代码审查记录
├── code/matlab/Qx/                    # MATLAB/北太天元代码（如需）
├── results/Qx/
│   ├── experiments/roundN/
│   │   ├── figures/ tables/ metrics/ logs/
│   │   ├── run_summary.json
│   │   └── qx_experiment_report_roundN.md
│   └── reports/
│       ├── qx_final_result_analysis.md
│       ├── qx_solution_package_for_writer.md
│       ├── frozen_numbers.json
│       └── freeze_change_log.md
├── robustness/Qx/qx_robustness_report.md
├── paper/
│   ├── sections/
│   ├── figures/
│   ├── audits/
│   ├── refs.bib
│   └── main.tex
├── workspace/
│   ├── data_raw/                      # 原始数据只读
│   ├── data_clean/
│   └── archived/<Qx>/<method>_REJECTED_roundN/
└── scratch/                           # 临时探索，不进正式证据链
```

## 每小问最小交付链

每个子问题 Qx 不能把“代码跑通”当成完成。至少完成：

1. `methods/Qx/qx_method_candidates.md`：2–4 个候选方法，包含 baseline；每候选有 PoC。
2. `methods/Qx/poc/<candidate>_poc.py`：≤30 行，在真实数据小切片上跑出一个可行性数字。
3. `code/Qx/*.py` 或 `code/matlab/Qx/*.m`：正式实现。
4. `code/Qx/reviews/qx_<lang>_review.md`：代码审查，至少 5 项明确检查。
5. `results/Qx/experiments/roundN/run_summary.json`：运行摘要（输入、输出、指标、随机种子）。
6. `results/Qx/reports/qx_final_result_analysis.md`：最终结果分析。
7. `robustness/Qx/qx_robustness_report.md`：稳健性/敏感性/baseline 对比。
8. `methods/Qx/qx_final_method_explanation.md`：最终方法数学解释。
9. `results/Qx/reports/frozen_numbers.json`：论文可用数字冻结快照。
10. `results/Qx/reports/qx_solution_package_for_writer.md`：给论文手的材料包。
11. `paper/sections/qx.tex` 或 `.md`：只引用材料包和冻结数字。

## G2：候选方法 PoC 要求

每个候选方法必须先做“小而真的”可行性测试：

- 代码不超过 30 行；
- 使用真实清洗数据的小切片，不用纯合成数据；
- 输出一个具体数字或 verdict，例如：`RMSE=2.41`、`LP feasible, objective=123.4`、`CR=0.07`、`infeasible: demand exceeds supply`；
- 失败候选标记 `[REJECTED]`，并移到 `workspace/archived/<Qx>/<candidate>_REJECTED_poc/`；
- 候选池至少保留 1 个 `[CHOSEN]`，同时明确 baseline。

候选方法模板：

```markdown
### Candidate M1: [方法名] [CHOSEN | BACKUP | REJECTED]
- Math idea: ...
- Why it fits: ...
- Strengths: ...
- Weaknesses: ...
- Expected outputs: results / figures / metrics
- Evaluation criteria: ...
- Baseline? yes/no
- PoC script: `methods/Qx/poc/m1_poc.py`
- Feasibility number: ...
- Verdict: PASS / FAIL
```

## G4：冻结数字规范

论文里的关键数字必须来自 `frozen_numbers.json`，不要从散落的 CSV、日志、截图里临时抄。

建议结构：

```json
{
  "Q1": [
    {
      "claim_id": "q1_main_score_max",
      "value": 0.8732,
      "unit": "score",
      "description": "综合评价最高得分",
      "source_file": "results/Q1/experiments/round2/metrics/q1_scores.csv",
      "source_column": "score",
      "source_row": "方案A",
      "frozen_at": "2026-xx-xxTxx:xx:xx",
      "frozen_by": "solution-package-builder"
    }
  ]
}
```

如果代码、参数、清洗逻辑变动导致数字变化，必须：

1. 在 `freeze_change_log.md` 写明解冻原因；
2. 更新源代码/结果并重跑；
3. 重新生成 `frozen_numbers.json`；
4. 检查论文段落、图表、摘要中的对应数字。

禁止手工编辑 frozen snapshot 来“凑一致”。

## 独立审计层

最终提交前做三类独立检查：

### 1. 一致性审计（Consistency）

检查论文、代码、结果、图表、符号表是否一致：

- 论文每个数字是否能在 `frozen_numbers.json` 找到；
- 公式符号是否都在 `symbol_table.md` 定义；
- 图表数据源是否存在；
- 参数名、单位、约束方向是否前后一致；
- 修改代码后是否标记冻结数字 stale。

### 2. 完整性审计（Completeness）

检查所有子问题是否都有最小交付链：方法候选、PoC、代码审查、结果分析、稳健性、材料包、冻结数字、论文段落。

### 3. 质量审计（QA）

检查是否存在：

- 漏答子问题；
- 方法无法产出题目要求的输出；
- 没 baseline 却宣称更优；
- 没稳健性却宣称稳定；
- 图表无来源或装饰性图表冒充证据；
- 虚构数据、引用、实验或结论。

## 变更传播规则

修改任意 `code/Qx/`、`methods/Qx/`、`results/Qx/reports/`、`planning/` 文件后，必须搜索受影响内容：

```bash
grep -rn '<changed_identifier_or_number>' methods/ code/ results/ paper/ planning/
```

把可能过期的文件同步更新，或标记 `STALE` 并写明修复路线。若 `frozen_numbers.json` 已存在，而代码或结果被修改，要在 `freeze_change_log.md` 标记冻结快照过期。

## 图表证据分级

- Type 1：诊断图，只供调试，不进论文；
- Type 2：方法/候选对比图，可用于方法选择报告；
- Type 3：论文图，必须来源清楚、可读、支持明确结论；
- Type 4：附录图，补充但非核心。

每张论文图/表必须回答：

1. 支持什么 claim？
2. 来源 artifact 是什么？
3. 放在论文哪一节？

使用表格呈现精确数值，使用图形呈现趋势、关系、对比和稳健性。图表必须继续遵守用户偏好：`plt.savefig(..., dpi=300, bbox_inches='tight')` + `plt.close()`，不要 `plt.show()`。

## 回退路由

| 问题 | 回退到 |
|---|---|
| 题意理解错 | 题目解析 |
| 题型判断错 | 子问题分类 |
| 方法和数据不匹配 | 方法候选 / G2 PoC |
| 符号冲突 | 符号表 |
| 原始数据被改 | 恢复 `data_raw/`，重新清洗 |
| 代码输出和方法不一致 | 代码审查 |
| 结果不稳定 | 稳健性分析 |
| 图表没有证据 | 图表计划 |
| 论文数字找不到来源 | 冻结数字 / 材料包 |
| 引用不可验证 | 参考文献管理 |
| 多处阻塞 | 从最早 Gate 重走 |
