#!/usr/bin/env python3
"""
Math Modeling Skill - 极简交互式快速启动向导 (Interactive Quickstart CLI)

为参赛选手和学习者提供终端可视化操作菜单，支持一键执行：
1. [选题] 赛题初筛与 4 维度量化评分
2. [检索] 学术文献检索、OA PDF 下载与综述合成
3. [审计] 自动化问题初步分析与设问递进图生成
4. [求解] 经典机理推导与 Python 算法模板运行
5. [验证] 同口径对比、参数弹性分析与数字冻结
6. [论文] LaTeX 论文模板编译与摘要生成
7. [封箱] 干净环境一键复跑测试与支撑材料打包
"""

import os
import sys
import argparse

# 添加 scripts 目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)

from math_modeling_utils import AHPTool, GameTheoryTool, StatisticsTool, CompositionalDataTool, OptimizationLinearizer
from openalex_scholar import OpenAlexScholar
from auto_problem_audit import AutoProblemAuditor


def print_banner():
    print("=" * 75)
    print("   Math Modeling Skill - 人机协同全真攻坚系统 (Interactive CLI)   ")
    print("   支持 CUMCM 国赛 / MCM 美赛 / MathorCup / APMCM / 研赛全流程攻坚   ")
    print("=" * 75)


def show_menu():
    print("\n[请选择需要执行的数学建模工作阶段 (支持单步按需执行)]:")
    print("  1. 🎯 [选题] 赛题初筛与量化决策表生成 (/topic)")
    print("  2. 🔍 [检索] 学术文献检索、下载与综述生成 (/search)")
    print("  3. 📋 [审计] 自动化问题拆解、递进图与参考文献库构建 (/audit)")
    print("  4. 💻 [求解] 经典算法工具箱与求解模板 (/solve)")
    print("  5. 📊 [验证] 参数弹性灵敏度分析与数字冻结 (/validate)")
    print("  6. 📝 [论文] LaTeX 论文模板与三段式摘要生成 (/paper)")
    print("  7. 📦 [封箱] 独立复现测试与支撑材料打包 (/pack)")
    print("  0. 退出向导")
    print("-" * 75)


def handle_search():
    query = input("\n请输入需要检索的学术文献关键词 (如: traffic flow shock wave): ").strip()
    if not query:
        print("[WARN] 关键词不能为空")
        return
    limit = input("请输入检索篇数 (默认 5): ").strip()
    limit = int(limit) if limit.isdigit() else 5
    
    scholar = OpenAlexScholar()
    papers = scholar.search_papers(query=query, limit=limit, sort="cited_by_count:desc")
    if not papers:
        print("[INFO] 未检索到相关文献。")
        return
    
    print(f"\n[OK] 成功检索到 {len(papers)} 篇权威文献:")
    for idx, p in enumerate(papers, 1):
        print(f"[{idx}] {p.title} ({p.publication_year}) | 被引: {p.cited_by_count}")
        print(f"    引用: {p.citation_format}")
    
    gen_rev = input("\n是否自动生成《文献综述与数模启发报告》(docs/literature_review.md)? (y/n, 默认 y): ").strip().lower()
    if gen_rev != 'n':
        report = scholar.synthesize_literature_review(papers, query=query)
        os.makedirs("docs", exist_ok=True)
        with open("docs/literature_review.md", "w", encoding="utf-8") as f:
            f.write(report)
        print("[OK] 已生成: docs/literature_review.md")


def handle_audit():
    title = input("\n请输入赛题标题: ").strip() or "数学建模赛题"
    desc = input("请输入赛题简述背景: ").strip() or "关于系统优化与决策建模"
    kw = input("请输入用于检索文献的核心关键词 (逗号隔开): ").strip()
    keywords = [k.strip() for k in kw.split(",") if k.strip()] if kw else ["optimization modeling"]
    
    auditor = AutoProblemAuditor(workspace_dir=".")
    res = auditor.run_auto_audit(
        problem_title=title,
        problem_description=desc,
        search_keywords=keywords,
        questions=[
            {"id": "问题1", "target": "基准方案求解与指标测算", "inputs": "附件数据", "constraints": "基础物理守恒", "model_type": "经典可解释基准模型 (Baseline)"},
            {"id": "问题2", "target": "新增现实约束下的增量模型改装", "inputs": "变化条件", "constraints": "非线性/容量限制", "model_type": "精确数学规划 (MILP/MINLP)"},
            {"id": "问题3", "target": "综合效益评价与决策策略体系", "inputs": "前两问结果", "constraints": "多主体协同", "model_type": "多目标优化 / 综合决策体系"}
        ],
        download_papers=False,
        max_papers=3
    )
    print("\n" + res["cp1_card"])


def handle_solve():
    print("\n[数学建模经典算法工具箱快捷入口]:")
    print("  a. 层次分析法 (AHP 特征值法与一致性检验)")
    print("  b. 合作博弈 Shapley 利益分配计算")
    print("  c. 成分数据 CLR 对数比流形转换")
    print("  d. 超产降价优化分段函数精确线性化规范")
    choice = input("请选择工具 (a/b/c/d): ").strip().lower()
    if choice == 'a':
        import numpy as np
        mat = np.array([[1, 2, 5], [1/2, 1, 3], [1/5, 1/3, 1]])
        w, cr, is_pass = AHPTool.eigenvalue_method(mat)
    elif choice == 'b':
        def v_demo(s):
            return 100 if len(s) == 3 else (60 if len(s) == 2 else 20)
        GameTheoryTool.shapley_value(3, v_demo)
    elif choice == 'c':
        import numpy as np
        d = np.array([[20.0, 30.0, 50.0]])
        clr = CompositionalDataTool.clr_transform(d)
        inv = CompositionalDataTool.inv_clr_transform(clr)
        print("  原始数据:", d)
        print("  CLR空间:", clr)
        print("  逆变换恢复:", inv)
    elif choice == 'd':
        OptimizationLinearizer.explain_overproduction_linearization()


def main():
    print_banner()
    while True:
        show_menu()
        choice = input("请输入选项编号 (0-7): ").strip()
        if choice == '0':
            print("\n感谢使用 Math Modeling Skill！祝竞赛取得优异成绩！\n")
            break
        elif choice == '1':
            print("\n[提示] 请阅读 stages/00_topic.md 并在对局中发送 /topic 启动量化选题！")
        elif choice == '2':
            handle_search()
        elif choice == '3':
            handle_audit()
        elif choice == '4':
            handle_solve()
        elif choice == '5':
            print("\n[提示] 参数弹性计算公式: S = (x/y)*(dy/dx)，详见 stages/03_validate.md")
        elif choice == '6':
            print("\n[提示] LaTeX 论文模板位于 templates/latex_template_cn.tex，详见 stages/04_paper.md")
        elif choice == '7':
            print("\n[提示] 封箱前请执行全量复跑与匿名扫描，详见 stages/05_pack.md")
        else:
            print("[WARN] 无效选项，请重新输入。")


if __name__ == "__main__":
    main()
