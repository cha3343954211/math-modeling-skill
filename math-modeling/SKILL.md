---
name: math-modeling
description: "数学建模竞赛全流程自动化：问题分析、模型构建、代码实现、论文写作、可视化。支持CUMCM/MCM/ICM等主流赛事。"
version: 6.0.0
author: MiMo V2.5 Pro + Capoo
metadata:
  hermes:
    tags: [mathematical-modeling, competition, optimization, statistics, machine-learning, paper-writing]
    related_skills: [data-science, software-development, creative]
---

# 数学建模 Skill v6.0

## 适用场景

当用户需要进行数学建模相关工作时加载此 Skill：
- **竞赛备赛**：CUMCM（国赛）、MCM/ICM（美赛）、MathorCup、APMCM等
- **课程作业**：数学建模课程、运筹学、统计分析
- **实际问题**：需要将实际问题转化为数学模型

---

## ⚡ 第一步：任务规模检测

收到题目后，先判断规模等级，决定流程重量：

| 等级 | 场景 | 流程 |
|------|------|------|
| **L1 课程作业** | 1-2问，数据简单，无竞赛压力 | 简化：直接建模+写论文，跳过PoC和冻结数字 |
| **L2 练习赛** | 3-4问，需要验证，有评分 | 标准：PoC→建模→验证→论文 |
| **L3 正式竞赛** | 完整赛题，限时提交 | 完整：全部门控+冻结数字+支撑材料 |

判断依据：用户是否提到"竞赛/比赛/CUMCM/MCM"、题目是否有多个子问题、是否有附件数据、是否有时间限制。

---

## 🔴 用户偏好硬规则（必须遵守）

1. **图表保存不弹窗**：所有 `plt.savefig(..., dpi=300, bbox_inches='tight')` + `plt.close()`，禁止 `plt.show()`
2. **中文路径兼容**：Python 代码中用 `E:/` 格式，不用 `/e/`；bash 中可用 `/e/`
3. **逐问求解**：先完成 Q1 再进入 Q2，每问形成小闭环（模型→验证→结果→结论）
4. **不要编造数据/结果**：数字必须来自真实代码运行，不从截图/CSV临时抄
5. **中文字体**：matplotlib 设置 `plt.rcParams['font.sans-serif'] = ['SimHei']`
6. **工作区**：默认 `E:\HermesE`；项目目录优先用用户指定路径
7. **不弹窗**：所有 Python 可视化脚本必须 savefig+close

---

## 📐 3-Phase Quality Gate（统一质量框架）

### Phase 1：输入门控（Input Gate）

完成以下检查后方可开始建模：

- [ ] 题目解析：每个子问题的"要求输出→核心对象→模型类型→输出形式"已明确
- [ ] 数据审计：缺失值、异常值、单位、口径、训练/测试划分规则已记录
- [ ] 方法选择：每个子问题有 baseline + 主模型候选，附选择理由
- [ ] PoC验证（L2/L3）：每个候选方法 ≤30行 PoC，输出可行性数字
- [ ] 假设清单：每条假设标注"必要性+合理性+在模型中如何使用"

### Phase 2：过程门控（Process Gate）

代码跑通、结果可信后方可写论文：

- [ ] 代码可复现：固定随机种子 `np.random.seed(42)`，路径不依赖本地临时目录
- [ ] 结果验证：预测类看MAE/RMSE/MAPE；优化类看约束满足；评价类看排名稳定性
- [ ] Baseline对比：主模型必须说明为什么比 baseline 更好
- [ ] 数字冻结（L3）：关键数字写入 `frozen_numbers.json`，论文只引用冻结数字
- [ ] 错误侦测：结果数量级合理、图表趋势与文字一致、无数据泄漏

### Phase 3：输出门控（Output Gate）

论文和支撑材料交付前最终检查：

- [ ] 摘要覆盖所有子问题，含具体方法名+关键数字结果
- [ ] 每个子问题有"问题要求→模型→求解→结果→解释→检验"完整链
- [ ] 所有图表有编号、单位、正文引用和2-4句解读
- [ ] 论文数字与代码/frozen_numbers一致，无手工改数
- [ ] 参考文献≥5篇，格式统一；附录含核心代码和复现说明
- [ ] PDF页数达标（竞赛≥15页；作业按用户要求）

### 三阶段不通过时的回退

