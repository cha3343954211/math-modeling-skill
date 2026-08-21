# 经典数学模型精要与机理推导手册

> 本手册基于经典教材《数学模型》（姜启源、谢金星、叶俊等著），系统整理了 13 个核心专题的经典模型机理、数学公式推导、关键参数意义与应用场景，供数学建模竞赛与研究中查阅与借鉴。

---

## 1. 建模方法论与量纲分析

### 1.1 建模全过程的 7 大闭环步骤
```
[实际问题] ──→ 1. 模型准备 (明确对象/目标/背景)
                 ↓
               2. 模型假设 (抓住主要矛盾，合理简化)
                 ↓
               3. 模型构成 (引入符号，建立数学关系)
                 ↓
               4. 模型求解 (解析解/数值解/仿真)
                 ↓
               5. 模型分析 (灵敏度/误差/理论性质/稳定性)
                 ↓
               6. 模型检验 (对比实际数据/专家评估)
                 ↓ ───[不符合检验要求]──→ 回退修正假设与构成
               7. 模型应用 (预测/控制/优化/决策建议)
```

### 1.2 量纲齐次原理与 Buckingham $\Pi$ 定理
- **量纲齐次性（Dimensional Homogeneity）**：任何反映物理实际规律的方程，其各项必须具有相同的量纲。基本量纲通常为质量 $[M]$、长度 $[L]$、时间 $[T]$ 等。
- **$\Pi$ 定理**：设物理系统涉及 $m$ 个物理量 $q_1, q_2, \dots, q_m$，其量纲矩阵包含 $n$ 个独立基本量纲，且量纲矩阵的秩为 $r = \text{rank}(A)$，则该物理过程可由 $m - r$ 个独立的无量纲量（$\pi$ 项）之间的函数关系表述：
  $$F(\pi_1, \pi_2, \dots, \pi_{m-r}) = 0$$
- **特征尺度与无量纲化（Characteristic Scales）**：通过选取系统固有特征参数（特征长度 $x_c$、特征时间 $t_c$），令 $\bar{x} = x/x_c, \bar{t} = t/t_c$，将方程转化为无量纲形式，能有效揭示系统的核心无量纲特征群（如 Reynolds 数 $\text{Re} = \frac{\rho v l}{\mu}$、Froude 数 $\text{Fr} = \frac{v}{\sqrt{lg}}$、无量纲微扰参数 $\varepsilon$），便于渐近展开与极限分析。

---

## 2. 初等与代数模型

### 2.1 比例与席位分配问题 (公平分配原理)
- **Hamilton 法 (最大余额法)**：按比例 $q_i = N \frac{p_i}{\sum p_i}$ 取整后，将剩余席位依小数部分从大到小分配。缺点：存在 **Alabama 悖论**（总席位增加反而某方席位减少）和 **人口悖论**。
- **d'Hondt 最大均数法 / 几何均值法 / Q值法**：
  - 判定指标 $Q_i = \frac{p_i^2}{n_i(n_i+1)}$ 或平均席位数对比，每次将新增席位分配给使不公平度最小（即 $Q_i$ 最大）的方。满足单调性，消除 Alabama 悖论。

### 2.2 几何与物理初等模型
- **双层玻璃保温功效模型**：通过稳态热传导定律 $Q = k \frac{\Delta T}{d}$，建立室内外温差与传热通量方程，证明空气夹层热阻远大于玻璃，热传导损失与厚度比 $h = l/d$ 密切相关。
- **McMahon 赛艇动力学模型**：
  - 阻力 $f \propto s v^2$，功率 $p \propto w$（体重），总功率 $n p \propto f v$
  - 湿面积 $s \propto A^{2/3} \propto w'^{2/3} \propto n^{2/3}$，得到航速 $v \propto n^{1/9}$，用时 $t \propto n^{-1/9}$，极佳地解释了比赛成绩随人数增长的对数线性关系。

---

## 3. 微分方程与连续动力系统

