"""
数学建模代码工具库 (Math Modeling Utilities)
版本：3.0 (基于姜启源《数学模型》与竞赛实践系统升级)
功能：封装常用数学建模函数与经典机理模型算法
- 优化工具：LP、IP、NLP、经典库存EOQ与报童随机存储模型
- 评价与博弈：AHP(特征值/和积/根法)、TOPSIS、熵权法、Shapley值合作博弈、Raiffa谈判解
- 动态系统与稳定性：Leslie矩阵种群预测、相平面自治系统平衡点稳定性分析(Jacobian特征根判据)
- 马尔可夫链：稳态分布求解、吸收马氏链基本矩阵与吸收概率计算
- 统计与诊断：正态性检验、相关性分析、Durbin-Watson自相关检验、参数敏感度弹性分析
- 可视化：雷达图、热力图、柱状图、折线图、相平面轨线图（严格遵循保存不弹窗）
使用方法：from math_modeling_utils import *
"""

import os
import math
import itertools
import numpy as np
import pandas as pd
from scipy import optimize, stats
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple, Dict, Optional, Union, Callable, Any
import warnings
warnings.filterwarnings('ignore')

# ============ 设置中文显示 ============
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans', 'sans-serif']
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


# ==========================================
# 1. 优化与存贮模型工具
# ==========================================

class OptimizationTool:
    """优化问题工具类"""

    @staticmethod
    def linear_programming(c, A_ub, b_ub, A_eq=None, b_eq=None, bounds=None):
        """
        线性规划求解
        min c^T x
        s.t. A_ub x <= b_ub, A_eq x == b_eq, bounds
        """
        c = np.asarray(c, dtype=float)
        A_ub = np.asarray(A_ub, dtype=float)
        b_ub = np.asarray(b_ub, dtype=float)

        result = optimize.linprog(c, A_ub=A_ub, b_ub=b_ub,
                                  A_eq=A_eq, b_eq=b_eq,
                                  bounds=bounds, method='highs')

        if result.success:
            print(f"[OK] 线性规划求解成功！最优解: {result.x}, 最优值: {result.fun}")
        else:
            print(f"[FAIL] 求解失败: {result.message}")

        return result

    @staticmethod
    def integer_programming(c, A_ub, b_ub, A_eq=None, b_eq=None, bounds=None, maximize=True):
        """
        整数规划求解（支持 PuLP，若无则使用 scipy.optimize.milp）
        """
        try:
            from scipy.optimize import milp, LinearConstraint, Bounds
            c_arr = np.asarray(c, dtype=float)
            if maximize:
                c_arr = -c_arr
            n = len(c_arr)

            # 约束汇总
            constraints = []
            if A_ub is not None and len(b_ub) > 0:
                A_ub = np.asarray(A_ub, dtype=float)
                b_ub = np.asarray(b_ub, dtype=float)
                constraints.append(LinearConstraint(A_ub, -np.inf, b_ub))
            if A_eq is not None and len(b_eq) > 0:
                A_eq = np.asarray(A_eq, dtype=float)
                b_eq = np.asarray(b_eq, dtype=float)
                constraints.append(LinearConstraint(A_eq, b_eq, b_eq))

            lb = [0] * n if bounds is None else [b[0] if b[0] is not None else 0 for b in bounds]
            ub = [np.inf] * n if bounds is None else [b[1] if b[1] is not None else np.inf for b in bounds]
            var_bounds = Bounds(lb, ub)
            integrality = np.ones(n)  # 1表示全部为整数变量

            res = milp(c=c_arr, constraints=constraints, bounds=var_bounds, integrality=integrality)
            if res.success:
                opt_val = -res.fun if maximize else res.fun
                print(f"✅ 整数规划求解成功！最优解: {res.x}, 最优值: {opt_val}")
                return {'success': True, 'x': res.x, 'fun': opt_val}
            else:
                print(f"❌ 求解未找到可行解: {res.status}")
                return {'success': False, 'x': None, 'fun': None}
        except Exception as e:
            print(f"❌ 整数规划求解异常: {e}")
            return None

    @staticmethod
    def nonlinear_programming(fun, x0, constraints=None, bounds=None):
        """非线性规划求解 (SLSQP)"""
        result = optimize.minimize(fun, x0, method='SLSQP',
                                   constraints=constraints, bounds=bounds)
        if result.success:
            print(f"✅ 非线性规划求解成功！最优解: {result.x}, 最优值: {result.fun}")
        else:
            print(f"❌ 求解失败: {result.message}")
        return result

    @staticmethod
    def economic_order_quantity(c1: float, c2: float, r: float, c3: Optional[float] = None) -> Dict[str, float]:
        if c3 is None or c3 <= 0:
            # 不允许缺货
            T_opt = np.sqrt((2 * c1) / (c2 * r))
            Q_opt = np.sqrt((2 * c1 * r) / c2)
            C_opt = np.sqrt(2 * c1 * c2 * r)
            print(f"[EOQ不允许缺货] 周期 T*={T_opt:.3f}, 批量 Q*={Q_opt:.3f}, 平均日成本 C*={C_opt:.3f}")
            return {'T_opt': T_opt, 'Q_opt': Q_opt, 'C_opt': C_opt, 'shortage_allowed': False}
        else:
            # 允许缺货
            lambda_factor = np.sqrt((c2 + c3) / c3)
            T_opt = np.sqrt((2 * c1 * (c2 + c3)) / (c2 * c3 * r))
            Q_prime = np.sqrt((2 * c1 * r * c3) / (c2 * (c2 + c3)))
            R_opt = r * T_opt  # 最大订购量
            C_opt = np.sqrt((2 * c1 * c2 * c3 * r) / (c2 + c3))
            print(f"[EOQ允许缺货] 周期 T*={T_opt:.3f}, 进货量 Q'*={Q_prime:.3f}, 订货量 R*={R_opt:.3f}, 成本 C*={C_opt:.3f}")
            return {'T_opt': T_opt, 'Q_prime_opt': Q_prime, 'R_opt': R_opt, 'C_opt': C_opt, 'shortage_allowed': True}

    @staticmethod
    def newsvendor(a: float, b: float, c: float, demand_mean: float, demand_std: float) -> Dict[str, float]:
        if not (b > a > c):
            raise ValueError("单价必须满足售价 b > 进货价 a > 残值 c")
        critical_fractile = (b - a) / (b - c)
        opt_quantity = stats.norm.ppf(critical_fractile, loc=demand_mean, scale=demand_std)
        print(f"[报童模型] 临界分位数 P(r <= n*) = {critical_fractile:.4f}, 最优订货量 n* = {opt_quantity:.2f}")
        return {'critical_fractile': critical_fractile, 'opt_quantity': opt_quantity}


