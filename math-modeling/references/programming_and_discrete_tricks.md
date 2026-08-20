# 运筹规划与离散建模经典技巧手册

> 本手册总结了《数学模型》教材中关于数学规划（LP/MIP/NLP）、0-1 变量逻辑转化、灵敏度对偶分析、离散网络与博弈评价等实用建模技巧。

---

## 1. 0-1 变量与逻辑命题转化技巧

### 1.1 互斥条件（Either-Or 约束）
若两个不等式 $f_1(x) \le 0$ 与 $f_2(x) \le 0$ 至少满足一个：
引入 0-1 变量 $y \in \{0, 1\}$ 和充分大正数 $M$：
$$\begin{cases} f_1(x) \le M y \\ f_2(x) \le M (1 - y) \end{cases}$$
推广至 $k$ 个条件中至少满足 $m$ 个：$\sum_{i=1}^k y_i \le k - m, \quad f_i(x) \le M y_i$。

### 1.2 条件激活与固定费用（Fixed Charge）
若 $x > 0$，则必须支付固定成本 $K$，且生产上限为 $C$：
引入 $y \in \{0, 1\}$：
$$x \le C y, \quad \text{Cost} = K y + c x$$

### 1.3 变量取值非零即达到阈值（Semi-Continuous 变量）
变量 $x$ 要么等于 0，要么 $x \ge L$（且上限 $U$）：
$$L y \le x \le U y, \quad y \in \{0, 1\}$$

### 1.4 分段线性函数转化 (Piecewise Linear Functions)
设分段点为 $b_1 \le b_2 \le \dots \le b_{n+1}$，函数值相应为 $f(b_k)$：
引入凸组合系数 $z_k \ge 0$ 与邻近激活 0-1 变量 $y_k \in \{0, 1\} (k=1,\dots,n)$：
$$\begin{cases}
x = \sum_{k=1}^{n+1} z_k b_k, \quad f(x) = \sum_{k=1}^{n+1} z_k f(b_k) \\
\sum_{k=1}^{n+1} z_k = 1, \quad \sum_{k=1}^n y_k = 1 \\
z_1 \le y_1, \quad z_k \le y_{k-1} + y_k \ (2 \le k \le n), \quad z_{n+1} \le y_n
\end{cases}$$

---

## 2. 线性规划的灵敏度分析与对偶解释

### 2.1 对偶价格 (Dual Price / 影子价格)
- 对偶变量 $y_i^*$ 表示第 $i$ 种资源增加 1 个单位时，目标函数最优值 $z^*$ 的边际增量：
  $$y_i^* = \frac{\partial z^*}{\partial b_i}$$
- **经济含义**：资源的边际价值。若资源未用尽（松弛变量 Slack > 0），则其对偶价格必为 0；若对偶价格 > 0，说明该资源是制约产出的瓶颈资源。

### 2.2 价值系数与右端常数容许变动范围 (Allowable Increase/Decrease)
- **目标系数变动**：在允许增减范围内，基变量集合不变，最优解 $x^*$ 不变，但最优目标值随之线性变动。
- **右端项变动**：在允许增减范围内，最优基矩阵保持不变，影子价格保持有效，最优解 $x^*$ 与最优目标值 $z^*$ 随之线性移动。

---

## 3. 层次分析法 (AHP) 进阶与残缺矩阵处理

### 3.1 权重计算的三种经典算法
设正互反矩阵 $A = (a_{ij})_{n \times n}$（满足 $a_{ij} > 0, a_{ji} = 1/a_{ij}, a_{ii} = 1$）：
1. **特征值法 (Exact Eigenvalue)**：求 $A \boldsymbol{w} = \lambda_{\max} \boldsymbol{w}$，归一化 $\boldsymbol{w}$。
2. **和积法 (Column-Normalized Arithmetic Mean)**：
   $$w_i = \frac{1}{n} \sum_{j=1}^n \frac{a_{ij}}{\sum_{k=1}^n a_{kj}}$$
3. **根法 / 几何均值法 (Geometric Mean Method)**：
   $$\bar{w}_i = \left(\prod_{j=1}^n a_{ij}\right)^{1/n}, \quad w_i = \frac{\bar{w}_i}{\sum_{k=1}^n \bar{w}_k}$$

### 3.2 组合一致性检验 (Hierarchical Combined Consistency)
总排序一致性指标：
$$CI_{total} = \sum_{j=1}^m w_j CI_j, \quad RI_{total} = \sum_{j=1}^m w_j RI_j, \quad CR_{total} = \frac{CI_{total}}{RI_{total}} < 0.1$$

### 3.3 残缺/不完全判断矩阵的处理 (Incomplete Pairwise Matrix)
若因信息不足部分元素未知（标记为 $\theta$）：
- 通过对数最小二乘拟合 $\min \sum (\ln a_{ij} - \ln(w_i/w_j))^2$ 仅对已知项求和；
- 或利用图论中强连通连通分支与生成树补全缺失比率。

---

## 4. 有向图与循环比赛排名 (Perron-Frobenius 理论)

- 设有向比赛胜负图邻接矩阵为 $A$（$a_{ij} = 1$ 表示 $i$ 战胜 $j$），令出度得分向量为 $\boldsymbol{s}^{(1)} = A \boldsymbol{e}$。
- 二阶得分向量 $\boldsymbol{s}^{(2)} = A \boldsymbol{s}^{(1)} = A^2 \boldsymbol{e}$（计入“战胜胜者”的间接实力）。
- **极限综合实力排名**：
  $$\boldsymbol{s}^* = \lim_{k \to \infty} \frac{A^k \boldsymbol{e}}{\lambda_1^k}$$
  其中 $\lambda_1$ 为 $A$ 的最大正特征值（Perron 根），$\boldsymbol{s}^*$ 为对应的非负主特征向量。