### 3.1 种群增长模型 (Population Growth)
1. **Malthus 简单增长模型**：
   $$\frac{dx}{dt} = rx \implies x(t) = x_0 e^{rt}$$
   适用于早期资源无限环境。
2. **Logistic 逻辑斯谛阻滞增长模型**：
   $$\frac{dx}{dt} = rx \left(1 - \frac{x}{x_m}\right), \quad x(0) = x_0$$
   - 饱和容量 $x_m$，增长率在 $x = x_m/2$ 时达到峰值 $\left(\frac{dx}{dt}\right)_{\max} = \frac{rx_m}{4}$。
   - 解析解：
     $$x(t) = \frac{x_m}{1 + \left(\frac{x_m}{x_0} - 1\right) e^{-rt}}$$
3. **Gompertz 肿瘤/细胞生长模型**：
   $$\frac{dx}{dt} = -r x \ln\left(\frac{x}{x_m}\right)$$
   适用于前期极快、后期平缓减速的非对称饱和生长。

### 3.2 传染病模型 (Epidemic Compartment Models)
- **SI 模型**：$\frac{di}{dt} = \lambda i (1 - i)$（Logistic 曲线）
- **SIS 模型**（可治愈复发）：
  $$\frac{di}{dt} = \lambda i (1 - i) - \mu i = \lambda i \left(1 - \frac{1}{\sigma} - i\right) \quad (\sigma = \frac{\lambda}{\mu})$$
  - **阈值定理**：若接触数 $\sigma = \lambda/\mu \le 1$，$i(t) \to 0$（疾病自愈消除）；若 $\sigma > 1$，$i(t) \to 1 - \frac{1}{\sigma}$（地方病平衡稳态）。
- **SIR 模型**（具有免疫力移出）：
  $$\begin{cases} \frac{ds}{dt} = -\lambda s i \\ \frac{di}{dt} = \lambda s i - \mu i \\ \frac{dr}{dt} = \mu i \end{cases}$$
  - 相轨线方程：$i(s) = s_0 + i_0 - s + \frac{1}{\sigma} \ln\frac{s}{s_0}$
  - 最大感染人数峰值 $i_{\max} = s_0 + i_0 - \frac{1}{\sigma} (1 + \ln(\sigma s_0))$（发生在 $s = 1/\sigma$ 时）。
  - 最终未感染比例 $s_\infty$ 由超越方程决定：$s_0 - s_\infty + \frac{1}{\sigma}\ln\frac{s_\infty}{s_0} = 0$。

### 3.3 药代动力学房室模型 (Compartment Models)
- **单室/二室静脉注射与口服吸收**：
  $$\begin{cases} \frac{dc_1}{dt} = -(k_{12} + k_{13}) c_1 + \frac{V_2}{V_1} k_{21} c_2 + \frac{f_0(t)}{V_1} \\ \frac{dc_2}{dt} = \frac{V_1}{V_2} k_{12} c_1 - k_{21} c_2 \end{cases}$$
  - 浓度解呈现多指数衰减形式：$c_1(t) = A e^{-\alpha t} + B e^{-\beta t}$。
  - 通过半对数坐标图的“残数法”（Residual Method）分离快慢处置相速率常数 $\alpha, \beta$ 与表观分布容积。

### 3.4 兰彻斯特作战模型 (Lanchester Combat Model)
- **正规战争（远距离瞄准射击，平方律）**：
  $$\begin{cases} \frac{dx}{dt} = -a y \\ \frac{dy}{dt} = -b x \end{cases} \implies b(x_0^2 - x^2) = a(y_0^2 - y^2)$$
  - 优势判定条件：$b x_0^2 > a y_0^2 \iff \frac{y_0}{x_0} < \sqrt{\frac{b}{a}}$。人数的优势呈平方放大。
- **游击战争（近距离面积散射，线性律）**：
  $$\begin{cases} \frac{dx}{dt} = -c x y \\ \frac{dy}{dt} = -d x y \end{cases} \implies d(x_0 - x) = c(y_0 - y)$$
  - 优势判定条件：$d x_0 > c y_0$。兵力优势呈线性效应。

---