# ==========================================
# 2. 统计与诊断工具
# ==========================================

class StatisticsTool:
    """统计分析与计量诊断工具类"""

    @staticmethod
    def descriptive_statistics(data):
        """描述性统计分析"""
        stats_df = pd.DataFrame(data).describe()
        print("[INFO] 描述性统计：\n", stats_df)
        return stats_df

    @staticmethod
    def normality_test(data, alpha=0.05):
        """正态性检验（Shapiro-Wilk）"""
        data = np.asarray(data).flatten()
        if len(data) < 3:
            print("[FAIL] 数据量不足（需至少3个样本）")
            return None
        stat, p_value = stats.shapiro(data)
        is_normal = p_value > alpha
        print(f"[INFO] 正态性检验：P值={p_value:.4f} -> {'[OK] 符合正态分布' if is_normal else '[FAIL] 不符合正态分布'}")
        return {'statistic': stat, 'p_value': p_value, 'is_normal': is_normal}

    @staticmethod
    def correlation_analysis(data, method='pearson', save_dir=DEFAULT_SAVE_DIR, filename='correlation_heatmap.png'):
        """相关性分析 + 热力图"""
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)
        corr_matrix = data.corr(method=method)
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0)
        plt.title(f'{method.capitalize()} 相关系数矩阵')
        plt.tight_layout()
        path = _save_fig(filename, save_dir)
        print(f"[INFO] 相关性热力图已保存: {path}")
        return corr_matrix

    @staticmethod
    def durbin_watson_test(residuals) -> Dict[str, Union[float, str]]:
        """
        Durbin-Watson (DW) 自相关检验
        DW = sum_{t=2}^n (e_t - e_{t-1})^2 / sum_{t=1}^n e_t^2
        """
        e = np.asarray(residuals, dtype=float).flatten()
        diff = np.diff(e)
        dw = np.sum(diff ** 2) / np.sum(e ** 2)
        rho_hat = 1.0 - dw / 2.0

        if dw < 1.2:
            diagnose = "存在显著正自相关 (Positive Autocorrelation)"
        elif dw > 2.8:
            diagnose = "存在显著负自相关 (Negative Autocorrelation)"
        else:
            diagnose = "无明显一阶自相关 (No Significant Autocorrelation)"

        print(f"[DW检验] DW值 = {dw:.4f}, 估计相关系数 rho ≈ {rho_hat:.4f} -> {diagnose}")
        return {'DW': dw, 'rho_hat': rho_hat, 'diagnosis': diagnose}

    @staticmethod
    def parameter_elasticity(x: float, y: float, dydx: float) -> float:
        """
        计算参数敏感度/弹性 (Elasticity/Sensitivity)
        S = (dy / y) / (dx / x) = (x / y) * (dy / dx)
        """
        if abs(y) < 1e-12:
            raise ZeroDivisionError("基准因变量 y 不能为 0")
        elasticity = (x / y) * dydx
        print(f"[灵敏度分析] 当 x={x}, y={y}, dy/dx={dydx:.4f} 时，参数弹性 S = {elasticity:.4f}")
        return elasticity


