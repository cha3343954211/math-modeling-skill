#!/usr/bin/env python3
"""
Auto Problem Audit & Literature Harvesting Tool (自动化问题初步分析与文献归档工具)

全自动执行：
1. 赛题文本解析与子问题要素拆解
2. 自动化前沿文献检索与 Open Access PDF 下载
3. 创建并维护独立的参考文献文件夹 (`docs/references/`) 与 `references.bib`
4. 自动生成《问题规格说明书》(docs/problem_spec.md) 与《文献综述及数模启发》(docs/literature_review.md)
5. 自动输出 CP1 人机协同审批卡
"""

import os
import sys
import json
import argparse
from typing import List, Dict, Optional

# 引入 openalex 学术检索工具
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from openalex_scholar import OpenAlexScholar, Paper


class AutoProblemAuditor:
    """自动化问题分析与文献收集器"""

    def __init__(self, workspace_dir: str = "."):
        self.workspace_dir = os.path.abspath(workspace_dir)
        self.docs_dir = os.path.join(self.workspace_dir, "docs")
        self.ref_dir = os.path.join(self.docs_dir, "references")
        self.papers_dir = os.path.join(self.ref_dir, "papers")
        self.scholar = OpenAlexScholar()

        # 创建目录结构
        os.makedirs(self.docs_dir, exist_ok=True)
        os.makedirs(self.ref_dir, exist_ok=True)
        os.makedirs(self.papers_dir, exist_ok=True)

    def run_auto_audit(
        self,
        problem_title: str,
        problem_description: str,
        search_keywords: List[str],
        questions: List[Dict[str, str]],
        download_papers: bool = True,
        max_papers: int = 5
    ) -> Dict[str, str]:
        """
        全自动执行问题分析、文献检索、综述合成与文件落盘
        """
        print(f"[INFO] 正在启动问题初步自动化分析: 《{problem_title}》...")
        
        # 1. 检索文献并自动落盘至 references/
        all_papers: List[Paper] = []
        for kw in search_keywords:
            print(f"[INFO] 正在检索学术文献: '{kw}'...")
            papers = self.scholar.search_papers(
                query=kw,
                limit=max_papers,
                sort="cited_by_count:desc"
            )
            all_papers.extend(papers)

        # 简单按 DOI/Title 去重
        unique_papers = []
        seen_titles = set()
        for p in all_papers:
            clean_t = p.title.strip().lower()
            if clean_t not in seen_titles:
                seen_titles.add(clean_t)
                unique_papers.append(p)

        unique_papers = unique_papers[:max_papers]
        print(f"[OK] 成功检索到 {len(unique_papers)} 篇高相关权威文献。")

        # 2. 下载开放获取 (OA) PDF
        downloaded_count = 0
        if download_papers:
            for idx, p in enumerate(unique_papers, 1):
                if p.is_oa and p.pdf_url:
                    first_auth = p.authors[0].split()[-1] if p.authors else "Ref"
                    year = p.publication_year or "unknown"
                    safe_name = f"{idx:02d}_{first_auth}_{year}.pdf"
                    save_path = os.path.join(self.papers_dir, safe_name)
                    if self.scholar.download_paper_pdf(p, save_path):
                        downloaded_count += 1

        # 3. 自动生成 references.bib
        bib_file = os.path.join(self.ref_dir, "references.bib")
        with open(bib_file, "w", encoding="utf-8") as f:
            for p in unique_papers:
                f.write(p.bibtex_entry + "\n\n")
        print(f"[OK] 已更新参考文献数据库: {bib_file}")

        # 4. 自动生成文献综述与数模启发 docs/literature_review.md
        review_md = self.scholar.synthesize_literature_review(
            papers=unique_papers,
            query=", ".join(search_keywords),
            problem_context=f"{problem_title} —— {problem_description[:200]}..."
        )
        review_file = os.path.join(self.docs_dir, "literature_review.md")
        with open(review_file, "w", encoding="utf-8") as f:
            f.write(review_md)
        print(f"[OK] 已生成文献综述与启发报告: {review_file}")

        # 5. 自动生成问题规格说明书 docs/problem_spec.md
        spec_md = self._generate_problem_spec(
            problem_title=problem_title,
            problem_description=problem_description,
            questions=questions,
            papers=unique_papers
        )
        spec_file = os.path.join(self.docs_dir, "problem_spec.md")
        with open(spec_file, "w", encoding="utf-8") as f:
            f.write(spec_md)
        print(f"[OK] 已生成问题规格说明书与设问递进图: {spec_file}")

        # 6. 生成 CP1 审批卡文本
        cp1_card = self._generate_cp1_card(
            problem_title=problem_title,
            questions=questions,
            papers_count=len(unique_papers),
            downloaded_count=downloaded_count
        )

        return {
            "spec_file": spec_file,
            "review_file": review_file,
            "bib_file": bib_file,
            "papers_dir": self.papers_dir,
            "cp1_card": cp1_card
        }

    def _generate_problem_spec(
        self,
        problem_title: str,
        problem_description: str,
        questions: List[Dict[str, str]],
        papers: List[Paper]
    ) -> str:
        """生成标准化 problem_spec.md"""
        lines = []
        lines.append(f"# 问题规格说明书与设问递进分析 (Problem Specification)\n")
        lines.append(f"> **题目**: {problem_title}\n")
        lines.append(f"## 1. 题目背景与核心目标\n{problem_description}\n")
        
        lines.append("## 2. 子问题要素拆解与建模映射 (Question Breakdown)\n")
        lines.append("| 子问题 | 目标与核心输出 | 输入已知量与数据 | 约束条件 | 初选模型类型与文献借鉴 |")
        lines.append("|:---|:---|:---|:---|:---|")
        
        for q in questions:
            qid = q.get("id", "Q")
            target = q.get("target", "求解最优化目标")
            inputs = q.get("inputs", "附件数据及题干参数")
            constraints = q.get("constraints", "物理守恒 / 容量限制 / 时间窗")
            model_type = q.get("model_type", "机理微分方程 / 运筹规划")
            lines.append(f"| **{qid}** | {target} | {inputs} | {constraints} | {model_type} |")

        lines.append("\n## 3. 设问递进关系图 (Question Progression Map)\n")
        lines.append("```mermaid")
        lines.append("graph LR")
        lines.append("    Q1[\"Q1: 基础层 (经典参照 / Baseline)\"] -->|\"引入新增现实条件 / 容量上限\"| Q2[\"Q2: 变化层 (增量改装模型)\"]")
        lines.append("    Q2 -->|\"综合Q1/Q2结论 / 多目标评价\"| Q3[\"Q3: 决策层 (多情景策略 / 建议体系)\"]")
        lines.append("```\n")

        lines.append("## 4. 参考文献与前沿启发依据\n")
        lines.append(f"本分析已自动关联 `docs/references/` 中的 {len(papers)} 篇权威文献：\n")
        for idx, p in enumerate(papers, 1):
            lines.append(f"- [{idx}] {p.citation_format} (详见 `docs/literature_review.md`)")

        return "\n".join(lines)

    def _generate_cp1_card(
        self,
        problem_title: str,
        questions: List[Dict[str, str]],
        papers_count: int,
        downloaded_count: int
    ) -> str:
        """生成 CP1 人机协同审批卡"""
        card = [
            "---",
            "### [CHECKPOINT 1: 数据审计、符号系统与假设清单] 人机协同审批卡",
            "",
            "**1. 自动化分析产出汇报：**",
            f"- 问题规格说明书：已生成 `docs/problem_spec.md` (拆解了 {len(questions)} 个子问题并绘制设问递进图)",
            f"- 参考文献库：已在 `docs/references/` 归档 {papers_count} 篇权威文献，成功下载 {downloaded_count} 篇 OA PDF 全文",
            "- 文献综述与启发：已生成 `docs/literature_review.md`，提取了基准模型与真实参数定界范围",
            "- 引用数据库：已自动生成 `docs/references/references.bib`，可直接供 LaTeX 引用",
            "",
            "**2. 子问题递进主线：**"
        ]
        for q in questions:
            card.append(f"- **{q.get('id', 'Q')}**: {q.get('target', '')} -> 初选【{q.get('model_type', '')}】")

        card.extend([
            "",
            "**3. 待人类决策确认 (Decisions Needed)：**",
            "- [ ] 审阅 `docs/problem_spec.md` 中的设问递进逻辑与变量继承是否合理？",
            "- [ ] 确认是否同意文献综述提取的基准参数范围，是否批准进入 Stage 2 进行公式推导？",
            "",
            "**4. 您可以执行的操作：**",
            "- 输入 `/approve`：审批通过，立即进入 Stage 2 开始核心建模与求解代码编写。",
            "- 输入 `/revise assumption [内容]`：修改或放宽特定假设。",
            "- 输入 `/search [新关键词]`：补充检索特定领域的其他参考文献。",
            "---"
        ])
        return "\n".join(card)