## 4. 稳定性理论与相平面分析

### 4.1 二维自治系统平衡点稳定性判据
对于非线性自治系统：
$$\begin{cases} \frac{dx}{dt} = f(x, y) \\ \frac{dy}{dt} = g(x, y) \end{cases}$$
令 $f(x_0, y_0) = g(x_0, y_0) = 0$ 求出平衡点 $P_0(x_0, y_0)$，计算平衡点处的 Jacobian 矩阵：
$$J = \begin{bmatrix} f_x & f_y \\ g_x & g_y \end{bmatrix}_{P_0}, \quad p = -\text{tr}(J) = -(f_x + g_y), \quad q = \det(J) = f_x g_y - f_y g_x$$
特征方程为 $\lambda^2 + p \lambda + q = 0$。

| 条件 | 特征值性质 | 平衡点类型 | 稳定性 |
|------|-----------|-----------|--------|
| $q < 0$ | 一正一负实根 | 鞍点 (Saddle) | 不稳定 |
| $q > 0, p > 0, p^2 - 4q > 0$ | 两负实根 | 稳定结点 (Stable Node) | 渐近稳定 |
| $q > 0, p < 0, p^2 - 4q > 0$ | 两正实根 | 不稳定结点 (Unstable Node) | 不稳定 |
| $q > 0, p > 0, p^2 - 4q < 0$ | 负实部共轭复根 | 稳定焦点 (Stable Focus) | 渐近稳定 |
| $q > 0, p < 0, p^2 - 4q < 0$ | 正实部共轭复根 | 不稳定焦点 (Unstable Focus) | 不稳定 |
| $q > 0, p = 0, p^2 - 4q < 0$ | 纯虚根 | 中心点 (Center) | 轨道稳定（线性近似下） |

### 4.2 捕食者-猎物 Volterra 模型
$$\begin{cases} \dot{x} = x(r_1 - a y) \\ \dot{y} = y(-r_2 + b x) \end{cases}$$
- 存在非零内平衡点 $(x_0, y_0) = (r_2/b, r_1/a)$，特征根为纯虚数 $\pm i\sqrt{r_1 r_2}$，相轨线为闭合族（守恒积分 $x^{r_2} e^{-bx} \cdot y^{r_1} e^{-ay} = C$）。
- 平均数量在一个周期内保持恒定 $\bar{x} = r_2/b, \bar{y} = r_1/a$。
- **Volterra 农药杀虫原理**：若同时对两物种同比例捕杀/喷洒农药（$r_1 \to r_1 - \varepsilon, -r_2 \to -r_2 - \varepsilon$），则害虫（猎物）平均数量 $\bar{x} = \frac{r_2+\varepsilon}{b}$ 反而上升，天敌 $\bar{y} = \frac{r_1-\varepsilon}{a}$ 下降。

### 4.3 种群竞争模型 (Species Competition)
$$\begin{cases} \dot{x_1} = r_1 x_1 \left(1 - \frac{x_1}{N_1} - \sigma_1 \frac{x_2}{N_2}\right) \\ \dot{x_2} = r_2 x_2 \left(1 - \sigma_2 \frac{x_1}{N_1} - \frac{x_2}{N_2}\right) \end{cases}$$
- $\sigma_1 < 1, \sigma_2 > 1$：物种 1 胜出，物种 2 灭绝；
- $\sigma_1 > 1, \sigma_2 < 1$：物种 2 胜出，物种 1 灭绝；
- $\sigma_1 < 1, \sigma_2 < 1$（种内竞争大于种间竞争）：两物种共存稳定平衡点 $P_3\left(\frac{N_1(1-\sigma_1)}{1-\sigma_1\sigma_2}, \frac{N_2(1-\sigma_2)}{1-\sigma_1\sigma_2}\right)$；
- $\sigma_1 > 1, \sigma_2 > 1$：双稳态，结果取决于初值。

---

## 5. 差分方程与离散动态系统