# ==========================================
# 3. 评价与博弈决策工具
# ==========================================

class EvaluationTool:
    """综合评价与博弈分配工具类"""

    @staticmethod
    def ahp(matrix, method: str = 'eigen') -> Tuple[np.ndarray, float, bool]:
        """
        层次分析法计算权重与一致性检验
        """
        matrix = np.asarray(matrix, dtype=float)
        n = matrix.shape[0]
        if matrix.shape != (n, n):
            raise ValueError("判断矩阵必须为方阵")

        if method == 'eigen':
            eigenvalues, eigenvectors = np.linalg.eig(matrix)
            max_idx = np.argmax(eigenvalues.real)
            max_eigenvalue = eigenvalues[max_idx].real
            w = eigenvectors[:, max_idx].real
            w = w / np.sum(w)
        elif method == 'arithmetic':
            col_sums = matrix.sum(axis=0)
            norm_matrix = matrix / col_sums
            w = norm_matrix.mean(axis=1)
            w = w / np.sum(w)
            Aw = np.dot(matrix, w)
            max_eigenvalue = np.mean(Aw / w)
        elif method == 'geometric':
            geo_mean = np.prod(matrix, axis=1) ** (1.0 / n)
            w = geo_mean / np.sum(geo_mean)
            Aw = np.dot(matrix, w)
            max_eigenvalue = np.mean(Aw / w)
        else:
            raise ValueError(f"未知方法: {method}，支持 'eigen', 'arithmetic', 'geometric'")

        CI = (max_eigenvalue - n) / (n - 1) if n > 1 else 0.0
        RI_TABLE = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.51, 1.54, 1.56, 1.58]
        RI = RI_TABLE[n - 1] if n <= len(RI_TABLE) else 1.58
        CR = CI / RI if RI > 0 else 0.0
        is_consistent = (CR < 0.10) or (n <= 2)

        print(f"[AHP({method})] 最大特征值 lambda_max={max_eigenvalue:.4f}, CI={CI:.4f}, CR={CR:.4f} -> {'[OK]通过一致性' if is_consistent else '[FAIL]未通过'}")
        print(f"  权重向量: {np.round(w, 4)}")
        return w, CR, is_consistent

    @staticmethod
    def topsis(data, weights, criteria_type):
        """TOPSIS优劣解距离法"""
        data = np.asarray(data, dtype=float)
        weights = np.asarray(weights, dtype=float)
        criteria_type = np.asarray(criteria_type)

        col_norms = np.sqrt(np.sum(data ** 2, axis=0))
        col_norms[col_norms == 0] = 1.0
        norm_data = (data / col_norms) * weights

        ideal_best = np.where(criteria_type == 1, norm_data.max(axis=0), norm_data.min(axis=0))
        ideal_worst = np.where(criteria_type == 1, norm_data.min(axis=0), norm_data.max(axis=0))

        dist_best = np.sqrt(np.sum((norm_data - ideal_best) ** 2, axis=1))
        dist_worst = np.sqrt(np.sum((norm_data - ideal_worst) ** 2, axis=1))

        total_dist = dist_best + dist_worst
        total_dist[total_dist == 0] = 1e-12
        closeness = dist_worst / total_dist
        ranking = np.argsort(-closeness) + 1
        return closeness, ranking

    @staticmethod
    def entropy_weight(data):
        """熵权法计算客观权重"""
        data = np.asarray(data, dtype=float)
        data_min = data.min(axis=0)
        data_range = data.max(axis=0) - data_min
        data_range[data_range == 0] = 1.0
        norm_data = (data - data_min) / data_range + 1e-10

        n, m = norm_data.shape
        k = 1.0 / np.log(n) if n > 1 else 1.0
        p = norm_data / norm_data.sum(axis=0)

        entropy = -k * np.sum(p * np.log(p + 1e-12), axis=0)
        d = 1.0 - entropy
        d_sum = d.sum()
        weights = d / d_sum if d_sum > 0 else np.ones(m) / m
        return weights

    @staticmethod
    def shapley_value(n_players: int, char_func: Callable[[Tuple[int, ...]], float]) -> np.ndarray:
        """合作博弈 Shapley 值计算"""
        players = list(range(1, n_players + 1))
        shapley = np.zeros(n_players)
        factorial_n = math.factorial(n_players)

        for i_idx, i in enumerate(players):
            other_players = [p for p in players if p != i]
            phi_i = 0.0
            for s_size in range(0, n_players):
                for subset in itertools.combinations(other_players, s_size):
                    subset_with_i = tuple(sorted(subset + (i,)))
                    subset_without_i = tuple(sorted(subset))
                    v_with = char_func(subset_with_i)
                    v_without = char_func(subset_without_i) if len(subset_without_i) > 0 else 0.0
                    marginal = v_with - v_without
                    weight = (math.factorial(s_size) * math.factorial(n_players - s_size - 1)) / factorial_n
                    phi_i += weight * marginal
            shapley[i_idx] = phi_i

        print(f"[Shapley值分摊] 各方分配值: {np.round(shapley, 4)}, 总计: {np.sum(shapley):.4f}")
        return shapley

    @staticmethod
    def raiffa_arbitration(conflict_points: List[float], total_surplus: float) -> np.ndarray:
        """Raiffa 谈判仲裁解"""
        b = np.asarray(conflict_points, dtype=float)
        n = len(b)
        b_bar = np.mean(b)
        factor = (2.0 * n - 3.0) / (2.0 * n - 1.0) if n > 1 else 1.0
        x = (total_surplus / n) + factor * (b_bar - b)
        print(f"[Raiffa谈判解] 分配方案: {np.round(x, 4)}")
        return x


