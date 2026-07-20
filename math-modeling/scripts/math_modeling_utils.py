"""
数学建模代码工具库
版本：2.0
日期：2026年7月20日
功能：封装常用数学建模函数，方便竞赛使用
变更：v2.0 - 修复 plt.show() → plt.savefig()+plt.close()
     - 增加输入验证和异常处理
     - 增加 save_dir 参数统一管理输出路径
     - 修复 grey_prediction 数值稳定性
使用方法：from math_modeling_utils import *
"""

import os
import numpy as np
import pandas as pd
from scipy import optimize, stats
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple, Dict, Optional, Union
import warnings
warnings.filterwarnings('ignore')

# ============ 设置中文显示 ============
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ============ 全局默认输出目录 ============
DEFAULT_SAVE_DIR = './figures'


def _ensure_dir(save_dir: str) -> str:
    """确保输出目录存在，返回目录路径"""
    os.makedirs(save_dir, exist_ok=True)
    return save_dir


def _save_fig(filename: str, save_dir: str = DEFAULT_SAVE_DIR,
              dpi: int = 300, close: bool = True) -> str:
    """
    统一保存图表，不弹窗。
    Returns: 保存的完整文件路径
    """
    path = os.path.join(_ensure_dir(save_dir), filename)
    plt.savefig(path, dpi=dpi, bbox_inches='tight')
    if close:
        plt.close()
    return path


# ============ 优化类工具 ============

class OptimizationTool:
    """优化问题工具类"""

    @staticmethod
    def linear_programming(c, A_ub, b_ub, A_eq=None, b_eq=None, bounds=None):
        """
        线性规划求解

        Args:
            c: 目标函数系数（最小化）
            A_ub: 不等式约束矩阵
            b_ub: 不等式约束向量
            A_eq: 等式约束矩阵
            b_eq: 等式约束向量
            bounds: 变量范围 [(low, high), ...]

        Returns:
            result: 求解结果
        """
        c = np.asarray(c, dtype=float)
        A_ub = np.asarray(A_ub, dtype=float)
        b_ub = np.asarray(b_ub, dtype=float)

        result = optimize.linprog(c, A_ub=A_ub, b_ub=b_ub,
                                  A_eq=A_eq, b_eq=b_eq,
                                  bounds=bounds, method='highs')

        if result.success:
            print(f"✅ 求解成功！")
            print(f"最优解: {result.x}")
            print(f"最优值: {result.fun}")
        else:
            print(f"❌ 求解失败: {result.message}")

        return result

    @staticmethod
    def integer_programming(c, A_ub, b_ub, A_eq=None, b_eq=None, bounds=None):
        """
        整数规划求解（使用PuLP）
        """
        try:
            from pulp import LpProblem, LpMaximize, LpVariable, lpSum, value

            n = len(c)
            prob = LpProblem("IP", LpMaximize)
            x = [LpVariable(f"x{i}", lowBound=0, cat='Integer') for i in range(n)]
            prob += lpSum([c[i] * x[i] for i in range(n)])

            for j in range(len(b_ub)):
                prob += lpSum([A_ub[j][i] * x[i] for i in range(n)]) <= b_ub[j]

            if A_eq is not None:
                for j in range(len(b_eq)):
                    prob += lpSum([A_eq[j][i] * x[i] for i in range(n)]) == b_eq[j]

            prob.solve()
            result = {'success': True, 'x': [value(var) for var in x], 'fun': value(prob.objective)}

            print(f"✅ 整数规划求解成功！")
            print(f"最优解: {result['x']}")
            print(f"最优值: {result['fun']}")
            return result

        except ImportError:
            print("❌ 需要安装PuLP: pip install pulp")
            return None

    @staticmethod
    def nonlinear_programming(fun, x0, constraints=None, bounds=None):
        """非线性规划求解"""
        result = optimize.minimize(fun, x0, method='SLSQP',
                                   constraints=constraints, bounds=bounds)

        if result.success:
            print(f"✅ 非线性规划求解成功！")
            print(f"最优解: {result.x}")
            print(f"最优值: {result.fun}")
        else:
            print(f"❌ 求解失败: {result.message}")
        return result


# ============ 统计类工具 ============

