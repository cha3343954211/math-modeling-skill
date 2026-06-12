# 支撑材料目录排放整理规范（v4.8.0）

本规范用于数学建模正式项目的文件落盘、目录命名、证据链组织与最终打包核验。目标是让每个题目目录从开工到提交都保持：**原地工作、分问清楚、证据可追溯、论文可编译、压缩包可核验**。

## 1. 总原则

1. **题目目录原地优先**：用户给出题目目录时，该目录就是唯一项目根目录；正式产物必须写入 `题目目录/支撑材料/`，不得在同级新建 `*_work`、`output`、`solution` 后长期推进。
2. **支撑材料是唯一交付树**：代码、图表、结果、论文、参考资料、审计记录、打包文件都归入 `支撑材料/`；原始题目附件可保留在题目根目录，同时复制或记录到 `支撑材料/data/`。
3. **按小问分区，按证据分层**：每个 `questN/` 只放该小问的代码、图表、输出、材料包；跨问共享的数据、冻结数字、论文、参考文献、QA 报告放在公共目录。
4. **临时目录可用但必须受控**：工具因中文路径、空格或 LaTeX 图片路径失败时，可使用 `支撑材料/scratch/` 或系统临时英文目录中转；产物必须复制回标准目录，最终打包前清理或标注 scratch。
5. **提交前按目录清单核验**：不能只看 PDF/zip 是否存在；必须检查必需文件路径、压缩包内容、匿名性、旧文件污染和可复现入口。

## 2. 推荐标准目录树

```text
题目目录/
├── 题目.pdf / 题目.docx / 附件*.xlsx       # 原始题面与附件，保持原貌
└── 支撑材料/
    ├── README.md                          # 运行说明、目录说明、主要结果
    ├── run.yaml                           # 竞赛状态、题目、时间、环境、入口
    ├── progress.jsonl                     # 关键动作日志：时间、阶段、产物、状态
    │
    ├── data/                              # 数据区
    │   ├── raw/                           # 原始附件副本，不修改
    │   ├── processed/                     # 清洗后数据、中间特征
    │   └── data_audit.md                  # 字段、缺失、异常、单位、口径
    │
    ├── references/                        # 外部资料与文献证据
    │   ├── phase0_ima_notes.md             # IMA/官方/论文/GitHub 学习记录
    │   ├── external_resource_notes.md      # 外部资源用途、风险、转化动作
    │   ├── literature_search_log.md        # Paper Search 检索日志
    │   ├── literature_candidates.json      # 候选文献原始结果
    │   ├── literature.md                   # 已核验可引用文献
    │   └── literature_rejected.md          # 未通过真实性门禁文献
    │
    ├── contracts/                         # 结构化契约/证据链
    │   ├── problem_analysis.json           # 题意、子问题、输入输出、依赖图
    │   ├── rubric_alignment.md             # 评分点→输出→证据→论文位置
    │   ├── model_contract.md               # 候选模型、baseline、PoC、验证计划
    │   ├── model_route.json                # 每问模型路线与淘汰记录
    │   ├── figure_contracts.md             # 关键图 Figure Contract
    │   ├── claim_evidence_map.md           # 论文主张→证据文件→冻结数字
    │   └── paper_outline.md                # 论文结构与证据引用计划
    │
    ├── quest1/                            # 问题一
    │   ├── codes/                         # 只放本问代码
    │   ├── figures/                       # 只放本问图表
    │   ├── outputs/                       # 本问结果表、模型输出、中间文件
    │   ├── tables/                        # 本问论文表格源文件
    │   └── q1_solution_package_for_writer.md
    ├── quest2/
    │   ├── codes/
    │   ├── figures/
    │   ├── outputs/
    │   ├── tables/
    │   └── q2_solution_package_for_writer.md
    ├── quest3/
    │   ├── codes/
    │   ├── figures/
    │   ├── outputs/
    │   ├── tables/
    │   └── q3_solution_package_for_writer.md
    │
    ├── results/                           # 全局最终结果
    │   ├── frozen_numbers.json             # 摘要/正文只允许引用这里的关键数字
    │   ├── final_results.csv               # 汇总结果表
    │   ├── metrics.json                    # 误差、排名稳定性、约束残差等
    │   └── conclusions.json                # 回答题目要求的结构化结论
    │
    ├── figures/                           # 跨问汇总图/论文主图索引
    ├── tables/                            # 跨问汇总表/最终表格
    │
    ├── qa/                                # 审计与门禁
    │   ├── preflight_report.md             # 题面、附件、旧产物、输出要求预检
    │   ├── code_review.md                  # 代码审查、约束方向、单位、随机种子
    │   ├── result_review.md                # 结果常识、baseline、稳健性
    │   ├── evidence_gate_report.md         # 证据门禁
    │   ├── format_gate_report.md           # 页数、图表、公式、引用、附录
    │   └── final_submission_audit.md       # 匿名性、zip、PDF、复现入口终审
    │
    ├── papper/                            # 沿用用户既有拼写：论文目录
    │   ├── 论文.md                         # Markdown 草稿
    │   ├── 论文.tex                        # LaTeX 源文件
    │   ├── 论文.pdf                        # 最终 PDF
    │   └── assets/                         # 论文专用图片/临时排版资源
    │
    ├── package/                           # 最终打包区
    │   ├── 支撑材料.zip
    │   └── zip_manifest.txt
    └── scratch/                           # 临时中转；提交前清理或说明
```