# ==========================================
# 4. 动力系统与离散演化工具
# ==========================================

class DynamicSystemTool:
    """连续与离散动力系统分析工具类"""

    @staticmethod
    def leslie_population_model(L: np.ndarray, x0: np.ndarray, steps: int = 15) -> Dict[str, Any]:
        """Leslie 种群年龄结构演化模型"""
        L = np.asarray(L, dtype=float)
        x = np.asarray(x0, dtype=float).reshape(-1, 1)
        n = L.shape[0]

        eigenvalues, eigenvectors = np.linalg.eig(L)
        real_eigs = eigenvalues.real
        max_idx = np.argmax(real_eigs)
        lambda_1 = real_eigs[max_idx]
        stable_dist = eigenvectors[:, max_idx].real
        stable_dist = stable_dist / np.sum(stable_dist)

        trajectory = [x.flatten()]
        curr_x = x.copy()
        for _ in range(steps):
            curr_x = np.dot(L, curr_x)
            trajectory.append(curr_x.flatten())

        trajectory = np.array(trajectory)
        print(f"[Leslie矩阵] 主特征值 lambda_1 = {lambda_1:.4f} ({'增长' if lambda_1 > 1 else '衰退' if lambda_1 < 1 else '稳态'})")
        print(f"  稳态年龄分布比例: {np.round(stable_dist, 4)}")
        return {
            'lambda_1': lambda_1,
            'stable_distribution': stable_dist,
            'trajectory': trajectory
        }

    @staticmethod
    def phase_plane_stability(f: Callable[[float, float], float],
                             g: Callable[[float, float], float],
                             x0: float, y0: float,
                             eps: float = 1e-5) -> Dict[str, Any]:
        """二维自治系统平衡点稳定性分析"""
        fx = (f(x0 + eps, y0) - f(x0 - eps, y0)) / (2 * eps)
        fy = (f(x0, y0 + eps) - f(x0, y0 - eps)) / (2 * eps)
        gx = (g(x0 + eps, y0) - g(x0 - eps, y0)) / (2 * eps)
        gy = (g(x0, y0 + eps) - g(x0, y0 - eps)) / (2 * eps)

        J = np.array([[fx, fy], [gx, gy]])
        p = -(fx + gy)  # -trace
        q = fx * gy - fy * gx  # det
        delta = p ** 2 - 4 * q

        if q < 0:
            status = "不稳定鞍点 (Saddle Point)"
            is_stable = False
        elif q > 0 and p > 0:
            is_stable = True
            status = "渐近稳定结点 (Stable Node)" if delta >= 0 else "渐近稳定焦点 (Stable Focus)"
        elif q > 0 and p < 0:
            is_stable = False
            status = "不稳定结点 (Unstable Node)" if delta >= 0 else "不稳定焦点 (Unstable Focus)"
        elif q > 0 and abs(p) < 1e-8:
            is_stable = True
            status = "中心点 (Center / 轨道稳定)"
        else:
            is_stable = False
            status = "临界/退化平衡点 (Degenerate Point)"

        print(f"[相平面稳定性] 平衡点 ({x0}, {y0}) -> trace={-p:.4f}, det={q:.4f}, Delta={delta:.4f}")
        print(f"  类型判断: {status}")
        return {'Jacobian': J, 'p': p, 'q': q, 'delta': delta, 'status': status, 'is_stable': is_stable}