class StatisticsTool:
    """统计分析工具类"""

    @staticmethod
    def descriptive_statistics(data):
        """描述性统计分析"""
        if isinstance(data, pd.DataFrame):
            stats_df = data.describe()
        else:
            stats_df = pd.DataFrame(data).describe()
        print("📊 描述性统计：")
        print(stats_df)
        return stats_df

    @staticmethod
    def normality_test(data, alpha=0.05):
        """正态性检验（Shapiro-Wilk）"""
        data = np.asarray(data).flatten()
        if len(data) < 3:
            print("❌ 数据量不足（需至少3个样本）")
            return None
        if len(data) > 5000:
            print("⚠️ 样本量>5000，Shapiro-Wilk 可能不准确，建议用 K-S 检验")
        stat, p_value = stats.shapiro(data)
        result = {'test': 'Shapiro-Wilk', 'statistic': stat, 'p_value': p_value, 'is_normal': p_value > alpha}

        print(f"📊 正态性检验：P值={p_value:.4f}")
        print(f"  {'✅ 符合正态分布' if p_value > alpha else '❌ 不符合正态分布'}")
        return result

    @staticmethod
    def correlation_analysis(data, method='pearson', save_dir=DEFAULT_SAVE_DIR,
                            filename='correlation_heatmap.png'):
        """相关性分析 + 热力图（保存不弹窗）"""
        corr_matrix = data.corr(method=method)
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0)
        plt.title(f'{method.capitalize()}相关系数矩阵')
        plt.tight_layout()
        path = _save_fig(filename, save_dir)
        print(f"📊 相关性热力图已保存: {path}")
        return corr_matrix


# ============ 预测类工具 ============

class PredictionTool:
    """预测分析工具类"""

    @staticmethod
    def arima_forecast(data, order=(2, 1, 2), steps=10):
        """ARIMA时间序列预测"""
        try:
            from statsmodels.tsa.arima.model import ARIMA
            data = np.asarray(data, dtype=float)
            if np.any(np.isnan(data)):
                print("⚠️ 数据包含 NaN，已自动丢弃")
                data = data[~np.isnan(data)]
            model = ARIMA(data, order=order)
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=steps)
            print(f"📊 ARIMA{order} 预测完成")
            return forecast
        except ImportError:
            print("❌ 需要安装 statsmodels: pip install statsmodels")
            return None
        except Exception as e:
            print(f"❌ ARIMA 求解失败: {e}")
            return None

    @staticmethod
    def exponential_smoothing(data, alpha=0.3, steps=10):
        """指数平滑预测"""
        data = np.asarray(data, dtype=float)
        if len(data) == 0:
            print("❌ 数据为空")
            return None
        result = [data[0]]
        for i in range(1, len(data)):
            result.append(alpha * data[i] + (1 - alpha) * result[-1])
        forecast = [result[-1]] * steps
        return forecast

    @staticmethod
    def grey_prediction(data, steps=10):
        """
        灰色预测GM(1,1)
        v2.0: 修复数值稳定性，增加输入校验
        """
        data = np.asarray(data, dtype=float).flatten()
        if len(data) < 4:
            print("❌ 灰色预测至少需要4个数据点")
            return None
        if np.any(data <= 0):
            print("⚠️ GM(1,1) 要求原始数据为正数，存在非正值")

        n = len(data)
        x1 = np.cumsum(data)
        z1 = 0.5 * (x1[:-1] + x1[1:])
        B = np.column_stack([-z1, np.ones(n - 1)])
        Y = data[1:]

        # 使用 lstsq 替代 inv，更稳定
        params, residuals, rank, sv = np.linalg.lstsq(B, Y, rcond=None)
        a, b = params

        if abs(a) < 1e-12:
            print("⚠️ 发展系数 a≈0，模型退化为常数预测")

        forecast = []
        for k in range(n, n + steps):
            x1_pred = (data[0] - b / a) * np.exp(-a * k) + b / a
            forecast.append(x1_pred)
        # 从累加值还原为原始值
        forecast = np.diff(np.concatenate([[x1[-1]], forecast]))
        return forecast


# ============ 评价类工具 ============

