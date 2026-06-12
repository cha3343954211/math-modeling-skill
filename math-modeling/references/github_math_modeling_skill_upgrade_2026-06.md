# GitHub 数学建模 Skill 四仓库融合研究（2026-06-06）

本文件记录对用户指定 4 个 GitHub 仓库的实地克隆检查结果，用于升级 Hermes `math-modeling` skill。仓库用于流程、质量门控、模板和工具思想参考；不直接复制外部仓库大段正文或代码。

## 仓库与版本快照

| 仓库 | 本地目录 | HEAD | 最新提交日期 | 可融合重点 |
|---|---|---:|---|---|
| `Lupynow/math-modeling-skills` | `math-modeling-skills` | `aa74c8d` | 2026-05-30 | solver/paper 双 skill、12 类问题本质、阶段 1.5 文献证据、95+ 场景模型矩阵、cookbook/playbook、MCM/Memo/Letter 写作规则 |
| `zhnnky329/MathModeling-skills` | `MathModeling-skills` | `1762e5b` | 2026-06-05 | 26 skill 串联、G1-G6 门控、≤30 行 PoC、`frozen_numbers.json`、review 文件落盘、三审计层、工作区产物链 |
| `XiaoMaColtAI/math-modeling-skill` | `math-modeling-skill` | `6ba1c47` | 2026-05-31 | 三角色协作（建模手/编程手/论文手）、Model Contract、术语表、Figure Contract、SVG+PNG+HTML 图表面板、Claim-Evidence 写作 |
| `yushui2022/MathModel-Skill` | `MathModel-Skill` | `058cb20` | 2026-06-02 | preflight、附件分类、结果模板识别、workflow contracts、Evidence Gate、Format Gate、结构化契约 |

## 融合后的核心执行原则

### 1. 先判定“是否真的需要建模”

来自 Lupynow 的问题拆解方法：在拆小问前先判断该小问是建模问题还是确定性计算。

- 建模问题：存在模型选择空间、需要假设、优化、不确定性、统计推断或多方法竞争。
- 非建模问题：题给公式代入、确定性乘加、min/max 截断、无方法选择余地的数据核算。
- 处理要求：非建模问题不强行套模型，只说明计算公式、输入、输出和误差来源；若题面明确要求“建立模型”，仍按建模问题处理。

### 2. 采用 12 类问题本质分类

对每个子问题至少标注一个主类型，必要时标注混合类型和前后数据流：

1. 预测/回归
2. 分类/判别
3. 评价/排序
4. 优化/决策
5. 机理/物理
6. 聚类/分组
7. 关联/因果
8. 博弈/策略
9. 几何/运动学
10. 统计推断/实验设计
11. 网络科学/图论
12. 生态系统/环境

常见混合：预测→优化、评价→优化、机理→优化、聚类→分类、网络→优化。混合题必须说明前置结果如何传递到后置模型。

### 3. 方法选择不查表拍脑袋：文献/案例证据 + 场景矩阵 + PoC

方法推荐至少同时满足：

- **场景匹配**：样本量、线性/非线性、是否外推、是否含整数变量、是否多目标、可解释性要求、计算规模。
- **证据支撑**：用 IMA、GitHub、论文、官方文档或教材查 2--3 个相近案例；记录方法、适用条件、风险。按用户偏好，不把 SkillHub 作为常规资料侦察来源。
- **baseline**：每个主模型默认有一个简单 baseline；无 baseline 必须解释。
- **≤30 行 PoC**：候选主方法进入正式代码前，必须在真实清洗数据小切片上跑出一个可行性数字；失败候选标记 `[REJECTED]`，不得在论文中写成已采用方法。

### 4. 三角色协作升级为“角色合同”

融合 XiaoMa 的三角色思想，但在 Hermes 中不强制拆成独立 skill，而是把职责写入过程文件：

- **建模手合同**：`planning/model_contract.md`，包含题目目标、输出要求、子问题依赖、候选模型、假设作用、baseline、验证计划、风险。
- **编程手合同**：`code/Qx/run_contract.md` 或 `支撑材料/questN/outputs/run_contract.md`，包含输入文件、清洗口径、随机种子、输出文件、图表计划、运行命令。
- **论文手合同**：`paper/claim_evidence_map.md`，每个结论必须映射到结果表、图表、冻结数字或文献引用。

### 5. Figure Contract 与图表分级

每张图表生成前写 Figure Contract：

```text
figure_id:
用途: 诊断图 / 对比图 / 论文主图 / 附录图
对应结论:
数据来源:
图表类型:
横纵轴/单位:
配色与标注:
输出格式: PNG 300dpi；必要时 SVG/PDF 矢量
正文解释要点:
```

图表分级：

- Type 1 诊断图：只用于排错，禁止进论文。
- Type 2 对比图：用于方法比较，可进支撑材料。
- Type 3 论文主图：通过中文渲染、字号、无遮挡、单位、标题、证据一致性检查后才能进正文。
- Type 4 附录图：补充说明。

### 6. Claim-Evidence 映射

论文写作前必须有 `claim_evidence_map.md` 或等价材料：

| claim_id | 论文位置 | 结论/主张 | 证据文件 | 冻结数字键 | 图表/表格 | 风险边界 |
|---|---|---|---|---|---|---|

规则：
- 没有证据的数字不进摘要和结论。
- 每个关键数值结果至少从“实际含义、baseline 对比、敏感性/稳健性、跨问一致性、不确定性”中选 3 类讨论。
- 论文结论不得引入未在模型结果和证据链中出现的新主张。

### 7. G1-G6 门控与三审计层

建议把现有 Hermes `S0 → G1-G6` 流程细化为：

- **S0 Preflight**：题面/附件可读性、结果模板识别、旧产物/stale 风险、输出目录确认。
- **G1 PROBLEM_PARSED**：完成题目解析、分类、依赖图、符号初表、数据归属表。
- **G2 METHOD_VALIDATED**：每问候选方法、baseline、≤30 行 PoC、可行性数字、淘汰记录。
- **G3 CODE_REVIEWED**：正式代码可运行；review 文件落盘，至少 5 条具体检查项，尽量带 `file:line`；优化题列约束方向表。
- **G4 RESULTS_FROZEN**：最终结果分析、稳健性报告、图表计划和 `frozen_numbers.json` 完成；改代码后必须重新冻结。
- **G5 PAPER_SECTION_READY**：论文段落只引用材料包、冻结数字和 Claim-Evidence map；每问闭环完整。
- **G6 AUDIT_LAYER_PASSED**：一致性审计、完整性审计、质量/反造假审计全部通过。

### 8. 失败回退路线

| 发现的问题 | 回退到 |
|---|---|
| 题意理解错、漏问 | G1 / problem parser |
| 模型不能输出题目要求 | G2 / method selector |
| PoC 跑不动或结果不合理 | G2，换候选或降级 baseline |
| 代码与公式不一致、约束方向错 | G3 / code review |
| 论文数字找不到来源 | G4 / solution package + frozen numbers |
| 图表和结论矛盾 | Figure Contract + G4 |
| 摘要或结论过度宣称 | G5/G6 paper audit |
| 引用、数据、实验疑似虚构 | G6，阻塞提交 |

## 对当前 Hermes math-modeling skill 的升级落点

1. 在主 `SKILL.md` 中新增“四仓库融合升级规则”。
2. 保留原有顺序求解、三层质量门控、IMA、支撑材料结构和用户偏好。
3. 强化 12 类题型分类、文献证据、PoC、Figure Contract、Claim-Evidence、三审计层。
4. 新增本研究文件为支持文件，作为后续维护和溯源依据。