# ==========================================
# 5. 马尔可夫链工具
# ==========================================

class MarkovTool:
    """马尔可夫链分析工具类"""

    @staticmethod
    def markov_steady_state(P: np.ndarray) -> np.ndarray:
        """计算不可约马氏链的稳态分布"""
        P = np.asarray(P, dtype=float)
        n = P.shape[0]
        A = np.vstack([P.T - np.eye(n), np.ones((1, n))])
        b = np.zeros(n + 1)
        b[-1] = 1.0
        w, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        print(f"[马氏链稳态分布] w = {np.round(w, 4)}")
        return w

    @staticmethod
    def absorbing_markov_chain(P: np.ndarray, n_absorbing: int) -> Dict[str, np.ndarray]:
        """吸收马氏链分析"""
        P = np.asarray(P, dtype=float)
        k = P.shape[0]
        r = n_absorbing
        t = k - r

        I_r = P[:r, :r]
        R = P[r:, :r]
        Q = P[r:, r:]

        I_t = np.eye(t)
        M = np.linalg.inv(I_t - Q)

        e = np.ones((t, 1))
        y = np.dot(M, e).flatten()
        F = np.dot(M, R)

        print(f"[吸收马氏链分析]")
        print(f"  各暂态平均吸收步数: {np.round(y, 3)}")
        print(f"  吸收概率矩阵 F:\n{np.round(F, 4)}")
        return {'Fundamental_Matrix_M': M, 'Mean_Absorption_Time_y': y, 'Absorption_Prob_F': F}


# ==========================================
# 6. 预测与时序工具
# ==========================================