### 5.1 蛛网模型 (Cobweb Model) 与市场稳定
- 需求方程 $Q_d(k) = a - b P(k)$，供给方程 $Q_s(k) = -c + d P(k-1)$，市场出清 $Q_d(k) = Q_s(k)$。
- 价格差分方程：$P(k) = -\frac{d}{b} P(k-1) + \frac{a+c}{b}$
- **稳定性准则**：
  - $d/b < 1$（供给弹性小于需求弹性/供给曲线斜率绝对值大于需求曲线）：价格收敛至均衡点（收敛蛛网）；
  - $d/b > 1$：发散蛛网；$d/b = 1$：等幅振荡。

### 5.2 Logistic 差分方程与分岔、混沌
$$x_{k+1} = \mu x_k (1 - x_k), \quad x_k \in [0, 1]$$
- $1 < \mu < 3$：单稳定平衡点 $x^* = 1 - 1/\mu$；
- $3 < \mu < 1 + \sqrt{6} \approx 3.449$：发生周期倍化分岔（Period-doubling Bifurcation），出现稳定 2 周期轨道；
- 随着 $\mu$ 进一步增加，相继出现 $2^2, 2^3, \dots, 2^n$ 周期轨道；
- 当 $\mu > \mu_\infty \approx 3.5699$ 时，系统进入**混沌（Chaos）**状态，对初值极度敏感（Feigenbaum 常数 $\delta \approx 4.669$）。

### 5.3 Leslie 人口年龄结构模型
将种群划分为 $n$ 个年龄段，第 $k$ 步各年龄人口向量为 $\boldsymbol{x}(k) = [x_1(k), x_2(k), \dots, x_n(k)]^T$：
$$\boldsymbol{x}(k+1) = L \boldsymbol{x}(k), \quad L = \begin{bmatrix} b_1 & b_2 & \dots & b_{n-1} & b_n \\ s_1 & 0 & \dots & 0 & 0 \\ 0 & s_2 & \dots & 0 & 0 \\ \vdots & & \ddots & & \vdots \\ 0 & \dots & & s_{n-1} & 0 \end{bmatrix}$$
- 由 Perron-Frobenius 定理，$L$ 存在唯一的正实特征值 $\lambda_1$（谱半径）和正特征向量 $\boldsymbol{x}^*$：
  - 若 $\lambda_1 > 1$，人口指数增长；
  - 若 $\lambda_1 = 1$，人口规模保持稳定；
  - 若 $\lambda_1 < 1$，人口逐渐衰退；
  - 无论初始人口分布如何，各年龄段比例最终收敛于稳态年龄分布 $\boldsymbol{x}^* = \left[1, \frac{s_1}{\lambda_1}, \frac{s_1 s_2}{\lambda_1^2}, \dots, \frac{\prod_{i=1}^{n-1} s_i}{\lambda_1^{n-1}}\right]^T$。

---

## 6. 随机模型与马尔可夫链

### 6.1 报童问题 (Newsvendor Problem) 与随机存储
- 进货单价 $a$，售价 $b$，未售出残值 $c$（满足 $a < b$ 且 $c < a$），市场需求 $r$ 服从连续概率密度 $p(r)$。
- 目标：确定进货量 $n$ 最大化期望利润 $E[G(n)]$：
  $$G(n, r) = \begin{cases} (b-a)r - (a-c)(n-r), & r \le n \\ (b-a)n, & r > n \end{cases}$$
- **最优临界分位数准则**：
  $$P(r \le n^*) = \int_0^{n^*} p(r) dr = \frac{b - a}{b - c} = \frac{C_u}{C_u + C_o}$$
  （其中 $C_u = b - a$ 为缺货损失，$C_o = a - c$ 为超储损失）。

### 6.2 离散时间马尔可夫链 (Discrete-Time Markov Chain)
1. **稳态分布**：
   对于不可约非周期马氏链，转移概率矩阵为 $P$，稳态分布向量 $\boldsymbol{w} = [w_1, \dots, w_k]$ 满足：
   $$\boldsymbol{w} P = \boldsymbol{w}, \quad \sum_{i=1}^k w_i = 1$$
   平均返回时间（Mean Recurrence Time）为 $\mu_{ii} = 1/w_i$。