if __name__ == "__main__":
    # 示例测试运行
    auditor = AutoProblemAuditor(workspace_dir=".")
    res = auditor.run_auto_audit(
        problem_title="城市应急救援车辆动态调度与路径优化",
        problem_description="在突发公共事件下，考虑道路通行能力下降、次生灾害风险与受灾点需求不确定性，建立多阶段应急救援车辆调度与路径优化模型。",
        search_keywords=["emergency vehicle routing optimization", "dynamic traffic disaster dispatching"],
        questions=[
            {"id": "问题1", "target": "确定静态最优配送路径与基准总耗时", "inputs": "路网距离矩阵、各点需求量", "constraints": "载重约束、单次配送", "model_type": "混合整数线性规划 (MILP Baseline)"},
            {"id": "问题2", "target": "应对道路受阻与动态需求的新增路径规划", "inputs": "时变路段通行时间、随机需求", "constraints": "动态时间窗、道路通行概率", "model_type": "随机动态规划 / 鲁棒优化"},
            {"id": "问题3", "target": "多救援中心协同调度与综合效益评价", "inputs": "多中心库存、救援紧迫度", "constraints": "多主体协同、公平性", "model_type": "多目标规划 + TOPSIS综合评价"}
        ],
        download_papers=False,
        max_papers=3
    )
    print("\n[SUCCESS] 自动化问题初步分析演示完成！")
    print(res["cp1_card"])

