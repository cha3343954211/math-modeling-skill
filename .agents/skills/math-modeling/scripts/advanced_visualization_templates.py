"""
高级可视化模板库 - 数学建模国一/O奖级图表
包含：3D曲面图、Pareto前沿、Tornado灵敏度图、蒙特卡洛分布图、
      雷达图、热力图聚类、网络图、时间演化图等。

使用方式：在项目代码中 import 并调用对应函数。
所有图表默认 plt.savefig() + plt.close()，不打开窗口。
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib import font_manager
import os

# === 中文字体设置 ===
_FONT_CANDIDATES = [
    r'C:/Windows/Fonts/msyh.ttc',
    r'C:/Windows/Fonts/simhei.ttf',
    r'C:/Windows/Fonts/NotoSansSC-VF.ttf',
    r'C:/Windows/Fonts/simsun.ttc',
]
for _font_path in _FONT_CANDIDATES:
    if Path(_font_path).exists():
        font_manager.fontManager.addfont(_font_path)
        _font_name = font_manager.FontProperties(fname=_font_path).get_name()
        plt.rcParams['font.sans-serif'] = [_font_name, 'DejaVu Sans']
        break
plt.rcParams['axes.unicode_minus'] = False


def plot_3d_surface(X, Y, Z, xlabel='参数1', ylabel='参数2', zlabel='目标值',
                    title='目标函数3D地形图', output_path='3d_surface.png', cmap='viridis'):
    """3D曲面图 - 适用于优化问题的目标函数地形展示"""
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap=cmap, alpha=0.85, edgecolor='none')
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_zlabel(zlabel, fontsize=11)
    ax.set_title(title, fontsize=14)
    fig.colorbar(surf, shrink=0.5, aspect=10)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] 3D曲面图已保存: {output_path}")


def plot_pareto_front(f1_all, f2_all, f1_pareto, f2_pareto,
                      xlabel='目标1', ylabel='目标2',
                      title='Pareto前沿', output_path='pareto_front.png'):
    """Pareto前沿图 - 适用于多目标优化"""
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.scatter(f1_all, f2_all, c='steelblue', alpha=0.3, s=20, label='可行解')
    ax.scatter(f1_pareto, f2_pareto, c='red', s=80, marker='*',
               label='Pareto最优解', zorder=5, edgecolors='darkred')
    # 连接Pareto点
    sorted_idx = np.argsort(f1_pareto)
    ax.plot(np.array(f1_pareto)[sorted_idx], np.array(f2_pareto)[sorted_idx],
            'r--', alpha=0.6, linewidth=1.5)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Pareto前沿图已保存: {output_path}")


def plot_tornado(params, effects, title='参数灵敏度Tornado图',
                 output_path='tornado_sensitivity.png', color='coral'):
    """Tornado灵敏度图 - 展示参数影响排序"""
    sorted_data = sorted(zip(params, effects), key=lambda x: abs(x[1]))
    sorted_params = [d[0] for d in sorted_data]
    sorted_effects = [d[1] for d in sorted_data]
    colors = ['#e74c3c' if e > 0 else '#3498db' for e in sorted_effects]

    fig, ax = plt.subplots(figsize=(10, max(6, len(params)*0.8)))
    bars = ax.barh(sorted_params, sorted_effects, color=colors, height=0.6, edgecolor='white')
    ax.set_xlabel('对输出的影响程度', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.axvline(x=0, color='black', linewidth=0.8)
    ax.grid(axis='x', alpha=0.3)
    # 添加数值标签
    for bar, val in zip(bars, sorted_effects):
        ax.text(bar.get_width() + 0.01 * max(abs(e) for e in effects),
                bar.get_y() + bar.get_height()/2,
                f'{val:.4f}', va='center', fontsize=9)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Tornado图已保存: {output_path}")


def plot_monte_carlo_distribution(mc_results, true_value=None,
                                   title='蒙特卡洛不确定性传播',
                                   output_path='mc_distribution.png'):
    """蒙特卡洛分布图 - 展示不确定性传播结果"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 左：分布直方图 + 置信区间
    axes[0].hist(mc_results, bins=50, density=True, alpha=0.7, color='steelblue',
                 edgecolor='white', label='模拟分布')
    ci_low = np.percentile(mc_results, 2.5)
    ci_high = np.percentile(mc_results, 97.5)
    axes[0].axvline(ci_low, color='red', linestyle='--', linewidth=2, label=f'95%CI: [{ci_low:.2f}, {ci_high:.2f}]')
    axes[0].axvline(ci_high, color='red', linestyle='--', linewidth=2)
    axes[0].axvline(np.mean(mc_results), color='green', linestyle='-', linewidth=2, label=f'均值: {np.mean(mc_results):.2f}')
    if true_value is not None:
        axes[0].axvline(true_value, color='orange', linestyle=':', linewidth=2, label=f'确定性值: {true_value:.2f}')
    axes[0].set_xlabel('输出结果', fontsize=12)
    axes[0].set_ylabel('概率密度', fontsize=12)
    axes[0].legend(fontsize=9)
    axes[0].set_title('结果分布', fontsize=13)

    # 右：统计信息文本框
    stats_text = (
        f"模拟次数: {len(mc_results):,}\n"
        f"均值: {np.mean(mc_results):.4f}\n"
        f"标准差: {np.std(mc_results):.4f}\n"
        f"变异系数(CV): {np.std(mc_results)/np.mean(mc_results)*100:.2f}%\n"
        f"95%置信区间: [{ci_low:.4f}, {ci_high:.4f}]\n"
        f"区间宽度: {ci_high - ci_low:.4f}\n"
    )
    if true_value is not None:
        stats_text += f"确定性值: {true_value:.4f}\n"
        stats_text += f"偏差: {abs(np.mean(mc_results) - true_value):.4f}\n"

    axes[1].text(0.1, 0.5, stats_text, transform=axes[1].transAxes,
                 fontsize=12, verticalalignment='center',
                 fontfamily='monospace',
                 bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    axes[1].set_xlim(0, 1)
    axes[1].set_ylim(0, 1)
    axes[1].axis('off')
    axes[1].set_title('统计摘要', fontsize=13)

    fig.suptitle(title, fontsize=15, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] 蒙特卡洛分布图已保存: {output_path}")


def plot_radar(categories, *datasets, labels=None, title='多维评价雷达图',
               output_path='radar_comparison.png', colors=None):
    """
    雷达图 - 适用于多维评价模型对比
    datasets: 每个数据集是一个与categories等长的数值列表
    """
    n_vars = len(categories)
    angles = np.linspace(0, 2 * np.pi, n_vars, endpoint=False).tolist()
    angles += angles[:1]

    if labels is None:
        labels = [f'模型{i+1}' for i in range(len(datasets))]
    if colors is None:
        colors = plt.cm.Set2(np.linspace(0, 1, len(datasets)))

    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))

    for i, data in enumerate(datasets):
        values = list(data) + [data[0]]
        ax.fill(angles, values, alpha=0.15, color=colors[i])
        ax.plot(angles, values, 'o-', linewidth=2, color=colors[i],
                label=labels[i], markersize=6)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11)
    ax.set_ylim(0, 1)
    ax.set_title(title, fontsize=14, pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] 雷达图已保存: {output_path}")


