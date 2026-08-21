---
name: math-modeling
description: "数学建模竞赛全流程自动化：问题分析、模型构建、代码实现、论文写作、可视化。支持CUMCM/MCM/ICM等主流赛事。"
version: 6.4.0
author: MiMo V2.5 Pro + Capoo
metadata:
  hermes:
    tags: [mathematical-modeling, competition, optimization, statistics, machine-learning, paper-writing]
    related_skills: [data-science, software-development, creative]
---

# 数学建模 Skill v6.4

## 适用场景

当用户需要进行数学建模相关工作时加载此 Skill：
- **竞赛备赛**：CUMCM（国赛）、MCM/ICM（美赛）、MathorCup、APMCM等
- **课程作业**：数学建模课程、运筹学、统计分析
- **实际问题**：需要将实际问题转化为数学模型

---

## ⚡ 模式与单步调用路由 (Execution Modes & Modular Invocation)

本 Skill 支持**「72h/96h 竞赛全流程流转（Full Pipeline）」**与**「模块化单步独立调用（Standalone Step）」**两种工作方式：

### 1. 五大场景化一键预设模式 (Scenario Presets)
随时输入对应指令，AI 将按特定场景自动调整执行深度与策略：

| 场景预设指令 | 适用场景 | 自动化策略与执行深度 |
| :--- | :--- | :--- |
| **`/mode contest`** | **72h/96h 正式竞赛** | **完整模式**：启动 CP0~CP5 全生命周期门控，严格执行数字冻结、1页摘要、18~25页论文、一键复跑与合规封箱。 |
| **`/mode solve_only`** | **闪电解题与代码求解** | **纯算模式**：快速做问题拆解、推导公式、编写 Python 求解代码并输出图表与数据表，跳过长篇论文撰写。 |
| **`/mode paper_only`** | **已有结果一键生成论文** | **写作模式**：读取已有代码、图表与数字，直接套用国赛/美赛 LaTeX 模板生成符合 18~25 页、1页三段式摘要的 PDF 论文。 |
| **`/mode review_only`** | **论文与代码质量体检** | **质检模式**：深度审查已有论文与代码（模型匹配度、数字一致性、可复现性、匿名合规排查）。 |
| **`/mode research`** | **前沿文献与参数定界** | **调研模式**：针对赛题自动检索 OpenAlex 权威文献，下载 OA PDF 全文，生成机理综述与参数基准表。 |

---

### 2. 模块化单步极简调用指令表（随时按需单步触发）
当您仅需完成某一特定环节时，可直接发送快捷指令（如 `/topic`, `/audit`, `/solve`, `/validate`, `/paper`, `/pack`），AI 将精准进入对应阶段执行：