class PredictionTool:
    """预测分析工具类"""

    @staticmethod
    def arima_forecast(data, order=(2, 1, 2), steps=10):
        """ARIMA时间序列预测"""
        try:
            from statsmodels.tsa.arima.model import ARIMA
            data = np.asarray(data, dtype=float)
            if np.any(np.isnan(data)):
                data = data[~np.isnan(data)]
            model = ARIMA(data, order=order)
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=steps)
            print(f"[INFO] ARIMA{order} 预测完成")
            return forecast
        except ImportError:
            print("[FAIL] 需要安装 statsmodels: pip install statsmodels")
            return None
        except Exception as e:
            print(f"[FAIL] ARIMA 求解失败: {e}")
            return None

    @staticmethod
    def exponential_smoothing(data, alpha=0.3, steps=10):
        """指数平滑预测"""
        data = np.asarray(data, dtype=float)
        if len(data) == 0:
            return None
        result = [data[0]]
        for i in range(1, len(data)):
            result.append(alpha * data[i] + (1 - alpha) * result[-1])
        forecast = [result[-1]] * steps
        return forecast

    @staticmethod
    def grey_prediction(data, steps=10):
        """灰色预测 GM(1,1)"""
        data = np.asarray(data, dtype=float).flatten()
        if len(data) < 4:
            print("[FAIL] 灰色预测至少需要4个数据点")
            return None
        n = len(data)
        x1 = np.cumsum(data)
        z1 = 0.5 * (x1[:-1] + x1[1:])
        B = np.column_stack([-z1, np.ones(n - 1)])
        Y = data[1:]

        params, _, _, _ = np.linalg.lstsq(B, Y, rcond=None)
        a, b = params

        forecast = []
        for k in range(n, n + steps):
            x1_pred = (data[0] - b / a) * np.exp(-a * k) + b / a
            forecast.append(x1_pred)
        forecast = np.diff(np.concatenate([[x1[-1]], forecast]))
        return forecast


# ==========================================
# 7. 可视化工具
# ==========================================

class VisualizationTool:
    """可视化工具类（所有图表保存不弹窗）"""

    @staticmethod
    def plot_radar(data, labels, title='雷达图', save_dir=DEFAULT_SAVE_DIR, filename='radar_chart.png'):
        """绘制雷达图"""
        data = np.asarray(data)
        if data.ndim == 1:
            data = data.reshape(1, -1)

        n_vars = len(labels)
        angles = np.linspace(0, 2 * np.pi, n_vars, endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        for i, row in enumerate(data):
            values = row.tolist() + [row[0]]
            ax.plot(angles, values, 'o-', linewidth=2, label=f'方案{i + 1}')
            ax.fill(angles, values, alpha=0.25)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        ax.set_title(title, pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
        plt.tight_layout()
        path = _save_fig(filename, save_dir)
        print(f"[INFO] 雷达图已保存: {path}")
        return path

    @staticmethod
    def plot_heatmap(data, x_labels, y_labels, title='热力图', save_dir=DEFAULT_SAVE_DIR, filename='heatmap.png'):
        """绘制热力图"""
        data = np.asarray(data)
        plt.figure(figsize=(10, 8))
        sns.heatmap(data, annot=True, fmt='.3f', cmap='coolwarm',
                    xticklabels=x_labels, yticklabels=y_labels)
        plt.title(title)
        plt.tight_layout()
        path = _save_fig(filename, save_dir)
        print(f"[INFO] 热力图已保存: {path}")
        return path

    @staticmethod
    def plot_bar(data, labels, title='柱状图', xlabel='', ylabel='', save_dir=DEFAULT_SAVE_DIR, filename='bar_chart.png', figsize=(10, 6)):
        """绘制柱状图"""
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
        print(f"[INFO] 柱状图已保存: {path}")
        return path

    @staticmethod
    def plot_line(x, y, title='折线图', xlabel='', ylabel='', save_dir=DEFAULT_SAVE_DIR, filename='line_chart.png', figsize=(10, 6)):
        """绘制折线图"""
        plt.figure(figsize=figsize)
        plt.plot(x, y, 'o-', linewidth=2)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        path = _save_fig(filename, save_dir)
        print(f"[INFO] 折线图已保存: {path}")
        return path

