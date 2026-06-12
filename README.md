# Math Modeling Skill for Hermes Agent

一个**特别基于 Hermes Agent 智能体使用**的数学建模竞赛 Skill 包，面向 CUMCM / MCM / ICM / MathorCup / 校赛 / 课程建模项目，覆盖从审题、资料检索、模型选择、代码求解、图表生成、结果冻结、论文写作到最终审计打包的完整流程。

本仓库适合两类使用者：

1. **Hermes Agent 用户**：把本 skill 安装到 Hermes 的 skills 目录，让智能体在数学建模任务中自动遵循本流程。
2. **数学建模参赛者/学习者**：直接阅读 `SKILL.md`、`references/`、`templates/` 和 `scripts/`，作为建模流程、论文写作和支撑材料组织指南。

> 公开版说明：本导出包已清理个人路径、私人邮箱、私有知识库 ID、自动使用外部私有 AI 服务的规则以及本机缓存文件。

## 1. 项目特点

- **Hermes Agent 原生 Skill 格式**：以 `SKILL.md` 为主入口，配合 `references/`、`templates/`、`scripts/` 使用。
- **全流程门控**：采用 S0 + G1-G7 工作流，要求每个关键阶段都有落盘证据。
- **获奖级论文导向**：强调摘要数字、小问闭环、baseline、验证、稳健性、Claim-Evidence 映射。
- **代码与论文一致性**：所有关键数字必须来自冻结结果文件，避免论文数字和代码输出不一致。
- **支撑材料标准化**：统一 `支撑材料/` 目录结构，便于复现、提交和审计。
- **可选学术检索工具**：提供 OpenAlex / AnySearch 检索脚本模板，用于查找可核验文献。
- **公开发布友好**：不包含个人凭据、个人账号、私有知识库 ID 或自动调用私人 AI 服务的规则。

## 2. 目录结构