class EvaluationTool:
    """综合评价工具类"""

    @staticmethod
    def ahp(matrix):
        """层次分析法计算权重"""
        matrix = np.asarray(matrix, dtype=float)
        n = matrix.shape[0]
        if matrix.shape != (n, n):
            print("❌ 判断矩阵必须是方阵")
            return None, None

        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        max_eigenvalue = np.max(eigenvalues.real)
        max_index = np.argmax(eigenvalues.real)
        weights = eigenvectors[:, max_index].real
        weights = weights / weights.sum()

        CI = (max_eigenvalue - n) / (n - 1) if n > 1 else 0
        RI = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
        CR = CI / RI[n - 1] if n <= len(RI) else float('inf')

        print(f"📊 AHP权重: {weights}")
        print(f"  一致性比率 CR = {CR:.4f} {'✅通过' if CR < 0.1 else '❌未通过'}")
        return weights, CR

    @staticmethod
    def topsis(data, weights, criteria_type):
        """TOPSIS优劣解距离法"""
        data = np.asarray(data, dtype=float)
        weights = np.asarray(weights, dtype=float)
        criteria_type = np.asarray(criteria_type)

        # 避免除零
        col_norms = np.sqrt(np.sum(data ** 2, axis=0))
        col_norms[col_norms == 0] = 1
        norm_data = data / col_norms
        weighted_data = norm_data * weights

        ideal_best = []
        ideal_worst = []
        for i, ctype in enumerate(criteria_type):
            if ctype == 1:
                ideal_best.append(np.max(weighted_data[:, i]))
                ideal_worst.append(np.min(weighted_data[:, i]))
            else:
                ideal_best.append(np.min(weighted_data[:, i]))
                ideal_worst.append(np.max(weighted_data[:, i]))

        dist_best = np.sqrt(np.sum((weighted_data - ideal_best) ** 2, axis=1))
        dist_worst = np.sqrt(np.sum((weighted_data - ideal_worst) ** 2, axis=1))

        # 避免除零
        total_dist = dist_best + dist_worst
        total_dist[total_dist == 0] = 1e-12
        closeness = dist_worst / total_dist
        ranking = np.argsort(-closeness) + 1

        print(f"📊 TOPSIS贴近度: {closeness}")
        return closeness, ranking

    @staticmethod
    def entropy_weight(data):
        """熵权法计算权重"""
        data = np.asarray(data, dtype=float)
        # 处理零值：加微小偏移避免 log(0)
        data_min = data.min(axis=0)
        data_range = data.max(axis=0) - data_min
        data_range[data_range == 0] = 1
        norm_data = (data - data_min) / data_range + 1e-10

        n, m = norm_data.shape
        k = 1 / np.log(n)

        # 归一化
        col_sums = norm_data.sum(axis=0)
        col_sums[col_sums == 0] = 1
        norm_data = norm_data / col_sums

        entropy = np.zeros(m)
        for j in range(m):
            for i in range(n):
                if norm_data[i, j] > 0:
                    entropy[j] -= k * norm_data[i, j] * np.log(norm_data[i, j])

        d = 1 - entropy
        d_sum = d.sum()
        if d_sum == 0:
            print("⚠️ 所有指标熵值相同，权重均分")
            weights = np.ones(m) / m
        else:
            weights = d / d_sum
        return weights


# ============ 可视化工具 ============

class VisualizationTool:
    """可视化工具类（所有图表保存不弹窗）"""

    @staticmethod
    def plot_radar(data, labels, title='雷达图', save_dir=DEFAULT_SAVE_DIR,
                   filename='radar_chart.png'):
        """绘制雷达图（保存不弹窗）"""
        data = np.asarray(data)
        if data.ndim == 1:
            data = data.reshape(1, -1)

        n_vars = len(labels)
        angles = np.linspace(0, 2 * np.pi, n_vars, endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        for i, row in enumerate(data):
            values = row.tolist() + [row[0]]
            ax.plot(angles, values, 'o-', linewidth=2, label=f'对象{i + 1}')
            ax.fill(angles, values, alpha=0.25)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        ax.set_title(title, pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
        plt.tight_layout()
        path = _save_fig(filename, save_dir)
        print(f"📊 雷达图已保存: {path}")
        return path

    @staticmethod
    def plot_heatmap(data, x_labels, y_labels, title='热力图',
                     save_dir=DEFAULT_SAVE_DIR, filename='heatmap.png'):
        """绘制热力图（保存不弹窗）"""
        data = np.asarray(data)
        plt.figure(figsize=(10, 8))
        sns.heatmap(data, annot=True, fmt='.3f', cmap='coolwarm',
                    xticklabels=x_labels, yticklabels=y_labels)
        plt.title(title)
        plt.tight_layout()
        path = _save_fig(filename, save_dir)
        print(f"📊 热力图已保存: {path}")
        return path

    @staticmethod
    def plot_bar(data, labels, title='柱状图', xlabel='', ylabel='',
                 save_dir=DEFAULT_SAVE_DIR, filename='bar_chart.png',
                 figsize=(10, 6)):
        """绘制柱状图（保存不弹窗）"""
        plt.figure(figsize=figsize)
        x = np.arange(len(labels))
        if np.asarray(data).ndim == 1:
            plt.bar(x, data)
        else:
            data = np.asarray(data)
            width = 0.8 / data.shape[0]
            for i in range(data.shape[0]):
                plt.bar(x + i * width, data[i], width, label=f'系列{i + 1}')
            plt.legend()
        plt.xticks(x, labels)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        path = _save_fig(filename, save_dir)
        print(f"📊 柱状图已保存: {path}")
        return path

    @staticmethod
    def plot_line(x, y, title='折线图', xlabel='', ylabel='',
                  save_dir=DEFAULT_SAVE_DIR, filename='line_chart.png',
                  figsize=(10, 6)):
        """绘制折线图（保存不弹窗）"""
        plt.figure(figsize=figsize)
        plt.plot(x, y, 'o-', linewidth=2)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        path = _save_fig(filename, save_dir)
        print(f"📊 折线图已保存: {path}")
        return path
