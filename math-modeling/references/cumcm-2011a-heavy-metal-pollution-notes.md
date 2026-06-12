# CUMCM 2011A 城市表层土壤重金属污染分析案例

## 适用触发

当题目涉及城市/土壤/沉积物重金属污染、空间分布、功能区污染评价、污染来源识别、污染源定位时，可参考本案例。典型关键词：`重金属`、`背景值`、`功能区`、`PCA源解析`、`污染源位置`、`生态风险`。

## 数据结构

2011A 附件常见结构：

- 附件1：采样点编号、`x(m)`、`y(m)`、海拔、功能区。功能区：1生活区、2工业区、3山区、4交通区、5公园绿地区。
- 附件2：As、Cd、Cr、Cu、Hg、Ni、Pb、Zn 八种元素浓度。注意 Cd/Hg 常为 `ng/g`，其他多为 `μg/g`，与背景值同单位比较即可。
- 附件3：各元素背景均值、标准偏差、范围。

读取 Excel 时一般需要跳过前两行说明，可用：

```python
loc = pd.read_excel(file, sheet_name='附件1', header=2, usecols=[0,1,2,3,4])
conc = pd.read_excel(file, sheet_name='附件2', header=2, usecols=list(range(9)))
bg = pd.read_excel(file, sheet_name='附件3', header=2, usecols=[0,1,2,3])
```

## 推荐模型链

### 1. 污染程度评价

Baseline：单因子累积倍数

\[
C_f^{ij}=C_{ij}/B_j
\]

主模型：内梅罗综合污染指数

\[
P_N^i=\sqrt{\frac{(\overline{C_f^i})^2+(C_{f,\max}^i)^2}{2}}
\]

生态风险补充：Hakanson 潜在生态风险指数

\[
E_r^{ij}=T_j C_f^{ij},\quad RI_i=\sum_jE_r^{ij}
\]

常用毒性响应系数：As=10、Cd=30、Cr=2、Cu=5、Hg=40、Ni=5、Pb=5、Zn=1。

输出：

- 8 种元素相对背景值的空间分布图；
- 综合污染指数 PN 空间图；
- 按功能区统计的平均 PN、最大 PN、平均 RI、最大 RI；
- 元素平均/最大累积倍数表。

### 2. 污染原因识别

Baseline：元素相关系数矩阵 + 功能区均值对比。

主模型：`log1p(浓度)` 后 Z-score 标准化，再做 PCA。

解释方式：

- PC1 若由 Cu/Zn/Pb/Cd 等主导，常解释为工业排放、交通磨损、建筑/城市活动复合源；
- Ni/As/Cr 组合可能包含自然母质背景与低强度人为扰动；
- Hg/As/Pb 局部高载荷可对应燃煤沉降、生活源或特殊点源。

用 KMeans 污染谱聚类作验证，K 可由轮廓系数选择。聚类图要叠加功能区，避免只给统计结果而没有现实解释。

### 3. 传播特征与污染源定位

不要简单把最高浓度点等同于污染源。推荐双证据定位：

1. 将 PCA 因子得分看作对应污染因子的空间响应强度，用 IDW 插值得到连续场，寻找局部极大值作为候选源；
2. 筛选高 RI 或高 PN 样点，用 DBSCAN 识别热点簇，以 RI 加权中心作为候选源交叉验证。

IDW 公式：

\[
\hat z(s)=\frac{\sum_i z(s_i)d(s,s_i)^{-p}}{\sum_i d(s,s_i)^{-p}},\quad p=2
\]

候选源表至少包含：因子、候选源序号、x、y、因子场强度、主导元素、邻近主要功能区、邻近样点编号。

### 4. 稳健性与模型评价

背景值是关键参数。建议做统一扰动敏感性：背景值乘以 0.8--1.2，重新计算 PN/RI，观察：

- 功能区污染排序是否稳定；
- 平均 PN/RI 如何变化；
- 高风险点数量如何变化。

若排序稳定，可写“相对污染格局稳定”；若高风险点数变化明显，应说明绝对风险等级对背景值敏感。

## 论文写作要点

- 问题一不要只给空间图：必须给功能区污染排序和元素累积倍数解释。
- 问题二不要只说 PCA：必须把主成分载荷、功能区分布和可能来源对应起来。
- 问题三不要声称精确污染源：在缺少风场、径流、企业排放清单时，只能给“候选源/影响中心”。
- 问题四要明确需要补充的信息：多年重复采样、风向风速、降雨径流、土地利用、道路车流量、工业企业排放清单、土壤 pH/有机质/粒径等。
- 后续演变模型可写对流—扩散—沉降模型：

\[
\frac{\partial C_j}{\partial t}=D_j\nabla^2C_j-\mathbf v\cdot\nabla C_j-k_jC_j+S_j(x,y,t)
\]

## 可复现代码骨架

```python
import numpy as np, pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from scipy.spatial import cKDTree

ELEMENTS = ['As','Cd','Cr','Cu','Hg','Ni','Pb','Zn']
TOX = {'As':10,'Cd':30,'Cr':2,'Cu':5,'Hg':40,'Ni':5,'Pb':5,'Zn':1}

# Cf / PN / RI
for e in ELEMENTS:
    df[f'{e}_Cf'] = df[e] / bg_mean[e]
    df[f'{e}_Er'] = TOX[e] * df[f'{e}_Cf']
cf_cols = [f'{e}_Cf' for e in ELEMENTS]
df['PN'] = np.sqrt((df[cf_cols].mean(axis=1)**2 + df[cf_cols].max(axis=1)**2)/2)
df['RI'] = df[[f'{e}_Er' for e in ELEMENTS]].sum(axis=1)

# PCA
X = StandardScaler().fit_transform(np.log1p(df[ELEMENTS]))
pca = PCA(n_components=4, random_state=42).fit(X)
scores = pca.transform(X)
loadings = pd.DataFrame(pca.components_.T, index=ELEMENTS)
```

## 常见陷阱

- `Cd`、`Hg` 单位不同不需要强制转成 μg/g，只要实测值和背景值单位一致；若跨元素比较原始浓度则必须说明单位不可直接比。
- 极端样点会强烈影响空间图和 PCA，PCA 前建议 `log1p`。
- IDW 是描述性插值，不等于真实扩散机制；论文中要把“候选污染源”与“确定污染源”区分开。
- 参考文献中的 `[1]` 直接写在 LaTeX 段首可能被解析为可选参数导致 `Illegal unit of measure`；用 `enumerate[label={[\arabic*]}]` 或 BibTeX 管理参考文献。
- 使用 antiword 提取 `.doc` 题面时，输出可能已是 UTF-8；不要盲目再按 GBK 转码。
