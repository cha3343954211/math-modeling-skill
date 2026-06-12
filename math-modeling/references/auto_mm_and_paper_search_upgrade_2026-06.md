# auto-MM + Paper Search 融合升级记录（2026-06）

> 本文件记录将 `deafenken/auto-MM` 与 `XiaoMaColtAI/math-modeling-skill` 的可复用机制融合进当前 Hermes `math-modeling` skill 的规则。重点是：竞赛长流程状态管理、完整性门禁、真实引用护栏，以及 XiaoMaColtAI 项目的 OpenAlex + AnySearch 双引擎论文检索。OpenAlex 礼貌池邮箱已按用户要求配置为 `<your-email@example.com>`。

## 1. 外部项目版本快照

- `deafenken/auto-MM`：本地克隆目录 `<USER_HOME>/AppData/Local/hermes/tmp/math_skill_repos/auto-MM`，HEAD `ac90a55`，提交信息 `feat: triage scores a 6th axis "Skill leverage" — pick the problem this suite is built to win on`。
- `XiaoMaColtAI/math-modeling-skill`：本地克隆目录 `<USER_HOME>/AppData/Local/hermes/tmp/math_skill_repos/math-modeling-skill`，HEAD `6ba1c47`，提交信息 `release: 角色子Skill重构 + AnySearch双引擎搜索 + 可视化面板升级`。

只融合工作流、配置方式和检索思想；不复制论文正文、竞赛答案或不可验证结论。

## 2. 从 auto-MM 融合的关键机制

### 2.1 长流程状态契约

auto-MM 强调“没有写盘就不存在”。当前 skill 后续执行正式竞赛/长期建模任务时，应把状态落盘到项目 `支撑材料/` 中，而不是只放在对话里：

```text
支撑材料/
├── run.yaml                  # 比赛、题目、deadline、语言、团队/匿名要求、预算
├── progress.jsonl            # append-only 进度日志
├── STOP / PAUSE              # 可选人工停止/暂停信号
├── references/literature.md  # 真实文献与检索记录
├── questN/outputs/           # 每问结果、实验配置、冻结数字
└── papper/                   # 论文草稿、LaTeX、PDF、构建日志
```

### 2.2 选题六轴评分

当用户给出 A/B/C/D 多题并要求选题时，在原可行性分析之外新增第 6 轴 `skill_leverage`：

1. 题意清晰度；
2. 数据/附件可处理性；
3. 模型可解释性；
4. 验证可行性；
5. 论文表达空间；
6. **skill_leverage**：当前 skill、已有案例、代码库、文献资源对该题的可复用程度。

选题不是选“看起来简单”，而是选最容易在 72 小时内形成证据链和高质量论文的题。

### 2.3 10 条完整性规则中必须吸收的规则

- 题面优先：题面与外部资料冲突时，正文主模型采用题面口径，外部口径进入敏感性分析。
- 匿名性硬门禁：正式提交 PDF、LaTeX、代码、图表、元数据不得泄露姓名、学校、系统用户名、git remote 等身份信息。
- 真实 citation only：参考文献必须能通过 DOI、arXiv、OpenAlex、出版社页面或稳定 URL 找到；找不到就删除或改写为假设。
- AI/ML 服务真实不确定性：不能用复杂模型预测闭式可算的量。
- 算法必须由问题结构解释：每个复杂算法组件要说明解决了哪类结构难点。
- 验证是交付物：baseline、小规模精确解 gap、消融、敏感性/稳健性至少覆盖 3 项，且正式论文中不得宣传缺少验证支撑的 headline number。
- 时间预算硬约束：最后 6 小时默认 lockdown，只允许写作、构建、检查、打包，不再开新模型。
- 图表是证据：每张正文图必须被正文引用并回答读者问题。
- 摘要必须有硬数字。
- 提交包卫生：zip 中只放竞赛要求文件，排除 `.git/`、临时文件、系统垃圾、构建中间件，并能在干净机器解压。

## 3. 从 XiaoMaColtAI 融合的 Paper Search 机制

XiaoMaColtAI 项目中 `tools/paper_search` 使用 **OpenAlex + AnySearch 双引擎并行搜索**：

