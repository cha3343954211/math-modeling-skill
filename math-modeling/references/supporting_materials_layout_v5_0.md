# 支撑材料目录排放整理规范（v5.0 简化版）

本规范用于数学建模正式项目的文件落盘、目录命名、证据链组织与最终打包核验。v5.0 版本简化了目录结构，从原来的13个顶级目录精简为6个，更清晰易用。

## 1. 总原则

1. **题目目录原地优先**：用户给出题目目录时，该目录就是唯一项目根目录；正式产物必须写入 `题目目录/支撑材料/`，不得在同级新建 `*_work`、`output`、`solution` 后长期推进。
2. **支撑材料是唯一交付树**：代码、图表、结果、论文、参考资料、审计报告都归入 `支撑材料/`；原始题目附件可保留在题目根目录，同时复制或记录到 `支撑材料/data/`。
3. **按小问分区**：`code/qN/` 和 `output/qN/` 只放该小问的代码和输出；跨问共享的冻结数字、论文、参考资料、审计报告放在公共目录。
4. **临时目录可用但必须受控**：工具因中文路径、空格或 LaTeX 图片路径失败时，可使用系统临时英文目录中转；产物必须复制回标准目录。
5. **提交前按目录清单核验**：不能只看 PDF/zip 是否存在；必须检查必需文件路径、压缩包内容、匿名性、旧文件污染和可复现入口。

## 2. 简化标准目录树（6个顶级目录）

```text
题目目录/
├── 题目.pdf / 题目.docx / 附件*.xlsx       # 原始题面与附件，保持原貌
└── 支撑材料/
    ├── README.md                          # 运行说明、目录说明、主要结果
    │
    ├── data/                              # 数据区
    │   ├── raw/                           # 原始附件副本，不修改
    │   └── processed/                     # 清洗后数据、中间特征
    │
    ├── code/                              # 代码区
    │   ├── q1/                            # 问题一代码
    │   │   ├── q1_main.py                 # 主求解脚本
    │   │   ├── q1_poc_baseline.py         # PoC 验证
    │   │   └── q1_utils.py               # 辅助函数
    │   ├── q2/                            # 问题二代码
    │   └── q3/                            # 问题三代码
    │
    ├── output/                            # 输出区
    │   ├── q1/                            # 问题一输出
    │   │   ├── q1_figure_01_compare.png   # 图表
    │   │   ├── q1_table_01_results.csv    # 表格
    │   │   └── q1_model_output.json       # 模型输出
    │   ├── q2/
    │   ├── q3/
    │   └── frozen_numbers.json            # 全局冻结数字（摘要/正文只引用这里）
    │
    ├── paper/                             # 论文区
    │   ├── 论文.md                        # Markdown 草稿
    │   ├── 论文.tex                       # LaTeX 源文件
    │   ├── 论文.pdf                       # 最终 PDF
    │   └── assets/                        # 论文专用图片/排版资源
    │
    ├── refs/                              # 参考资料区
    │   ├── literature.md                  # 已核验可引用文献
    │   ├── model_contract.md              # 候选模型、baseline、PoC、验证计划
    │   ├── claim_evidence.md              # 论文主张→证据文件→冻结数字
    │   └── phase0_notes.md               # IMA/外部资源学习记录
    │
    └── audit/                             # 审计区
        ├── preflight.md                   # 题面、附件、旧产物预检
        ├── code_review.md                 # 代码审查
        ├── result_review.md               # 结果审查
        └── final_audit.md                 # 最终提交审计
```

## 3. 各目录职责边界

| 目录 | 放什么 | 不放什么 |
|---|---|---|
| `data/raw/` | 原始题面附件副本 | 清洗后数据、代码输出 |
| `data/processed/` | 清洗数据、特征表、统一口径数据 | 最终结论数字 |
| `code/qN/` | 第 N 问代码、PoC、求解脚本 | 其他小问代码 |
| `output/qN/` | 第 N 问图表、结果表、模型输出 | 摘要最终数字（应汇总到 `output/frozen_numbers.json`） |
| `output/` | 冻结数字、跨问汇总结果 | 未审计临时输出 |
| `paper/` | 论文草稿、LaTeX、PDF | 代码、原始数据 |
| `refs/` | 文献、模型契约、主张-证据映射、学习记录 | 大量中间图表、代码 |
| `audit/` | 审计、review、门禁报告 | 无记录的口头检查 |

## 4. 命名规范

### 4.1 目录命名

- 小问目录：`q1/`, `q2/`, `q3/`，题目超过三问则顺延 `q4/`。
- 代码目录统一为 `code/qN/`，输出为 `output/qN/`。
- 冻结数字放 `output/frozen_numbers.json`，不要散落在各脚本当前目录。

### 4.2 文件命名

| 类型 | 推荐命名 |
|---|---|
| 主代码 | `q1_main.py`, `q2_model.py`, `q3_optimization.py` |
| PoC | `q1_poc_baseline.py`, `q2_poc_candidate.py` |
| 图表 | `q1_figure_01_baseline_compare.png`, `q2_figure_02_sensitivity.png` |
| 表格 | `q1_table_01_final_results.csv`, `q2_table_02_ranking.csv` |
| 审计 | `preflight.md`, `code_review.md`, `final_audit.md` |

