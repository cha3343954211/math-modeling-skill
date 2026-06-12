# CUMCM 2011D：受限/稀疏模式池求解记录

## 触发场景

适用于天然肠衣搭配、装箱、切割库存、原料配组等问题：

- 聚合整数规划能给出很高上界，但逐捆/逐箱分解失败；
- 直接 CP-SAT 按“捆 × 长度档”建模，长时间只有 `UNKNOWN` 或搜索空间过大；
- 全枚举合法单捆模式导致模式数量爆炸，PuLP/CBC 写 MPS 或求解时内存爆炸；
- 需要先交付一个逐行可验证的高质量可行方案，而不是只报告理论上界。

## 本次稳定路线

对 2011D，最终可工作的路线是：

1. **先保留聚合模型作为上界筛查**：
   - 总长度上界：`floor(total_length / 88.5)`；
   - 聚合 MILP 可用于产生候选规格数量，但不能直接作为最终方案。
2. **生成受限合法单捆模式池**：
   - 每个模式本身必须满足：规格下限、根数范围、单捆长度 `[88.5, 89.5]`；
   - 长规格模式较少，可较充分生成；
   - 中/短规格组合爆炸，只生成随机+启发式筛选后的高质量模式池。
3. **主问题使用稀疏矩阵 MILP**：
   - 变量：每个模式采用次数；
   - 约束：各长度档使用量不超过库存；
   - 目标：大权重字典序 `总捆数 >> 长规格捆数 >> 中规格捆数`。
4. **避免 PuLP 全量大模式池**：
   - PuLP/CBC 会先写 MPS 文件，几十万模式时容易 `MemoryError`；
   - 大模式池优先用 `scipy.optimize.milp` + `scipy.sparse`，或分批/列生成。
5. **最终必须展开并独立验证**：
   - `final_matching_plan.csv`：逐捆配方；
   - `material_usage_by_length.csv`：各长度档使用与剩余；
   - `summary_by_spec.csv`：分规格统计；
   - `frozen_numbers.json`：论文冻结数字；
   - `validation_report.json`：逐捆长度、根数、规格下限、库存校验。

## 代码骨架

核心模式：

```python
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix

# pats = [(spec, vector_46), ...]
A = lil_matrix((46, len(pats)))
c = np.zeros(len(pats))
for j, (spec, v) in enumerate(pats):
    for i, q in enumerate(v):
        if q:
            A[i, j] = q
    c[j] = -(1_000_000 + (10_000 if spec == 'L' else 100 if spec == 'M' else 0))

constraints = LinearConstraint(A.tocsr(), np.zeros(46), counts)
res = milp(
    c,
    integrality=np.ones(len(pats)),
    bounds=Bounds(np.zeros(len(pats)), np.full(len(pats), np.inf)),
    constraints=constraints,
    options={'time_limit': 80, 'mip_rel_gap': 0.02},
)
```

## 写论文时的表述边界

- 若只证明了长度上界或聚合上界，不得写“最优方案”；只能写“理论/聚合上界”。
- 只有逐捆表通过校验后，才能写“可执行搭配方案”。
- 若受限模式池未证明全局最优，应写“高质量可行解/可复现可执行方案”，并说明未来可用列生成增强最优性证明。

## 2011D 本次可复用数字口径

本次稳定验证过的方案口径为：

- 总捆数：191；
- 长规格：130；中规格：47；短规格：14；
- 使用：1302 根，17001.0 m；
- 剩余：21 根，169.5 m；
- 单捆长度：88.5--89.5 m；
- 验证错误数：0。

这些数字属于本次题目数据，不要作为其他题目的固定结论；可作为测试实现是否复现的参考。