> 兼容说明：如果已有旧模板使用 `readme.txt`、`代码/`、`图表/`、`论文/`，可以保留，但正式新项目优先按上面目录组织。`papper/` 拼写虽然不规范，但已成为用户既有模板目录，继续沿用以避免破坏历史工作流。

## 3. 各目录职责边界

| 目录 | 放什么 | 不放什么 |
|---|---|---|
| `data/raw/` | 原始题面附件副本 | 清洗后数据、代码输出 |
| `data/processed/` | 清洗数据、特征表、统一口径数据 | 最终结论数字 |
| `references/` | 文献、外部资源、IMA 学习记录 | 未核验就进入论文的引用 |
| `contracts/` | 题意、模型、图表、主张-证据映射 | 大量中间图表、代码 |
| `questN/codes/` | 第 N 问代码、PoC、求解脚本 | 其他小问代码、全局打包脚本 |
| `questN/outputs/` | 第 N 问模型输出、中间结果 | 摘要最终数字（应汇总到 `results/frozen_numbers.json`） |
| `questN/figures/` | 第 N 问诊断图、对比图、论文候选图 | 跨问汇总图（放 `figures/`） |
| `results/` | 冻结数字、最终结果、指标、结构化结论 | 未审计临时输出 |
| `qa/` | 审计、review、门禁报告 | 无记录的口头检查 |
| `papper/` | 论文草稿、LaTeX、PDF | 代码、原始数据 |
| `package/` | 最终 zip 与 manifest | 未核验旧 zip |
| `scratch/` | 临时中转 | 长期正式产物 |

## 4. 命名规范

### 4.1 目录命名

- 小问目录：`quest1/`, `quest2/`, `quest3/`，题目超过三问则顺延 `quest4/`。
- 代码目录统一为 `codes/`，图表为 `figures/`，结果为 `outputs/`。
- 公共最终结果放 `results/`，不要散落在各脚本当前目录。

### 4.2 文件命名

| 类型 | 推荐命名 |
|---|---|
| 主代码 | `q1_main.py`, `q2_model.py`, `q3_optimization.py` |
| PoC | `q1_poc_baseline.py`, `q2_poc_candidate_model.py` |
| 图表 | `q1_figure_01_baseline_compare.png`, `q2_figure_02_sensitivity.png` |
| 表格 | `q1_table_01_final_results.csv`, `q2_table_02_ranking_stability.csv` |
| 材料包 | `q1_solution_package_for_writer.md` |
| 审计 | `preflight_report.md`, `final_submission_audit.md` |

中文图题可写在论文 caption 中；文件名建议使用英文/数字/下划线，避免 `/`、`%`、`:`、空格和过长中文路径导致脚本或 LaTeX 失败。

## 5. 开工时必须创建的最小目录

正式建模任务开始后，先创建以下最小结构再推进：

```text
支撑材料/
├── README.md
├── run.yaml
├── progress.jsonl
├── data/raw/
├── data/processed/
├── references/
├── contracts/
├── quest1/codes/ figures/ outputs/ tables/
├── quest2/codes/ figures/ outputs/ tables/
├── quest3/codes/ figures/ outputs/ tables/
├── results/
├── figures/
├── tables/
├── qa/
├── papper/assets/
├── package/
└── scratch/
```

如果题目只有 1--2 问，可只创建需要的 `questN/`；如果尚未确定小问数量，可先建 `quest1` 到 `quest3`。

## 6. 阶段产物落盘规则

