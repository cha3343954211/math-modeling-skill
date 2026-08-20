# 搜索与文献资料调研指南 (Search & Scholar)

> **功能定位**：贯穿数学建模全流程的“信息侦察机”。解决赛题背景陌生、缺乏物理/行业常识、参数取值无依据、模型缺乏文献背书等痛点。支持随时独立调用 `/search` 或 `/scholar` 进行学术论文检索、参数定界与 BibTeX 引用生成。

---

## 1. 核心搜索应用场景

| 阶段 | 搜索目标 | 核心产出 | 推荐渠道与工具 |
|------|---------|---------|--------------|
| **选题前后** | 行业背景常识、物理/生物机理法则 | 明确赛题现实意义与约束来源 | 学术搜索引擎、专业百科、行业国家标准 |
| **方案选型** | 同类赛题高分论文、领域经典权威算法 | 确定 Baseline 与主模型架构 | OpenAlex、知网 (CNKI)、Google Scholar、arXiv |
| **参数定界** | 真实物理常数、经济参数合理波动范围 | 为假设和灵敏度分析（$\pm 10\%\sim 20\%$）提供文献依据 | 统计年鉴、行业技术手册、学术文献 |
| **论文排版** | 标准学术引用格式 (APA / GB/T 7714 / BibTeX) | 生成论文末尾的规范参考文献列表 | `scripts/openalex_scholar.py` / `scripts/hybrid_scholar.py` |

---

## 2. 内置学术检索工具使用方法

本 Skill 内置了免 API Key 的学术文献检索工具箱：

### 2.1 命令行检索、下载 PDF 与一键生成综述报告
```bash
# 1. 搜索高被引论文并自动生成《文献综述与数模启发报告》
python scripts/openalex_scholar.py --query "traffic flow shock wave modeling" --sort cited_by_count:desc --limit 5 --review docs/literature_review.md

# 2. 搜索并自动下载所有 Open Access 开放获取的 PDF 全文到本地
python scripts/openalex_scholar.py --query "battery thermal management" --field physics --year-start 2020 --download-dir data/papers/
```

### 2.2 Python 代码中直接调用
```python
from openalex_scholar import OpenAlexScholar

scholar = OpenAlexScholar()
papers = scholar.search_papers("supply chain inventory optimization EOQ", limit=5, sort="cited_by_count:desc")

# 1. 自动生成包含方法矩阵、参数定界与赛题启发的综述报告
review_report = scholar.synthesize_literature_review(
    papers,
    query="供应链库存优化与EOQ模型",
    problem_context="某制造企业在需求随机波动下的多级库存协同优化"
)
with open("docs/literature_review.md", "w", encoding="utf-8") as f:
    f.write(review_report)

# 2. 批量下载开放获取 PDF 全文
for paper in papers:
    if paper.is_oa and paper.pdf_url:
        scholar.download_paper_pdf(paper, f"data/papers/{paper.doi.replace('/', '_')}.pdf")
```

---

## 3. 搜索资料的高分原则与避坑红线

1. **拒绝胡编参数范围**：
   - 灵敏度分析中，不能随意假设“参数 A 上下浮动 50%”；必须通过文献搜索指明：“*根据文献[3]统计，该地区降雨流失系数通常介于 0.15~0.25 之间*”。
2. **拒绝盲目搬运不可复现的庞大模型**：
   - 检索到复杂的深度神经网络时，必须先评估是否有足够数据训练；小数据赛题优先采用经典可解释模型。
3. **严格遵守学术引用规范**：
   - 凡是引入前人公式、行业常数、已证明定理，正文必须打上角标 `[1]`并在文末列出完整作者、篇名、期刊、年份。
4. **全真竞赛纪律红线**：
   - 比赛期间**严禁在外部论坛、社交平台发帖求助或购买答案**；检索仅限于查阅公开已发表的学术文献、开源文档与官方公开数据集。