def plot_sensitivity_heatmap(param1_range, param2_range, result_matrix,
                              xlabel='参数1', ylabel='参数2',
                              title='双参数灵敏度热力图',
                              output_path='sensitivity_heatmap.png'):
    """双参数灵敏度热力图 - 展示两参数同时变化对结果的影响"""
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(result_matrix, cmap='RdYlBu_r', aspect='auto',
                    extent=[param1_range[0], param1_range[-1],
                            param2_range[0], param2_range[-1]],
                    origin='lower')
    fig.colorbar(im, ax=ax, label='目标函数值')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14)

    # 添加等高线
    X, Y = np.meshgrid(param1_range, param2_range)
    contours = ax.contour(X, Y, result_matrix, colors='black', linewidths=0.5, alpha=0.5)
    ax.clabel(contours, inline=True, fontsize=8, fmt='%.2f')

    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] 灵敏度热力图已保存: {output_path}")


def plot_ablation_bar(modules, full_metric, ablated_metrics, metric_name='MAPE(%)',
                      title='消融实验结果', output_path='ablation_study.png'):
    """消融实验柱状图 - 展示各模块贡献"""
    fig, ax = plt.subplots(figsize=(10, 6))

    all_labels = ['完整模型'] + [f'去掉{m}' for m in modules]
    all_values = [full_metric] + ablated_metrics
    colors = ['#2ecc71'] + ['#e74c3c'] * len(modules)

    bars = ax.bar(all_labels, all_values, color=colors, edgecolor='white', width=0.6)
    ax.axhline(y=full_metric, color='green', linestyle='--', alpha=0.5, label=f'完整模型: {full_metric:.2f}')

    # 添加数值标签
    for bar, val in zip(bars, all_values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f'{val:.2f}', ha='center', fontsize=11, fontweight='bold')

    # 添加贡献度标注
    for i, (module, ablated_val) in enumerate(zip(modules, ablated_metrics)):
        delta = ablated_val - full_metric
        ax.annotate(f'Δ={delta:+.2f}',
                    xy=(i+1, ablated_val),
                    xytext=(i+1, ablated_val + max(all_values)*0.05),
                    ha='center', fontsize=9, color='darkred',
                    arrowprops=dict(arrowstyle='->', color='darkred'))

    ax.set_ylabel(metric_name, fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.grid(axis='y', alpha=0.3)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] 消融实验图已保存: {output_path}")