| 阶段 | 必须落盘到哪里 |
|---|---|
| S0 预检 | `qa/preflight_report.md`, `data/raw/`, `run.yaml` |
| G1 审题 | `contracts/problem_analysis.json`, `contracts/rubric_alignment.md` |
| Phase 0 学习 | `references/phase0_ima_notes.md`, `references/external_resource_notes.md` |
| 文献检索 | `references/literature_search_log.md`, `literature_candidates.json`, `literature.md`, `literature_rejected.md` |
| G2 方法选择/PoC | `contracts/model_contract.md`, `contracts/model_route.json`, `questN/codes/*poc*.py`, `questN/outputs/` |
| G3 正式求解 | `questN/codes/`, `questN/outputs/`, `questN/figures/`, `qa/code_review.md` |
| G4 结果冻结 | `results/frozen_numbers.json`, `results/metrics.json`, `questN/qN_solution_package_for_writer.md` |
| G5 论文写作 | `contracts/claim_evidence_map.md`, `papper/论文.md`, `papper/论文.tex` |
| G6/G7 审计提交 | `qa/evidence_gate_report.md`, `qa/format_gate_report.md`, `qa/final_submission_audit.md`, `package/` |

## 7. 最终打包核验清单

最终提交或发邮件前，至少核验：

```text
□ papper/论文.pdf 存在，页数达标，摘要和目录页数符合要求
□ papper/论文.tex 或论文源文件存在
□ results/frozen_numbers.json 存在，论文关键数字可追溯
□ quest*/codes/ 有可运行代码，README 中写明入口
□ quest*/figures/ 或 figures/ 有关键图，图中文字已抽查无乱码
□ quest*/outputs/、tables/、results/ 有最终表格和模型输出
□ references/ 有资料学习与文献真实性记录
□ contracts/claim_evidence_map.md 将摘要/正文主张映射到证据
□ qa/ 有 preflight、code/result review、evidence/format/final audit
□ package/支撑材料.zip 的内容来自当前 `支撑材料/`，不是外部临时目录
□ zip 中不包含 `.git/`、`__pycache__/`、`.aux/.log/.toc`、旧 PDF、个人隐私、学校/姓名等匿名性风险
```

## 8. 压缩包 manifest 核验脚本模板

可在项目根目录或 `支撑材料/` 中运行：

```python
from pathlib import Path
import zipfile

root = Path('支撑材料')
zip_path = root / 'package' / '支撑材料.zip'
required = [
    'README.md',
    'run.yaml',
    'papper/论文.pdf',
    'papper/论文.tex',
    'results/frozen_numbers.json',
    'contracts/claim_evidence_map.md',
    'qa/final_submission_audit.md',
]

with zipfile.ZipFile(zip_path, 'r') as z:
    names = set(z.namelist())
    missing = [p for p in required if p not in names]
    banned = [n for n in names if any(x in n for x in ['.git/', '__pycache__/', '.DS_Store'])]

print('missing:', missing)
print('banned:', banned)
assert not missing, missing
assert not banned, banned
```

## 9. 回退与整理规则

- 发现正式产物落到外部临时目录：立即复制回 `支撑材料/` 对应位置，再继续推进。
- 发现 `questN/` 混放其他小问代码：按小问拆分，更新 README 和运行入口。
- 发现最终数字散落在脚本日志：汇总到 `results/frozen_numbers.json`，并更新 `claim_evidence_map.md`。
- 发现多个 PDF/zip 难以判断最终版：只保留或明确标注最终版，旧版移到 `scratch/archive_old_versions/` 或删除。
- 发现中文路径导致 LaTeX/图片失败：使用英文临时目录编译，但 PDF、tex、图片必须回写 `papper/` 和 `figures/`，并在 `qa/format_gate_report.md` 记录。

## 10. README 最小内容

`README.md` 至少包含：

```markdown
# 支撑材料说明

## 项目信息
- 题目：
- 日期：
- 负责人/队伍：匿名版可留空或写队伍编号

## 目录结构
说明 data/references/contracts/questN/results/qa/papper/package 的用途。

## 运行环境
Python 版本、主要依赖、LaTeX 编译方式。

## 运行入口
- 问题一：`python quest1/codes/q1_main.py`
- 问题二：`python quest2/codes/q2_main.py`
- 问题三：`python quest3/codes/q3_main.py`

## 主要结果
列出每问最终答案，并说明完整数字见 `results/frozen_numbers.json`。

## 复现顺序
1. 数据预处理
2. 各问模型求解
3. 生成图表/表格
4. 编译论文
5. 打包与审计
```