| 极简调用指令 | 步骤中文名 | 对应独立规范文件 | 核心输入 | 核心交付产出 |
| :--- | :--- | :--- | :--- | :--- |
| **`/topic`** | **1. 选题** | [`stages/00_topic.md`](file:///f:/CodeworksF/skills/math-modeling/stages/00_topic.md) | 赛题题目集 | 选题量化评分矩阵、`topic_decision.md`、`competition_brief.md` |
| **`/search`** | **🔍 检索** | [`stages/00_search.md`](file:///f:/CodeworksF/skills/math-modeling/stages/00_search.md) | 关键词/领域/赛题 | 权威学术文献列表、真实物理/行业参数范围、BibTeX 引用 |
| **`/audit`** | **2. 审计** | [`stages/01_audit.md`](file:///f:/CodeworksF/skills/math-modeling/stages/01_audit.md) | 赛题与原始附件 | 数据审计报告、全局统一符号表 `symbols.md`、`assumptions.md`、PoC代码 |
| **`/solve`** | **3. 求解** | [`stages/02_solve.md`](file:///f:/CodeworksF/skills/math-modeling/stages/02_solve.md) | 算法方案、清洗数据 | 完整数学公式推导、Python 求解代码、中间解表格与高分辨率图表 |
| **`/validate`** | **4. 验证** | [`stages/03_validate.md`](file:///f:/CodeworksF/skills/math-modeling/stages/03_validate.md) | 求解代码与结果 | 改装效果对照表、参数弹性 $S = \frac{x}{y}\frac{dy}{dx}$、DW检验、`frozen_numbers.json` |
| **`/paper`** | **5. 论文** | [`stages/04_paper.md`](file:///f:/CodeworksF/skills/math-modeling/stages/04_paper.md) | 冻结数字、图表、结论 | 1页三段式灵魂摘要、1页目录、18~25页正文的完整 LaTeX 源码与 PDF |
| **`/pack`** | **6. 封箱** | [`stages/05_pack.md`](file:///f:/CodeworksF/skills/math-modeling/stages/05_pack.md) | 论文 PDF、全量代码 | 独立环境一键复跑验证报告、匿名合规扫描、支撑材料包与 MD5 码 |

### 3. 全局辅助与状态控制指令
- **`/status`**：查看当前竞赛进度时钟、各子问题完成状态与已锁定的数字清单。
- **`/resume`**：从最近一次中断或审批通过的 Checkpoint 节点无缝恢复继续。
- **`/export`**：一键整理并导出符合国赛/美赛提交规范的 `支撑材料/` 压缩包。

---

## 🔴 真实竞赛高分硬规则（必须遵守）

1. **图表保存不弹窗**：所有 `plt.savefig(..., dpi=300, bbox_inches='tight')` + `plt.close()`，禁止 `plt.show()`
2. **中文路径兼容**：Python 代码中用 `E:/` 格式，不用 `/e/`；bash 中可用 `/e/`
3. **逐问迭代求解**：先完成 Q1 再进入 Q2，每问形成小闭环（Q1基准 $\to$ Q2现实改装 $\to$ Q3综合决策）
4. **拒绝编造数据/结果**：数字必须来自真实代码运行，禁止从截图/CSV临时抄凑
5. **中文字体**：matplotlib 设置 `plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']`
6. **工作区**：默认 `E:\HermesE`；项目目录优先用用户指定路径
7. **全局符号系统统一**：开赛必先建立 `symbols.md`，全篇公式符号必须严格一致，禁止前后矛盾
8. **不探查 SkillHub**：做数学建模时，外部资料探查用 GitHub/论文/官方文档
9. **论文篇幅与格式硬规范**：竞赛论文必须满足——①正文（问题重述至模型评价结束，不含摘要/目录/参考文献/附录）**18~25页**，不足18页必须扩充分析/验证/图表解读/灵敏度实质内容，超过25页必须精简；②附录（代码/支撑说明）**不限页数**；③**第1页为摘要页，严格限定1页**（300~800字，含方法+关键数字+稳健性结论），不得跨页；④**第2页起为目录**，强制只占1页，目录**保留到二级标题**，通过调整行距（如\setstretch{1.0}）、字号（如\small）、tocdepth=2 压至1页；⑤页码从**正文起标1**（默认），摘要页与目录页不标页码或标罗马数字；⑥禁止靠加图加表凑页数
10. **每次必写论文**：任何等级的数学建模任务完成后必须产出论文，不允许只交代码或只给结论
11. **封箱前必一键复跑**：在独立干净目录下执行全量一键复跑脚本，确认生成的所有图表和表格与论文数字 100% 吻合
12. **人机协同与分阶段审批（Human-in-the-Loop Gates）**：在 L2/L3 任务中，严禁 AI 从头到尾黑盒盲跑。每个关键阶段（CP0~CP5）必须输出标准【人机协同审批卡】，主动列出已完成产出、待决策事项、AI推荐方案及备选方案，等待人类（队长/指导教师/用户）进行确认（`/approve`）、修改参数或假设（`/revise`）、选择路线（`/select`）后方可推进至下一阶段。

---

## 🏆 极简 6 步真实竞赛工作流 (6 Steps & CP0~CP5)

> 详细规范与协同协议参见 [`references/real_competition_workflow_72h.md`](file:///f:/CodeworksF/skills/math-modeling/references/real_competition_workflow_72h.md) 与 [`references/human_in_the_loop_protocol.md`](file:///f:/CodeworksF/skills/math-modeling/references/human_in_the_loop_protocol.md)。

```
【Step 0: 选题】赛题初筛、量化评估与立项 ──────→ 📋 [CP0 审批点] 选题决策卡与规则确认
                                                      ↓ (/approve 或 /select_topic)
【Step 1: 审计】数据清洗、统一符号与假设 ──────→ 📋 [CP1 审批点] 符号系统、数据审计与假设清单
                                                      ↓ (/approve 或 /revise)
【Step 2: 求解】多问递进建模与代码求解 ────────→ 📋 [CP2 审批点] 公式推导、约束满足与中间解复核
                                                      ↓ (/approve 或 /tune)
【Step 3: 验证】全方位验证、灵敏度与冻结 ──────→ 📋 [CP3 审批点] 改装对照表、参数弹性与数字冻结
                                                      ↓ (/approve 或 /freeze)
【Step 4: 论文】灵魂摘要精雕与LaTeX排版 ────────→ 📋 [CP4 审批点] 1页三段式摘要与论文大纲评审
                                                      ↓ (/approve 或 /refine)
【Step 5: 封箱】独立复现质检、匿名与打包 ───────→ 📋 [CP5 审批点] 干净环境一键复跑报告与终审交付
```

---

### Step 0：选题 (Topic) ➔ 📋 Checkpoint 0
> 详见独立规范：[`stages/00_topic.md`](file:///f:/CodeworksF/skills/math-modeling/stages/00_topic.md) | 快捷指令：`/topic`
- **AI 动作**：通读所有候选赛题，从“数据可得性、算法可解性、团队技术栈匹配度、12h跑通Baseline概率”四个维度进行量化评分；生成 `topic_decision.md` 与 `competition_brief.md`。
- **人类动作**：队长/团队召开选题会，结合专业背景敲定最终选题（`/select_topic [题号]`），明确队伍三角色分工与时间线。

---

### Step 1：审计 (Audit) ➔ 📋 Checkpoint 1
> 详见独立规范：[`stages/01_audit.md`](file:///f:/CodeworksF/skills/math-modeling/stages/01_audit.md) | 快捷指令：`/audit`
- **AI 动作**：
  - 建立数据证据链（`data/raw/` 保持只读、`data_processing_log.md` 记录清洗规则）；
  - 进行探索性数据分析 (EDA)，检测缺失机制与极端值分布；
  - 建立全篇统一的数学符号表 `symbols.md`，绘制设问递进图；
  - 梳理《核心假设清单》`assumptions.md`（注明合理性与失效影响）；
  - 运行 ≤30 行 Baseline PoC 代码，获取第一批保底运行数字。
- **人类动作**：审核符号定义是否清晰、检查假设是否符合实际常识、确认数据清洗逻辑（`/approve` 或 `/revise assumption`）。

---

### Step 2：求解 (Solve) ➔ 📋 Checkpoint 2
> 详见独立规范：[`stages/02_solve.md`](file:///f:/CodeworksF/skills/math-modeling/stages/02_solve.md) | 快捷指令：`/solve`
- **AI 动作**：
  - **Q1 基础层**：建立可解释的经典模型（如线性规划、微分方程、基础统计回归），生成基准解；
  - **Q2 变化层**：明确题干新增条件，进行增量模型改装（松弛假设、引入新约束/非线性项/不确定性）；
  - **Q3 开放层**：构建量化评价指标体系、反事实推演、多情景仿真或政策建议；
  - 编写规范求解代码，监控求解器收敛状态与约束满足率（Slack/Surplus）。
- **人类动作**：复核数学公式逻辑与物理量纲、评估中间解是否反常识、调整关键超参数（`/approve` 或 `/tune`）。

---

### Step 3：验证 (Validate) ➔ 📋 Checkpoint 3
> 详见独立规范：[`stages/03_validate.md`](file:///f:/CodeworksF/skills/math-modeling/stages/03_validate.md) | 快捷指令：`/validate`
- **AI 动作**：
  - 执行严格验证协议（时间外/滚动验证、残差诊断、Durbin-Watson 检验）；
  - 制作 **改装效果对照表**（同口径对比 Baseline vs 改进模型）；
  - 计算关键参数弹性 $S = \frac{x}{y}\frac{dy}{dx}$ 与 ±10%~±20% 扰动敏感性分析；
  - 汇总结算全题关键指标，生成待冻结数据表。
- **人类动作**：核验验证指标的真实提升幅度、指定需深入分析的敏感参数，批准锁定最终数据（`/approve` 锁定写入 `frozen_numbers.json`）。

---

### Step 4：论文 (Paper) ➔ 📋 Checkpoint 4
> 详见独立规范：[`stages/04_paper.md`](file:///f:/CodeworksF/skills/math-modeling/stages/04_paper.md) | 快捷指令：`/paper`
- **AI 动作**：
  - 撰写 **1 页三段式灵魂摘要**（首段背景定位 + 中段分问方法与精确冻结数字 + 末段模型特色与稳健性结论）；
  - 绘制高质量矢量图（雷达图、相图、热力图、流向图）与标准三线表（booktabs）；
  - 排版 LaTeX 源码，严格控制正文 18~25 页、第1页摘要、第2页目录（二级标题）、正文页码从 1 开始。
- **人类动作**：逐句推敲摘要行文与亮点表达、审定图表解读深度、调整各章节篇幅比例（`/approve` 或 `/refine abstract`）。

---

### Step 5：封箱 (Pack) ➔ 📋 Checkpoint 5
> 详见独立规范：[`stages/05_pack.md`](file:///f:/CodeworksF/skills/math-modeling/stages/05_pack.md) | 快捷指令：`/pack`
- **AI 动作**：
  - 在独立干净目录下执行全量一键复跑测试脚本，核对生成图表/表格与论文数字 100% 吻合；
  - 全文匿名合规扫描（清除代码、注释、正文、PDF 元数据中的任何个人/学校信息）；
  - 整理支撑材料目录树（`supporting_materials/`），生成 README 说明与 MD5 校验码。
- **人类动作**：终审签名确认、核对赛事系统提交要求、完成最终封箱提交。

---

## 🪜 多问递进题：从设问到创新的执行框架（L2/L3必用）

### 核心判断

多问竞赛题常采用“基础参照 → 条件变化 → 开放评价/决策”的递进，但这只是**优先检验的假设**，不是机械定律。必须依据题干中的变量继承、条件变化和输出依赖确认；若题目明确要求独立求解，则按独立问题处理。

| 问题层级 | 首要目标 | 建模策略 | 高价值输出 |
|---|---|---|---|
| Q1 基础层 | 建立可信参照 | 简洁、可解释的经典模型 | 基准方案、误差/目标值、关键假设与局限 |
| Q2 变化层 | 回应新增现实条件 | 从 Q1 增量改装，少做无关重构 | 条件→模型改动映射、与 Q1 的同口径对照 |
| Q3 开放层 | 解释、评价或决策 | 组织前两问结果为评价体系/情景建议 | 指标定义、机制解释、阈值/排序、边界条件 |

### 审题表（开始建模前填写）

| 项目 | Q1 | Q2（相对 Q1 的变化） | Q3（对 Q1/Q2 的要求） |
|---|---|---|---|
| 目标与输出 |  |  |  |
| 新增条件/数据 | — |  |  |
| 继承的变量/结论 | — |  |  |
| 失效的假设 | — |  |  |
| 模型动作 | baseline | 新参数/约束/机制 | 评价指标/情景/建议 |
| 验证指标 |  | 同口径对照 | 稳健性与可解释性 |

### “新增条件 → 模型改装”词典

| 题干信号 | 可选模型动作 | 必须验证 |
|---|---|---|
| 缺失、观测不全、数据质量差 | 机制说明的插补、多重插补、贝叶斯估计、缺失敏感性分析 | 不同处理下结论是否稳定；避免用测试信息插补训练集 |
| 时间窗、容量、预算、服务水平 | 新增硬约束，或有含义明确的惩罚项/松弛变量 | 可行性、约束违背率、目标代价 |
| 扰动、需求波动、事故、随机性 | 情景集、蒙特卡洛、鲁棒/随机优化 | 分位数表现、风险指标、不同随机种子稳定性 |
| 多主体目标冲突 | 多目标优化、Pareto 前沿、权重法与权重敏感性 | 权重变化是否导致结论翻转 |
| “是否合理”、影响机理、给建议 | 构造可解释指标体系、反事实/情景模拟、阈值分析 | 指标方向、权重来源、建议对结果的可追溯性 |

### 三天资源分配（72小时赛，仅作可调整默认）

- **0–12小时**：完成题意、数据和递进关系审计；先跑通 Q1 可复现 baseline，保留全部中间结果。
- **12–36小时**：针对 Q2 的新增条件逐项改装、验证；优先完成真实的 Q1 vs Q2 同口径对照，不以复杂度替代证据。
- **36–54小时**：完成 Q3 的指标体系/机制解释/情景建议，补充敏感性和局限性。
- **54–72小时**：冻结数字、补全论文叙事、交叉核对图表与代码、完成格式和复现检查。

### 禁止做法

1. 不经题干验证就武断把 Q1/Q2/Q3 套入固定套路。
2. Q2 完全推翻 Q1 却不解释为何基础结构无法保留。
3. 用不同数据、不同指标比较 Q1/Q2，并据此宣称“改进”。
4. 用“创新”“更准确”等词替代真实的对照实验与量化结果。
5. Q3 只写空泛建议，未给出指标、证据或适用条件。

---

## ⚠️ Top 13 坑（高频致命错误）

1. **先写结果后补模型** → 论文逻辑倒置，直接降档
2. **没有 baseline 就宣称更优** → 无法证明模型价值
3. **plt.show() 弹窗** → 用户明确禁止，必须 savefig+close
4. **数字不一致** → 摘要/正文/表格/图表中同一数字不同
5. **中文路径崩溃** → Python 用 `E:/`，bash 用 `/e/`
6. **数据泄漏** → 用全量标准化后再划分训练/测试
7. **异常值删除不说明** → 必须记录删除规则和数量
8. **图表无解读** → 每张图/表后必须有2-4句分析文字
9. **摘要无数字** → 必须包含每个子问题的关键数值结果
10. **模型过复杂** → 深度学习在小数据场景不如简单模型
11. **把递进设问写成割裂的三篇小论文** → 先审计变量/条件继承；能迭代则保留 Q1 为 baseline，并以 Q2 的新增条件驱动改装
12. **把“创新”写成口号** → 创新必须对应题干条件、明确的模型变动和同口径的量化验证
13. **把Q3建议写成常识** → 至少给出指标定义、阈值/情景或排序依据，并说明适用边界

---

## 📚 参考文件索引

### 核心参考（按需加载）

| 文件 | 内容 | 何时加载 |
|------|------|---------|
| `references/real_competition_workflow_72h.md` | 72h/96h 真实竞赛全真生命周期、三角色协同分工与评委偏好指南 | 赛前开题、流程规划与时间线对齐时 |
| `references/human_in_the_loop_protocol.md` | 人机协同各审批点规范 (CP0~CP5)、交互指令集与审批卡模板 | 阶段转换与请求人类审批时 |
| `references/competition_execution_protocol_v6_3.md` | 赛事规则卡、问题规格、数据证据链、验证协议、协作与复现门控 | L2/L3建模启动、验证与提交前 |
| `references/model_selection_guide.md` | 模型选择决策树 + 题型到方法映射 + 经典机理矩阵 | Step 2 方法选择时 |
| `references/classic_math_models_handbook.md` | 《数学模型》全书13个专题经典模型公式/推导/判据速查手册 | 机理推导/微分方程/差分/博弈/马氏链建模时 |
| `references/programming_and_discrete_tricks.md` | 运筹规划与离散建模技巧（0-1大M法/分段线性/对偶价格/AHP/有向图排名） | 建立优化与离散评价模型时 |
| `references/paper_writing_guide.md` | 论文逐模块写作规范+模板 | Step 5 写论文时 |
| `references/paper_quality_checklist.md` | 论文格式/篇幅/质量检查清单 | Phase 3 最终检查时 |
| `references/latex_guide.md` | LaTeX编译+目录控制+常见问题 | 编译PDF时 |
| `references/latex_windows_patterns.md` | Windows LaTeX 环境检查与编译模式 | MiKTeX/TeXLive 环境排查时 |
| `references/windows-latex-temp-compile-and-zip.md` | 中文路径下 LaTeX 稳健编译与打包 | 项目路径含中文/空格导致编译失败时 |
| `references/visualization_guide.md` | 可视化规范+字体+图表命名 | 画图时 |
| `references/cumcm_c_problem_expert_handbook.md` | 国赛C题专家评审精要与真题解法全集 (2020~2025，含CLR转换与线性化) | 求解C题/数据驱动与运筹规划时 |
| `references/supporting_materials_layout_v5_0.md` | 支撑材料目录结构（v5.0 精简版） | 打包交付时 |

### 案例参考（特定题型时加载）

| 文件 | 内容 |
|------|------|
| `references/water_quality_case.md` | 水质/供水类题目经验 |
| `references/air_quality_analysis.md` | 空气质量分析案例 |
| `references/oil_tank_calibration_case.md` | 储油罐变位识别/罐容表标定（几何+标定类） |

### 案例库（cases/）

本地私有案例库（60+个国赛/校赛/APMCM 复盘记录，含真实路径与内部踩坑），**仅本地保留，不随公开版发布**。做题前请先在本地 `cases/` 目录按题型检索同类题经验。

### 竞赛攻略（正式竞赛时加载）

| 文件 | 内容 |
|------|------|
| `references/cumcm_competition_guide.md` | 国赛72小时工作流+评分标准 |
| `references/advanced_competition_strategy.md` | 国一/O奖深度策略 |

### 脚本与模板

| 文件 | 内容 |
|------|------|
| `scripts/math_modeling_utils.py` | 优化/统计诊断/预测/评价/动力系统与马氏链/博弈/可视化工具库 (v3.0) |
| `scripts/advanced_visualization_templates.py` | 高级可视化模板（依赖 matplotlib+numpy） |
| `scripts/hybrid_scholar.py` | 论文检索融合（OpenAlex+AnySearch 交叉验证） |
| `scripts/anysearch_academic.py` | AnySearch 学术检索 |
| `scripts/openalex_scholar.py` | OpenAlex 学术检索（无需API Key） |
| `templates/latex_template_cn.tex` | 中文LaTeX论文模板（已内置硬规则9页码/目录控制） |
| `templates/paper_template.tex` | 英文论文模板 |
| `templates/paper_search_config.yaml` | 论文检索配置 |
| `templates/supporting_materials_README.md` | 支撑材料说明模板 |
| `references/legacy-ppt-conversion.md` | 旧版 .ppt→.pptx 转换（PowerPoint COM） |

---

## IMA 知识库（可选，本地配置）

本地版 Skill 关联私有 IMA 知识库「数学建模2026」用于案例检索；公开版不包含私有知识库 ID，如本地使用请自行配置。