def plot_network(nodes, edges, weights=None, node_labels=None,
                 title='网络关系图', output_path='network_graph.png',
                 layout='spring'):
    """网络关系图 - 适用于图论/关联分析"""
    import networkx as nx
    G = nx.Graph()
    G.add_nodes_from(nodes)
    if weights:
        for (u, v), w in zip(edges, weights):
            G.add_edge(u, v, weight=w)
    else:
        G.add_edges_from(edges)

    if layout == 'spring':
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
    elif layout == 'circular':
        pos = nx.circular_layout(G)
    elif layout == 'kamada_kawai':
        pos = nx.kamada_kawai_layout(G)
    else:
        pos = nx.spring_layout(G)

    fig, ax = plt.subplots(figsize=(12, 10))

    # 节点大小基于度数
    degrees = dict(G.degree())
    node_sizes = [300 + 200 * degrees.get(n, 0) for n in G.nodes()]

    # 节点颜色基于度数
    node_colors = [degrees.get(n, 0) for n in G.nodes()]

    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors,
                           cmap='YlOrRd', alpha=0.8, ax=ax)

    if weights:
        edge_widths = [w * 2 / max(weights) for w in weights]
        nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.5, ax=ax)
        edge_labels = {(u, v): f'{w:.2f}' for (u, v), w in zip(edges, weights)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8, ax=ax)
    else:
        nx.draw_networkx_edges(G, pos, alpha=0.5, ax=ax)

    labels = node_labels if node_labels else {n: str(n) for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=9, font_family='SimHei', ax=ax)

    ax.set_title(title, fontsize=14)
    ax.axis('off')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] 网络图已保存: {output_path}")


def plot_time_evolution(time_data, *value_datasets, labels=None,
                        xlabel='时间', ylabel='值',
                        title='时间演化过程', output_path='time_evolution.png',
                        highlight_regions=None):
    """时间演化图 - 适用于动态过程展示，支持高亮区间"""
    fig, ax = plt.subplots(figsize=(12, 6))

    if labels is None:
        labels = [f'序列{i+1}' for i in range(len(value_datasets))]

    colors = plt.cm.tab10(np.linspace(0, 1, len(value_datasets)))
    for i, data in enumerate(value_datasets):
        ax.plot(time_data, data, color=colors[i], linewidth=2, label=labels[i])

    if highlight_regions:
        for region in highlight_regions:
            ax.axvspan(region['start'], region['end'],
                       alpha=0.15, color=region.get('color', 'yellow'),
                       label=region.get('label', ''))

    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] 时间演化图已保存: {output_path}")


