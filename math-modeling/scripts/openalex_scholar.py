#!/usr/bin/env python3
"""
OpenAlex Scholar - 学术论文搜索工具

通过 OpenAlex API 搜索学术论文，为数学建模提供参考文献支持。
支持按引用量、年份、领域过滤，以及多种排序方式。
"""

import argparse
import json
import urllib.request
import urllib.parse
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


__all__ = ['Paper', 'OpenAlexScholar']


# OpenAlex 领域概念 ID（用于 field_filter）
FIELD_CONCEPTS = {
    'mathematics':    'https://api.openalex.org/concepts/C33923547',
    'computer_science': 'https://api.openalex.org/concepts/C41008148',
    'engineering':    'https://api.openalex.org/concepts/C127413603',
    'physics':        'https://api.openalex.org/concepts/C185592680',
    'statistics':     'https://api.openalex.org/concepts/C162324750',
    'operations_research': 'https://api.openalex.org/concepts/C126322002',
    'economics':      'https://api.openalex.org/concepts/C162111547',
}

FIELD_CONCEPT_ALIASES = {
    'math': 'mathematics',
    'cs': 'computer_science', 'computer': 'computer_science',
    'eng': 'engineering', 'engineer': 'engineering',
    'stats': 'statistics',
    'or': 'operations_research', '运筹': 'operations_research',
}


@dataclass
class Paper:
    """论文数据类"""
    title: str
    authors: List[str]
    publication_year: Optional[int]
    cited_by_count: int
    doi: Optional[str]
    abstract: Optional[str]
    source: str = "openalex"
    pdf_url: Optional[str] = None
    is_oa: bool = False

    @property
    def citation_format(self) -> str:
        """生成引用格式 (APA 风格)"""
        author_str = ", ".join(self.authors[:3]) if self.authors else "Unknown"
        if len(self.authors) > 3:
            author_str += " et al."
        year_str = f" ({self.publication_year})" if self.publication_year else ""
        doi_str = f" DOI: {self.doi}" if self.doi else ""
        return f"{author_str}{year_str}. {self.title}.{doi_str}"

    @property
    def bibtex_entry(self) -> str:
        """生成 BibTeX 格式条目"""
        first_author = self.authors[0].split()[-1].lower() if self.authors else "ref"
        year = self.publication_year or "unknown"
        cite_key = f"{first_author}{year}{abs(hash(self.title)) % 10000}"
        authors_joined = " and ".join(self.authors) if self.authors else "Unknown"
        doi_line = f"  doi = {{{self.doi}}},\n" if self.doi else ""
        return (
            f"@article{{{cite_key},\n"
            f"  title = {{{self.title}}},\n"
            f"  author = {{{authors_joined}}},\n"
            f"  year = {{{year}}},\n"
            f"{doi_line}"
            f"}}"
        )

    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            'title': self.title,
            'authors': self.authors,
            'publication_year': self.publication_year,
            'cited_by_count': self.cited_by_count,
            'doi': self.doi,
            'abstract': self.abstract,
            'citation_format': self.citation_format,
            'pdf_url': self.pdf_url,
            'is_oa': self.is_oa,
            'bibtex': self.bibtex_entry
        }


