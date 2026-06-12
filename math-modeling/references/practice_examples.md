# 数学建模实践案例库

本文档包含5个完整的实践案例，覆盖常见建模问题类型。

---

## 案例1：物流配送优化（线性规划）

**问题**：3个仓库向4个配送点配送，最小化运输成本

**核心代码**：
```python
from scipy.optimize import linprog

# 成本系数
c = [10, 12, 15, 8, 14, 9, 16, 11, 13, 11, 12, 9]

# 供应约束
A_ub = [[1,1,1,1,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,1,1,1]]
b_ub = [300, 500, 200]

# 需求约束
A_eq = [[1,0,0,0,1,0,0,0,1,0,0,0],
        [0,1,0,0,0,1,0,0,0,1,0,0],
        [0,0,1,0,0,0,1,0,0,0,1,0],
        [0,0,0,1,0,0,0,1,0,0,0,1]]
b_eq = [200, 300, 150, 350]

result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, method='highs')
# 最优成本：9,950元
```

**结果解读**：
- 仓库A → 配送点1(200吨) + 配送点4(100吨)
- 仓库B → 配送点2(300吨) + 配送点4(200吨)
- 仓库C → 配送点3(150吨) + 配送点4(50吨)

---

## 案例2：PM2.5浓度预测（时间序列）

**问题**：预测未来7天PM2.5浓度

**ARIMA实现**：
```python
from statsmodels.tsa.arima.model import ARIMA

# 训练
model = ARIMA(train_data, order=(2, 1, 2))
model_fit = model.fit()

# 预测
forecast = model_fit.forecast(steps=7)
```

**评估指标**：
- RMSE: 9.70 μg/m³
- MAE: 7.66 μg/m³

**关键技巧**：
1. 先做数据探索（时序图、ACF、分布）
2. 用ADF检验判断是否需要差分
3. 通过AIC/BIC选择(p,d,q)参数

---

## 案例3：投资组合优化（多目标）

**问题**：5只股票，同时最大化收益、最小化风险

**加权求和法**：
```python
def weighted_objective(weights, alpha=0.5):
    """alpha控制风险偏好：0=纯收益，1=纯风险"""
    return alpha * portfolio_variance(weights) + (1-alpha) * (-returns @ weights)

# 不同alpha下的最优组合
for alpha in [0.2, 0.5, 0.8]:
    result = minimize(weighted_objective, x0, args=(alpha,), ...)
```

**夏普比率最优组合**：
- 收益率: 15.44%
- 风险: 11.38%
- 夏普比率: 1.09

---

## 案例4：城市宜居性评价（AHP+TOPSIS）

**AHP权重计算**：
```python
def ahp(matrix):
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    max_idx = np.argmax(eigenvalues.real)
    weights = eigenvectors[:, max_idx].real
    weights = weights / weights.sum()
    
    # 一致性检验
    CI = (eigenvalues[max_idx].real - n) / (n - 1)
    RI = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
    CR = CI / RI[n-1]
    return weights, CR
```

**TOPSIS评价**：
```python
def topsis(data, weights, criteria_type):
    # 标准化
    norm_data = data / np.sqrt(np.sum(data**2, axis=0))
    weighted_data = norm_data * weights
    
    # 正负理想解
    ideal_best = [max/min(col) for col in weighted_data.T]
    ideal_worst = [min/max(col) for col in weighted_data.T]
    
    # 贴近度
    closeness = dist_worst / (dist_best + dist_worst)
    return closeness
```

**结果**：北京第一（贴近度0.89），生活成本权重最高（0.36）

---

## 案例5：空气质量分析与预测（统计+回归）

**问题**：8个监测站60天空气质量数据分析与预测

**数据结构**：
- 附件1：空气质量监测数据（480条，13个字段）
- 附件2：气象数据（60条，8个字段）

**核心方法**：
1. **问题一**：groupby分组统计 + 柱状图/饼图可视化
2. **问题二**：皮尔逊相关系数 + 多元线性回归
3. **问题三**：训练集/测试集划分 + MAPE/RMSE评价

**关键代码**：
```python
# 相关系数计算
from scipy import stats
corr, p_value = stats.pearsonr(df['AQI'], df['风速(m/s)'])

# 多元线性回归
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# 评价指标
mape = mean_absolute_percentage_error(y_test, y_pred) * 100
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
```

**实践结果**：
- 风速与AQI显著正相关（r=0.260, p<0.05）
- 回归方程：AQI = 100.43 + 1.27×风速 - 0.81×最低温度
- R² = 0.108（解释力较弱，AQI受多因素影响）
- 测试集MAPE = 12.22%，RMSE = 14.63

**详细案例**：见 `references/air_quality_analysis.md`

---

## 常见陷阱

1. **线性规划**：约束条件必须完整，遗漏会导致无界解
2. **ARIMA**：R²为负不代表模型差，可能是数据波动大
3. **AHP**：CR必须<0.1，否则需要调整判断矩阵
4. **TOPSIS**：注意区分正向/逆向指标
5. **Windows路径**：Python使用 `E:/` 而非 `/e/`