def plot_bootstrap_ci(data, stat_func=np.mean, n_bootstrap=10000,
                      ci_level=0.95, title='Bootstrap置信区间',
                      output_path='bootstrap_ci.png'):
    """Bootstrap置信区间可视化"""
    np.random.seed(42)
    boot_stats = []
    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=len(data), replace=True)
        boot_stats.append(stat_func(sample))
    boot_stats = np.array(boot_stats)

    alpha = (1 - ci_level) / 2
    ci_low = np.percentile(boot_stats, alpha * 100)
    ci_high = np.percentile(boot_stats, (1 - alpha) * 100)
    point_est = stat_func(data)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 左：Bootstrap分布
    axes[0].hist(boot_stats, bins=50, density=True, alpha=0.7, color='steelblue',
                 edgecolor='white')
    axes[0].axvline(ci_low, color='red', linestyle='--', linewidth=2)
    axes[0].axvline(ci_high, color='red', linestyle='--', linewidth=2)
    axes[0].axvline(point_est, color='green', linewidth=2, label=f'点估计: {point_est:.4f}')
    axes[0].fill_betweenx([0, axes[0].get_ylim()[1] if axes[0].get_ylim()[1] > 0 else 1],
                           ci_low, ci_high, alpha=0.15, color='red',
                           label=f'{ci_level*100:.0f}%CI: [{ci_low:.4f}, {ci_high:.4f}]')
    axes[0].set_xlabel('统计量', fontsize=12)
    axes[0].set_ylabel('密度', fontsize=12)
    axes[0].legend(fontsize=10)
    axes[0].set_title('Bootstrap分布', fontsize=13)

    # 右：统计摘要
    stats_text = (
        f"原始样本量: {len(data)}\n"
        f"Bootstrap次数: {n_bootstrap:,}\n"
        f"点估计: {point_est:.4f}\n"
        f"Bootstrap标准误: {np.std(boot_stats):.4f}\n"
        f"{ci_level*100:.0f}%置信区间:\n"
        f"  下界: {ci_low:.4f}\n"
        f"  上界: {ci_high:.4f}\n"
        f"区间宽度: {ci_high - ci_low:.4f}\n"
    )
    axes[1].text(0.1, 0.5, stats_text, transform=axes[1].transAxes,
                 fontsize=12, verticalalignment='center', fontfamily='monospace',
                 bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    axes[1].axis('off')
    axes[1].set_title('统计摘要', fontsize=13)

    fig.suptitle(title, fontsize=15, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Bootstrap CI图已保存: {output_path}")


# === 使用示例 ===
if __name__ == '__main__':
    # 示例1：3D曲面图
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))
    plot_3d_surface(X, Y, Z, 'x', 'y', 'f(x,y)', '优化目标函数地形图', 'example_3d.png')

    # 示例2：Pareto前沿
    np.random.seed(42)
    f1_all = np.random.uniform(0, 10, 200)
    f2_all = np.random.uniform(0, 10, 200)
    mask = (f1_all + f2_all > 8) & (f1_all + f2_all < 12)
    f1_p = np.linspace(2, 8, 20)
    f2_p = 10 - f1_p + np.random.normal(0, 0.3, 20)
    plot_pareto_front(f1_all, f2_all, f1_p, f2_p, '成本', '质量', 'Pareto前沿', 'example_pareto.png')

    # 示例3：Tornado图
    params = ['温度', '压力', '浓度', '时间', '催化剂']
    effects = [0.35, -0.22, 0.18, -0.12, 0.08]
    plot_tornado(params, effects, output_path='example_tornado.png')

    # 示例4：蒙特卡洛
    mc_results = np.random.normal(100, 15, 10000)
    plot_monte_carlo_distribution(mc_results, true_value=98.5, output_path='example_mc.png')

    # 示例5：雷达图
    categories = ['精度', '稳定性', '计算效率', '可解释性', '泛化能力']
    model_a = [0.85, 0.78, 0.92, 0.65, 0.72]
    model_b = [0.91, 0.85, 0.75, 0.80, 0.88]
    plot_radar(categories, model_a, model_b, labels=['XGBoost', '随机森林'], output_path='example_radar.png')

    # 示例6：消融实验
    modules = ['特征工程', '超参优化', '集成融合']
    ablated = [7.8, 6.1, 5.9]
    plot_ablation_bar(modules, 5.2, ablated, output_path='example_ablation.png')

    print("\n所有示例图表已生成！")