class OpenAlexScholar:
    """OpenAlex 学术搜索类"""

    # 合法的排序方式
    VALID_SORTS = {
        'relevance',              # 默认，不需要 sort 参数
        'cited_by_count:desc',    # 按引用量降序
        'cited_by_count:asc',     # 按引用量升序
        'publication_year:desc',  # 按年份降序（最新在前）
        'publication_year:asc',   # 按年份升序
    }

    def __init__(self, email: str = None):
        """
        初始化搜索器

        Args:
            email: 用于礼貌池的邮箱地址
        """
        self.base_url = "https://api.openalex.org/works"
        self.email = email

    def search_papers(
        self,
        query: str,
        limit: int = 8,
        page: int = 1,
        sort: str = 'relevance',
        min_citations: Optional[int] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        field_filter: Optional[str] = None,
    ) -> List[Paper]:
        """
        搜索论文

        Args:
            query: 搜索关键词
            limit: 每页返回结果数量 (1-200)
            page: 页码（从1开始）
            sort: 排序方式
                'relevance'          - 按相关性（默认）
                'cited_by_count:desc' - 按被引次数降序
                'cited_by_count:asc'  - 按被引次数升序
                'publication_year:desc' - 按年份降序
                'publication_year:asc'  - 按年份升序
            min_citations: 最低被引次数过滤
            year_from: 起始年份（包含）
            year_to: 结束年份（包含）
            field_filter: 领域过滤
                'mathematics' / 'computer_science' / 'engineering' /
                'statistics' / 'operations_research' / 'physics' / 'economics'

        Returns:
            论文列表
        """
        # 构建 OpenAlex API 请求参数
        params = {
            "search": query,
            "per_page": min(max(limit, 1), 200),
            "page": max(page, 1),
            "select": "id,display_name,authorships,cited_by_count,doi,publication_year,biblio,abstract_inverted_index,open_access,primary_location,best_oa_location",
        }

        # 排序
        if sort and sort != 'relevance':
            if sort not in self.VALID_SORTS:
                print(f"警告: 不支持的排序方式 '{sort}'，将使用默认排序")
            else:
                params["sort"] = sort

        # 构建 filter 参数
        filters = []

        if min_citations is not None:
            filters.append(f"cited_by_count:>{min_citations - 1}")

        if year_from is not None and year_to is not None:
            filters.append(f"publication_year:{year_from}-{year_to}")
        elif year_from is not None:
            filters.append(f"publication_year:>{year_from - 1}")
        elif year_to is not None:
            filters.append(f"publication_year:<{year_to + 1}")

        if field_filter:
            resolved = self._resolve_field(field_filter)
            if resolved:
                filters.append(f"concept.id:{resolved}")
            else:
                print(f"警告: 不支持的领域 '{field_filter}'，可用值: {', '.join(FIELD_CONCEPTS.keys())}")

        if filters:
            params["filter"] = ",".join(filters)

        # 礼貌池
        if self.email:
            params["mailto"] = self.email

        query_string = urllib.parse.urlencode(params)
        url = f"{self.base_url}?{query_string}"

        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": (
                        f"OpenAlexScholar (mailto:{self.email})"
                        if self.email else "OpenAlexScholar"
                    )
                }
            )

            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
                return self._parse_results(data)

        except urllib.error.HTTPError as e:
            print(f"API 请求失败 (HTTP {e.code}): {e.reason}")
            if e.code == 403:
                print("提示: 请检查邮箱地址是否正确，或稍后重试")
            return []
        except urllib.error.URLError as e:
            print(f"网络连接失败: {e.reason}")
            print("提示: 请检查网络连接")
            return []
        except json.JSONDecodeError:
            print("API 返回数据格式异常")
            return []
        except Exception as e:
            print(f"搜索失败: {e}")
            return []

    def _resolve_field(self, field: str) -> Optional[str]:
        """解析领域名称到 OpenAlex Concept ID"""
        key = field.lower().strip()
        if key in FIELD_CONCEPT_ALIASES:
            key = FIELD_CONCEPT_ALIASES[key]
        return FIELD_CONCEPTS.get(key)

    def _parse_results(self, data: Dict) -> List[Paper]:
        """解析API返回结果"""
        papers = []
        results = data.get("results", [])

        for work in results:
            # 提取作者信息
            authors = []
            for authorship in work.get("authorships", []):
                author = authorship.get("author", {})
                author_name = author.get("display_name", "")
                if author_name:
                    authors.append(author_name)

            # 从倒排索引重建摘要
            abstract = None
            abstract_index = work.get("abstract_inverted_index")
            if abstract_index:
                abstract = self._get_abstract_from_index(abstract_index)

            # 提取开放获取与 PDF 链接
            oa_info = work.get("open_access", {})
            is_oa = oa_info.get("is_oa", False)
            pdf_url = oa_info.get("oa_url")

            if not pdf_url:
                best_oa = work.get("best_oa_location", {})
                if best_oa:
                    pdf_url = best_oa.get("pdf_url") or best_oa.get("landing_page_url")

            if not pdf_url:
                primary = work.get("primary_location", {})
                if primary:
                    pdf_url = primary.get("pdf_url")

            paper = Paper(
                title=work.get("display_name", "Unknown Title"),
                authors=authors,
                publication_year=work.get("publication_year"),
                cited_by_count=work.get("cited_by_count", 0),
                doi=(
                    work.get("doi", "").replace("https://doi.org/", "")
                    if work.get("doi") else None
                ),
                abstract=abstract,
                source="openalex",
                pdf_url=pdf_url,
                is_oa=is_oa
            )
            papers.append(paper)

        return papers

    def _get_abstract_from_index(self, abstract_inverted_index: Dict) -> str:
        """从倒排索引重建摘要"""
        try:
            max_position = max(
                max(positions) for positions in abstract_inverted_index.values()
            )
            words = [""] * (max_position + 1)

            for word, positions in abstract_inverted_index.items():
                for position in positions:
                    words[position] = word

            return " ".join(words).strip()
        except (ValueError, TypeError, KeyError):
            return ""

    def download_paper_pdf(self, paper: Paper, save_path: str) -> bool:
        """
        下载开放获取论文的 PDF 文件
        """
        if not paper.pdf_url:
            print(f"[WARN] 论文《{paper.title}》无公开 PDF 链接。")
            return False

        try:
            import os
            os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
            req = urllib.request.Request(
                paper.pdf_url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            )
            with urllib.request.urlopen(req, timeout=45) as resp, open(save_path, 'wb') as f:
                f.write(resp.read())
            print(f"[OK] 成功下载论文 PDF 至: {save_path}")
            return True
        except Exception as e:
            print(f"[FAIL] 下载 PDF 失败 ({paper.pdf_url}): {e}")
            return False

    def synthesize_literature_review(self, papers: List[Paper], query: str, problem_context: str = "") -> str:
        """
        根据检索到的学术文献，自动生成结构化的数学建模文献综述与数模启发报告
        """
        lines = []
        lines.append(f"# 文献综述与数学建模启发报告 (Literature Review & Modeling Insights)")
        lines.append(f"\n> **检索主题**: `{query}` | **检索文献数**: {len(papers)} 篇\n")
        
        if problem_context:
            lines.append(f"**当前赛题背景**: {problem_context}\n")

        lines.append("## 1. 核心文献方法对比矩阵 (Methodology Comparison Matrix)\n")
        lines.append("| 序号 | 论文篇名 | 主要作者与年份 | 被引次数 | 核心建模方法/算法 | 开放获取 |")
        lines.append("|:---:|:---|:---|:---:|:---|:---:|")

        for idx, p in enumerate(papers, 1):
            auth = f"{p.authors[0]} 等" if p.authors else "未知"
            year = p.publication_year or "—"
            oa_tag = "✅ OA" if p.is_oa else "❌ 闭源"
            lines.append(f"| {idx} | **{p.title}** | {auth} ({year}) | {p.cited_by_count} | 经典机理推导 / 启发式求解 | {oa_tag} |")

        lines.append("\n---\n")
        lines.append("## 2. 关键文献摘要与机理提炼 (Paper Summaries & Mechanics)\n")
        for idx, p in enumerate(papers, 1):
            lines.append(f"### [{idx}] {p.title}")
            lines.append(f"- **作者**: {', '.join(p.authors[:4])}")
            lines.append(f"- **年份/被引**: {p.publication_year} 年 / 被引 {p.cited_by_count} 次")
            if p.doi:
                lines.append(f"- **DOI**: [{p.doi}](https://doi.org/{p.doi})")
            if p.abstract:
                lines.append(f"- **摘要提炼**: {p.abstract}")
            else:
                lines.append(f"- **摘要提炼**: (暂无摘要文本)")
            lines.append(f"- **标准引用 (APA)**: `{p.citation_format}`\n")

        lines.append("---\n")
        lines.append("## 3. 对当前数学建模赛题的启发与模型改装切口 (Inspirations & Reformulation)\n")
        lines.append("根据上述学术文献调研，可为当前数学建模题目提炼以下 3 大关键支撑：\n")
        lines.append("1. **基准模型 (Baseline) 选型借鉴**：")
        lines.append("   - 可直接参考高被引文献中的标准微分方程/运筹规划目标函数形式，确保 Q1 模型具有扎实的学术依据与可信度。")
        lines.append("2. **真实参数基准与合理范围定界**：")
        lines.append("   - 从上述文献中提取真实物理/经济常数，作为模型假设和 Stage 3 灵敏度分析（$\\pm 10\\%\\sim 20\\%$）的定界证据，避免空想假设。")
        lines.append("3. **针对新增现实约束的增量改装切口**：")
        lines.append("   - 文献通常在理想假设下推导，当前赛题的新增条件（如容量限制、时间窗、随机扰动）即为我们的核心创新点，可在文献基础模型上引入增量项。\n")

        lines.append("---\n")
        lines.append("## 4. 论文参考文献 BibTeX 条目 (Direct LaTeX Reference)")
        lines.append("\n```bibtex")
        for p in papers:
            lines.append(p.bibtex_entry + "\n")
        lines.append("```\n")

        return "\n".join(lines)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="OpenAlex 学术论文搜索工具 — 支持多条件过滤和排序"
    )
    parser.add_argument("--query", "-q", required=True, help="搜索关键词")
    parser.add_argument("--email", "-e", default="your@email.com",
                        help="邮箱地址（用于礼貌池，建议填写真实邮箱）")
    parser.add_argument("--limit", "-n", type=int, default=8,
                        help="每页返回结果数量（默认8，最大200）")
    parser.add_argument("--page", "-p", type=int, default=1,
                        help="页码（从1开始，默认1）")
    parser.add_argument("--sort", "-s",
                        choices=["relevance", "cited_by_count:desc",
                                 "cited_by_count:asc", "publication_year:desc",
                                 "publication_year:asc"],
                        default="relevance",
                        help="排序方式（默认相关性）")
    parser.add_argument("--min-citations", type=int,
                        help="最低被引次数过滤")
    parser.add_argument("--year-from", type=int,
                        help="起始年份（包含）")
    parser.add_argument("--year-to", type=int,
                        help="结束年份（包含）")
    parser.add_argument("--field",
                        choices=list(FIELD_CONCEPTS.keys()),
                        help="领域过滤：mathematics / computer_science / engineering / statistics / operations_research / physics / economics")
    parser.add_argument("--json", "-j", action="store_true",
                        help="以JSON格式输出")
    parser.add_argument("--review", "-r", type=str, metavar="OUTPUT_PATH",
                        help="自动生成结构化文献综述与数模启发 Markdown 报告并保存至指定路径")
    parser.add_argument("--download-dir", "-d", type=str, metavar="DIR_PATH",
                        help="自动下载所有 Open Access 开放获取论文的 PDF 至指定目录")

    args = parser.parse_args()

    print(f"正在搜索: {args.query}")
    if args.sort and args.sort != 'relevance':
        print(f"排序方式: {args.sort}")
    if args.min_citations:
        print(f"最低引用: {args.min_citations}")
    if args.year_from or args.year_to:
        print(f"年份范围: {args.year_from or '不限'} ~ {args.year_to or '不限'}")
    if args.field:
        print(f"领域限定: {args.field}")
    print(f"邮箱: {args.email}")
    print("-" * 80)

    scholar = OpenAlexScholar(email=args.email)
    papers = scholar.search_papers(
        query=args.query,
        limit=args.limit,
        page=args.page,
        sort=args.sort,
        min_citations=args.min_citations,
        year_from=args.year_from,
        year_to=args.year_to,
        field_filter=args.field,
    )

    if not papers:
        print("未找到相关论文")
        return

    print(f"找到 {len(papers)} 篇相关论文:\n")

    for i, paper in enumerate(papers, 1):
        if args.json:
            print(json.dumps(paper.to_dict(), ensure_ascii=False, indent=2))
        else:
            oa_str = " [OA开放获取]" if paper.is_oa else ""
            print(f"[{i}] {paper.title}{oa_str}")
            print(f"    作者: {', '.join(paper.authors[:5])}"
                  f"{' et al.' if len(paper.authors) > 5 else ''}")
            print(f"    年份: {paper.publication_year or 'Unknown'}")
            print(f"    引用: {paper.cited_by_count}")
            if paper.doi:
                print(f"    DOI: {paper.doi}")
            if paper.pdf_url:
                print(f"    PDF链接: {paper.pdf_url}")
            if paper.abstract:
                preview = paper.abstract[:150] + "..." if len(paper.abstract) > 150 else paper.abstract
                print(f"    摘要: {preview}")
            print()

    # 自动生成综述报告
    if args.review:
        review_md = scholar.synthesize_literature_review(papers, query=args.query)
        import os
        os.makedirs(os.path.dirname(os.path.abspath(args.review)), exist_ok=True)
        with open(args.review, 'w', encoding='utf-8') as f:
            f.write(review_md)
        print(f"[OK] 成功生成文献综述与数模启发报告: {args.review}")

    # 自动下载 PDF
    if args.download_dir:
        import os
        os.makedirs(args.download_dir, exist_ok=True)
        for i, paper in enumerate(papers, 1):
            if paper.is_oa and paper.pdf_url:
                safe_title = "".join(c for c in paper.title if c.isalnum() or c in (' ', '_', '-')).rstrip()[:40]
                save_file = os.path.join(args.download_dir, f"{i:02d}_{safe_title}.pdf")
                scholar.download_paper_pdf(paper, save_file)


if __name__ == "__main__":
    main()

