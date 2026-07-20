# 可视化图表保存规范

## 标准保存模式

**所有图表必须保存不弹窗**：

```python
import matplotlib.pyplot as plt
import os

# 创建输出目录
os.makedirs('figures', exist_ok=True)

# 绘图
plt.figure(figsize=(10, 6))
# ... 绑图代码 ...

# 保存不弹窗
plt.savefig('figures/chart.png', dpi=300, bbox_inches='tight')
plt.close()
```

**禁止 `plt.show()`** — 用户明确要求不弹窗。

## 中文字体渲染核验（交付前必做）

```python
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
plt.rcParams['axes.unicode_minus'] = False     # 解决负号显示

# 验证：生成测试图，检查中文是否正常显示
plt.figure(figsize=(6, 4))
plt.title('中文字体测试')
plt.xlabel('横轴标签')
plt.ylabel('纵轴标签')
plt.plot([1, 2, 3], [1, 4, 9])
plt.savefig('figures/font_test.png', dpi=150)
plt.close()
```

可用中文字体：SimHei（黑体）、Microsoft YaHei（微软雅黑）、SimSun（宋体）、KaiTi（楷体）。

## 图表命名规范

- **表题在上**：`表1 XX数据表`（表的上方）
- **图题在下**：`图1 XX示意图`（图的下方）
- 编号连续：全文图表分别从1开始连续编号
- 正文必须引用：`如表1所示`、`由图1可得`
- 所有图表必须有解读文字（2-4句）

## 图表类型选择

| 需求 | 推荐图表 | 适用场景 |
|------|---------|---------|
| 比较数值大小 | 柱状图/条形图 | 方案对比、排名展示 |
| 展示变化趋势 | 折线图 | 时间序列、预测结果 |
| 展示分布 | 直方图/箱线图 | 数据分布、异常值检测 |
| 展示关系 | 散点图 | 相关性、聚类结果 |
| 展示组成 | 饼图/堆叠柱状图 | 占比、组成分析 |
| 多维度对比 | 雷达图 | 综合评价结果 |
| 热力关系 | 热力图 | 相关系数、矩阵数据 |
| 展示流程 | 流程图/框图 | 模型架构、算法流程 |

## 配色方案建议

```python
# 方案1：专业蓝（推荐）
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B']

# 方案2：柔和色
colors = ['#4E79A7', '#F28E2B', '#E15759', '#76B7B2', '#59A14F']

# 方案3：渐变蓝
colors = plt.cm.Blues(np.linspace(0.3, 0.9, 5))
```

## 图表尺寸建议

| 图表类型 | 建议尺寸 (figsize) |
|---------|-------------------|
| 一般图表 | (10, 6) |
| 大型对比图 | (14, 8) |
| 雷达图 | (8, 8) |
| 热力图 | (10, 8) |
| 并排子图 | (16, 6) |