2. **吸收马氏链 (Absorbing Markov Chains)**：
   将转移矩阵写成分块标准型（前 $r$ 个为吸收态，后 $k-r$ 个为暂态）：
   $$P = \begin{bmatrix} I_{r\times r} & 0 \\ R & Q \end{bmatrix}$$
   - **基本矩阵**：$M = (I - Q)^{-1} = \sum_{s=0}^\infty Q^s$（元素 $m_{ij}$ 表示从暂态 $i$ 出发访问暂态 $j$ 的期望次数）
   - **平均吸收时间（步数）**：$\boldsymbol{y} = M \boldsymbol{e}$（$\boldsymbol{e} = [1, 1, \dots, 1]^T$）
   - **最终被各吸收态吸收的概率矩阵**：$F = M R$

---

## 7. 合作博弈与离散决策模型

### 7.1 合作博弈与 Shapley 值 (费用与收益公平分摊)
对于特征函数博弈 $(I, v)$，参与者集合 $I = \{1, 2, \dots, n\}$，联盟 $s \subseteq I$ 的价值为 $v(s)$。
- **Shapley 值计算公式**：
  $$\varphi_i(v) = \sum_{s \subseteq I \setminus \{i\}} \frac{|s|! (n - |s| - 1)!}{n!} [v(s \cup \{i\}) - v(s)]$$
- **公理化性质**：有效性（$\sum \varphi_i = v(I)$）、对称性、虚拟人公理、可加性。常用于公用工程供水/排污管道建设费用分摊、电网成本分摊、多方投资利益分配。

### 7.2 Raiffa 谈判解
在没有完整联盟特征函数时，通过确定冲突点 $b_i$（不合作时的损失上限），各方按相对议价能力逐步让步折中：
$$x_i = \frac{B}{n} + \frac{2n-3}{2n-1}\left(\frac{1}{n}\sum_{j=1}^n b_j - b_i\right)$$

### 7.3 社会选择与 Arrow 不可能定理
- **Borda 计分法**：$m$ 个候选对象，按每位选民排序赋予分值 $m-1, m-2, \dots, 0$ 进行累加，但可能受无关候选人影响。
- **Arrow 不可能定理**：当候选方案 $\ge 3$ 时，不存在同时满足“无限制范围、Pareto 最优、独立于无关备选项 (IIA)、非独裁性”的群体决策规则。建模中处理多准则/多主体偏好时必须明确偏好聚合的权衡。

---

## 8. 最优控制与变分法

### 8.1 变分法基础与 Euler-Lagrange 方程
泛函极值问题：$J[y] = \int_{x_0}^{x_1} F(x, y(x), y'(x)) dx$
极值必要条件为 Euler-Lagrange 方程：
$$F_y - \frac{d}{dx} F_{y'} = 0$$
- 若 $F$ 不显含 $x$（$F = F(y, y')$），则存在一阶积分（Beltrami 恒等式）：
  $$F - y' F_{y'} = C$$
  （典型应用：最速降线 Brachistochrone 问题，解为旋轮线/摆线）。

### 8.2 连续最优控制与 Pontryagin 极大值原理
系统状态方程 $\dot{x} = f(t, x, u)$，性能指标 $J = \int_0^T F(t, x, u) dt$。
构造 Hamilton 函数：
$$H(t, x, u, \lambda) = F(t, x, u) + \lambda(t) f(t, x, u)$$
最优控制轨线满足：
$$\begin{cases} \dot{x} = \frac{\partial H}{\partial \lambda} = f(t, x, u) \\ \dot{\lambda} = -\frac{\partial H}{\partial x} \\ \frac{\partial H}{\partial u} = 0 \quad (\text{或 } u^*(t) = \arg\max_{u \in U} H) \end{cases}$$
- 典型案例：Keller 赛跑最优体力分配模型（速度 $v(t)$ 与无氧储备 $E(t)$ 耦合，前段匀加速达极速，中段匀速，终点耗尽能量）。