- OpenAlex：免费、无需 API Key；通过 `mailto`/User-Agent 中的邮箱进入 Polite Pool，提高速率限制；
- AnySearch：JSON-RPC 2.0 调用 `https://api.anysearch.com/mcp` 的 academic 搜索；可匿名访问但速率较低；若用户提供 `ANYSEARCH_API_KEY`，通过环境变量或 CLI 参数使用；
- Hybrid Scholar：`ThreadPoolExecutor` 并行调用两源，先 DOI 精确去重，再标题模糊去重；结果分为“交叉验证 / OpenAlex 独有 / AnySearch 独有”。

当前 skill 已安装脚本到：

```text
scripts/openalex_scholar.py
scripts/anysearch_academic.py
scripts/hybrid_scholar.py
```

并已将 `hybrid_scholar.py` 默认 OpenAlex 邮箱配置为：

```text
<your-email@example.com>
```

## 4. 论文检索执行规则

正式建模前，除 IMA/GitHub/官方文档外，若需要学术文献支撑模型选择、算法来源、评价指标、领域背景，优先运行双引擎检索。

### 4.1 默认命令

在 skill 目录或复制脚本到项目 `支撑材料/references/tools/` 后运行：

```bash
python scripts/hybrid_scholar.py \
  --query "TOPSIS entropy weight evaluation mathematical modeling" \
  --email "your-email@example.com" \
  --limit 8 \
  --field mathematics \
  --json
```

如果只需 OpenAlex 或 AnySearch：

```bash
python scripts/hybrid_scholar.py --query "vehicle routing integer programming" --email "your-email@example.com" --openalex-only --json
python scripts/hybrid_scholar.py --query "grey prediction model GM(1,1)" --anysearch-only --json
```

AnySearch API Key 是可选项，不写入 skill。若用户另行提供，应使用临时环境变量：

```bash
export ANYSEARCH_API_KEY="[REDACTED]"
python scripts/hybrid_scholar.py --query "..." --email "your-email@example.com" --json
```

### 4.2 检索记录落盘格式

每次正式检索应写入项目：

```text
支撑材料/references/literature_search_log.md
支撑材料/references/literature_candidates.json
支撑材料/references/literature.md
```

`literature_search_log.md` 建议格式：

```text
query | date | engine | hits | selected | reason | risk
TOPSIS entropy weight evaluation | 2026-06-06 | OpenAlex+AnySearch | 16 | 3 | 评价模型/权重方法来源 | 需核验 DOI/URL
```

`literature.md` 中每条候选文献必须记录：

```text
标题；作者；年份；DOI/URL/arXiv；来源引擎；是否交叉验证；用于本文哪里；不能支撑的内容。
```

## 5. 引用门禁

文献只能支撑“方法来源、理论背景、指标定义、领域常识”，不能替代本题实验结果。进入论文参考文献前必须通过：

1. 有 DOI、arXiv、OpenAlex ID、出版社页或稳定 URL；
2. 标题和作者能在检索结果中复核；
3. 与本文模型/指标确实相关；
4. 引用位置明确：问题分析、模型建立、指标定义或模型评价；
5. 不把 AnySearch/OpenAlex 单源摘要当作事实结论直接引用；必要时再打开原文/摘要页核验。

若文献不可验证，写入 `literature_rejected.md`，不得进入 `references.bib` 或参考文献列表。

## 6. 与当前获奖级流程的结合

- G1：根据题型生成 3--5 个英文检索 query；
- G2：用 Paper Search 找到 2--3 篇可验证方法来源，支持候选模型选择；
- G3：代码阶段不直接复制外部代码，只参考方法描述；
- G4：冻结数字与文献分离，文献不能证明本题结果，只能证明方法合理；
- G5：`claim_evidence_map.md` 中引用类 claim 必须绑定 `literature.md` 条目；
- G6/G7：匿名扫描与提交包卫生按 auto-MM 完整性规则执行。

## 7. 配置模板

当前 skill 另存模板：`templates/paper_search_config.yaml`。默认邮箱已填：

```yaml
openalex:
  email: <your-email@example.com>
anysearch:
  api_key_env: ANYSEARCH_API_KEY
```