> 测试结果仓库：完整数学建模国赛应用测试结果已单独放在 [`math-m-skill-test`](https://github.com/cha3343954211/math-m-skill-test) 仓库中。本仓库仅保留 skill 主包、模板、脚本和说明文档。

```text
math-modeling-skill/
├── README.md
├── LICENSE
├── .gitignore
├── math-modeling/
│   ├── SKILL.md                 # Hermes Skill 主文件
│   ├── references/              # 工作流、质量门控、案例笔记、踩坑记录
│   ├── templates/               # LaTeX、支撑材料 README、论文检索配置模板
│   └── scripts/                 # 学术检索与数学建模工具脚本
└── math-modeling-skill-public.zip
```

## 3. 安装到 Hermes Agent

### 3.1 用户本地安装（推荐）

把 `math-modeling/` 复制到 Hermes 用户 skills 目录：

```bash
# Windows Git Bash / Linux / macOS 类 Unix shell
mkdir -p "$HOME/.hermes/skills/research"
cp -r math-modeling "$HOME/.hermes/skills/research/math-modeling"
```

然后重启 Hermes Agent 会话。之后当用户提出数学建模相关任务时，Hermes 会根据 skill 触发条件自动加载；也可以在提示词中明确要求：

```text
请加载 math-modeling skill，完整求解这个数学建模题。
```

### 3.2 放入 Hermes Agent 源码仓库

如果你维护 Hermes Agent 源码树，可放到：

```text
skills/research/math-modeling/SKILL.md
skills/research/math-modeling/references/
skills/research/math-modeling/templates/
skills/research/math-modeling/scripts/
```

### 3.3 验证安装

重启会话后向 Hermes 发送：

```text
列出可用 skills，确认 math-modeling 是否可用。
```

或者直接发起一个小任务：

```text
请使用 math-modeling skill，给我一个评价类数学建模题的建模流程。
```

## 4. Hermes 智能体推荐使用方式

本 skill 不是普通资料包，而是为 Hermes Agent 的“工具调用 + 文件落盘 + 代码执行 + 论文生成”工作方式设计。建议用户给 Hermes 的任务尽量包含以下信息：

```text
请使用 math-modeling skill 完成数学建模任务。
题目目录：<你的题目目录>
目标：完整求解 / 只做审题 / 只写论文 / 检查已有论文 / 生成支撑材料
要求：所有代码、图表、结果、论文都保存到题目目录下的 支撑材料/ 中。
```

### 示例 1：完整求解题目

```text
请使用 math-modeling skill 完整求解 E:/contest/problemC 这个数学建模题。
要求：
1. 原地创建 支撑材料/ 目录；
2. 先做题面和附件预检；
3. 按问题一、问题二、问题三顺序求解，不要割裂并发；
4. 代码、图表、输出和论文都保存到支撑材料；
5. 最终给出论文 PDF、LaTeX、冻结数字、运行说明和压缩包。
```

### 示例 2：只做审题与模型路线

```text
请使用 math-modeling skill 阅读这个题目，先不要写正式代码。
请输出：
1. 子问题拆解；
2. 题型分类；
3. 输入输出和约束；
4. baseline；
5. 候选主模型；
6. 风险点和验证方案。
```

### 示例 3：检查已有论文和支撑材料

```text
请使用 math-modeling skill 审计这个数学建模项目。
重点检查：
1. 摘要是否有每问关键数字；
2. 论文数字是否来自 frozen_numbers.json；
3. 图表是否有来源和正文解释；
4. 代码是否能复现；
5. 支撑材料 zip 是否完整。
```

## 5. 核心工作流

推荐遵循以下门控流程：

1. **S0 输入资产预检**
   - 检查题面、附件、结果模板是否可读。
   - 建立标准 `支撑材料/` 目录。
   - 记录 `qa/preflight_report.md`。

2. **G1 题目解析与题型分类**
   - 拆解每个子问题。
   - 判断预测、评价、优化、机理、图论、仿真等题型。
   - 形成 `contracts/problem_analysis.json`、`contracts/rubric_alignment.md`。

3. **G2 方法验证与 PoC**
   - 每个建模问题至少设置 baseline。
   - 候选模型先用真实数据小切片跑 ≤30 行 PoC。
   - 记录可行性数字和淘汰理由。

4. **G3 正式代码与结果生成**
   - 代码写入 `questN/codes/`。
   - 图表写入 `questN/figures/`。
   - 表格写入 `questN/tables/`。
   - 输出写入 `questN/outputs/`。

5. **G4 结果冻结与证据包**
   - 生成 `results/frozen_numbers.json`。
   - 每问生成 `qN_solution_package_for_writer.md`。
   - 关键图表建立 Figure Contract。

6. **G5 论文写作**
   - 论文只引用冻结数字、结果表、证据文件和可核验文献。
   - 每问按“题目要求 → 输入数据 → baseline → 主模型 → 求解 → 结果 → 验证 → 小结”闭环写作。

7. **G6/G7 审计与打包**
   - Evidence Gate：数字、图表、表格、结论都有证据。
   - Format Gate：页数、目录、标题、图表、引用、附录格式达标。
   - 最终打包 `package/支撑材料.zip` 并核验内容。

## 6. 支撑材料推荐结构

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
│   └── tables/
├── quest2/
│   ├── codes/
│   ├── figures/
│   ├── outputs/
│   └── tables/
├── quest3/
│   ├── codes/
│   ├── figures/
│   ├── outputs/
│   └── tables/
├── results/
├── figures/
├── tables/
├── qa/
├── papper/
│   └── assets/
├── package/
└── scratch/
```

## 7. 可选配置

### 7.1 Python 依赖

基础依赖：

```bash
pip install numpy pandas scipy scikit-learn matplotlib seaborn statsmodels pulp networkx requests pyyaml
```

按需安装：

```bash
pip install xgboost lightgbm ortools openpyxl python-docx
```

### 7.2 LaTeX 依赖

中文论文建议使用 XeLaTeX：

```bash
xelatex -interaction=nonstopmode 论文.tex
xelatex -interaction=nonstopmode 论文.tex
xelatex -interaction=nonstopmode 论文.tex
```

Windows 可安装 MiKTeX 或 TeX Live；Linux 可安装 `texlive-xetex` 与中文字体包。

### 7.3 学术检索

`scripts/hybrid_scholar.py` 支持 OpenAlex + AnySearch 检索。请使用你自己的联系邮箱：

```bash
python scripts/hybrid_scholar.py \
  --query "TOPSIS entropy weight evaluation mathematical modeling" \
  --email "your-email@example.com" \
  --limit 8 \
  --field mathematics \
  --json
```

AnySearch Key 不要写入仓库，可通过环境变量传入：

```bash
export ANYSEARCH_API_KEY="your_api_key"
```

### 7.4 个人知识库

本公开包不包含任何私有知识库 ID。若你有 IMA、Obsidian、Zotero 或其他个人资料库，可以把相关检索步骤作为可选 Phase 0；账号、token、knowledge base id 应放在本机环境变量或私有配置中。

## 8. 参考与融合的开源仓库

本 skill 的流程设计和部分规则参考、融合或受到以下公开项目启发。发布到 GitHub 时建议保留本节作为 attribution：

- `Lupynow/math-modeling-skills`：solver / paper 双流程、问题本质分类、文献证据、模型决策矩阵等思想。
- `zhnnky329/MathModeling-skills`：G1-G6 门控、PoC、review 落盘、冻结数字、三层审计等思想。
- `XiaoMaColtAI/math-modeling-skill`：建模手 / 编程手 / 论文手角色合同、Figure Contract、Claim-Evidence 映射等思想。
- `yushui2022/MathModel-Skill`：Preflight、附件分类、workflow contracts、Evidence Gate、Format Gate 等思想。
- `deafenken/auto-MM`：长流程竞赛状态管理、完整性门禁、匿名与提交包护栏等思想。
- `latexstudio/CUMCMThesis`：CUMCM LaTeX 模板与论文排版规范参考。
- `google/or-tools`、`Pyomo/pyomo`、`scipy/scipy`：运筹优化建模与求解工具参考。
- `Valdecy/pyDecision`、`anyoptimization/pymoo`：评价决策、多目标优化方法参考。
- `statsmodels/statsmodels`、`scikit-learn/scikit-learn`：统计建模、机器学习 baseline 与验证工具参考。

说明：本仓库是 Hermes Agent Skill 包和数学建模流程整理，不是上述仓库的直接镜像。若你复制了第三方仓库代码或模板，请按对应许可证补充 NOTICE 和 license 文件。

## 9. License

建议使用 MIT License；如果你引用或改写了第三方仓库内容，请按其许可证补充 NOTICE / attribution。