| 阶段 | 常见问题 | 回退到 |
|------|---------|--------|
| P1失败 | 题意理解错、方法不匹配 | 审题/方法选择 |
| P2失败 | 代码报错、结果不合理 | 代码调试/数据检查 |
| P3失败 | 摘要无数字、逻辑断裂 | 论文补写 |

---

## 🔄 工作流主干（5步）

### Step 1：审题与解析

- 拆解每个子问题：输入条件、约束、目标、输出形式
- 识别题型：评价/预测/优化/机理/分类/仿真/图论/数据分析/混合
- 生成数据审计摘要（来源、字段、缺失、异常、单位、划分）
- 确定子问题间的依赖关系（Q1结论是否支撑Q2）

### Step 2：方法选择与验证

- 按题型选 baseline + 主模型（参考 `references/model_selection_guide.md`）
- PoC 要求（L2/L3）：≤30行，真实数据小切片，输出一个可行性数字
- 候选方法池至少2个，附选择理由和淘汰记录
- 失败候选标记 `[REJECTED]` 并归档

### Step 3：建模与求解

- 分子问题依次求解，每问形成闭环
- 代码规范：路径用 `E:/` 格式；随机种子固定；中间结果存 `outputs/`；图表存 `figures/`
- 关键数字写入 `frozen_numbers.json`（L3必做，L2推荐）
- 每问完成后生成 run_summary.json（输入、输出、指标、种子）

### Step 4：验证与稳健性

- 灵敏度分析：至少2个关键参数，±10%~20%扰动，输出对比表/图
- Baseline对比：主模型 vs baseline 的指标对比表
- 随机算法至少跑3次，检查结论稳定性
- 重要公式用小样本手算或 SymPy 验证

### Step 5：论文写作与交付

- 论文结构：摘要→问题重述→问题分析→模型假设→符号说明→模型建立→检验→评价→参考文献→附录
- 摘要公式：背景+子问题1方法和结果+子问题2方法和结果+…+稳健性结论
- 每个关键结果用"数值+对比+含义"三段式
- LaTeX 模板见 `templates/latex_template_cn.tex`
- 支撑材料按 `references/supporting_materials_layout_v5_0.md` 组织

---

## ⚠️ Top 10 坑（高频致命错误）

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

---

## 📚 参考文件索引

### 核心参考（按需加载）

| 文件 | 内容 | 何时加载 |
|------|------|---------|
| `references/model_selection_guide.md` | 模型选择决策树+题型→方法映射 | Step 2 方法选择时 |
| `references/paper_writing_guide.md` | 论文逐模块写作规范+模板 | Step 5 写论文时 |
| `references/paper_quality_checklist.md` | 论文格式/篇幅/质量检查清单 | Phase 3 最终检查时 |
| `references/latex_guide.md` | LaTeX编译+目录控制+常见问题 | 编译PDF时 |
| `references/visualization_guide.md` | 可视化规范+字体+图表命名 | 画图时 |
| `references/windows_patterns.md` | Windows路径/字体/Excel读取 | 遇到环境问题时 |
| `references/supporting_materials_layout_v5_0.md` | 支撑材料目录结构 | 打包交付时 |
| `references/gemini_assisted_modeling.md` | Gemini辅助建模流程 | 需要外部AI协助时 |

### 案例参考（特定题型时加载）

| 文件 | 内容 |
|------|------|
| `references/water_quality_case.md` | 水质/供水类题目经验 |
| `references/air_quality_analysis.md` | 空气质量分析案例 |
| `references/canteen_case_study.md` | 食堂选址案例 |

### 竞赛攻略（正式竞赛时加载）

| 文件 | 内容 |
|------|------|
| `references/cumcm_competition_guide.md` | 国赛72小时工作流+评分标准 |
| `references/advanced_competition_strategy.md` | 国一/O奖深度策略 |

### 脚本与模板

| 文件 | 内容 |
|------|------|
| `scripts/math_modeling_utils.py` | 优化/统计/预测/评价/可视化工具库 |
| `templates/latex_template_cn.tex` | 中文LaTeX论文模板 |
| `templates/paper_template.tex` | 英文论文模板 |
| `templates/paper_search_config.yaml` | 论文检索配置 |

---

## IMA 知识库

**知识库名称**：数学建模2026
**知识库 ID**：`cw0vzkonAnWnUx1GR_nB4Hg0e9iYkipcEw6a1BTE-w8=`

查询时机：审题阶段查类似题解法；方法选择阶段查算法实现；论文阶段查优秀论文结构。