中文图题可写在论文 caption 中；文件名建议使用英文/数字/下划线，避免 `/`、`%`、`:`、空格和过长中文路径导致脚本或 LaTeX 失败。

## 5. 开工时必须创建的最小目录

正式建模任务开始后，先创建以下最小结构再推进：

```text
支撑材料/
├── README.md
├── data/raw/
├── data/processed/
├── code/q1/
├── code/q2/
├── code/q3/
├── output/q1/
├── output/q2/
├── output/q3/
├── paper/assets/
├── refs/
└── audit/
```

如果题目只有 1--2 问，可只创建需要的 `code/qN/` 和 `output/qN/`；如果尚未确定小问数量，可先建 `q1` 到 `q3`。

## 6. 阶段产物落盘规则

| 阶段 | 必须落盘到哪里 |
|---|---|
| S0 预检 | `audit/preflight.md`, `data/raw/` |
| G1 审题 | `refs/model_contract.md` |
| Phase 0 学习 | `refs/phase0_notes.md` |
| 文献检索 | `refs/literature.md` |
| G2 方法选择/PoC | `refs/model_contract.md`, `code/qN/*poc*.py`, `output/qN/` |
| G3 正式求解 | `code/qN/`, `output/qN/`, `audit/code_review.md` |
| G4 结果冻结 | `output/frozen_numbers.json`, `refs/claim_evidence.md` |
| G5 论文写作 | `refs/claim_evidence.md`, `paper/论文.md`, `paper/论文.tex` |
| G6/G7 审计提交 | `audit/final_audit.md` |

## 7. 最终打包核验清单

最终提交或发邮件前，至少核验：

```text
□ paper/论文.pdf 存在，页数达标，摘要和目录页数符合要求
□ paper/论文.tex 或论文源文件存在
□ output/frozen_numbers.json 存在，论文关键数字可追溯
□ code/q*/ 有可运行代码，README 中写明入口
□ output/q*/ 有关键图表，图中文字已抽查无乱码
□ refs/ 有文献和契约记录
□ audit/ 有最终审计报告
□ 最终 zip 的内容来自当前 `支撑材料/`，不是外部临时目录
□ zip 中不包含 `.git/`、`__pycache__/`、`.aux/.log/.toc`、旧 PDF、个人隐私、学校/姓名等匿名性风险
```

## 8. 压缩包 manifest 核验脚本模板

可在项目根目录或 `支撑材料/` 中运行：

```python
from pathlib import Path
import zipfile

root = Path('支撑材料')
zip_path = root / '支撑材料.zip'
required = [
    'README.md',
    'paper/论文.pdf',
    'paper/论文.tex',
    'output/frozen_numbers.json',
    'refs/claim_evidence.md',
    'audit/final_audit.md',
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
- 发现 `code/qN/` 混放其他小问代码：按小问拆分，更新 README 和运行入口。
- 发现最终数字散落在脚本日志：汇总到 `output/frozen_numbers.json`，并更新 `refs/claim_evidence.md`。
- 发现多个 PDF 难以判断最终版：只保留或明确标注最终版，旧版删除或移到临时目录。
- 发现中文路径导致 LaTeX/图片失败：使用英文临时目录编译，但 PDF、tex 必须回写 `paper/`，并在 `audit/final_audit.md` 记录。

## 10. README 最小内容

`README.md` 至少包含：

```markdown
# 支撑材料说明

## 项目信息
- 题目：
- 日期：
- 负责人/队伍：匿名版可留空或写队伍编号

## 目录结构
说明 data/code/output/paper/refs/audit 的用途。

## 运行环境
Python 版本、主要依赖、LaTeX 编译方式。

## 运行入口
- 问题一：`python code/q1/q1_main.py`
- 问题二：`python code/q2/q2_main.py`
- 问题三：`python code/q3/q3_main.py`

## 主要结果
列出每问最终答案，并说明完整数字见 `output/frozen_numbers.json`。

## 复现顺序
1. 数据预处理
2. 各问模型求解
3. 生成图表/表格
4. 编译论文
5. 打包与审计
```

## 11. 从 v4.8 迁移到 v5.0

如果已有旧结构项目，可按以下映射迁移：

| v4.8 旧路径 | v5.0 新路径 |
|---|---|
| `questN/codes/` | `code/qN/` |
| `questN/figures/` | `output/qN/` |
| `questN/outputs/` | `output/qN/` |
| `questN/tables/` | `output/qN/` |
| `results/frozen_numbers.json` | `output/frozen_numbers.json` |
| `figures/` | `output/` (跨问图放对应 `output/qN/`) |
| `tables/` | `output/` (跨问表放对应 `output/qN/`) |
| `references/` | `refs/` |
| `contracts/` | `refs/` (契约文件合并) |
| `qa/` | `audit/` |
| `papper/` | `paper/` |
| `package/` | 删除（打包时临时创建） |
| `scratch/` | 删除（使用系统临时目录） |
